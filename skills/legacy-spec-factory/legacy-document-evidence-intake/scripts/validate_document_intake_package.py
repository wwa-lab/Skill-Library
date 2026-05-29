#!/usr/bin/env python3
"""Validate a legacy-document-evidence-intake package without external deps.

Checks package manifests, per-document manifests, declared outputs, and
honest-conversion guardrails. It never performs real document conversion or
extraction.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_FILES = (
    "intake.manifest.yaml",
    "conversion-log.md",
    "extraction-quality.yaml",
    "extraction-warnings.md",
    "evidence-coordinates.md",
)

GATES = {"ready", "ready_with_warnings", "blocked"}
READY_GATES = {"ready", "ready_with_warnings"}

DOC_FIELDS = (
    "doc_id",
    "path",
    "family",
    "file_type",
    "size_bytes",
    "sha256",
    "sensitivity",
    "authorization_status",
    "document_gate",
)

MACRO_FILE_TYPES = ("xlsm", "docm", "pptm")
NON_TOOL_VALUES = {
    "",
    "n/a",
    "na",
    "none",
    "none available",
    "not available",
    "tool_unavailable",
    "unavailable",
    "unknown",
}

FORBIDDEN_IDS_RE = re.compile(r"\b(?:BR|CAP|STEP|SYS|PGM|DATA)-[A-Z0-9-]+-\d{3}\b")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def scalar_value(text: str, key: str) -> str | None:
    match = re.search(rf"^\s*{re.escape(key)}:\s*[\"']?([^\"'\n#]+)", text, re.M)
    if not match:
        return None
    return match.group(1).strip()


def normalized_value(value: str | None) -> str:
    if value is None:
        return ""
    return value.strip().strip("\"'").lower()


def has_real_tool(value: str | None) -> bool:
    normalized = normalized_value(value)
    return normalized not in NON_TOOL_VALUES and "unavailable" not in normalized


def list_values(text: str, key: str) -> list[str]:
    """Return simple YAML list scalar values for `key:` without external deps."""
    match = re.search(rf"^(?P<indent>\s*){re.escape(key)}:\s*$", text, re.M)
    if not match:
        return []

    key_indent = len(match.group("indent"))
    values: list[str] = []
    for line in text[match.end():].splitlines():
        if not line.strip():
            continue

        line_indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()
        if line_indent <= key_indent and not stripped.startswith("- "):
            break
        if not stripped.startswith("- "):
            continue

        raw = stripped[2:].strip()
        if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in {"'", '"'}:
            raw = raw[1:-1]
        values.append(raw)

    return values


def document_blocks(text: str) -> list[str]:
    """Split the documents: list into one text block per `- doc_id:` entry."""
    block = re.search(r"^documents:\s*$", text, re.M)
    if not block:
        return []
    body = text[block.end():]
    # Stop at the next top-level key (a non-indented `key:` line).
    end = re.search(r"^\S[^:\n]*:\s*(?:\n|$)", body, re.M)
    if end:
        body = body[: end.start()]
    entries = re.split(r"^\s*-\s+doc_id:", body, flags=re.M)
    return [chunk for chunk in entries[1:]]


def document_manifest_index(package_dir: Path) -> tuple[dict[str, Path], list[str]]:
    """Return doc_id -> document.manifest.yaml path for package document manifests."""
    index: dict[str, Path] = {}
    findings: list[str] = []
    documents_dir = package_dir / "documents"
    if not documents_dir.is_dir():
        return index, findings

    for manifest_path in sorted(documents_dir.glob("*/document.manifest.yaml")):
        text = read_text(manifest_path)
        doc_id = scalar_value(text, "doc_id")
        if not doc_id:
            findings.append(f"{manifest_path.relative_to(package_dir)} missing doc_id")
            continue
        if doc_id in index:
            findings.append(
                f"duplicate document.manifest.yaml for {doc_id}: "
                f"{index[doc_id].relative_to(package_dir)} and "
                f"{manifest_path.relative_to(package_dir)}"
            )
            continue
        index[doc_id] = manifest_path

    return index, findings


def conversion_log_findings(text: str) -> list[str]:
    findings: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or "---" in stripped or "Doc ID" in stripped:
            continue

        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 5:
            continue

        doc_id, _from_ext, _to_ext, tool, result = cells[:5]
        if normalized_value(result) == "succeeded" and not has_real_tool(tool):
            findings.append(
                f"conversion-log.md records succeeded conversion without a real "
                f"tool for {doc_id}"
            )

    return findings


def validate_document_manifest(
    package_dir: Path,
    manifest_path: Path,
    doc_id: str,
    doc_gate: str | None,
    file_type: str,
) -> list[str]:
    findings: list[str] = []
    text = read_text(manifest_path)
    rel_path = manifest_path.relative_to(package_dir)

    manifest_doc_id = scalar_value(text, "doc_id")
    if manifest_doc_id != doc_id:
        findings.append(f"{rel_path} doc_id mismatch: expected {doc_id}")

    manifest_gate = scalar_value(text, "document_gate")
    if manifest_gate not in GATES:
        findings.append(f"{rel_path} has invalid document_gate: {manifest_gate}")

    if "structure:" not in text:
        findings.append(f"{rel_path} missing structure block")
    if "fragments:" not in text:
        findings.append(f"{rel_path} missing fragments block")
    elif doc_gate in READY_GATES and "fragment_id:" not in text:
        findings.append(f"{rel_path} must list at least one fragment for ready gates")

    if file_type in MACRO_FILE_TYPES:
        if "macro_findings:" not in text:
            findings.append(f"macro-enabled file ({file_type}) missing macro_findings")
        if scalar_value(text, "security_review_required") is None:
            findings.append(
                f"macro-enabled file ({file_type}) must declare "
                "security_review_required in document.manifest.yaml"
            )
        if re.search(r"executed:\s*true", text):
            findings.append(f"macros must never execute: {rel_path} has executed: true")

    return findings


def validate(package_dir: Path, allow_blocked: bool) -> list[str]:
    findings: list[str] = []

    if not package_dir.exists() or not package_dir.is_dir():
        return [f"Package directory does not exist: {package_dir}"]

    missing = [name for name in REQUIRED_FILES if not (package_dir / name).is_file()]
    if missing:
        findings.append(f"Missing required files: {', '.join(missing)}")
        return findings

    manifest = read_text(package_dir / "intake.manifest.yaml")

    if "package_type: document_evidence_intake" not in manifest and (
        'package_type: "document_evidence_intake"' not in manifest
    ):
        findings.append(
            "intake.manifest.yaml must declare package_type: document_evidence_intake"
        )

    if not scalar_value(manifest, "module_slug"):
        findings.append("intake.manifest.yaml must declare module_slug")
    if not scalar_value(manifest, "docset_slug"):
        findings.append("intake.manifest.yaml must declare docset_slug")

    gate = scalar_value(manifest, "gate")
    if gate not in GATES:
        findings.append(f"intake.manifest.yaml has invalid gate: {gate or 'missing'}")
    elif gate == "blocked" and not allow_blocked:
        findings.append("Package is blocked (use --allow-blocked to inspect structurally)")

    outputs = list_values(manifest, "outputs")
    if not outputs:
        findings.append("intake.manifest.yaml must declare outputs list")
    for name in REQUIRED_FILES:
        if name not in outputs:
            findings.append(f"intake.manifest.yaml outputs must list file: {name}")
    for output in outputs:
        if not (package_dir / output).is_file():
            findings.append(f"intake.manifest.yaml outputs lists missing file: {output}")

    blocks = document_blocks(manifest)
    if not blocks:
        findings.append("intake.manifest.yaml must list at least one document")

    doc_manifest_index, doc_manifest_findings = document_manifest_index(package_dir)
    findings.extend(doc_manifest_findings)

    for index, block in enumerate(blocks, start=1):
        block = "doc_id:" + block  # restore the field stripped by the split
        doc_id = scalar_value(block, "doc_id") or f"#{index}"
        for field in DOC_FIELDS:
            if scalar_value(block, field) is None:
                findings.append(f"document {doc_id} missing required field: {field}")

        doc_gate = scalar_value(block, "document_gate")
        if doc_gate is not None and doc_gate not in GATES:
            findings.append(f"document has invalid document_gate: {doc_gate}")

        file_type = (scalar_value(block, "file_type") or "").lower()
        result = normalized_value(scalar_value(block, "result"))
        if result == "succeeded" and not has_real_tool(scalar_value(block, "tool")):
            findings.append(
                f"document {doc_id} records conversion succeeded without a real tool"
            )

        if file_type in MACRO_FILE_TYPES:
            review = scalar_value(block, "security_review_required")
            if review is None:
                findings.append(
                    f"macro-enabled file ({file_type}) must declare security_review_required"
                )

        doc_manifest = doc_manifest_index.get(doc_id)
        if doc_manifest is None:
            findings.append(
                f"document {doc_id} missing documents/<DOC-SLUG>/document.manifest.yaml"
            )
        else:
            findings.extend(
                validate_document_manifest(
                    package_dir,
                    doc_manifest,
                    doc_id,
                    doc_gate,
                    file_type,
                )
            )

        normalized_outputs = list_values(block, "normalized_outputs")
        if doc_gate in READY_GATES and not normalized_outputs:
            findings.append(f"document {doc_id} must list normalized_outputs")
        for output in normalized_outputs:
            if not (package_dir / output).is_file():
                findings.append(f"document {doc_id} normalized output missing: {output}")

        if gate in READY_GATES:
            sensitivity = scalar_value(block, "sensitivity")
            authorization = scalar_value(block, "authorization_status")
            if sensitivity == "unknown":
                findings.append(
                    "ready packages cannot include documents with unknown sensitivity"
                )
            if authorization in {"unauthorized", "pending"}:
                findings.append(
                    "ready packages cannot include unauthorized or pending documents"
                )

    quality = read_text(package_dir / "extraction-quality.yaml")
    if re.search(r"executed:\s*true", quality):
        findings.append("macros must never execute: extraction-quality.yaml has executed: true")
    if re.search(r"executed:\s*true", manifest):
        findings.append("macros must never execute: intake.manifest.yaml has executed: true")

    findings.extend(conversion_log_findings(read_text(package_dir / "conversion-log.md")))

    coordinates = read_text(package_dir / "evidence-coordinates.md")
    if "DOC-" not in coordinates or "FRAG-" not in coordinates:
        findings.append("evidence-coordinates.md must reference DOC-* and FRAG-* ids")

    for name in ("evidence-coordinates.md", "extraction-warnings.md"):
        forbidden = sorted(set(FORBIDDEN_IDS_RE.findall(read_text(package_dir / name))))
        if forbidden:
            findings.append(
                f"{name} must not mint downstream ids (found: {', '.join(forbidden)})"
            )

    return findings


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "package_dir",
        type=Path,
        help="Path to 00_context_packages/<MODULE-SLUG>/document-intake/<DOCSET-SLUG>",
    )
    parser.add_argument(
        "--allow-blocked",
        action="store_true",
        help="Validate blocked packages structurally without failing on blocked gate.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    findings = validate(args.package_dir, args.allow_blocked)
    if findings:
        print("FAIL: document intake package validation failed")
        for finding in findings:
            print(f"- {finding}")
        return 1

    print("OK: document intake package is structurally valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
