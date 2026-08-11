---
name: task-handoff
description: Create, maintain, and select local task handoff records so work can continue after switching Codex accounts or devices. Use when a user asks to preserve, transfer, resume, summarize, list, select, or index a Codex task across accounts without relying on chat history.
---

# Task Handoff

Maintain portable, human-readable handoff files in the shared project folder. It does not access, merge, or display chats that belong to another OpenAI account.

## Workflow

1. Determine a durable shared location. Prefer `<project>/.codex/handoffs/<task-slug>.md`; use a user-provided shared folder when the project itself is not shared.
2. Run `scripts/manage_handoffs.py refresh --project <project>` whenever this skill creates or updates a handoff. This refreshes `<project>/.codex/handoffs/INDEX.md` while preserving the user's selections.
3. Use `scripts/create_handoff.py` to create the record if it does not exist. Preserve prior notes unless the user requests replacement.
4. Record only what another account needs: goal, project path, important files, completed work, decisions, commands/results, open issues, and the next concrete action. Never put passwords, API keys, access tokens, or private data into the record.
5. For a new account or when several handoffs exist, refresh the index and read only files marked `[x]`. If none are selected, show the candidate list and ask the user which task or tasks to mark for handoff. Do not infer a selection.
6. Before switching accounts, update the selected record and index, then tell the user both exact paths. In the new account, read the selected records first and continue from their **Next action** sections.

## Commands

Create a handoff file:

```sh
python3 scripts/create_handoff.py --project /absolute/project/path --title "Task title"
```

Use `--path /shared/location/handoff.md` when the handoff must live outside the project.

Refresh and list local handoffs:

```sh
python3 scripts/manage_handoffs.py refresh --project /absolute/project/path
python3 scripts/manage_handoffs.py list --project /absolute/project/path
```

Users select handoffs by changing `- [ ]` to `- [x]` in `INDEX.md`, or by telling Codex which listed task names to select. Refreshing preserves existing checked items.

## Sync behavior

The skill automatically refreshes the local index each time it is invoked to create, update, list, or resume a handoff. It cannot run in the background, monitor chat activity, or extract another account's native task history. Ask the user to invoke the skill before switching accounts when a final update is needed.

## Constraints

- A new account cannot see or reopen the original account's Codex chat from this file.
- Local files remain local. Ensure the new account/device has access to the project folder, for example through a shared Git repository or synced folder.
- Do not delete the original conversation. It stays available when signed into the original account.
