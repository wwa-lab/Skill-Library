# Report Analysis: OBJ-INVOICE-RPT-004

**Artifact Metadata**

| Field | Value |
|-------|-------|
| Object ID | OBJ-INVOICE-RPT-004 |
| Object Name | INVOICERPT (printer file) |
| Surface Type | PRTF (printed report with control breaks) |
| Analysis Date | 2026-05-11 |
| Analyst | Claude Code (skill: legacy-ibmi-screen-report-analyzer) |
| Status | draft |

## Source Evidence Summary

| Evidence ID | Source Type | Location | Sensitivity | Notes |
|-------------|-------------|----------|-------------|-------|
| EV-INVOICE-RPT-021 | PRTF source | DEMO01/INVOICERPT member | safe | Complete DDS definition |
| EV-INVOICE-RPT-022 | Spool sample (page 1) | sample-spool-page-1.txt | redacted | Customer names, invoice amounts redacted |

## Surface Type Classification

**Type:** PRTF (Printed Report with Multi-Level Control Breaks)

**Description:** Invoice report layout showing invoice detail rows and total-like
report lines. Grouping, sorting, and total formulas require program/spool/SME
evidence beyond the PRTF layout.

**Related Objects:**
- OBJ-INVOICE-PROG-001 (program that generates report via WRITE statements)
- OBJ-INVOICE-FILE-001 (invoice data file)

## Layout Summary

### Overall Dimensions (PRTF)
- Record Format Names: RPTHEAD, COLHEAD, INVDETAIL, CUSTSUBTL, RPTOTAL
- Page Size: 66 lines, 80 columns (PAGESIZE(66 80))
- Margins: 2 top, 2 bottom, 5 left, 5 right
- Overflow: Page break at line 60 (OVERFLOW(60))

### Visual Description
The report header (rows 1-4) displays "INVOICE REPORT", current date, page number, and column headers (Customer ID, Customer Name, Invoice No, Amount). Detail lines in the sample show customer, customer name, invoice number, and amount. The spool sample also shows subtotal-like lines labelled "Customer Total" and a trailer-like line labelled "GRAND TOTAL"; trigger and formula semantics remain pending program/SME evidence.

## Fields and Indicators

### Field Inventory (Reporting Context)

| Field Name | Type | Length | Dec | Edit Code | Purpose | Evidence |
|------------|------|--------|-----|-----------|---------|----------|
| CUSTID | N | 5 | 0 | 00000 | Customer ID; candidate grouping field from spool sample | EV-INVOICE-RPT-021, EV-INVOICE-RPT-022 |
| CUSTNAME | A | 30 | – | – | Customer name; display only | EV-INVOICE-RPT-021 |
| INVNO | A | 10 | – | – | Invoice number; unique per invoice | EV-INVOICE-RPT-021 |
| INVAMT | N | 10 | 2 | A (comma) | Amount displayed on detail line; calculation/source requires program evidence | EV-INVOICE-RPT-021 |
| CUSTCNT | N | 4 | 0 | - | Count-like field on subtotal format; meaning requires program/SME evidence | EV-INVOICE-RPT-021 |
| CUSTTOTAL | N | 10 | 2 | A (comma) | Total-like field on subtotal format; formula requires program/SME evidence | EV-INVOICE-RPT-021 |
| INVCOUNT | N | 5 | 0 | - | Count-like field on trailer format; meaning requires program/SME evidence | EV-INVOICE-RPT-021 |
| GRANDTOTAL | N | 10 | 2 | A (comma) | Total-like field on trailer format; formula requires program/SME evidence | EV-INVOICE-RPT-021 |
| PAGENMBR | N | 5 | 0 | – | Page number; system-supplied | EV-INVOICE-RPT-021 |
| CURDATE | N | 8 | 0 | MM/DD/YY | Current date; system-supplied | EV-INVOICE-RPT-021 |

### Total / Count Fields

| Field | Evidence Classification | Trigger / Formula Status | Evidence |
|-------|-------------------------|--------------------------|----------|
| INVAMT | Detail amount displayed in PRTF and spool | Source of value requires program/file evidence | EV-INVOICE-RPT-021, EV-INVOICE-RPT-022 |
| CUSTTOTAL | Subtotal-like value displayed in spool | Program evidence required to prove formula and break trigger | EV-INVOICE-RPT-021, EV-INVOICE-RPT-022 |
| GRANDTOTAL | Grand-total-like value displayed in spool | Program evidence required to prove formula and inclusion/exclusion rules | EV-INVOICE-RPT-021, EV-INVOICE-RPT-022 |

