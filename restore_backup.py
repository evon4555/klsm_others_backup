"""Verify/decrypt migration assets and extract to a NEW staging directory."""
import argparse
import base64
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import zipfile
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

MAGIC = b'CBX1'

def read_key(path):
    obj = json.loads(Path(path).read_text(encoding='utf-8'))
    key = base64.b64decode(obj['key_base64'], validate=True)
    if len(key) != 32:
        raise ValueError('Expected a 256-bit recovery key')
    return key

def decrypt_part(path, expected, key):
    data = Path(path).read_bytes()
    if hashlib.sha256(data).hexdigest() != expected['sha256']:
        raise ValueError('Encrypted asset checksum mismatch: ' + path.name)
    if data[:4] != MAGIC:
        raise ValueError('Unknown encrypted backup format')
    return AESGCM(key).decrypt(data[4:16], data[16:], path.name.encode('utf-8'))

def verify_extract(archive, destination, verify_only=False):
    destination = Path(destination)
    if not verify_only and destination.exists():
        raise ValueError('Restore destination must not exist: ' + str(destination))
    with zipfile.ZipFile(archive) as z:
        names = set(z.namelist())
        manifest = json.loads(z.read('metadata/manifest.json'))
        for item in manifest['files']:
            rel = Path(item['path'])
            if rel.is_absolute() or '..' in rel.parts or rel.drive:
                raise ValueError('Unsafe archived path')
            name = 'data/' + rel.as_posix()
            if name not in names:
                raise ValueError('Missing archived file: ' + name)
            info = z.getinfo(name)
            if info.file_size != item['bytes']:
                raise ValueError('Archived size mismatch: ' + name)
            h = hashlib.sha256()
            out = None
            try:
                if not verify_only:
                    target = destination / 'data' / rel
                    if not target.resolve().is_relative_to(destination.resolve()):
                        raise ValueError('Unsafe resolved archive path')
                    target.parent.mkdir(parents=True, exist_ok=True)
                    out = target.open('xb')
                with z.open(name) as inp:
                    while block := inp.read(1024 * 1024):
                        h.update(block)
                        if out:
                            out.write(block)
            finally:
                if out:
                    out.close()
            if h.hexdigest() != item['sha256']:
                raise ValueError('Restored checksum mismatch: ' + name)
            if not verify_only:
                stamp = item.get('source_mtime_ns')
                if stamp is not None:
                    os.utime(target, ns=(stamp, stamp))
        if not verify_only:
            destination.mkdir(parents=True, exist_ok=True)
            (destination / 'backup-manifest.json').write_text(
                json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    return len(manifest['files'])

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', required=True, type=Path)
    parser.add_argument('--assets', required=True, type=Path)
    parser.add_argument('--key-file', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--package')
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    key = read_key(args.key_file)
    manifest = json.loads(args.manifest.read_text(encoding='utf-8'))
    args.output.mkdir(parents=True, exist_ok=True)
    packages = [p for p in manifest['packages'] if not args.package or p['id'] == args.package]
    if not packages:
        raise ValueError('No matching backup package')
    for package in packages:
        dest = args.output / package['id']
        if not args.verify_only and dest.exists():
            raise ValueError('Restore destination already exists: ' + str(dest))
        archive = args.output / (package['id'] + '.verified.zip')
        if archive.exists():
            raise ValueError('Temporary archive already exists: ' + str(archive))
        h = hashlib.sha256()
        with archive.open('xb') as out:
            for part in package['parts']:
                plain = decrypt_part(args.assets / part['name'], part, key)
                h.update(plain)
                out.write(plain)
        if h.hexdigest() != package['zip_sha256']:
            raise ValueError('Combined archive checksum mismatch')
        count = verify_extract(archive, dest, args.verify_only)
        archive.unlink()
        print(json.dumps({'package': package['id'], 'verified_files': count,
                          'extracted': not args.verify_only}), flush=True)

if __name__ == '__main__':
    main()
