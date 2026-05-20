#!/usr/bin/env python3
"""List all Legacy Spec Factory projects in this repository.

Scans `docs/*/workflow-state.yaml` and prints a table showing each
project's current focus, capability count, and blocker count.

Useful for: PM weekly review, picking up a teammate's project, auditing
"what's in flight" across a multi-project repo.

Usage:
  python3 scripts/list-projects.py              # table to stdout
  python3 scripts/list-projects.py --markdown   # markdown table
  python3 scripts/list-projects.py --json       # machine-readable

Exit 0 on success (including when no projects are found).

Standalone: only depends on PyYAML.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Install with: pip install pyyaml")
    sys.exit(2)


# Scan the current working directory's docs/ — this script is typically
# invoked from inside a user repo that hosts one or more LSF projects, not
# from the legacy-spec-factory skills repo itself.
REPO_ROOT = Path.cwd()
DOCS_DIR = REPO_ROOT / "docs"


STAGE_PROGRESS_PREFIXES = [
    ("10", 10), ("9", 9), ("8c", 8), ("8b", 7), ("8a", 6),
    ("7", 5), ("6", 5), ("5", 5), ("4b", 5), ("4a", 5),
    ("3f", 5), ("3e", 5), ("3d", 4), ("3c", 4), ("3b", 3), ("3a", 3),
    ("2", 2), ("1", 1), ("0", 0),
]


def stage_to_step(stage_id: str | None) -> int:
    if not stage_id:
        return 0
    s = stage_id.strip().lower()
    for prefix, step in STAGE_PROGRESS_PREFIXES:
        if s.startswith(prefix.lower()):
            return step
    return 0


def progress_bar(step: int, total: int = 10) -> str:
    return "[" + "●" * step + "○" * (total - step) + f"] {step}/{total}"


def count_blocking(caps: list[dict]) -> int:
    total = 0
    for cap in caps:
        if cap.get("archived"):
            continue
        b = cap.get("blocking") or {}
        total += len(b.get("tbds") or [])
        total += len(b.get("sme_pending") or [])
        total += len(b.get("gates") or [])
    return total


def scan() -> list[dict]:
    projects: list[dict] = []
    if not DOCS_DIR.exists():
        return projects
    for state_path in sorted(DOCS_DIR.glob("*/workflow-state.yaml")):
        try:
            with state_path.open("r", encoding="utf-8") as fh:
                state = yaml.safe_load(fh) or {}
        except yaml.YAMLError:
            projects.append(
                {
                    "name": state_path.parent.name,
                    "error": "yaml parse error",
                    "path": str(state_path.relative_to(REPO_ROOT)),
                }
            )
            continue

        project = state.get("project") or {}
        focus = state.get("current_focus") or {}
        caps = state.get("capabilities") or []
        active = [c for c in caps if not c.get("archived")]
        archived = [c for c in caps if c.get("archived")]

        focus_str = "(no focus)"
        focus_progress = progress_bar(0)
        if focus.get("capability_id"):
            stage = focus.get("stage_id", "?")
            focus_str = f"{focus['capability_id']} @ {stage}"
            focus_progress = progress_bar(stage_to_step(stage))

        last_updated = project.get("last_updated_at") or "?"
        # PyYAML auto-parses ISO date strings into date/datetime objects.
        if isinstance(last_updated, datetime):
            last_updated = last_updated.date().isoformat()
        elif hasattr(last_updated, "isoformat"):
            last_updated = last_updated.isoformat()
        else:
            last_updated = str(last_updated)

        projects.append(
            {
                "name": project.get("name") or state_path.parent.name,
                "root": project.get("root") or f"docs/{state_path.parent.name}/",
                "current_focus": focus_str,
                "progress": focus_progress,
                "active_capabilities": len(active),
                "archived_capabilities": len(archived),
                "open_blockers": count_blocking(caps),
                "last_updated": last_updated,
                "last_updated_by": project.get("last_updated_by") or "?",
                "path": str(state_path.relative_to(REPO_ROOT)),
            }
        )
    return projects


def render_text(projects: list[dict]) -> str:
    if not projects:
        return f"No projects found under {DOCS_DIR.relative_to(REPO_ROOT)}/"
    lines = [
        f"Found {len(projects)} project(s) under "
        f"{DOCS_DIR.relative_to(REPO_ROOT)}/",
        "",
    ]
    headers = ["Project", "Progress", "Focus", "Caps", "Blockers", "Updated", "By"]
    rows: list[list[str]] = []
    for p in projects:
        if "error" in p:
            rows.append([p["name"], "—", f"ERROR: {p['error']}", "—", "—", "—", "—"])
            continue
        caps = f"{p['active_capabilities']}"
        if p["archived_capabilities"]:
            caps += f" (+{p['archived_capabilities']} archived)"
        rows.append(
            [
                p["name"],
                p["progress"],
                p["current_focus"],
                caps,
                str(p["open_blockers"]),
                p["last_updated"],
                p["last_updated_by"],
            ]
        )
    widths = [
        max(len(headers[i]), max(len(row[i]) for row in rows))
        for i in range(len(headers))
    ]
    fmt = "  ".join(f"{{:<{w}}}" for w in widths)
    lines.append(fmt.format(*headers))
    lines.append(fmt.format(*["-" * w for w in widths]))
    for row in rows:
        lines.append(fmt.format(*row))
    return "\n".join(lines)


def render_markdown(projects: list[dict]) -> str:
    if not projects:
        return f"No projects found under `{DOCS_DIR.relative_to(REPO_ROOT)}/`."
    lines = [
        f"# Projects in This Repo ({len(projects)})",
        "",
        "| Project | Progress | Focus | Capabilities | Blockers | Updated | By |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for p in projects:
        if "error" in p:
            lines.append(
                f"| {p['name']} | — | ERROR: {p['error']} | — | — | — | — |"
            )
            continue
        caps = f"{p['active_capabilities']}"
        if p["archived_capabilities"]:
            caps += f" (+{p['archived_capabilities']} archived)"
        lines.append(
            f"| [{p['name']}]({p['root']}STATUS.md) "
            f"| `{p['progress']}` "
            f"| {p['current_focus']} "
            f"| {caps} "
            f"| {p['open_blockers']} "
            f"| {p['last_updated']} "
            f"| {p['last_updated_by']} |"
        )
    return "\n".join(lines)


def main() -> int:
    args = sys.argv[1:]
    fmt = "text"
    if args and args[0] in ("--markdown", "--md"):
        fmt = "markdown"
        args = args[1:]
    elif args and args[0] == "--json":
        fmt = "json"
        args = args[1:]
    if args:
        print(
            "Usage: python3 scripts/list-projects.py [--markdown | --json]"
        )
        return 2
    projects = scan()
    if fmt == "json":
        print(json.dumps(projects, indent=2, default=str))
    elif fmt == "markdown":
        print(render_markdown(projects))
    else:
        print(render_text(projects))
    return 0


if __name__ == "__main__":
    sys.exit(main())
