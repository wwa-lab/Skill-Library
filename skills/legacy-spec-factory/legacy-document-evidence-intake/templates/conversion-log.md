# Conversion Log

Module: `<MODULE-SLUG>` · Document set: `<DOCSET-SLUG>`

Human-readable audit trail of every conversion and extraction attempt. Record
the tool that ran (or "none available") and the honest outcome. Never record a
conversion as successful when no tool ran.

## Tooling Availability

| Tool | Status | Version / Notes |
| --- | --- | --- |
| LibreOffice (`soffice`) | available / unavailable | <version> |
| Docling | available / unavailable | optional enhancer |
| OCR engine | available / unavailable | <name> |
| PDF renderer | available / unavailable | <name> |

## Conversion Attempts

| Doc ID | From | To | Tool | Result | Notes |
| --- | --- | --- | --- | --- | --- |
| DOC-<MODULE-SLUG>-001 | .xls | .xlsx | libreoffice | succeeded | <command / outcome> |
| DOC-<MODULE-SLUG>-002 | .vsd | pdf,svg,png | libreoffice | tool_unavailable | remediation: install LibreOffice or supply vendor PDF |

Result values: `succeeded` | `partial` | `tool_unavailable` | `not_required`.

## Extraction Attempts

| Doc ID | Method | Coverage | Result | Notes |
| --- | --- | --- | --- | --- |
| DOC-<MODULE-SLUG>-001 | deterministic | all sheets | succeeded | <notes> |
| DOC-<MODULE-SLUG>-003 | ocr | 12/14 pages | partial | 2 pages low-confidence — see warnings |

## Remediation Needed

- <Document>: <what is needed to lift the gate — better export, install tool, etc.>
