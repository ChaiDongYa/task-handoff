#!/usr/bin/env python3
"""List and refresh a user-selectable index of local task handoffs."""

import argparse
import re
from datetime import datetime
from pathlib import Path


def text_after_heading(text: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not match:
        return ""
    for line in match.group(1).splitlines():
        value = line.removeprefix("- ").strip()
        if value:
            return value
    return ""


def records(project: Path) -> list[dict[str, str]]:
    directory = project / ".codex" / "handoffs"
    if not directory.exists():
        return []
    result = []
    for path in sorted(directory.glob("*.md")):
        if path.name == "INDEX.md":
            continue
        text = path.read_text(encoding="utf-8")
        title = re.search(r"^#\s+Task handoff:\s*(.+)$", text, re.M)
        result.append(
            {
                "name": path.name,
                "title": title.group(1).strip() if title else path.stem,
                "next": text_after_heading(text, "Next action") or "No next action recorded",
                "updated": datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
            }
        )
    return result


def selected_names(index: Path) -> set[str]:
    if not index.exists():
        return set()
    return set(re.findall(r"^- \[x\] `([^`]+)`", index.read_text(encoding="utf-8"), re.M))


def render(items: list[dict[str, str]], selected: set[str]) -> str:
    lines = ["# Task handoff index", "", "Mark `[x]` for each handoff to continue in the next account.", ""]
    if not items:
        lines.append("No handoff records yet.")
    for item in items:
        check = "x" if item["name"] in selected else " "
        lines.extend(
            [
                f"- [{check}] `{item['name']}` — {item['title']}",
                f"  - Updated: {item['updated']}",
                f"  - Next: {item['next']}",
            ]
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="List or refresh local task handoffs.")
    parser.add_argument("action", choices=("list", "refresh"))
    parser.add_argument("--project", required=True, type=Path)
    args = parser.parse_args()
    project = args.project.expanduser().resolve()
    index = project / ".codex" / "handoffs" / "INDEX.md"
    output = render(records(project), selected_names(index))
    if args.action == "refresh":
        index.parent.mkdir(parents=True, exist_ok=True)
        index.write_text(output, encoding="utf-8")
        print(f"Refreshed index: {index}")
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
