# 恢复顺序

先恢复基线，再覆盖后列增量。零文件包无需复制；每个包的 data 复制到对应 source。

## windows

1. `codex-home/data` → `C:\Users\klsm\.codex` 
2. `codex-desktop-roaming/data` → `C:\Users\klsm\AppData\Roaming\Codex` 
3. `codex-store-appdata/data` → `C:\Users\klsm\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0` 
4. `codex-documents/data` → `C:\Users\klsm\Documents\Codex` 
5. `downloads-sun2/data` → `C:\Users\klsm\Downloads\sun2` 
6. `workspace-tools-rootfiles/data` → `D:\workspace_tools` 
7. `workspace-tools-project-01/data` → `D:\workspace_tools\AI Leaning` 
8. `workspace-tools-project-02/data` → `D:\workspace_tools\Exam` 
9. `workspace-tools-project-03/data` → `D:\workspace_tools\Test Case Review and Update` 
10. `workspace-tools-project-04/data` → `D:\workspace_tools\nanoclaw` 
11. `workspace-tools-project-05/data` → `D:\workspace_tools\personal health check` 
12. `workspace-tools-project-06/data` → `D:\workspace_tools\sun2` 
13. `workspace-tools-project-07/data` → `D:\workspace_tools\wangyifan` 
14. `workspace-tools-project-08/data` → `D:\workspace_tools\webpage_to_word_preserver_v8` 
15. `workspace-tools-project-09/data` → `D:\workspace_tools\west-kowloon-website-performance-api-2026-06-22` 
16. `workspace-tools-project-10/data` → `D:\workspace_tools\workout` 
17. `workspace-tools-project-11/data` → `D:\workspace_tools\压测` 
18. `workspace-tools-project-12/data` → `D:\workspace_tools\学生考卷和作业生成_数学` 
19. `workspace-tools-project-13/data` → `D:\workspace_tools\学生考卷和作业生成_英语` 
20. `workspace-tools-project-14/data` → `D:\workspace_tools\music` 
21. `delta-20261022-codex-home/data` → `C:\Users\klsm\.codex` （增量覆盖）
22. `delta-20261022-codex-store-appdata/data` → `C:\Users\klsm\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0` （增量覆盖）
23. `delta-20261022-codex-documents/data` → `C:\Users\klsm\Documents\Codex` （增量覆盖）
24. `delta-20261022-workspace-tools-project-02/data` → `D:\workspace_tools\Exam` （增量覆盖）
25. `supplement-workspace-uncommitted-20261022/data` → `D:\Workspace` （先克隆原 Workspace 仓库，再复制这些未提交文件）
26. `supplement-nanoclaw-codex-home-20261022/data` → `C:\Users\klsm\AppData\Local\NanoClaw\codex-home` 
27. `supplement-workspace-ignored-data-20261022/data` → `D:\Workspace` 
28. `supplement-claude-windows-home-20261022/data` → `C:\Users\klsm\.claude` 

## wsl

1. `supplement-wsl-nanoclaw-20261022/data` → `/home/klsm/nanoclaw` 
2. `supplement-wsl-user-service-20261022/data` → `/home/klsm/.config/systemd/user` 
3. `supplement-claude-wsl-home-20261022/data` → `/home/klsm/.claude` 
