#!/usr/bin/env python3
"""Validate a legacy-flow-context-normalizer package without external deps."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_FILES = (
    "flow-context-index.yaml",
    "source-document-index.yaml",
    "01-operation-business-flow.md",
    "02-system-flow.md",
    "03-program-flow.md",
    "04-data-flow.md",
    "evidence-map.md",
    "contradiction-log.md",
    "open-questions.md",
    "sme-review-pack.md",
)

READY_STATUSES = {
    "ready_for_context_intake",
    "ready_with_warnings",
}

DRAFT_STATUSES = {
    "draft_needs_sme_review",
    "triage_needs_source_enrichment",
}

BLOCKED_STATUSES = {
    "blocked_pending_evidence",
    "blocked_pending_scope",
    "blocked_pending_readable_source",
    "blocked_pending_contradiction_review",
}

ALL_STATUSES = READY_STATUSES | DRAFT_STATUSES | BLOCKED_STATUSES

EVIDENCE_ID_RE = re.compile(
    r"\b(?:DOC|FRAG|SYS|PGM|DATA)-[A-Z0-9-]+-\d{3}\b"
)

PGM_ID_RE = re.compile(r"\bPGM-[A-Z0-9-]+-\d{3}\b")
DATA_ID_RE = re.compile(r"\bDATA-[A-Z0-9-]+-\d{3}\b")

_UNKNOWN_AUTH_RE = re.compile(r"authorization_status:\s*[\"']?unknown[\"']?")
_UNREADABLE_RE = re.compile(r"readable_status:\s*[\"']?unreadable[\"']?")

VIEW_FILES = REQUIRED_FILES[2:6]
VIEW_REQUIRED_HEADINGS = (
    "Normalization Status",
    "Summary",
    "Mermaid Flow Diagram",
    "Evidence-Linked Flow Steps",
    "Candidate Seeds",
    "Gaps For SME Review",
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


def top_level_block(text: str, key: str) -> str:
    pattern = re.compile(rf"^{re.escape(key)}:\s*$", re.M)
    match = pattern.search(text)
    if not match:
        return ""
    start = match.end()
    next_match = re.search(r"^\S[^:\n]*:\s*(?:\n|$)", text[start:], re.M)
    if not next_match:
        return text[start:]
    return text[start : start + next_match.start()]


def markdown_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def ids_in_view_files(package_dir: Path) -> set[str]:
    ids: set[str] = set()
    for name in VIEW_FILES:
        ids.update(EVIDENCE_ID_RE.findall(read_text(package_dir / name)))
    return ids


def view_has_data_rows(text: str, heading: str) -> bool:
    rows = [
        line
        for line in section(text, heading).splitlines()
        if line.startswith("|") and "---" not in line
    ]
    return len(rows) >= 2


def view_has_mermaid_diagram(text: str) -> bool:
    diagram = section(text, "Mermaid Flow Diagram")
    return bool(re.search(r"```mermaid\s+flowchart\s+(?:TD|LR|BT|RL)", diagram, re.I))


def view_has_source_supplement_placeholder(text: str) -> bool:
    return "source_supplement_required" in text and "TBD-" in text


def validate(package_dir: Path, allow_blocked: bool, allow_draft: bool) -> list[str]:
    findings: list[str] = []

    if not package_dir.exists() or not package_dir.is_dir():
        return [f"Package directory does not exist: {package_dir}"]

    missing = [name for name in REQUIRED_FILES if not (package_dir / name).is_file()]
    if missing:
        findings.append(f"Missing required files: {', '.join(missing)}")
        return findings

    index_text = read_text(package_dir / "flow-context-index.yaml")
    if "package_type: flow_context_normalization" not in index_text and (
        'package_type: "flow_context_normalization"' not in index_text
    ):
        findings.append(
            "flow-context-index.yaml must declare package_type: flow_context_normalization"
        )

    status = scalar_value(index_text, "status")
    if status not in ALL_STATUSES:
        findings.append(f"flow-context-index.yaml has invalid normalization status: {status or 'missing'}")
    elif status in BLOCKED_STATUSES and not allow_blocked:
        findings.append(f"Package is blocked: {status}")
    elif status in DRAFT_STATUSES and not allow_draft:
        findings.append(f"Package still needs SME review: {status}")

    for name in REQUIRED_FILES:
        if name not in index_text:
            findings.append(f"flow-context-index.yaml does not list output file: {name}")

    source_index = read_text(package_dir / "source-document-index.yaml")
    if "doc_id:" not in source_index:
        findings.append("source-document-index.yaml must list at least one document")
    if _UNKNOWN_AUTH_RE.search(source_index) and status in READY_STATUSES:
        findings.append("ready packages cannot include documents with unknown authorization")
    if _UNREADABLE_RE.search(source_index) and status in READY_STATUSES:
        findings.append("ready packages cannot include required unreadable documents")

    for name in VIEW_FILES:
        text = read_text(package_dir / name)
        for heading in VIEW_REQUIRED_HEADINGS:
            if f"## {heading}" not in text:
                findings.append(f"{name} missing required section: {heading}")
        if not view_has_mermaid_diagram(text):
            findings.append(f"{name} must include a Mermaid flowchart in Mermaid Flow Diagram")
        if not view_has_data_rows(text, "Evidence-Linked Flow Steps"):
            findings.append(f"{name} must include at least one evidence-linked flow step")

    coverage_block = top_level_block(index_text, "coverage")
    if status in READY_STATUSES and "technical_anchor_coverage:" not in coverage_block:
        findings.append("ready packages must declare coverage.technical_anchor_coverage")

    program_flow = read_text(package_dir / "03-program-flow.md")
    if status in READY_STATUSES and not PGM_ID_RE.search(program_flow):
        if not view_has_source_supplement_placeholder(program_flow):
            findings.append(
                "03-program-flow.md must either cite an IBM i program/job/object anchor "
                "as PGM-* or carry a source_supplement_required TBD placeholder"
            )

    data_flow = read_text(package_dir / "04-data-flow.md")
    if status in READY_STATUSES and not DATA_ID_RE.search(data_flow):
        if not view_has_source_supplement_placeholder(data_flow):
            findings.append(
                "04-data-flow.md must either cite an IBM i file/table/data-object anchor "
                "as DATA-* or carry a source_supplement_required TBD placeholder"
            )

    evidence_map = read_text(package_dir / "evidence-map.md")
    missing_ids = sorted(id_ for id_ in ids_in_view_files(package_dir) if id_ not in evidence_map)
    if missing_ids:
        findings.append(
            "Evidence IDs referenced in view files are missing from evidence-map.md: "
            + ", ".join(missing_ids)
        )

    candidate_section = section(evidence_map, "Candidate Facts")
    approved_candidate = False
    for line in candidate_section.splitlines():
        if not line.startswith("|") or "---" in line:
            continue
        cells = markdown_cells(line)
        if cells and cells[0].startswith("CAND-") and any(
            cell.lower() == "approved" for cell in cells[1:]
        ):
            approved_candidate = True
            break
    if approved_candidate:
        findings.append("Candidate facts must not use Promotion Status 'approved'")

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
    if "legacy-module-context-intake" not in open_questions and status in READY_STATUSES:
        findings.append("ready packages must name legacy-module-context-intake as the next prompt")

    sme_review = read_text(package_dir / "sme-review-pack.md")
    if "## Sign-Off" not in sme_review:
        findings.append("sme-review-pack.md must include Sign-Off")
    if status in READY_STATUSES and re.search(r"\|\s*pending\s*\|", sme_review, re.I):
        findings.append("ready packages cannot have pending sign-off decisions in sme-review-pack.md")

    return findings


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "package_dir",
        type=Path,
        help="Path to 00_context_packages/<MODULE-SLUG>/flow-normalization",
    )
    parser.add_argument(
        "--allow-blocked",
        action="store_true",
        help="Validate blocked packages structurally without failing on blocked status.",
    )
    parser.add_argument(
        "--allow-draft",
        action="store_true",
        help="Validate draft packages structurally without failing on SME-review status.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    findings = validate(args.package_dir, args.allow_blocked, args.allow_draft)
    if findings:
        print("FAIL: flow context package validation failed")
        for finding in findings:
            print(f"- {finding}")
        return 1

    print("OK: flow context package is structurally valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
