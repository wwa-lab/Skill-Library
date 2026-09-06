---
name: legacy-ibmi-screen-report-analyzer
description: Analyze IBM i DSPF, PRTF, menus, subfiles, function keys, indicators, screen samples, spool/report samples, and presentation-layer behavior with evidence backing. Use when screen/report artifacts need structured analysis before or alongside program/flow analysis. Layer 1 (platform-specific) skill of the Legacy Spec Factory reverse chain.
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

# IBM i Screen & Report Analyzer

## Purpose

Create a detailed analysis of IBM i display files (DSPF), printer files (PRTF), menu definitions, subfile behavior, function keys, indicators, field-level presentation logic, report layouts, report sections, and related runtime evidence. This skill does not generate modernization code or infer business rules from presentation alone. It produces evidence-backed analysis of the presentation layer ready for SME validation and downstream capability modeling.

## Pipeline Position — Conditionally Required

This skill is **mandatory** (not optional) when
`inventory.yaml.sme_review.downstream_required.screen_report_analyzer.required: true`.
The inventory skill auto-detects this trigger from DSPF / PRTF / menu
objects; the SME confirms during the same single batched signoff that
confirms criticality. Full trigger rules:
[`skills/legacy-ibmi-inventory/references/downstream-triggers.md`](../legacy-ibmi-inventory/references/downstream-triggers.md).

Once triggered, the orchestrator's `3b Program Analysis Done` gate
refuses to advance until every triggered DSPF/PRTF/menu has an approved
`screen-report-analysis.md`. Without this enforcement, ~40% of real
screen-driven business rules (F-key bindings, conditional field
attributes, subfile control semantics) slip through into ad-hoc
`program-analysis.md` prose.

For tiny modules with no display files, the skill is correctly skipped
(`downstream_required.screen_report_analyzer.required: false`) and adds
no overhead.

## Inputs

Accept any combination of:

- DSPF DDS source (display files with record formats, field definitions, indicators)
- PRTF DDS source (printer-file layout, page size, record formats, fields,
  spacing, and formatting)
- *MENU definitions or menu command exports
- screen captures or terminal screenshots
- spool files or report samples (redacted per `../../docs/data-collection-and-redaction.md`)
- job logs related to report generation
- RPGLE/CLLE/COBOL snippets only when needed to understand indicator usage,
  EXFMT, WRITE, READ, O-specs, or report-control logic
- SME notes on screen flow, field validation, report control breaks, or presentation intent

**Required:**
- Screen/report source or sample must be referenced in an approved `01_inventory/inventory.yaml` via object ID (OBJ-*)

**Stop conditions:**
- inventory is missing or not approved
- OBJ-* cannot be located in inventory
- raw production data (customer accounts, SSNs, transaction details) is unredacted
- screen/report sample contains sensitive data without redaction review per `../../docs/data-collection-and-redaction.md`
- only screenshots exist and they cannot be tied to an inventory object,
  current DDS/source, controlled job log, or SME-reviewed runtime capture
- field meaning, function-key action, or report calculation requires business
  judgment not present in source, runtime evidence, program analysis, or SME
  notes

## Output Contract

Produce:

- `screen-report-analysis-<OBJ-ID>.md` per screen/report (one file per analysis session)

Use:

- `templates/screen-report-analysis.md` as starting point
- `references/output-contract.md` for field definitions and evidence tagging
- `references/dspf-screen-patterns.md` for DSPF pattern recognition
- `references/prtf-report-patterns.md` for PRTF pattern recognition
- `references/runtime-evidence.md` for spool/report sample analysis

Follow:

- `../../docs/id-conventions.md` for stable IDs (OBJ-*, EV-*, BEH-*,
  IN-*, OUT-*, DATA-*, SEED-*, TBD-*)
- `../../docs/evidence-and-knowledge-taxonomy.md` for evidence strength labels
- `../../docs/input-readiness-rubric.md` for input readiness scoring

Examples:

- `examples/interactive-subfile-positive/` — subfile screen with edit, function keys, record-level validation
- `examples/printed-report-positive/` — report layout and spool sample with header, detail, subtotal-like, and trailer-like sections
- `examples/incomplete-evidence-negative/` — negative case: missing DDS or spool sample, TBD handling

## Step Contract

This skill is one step in the Legacy Spec Factory reverse chain. It conforms
to the canonical Step Contract shape — see
`../legacy-step-contract/SKILL.md` and
`../legacy-step-contract/references/step-contract.md` for the full
field-level rules. The summary below is normative for this skill.

