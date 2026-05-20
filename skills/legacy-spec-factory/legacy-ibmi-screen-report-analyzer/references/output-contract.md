# Screen/Report Analysis Output Contract

This document defines the canonical structure, required fields, ID usage, and evidence tagging for screen and report analysis artifacts produced by `legacy-ibmi-screen-report-analyzer`.

## Canonical Artifact

**File Name:** `screen-report-analysis-<OBJ-ID>.md`

**Location:** Typically placed in:
- `02_screens/<CAPABILITY-SLUG>/screen-report-analysis-<OBJ-ID>.md` (in Analysis Output Repo)
- Or same directory as related program analysis

**Format:** Markdown with frontmatter (if using YAML), structured sections, and ID-tagged evidence.

## Required Sections

Every analysis must include these sections, even if content is minimal:

1. **Artifact Metadata**
   - Object ID (OBJ-* from inventory)
   - Object name
   - Surface type (DSPF, PRTF, MENU, interactive screen sample, spool/report sample)
   - Analysis date
   - Analyst name
   - Review status (draft, needs_sme_review, approved, approved_with_non_blocking_tbd)

2. **Source Evidence Summary**
   - Table listing all evidence items (EV-* IDs)
   - Evidence type (DDS source, screenshot, spool sample, SME note, job log)
   - Location reference
   - Sensitivity assessment (redacted/safe/unknown)

3. **Surface Type Classification**
   - Classification (DSPF / PRTF / MENU / Screen Sample / Spool Sample)
   - Presentation purpose or description; business purpose only when confirmed
     by SME or upstream artifact
   - Related objects (OBJ-* IDs for programs, files)

4. **Layout Summary**
   - For DSPF: record format names, field roles (input/output/both/hidden),
     and position on screen
   - For PRTF: record format names, page dimensions, line count, spacing, and
     field positions
   - Visual description or reference to screenshot

5. **Fields and Indicators**
   - Comprehensive field inventory table with: name, role, type, length, decimal places, edit code/mask, associated indicators
   - Indicator mapping table: indicator number, keyword context, set-by source, cleared-by source
   - Each field linked to evidence (EV-*)

6. **User Actions & Navigation**
   - Function keys (F1-F24) and command keys (CA01-CA24, CF01-CF24)
   - DDS labels / response indicators and program actions only when evidenced
   - For subfiles: select/deselect, paging, record-level actions

7. **Subfile Behavior** (if applicable)
   - Subfile record format name, page size (SFLPAG), subfile size (SFLSIZ)
   - Selection logic (single/multi-select, action trigger)
   - DDS-declared paging/display keywords and program-controlled load/clear
     behavior, kept separate
   - Load/reload/clear triggers

8. **Validation & Error Messages**
   - Fields with validation constraints
   - Validation type (MINVAL, MAXVAL, RANGE, EDTCDE, custom program logic)
   - Error message display (ERRMSG keyword, indicator)
   - Confidence and evidence for each

9. **Report Structure** (PRTF / Spool)
   - Page layout: header, detail, subtotal, grand total sections
   - Control breaks: control field, trigger, subtotal fields, accumulation
     logic, with program/spool/SME evidence
   - Multi-column or multi-section layouts if present
   - Evidence for calculated totals (program/O-spec evidence, spool reconciliation, or SME confirmation)

10. **Program Touchpoints**
    - Programs that EXFMT or WRITE to this screen/report (OBJ-*)
    - Indicator correlation (indicator set/tested by program)
    - Discrepancies between DDS and program behavior (marked as TBD)

11. **Observed Behaviors**
    - From runtime evidence (spool samples, screenshots)
    - BEH-* IDs for each behavior
    - Confidence level (high/medium/low)
    - Evidence link (EV-*)

12. **Inferred Questions**
    - Candidate seeds (SEED-*) for downstream business rule / capability analysis
    - Questions that require SME judgment
    - Related fields and indicators

13. **TBD Ledger**
    - Every open question or unknown fact
    - TBD-* ID, category, blocking status, resolution path, owner
    - Categories: pending_source, pending_program_context, pending_sme_judgment, pending_redaction_review

14. **SME Review Checklist**
    - Checklist items for SME validation
    - SME sign-off: name, role, review date, decision (approved / approved_with_non_blocking_tbd / blocked)

15. **Handoff Status**
    - Analysis complete (yes/no)
    - Ready for downstream use (flow analysis, module analysis)
    - Any blocking or non-blocking TBDs
    - Draft / smoke-test outputs must remain `draft` or `needs_sme_review`
      unless SME approval is explicitly included in the evidence bundle

## ID Usage Rules

### OBJ-* (Object)

- Reused from `01_inventory/inventory.yaml`
- One OBJ-* per screen or report analyzed
- Example: `OBJ-ORDER-ENTRY-003` for an order-entry screen

### EV-* (Evidence)

- Reused from inventory / evidence intake. Do not mint new `EV-*` directly in
  this skill unless the local evidence-governance step has assigned it first.
- One EV-* per distinct evidence item (DDS source file, screenshot, spool
  sample, job log, program excerpt, SME note)
- Link evidence in tables and narrative
- Example: `EV-ORDER-ENTRY-012` for a DDS member, `EV-ORDER-ENTRY-013` for a spool sample

### BEH-* (Observed Behavior)

- Minted locally within this analysis (does not exist in inventory)
- One BEH-* per observable behavior seen in runtime evidence
- Format: `BEH-<CAPABILITY-SLUG>-<NNN>` (use same slug as OBJ-*)
- Linked to at least one EV-*
- Example: `BEH-ORDER-ENTRY-001` for "subfile auto-refreshes on WRITE"

### IN-* / OUT-* / DATA-* (Field and Data Movement)

