# Programs Batch Digest — PRICE-CALC

**Generated:** 2026-05-16 by `legacy-ibmi-batch-digest` v0.1.0
**Source:** 1 `program-analysis.md` file in `02_programs/PRICE-CALC/`
**Inventory:** [`../../01_inventory/inventory.yaml`](../../01_inventory/inventory.yaml)
  · criticality confirmed 2026-05-16 by Jane Doe

## At a glance

| Bucket | Count | SME effort |
| --- | --- | --- |
| Critical | 1 | full review per program (~20 min) |
| Standard | 0 | — |
| Low-risk | 0 | — |
| Not yet analyzed | 0 | — |

Estimated SME time: 20-30 minutes  ·  (vs. ~5 minutes baseline — this is
a tiny synthetic example; the digest shape matters more than the count)

---

## Critical (1) — full SME review per program

| OBJ | Role (1 line) | Key pending decisions | TBDs | Status | Detail |
| --- | --- | --- | --- | --- | --- |
| OBJ-PRICE-CALC-PRICECALC | Calculates final unit price given customer tier and item | (none — all resolved via SME walkthrough) | 0 | approved | [`PRICECALC/program-analysis.md`](PRICECALC/program-analysis.md) |

---

## SME signoff

Tick when you finish each bucket. Detailed rejections / corrections go in
`08_business-understanding/<CAP-*>/sme-review-<YYYY-MM-DD>.md`.

- **Critical bucket** (1 program)
  - Reviewed by: Jane Doe
  - Date: 2026-05-16
  - Result: ☒ all approved

- **Standard bucket** (0 programs) — n/a
- **Low-risk bucket** (0 programs) — n/a
- **Not-yet-analyzed bucket** (0 programs) — n/a

---

## Re-render

Re-run `legacy-ibmi-batch-digest` for module `PRICE-CALC` after any
program-analysis.md changes or after new program-analysis files land.
This file is fully regenerated — do not hand-edit table rows.

## Notes for studying this digest

In a real 50-program module, this digest would have three bucket
tables (Critical / Standard / Low-risk), each with N rows. The SME
opens **this one file**, scans the Critical table (5-15 rows
typically), spot-checks a few rows in Standard, batch-confirms
Low-risk. Total elapsed time ~30-90 minutes for the whole module
instead of 4-8 hours opening every file.
