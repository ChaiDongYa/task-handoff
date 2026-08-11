# task-handoff

一个用于跨 Codex 账号或设备续接本地任务的 Skill。

它会在项目中创建可共享的交接记录，包含任务目标、已完成内容、重要文件、决策与下一步。它还会自动维护 `.codex/handoffs/INDEX.md`：用户在其中将需要续接的任务标为 `[x]`，新账号只读取被选中的记录。它不会读取、迁移或合并不同 OpenAI 账号的原生 Codex 对话。

## 安装

将本仓库中的 `SKILL.md`、`agents/` 和 `scripts/` 作为一个名为 `task-handoff` 的技能目录安装到 Codex 技能目录中。

## 使用

在 Codex 中请求：`使用 $task-handoff 为当前任务创建可跨账号续接的本地交接记录。`
