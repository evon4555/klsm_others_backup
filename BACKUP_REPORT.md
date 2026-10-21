# 备份完成与校验报告

- 私有仓库：`evon4555/klsm_others_backup`
- Release：`migration-2026-10-21`
- 数据包：20 个；加密分卷：242 个。
- 已备份文件：45,927 个；压缩后数据约 30.58 GB。
- 读取失败：4 项；源文件变化警告：0 项。具体项见下方。
- 每个已归档文件的 SHA-256 已在本地解压读取校验。
- 每个分卷已通过本地加密/解密往返校验，并与 GitHub 返回的 SHA-256 和大小比对。
- 已从 GitHub 实际下载桌面设置包，完成解密、还原与 17 个文件的 SHA-256 校验。
- 实际新电脑上的 Codex 启动、历史会话展示和项目运行尚未验证。
- 恢复密钥仅在旧电脑本次归档目录，未上传；换机前必须另外保存。
- 不包含 D:\Workspace；不包含 WSL/Docker 内部数据、认证文件、浏览器数据及可重装环境。
- 本次迁移任务自身的工作目录整体排除，以免递归备份；恢复工具与最终报告单独保存在仓库。

| 包 | 原目录 | 文件数 | 压缩后 GB | 读取失败 | 变化警告 |
| --- | --- | ---: | ---: | ---: | ---: |
| codex-home | `C:\Users\klsm\.codex` | 2266 | 1.288 | 1 | 0 |
| codex-desktop-roaming | `C:\Users\klsm\AppData\Roaming\Codex` | 17 | 0.000 | 0 | 0 |
| codex-store-appdata | `C:\Users\klsm\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0` | 146 | 0.022 | 3 | 0 |
| codex-documents | `C:\Users\klsm\Documents\Codex` | 3447 | 0.348 | 0 | 0 |
| downloads-sun2 | `C:\Users\klsm\Downloads\sun2` | 1518 | 0.345 | 0 | 0 |
| workspace-tools-rootfiles | `D:\workspace_tools` | 4 | 0.000 | 0 | 0 |
| workspace-tools-project-01 | `D:\workspace_tools\AI Leaning` | 150 | 0.033 | 0 | 0 |
| workspace-tools-project-02 | `D:\workspace_tools\Exam` | 4085 | 0.671 | 0 | 0 |
| workspace-tools-project-03 | `D:\workspace_tools\Test Case Review and Update` | 3 | 0.001 | 0 | 0 |
| workspace-tools-project-04 | `D:\workspace_tools\nanoclaw` | 6 | 0.000 | 0 | 0 |
| workspace-tools-project-05 | `D:\workspace_tools\personal health check` | 4 | 0.002 | 0 | 0 |
| workspace-tools-project-06 | `D:\workspace_tools\sun2` | 4029 | 0.381 | 0 | 0 |
| workspace-tools-project-07 | `D:\workspace_tools\wangyifan` | 560 | 0.163 | 0 | 0 |
| workspace-tools-project-08 | `D:\workspace_tools\webpage_to_word_preserver_v8` | 0 | 0.000 | 0 | 0 |
| workspace-tools-project-09 | `D:\workspace_tools\west-kowloon-website-performance-api-2026-06-22` | 27 | 0.001 | 0 | 0 |
| workspace-tools-project-10 | `D:\workspace_tools\workout` | 2 | 0.000 | 0 | 0 |
| workspace-tools-project-11 | `D:\workspace_tools\压测` | 27992 | 2.114 | 0 | 0 |
| workspace-tools-project-12 | `D:\workspace_tools\学生考卷和作业生成_数学` | 267 | 0.031 | 0 | 0 |
| workspace-tools-project-13 | `D:\workspace_tools\学生考卷和作业生成_英语` | 212 | 0.043 | 0 | 0 |
| workspace-tools-project-14 | `D:\workspace_tools\music` | 1192 | 25.141 | 0 | 0 |

## 读取失败与变化警告

- `C:\Users\klsm\.codex\.codex-provisioning-d886ec195a62e599.guard`：PermissionError。未包含在备份中。
- `C:\Users\klsm\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\Settings/settings.dat`：PermissionError。未包含在备份中。
- `C:\Users\klsm\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\Settings/settings.dat.LOG1`：PermissionError。未包含在备份中。
- `C:\Users\klsm\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\Settings/settings.dat.LOG2`：PermissionError。未包含在备份中。

## 主动排除项

已识别的凭据、私钥、环境密钥文件，以及缓存、浏览器数据、运行时和依赖目录未上传。每个加密包内的 backup-manifest.json 保存详细路径和原因。这是一份带明确排除项的可迁移备份，不是整机镜像。
