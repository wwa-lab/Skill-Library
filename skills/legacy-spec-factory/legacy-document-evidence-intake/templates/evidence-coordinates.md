# Evidence Coordinates

Module: `<MODULE-SLUG>` · Document set: `<DOCSET-SLUG>`

Stable coordinate for every extracted fragment so downstream skills can cite the
exact origin of a fact. Mirrors the `fragments` block in each
`documents/<DOC-SLUG>/document.manifest.yaml`. This skill mints only `DOC-*`,
`FRAG-*`, and `TBD-*` — never `BR-*`, `CAP-*`, `STEP-*`, `SYS-*`, `PGM-*`, or
`DATA-*`.

| Fragment ID | Doc ID | Coordinate | Method | Confidence | Promotion |
| --- | --- | --- | --- | --- | --- |
| FRAG-<MODULE-SLUG>-001 | DOC-<MODULE-SLUG>-001 | workbook/Sheet1/A1:H42 | deterministic | high | open |
| FRAG-<MODULE-SLUG>-002 | DOC-<MODULE-SLUG>-002 | page 2 / shape "Approve" | visual_review | medium | open |
| FRAG-<MODULE-SLUG>-003 | DOC-<MODULE-SLUG>-003 | page 7 / region top-right | ocr | low | open |

Coordinate shapes by family:

- Excel: `workbook / sheet / row / column / cell-range`
- Word: `section / heading / paragraph / table`
- PowerPoint: `slide / shape / table / note`
- Visio: `page / shape / connector / OCR-region`
- PDF: `page / region / table`
- Image / scanned: `page / OCR-region`
