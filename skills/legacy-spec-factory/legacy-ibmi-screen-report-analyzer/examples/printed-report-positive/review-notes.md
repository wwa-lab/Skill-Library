# Review Notes: Printed Report Example

**Example Objective:** Demonstrate a positive PRTF/report analysis that
separates layout evidence from program behavior:

- PRTF DDS proves page layout, fields, headings, spacing, and edit masks.
- Spool evidence proves what appeared in one controlled run.
- Program/O-spec or SME evidence is still required for sorting, control
  breaks, totals, filters, rounding, and inclusion rules.

## Key Analysis Elements Demonstrated

### 1. PRTF Evidence Boundaries

- Record formats are identified by exact PRTF DDS names: RPTHEAD, COLHEAD,
  INVDETAIL, CUSTSUBTL, RPTOTAL.
- `PAGESIZE` and `OVERFLOW` are layout facts, not proof of repeated header
  behavior in every runtime path.
- Labels such as `Customer Total` and `GRAND TOTAL` are presentation evidence;
  they raise questions until source/SME confirms formulas.

### 2. Report Section Analysis

- Header and column-heading formats are sourced from PRTF DDS.
- Detail lines are visible in both DDS and spool sample.
- Subtotal-like and grand-total-like lines are visible, but break triggers and
  arithmetic formulas remain pending program/SME evidence.

### 3. Spool Sample Cross-Reference

- Fixed-width layout is matched against PRTF fields and literals.
- Edit formatting is observed in runtime output.
- Grouping by customer is observed in the sample and promoted only to a
  `SEED-*` / SME question, not an approved rule.
- Missing multi-page evidence becomes a non-blocking `TBD-*`.

### 4. Total / Count Handling

The example classifies totals carefully:

- `CUSTTOTAL` is a total-like field on a subtotal-like line.
- `GRANDTOTAL` is a total-like field on a trailer-like line.
- `CUSTCNT` and `INVCOUNT` are count-like fields.
- Program analysis must confirm what is counted, when accumulators reset, and
  whether credits, adjustments, voids, or filters are included.

## What This Example Gets Right

- No PRTF layout label is treated as calculation proof.
- Every field and observed behavior links to `EV-*` evidence.
- Ambiguities become `SEED-*` or `TBD-*`.
- Program responsibilities are explicitly deferred to program analysis.
- SME approval remains required for business meaning and report intent.

## Common Mistakes Avoided

Wrong: "The report sums customer invoices because the label says Customer Total."

Right: "The spool shows a subtotal-like line labelled Customer Total; formula and
break trigger require program/O-spec or SME confirmation."

Wrong: "Grand total is automatically calculated by the printer file."

Right: "PRTF DDS defines the field placement; the program supplies the value."

Wrong: "Page 1 spool proves all pages have the same header."

Right: "Page 1 shows the header; multi-page behavior needs a full spool sample
or program evidence."

## How to Use This Example

For analysts:

- Follow the analysis artifact shape.
- Preserve the distinction between layout, runtime observation, and business
  interpretation.
- Create `TBD-*` items for missing program evidence or incomplete spool samples.

For reviewers:

- Check that formulas, filters, and control breaks are not invented.
- Check that all report fields and observed behaviors resolve to `EV-*`.
- Check that SME review is required before report business meaning is approved.

For downstream skills:

- Program analyzer resolves write order, sorting, filters, counters, and totals.
- Module analyzer can use observed report surfaces, not unapproved business
  rules.
- Spec writer should consume only approved report behavior or SME-confirmed
  rules.

## Conformance to Review Gate

- Purpose and trigger clarity: report analysis with approved inventory required.
- Workflow completeness: examples cover layout, runtime evidence, and TBDs.
- IBM i correctness: PRTF DDS, program/O-specs, and spool samples are kept as
  separate evidence types.
- Evidence integrity: no formulas or business rules are approved without
  source/SME support.
- Output contract: IDs and handoff rules match the skill contract.
