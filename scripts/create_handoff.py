#!/usr/bin/env python3
"""Create a portable Codex task handoff record without overwriting existing notes."""

import argparse
import re
from datetime import date
from pathlib import Path


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "task-handoff"


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a Codex task handoff file.")
    parser.add_argument("--project", type=Path, help="Project folder for the default handoff location.")
    parser.add_argument("--path", type=Path, help="Explicit handoff file path.")
    parser.add_argument("--title", required=True, help="Short task title.")
    args = parser.parse_args()

    if bool(args.project) == bool(args.path):
        parser.error("provide exactly one of --project or --path")

    path = args.path or args.project / ".codex" / "handoffs" / f"{slugify(args.title)}.md"
    path = path.expanduser().resolve()
    if path.exists():
        print(f"Existing handoff preserved: {path}")
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"# Task handoff: {args.title}\n\n"
        f"Created: {date.today().isoformat()}\n\n"
        "## Goal\n\n- \n\n"
        "## Project\n\n- Path: \n\n"
        "## Completed\n\n- \n\n"
        "## Important files\n\n- \n\n"
        "## Decisions and constraints\n\n- \n\n"
        "## Verification\n\n- \n\n"
        "## Next action\n\n- \n",
        encoding="utf-8",
    )
    print(f"Created handoff: {path}")


if __name__ == "__main__":
    main()