### Input

- **Required**: one DSPF, PRTF, or MENU DDS source file, or screen/report runtime sample; the object's `OBJ-*` ID located in an `approved` (or `approved_with_non_blocking_tbd`) `01_inventory/inventory.yaml`.
- **Optional**: related RPGLE/CLLE/COBOL source snippets showing indicator usage or EXFMT/WRITE/READ logic; SME notes on field validation, user workflows, or report control breaks; program analysis artifacts that reference this screen/report.
- **Input readiness scoring**:
  - `0-5 blocked`: approved inventory missing, target DSPF/PRTF/menu object
    unresolved, display/report source or controlled sample missing, or
    evidence authorization unresolved.
  - `6 minimum_pass`: approved inventory plus authoritative DSPF/PRTF/menu
    source or controlled runtime sample is present; missing user meaning
    becomes TBDs.
  - `7-8 usable`: screenshots, sample spool output, related program snippets,
    and navigation/report context are supplied.
  - `9-10 strong`: screen recordings, role-specific SME notes, function-key
    behavior, error/message examples, and report reconciliation samples are
    also supplied.
  - Missing screenshots or SME notes does not block layout/report extraction;
    it limits workflow interpretation.
- **Readiness checks**: Inventory Completeness Gate passing; object is not marked `blocked` in inventory; evidence authorization is resolved; DDS source is current or runtime sample is from controlled execution.
- **Stop conditions**: source missing or incomplete; object marked `blocked` in inventory; `OBJ-*` not found in inventory; unauthorized raw production data present; field meaning cannot be understood without business context.

### Execution

- **Procedure**: see the Workflow section below (9 ordered steps).
- **Allowed inference**: visual layout from DSPF/PRTF keywords and DDS record
  format definitions; indicator context from keywords such as ERRMSG,
  PROTECT, DSPATR, and display conditioning; subfile dimensions from SFLPAG
  and SFLSIZ; field formatting from EDTCDE/EDTWRD/EDTMSK; validation
  constraints from DDS keywords such as COMP, RANGE, VALUES, CHECK, and
  MANDATORY; report layout and pagination from PRTF DDS; report print order,
  control breaks, and total calculations only from program O-specs / WRITE
  logic, runtime spool evidence, or SME confirmation.
- **Forbidden assumptions**: inventing field names, function keys, indicators,
  subfile behavior, or report section structure not present in evidence;
  treating CA/CF labels as business actions without program or SME evidence;
  deriving business meaning from field labels without confirmation; reading
  non-redacted evidence; assuming field validation is business-critical without
  SME input; treating PRTF layout as proof of calculation semantics.
- **TBD handling**: missing DDS → `TBD: pending_source`; unclear indicator usage → `TBD: pending_program_context`; field business meaning unknown → `TBD: pending_sme_judgment`; report total calculation unclear → `TBD: pending_sme_judgment`; non-blocking gaps tagged `non_blocking`.

### Output

- **Canonical artifact**: `screen-report-analysis-<OBJ-ID>.md` (one per screen/report).
- **Required sections**: artifact metadata, source evidence summary, surface type, layout summary, fields and indicators, user actions/function keys/command keys, subfile behavior (if applicable), validation/error message surfaces, report sections/breaks/pagination (if applicable), program touchpoints, observed behaviors, inferred questions (clearly marked), TBD ledger, SME review checklist.
- **Required IDs**: reuses `OBJ-*` and `EV-*` from inventory / evidence
  intake; mints screen/report-local `BEH-*`, explicit `IN-*` / `OUT-*` /
  `DATA-*` items when field movement is evidenced, `SEED-*`, and `TBD-*`.
  Does not mint `BR-*`, `CAP-*`, `DEC-*`, or Java implementation IDs.
- **Handoff status**: `status: draft` or `needs_sme_review` until SME review
  is explicitly recorded. A smoke-test summary, preview, or analysis with
  pending SME sign-off must not report `approved` or
  `approved_with_non_blocking_tbd`. Downstream flow/module/spec skills require
  `approved` or `approved_with_non_blocking_tbd`.

### Validation

