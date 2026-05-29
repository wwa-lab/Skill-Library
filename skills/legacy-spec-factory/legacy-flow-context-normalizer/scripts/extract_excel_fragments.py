#!/usr/bin/env python3
"""Extract multi-sheet XLSX rows into flow-normalizer DOC/FRAG YAML.

The script uses only Python's standard library so it can run in Codex,
Claude Code, and OpenCode environments without installing spreadsheet
dependencies.
"""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree as ET


NS = {
    "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "rel": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "pkgrel": "http://schemas.openxmlformats.org/package/2006/relationships",
}

VIEW_KEYWORDS = {
    "operation_business_flow": (
        "operation",
        "business",
        "function spec",
        "functional spec",
        "requirement",
        "use case",
        "process",
        "procedure",
        "actor",
        "role",
        "approval",
        "exception",
        "manual",
        "step",
        "handoff",
        "workflow",
    ),
    "system_flow": (
        "system",
        "technical design",
        "solution design",
        "architecture",
        "interface",
        "interface spec",
        "integration design",
        "integration",
        "upstream",
        "downstream",
        "api",
        "queue",
        "message",
        "batch",
        "schedule",
        "channel",
    ),
    "program_flow": (
        "program",
        "program spec",
        "program specification",
        "job spec",
        "screen spec",
        "report spec",
        "pgm",
        "job",
        "menu",
        "screen",
        "report",
        "call",
        "module",
        "application",
        "trigger",
        "cl",
        "rpg",
    ),
    "data_flow": (
        "data",
        "file spec",
        "file specification",
        "record layout",
        "record format",
        "physical file",
        "logical file",
        "field",
        "file",
        "table",
        "crud",
        "read",
        "write",
        "update",
        "delete",
        "dictionary",
        "entity",
        "column",
        "record",
    ),
}


@dataclass(frozen=True)
class SheetData:
    name: str
    rows: list[list[str]]


@dataclass(frozen=True)
class Fragment:
    fragment_id: str
    doc_id: str
    locator: str
    summary: str
    candidate_view: str
    evidence_strength: str


def xml_root(zf: zipfile.ZipFile, path: str) -> ET.Element:
    return ET.fromstring(zf.read(path))


def column_index(cell_ref: str) -> int:
    match = re.match(r"([A-Z]+)", cell_ref.upper())
    if not match:
        return 0
    value = 0
    for char in match.group(1):
        value = value * 26 + (ord(char) - ord("A") + 1)
    return value - 1


def text_of(element: ET.Element | None) -> str:
    if element is None:
        return ""
    return "".join(element.itertext()).strip()


def load_shared_strings(zf: zipfile.ZipFile) -> list[str]:
    try:
        root = xml_root(zf, "xl/sharedStrings.xml")
    except KeyError:
        return []
    strings: list[str] = []
    for item in root.findall("main:si", NS):
        strings.append(text_of(item))
    return strings


def workbook_sheets(zf: zipfile.ZipFile) -> list[tuple[str, str]]:
    workbook = xml_root(zf, "xl/workbook.xml")
    rels_root = xml_root(zf, "xl/_rels/workbook.xml.rels")
    rels = {
        rel.attrib["Id"]: rel.attrib["Target"]
        for rel in rels_root.findall("pkgrel:Relationship", NS)
    }

    sheets: list[tuple[str, str]] = []
    for sheet in workbook.findall("main:sheets/main:sheet", NS):
        name = sheet.attrib.get("name", "Sheet")
        rel_id = sheet.attrib.get(f"{{{NS['rel']}}}id")
        if not rel_id or rel_id not in rels:
            continue
        target = rels[rel_id]
        path = "xl/" + target.lstrip("/")
        if not path.startswith("xl/worksheets/") and "worksheets/" in path:
            path = "xl/" + path[path.index("worksheets/") :]
        sheets.append((name, path))
    return sheets


def cell_value(cell: ET.Element, shared_strings: list[str]) -> str:
    cell_type = cell.attrib.get("t", "")
    if cell_type == "s":
        raw = text_of(cell.find("main:v", NS))
        if not raw:
            return ""
        try:
            return shared_strings[int(raw)]
        except (ValueError, IndexError):
            return raw
    if cell_type == "inlineStr":
        return text_of(cell.find("main:is", NS))
    if cell_type == "b":
        return "TRUE" if text_of(cell.find("main:v", NS)) == "1" else "FALSE"
    return text_of(cell.find("main:v", NS))


