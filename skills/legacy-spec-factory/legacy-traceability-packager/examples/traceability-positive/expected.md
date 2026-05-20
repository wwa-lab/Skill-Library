# Example: Traceability Positive — `pass`

## Scenario

Capability **Credit Limit Enforcement** (`CAP-CREDIT-CHECK-001`) has run through the full Legacy Spec Factory chain. Every artefact required by `legacy-traceability-packager` is approved and consistent:

- `01_inventory/inventory.yaml` — `sme_review.decision: approved`
- `02_programs/CREDIT-CHECK/program-analysis.md` — `approved`
- `03_flows/CREDIT-CHECK/credit-check-auth/flow.md` — `approved`
- `04_modules/card-auth/` — all four views `approved`
- `05_brds/CREDIT-CHECK/brd.md` — `approved` (SME: John Smith, 2026-05-14)
- `05_specs/CREDIT-CHECK/spec.yaml` — `approved` (SME: John Smith, 2026-05-15)
- `evidence/manifest.yaml` — `package_state: approved_for_inventory`
- `06_sdd_handoffs/CREDIT-CHECK/sdd-handoff.yaml` — `approved` (cross-check passes)

Capability contains 2 `BR-*`, 3 `AC-*`, 4 `EV-*`, 2 `BEH-*`, 1 `DEC-*`, 1 `TC-*` (golden master), and no open `TBD-*`.

## Expected Gate Result

| Step | Result |
| --- | --- |
| 1 — Intake | pass |
| 2 — ID Inventory | pass |
| 3 — Cross-Reference Walk | pass |
| 4 — Evidence Sensitivity | pass |
| 5 — BR Closure | pass |
| 6 — Coverage Tables | pass |
| 7 — TBD Carry-Forward | pass |
| 8 — Assembly | pass |

**Final status:** `pass`.

## Expected Output Files

Under `06_traceability_packages/CREDIT-CHECK/`:

- `traceability-package.yaml` — identical in shape to `templates/traceability-package.yaml`
- `traceability-package.md` — identical in shape to `templates/traceability-package.md`
- `coverage-audit.md` — identical in shape to `templates/coverage-audit.md`
- `traceability-review.md` — identical in shape to `templates/traceability-review.md`

## Expected Metrics

| Metric | Value |
| --- | --- |
| Approved `BR-*` closure rate | 1.00 |
| `AC-*` approval rate | 1.00 |
| `TC-*` to `AC-*` coverage | 0.33 |
| Evidence usage rate | 1.00 |

## Expected `findings`

```yaml
findings:
  blocking: []
  warnings: []
  info: []
```

## What a Reviewer Should Verify

1. The four files exist; `blocking-findings.yaml` does not.
2. Every `EV-*` in `evidence_coverage` appears under at least one `referenced_by` key.
3. Every approved `BR-*` in `business_rule_coverage` has non-empty `evidence_ids`, `behavior_ids`, and `acceptance_criteria_ids`.
4. `id_inventory.totals` sums match the explicit `ids` lists.
5. `next_routing.primary_next_skill` is `legacy-brd-to-sdd-handoff` (or `none` if the handoff is already current).
6. The packager did not invent any ID outside of `FIND-*` and `PKG-*`.