- **Mechanical**: every non-trivial field, indicator, or report section has ≥1 `EV-*` link; every function key or command key has DDS/runtime evidence and program-action evidence when an action is claimed; every TBD has a blocking-status tag; required sections all present.
- **AI semantic**: fields and indicators are consistent with linked DDS lines or spool samples; no invented fields, indicators, function keys, subfile logic, or report structure; evidence strength not overstated (no `weakly_inferred` posing as `confirmed_from_code`); layout descriptions reconciled against both DDS and runtime samples when both exist.
- **SME / human approval**: SME confirms field labels and validation, subfile behavior realism, report section/break logic, function key mapping accuracy, indicator usage, and presentation intent when questions exist. Required when the screen/report affects transaction entry, critical data output, compliance reporting, or financial calculations.
- **Blocking conditions**: any `BEH-*` without evidence; any invented IBM i DSPF/PRTF fact; any unresolved `pending_source` TBD on a screen element or report section that downstream analysis depends on; SME absence when the screen/report is load-bearing for a program's functionality or a report's compliance purpose.

Emit a Step Validation Report (see
`../legacy-step-contract/templates/step-validation-report.md`) with
status `pass`, `pass_with_warnings`, or `blocked` when reporting upward
to the orchestrator.

## Workflow

1. **Select Screen/Report & Verify Inventory**
   - Accept object ID (OBJ-*) from approved `01_inventory/inventory.yaml`
   - Confirm object name, type (DSPF, PRTF, or MENU), library, and description
   - Stop if object is marked `blocked` or inventory is not approved
   - Document source location and collection date

2. **Classify Surface Type**
   - Identify whether this is an interactive display file (DSPF, subfile-based menu), a printed report (PRTF), a CL menu, or a runtime screen/spool sample
   - Note if multiple formats or modes exist (browse mode vs. edit mode, multiple report sections)
   - Document visibility constraints (PROTECT keywords, INVISIBLE keywords if using DSPF)

3. **Extract Record Formats & Fields**
   - For DSPF: list all record formats from DDS; for each format, document field roles (input, output, both, hidden, constant/message)
   - For PRTF: list all record formats and their position in the page/report sequence
   - For each record format, extract fields: name, role (input, output,
     both, hidden, message, constant), type, length, decimal places, edit code
   - Tag each field with evidence strength (confirmed from code, observed in runtime, needs sme review)

4. **Document Indicators & Edit Codes**
   - Extract all indicators (#01-#99, named response indicators, and
     conditioned keywords) and document the keyword context where they appear
   - For field edit codes or masks (EDTCDE, EDTWRD, EDTMSK), document display
     formatting only; do not treat formatting as business validation
   - For report control fields, document only what is evidenced by program
     O-specs / WRITE logic, spool samples, or SME notes
   - Mark ambiguous indicator usage as TBD pending program context

5. **Analyze User Actions & Navigation**
   - Extract function keys (F1-F24) and command keys (CA/CF keywords) from
     DSPF or menu definitions
   - Document only key availability and label from DDS; map to program action
     only when program analysis, job log, or SME notes support it
   - For subfile screens, document page-up/page-down, select/deselect logic, and single-row vs. bulk action patterns
   - Identify error message surfaces (keywords ERRMSG, ERRSFL)

6. **Analyze Subfile Behavior (if applicable)**
   - Extract subfile dimensions (SFLPAG, SFLSIZ)
   - Document record-selection behavior (selection field position, single vs. multiple, action per selection)
   - Document subfile keywords exactly as written and separate DDS-declared
     behavior from program-controlled load, clear, and paging behavior
   - Identify subfile-clearing and load/reload patterns from DDS, program evidence, runtime evidence, or SME notes

7. **Analyze Report Structure (if PRTF)**
   - Extract page size, margins, overflow, spacing, and field placement from
     PRTF DDS
   - Identify report sections by combining PRTF record formats, program WRITE
     order / O-specs, spool samples, and SME notes
   - Document control-break fields and total accumulation fields only when
     evidenced outside layout labels
   - Identify multi-column layouts, report groups, or section separation keywords
   - Tag any calculated totals with evidence source (program logic,
     O-specs/output specs, runtime spool reconciliation, or SME confirmation)

8. **Correlate with Program Evidence**
   - If program analysis is available for programs that EXFMT or WRITE to this screen/report, cross-reference:
     - indicator setting logic in the program
     - field pre-population or default values
     - error handling and error message mapping
   - Document any contradictions between DDS definition and program behavior as TBDs

