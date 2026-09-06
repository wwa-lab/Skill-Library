# Screen/Report Analysis Review Checklist

**Document:** `screen-report-analysis-<OBJ-ID>.md`

**Reviewer:** ________________  **Date:** ________________

**Review Status:** ☐ Pass  ☐ Pass with Warnings  ☐ Blocked

---

## Structural Completeness

- [ ] Artifact metadata (OBJ-ID, name, surface type, date, analyst) is present and correct
- [ ] Source evidence summary includes all DDS, spool, screenshot, or SME-note evidence items
- [ ] Surface type (DSPF / PRTF / MENU / Screen Sample / Spool Sample) is clearly identified
- [ ] Layout summary section describes visual structure and DDS record formats
- [ ] Fields and Indicators section includes all DDS-defined fields with names, roles, types, lengths, edit codes/masks
- [ ] User Actions section documents all function keys and command keys; program actions are mapped only with evidence
- [ ] Subfile behavior section is complete (if screen has subfiles) or marked N/A
- [ ] Report structure section is complete (if PRTF or spool report) or marked N/A
- [ ] Program Touchpoints section links to EXFMT/WRITE/READ programs in inventory
- [ ] Observed Behaviors section documents behaviors visible in runtime evidence
- [ ] Inferred Questions section lists candidate downstream seeds
- [ ] TBD Ledger is present with blocking status for each open item
- [ ] SME Review Checklist is complete with reviewer sign-off

## Evidence & Traceability

- [ ] Every field is tagged with at least one `EV-*` link (DDS source or runtime sample)
- [ ] Every indicator is linked to evidence showing its purpose (keyword, program usage, or spool sample)
- [ ] Every function key and command key is linked to evidence (DDS keyword or SME note)
- [ ] Subfile behavior (if present) separates DDS keywords from program-controlled load/clear/paging behavior
- [ ] Report control-break logic references program/O-spec evidence, runtime spool reconciliation, or SME confirmation
- [ ] All `BEH-*` (observed behavior) items have at least one `EV-*` link
- [ ] All `SEED-*` (inferred question) items reference the fields or indicators that raised the question
- [ ] All `TBD-*` items have a category and resolution path

## IBM i / DSPF / PRTF Correctness

### DSPF-Specific (if applicable)

- [ ] Record format names are valid for the shop / IBM i naming convention and match source exactly
- [ ] Field roles (input/output/both/hidden/constant) are correct per DDS and program usage
- [ ] Field types match IBM i legal types (A = character, N = numeric, P = packed, S = zoned, D = date)
- [ ] Edit codes or masks (if specified) are valid for IBM i / shop standards
- [ ] Indicator numbers (#01–#99) are within valid range
- [ ] Indicator usage (ERRMSG, PROTECT, OVERLAY, INVISIBLE) matches DDS keywords
- [ ] Subfile keywords (SFLPAG, SFLSIZ, SFLDROP/SFLFOLD, SFLDLTPG, SFLCLR) are quoted exactly if present
- [ ] Function key naming (F01–F24, CA01–CA24, CF01–CF24) is correct
- [ ] No invented DSPF keywords or behavior is present

### PRTF-Specific (if applicable)

- [ ] Record format names are valid
- [ ] Page size, margins, overflow, spacing, and line count are documented from PRTF DDS or OVRPRTF evidence
- [ ] Control-break fields are actual fields in the report detail record
- [ ] Total/count fields are supported by program/O-spec, spool reconciliation, or SME evidence
- [ ] Page header, detail, subtotal, and grand-total sections are present
- [ ] Multi-column or multi-section layouts are explicitly documented
- [ ] No invented PRTF behavior, sort/filter, control-break, or calculation logic is present (unless explicitly marked `SEED-*` or `TBD-*`)

### Menu-Specific (if applicable)

- [ ] Menu type (CL menu, DSPF-based menu) is identified
- [ ] Options are listed with their function or program action
- [ ] Selection logic (single-select, multi-select, command-line entry) is clear
- [ ] Navigation between menus is documented

## Anti-Hallucination

- [ ] No field names are invented (all are present in DDS or spool sample)
- [ ] No indicator numbers are invented
- [ ] No function keys are invented
- [ ] No subfile behavior is fabricated
- [ ] No report calculations are invented without explicit `SEED-*` or `TBD-*` marking
- [ ] Field validation constraints (MINVAL, MAXVAL, RANGE, EDTCDE) come from DDS or are marked `SEED-*`
- [ ] Every claim about behavior is linked to evidence or marked as an inferred question

## Evidence Quality & Redaction

- [ ] No raw production data (customer names, account numbers, SSNs, transaction details) is visible
- [ ] Spool samples, screenshots, and job logs are redacted per `../../docs/data-collection-and-redaction.md`
- [ ] Evidence sensitivity is marked (redacted/safe) for each item
- [ ] DDS source code is not sensitive (contains no embedded credentials, API keys, or hardcoded data)

## TBD Handling

- [ ] All TBDs have a category: `pending_source`, `pending_program_context`, `pending_sme_judgment`, or `pending_redaction_review`
- [ ] All TBDs have a blocking status: `yes` (blocks handoff) or `no` (non-blocking, can proceed)
- [ ] Blocking TBDs have a clear resolution path (e.g., "SME clarification needed", "Program analysis required")
- [ ] No TBDs are masquerading as facts in the main narrative

## Downstream Readiness

- [ ] Analysis is complete enough for a program analyzer to correlate program logic with screen/report behavior
- [ ] Analysis is complete enough for a flow analyzer to understand user interactions and data movement
- [ ] Analysis is complete enough for module synthesis to understand user-facing screens and reports
- [ ] All object references (OBJ-*) and evidence references (EV-*) resolve to known items in `01_inventory/inventory.yaml`

## SME Review Adequacy

- [ ] For interactive screens affecting transaction entry: SME has reviewed field validation, function keys, subfile behavior, and error handling
- [ ] For compliance or financial reports: SME has reviewed control breaks, totals, and report structure
- [ ] For critical business screens/reports: SME has signed off on the analysis
- [ ] For non-critical presentations: SME review is recommended but may be deferred if all facts are source-derived

## Overall Assessment

| Criterion | Pass | Warn | Fail | Notes |
|-----------|------|------|------|-------|
| Completeness | ☐ | ☐ | ☐ | |
| Correctness | ☐ | ☐ | ☐ | |
| Evidence | ☐ | ☐ | ☐ | |
| Redaction | ☐ | ☐ | ☐ | |
| Anti-Hallucination | ☐ | ☐ | ☐ | |
| SME Involvement | ☐ | ☐ | ☐ | |
| Downstream Readiness | ☐ | ☐ | ☐ | |

## Findings & Recommendations

### Blocking Issues (if Status = Blocked)

1. 
2. 

**Required Action:** [Specify what must be fixed or clarified]

### Warnings (if Status = Pass with Warnings)

1. 
2. 

**Recommendation:** [Suggest how to address before downstream use]

### Approved Items (if Status = Pass)

[Confirm readiness for flow/module analysis; note any recommended follow-up]

---

**Reviewer Signature:** ________________  **Date:** ________________

**SME Sign-Off (if Required):** ________________  **Date:** ________________
