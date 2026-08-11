---
name: task-handoff
description: Create and maintain local task handoff records so work can continue after switching Codex accounts or devices. Use when a user asks to preserve, transfer, resume, summarize, or index a Codex task across accounts without relying on chat history.
---

# Task Handoff

Maintain a portable, human-readable handoff file in the shared project folder. It does not access, merge, or display chats that belong to another OpenAI account.

## Workflow

1. Determine a durable shared location. Prefer `<project>/.codex/handoffs/<task-slug>.md`; use a user-provided shared folder when the project itself is not shared.
2. Use `scripts/create_handoff.py` to create the record if it does not exist. Preserve prior notes unless the user requests replacement.
3. Record only what another account needs: goal, project path, important files, completed work, decisions, commands/results, open issues, and the next concrete action. Never put passwords, API keys, access tokens, or private data into the record.
4. Before switching accounts, update the file and tell the user its exact path. In the new account, read the file first and continue from its **Next action** section.

## Commands

Create a handoff file:

```sh
python3 scripts/create_handoff.py --project /absolute/project/path --title "Task title"
```

Use `--path /shared/location/handoff.md` when the handoff must live outside the project.

## Constraints

- A new account cannot see or reopen the original account's Codex chat from this file.
- Local files remain local. Ensure the new account/device has access to the project folder, for example through a shared Git repository or synced folder.
- Do not delete the original conversation. It stays available when signed into the original account.