9. **Compile TBD Ledger, Validation Checklist, and Handoff Status**
   - List all `TBD-*` items with blocking status and resolution path
   - Provide a checklist for SME review covering field validation realism, subfile behavior, function key mapping, report structure, and overall presentation flow
   - Mark handoff status as `draft`, `needs_sme_review`, `approved`, or `approved_with_non_blocking_tbd`

## Workflow State Write-Back (history only — supplemental)

This is a supplemental Layer 1 skill. It analyzes DSPF / PRTF / subfile /
menu artifacts that strengthen evidence for downstream program / flow /
module analysis, but does NOT advance the main linear stage. It does NOT
mutate `capabilities[].stage_id` or `current_focus`.

After a run, append one `history[]` entry to
`<project-root>/workflow-state.yaml` per
[`docs/workflow-state-contract.md`](../../docs/workflow-state-contract.md):

```yaml
history:
  - at: <ISO 8601>
    skill: legacy-ibmi-screen-report-analyzer
    capability_id: <CAP-* from current_focus, or null if module-scoped>
    stage_after: <UNCHANGED stage_id>
    artifact: <path to the screen/report analysis, e.g. 02_programs/<MODULE>/<OBJ>/screen-report-analysis.md>
    note: "analyzed <DSPF | PRTF | menu | subfile> for <OBJ-*>"
```

Also overwrite `project.last_updated_at` / `project.last_updated_by`.

**Permitted side-effect:** if the analysis uncovers new TBDs or evidence
gaps, you MAY append to `capabilities[<CAP-*>].blocking.tbds`. You MUST
NOT change `stage_id`, `last_artifact`, or `last_skill`.

If `workflow-state.yaml` does not exist, this skill does NOT create it.

## Review Checklist

- [ ] All fields in the screen/report layout have names, roles, and types consistent with DDS or runtime evidence
- [ ] All indicators have their DDS keyword context documented; purpose is confirmed by program or SME evidence when needed
- [ ] All function keys and command keys are listed; program actions are mapped only with supporting evidence
- [ ] Subfile behavior (if present) is documented: page size, record selection, paging logic
- [ ] Report structure (if PRTF) includes header, detail, break/subtotal, footer/grand total sections
- [ ] Any field validation (min/max, range, edit code) is documented and tagged with evidence
- [ ] Calculated totals in reports are marked as derived from program/O-spec evidence, spool reconciliation, or SME confirmation
- [ ] All TBDs are listed with blocking status and resolution owner
- [ ] No invented fields, indicators, subfile logic, or report sections are present
- [ ] Evidence is redacted and no sensitive customer/account data is visible
- [ ] SME has reviewed critical screens/reports and confirmed validation, behavior, and business intent
- [ ] Handoff status is `approved` or `approved_with_non_blocking_tbd` before use in downstream flow/module analysis

## Handoff

Screen/report analysis is ready for downstream use when:

1. All required sections are present and complete
2. Every field, indicator, subfile behavior, and report section is linked to DDS source, program evidence, runtime evidence, or SME confirmation
3. All invented facts have been removed or reclassified as TBDs
4. SME has reviewed the analysis and approved (`decision: approved`) or approved with non-blocking TBDs (`decision: approved_with_non_blocking_tbd`)
5. Blocking TBDs are resolved or explicitly documented as preventing the next stage
6. The analysis is ready to be referenced by downstream flow analysis (`legacy-ibmi-flow-analyzer`) or field-level data modeling

No-write smoke tests and draft previews must report the canonical artifact
filename, allowed and forbidden ID namespaces, unresolved `TBD-*` / `SEED-*`
items, and a non-approved handoff status unless SME approval is part of the
provided evidence.

## Version History

- v0.2.0 (2026-05-16): Promoted from "optional supplemental" to
  "conditionally required". When `inventory.yaml.sme_review.downstream_required.screen_report_analyzer.required: true`,
  this skill becomes a mechanically enforced prerequisite for `3b
  Program Analysis Done` — no more screen-driven rules slipping into
  ad-hoc program-analysis prose. Inventory auto-detects DSPF / PRTF /
  menu objects and SME confirms in the batched inventory signoff.
- v0.1.0 (2026-05-16): Initial screen/report analyzer. Positive no-write
  smoke test passed in Codex CLI (`gpt-5.4-mini`), Claude Code (`haiku`), and
  OpenCode (`opencode/minimax-m2.5-free`); artifact remains repo-ready pending
  SME/domain validation with real redacted DSPF/PRTF evidence.
