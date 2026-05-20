# Screen Analysis: OBJ-ORDER-ENTRY-003

**Artifact Metadata**

| Field | Value |
|-------|-------|
| Object ID | OBJ-ORDER-ENTRY-003 |
| Object Name | ORDERENT (display file) |
| Surface Type | DSPF (interactive screen with subfile) |
| Analysis Date | 2026-05-11 |
| Analyst | Claude Code (skill: legacy-ibmi-screen-report-analyzer) |
| Status | draft |

## Source Evidence Summary

| Evidence ID | Source Type | Location | Sensitivity | Notes |
|-------------|-------------|----------|-------------|-------|
| EV-ORDER-ENTRY-012 | DSPF source | DEMO01/ORDERENT member | safe | Complete DDS definition, no embedded data |
| EV-ORDER-ENTRY-013 | Screenshot (normal state) | screen-entry-normal.png | redacted | Customer ID and total redacted |
| EV-ORDER-ENTRY-014 | Job log excerpt | JOBLOG.TXT | safe | Shows EXFMT sequence, no sensitive data |

## Surface Type Classification

**Type:** DSPF (Interactive Display File with Subfile)

**Description:** Order-entry display file with a main form area and a line-item subfile area. Source comments and labels suggest add/edit/delete intent, but save/delete business semantics remain pending program/SME confirmation.

**Related Objects:** 
- OBJ-ORDER-ENTRY-001 (program ORDERENT that uses this DSPF)
- OBJ-ORDERFILE-001 (physical file with order data)

## Layout Summary

### Overall Dimensions (DSPF)
- Record Format Names: MAINSCR, ORDDETAIL (subfile detail), ORDCTL (subfile control)
- Field Roles Present: input, output, protected output, subfile selection
- Screen Size: 24 rows × 80 columns (DSPSIZ(24 80))

### Visual Description
The screen displays a form-like interface. The top section (rows 1–7) contains order header information: order number (protected, output-only), customer ID (input field), order date (protected), and total amount (protected). Row 8 contains a label "Select items:" indicating the start of the subfile section. Rows 10–20 contain the subfile display area showing individual line items with columns for line number, item number, item description, quantity, unit price, and line amount. Row 23 shows function key labels (F1=Accept, F2=Cancel, F5=Refresh).

## Fields and Indicators

### Field Inventory

| Field Name | Role | Type | Length | Dec | Edit Code | Indicators / Conditions | Notes | Evidence |
|------------|------|------|--------|-----|-----------|-------------------------|-------|----------|
| ORDNO | input/protected by condition | A | 5 | - | - | #03 condition in DDS | Program meaning of #03 requires program evidence | EV-ORDER-ENTRY-012 |
| CUSTID | input | A | 5 | - | - | #04 condition in DDS | Mandatory in DDS; lookup semantics require program/SME evidence | EV-ORDER-ENTRY-012 |
| ORDDATE | input/protected by condition | A | 8 | - | DATFMT(*ISO) | #05 condition in DDS | Date format is source-evidenced; assignment semantics require program evidence | EV-ORDER-ENTRY-012 |
| TOTAL | output/protected by condition | N | 9 | 2 | A | #06 condition in DDS | Display formatting source-evidenced; formula requires program/SME evidence | EV-ORDER-ENTRY-012 |
| SEL | input | A | 1 | - | - | none | Selection value entered by user; action semantics require program evidence | EV-ORDER-ENTRY-012 |
| LINENO | output | N | 3 | 0 | - | none | Line number displayed in subfile | EV-ORDER-ENTRY-012 |
| ITEMNO | output | A | 5 | - | - | none | Item number displayed in subfile | EV-ORDER-ENTRY-012 |
| ITEMDESC | output | A | 30 | - | - | none | Item description displayed in subfile | EV-ORDER-ENTRY-012 |
| QTY | input | N | 5 | 0 | - | none | Quantity field; validation rules require program/SME evidence | EV-ORDER-ENTRY-012 |
| UNITPRICE | output | N | 8 | 2 | A | none | Displayed unit price; source of value requires program/file evidence | EV-ORDER-ENTRY-012 |
| LINEAMT | output | N | 9 | 2 | A | none | Displayed line amount; formula requires program/SME evidence | EV-ORDER-ENTRY-012 |