- Minted only when the artifact explicitly documents a field-level input,
  output, or data movement that is evidenced by DDS plus program/runtime
  evidence.
- `IN-*` is for user-entered or externally supplied values visible at the
  surface.
- `OUT-*` is for values emitted to a screen, report, spool, or message surface.
- `DATA-*` is for movement across screen/report and program/file boundaries.
- Do not create these IDs for every field by default; create them when
  downstream flow/module analysis needs a stable contract item.

### SEED-* (Inferred Question)

- Minted locally within this analysis
- One SEED-* per inferred question for downstream analysis
- Format: `SEED-<CAPABILITY-SLUG>-<NNN>`
- Clearly marked as a question, not a fact
- Example: `SEED-ORDER-ENTRY-001` for "Is field X mandatory in all modes or only during add?"

### TBD-* (To Be Determined)

- Minted locally within this analysis
- One TBD-* per unresolved fact, missing evidence, or open question
- Format: `TBD-<CAPABILITY-SLUG>-<NNN>`
- Must include: issue description, category, blocking status, resolution path
- Example: `TBD-ORDER-ENTRY-003` for "Missing PRTF source for the invoice report"

### CAP-*, BR-*, DEC-*

- **NOT minted** in this skill
- Business rules (BR-*) are downstream from this analysis
- Capability IDs (CAP-*) and decision IDs (DEC-*) are outside the scope

## Evidence Tagging

Every claim must be tagged with evidence strength. Do not leave evidence implicit.

### Tagging Pattern

In tables, use one column per field:

```
| Field Name | Type | Evidence | Confidence | Notes |
|------------|------|----------|-----------|-------|
| CUSTNO | Numeric (5,0) | EV-001 (DDS CUSTNO field) | high | Confirmed from DDS |
| FNAME | Character (30) | EV-001, EV-002 (DDS + spool) | high | Observed in runtime |
| AMOUNT | Packed (9,2) | EV-001 | medium | DDS present, no spool evidence |
| CONTROL_BREAK | Not defined | TBD-001 | low | Inferred from spool subtotals |
```

In narrative, use inline tagging:

```
The field CUSTNO is a 5-digit numeric [EV-001: DDS keyword CUSTNO 5S 0, confirmed_from_code].
The subfile page size is 10 records [EV-002: DDS SFLPAG(10), confirmed_from_code].
Pressing F1 submits the form and returns to the menu [EV-003: SME note, confirmed_by_sme].
```

### Evidence Strength Labels

Use these labels when explicitly calling out confidence:

- `confirmed_from_code`: fact is directly present in DDS or source
- `observed_in_runtime`: fact is visible in spool sample, screenshot, or job log
- `confirmed_by_sme`: SME has verified or confirmed the fact
- `strongly_inferred`: strong inference from multiple evidence points
- `weakly_inferred`: plausible but under-supported (avoid if possible)
- `needs_sme_review`: fact is unclear and requires human judgment
- `missing`: required evidence has not been collected

## Coverage Completeness

A screen/report analysis is considered complete when:

### For DSPF (Interactive Screen)

- [ ] All record formats are listed
- [ ] All fields (input, output, both, hidden, constants/messages) are documented with name, role, type, length, edit code/mask
- [ ] All indicators (#01–#99) with DDS keywords are listed
- [ ] All function keys (F01–F24, CA01–CA24) are documented
- [ ] All validation constraints are noted (MINVAL, MAXVAL, RANGE, EDTCDE)
- [ ] Subfile dimensions and program-controlled load/clear behavior (if present) are fully separated
- [ ] Error message surfaces are identified
- [ ] Related programs (EXFMT/WRITE) are referenced
- [ ] Runtime evidence (screenshots, SME notes) is included and redacted

### For PRTF (Printer File) / Spool Report

- [ ] All record formats are documented
- [ ] Page layout (header, detail, subtotal, grand-total) is described
- [ ] All control-break fields and their triggers are listed with program,
  spool, or SME evidence
- [ ] All calculated totals are identified and sourced from program/O-spec
  evidence, spool reconciliation, or SME confirmation
- [ ] Page size, margins, line count are documented
- [ ] Multi-column or multi-section layouts are explicit
- [ ] Related programs (WRITE, OVRPRTF) are referenced
- [ ] Spool sample (if available) is included and redacted

### For MENU

- [ ] Menu type (CL or DSPF-based) is identified
- [ ] All options are listed with selection number and action/program
- [ ] Selection logic is documented
- [ ] Navigation between menus is clear

## Redaction & Safety

- [ ] No unredacted customer names, account numbers, SSNs, or transaction details in any evidence
- [ ] Spool samples have PII redacted or masked
- [ ] Screenshots have sensitive data obscured
- [ ] Job logs do not contain unredacted credentials or sensitive parameter values
- [ ] DDS source code itself should not contain embedded data or credentials

## Handoff Conditions

Analysis is ready for handoff to downstream skills when:

1. All required sections are complete
2. All fields and indicators are linked to evidence
3. All invented facts have been removed or marked as SEED-* or TBD-*
4. SME has reviewed and approved (if required by risk level or complexity)
5. All blocking TBDs are resolved or documented with resolution path
6. Evidence is properly redacted
7. Analysis status is `approved` or `approved_with_non_blocking_tbd`

Do not report `approved` or `approved_with_non_blocking_tbd` for a smoke-test
summary, preview, or artifact that has no explicit SME sign-off evidence.

## Versioning

If the analysis is revised, increment the version or revision ID:

- Version 0.1: initial draft
- Version 0.2: after first SME review feedback
- Version 1.0: after SME approval
- Version 1.1: after downstream use feedback

Record version changes in a header comment or frontmatter.