def sheet_rows(zf: zipfile.ZipFile, path: str, shared_strings: list[str]) -> list[list[str]]:
    root = xml_root(zf, path)
    rows: list[list[str]] = []
    for row in root.findall("main:sheetData/main:row", NS):
        values: list[str] = []
        for cell in row.findall("main:c", NS):
            ref = cell.attrib.get("r", "")
            idx = column_index(ref) if ref else len(values)
            while len(values) <= idx:
                values.append("")
            values[idx] = cell_value(cell, shared_strings)
        while values and not values[-1]:
            values.pop()
        rows.append(values)
    return rows


def load_workbook(path: Path) -> list[SheetData]:
    with zipfile.ZipFile(path) as zf:
        shared_strings = load_shared_strings(zf)
        sheets = workbook_sheets(zf)
        return [
            SheetData(name=name, rows=sheet_rows(zf, sheet_path, shared_strings))
            for name, sheet_path in sheets
        ]


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "-", value.strip().upper())
    return cleaned.strip("-") or "MODULE"


def yaml_quote(value: str | None) -> str:
    if value is None:
        return "null"
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def summarize_row(headers: list[str], row: list[str], max_cell_chars: int) -> str:
    pairs: list[str] = []
    width = max(len(headers), len(row))
    for idx in range(width):
        header = headers[idx].strip() if idx < len(headers) and headers[idx].strip() else f"Column {idx + 1}"
        value = row[idx].strip() if idx < len(row) else ""
        if not value:
            continue
        if len(value) > max_cell_chars:
            value = value[: max_cell_chars - 3].rstrip() + "..."
        pairs.append(f"{header}: {value}")
    return "; ".join(pairs)


def classify_view(sheet_name: str, headers: list[str], summary: str) -> str:
    haystack = " ".join([sheet_name, *headers, summary]).lower()
    scores = {
        view: sum(1 for keyword in keywords if keyword in haystack)
        for view, keywords in VIEW_KEYWORDS.items()
    }
    best_view, best_score = max(scores.items(), key=lambda item: item[1])
    return best_view if best_score > 0 else "cross_view"


def build_fragments(
    sheets: list[SheetData],
    module_slug: str,
    doc_id: str,
    max_rows_per_sheet: int,
    max_cell_chars: int,
) -> list[Fragment]:
    fragments: list[Fragment] = []
    seq = 1
    for sheet in sheets:
        non_empty_rows = [row for row in sheet.rows if any(cell.strip() for cell in row)]
        if not non_empty_rows:
            continue
        headers = non_empty_rows[0]
        data_rows = non_empty_rows[1 : max_rows_per_sheet + 1]
        for offset, row in enumerate(data_rows, start=2):
            summary = summarize_row(headers, row, max_cell_chars)
            if not summary:
                continue
            fragments.append(
                Fragment(
                    fragment_id=f"FRAG-{module_slug}-{seq:03d}",
                    doc_id=doc_id,
                    locator=f"{sheet.name} row {offset}",
                    summary=summary,
                    candidate_view=classify_view(sheet.name, headers, summary),
                    evidence_strength="medium",
                )
            )
            seq += 1
    return fragments


