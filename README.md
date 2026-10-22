# Codex 换机迁移备份

这是 `evon4555/klsm_others_backup` 私有迁移仓库。原电脑的 `D:\Workspace` 按用户要求继续使用 `evon4555/klsm_workspace`，不包含在本次备份。

**数据以 AES-256-GCM 加密分卷保存于本仓库的 Releases 附件，Git 仓库保存恢复工具、校验清单和说明。仅下载仓库 ZIP 或 git clone 不会下载迁移数据。**

恢复密钥不在 GitHub，必须由本人从旧电脑另行带走。密钥丢失无法恢复。请保持仓库私有；不要把恢复密钥提交进仓库。

## 恢复步骤

**优先阅读 [新电脑恢复说明](新电脑恢复说明.md)。** 2026-10-22 已补存未提交工作区文件、NanoClaw 的 WSL 部署、独立 Codex 数据及当天增量。还原时先基线、再增量；Linux 包应在 WSL 中单独恢复。恢复工具默认按当前平台筛选。

无需安装 GitHub CLI 也可使用自带的 `download_backup.py` 下载；它通过已有 Git/GitHub 登录授权，支持校验已有分卷、断点续传和重试。示例：

```powershell
python download_backup.py --assets D:\Codex备份分卷
```

1. 从旧电脑另存 `恢复密钥_请单独保存.json`，建议保存到加密移动硬盘或密码管理器的安全附件。不要把密钥上传 GitHub。
2. 克隆本仓库或下载其代码 ZIP，安装 Python 3.10+ 和依赖：

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. 安装并登录 GitHub CLI 后下载本次 Release 的全部 `.cbx` 附件（或从 Releases 页面下载）：

   ```powershell
   gh auth login
   gh release download migration-2026-10-21 --repo evon4555/klsm_others_backup --pattern "*.cbx" --dir .\assets
   ```

4. 解密到一个新的中转目录。此工具不会自动覆盖新电脑的 Codex 或项目目录：

   ```powershell
   python restore_backup.py --manifest .\backup-manifest.json --assets .\assets --key-file "E:\恢复密钥_请单独保存.json" --output "D:\Codex迁移中转"
   ```

   可加 `--package codex-home` 先恢复 Codex 核心数据；可加 `--verify-only` 仅检验，不提取文件。每一分卷和每一个恢复文件都会校验 SHA-256；加密认证失败会中止。

5. 根据 `backup-manifest.json` 的 `source` 字段，把各包恢复目录里的 `data` 内容复制回原位置。`backup-manifest.json`（包内文件）记录原文件路径、哈希、排除项、错误、警告和快照时间，供逐项检查。
6. 恢复 `.codex` 和应用数据前先完全退出 Codex，保留新机已有数据副本。尽量沿用原盘符和路径；用户名变化后检查配置中的绝对路径。重新登录 Codex 和所需的外部服务。
7. 安装项目运行环境，核对聊天、归档、附件、记忆、技能、项目文件。**通过新机验收后再清空旧电脑。**

## 范围与限制

- 包括 `.codex` 中的会话、归档、记忆、技能、配置与状态；桌面应用可迁移的用户数据；`D:\workspace_tools` 下的项目和产物；`Documents\Codex`；`Downloads\sun2`。
- 排除已识别的登录凭据文件、私钥、`.env` 等认证文件；排除浏览器数据、缓存、沙盒运行组件、虚拟环境、`node_modules` 等可重装内容。依赖目录链接不追踪，需重新安装。
- 文档、脚本和历史会话可能含嵌入式敏感信息，因此所有源文件均放入加密数据包，仓库中不明文展开这些内容。
- SQLite 数据库通过 SQLite 在线备份接口生成快照，并进行 `quick_check`；同名 WAL/SHM 不作为独立恢复文件。其他文件按各包记录的时间读取。不同包不是同一瞬间的全机快照，当前聊天后续消息不在较早快照中。
- Windows 登录状态、文件 ACL、目录链接、独立 WSL/Docker 内部数据不在本次可迁移内容内。空目录可能不保留。应用数据跨版本兼容性和新机业务可用性需另行验收。
- 具体完成状态、文件数、体积、错误与警告以最终 `backup-manifest.json` 和 `BACKUP_REPORT.md` 为准；有错误项时不得视作完整备份。

大文件使用 Releases 附件，避免占用普通 Git 对象或 Git LFS 配额。GitHub 官方说明：每个附件小于 2 GiB、每个 Release 最多 1000 个附件：[About releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)。
