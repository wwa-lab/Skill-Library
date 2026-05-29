# Extraction Warnings

Module: `<MODULE-SLUG>` · Document set: `<DOCSET-SLUG>`

Narrative list of every warning that must travel forward to
`legacy-flow-context-normalizer`. An empty section means "evaluated, none found"
— state that explicitly rather than deleting the section.

## Security Review Flags (macros / encrypted content)

| Doc ID | Finding | Static evidence | Promotion | Reviewer |
| --- | --- | --- | --- | --- |
| DOC-<MODULE-SLUG>-001 | macro-enabled workbook; VBA not executed | module names listed in document.manifest.yaml | blocked | unassigned |

Macro-derived content marked `promotion: blocked` must NOT become strong
evidence downstream without a named security reviewer's sign-off.

## Low-Confidence OCR Regions

| Doc ID | Coordinate | OCR confidence | Action |
| --- | --- | --- | --- |
| DOC-<MODULE-SLUG>-003 | page 7 / region top-right | 41 | needs source/SME confirmation |

## Visual-Review Needs (Visio / diagrams / scans)

| Doc ID | Coordinate | Why visual review is needed |
| --- | --- | --- |
| DOC-<MODULE-SLUG>-002 | page 2 / connector cluster | connectors not machine-extractable; confirm flow visually |

## Partial / Failed Conversions

| Doc ID | What is missing | Remediation |
| --- | --- | --- |
| DOC-<MODULE-SLUG>-002 | no PDF/SVG export (tool unavailable) | install LibreOffice or supply vendor export |

## Contradictions Carried Forward

| TBD ID | Conflicting docs | Description |
| --- | --- | --- |
| TBD-<MODULE-SLUG>-001 | DOC-...-001 vs DOC-...-004 | <conflicting statement — do not resolve here> |