### Indicator Mapping

| Indicator | Purpose | Set By | Cleared By | Evidence | Notes |
|-----------|---------|--------|-----------|----------|-------|
| #01 | Error message condition in DDS | Program context required | Program context required | EV-ORDER-ENTRY-012 | `ERRMSG('Invalid input' 01)` ties #01 to message display; set/clear logic is program evidence |
| #03 | ORDNO field conditioning/protection context | Program context required | Program context required | EV-ORDER-ENTRY-012 | Exact mode behavior is TBD until program analysis confirms it |
| #04 | CUSTID field conditioning/error context | Program context required | Program context required | EV-ORDER-ENTRY-012 | DDS shows conditioning; lookup failure behavior requires program evidence |
| #05 | ORDDATE protection/display context | Program context required | Program context required | EV-ORDER-ENTRY-012 | Runtime screenshot shows protected display; set/clear logic pending |
| #06 | TOTAL protection/display context | Program context required | Program context required | EV-ORDER-ENTRY-012 | Runtime screenshot shows protected display; formula pending |
| #99 | Subfile clear condition | Program (refresh path in job log) | Program context required | EV-ORDER-ENTRY-012, EV-ORDER-ENTRY-014 | Job log supports clear/reload on refresh; other set/clear paths pending |

## User Actions & Navigation

### Function Keys & Command Keys

| Key | DDS Label / Response | Confirmed Program Action | Evidence | Notes |
|-----|----------------------|--------------------------|----------|-------|
| F1 | ACCEPT | pending program/SME confirmation | EV-ORDER-ENTRY-012, EV-ORDER-ENTRY-013 | Label is visible; save semantics are a downstream question |
| F2 | CANCEL | pending program/SME confirmation | EV-ORDER-ENTRY-012, EV-ORDER-ENTRY-013 | Label is visible; discard semantics require program/SME evidence |
| F5 | REFRESH | program sets subfile clear/reload path in job log | EV-ORDER-ENTRY-012, EV-ORDER-ENTRY-014 | Runtime evidence supports refresh behavior |
| F6 | DELETE | pending program confirmation for delete semantics | EV-ORDER-ENTRY-012 | DDS label alone is not enough to prove deletion logic |

### Subfile User Actions

- **Select Item**: User types any value in the SEL field (column 1 of subfile); typically "X" or "1"
- **Edit Quantity**: User types new QTY value in the QTY column of a subfile record
- **Page Down**: Screenshot sequence shows a changed visible row set after page-down; exact DDS/program mechanism remains pending program context
- **Page Up**: Page-up behavior not evidenced in this sample; leave as TBD unless runtime/program evidence is added

## Subfile Behavior

**Subfile Definition**

| Property | Value | Evidence |
|----------|-------|----------|
| Subfile Record Format Name | ORDDETAIL | EV-ORDER-ENTRY-012 |
| Page Size (SFLPAG) | 10 rows/page | EV-ORDER-ENTRY-012 |
| Subfile Size (SFLSIZ) | 100 total rows (maximum) | EV-ORDER-ENTRY-012 |
| Selection Field Name | SEL | EV-ORDER-ENTRY-012 |
| Selection Field Position | Column 1 of subfile detail record | EV-ORDER-ENTRY-012 |

**Record Selection Logic**

- **Single-select or multi-select:** Multi-select (user can mark multiple items via SEL field)
- **Action trigger:** F6 is labelled DELETE; actual delete processing requires program confirmation. F1 is labelled ACCEPT; save/submit semantics require program/SME confirmation.
- **Return field(s):** SEL, QTY (modified quantities); LINENO identifies which item
- **Evidence:** EV-ORDER-ENTRY-012 (DSPF definition), EV-ORDER-ENTRY-014 (job log showing F6 triggers deletion)