## Report Structure (PRTF / Spool Sample)

### Page Layout

| Section | Record Format | Lines | Trigger | Content | Evidence |
|---------|---------------|-------|---------|---------|----------|
| Header | RPTHEAD, COLHEAD | rows 1–4 | Page/report start, pending program confirmation for repeat behavior | Title, date, page number, column headers | EV-INVOICE-RPT-021, EV-INVOICE-RPT-022 |
| Detail | INVDETAIL | rows 5-59 in sample | Per visible invoice detail row; WRITE trigger pending program evidence | CUSTID, CUSTNAME, INVNO, INVAMT | EV-INVOICE-RPT-021, EV-INVOICE-RPT-022 |
| Subtotal-like | CUSTSUBTL | 1 row in sample | Appears after customer group in sample; trigger pending program evidence | "Customer Total:", CUSTID, CUSTCNT, CUSTTOTAL | EV-INVOICE-RPT-021, EV-INVOICE-RPT-022 |
| Trailer-like | RPTOTAL | 1 row in sample | Appears at end of sample; trigger pending program evidence | "GRAND TOTAL", INVCOUNT, GRANDTOTAL | EV-INVOICE-RPT-021, EV-INVOICE-RPT-022 |

### Control Breaks & Totals

| Control Field | Break Trigger | Subtotal Fields | Accumulation Logic | Evidence |
|---------------|---------------|-----------------|-------------------|----------|
| CUSTID | Spool grouping suggests CUSTID break; program proof pending | CUSTCNT, CUSTTOTAL | Formula pending program/O-spec or SME confirmation | EV-INVOICE-RPT-021, EV-INVOICE-RPT-022 |
| (Report End) | Trailer appears at end of sample | INVCOUNT, GRANDTOTAL | Formula pending program/O-spec or SME confirmation | EV-INVOICE-RPT-021, EV-INVOICE-RPT-022 |

**Control Break Behavior (from Spool Sample):**
- Spool shows 3 customers (CUSTID 00001, 00002, 00003)
- Each customer has 1–2 invoices
- Subtotal-like line prints after each visible customer group (rows blank, "Customer Total:" line)
- Grand-total-like line prints at end of sample
- Supports a `SEED-*` / SME question about CUSTID grouping; it does not by
  itself prove the program's break trigger or formula

## Validation & Edit Codes

| Field | Edit Code | Format Example | Evidence |
|-------|-----------|-----------------|----------|
| CUSTID | 00000 | 00001 (leading zeros) | EV-INVOICE-RPT-021, EV-INVOICE-RPT-022 |
| INVAMT | A (comma) | 10,234.56 (currency with commas and decimals) | EV-INVOICE-RPT-021, EV-INVOICE-RPT-022 |
| CUSTTOTAL | A (comma) | 10,234.56 (currency with commas and decimals) | EV-INVOICE-RPT-021, EV-INVOICE-RPT-022 |
| GRANDTOTAL | A (comma) | 21,716.91 (currency with commas and decimals) | EV-INVOICE-RPT-021, EV-INVOICE-RPT-022 |

## Program Touchpoints

| Program | WRITE Records | Details | Evidence |
|---------|---------------|---------|----------|
| OBJ-INVOICE-PROG-001 | WRITE INVDETAIL (detail loop) | Program evidence needed to confirm read order and one-write-per-invoice behavior | EV-INVOICE-RPT-022 (spool observation only) |
| OBJ-INVOICE-PROG-001 | WRITE CUSTSUBTL | Program evidence needed to confirm trigger and reset behavior | EV-INVOICE-RPT-022 (spool observation only) |
| OBJ-INVOICE-PROG-001 | WRITE RPTOTAL | Program evidence needed to confirm end-of-file timing | EV-INVOICE-RPT-022 (spool observation only) |

**Program Logic Correlation:**
- PRTF DDS defines overflow at line 60; runtime/program evidence is needed to
  prove repeated headers and forced page behavior
- Program likely sorts or reads invoices in CUSTID order because the spool is
  grouped, but this remains pending program evidence
- Program must supply CUSTCNT, INVCOUNT, CUSTTOTAL, and GRANDTOTAL values; PRTF
  layout alone does not prove formulas

## Observed Behaviors

