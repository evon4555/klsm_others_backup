# 迁移备份与恢复验证报告

- 私有仓库：`evon4555/klsm_others_backup`；Release：`migration-2026-10-21`。
- 共 29 个包、252 个加密分卷，压缩后约 30.98 GB。
- 共 52,525 条归档文件记录（包含增量版本，不等于去重后的文件总数）。
- 原始基线 20 包保留，含全部音乐；另补充 9 包，约 395 MB。
- 所有归档文件均在本地读取并核对 SHA-256；加密分卷做过解密往返验证。
- 所有远程分卷均核对 GitHub 的 SHA-256 和大小。
- 实际从 GitHub 下载完整 Codex 核心基线和当天增量，解密并还原 2266 + 243 条文件记录。
- 合并增量后，6 个 SQLite 数据库 quick_check 均通过；历史、技能、记忆、配置存在，auth.json 未包含。
- 随身目录中的密钥实际参与恢复测试，且其副本与原件哈希一致。
- 下载器已验证断点续传、服务器忽略 Range 时从头下载、错误哈希拒绝交付；恢复器验证在线数据库和错误密钥拒绝恢复。
- 新物理机上的 Codex 启动、登录、界面展示及项目运行仍需新机验收。

## 备份范围

| 包 | 原位置 | 文件记录 | 压缩后 GB | 目标 |
| --- | --- | ---: | ---: | --- |
| codex-home | `C:\Users\klsm\.codex` | 2266 | 1.288 | windows |
| codex-desktop-roaming | `C:\Users\klsm\AppData\Roaming\Codex` | 17 | 0.000 | windows |
| codex-store-appdata | `C:\Users\klsm\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0` | 146 | 0.022 | windows |
| codex-documents | `C:\Users\klsm\Documents\Codex` | 3447 | 0.348 | windows |
| downloads-sun2 | `C:\Users\klsm\Downloads\sun2` | 1518 | 0.345 | windows |
| workspace-tools-rootfiles | `D:\workspace_tools` | 4 | 0.000 | windows |
| workspace-tools-project-01 | `D:\workspace_tools\AI Leaning` | 150 | 0.033 | windows |
| workspace-tools-project-02 | `D:\workspace_tools\Exam` | 4085 | 0.671 | windows |
| workspace-tools-project-03 | `D:\workspace_tools\Test Case Review and Update` | 3 | 0.001 | windows |
| workspace-tools-project-04 | `D:\workspace_tools\nanoclaw` | 6 | 0.000 | windows |
| workspace-tools-project-05 | `D:\workspace_tools\personal health check` | 4 | 0.002 | windows |
| workspace-tools-project-06 | `D:\workspace_tools\sun2` | 4029 | 0.381 | windows |
| workspace-tools-project-07 | `D:\workspace_tools\wangyifan` | 560 | 0.163 | windows |
| workspace-tools-project-08 | `D:\workspace_tools\webpage_to_word_preserver_v8` | 0 | 0.000 | windows |
| workspace-tools-project-09 | `D:\workspace_tools\west-kowloon-website-performance-api-2026-06-22` | 27 | 0.001 | windows |
| workspace-tools-project-10 | `D:\workspace_tools\workout` | 2 | 0.000 | windows |
| workspace-tools-project-11 | `D:\workspace_tools\压测` | 27992 | 2.114 | windows |
| workspace-tools-project-12 | `D:\workspace_tools\学生考卷和作业生成_数学` | 267 | 0.031 | windows |
| workspace-tools-project-13 | `D:\workspace_tools\学生考卷和作业生成_英语` | 212 | 0.043 | windows |
| workspace-tools-project-14 | `D:\workspace_tools\music` | 1192 | 25.141 | windows |
| delta-20261022-codex-home | `C:\Users\klsm\.codex` | 243 | 0.111 | windows |
| delta-20261022-codex-store-appdata | `C:\Users\klsm\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0` | 7 | 0.002 | windows |
| delta-20261022-codex-documents | `C:\Users\klsm\Documents\Codex` | 1 | 0.004 | windows |
| delta-20261022-workspace-tools-project-02 | `D:\workspace_tools\Exam` | 2 | 0.000 | windows |
| supplement-workspace-uncommitted-20261022 | `D:\Workspace` | 24 | 0.010 | windows |
| supplement-nanoclaw-codex-home-20261022 | `C:\Users\klsm\AppData\Local\NanoClaw\codex-home` | 198 | 0.027 | windows |
| supplement-wsl-nanoclaw-20261022 | `/home/klsm/nanoclaw` | 4981 | 0.070 | wsl |
| supplement-wsl-user-service-20261022 | `/home/klsm/.config/systemd/user` | 8 | 0.000 | wsl |
| supplement-workspace-ignored-data-20261022 | `D:\Workspace` | 1134 | 0.171 | windows |

## 范围与未包含项

- D:\Workspace 全量继续使用 klsm_workspace；这次仅额外加密保存 24 个未提交/未跟踪文件，没有向原公开仓库提交变更。
- 另加密保存被 Git 忽略的源资料、应用数据和测试证据；排除依赖目录及 Git 嵌套备份，不影响原工作区。
- NanoClaw 实际部署、用户服务和独立 Windows Codex 数据已补存；原运行服务未被停止、重启或修改，没有发送对外测试消息。
- .env、私钥、OAuth 等已识别认证文件与浏览器数据未上传，需本人重新配置。
- 安装依赖、运行时和缓存可重装；WSL 整机、Docker 镜像和两个 Prometheus 卷内历史数据未导出。
- 增量先后覆盖顺序记录在 restore_order 中；新增/变化文件被保存，不自动删除基线中后来消失的文件。
- 源文件、数据库按各包记录的时间采集，不是同一瞬间的整机镜像。零文件包只有元数据，无需复制 data。
- 原始基线仍有下列 4 个系统锁定文件未读取：
- `C:\Users\klsm\.codex\.codex-provisioning-d886ec195a62e599.guard`：PermissionError。未包含在备份中。
- `C:\Users\klsm\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\Settings/settings.dat`：PermissionError。未包含在备份中。
- `C:\Users\klsm\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\Settings/settings.dat.LOG1`：PermissionError。未包含在备份中。
- `C:\Users\klsm\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\Settings/settings.dat.LOG2`：PermissionError。未包含在备份中。

## 交付

- 以《新电脑恢复说明.md》为主线。Git clone 或仓库 ZIP 不包含加密分卷，需另行下载 Releases 附件。
- 本机“换机随身包_不要上传Git”含密钥、工具和清单，只复制到本人保管的介质，不上传整个目录。
- 恢复全部数据建议预留约 100 GB 空间。新机验收通过后再清空旧电脑。
