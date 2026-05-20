# Screen/Report Analysis: <OBJ-ID>

**Artifact Metadata**

| Field | Value |
|-------|-------|
| Object ID | <OBJ-ID> |
| Object Name | |
| Surface Type | DSPF / PRTF / MENU / Screen Sample / Spool Sample |
| Analysis Date | |
| Analyst | |
| Status | draft / needs_sme_review / approved / approved_with_non_blocking_tbd |

## Source Evidence Summary

| Evidence ID | Source Type | Location | Sensitivity | Notes |
|-------------|-------------|----------|-------------|-------|
| EV-* | DDS source / screenshot / spool sample / SME note | | redacted/safe | |

## Surface Type Classification

**Type:** [DSPF / PRTF / MENU / Interactive Screen / Printed Report Sample]

**Description:** [Brief purpose of the screen or report]

**Related Objects:** [OBJ-* IDs for programs that EXFMT/WRITE to this screen; OBJ-* IDs for files referenced]

## Layout Summary

### Overall Dimensions (DSPF)
- Record Format Names: 
- Field Roles Present: (input, output, both, hidden, constant/message)
- Position on Screen: (top left, centered, etc. if relevant)

### Overall Dimensions (PRTF)
- Record Format Names:
- Page Size: (width × height, lines per page)
- Print Position: (beginning of page, middle, continuation)

### Visual Description
[Describe the visual layout as it appears on screen or in spool output. Reference DDS keywords or screenshot evidence.]

## Fields and Indicators

### Field Inventory

| Field Name | Role | Type | Length | Dec | Edit Code / Mask | Indicators / Conditions | Evidence | Notes |
|------------|------|------|--------|-----|------------------|-------------------------|----------|-------|
| | input/output/both/hidden/constant | | | | | | EV-* | |

**Legend:**
- Type: character (A), numeric (N), packed (P), zoned (S), date (D)
- Edit Code: EDTCDE keyword or format
- Indicators: indicator numbers controlling display/input/protection (e.g., 01, 02)
- Evidence: EV-* link; mark confidence level

### Indicator Mapping

| Indicator | Purpose | Set By | Cleared By | Evidence | Notes |
|-----------|---------|--------|-----------|----------|-------|
| #01 | | | | EV-* | |

**Indicator Codes:**
- Error indicator: used to display error messages
- Protection indicator: controls PROTECT keyword (field not enterable)
- Overlay indicator: controls field display via OVERLAY keyword
- Visibility indicator: INVISIBLE keyword if used

## User Actions & Navigation

### Function Keys & Command Keys

| Key | DDS Label / Response | Confirmed Program Action | Evidence | Notes |
|-----|----------------------|--------------------------|----------|-------|
| F1 | | TBD unless program/SME evidence exists | EV-* | |
| CA01 | | | EV-* | |

**For Interactive Screens:**
- Document any special command-key handling (CA01–CA24, CF01–CF24)
- Note any immediate-exit behavior (pressing Enter vs. requiring a function key)

## Subfile Behavior (if applicable)

**Subfile Definition**

| Property | Value | Evidence |
|----------|-------|----------|
| Subfile Record Format Name | | EV-* |
| Page Size (SFLPAG) | rows/page | EV-* |
| Subfile Size (SFLSIZ) | total rows | EV-* |
| Selection Field Name | | EV-* |
| Selection Field Position | | EV-* |

**Record Selection Logic**

- Single-select or multi-select: 
- Action trigger: (F-key, Enter, automatic)
- Return field(s): (which fields are returned to program)
- Evidence: EV-*

**Paging Behavior**

- DDS-declared subfile keywords: (SFLPAG, SFLSIZ, SFLDROP/SFLFOLD, SFLDLTPG, SFLCLR)
- Program/runtime paging behavior:
- Clear trigger: (automatic, program-controlled via clear indicator)
- Load/reload pattern: (single load, repeated loads, refresh on error)
- Evidence: EV-*

## Validation & Error Message Surfaces

| Field | Validation | Error Message | Indicator | Evidence |
|-------|-----------|---------------|-----------|----------|
| | | | | EV-* |

**Validation Types:**
- MINVAL / MAXVAL (numeric range)
- RANGE (value list)
- LENGTH (character length already enforced by field definition)
- EDTCDE (edit code formatting)
- Custom (set by program logic)