| Behavior ID | Description | Observed In | Confidence | Evidence | Notes |
|-------------|-------------|-------------|-----------|----------|-------|
| BEH-INVOICE-RPT-001 | Subtotal line prints on separate line with label "Customer Total:", control field value, count, and total amount with underline | EV-INVOICE-RPT-022 (spool) | high | Matches DDS SPACEB(1), SPACEA(1), UNDERLINE keywords |
| BEH-INVOICE-RPT-002 | Grand-total-like line prints at end of sample with label "GRAND TOTAL" and count/amount fields | EV-INVOICE-RPT-022 (spool) | medium | Formula and inclusion rules require program/SME evidence |
| BEH-INVOICE-RPT-003 | Customer amounts are right-aligned and formatted with commas and two decimal places (e.g., 10,234.56) | EV-INVOICE-RPT-022 (spool) | high | Matches DDS EDTCDE(A) keyword |
| BEH-INVOICE-RPT-004 | PRTF DDS defines overflow at line 60 | EV-INVOICE-RPT-021 | medium | Full multi-page spool sample needed to observe actual page break and repeated headers |

## Inferred Questions (Candidate Downstream Seeds)

| Seed ID | Question | Related Fields | Downstream Owner |
|---------|----------|----------------|------------------|
| SEED-INVOICE-RPT-001 | Should the subtotal and grand total include or exclude certain invoice types (credit memos, adjustments) or statuses? | INVAMT, CUSTTOTAL, GRANDTOTAL | SME, program analyzer |
| SEED-INVOICE-RPT-002 | What exactly does CUSTCNT count: invoices, invoice lines, transactions, or printed detail rows? | CUSTCNT | SME, program analyzer |
| SEED-INVOICE-RPT-003 | Can the report be filtered by date range, customer segment, or other criteria, or is it always full historical? | CURDATE | Capability modeler, modernization decision |

## TBD Ledger

| TBD ID | Issue | Category | Blocking | Resolution Path | Owner |
|--------|-------|----------|----------|-----------------|-------|
| TBD-INVOICE-RPT-001 | Multi-page behavior: Spool sample shows page 1 only; cannot confirm whether headers repeat on every page | pending_source | no | Obtain full multi-page spool sample and program WRITE/order evidence | Program/report analyst |
| TBD-INVOICE-RPT-002 | Customer count field (CUSTCNT) purpose: Is it a count of invoices per customer (implied by position), or count of line items, or count of transactions? Program context needed | pending_program_context | no | Examine program logic for CUSTCNT increment trigger; confirm what is being counted | Program analyzer |
| TBD-INVOICE-RPT-003 | Rounding and decimal handling: Invoice amounts shown to 2 decimals; unclear if rounding occurs at line level or grand total only | pending_sme_judgment | no | SME confirmation of rounding rule and its business impact (e.g., penny rounding for tax calculation) | SME |

## SME Review Checklist

- [ ] Customer ID is the correct control-break field (vs. other possibilities like Customer Name or Invoice Date)
- [ ] Customer count (CUSTCNT) and grand total invoice count (INVCOUNT) capture the right metrics
- [ ] Subtotal calculations (sum of amounts per customer) are correct and complete
- [ ] Grand total meaning and reconciliation rule are confirmed (including any hidden adjustments or exclusions)
- [ ] Edit code (A = comma format) is appropriate for invoice amounts
- [ ] Page breaks (OVERFLOW(60)) occur at the right position in the document
- [ ] All fields (CUSTID, CUSTNAME, INVNO, INVAMT) are accessible and correctly mapped
- [ ] No invented fields, control breaks, or report structure are present
- [ ] TBDs are resolvable and do not block usage

**SME Sign-Off**

| Field | Value |
|-------|-------|
| SME Name | [Awaiting SME review] |
| SME Role | Invoice/accounting business expert, PRTF analyst |
| Review Date | [Pending] |
| Decision | [Pending: approved / approved_with_non_blocking_tbd / blocked] |
| Notes | [Awaiting SME feedback] |

## Handoff Status

| Status | Value |
|--------|-------|
| Analysis Complete | Yes (draft) |
| Ready for Flow Analysis | Yes (after SME approval) |
| Ready for Module Analysis | Yes (after SME approval) |
| Non-Blocking TBDs | TBD-INVOICE-RPT-001, TBD-INVOICE-RPT-002, TBD-INVOICE-RPT-003 |
| Blocking Issues | None |

**Next Steps:**
1. Obtain SME review and sign-off
2. Forward TBD-INVOICE-RPT-001 to program analyst (multi-page spool sample needed)
3. Forward TBD-INVOICE-RPT-002 to program analyzer (CUSTCNT logic)
4. Forward SEED-INVOICE-RPT-* to capability modeler for business rule mining