def render_source_document_index(
    workbook_path: Path,
    module_slug: str,
    doc_id: str,
    title: str,
    owner: str,
    sensitivity: str,
    authorization_status: str,
    sheets: list[SheetData],
    fragments: list[Fragment],
) -> str:
    sheet_names = ", ".join(sheet.name for sheet in sheets)
    used_in = sorted(
        {
            {
                "operation_business_flow": "01-operation-business-flow.md",
                "system_flow": "02-system-flow.md",
                "program_flow": "03-program-flow.md",
                "data_flow": "04-data-flow.md",
            }.get(fragment.candidate_view, "open-questions.md")
            for fragment in fragments
        }
    )

    lines = [
        'schema_version: "0.1"',
        "",
        "documents:",
        f"  - doc_id: {doc_id}",
        f"    title: {yaml_quote(title)}",
        f"    path: {yaml_quote(str(workbook_path))}",
        "    format: xlsx",
        "    source_type: mixed_spec_workbook",
        f"    owner: {yaml_quote(owner)}",
        '    document_date: "unknown"',
        f"    sensitivity: {sensitivity}",
        f"    authorization_status: {authorization_status}",
        "    readable_status: extracted",
        '    extraction_method: "xlsx workbook sheet rows via extract_excel_fragments.py"',
        f"    pages_or_sheets: {yaml_quote(sheet_names)}",
        f'    quality_notes: "Extracted {len(fragments)} non-empty data rows across {len(sheets)} sheet(s)."',
        "    used_in:",
    ]
    if used_in:
        lines.extend(f"      - {name}" for name in used_in)
    else:
        lines.append("      - open-questions.md")

    lines.extend(["", "fragments:"])
    if not fragments:
        lines.extend(
            [
                f"  - fragment_id: FRAG-{module_slug}-001",
                f"    doc_id: {doc_id}",
                '    locator: "workbook"',
                '    summary: "No non-empty data rows found after header rows."',
                "    candidate_view: cross_view",
                "    evidence_strength: low",
            ]
        )
    else:
        for fragment in fragments:
            lines.extend(
                [
                    f"  - fragment_id: {fragment.fragment_id}",
                    f"    doc_id: {fragment.doc_id}",
                    f"    locator: {yaml_quote(fragment.locator)}",
                    f"    summary: {yaml_quote(fragment.summary)}",
                    f"    candidate_view: {fragment.candidate_view}",
                    f"    evidence_strength: {fragment.evidence_strength}",
                ]
            )
    return "\n".join(lines) + "\n"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xlsx_path", type=Path, help="Path to an .xlsx workbook")
    parser.add_argument("--module-slug", required=True, help="Business module slug")
    parser.add_argument("--doc-id", help="Stable DOC-* ID. Defaults to DOC-<MODULE>-001")
    parser.add_argument("--title", help="Document title. Defaults to workbook filename")
    parser.add_argument("--owner", default="unknown", help="Document owner")
    parser.add_argument(
        "--sensitivity",
        default="internal",
        choices=("public", "internal", "confidential", "restricted", "synthetic_non_production", "unknown"),
    )
    parser.add_argument(
        "--authorization-status",
        default="approved",
        choices=("approved", "blocked", "unknown"),
    )
    parser.add_argument("--max-rows-per-sheet", type=int, default=200)
    parser.add_argument("--max-cell-chars", type=int, default=160)
    parser.add_argument("--output", type=Path, help="Write YAML to this path instead of stdout")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if not args.xlsx_path.is_file():
        print(f"Workbook not found: {args.xlsx_path}", file=sys.stderr)
        return 1
    if args.xlsx_path.suffix.lower() != ".xlsx":
        print("Expected an .xlsx workbook", file=sys.stderr)
        return 1
    if args.max_rows_per_sheet < 1:
        print("--max-rows-per-sheet must be >= 1", file=sys.stderr)
        return 1
    if args.max_cell_chars < 20:
        print("--max-cell-chars must be >= 20", file=sys.stderr)
        return 1

    module_slug = slugify(args.module_slug)
    doc_id = args.doc_id or f"DOC-{module_slug}-001"
    if not re.fullmatch(rf"DOC-{module_slug}-\d{{3}}", doc_id):
        print(f"--doc-id must match DOC-{module_slug}-NNN", file=sys.stderr)
        return 1

    try:
        sheets = load_workbook(args.xlsx_path)
    except (KeyError, ET.ParseError, zipfile.BadZipFile) as exc:
        print(f"Could not parse workbook: {exc}", file=sys.stderr)
        return 1

    fragments = build_fragments(
        sheets=sheets,
        module_slug=module_slug,
        doc_id=doc_id,
        max_rows_per_sheet=args.max_rows_per_sheet,
        max_cell_chars=args.max_cell_chars,
    )
    output = render_source_document_index(
        workbook_path=args.xlsx_path,
        module_slug=module_slug,
        doc_id=doc_id,
        title=args.title or args.xlsx_path.name,
        owner=args.owner,
        sensitivity=args.sensitivity,
        authorization_status=args.authorization_status,
        sheets=sheets,
        fragments=fragments,
    )

    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
