#!/usr/bin/env python3
"""Validate a legacy-module-context-intake package without external deps."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_FILES = (
    "context-index.yaml",
    "01-operation-business-flow.md",
    "02-system-flow.md",
    "03-program-flow.md",
    "04-data-flow.md",
    "rag-evidence-map.md",
    "contradiction-log.md",
    "open-questions.md",
)

READY_STATUSES = {
    "ready_for_module_analysis",
    "ready_with_warnings",
}

BLOCKED_STATUSES = {
    "blocked_pending_evidence",
    "blocked_pending_scope",
    "blocked_pending_contradiction_review",
}

ALL_STATUSES = READY_STATUSES | BLOCKED_STATUSES

EVIDENCE_ID_RE = re.compile(
    r"\b(?:SNP|RUN|DD|EV)-[A-Z0-9-]+(?:-\d{3})?\b|"
    r"\bRAG-(?:CAND|CONFLICT|GAP|ASM)-[A-Z0-9-]+-\d{3}\b"
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def scalar_value(text: str, key: str) -> str | None:
    match = re.search(rf"^\s*{re.escape(key)}:\s*[\"']?([^\"'\n#]+)", text, re.M)
    if not match:
        return None
    return match.group(1).strip()


def section(text: str, heading: str) -> str:
    pattern = re.compile(rf"^## {re.escape(heading)}\s*$", re.M)
    match = pattern.search(text)
    if not match:
        return ""
    start = match.end()
    next_match = re.search(r"^##\s+", text[start:], re.M)
    if not next_match:
        return text[start:]
    return text[start : start + next_match.start()]


def markdown_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def ids_in_view_files(package_dir: Path) -> set[str]:
    ids: set[str] = set()
    for name in REQUIRED_FILES[1:5]:
        ids.update(EVIDENCE_ID_RE.findall(read_text(package_dir / name)))
    return ids


def validate(package_dir: Path, allow_blocked: bool) -> list[str]:
    findings: list[str] = []

    if not package_dir.exists() or not package_dir.is_dir():
        return [f"Package directory does not exist: {package_dir}"]

    missing = [name for name in REQUIRED_FILES if not (package_dir / name).is_file()]
    if missing:
        findings.append(f"Missing required files: {', '.join(missing)}")
        return findings

    index_text = read_text(package_dir / "context-index.yaml")
    if "package_type: module_context_intake" not in index_text:
        findings.append("context-index.yaml must declare package_type: module_context_intake")

    status = scalar_value(index_text, "status")
    if status not in ALL_STATUSES:
        findings.append(f"context-index.yaml has invalid intake status: {status or 'missing'}")
    elif status in BLOCKED_STATUSES and not allow_blocked:
        findings.append(f"Package is blocked: {status}")

    for name in REQUIRED_FILES[1:]:
        if name not in index_text:
            findings.append(f"context-index.yaml does not list output file: {name}")

    evidence_map = read_text(package_dir / "rag-evidence-map.md")
    missing_ids = sorted(id_ for id_ in ids_in_view_files(package_dir) if id_ not in evidence_map)
    if missing_ids:
        findings.append(
            "Evidence IDs referenced in view files are missing from rag-evidence-map.md: "
            + ", ".join(missing_ids)
        )

    candidate_section = section(evidence_map, "Candidate Facts")
    approved_candidate = False
    for line in candidate_section.splitlines():
        if not line.startswith("|") or "---" in line:
            continue
        cells = markdown_cells(line)
        if cells and cells[0].startswith("RAG-CAND-") and any(
            cell.lower() == "approved" for cell in cells[1:]
        ):
            approved_candidate = True
            break
    if approved_candidate:
        findings.append("RAG candidate facts must not use Promotion Status 'approved'")

    contradiction_text = read_text(package_dir / "contradiction-log.md")
    if "status: none_found" in contradiction_text:
        if "evaluated_checks_present: true" not in contradiction_text:
            findings.append("none_found contradiction logs must set evaluated_checks_present: true")
        evaluated = section(contradiction_text, "Evaluated Checks")
        data_rows = [line for line in evaluated.splitlines() if line.startswith("|") and "---" not in line]
        if len(data_rows) < 2:
            findings.append("none_found contradiction logs must include at least one evaluated check")

    open_questions = read_text(package_dir / "open-questions.md")
    if "## Recommended Next Prompt" not in open_questions:
        findings.append("open-questions.md must include Recommended Next Prompt")
    if "legacy-ibmi-module-analyzer" not in open_questions and status in READY_STATUSES:
        findings.append("ready packages must name legacy-ibmi-module-analyzer as the next prompt")

    return findings


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package_dir", type=Path, help="Path to 00_context_packages/<MODULE-SLUG>/")
    parser.add_argument(
        "--allow-blocked",
        action="store_true",
        help="Validate blocked packages structurally without failing on blocked status.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    findings = validate(args.package_dir, args.allow_blocked)
    if findings:
        print("FAIL: module context package validation failed")
        for finding in findings:
            print(f"- {finding}")
        return 1

    print("OK: module context package is structurally valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