**Paging Behavior**

- **Page-up / Page-down:** Runtime screenshot sequence shows page-down changes the visible rows; DDS keyword is recorded but reload mechanism is program-controlled
- **Deletion behavior (SFLDLTPG):** Keyword not present in provided DDS; no page-delete behavior claimed
- **Clear trigger:** SFLCLR(99) is present; job log supports clear/reload on F5 only
- **Load/reload pattern:** Job log supports an F5 clear/reload path; initial load and mode-change behavior need program analysis
- **Evidence:** EV-ORDER-ENTRY-012 (SFLPAG(10), SFLDROP(05), SFLCLR(99)), EV-ORDER-ENTRY-013 (page-down screenshot sequence), EV-ORDER-ENTRY-014 (job log showing load pattern)

## Validation & Error Message Surfaces

| Field | Validation | Error Message | Indicator | Evidence |
|-------|-----------|---------------|-----------|----------|
| CUSTID | Mandatory (MANDATORY keyword); existence lookup requires program/SME evidence | Message text TBD | #04 context visible | EV-ORDER-ENTRY-012 |
| QTY | Numeric field; range/stock validation not present in DDS | TBD | Program-set indicator TBD | EV-ORDER-ENTRY-012; needs program analysis |

**Validation Types:**
- MANDATORY: CUSTID is required before order can be accepted
- Custom program validation: QTY range checking and stock availability are candidate questions, not confirmed facts
- Error Message Surface: ERRSFL(SUBFAIL 00) — errors display in subfile on indicator #00

## Program Touchpoints

| Program | EXFMT/WRITE/READ | Details | Evidence |
|---------|------------------|---------|----------|
| OBJ-ORDER-ENTRY-001 | EXFMT MAINSCR | Program displays MAINSCR and waits for user action; exact indicator set/clear paths need program analysis | EV-ORDER-ENTRY-014 |
| OBJ-ORDER-ENTRY-001 | WRITE ORDCTL + ORDDETAIL | Program writes subfile records; loop and positioning details need source confirmation | EV-ORDER-ENTRY-014 |
| OBJ-ORDER-ENTRY-001 | READ (implicit) | EXFMT receives user input: field values, function key pressed, selected items (SEL field) | EV-ORDER-ENTRY-014 |

**Indicator Correlation:**
- Indicator #03 (ORDNO protect context): mode-specific set/clear behavior pending program analysis
- Indicator #04 (CUSTID error context): lookup failure behavior pending program analysis
- Indicator #05, #06 (ORDDATE, TOTAL protect context): runtime shows protected display; complete set/clear behavior pending
- Indicator #99 (subfile clear): job log supports F5 refresh clear/reload path

## Observed Behaviors

### From Runtime Evidence (Screenshots & Job Log)

| Behavior ID | Description | Observed In | Confidence | Evidence | Notes |
|-------------|-------------|-------------|-----------|----------|-------|
| BEH-ORDER-ENTRY-001 | Page-down screenshot sequence shows the visible subfile rows change | EV-ORDER-ENTRY-013 (screen capture sequence) | medium | DDS confirms subfile dimensions; exact reload/scroll mechanism needs program context |
| BEH-ORDER-ENTRY-002 | When F5 (REFRESH) is pressed, subfile display clears (all records disappear), then repopulates with current data | EV-ORDER-ENTRY-014 (job log showing SFLCLR trigger) | high | SFLCLR(99) in DDS confirms; program sets #99 indicator |
| BEH-ORDER-ENTRY-003 | Selection field and F6 DELETE label are visible; delete effect requires program confirmation | EV-ORDER-ENTRY-013, EV-ORDER-ENTRY-014 | medium | Treat as observed surface plus downstream program question |
| BEH-ORDER-ENTRY-004 | When invalid CUSTID is entered and F1 (ACCEPT) is pressed, error message appears and screen is redisplayed without clearing order header | EV-ORDER-ENTRY-013 (error-state screenshot) | medium | Error message location and re-entry behavior observed; program logic inferred |

