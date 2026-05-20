# PRTF Report Patterns Reference

Use this reference when analyzing IBM i printer-file DDS, RPG output specs
(O-specs), report programs, and spool samples. Keep layout facts separate from
calculation and print-order facts.

## Evidence Boundaries

| Evidence | What it can prove | What it cannot prove alone |
| --- | --- | --- |
| PRTF DDS | Record formats, fields, constants, positions, spacing, page size, overflow, edit codes/masks | Which records print in what business sequence, total formulas, filters, sorting |
| RPG / COBOL / CL program evidence | WRITE order, O-specs, control-break tests, accumulator updates, OVRPRTF usage | SME meaning of a total or regulatory intent |
| Spool sample | Runtime appearance, page breaks in that run, observed subtotal/grand-total lines | General formulas unless reconciled to source/data |
| SME note | Business meaning, intended report use, whether a behavior is required | Source-level proof of exact implementation |

If PRTF DDS and program/spool evidence disagree, create a `TBD-*` instead of
choosing the smoother story.

## Common PRTF DDS Keywords and Constructs

### Page and Printer Definition

| Keyword / construct | Purpose | Analysis note |
| --- | --- | --- |
| `PAGESIZE` | Page length and width | Cite exact value and source line |
| `OVERFLOW` | Overflow line or condition | Confirms layout boundary, not full page-break behavior by itself |
| `SPACEA` / `SPACEB` | Space after / before a record format | Helps distinguish section spacing in spool |
| `SKIPA` / `SKIPB` | Skip after / before printing | May indicate page or section transitions |
| `PAGNBR` / page-number field | Page number output | Confirm display position and edit format |
| `EDTCDE` / `EDTWRD` / `EDTMSK` | Numeric formatting | Formatting only; not business calculation |
| `TEXT` / literals | Labels and headings | Labels are presentation evidence, not rule proof |

### Record Format Classification

PRTF DDS usually defines named record formats. Classify each format by
evidence, not by name alone:

| Role | Typical evidence |
| --- | --- |
| Page header | Written at page start or appears on each page in spool |
| Report header | Written once near report start |
| Column header | Repeating literals above detail rows |
| Detail | Repeated once per input record or line item |
| Subtotal / break | Appears when a grouped value changes; requires program/spool/SME evidence |
| Grand total / trailer | Appears at report end; requires program/spool/SME evidence |
| Exception / message | Printed only under error or special condition |

Do not treat record format names like `TOTAL`, `SUBTL`, or `HEADER` as proof
without WRITE order, O-spec, spool, or SME evidence.

## Report Structure Analysis

For each report, capture:

- Page dimensions and overflow definition
- Record formats and literal headings
- Field inventory with position, type, length, decimals, edit code/mask
- Record format roles with evidence source
- Program touchpoints: WRITE statements, O-specs, overrides, sorting/filtering
- Runtime reconciliation against spool samples
- Totals and counts as observed behaviors until source/SME confirms the formula

## Control Breaks and Totals

Control breaks and totals are load-bearing for downstream specifications. Use
this evidence ladder:

1. Program code or O-spec explicitly tests a control field and writes a break
   record.
2. Spool sample shows grouped detail rows followed by a subtotal and the input
   data supports the grouping.
3. SME confirms the intended break and total semantics.

If only a label such as `Customer Total` is visible, create a `SEED-*` or
`TBD-*`; do not mint a business rule.

### Total Classification

| Classification | Required evidence |
| --- | --- |
| Displayed total | Spool/report shows a total-like value |
| Layout total field | PRTF DDS has a field placed on a total/trailer format |
| Program-computed total | Program code accumulates or assigns the value |
| Business-approved total | SME confirms meaning and expected inclusion/exclusion rules |

## Spool Sample Reconciliation

When spool evidence is available:

1. Preserve fixed-width formatting.
2. Mark page boundaries, headings, detail rows, subtotals, trailers, and blank
   lines.
3. Reconcile each visible field to a PRTF field or literal when possible.
4. Reconcile totals only when the source rows in the same sample are sufficient.
5. Create `TBD-*` for missing pages, redacted amounts that prevent arithmetic
   checks, or unexplained totals.

## Common Anti-Patterns

1. **Treating PRTF layout as calculation logic.** A positioned amount field is
   not proof of the formula that produced it.
2. **Inferring control breaks from labels only.** `Department Total` is a hint,
   not proof of the break trigger.
3. **Using one redacted page as full report evidence.** Single-page samples
   rarely prove page overflow, repeated headers, or end-of-report trailers.
4. **Assuming all numeric fields are additive.** Counts, averages, rates,
   balances, and signs require source or SME evidence.
5. **Collapsing O-spec and PRTF DDS.** Record which artifact supplied each
   claim; do not call RPG output specs PRTF DDS.

## Review Checklist

- [ ] Page and printer settings are sourced from PRTF DDS or OVRPRTF evidence
- [ ] Each record format role is supported by source, WRITE order, spool, or SME evidence
- [ ] Every total/counter has an evidence classification
- [ ] Control-break fields are not inferred from labels alone
- [ ] Spool samples are redacted but still preserve fixed-width structure
- [ ] Any formula, inclusion rule, sort order, or filter becomes `TBD-*` unless evidenced
