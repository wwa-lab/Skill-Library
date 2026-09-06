---
name: legacy-document-evidence-intake
description: "Intake and format-normalize legacy enterprise documents (Excel .xlsx/.xlsm/.xls, Word .docx/.doc, PowerPoint .pptx/.ppt, Visio .vsdx/.vsd, PDF, images, screenshots, scanned docs) into Markdown, CSV, PDF, PNG/SVG, and manifests with evidence coordinates and quality gates before legacy-flow-context-normalizer. Use when business/technical documents are in formats that GitHub Copilot or downstream LLM skills cannot reliably consume, when legacy binary Office or Visio files need conversion, or when macros, scanned pages, or unauthorized production data require security/redaction review. Does not infer business rules, generate BRD/spec content, approve evidence, or hide contradictions. Routes to legacy-ibmi-evidence-intake when sensitivity or authorization is unresolved; otherwise hands off to legacy-flow-context-normalizer."
license: Apache-2.0
metadata:
  author: Leo L Zhang
  maintainer: platform-engineering
  source: https://github.com/wwa-lab/legacy-spec-factory
  source_commit: 3b6a16b
  domain: legacy-spec-factory
---

<!--
Legacy Spec Factory
Copyright 2026 Leo L Zhang

Original author: Leo L Zhang
License: Apache License 2.0

This skill is part of the Legacy Spec Factory project.
Retain this notice in substantial copies or derived versions.
-->

# Legacy Document Evidence Intake

## Purpose

Turn historical business and technical documents that are trapped in formats
downstream skills cannot reliably read into a **normalized, evidence-coordinate
document-intake package**:

```text
00_context_packages/<MODULE-SLUG>/document-intake/<DOCSET-SLUG>/
|-- intake.manifest.yaml
|-- conversion-log.md
|-- extraction-quality.yaml
|-- extraction-warnings.md
|-- documents/
|   |-- <DOC-SLUG>/
|   |   |-- document.manifest.yaml
|   |   |-- normalized/        # .md, .csv, .pdf, .png, .svg outputs
|   |   `-- source/            # pointer/metadata to the authorized original
|   `-- ...
`-- evidence-coordinates.md
```

This skill is the **pre-normalization entry layer**. It makes legacy Excel,
Word, PowerPoint, Visio, PDF, image, screenshot, and scanned-document material
machine-consumable, records exactly how each artifact was converted or
extracted, and assigns evidence coordinates so that every fragment is traceable.

It does **not**:

- infer business rules, capabilities, or flows,
- generate BRD or spec content,
- approve evidence sensitivity or redaction,
- smooth over contradictions or pretend a failed conversion succeeded.

The next normal skill after a successful document intake is
`legacy-flow-context-normalizer`, which synthesizes the four-view context
package from the normalized fragments produced here.

## Boundary

Use this skill **before** `legacy-flow-context-normalizer` when the source
material is still in raw Office / Visio / PDF / image form and has not been
converted to Markdown / CSV / PDF / PNG / SVG with manifests.

Do not use it as a replacement for:

- `legacy-ibmi-evidence-intake` — when sensitivity is unknown, source
  authorization is missing, production data is unapproved, or redaction is
  required. Route there first; this skill must not inspect unauthorized content.
- `legacy-flow-context-normalizer` — which owns four-view context synthesis,
  Mermaid drafting, and `FRAG-*`/view classification. This skill only produces
  normalized format outputs and coordinates, not flow views.
- `legacy-module-context-intake` — which normalizes already-reviewed context
  or external RAG output.

This skill performs **format normalization and structural extraction only**.
If you find yourself classifying fragments into Operation / System / Program /
Data views or drawing flows, you are in the wrong skill.

## Supported Input Families

| Family | Extensions | Normalization Target |
| --- | --- | --- |
| Excel | `.xlsx`, `.xlsm`, `.xls` | Markdown tables + per-sheet CSV + structure manifest |
| Word | `.docx`, `.doc` | Markdown + extracted images |
| PowerPoint | `.pptx`, `.ppt` | Markdown (titles, text, notes) + slide PNG + optional PDF |
| Visio | `.vsdx`, `.vsd` | PDF / SVG / PNG export + shape-text Markdown + OCR/visual-review warnings |
| PDF | `.pdf` | Markdown text + tables (CSV) + page PNG |
| Images / screenshots / scanned docs | `.png`, `.jpg`, `.jpeg`, `.tif`, `.tiff`, `.bmp` | OCR Markdown + page PNG + low-confidence warnings |

See `references/format-strategy.md` for the per-format extraction and
conversion procedure, and `references/quality-gates.md` for the gate rubric.

## Required Inputs

- Module slug (`MODULE-SLUG`) and a document-set slug (`DOCSET-SLUG`).
- One or more source documents in a supported family, each with:
  - source path,
  - declared file type,
  - file size,
  - `sha256` (or a recorded reason it could not be computed),
  - owner,
  - sensitivity (`public` / `internal` / `confidential` / `unknown`),
  - authorization status (`authorized` / `unauthorized` / `pending`).
- A statement of available conversion tooling (LibreOffice / `soffice`,
  Docling, OCR engine, PDF renderer) or an explicit "none available".

## Stop / Reroute Conditions

Stop and produce only blocking findings (gate `blocked`) if any apply:

| Condition | Route |
| --- | --- |
| Any source has `sensitivity: unknown` | `legacy-ibmi-evidence-intake` |
| Source authorization is missing or `unauthorized` | `legacy-ibmi-evidence-intake` |
| Production data sample is present and unapproved | `legacy-ibmi-evidence-intake` |
| Redaction is required and no approval is recorded | `legacy-ibmi-evidence-intake` |
| Module slug or document-set slug is missing | document owner clarification |
| No supplied document can be opened or extracted in any way | request a readable export / better tooling |

Missing conversion tooling is **not** a hard stop. Produce a `blocked` or
`ready_with_warnings` package with explicit remediation (install LibreOffice,
provide a vendor PDF export, etc.) rather than pretending conversion succeeded.

## Macro Security Policy (`.xlsm` and macro-enabled Office)

- `.xlsm` (and any macro-enabled Office file) must **never execute macros**.
- VBA / macro extraction is **static only** — read bytes, never run them.
- If macros are encrypted, password-protected, unavailable, or make external
  calls (network, shell, file-system, registry), mark
  `security_review_required: true` and do not treat extracted VBA as cleared.
- A macro-containing file gates at **`ready_with_warnings` at best** unless a
  named security reviewer has explicitly reviewed and signed off.
- If macro content is likely business logic but cannot be inspected, **block
  downstream promotion of that content as strong evidence**: record it as a
  `TBD-*` and mark its evidence coordinates `confidence: low,
  promotion: blocked`.

## Tooling / Docling Policy

- Deterministic structural extraction + manifests are the **canonical output**.
- Docling MAY be referenced as an optional renderer/enhancer for supported
  formats (`.xlsx`, `.docx`, `.pptx`, PDF). It must **not** be the only source
  of truth, and its output must be recorded as one extraction method among
  others, not as ground truth.
- Legacy binary formats (`.xls`, `.doc`, `.ppt`, `.vsd`) should be normalized
  first with LibreOffice / `soffice` (or another documented converter) before
  structural extraction:
  - `.xls` → `.xlsx`
  - `.doc` → `.docx`
  - `.ppt` → `.pptx` and/or PDF
  - `.vsd` → PDF / SVG / PNG
- If a converter is unavailable, record the gap in `conversion-log.md`, set the
  affected document gate to `blocked` (or `ready_with_warnings` when partial
  extraction still produced usable output), and give remediation steps. Never
  record a conversion as successful when no tool ran.

## Output Contract

Use `references/quality-gates.md` for required fields. Start from the templates
under `templates/`. The package directory is:

```text
00_context_packages/<MODULE-SLUG>/document-intake/<DOCSET-SLUG>/
```

Required package-level files:

- `intake.manifest.yaml` — registry of every source document with path, type,
  size, `sha256`, owner, sensitivity, authorization status, conversion result,
  per-document gate, and the package-level gate decision.
- `conversion-log.md` — human-readable audit trail of every conversion and
  extraction attempt, the tool used (or "none available"), and the outcome.
- `extraction-quality.yaml` — per-document and per-fragment quality signals
  (extraction method, coverage, OCR confidence, macro findings, warnings).
- `extraction-warnings.md` — narrative list of warnings, security-review flags,
  visual-review needs, and low-confidence OCR regions.

Per-document files under `documents/<DOC-SLUG>/`:

- `document.manifest.yaml` — the single document's structure (sheets, sections,
  slides, pages, shapes), extracted outputs, and evidence coordinates.
- `normalized/` — the converted/normalized artifacts (`.md`, `.csv`, `.pdf`,
  `.png`, `.svg`).

The package-level **quality gate** in `intake.manifest.yaml` must be one of:

- `ready` — every document extracted cleanly; no macro/security flags; no
  unresolved authorization or sensitivity issues.
- `ready_with_warnings` — usable output exists, but some documents carry
  warnings (macros statically extracted, OCR low-confidence regions, visual
  review needed, partial conversion). Warnings travel forward.
- `blocked` — at least one hard issue (unauthorized/unknown sensitivity,
  required redaction missing, no tooling and no usable extraction, or no
  document could be opened).

Allowed handoff:

- `ready` / `ready_with_warnings` → `legacy-flow-context-normalizer`
- `blocked` (authorization/sensitivity) → `legacy-ibmi-evidence-intake`
- `blocked` (tooling/readability) → request better export or tooling; record
  remediation in `extraction-warnings.md` and `intake.manifest.yaml`

## Evidence Coordinates

Every extracted fragment gets a stable coordinate so downstream skills can cite
exactly where a fact came from. Record them in each `document.manifest.yaml` and
summarize in `evidence-coordinates.md`.

| Format | Coordinate shape |
| --- | --- |
| Excel | workbook / sheet / row / column / cell-range |
| Word | section / heading / paragraph / table |
| PowerPoint | slide / shape / table / note |
| Visio | page / shape / connector / OCR-region |
| PDF | page / region / table |
| Image / scanned | page / OCR-region |

Mint `DOC-*` per source document and `FRAG-*` per extracted fragment, consistent
with `docs/id-conventions.md`. This skill does **not** mint `BR-*`, `CAP-*`,
`STEP-*`, `SYS-*`, `PGM-*`, or `DATA-*` — those belong to downstream skills.

## Step Contract

This skill conforms to the Legacy Spec Factory Step Contract. See
`../legacy-step-contract/references/step-contract.md` for field-level rules.

### Input

- **Required**: module slug, document-set slug, source document list with path,
  type, size, `sha256`, owner, sensitivity, and authorization status; declared
  available tooling.
- **Optional**: prior intake manifests to append to, known macro/scan flags,
  redaction approvals, Docling availability, preferred OCR engine.
- **Input readiness scoring**:
  - `0-5 blocked`: any source has `sensitivity: unknown`, missing
    authorization, unapproved production data, or required redaction without
    approval; or no document can be opened by any means.
  - `6 minimum_pass`: module/docset slugs, an authorized readable document set,
    and at least one extractable document are present; unknowns are TBDs.
  - `7-8 usable`: most documents convert/extract cleanly with sizes, hashes,
    and methods recorded; warnings are explicit.
  - `9-10 strong`: every document extracted with full structure, evidence
    coordinates, OCR confidence, and macro findings recorded; no unresolved
    authorization or sensitivity gaps.

### Execution

- **Procedure**: follow the Workflow below; per-format detail lives in
  `references/format-strategy.md`.
- **Allowed inference**: detecting file type from extension/header; choosing a
  documented converter; identifying sheets/sections/slides/pages/shapes;
  recording OCR text and confidence; statically listing VBA module names.
- **Forbidden assumptions**: executing macros; inventing content not present in
  the source; claiming a conversion ran when no tool was available; reading
  unauthorized or unknown-sensitivity content; classifying fragments into flow
  views; promoting macro logic to strong evidence without security review.
- **ID policy**: may mint `DOC-*`, `FRAG-*`, and `TBD-*`. Must not mint
  `BR-*`, `CAP-*`, `STEP-*`, `SYS-*`, `PGM-*`, or `DATA-*`.

### Output

- **Canonical directory**:
  `00_context_packages/<MODULE-SLUG>/document-intake/<DOCSET-SLUG>/`.
- **Required files**: `intake.manifest.yaml`, `conversion-log.md`,
  `extraction-quality.yaml`, `extraction-warnings.md`, `evidence-coordinates.md`,
  and one `document.manifest.yaml` per source document with its `normalized/`
  outputs.
- **Required gates**: authorization/sensitivity, conversion-honesty (no faked
  conversions), macro security, extraction quality, and no downstream
  inference.
- **Handoff status**: only `ready` and `ready_with_warnings` may feed
  `legacy-flow-context-normalizer`; warnings travel forward.

### Validation

- **Mechanical**: run the bundled validator (below). All required files exist;
  `intake.manifest.yaml` declares `package_type: document_evidence_intake`, a
  valid gate, and every document with required fields; the `outputs` index
  lists the required package files; every registered document has a matching
  `documents/<DOC-SLUG>/document.manifest.yaml`; and every non-blocked document
  output listed in `normalized_outputs` exists on disk.
- **Semantic**: no conversion is recorded as successful without a tool or a
  recorded fallback; every `.xlsm`/macro file carries macro findings and a
  security flag; unauthorized/unknown-sensitivity documents are not present in a
  `ready`/`ready_with_warnings` package; no flow-view classification or business
  rule appears.
- **Human approval**: a named reviewer signs off macro security review and any
  redaction decision before those documents are treated as cleared.
- **Blocking conditions**: unauthorized/unknown sensitivity, faked conversion,
  unexecuted-but-claimed extraction, missing macro security flag on a
  macro-enabled file, or any downstream inference.

Emit a Step Validation Report (see
`../legacy-step-contract/templates/step-validation-report.md`) with status
`pass`, `pass_with_warnings`, or `blocked` when reporting to the orchestrator.

## Workflow

1. **Resolve identity and tooling**
   - Confirm `MODULE-SLUG`, `DOCSET-SLUG`, and which converters/OCR/Docling are
     available. Record availability in `conversion-log.md`.

2. **Register source files** (`intake.manifest.yaml`)
   - For each document record path, file type, size, `sha256`, owner,
     sensitivity, and authorization status. Mint a `DOC-*` ID.

3. **Gate authorization and sensitivity**
   - If any document has `sensitivity: unknown`, missing/`unauthorized`
     authorization, unapproved production data, or required-but-unapproved
     redaction, stop and route the package to `legacy-ibmi-evidence-intake`.
     Do not open that content.

4. **Normalize legacy binary formats**
   - Convert `.xls`→`.xlsx`, `.doc`→`.docx`, `.ppt`→`.pptx`/PDF, `.vsd`→PDF/SVG/
     PNG using LibreOffice or a documented converter. If unavailable, record the
     gap and set the document gate accordingly — never fake success.

5. **Extract structure** (per format, see `references/format-strategy.md`)
   - Excel: sheets (incl. hidden), used ranges, tables, formulas, merged cells,
     hyperlinks, cross-sheet references.
   - `.xlsm`: detect macros; never execute; statically extract VBA module names
     if tooling allows; set `security_review_required`.
   - Word: headings, paragraphs, tables, images, sections.
   - PowerPoint: slides, titles, text boxes, tables, speaker notes, embedded
     images, slide screenshots.
   - Visio: pages, shape text, connectors where available, visual exports,
     OCR/visual-review warnings.
   - PDF / image / scanned: page text, OCR (with confidence), tables, page
     images.

6. **Assign evidence coordinates**
   - Mint `FRAG-*` for each extracted fragment and record its format-specific
     coordinate in `document.manifest.yaml`; summarize in
     `evidence-coordinates.md`.

7. **Record quality and warnings**
   - Fill `extraction-quality.yaml` (method, coverage, OCR confidence, macro
     findings) and `extraction-warnings.md` (security flags, visual-review
     needs, low-confidence regions, partial conversions).

8. **Set the package gate**
   - `ready`, `ready_with_warnings`, or `blocked` per
     `references/quality-gates.md`.

9. **Validate**
   - Run the bundled validator and fix every finding before handoff:
     ```bash
     python3 skills/legacy-document-evidence-intake/scripts/validate_document_intake_package.py \
       00_context_packages/<MODULE-SLUG>/document-intake/<DOCSET-SLUG>
     ```

## Handoff

After a `ready` / `ready_with_warnings` package is validated, run
`legacy-flow-context-normalizer` with:

- the normalized Markdown / CSV / PDF / PNG / SVG outputs,
- `intake.manifest.yaml` and `evidence-coordinates.md` (so `DOC-*` / `FRAG-*`
  IDs carry forward),
- `extraction-warnings.md` (so macro/OCR/visual-review warnings stay visible).

Tell the normalizer that any macro-derived content marked `promotion: blocked`
must not become strong evidence without security review, and that
low-confidence OCR fragments remain low-confidence until SME/source confirms.

## Adversarial Cases

- **Missing converter**: do not fake the conversion. Record "tool unavailable",
  set the document gate to `blocked` or `ready_with_warnings`, and provide
  remediation.
- **Macro-laden workbook**: never execute; statically list VBA; set
  `security_review_required: true`; cap at `ready_with_warnings`; block macro
  content from strong-evidence promotion.
- **Scanned/illegible page**: record OCR with low confidence and a
  visual-review warning; do not invent text for unreadable regions.
- **Unknown sensitivity / unauthorized**: route to
  `legacy-ibmi-evidence-intake`; do not open the content.
- **Contradictory documents**: record both; do not silently pick one. Carry the
  conflict forward as a `TBD-*` for the normalizer/SME.

## Success Criteria

- ✅ Every source document is registered with path, type, size, `sha256`,
  owner, sensitivity, and authorization status.
- ✅ Legacy binary formats are converted with a documented tool, or the gap is
  recorded honestly.
- ✅ Structure is extracted per format with evidence coordinates.
- ✅ Macro-enabled files carry static-only findings and a security flag.
- ✅ Quality gate is one of `ready`, `ready_with_warnings`, `blocked`.
- ✅ No business rules, flows, BRD/spec content, or approvals were produced.
- ✅ The validator passes before handoff to
  `legacy-flow-context-normalizer`.

## Runtime Portability

The canonical skill source lives under:

```text
skills/legacy-document-evidence-intake/SKILL.md
skills/legacy-document-evidence-intake/references/
skills/legacy-document-evidence-intake/templates/
skills/legacy-document-evidence-intake/scripts/validate_document_intake_package.py
```

Runtime copies may be synced to `.claude/skills/`, `.opencode/skills/`,
`.agents/skills/`, and `.codex/skills/`. From the repository root use
`scripts/sync-skills.sh` to create or check runtime copies. Do not edit adapter
copies directly. No runtime-specific assumptions are baked into this source.

## Version History

- v0.1.0 (2026-05-29): Initial legacy document evidence intake and format
  normalization skill. Converts Excel / Word / PowerPoint / Visio / PDF / image
  / scanned documents into Markdown / CSV / PDF / PNG / SVG with manifests,
  evidence coordinates, and `ready` / `ready_with_warnings` / `blocked` quality
  gates. Static-only macro policy, honest-conversion policy, optional Docling
  as a non-canonical enhancer. Pre-normalization entry layer before
  `legacy-flow-context-normalizer`; routes unauthorized/unknown-sensitivity
  material to `legacy-ibmi-evidence-intake`.