## Report Structure (PRTF / Spool Sample)

### Page Layout

| Section | Record Format | Lines | Trigger | Evidence |
|---------|---------------|-------|---------|----------|
| Header | | | page start | EV-* |
| Detail | | | per record | EV-* |
| Subtotal | | | on control break | EV-* |
| Grand Total | | | page/report end | EV-* |

### Control Breaks & Totals

| Control Field | Break Trigger | Subtotal Fields | Accumulation Logic | Evidence |
|---------------|---------------|-----------------|-------------------|----------|
| | | | | EV-* |

**Notes:**
- List the control field (e.g., customer ID, month, region)
- Identify which numeric fields are summed, counted, or averaged on break
- For calculated totals, mark whether the formula is evidenced by program/O-spec
  logic, spool reconciliation, or SME confirmation; labels alone are seeds/TBDs

## Input / Output / Data Contract Items (if needed)

Create these IDs only when a stable field-level contract is useful downstream
and evidence supports it.

| ID | Type | Field / Surface | Direction | Evidence | Notes |
|----|------|-----------------|-----------|----------|-------|
| IN-* / OUT-* / DATA-* | input/output/data_movement | | | EV-* | |

### Multi-Column or Multi-Section Layout

[Describe if the report has side-by-side columns, multiple detail sections, or conditional layout based on indicators]

## Program Touchpoints

| Program | EXFMT/WRITE/READ | Details | Evidence |
|---------|------------------|---------|----------|
| OBJ-* | EXFMT | | EV-* |

**Indicator Correlation:**
- [List any indicator settings made by the program; mark any discrepancies with DDS definition as TBD]

## Observed Behaviors

### From Runtime Evidence (Spool / Screenshots)

| Behavior ID | Description | Observed In | Confidence | Evidence | Notes |
|-------------|-------------|-------------|-----------|----------|-------|
| BEH-* | | spool sample / screenshot | high/medium/low | EV-* | |

**Examples:**
- Page 2 starts with the same column headings as page 1
- A subtotal-like line is visible after each customer group in the spool sample
- Error-state screenshot shows message text in the message subfile area

## Inferred Questions (Candidate Downstream Seeds)

[List questions raised by the analysis that downstream business rule or capability analysis might address. Mark each as `SEED-<SLUG>-<NNN>`.]

| Seed ID | Question | Related Fields / Indicators | Downstream Owner |
|---------|----------|---------------------------|------------------|
| SEED-* | Should field X be editable in all modes or only in add mode? | | |
| SEED-* | Is the subtotal logic in the report a business requirement or an artifact of the print program's implementation? | | |

## TBD Ledger

| TBD ID | Issue | Category | Blocking | Resolution Path | Owner |
|--------|-------|----------|----------|-----------------|-------|
| TBD-* | [Description] | pending_source / pending_program_context / pending_sme_judgment | yes/no | | |

**Categories:**
- `pending_source`: Missing DDS or runtime evidence
- `pending_program_context`: Indicator or subfile logic unclear without program analysis
- `pending_sme_judgment`: Field meaning, validation realism, or business intent unknown
- `pending_redaction_review`: Evidence requires redaction assessment

## SME Review Checklist

- [ ] Field names, types, and edit codes are correct
- [ ] Indicator usage and error message mapping are accurate
- [ ] Subfile behavior (paging, selection, record deletion) is correct
- [ ] Function key mappings to program actions are verified
- [ ] Report control breaks and totals are correct
- [ ] Validation logic (min/max, range, edit code) is realistic
- [ ] Overall screen/report flow and presentation intent are captured
- [ ] No invented fields, indicators, or report sections are present
- [ ] All blocking TBDs are resolved or documented
- [ ] Evidence is properly redacted

**SME Sign-Off**

| Field | Value |
|-------|-------|
| SME Name | |
| SME Role | IBM i / DSPF / PRTF expert |
| Review Date | |
| Decision | approved / approved_with_non_blocking_tbd / blocked |
| Notes | |

## Handoff Status

| Status | Value |
|--------|-------|
| Analysis Complete | draft / needs_sme_review / approved |
| Ready for Flow Analysis | yes / no |
| Ready for Module Analysis | yes / no |
| Non-Blocking TBDs | [list if any] |
| Blocking Issues | [list if any] |