## Inferred Questions (Candidate Downstream Seeds)

| Seed ID | Question | Related Fields / Indicators | Downstream Owner |
|---------|----------|---------------------------|------------------|
| SEED-ORDER-ENTRY-001 | Is selecting an item via SEL field and F6 (DELETE) the only way to remove items from an order, or can items be modified in other modes? | SEL, QTY, F6 | Program analyzer / capability modeler |
| SEED-ORDER-ENTRY-002 | When F1 (ACCEPT) is pressed with selected items, does the program process deletions, quantity updates, and new items in a specific sequence? Are there any interdependencies? | SEL, QTY, F1 | Program analyzer |
| SEED-ORDER-ENTRY-003 | Should the target UI preserve the 10-row page size or treat it as a legacy presentation constraint? | SFLPAG(10) | Capability modeler / modernization decision |
| SEED-ORDER-ENTRY-004 | Are there any status codes or special item types that prevent editing or deletion from the order? | ITEMNO, ITEMDESC | SME business rule review |

## TBD Ledger

| TBD ID | Issue | Category | Blocking | Resolution Path | Owner |
|--------|-------|----------|----------|-----------------|-------|
| TBD-ORDER-ENTRY-001 | QTY field validation: MINVAL, MAXVAL, or custom program logic not visible in DSPF; stock availability check mentioned but DDS constraint unclear | pending_source | no | Review program I-specs and MONITOR block for QTY validation; cross-check with inventory file constraints | Program analyzer |
| TBD-ORDER-ENTRY-002 | Relationship between SEL field and line-item deletion: Does F6 trigger deletion, and how does the program interpret SEL values? | pending_program_context | no | Examine program logic for deletion trigger and SEL processing | Program analyzer |
| TBD-ORDER-ENTRY-003 | LINEAMT calculation: Shown as output-only in DDS but formula (QTY × UNITPRICE) and rounding are not explicit. Does program calculate or is it derived from database? | pending_sme_judgment | no | SME confirmation of line-item pricing logic; verify whether amounts are calculated or stored | SME, program analyzer |

## SME Review Checklist

- [ ] Field names (ORDNO, CUSTID, ORDDATE, TOTAL, LINENO, ITEMNO, ITEMDESC, QTY, UNITPRICE, LINEAMT) are correct and match business terminology
- [ ] Indicator usage (#01 message, #03-#06 conditioning/protection, #99 subfile clear) is accurate and matches program behavior
- [ ] Subfile paging (10 records per page, observed page-down behavior) is intended design and realistic for user experience
- [ ] Function key mappings (F1=ACCEPT, F2=CANCEL, F5=REFRESH, F6=DELETE) are correct
- [ ] Edit codes (A for currency fields) are appropriate
- [ ] Validation (mandatory CUSTID, QTY constraints, stock check) is realistic
- [ ] No invented fields, indicators, subfile logic, or function keys are present
- [ ] All blocking TBDs are resolvable through program analysis or SME judgment

**SME Sign-Off**

| Field | Value |
|-------|-------|
| SME Name | [Awaiting SME review] |
| SME Role | IBM i / DSPF expert, order-entry business expert |
| Review Date | [Pending] |
| Decision | [Pending: approved / approved_with_non_blocking_tbd / blocked] |
| Notes | [Awaiting SME feedback] |

## Handoff Status

| Status | Value |
|--------|-------|
| Analysis Complete | Yes (draft) |
| Ready for Flow Analysis | Yes (after SME approval) |
| Ready for Module Analysis | Yes (after SME approval) |
| Non-Blocking TBDs | TBD-ORDER-ENTRY-001, TBD-ORDER-ENTRY-002, TBD-ORDER-ENTRY-003 |
| Blocking Issues | None |

**Next Steps:**
1. Obtain SME review and sign-off
2. Forward TBDs to program analyzer for context during OBJ-ORDER-ENTRY-001 analysis
3. Use this analysis to inform flow analysis for ORDER-ENTRY capability
