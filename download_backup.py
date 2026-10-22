"""Download selected encrypted backup parts with retries, resumption and SHA-256 checks."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import threading
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

LOCAL = threading.local()

def sha256_file(path):
    h = hashlib.sha256()
    with path.open('rb') as inp:
        while block := inp.read(4 * 1024 * 1024):
            h.update(block)
    return h.hexdigest()

def authorization():
    token = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    if not token and shutil.which('gh'):
        result = subprocess.run(['gh', 'auth', 'token', '--hostname', 'github.com'],
                                capture_output=True, text=True)
        if result.returncode == 0:
            token = result.stdout.strip()
    if not token and shutil.which('git'):
        env = dict(os.environ, GIT_TERMINAL_PROMPT='0', GCM_INTERACTIVE='never')
        result = subprocess.run(['git', '-c', 'credential.interactive=never', 'credential', 'fill'],
                                input='protocol=https\nhost=github.com\n\n', capture_output=True,
                                text=True, timeout=30, env=env)
        if result.returncode == 0:
            fields = dict(line.split('=', 1) for line in result.stdout.splitlines() if '=' in line)
            token = fields.get('password')
    if not token:
        raise RuntimeError('GitHub login unavailable. Sign in with Git or GitHub CLI first.')
    return token

def client(token):
    if not hasattr(LOCAL, 'session'):
        s = requests.Session()
        s.headers.update({'Authorization': 'Bearer ' + token, 'User-Agent': 'Codex-Backup-Recovery',
                          'X-GitHub-Api-Version': '2022-11-28'})
        retry = Retry(total=5, backoff_factor=1, allowed_methods=('GET', 'HEAD'),
                      status_forcelist=(429, 500, 502, 503, 504))
        s.mount('https://', HTTPAdapter(max_retries=retry))
        LOCAL.session = s
    return LOCAL.session

def download_part(part, folder, repository, token):
    target = folder / part['name']
    partial = target.with_suffix(target.suffix + '.partial')
    if target.exists() and target.stat().st_size == part['bytes'] and sha256_file(target) == part['sha256']:
        return 'verified_existing'
    s = client(token)
    for attempt in range(1, 6):
        try:
            if partial.exists() and partial.stat().st_size > part['bytes']:
                partial.unlink()
            offset = partial.stat().st_size if partial.exists() else 0
            if offset != part['bytes']:
                headers = {'Accept': 'application/octet-stream'}
                if offset:
                    headers['Range'] = f'bytes={offset}-'
                url = f"https://api.github.com/repos/{repository}/releases/assets/{part['asset_id']}"
                with s.get(url, headers=headers, stream=True, timeout=(30, 180)) as response:
                    if response.status_code not in (200, 206):
                        raise RuntimeError('Download HTTP ' + str(response.status_code))
                    if response.status_code == 206:
                        expected_prefix = f'bytes {offset}-'
                        if not response.headers.get('Content-Range', '').startswith(expected_prefix):
                            raise ValueError('Unexpected resumed Content-Range')
                    else:
                        offset = 0
                    with partial.open('ab' if offset else 'wb') as out:
                        for block in response.iter_content(1024 * 1024):
                            if block:
                                out.write(block)
            if partial.stat().st_size != part['bytes'] or sha256_file(partial) != part['sha256']:
                partial.unlink()
                raise ValueError('Downloaded SHA-256 or size mismatch')
            partial.replace(target)
            return 'downloaded_and_verified'
        except Exception:
            if attempt == 5:
                raise
            time.sleep(min(attempt * 3, 15))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, default=Path(__file__).with_name('backup-manifest.json'))
    parser.add_argument('--assets', type=Path, required=True)
    parser.add_argument('--package', action='append', help='Repeat to select several packages; default all')
    parser.add_argument('--workers', type=int, default=2, choices=range(1, 5))
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding='utf-8-sig'))
    packages = [p for p in manifest['packages'] if not args.package or p['id'] in args.package]
    if not packages or (args.package and set(args.package) - {p['id'] for p in packages}):
        raise ValueError('Unknown package selection')
    parts = [part for package in packages for part in package['parts']]
    args.assets.mkdir(parents=True, exist_ok=True)
    token = authorization()
    done = 0
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(download_part, p, args.assets, manifest['repository'], token): p for p in parts}
        for future in as_completed(futures):
            result = future.result()
            done += 1
            print(json.dumps({'part': futures[future]['name'], 'result': result,
                              'done': done, 'total': len(parts)}), flush=True)

if __name__ == '__main__':
    main()
