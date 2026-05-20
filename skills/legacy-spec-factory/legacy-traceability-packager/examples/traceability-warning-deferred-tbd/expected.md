# Example: Traceability Warning — Deferred Blocking TBD

## Scenario

Capability **Returns Processing** (`CAP-RETURNS-001`) has every upstream artefact approved:

- `01_inventory/inventory.yaml` — approved
- `02_programs/RETURNS/program-analysis.md` — approved
- `03_flows/RETURNS/return-claim/flow.md` — approved
- `04_modules/returns/` — approved
- `05_brds/RETURNS/brd.md` — approved (SME: Aisha Khan, 2026-05-14)
- `05_specs/RETURNS/spec.yaml` — `status: approved` (SME: Aisha Khan, 2026-05-15)
- `evidence/manifest.yaml` — `approved_for_inventory`

The spec carries one `TBD-*` that remained `blocking: true` at sign-off because the SME chose to defer rather than demote:

```yaml
# 05_specs/RETURNS/spec.yaml (excerpt)
open_questions:
  - id: TBD-RETURNS-002
    question: "Should partial-refund returns inherit the original order's audit trail or start a new chain?"
    blocking: true
    resolution: "Deferred to Phase 2 by Aisha Khan, Returns Policy Owner."
    resolver: "Aisha Khan"
    planned_resolution_date: "2026-07-31"
    deferral_recorded_in: "05_specs/RETURNS/spec-review.md#sme-decisions"
```

All four deferral fields are present and `deferral_recorded_in` points to a concrete review section, so Step 7 raises `BLOCKING-TBD-DEFERRED` (warning) instead of `BLOCKING-TBD-UNRESOLVED` (blocking).

Every other gate passes. There are 3 `BR-*`, 4 `AC-*`, 5 `EV-*`, 3 `BEH-*`, 2 `DEC-*`, and 2 `TC-*`.

## Expected Gate Result

| Step | Result |
| --- | --- |
| 1 — Intake | pass |
| 2 — ID Inventory | pass |
| 3 — Cross-Reference Walk | pass |
| 4 — Evidence Sensitivity | pass |
| 5 — BR Closure | pass |
| 6 — Coverage Tables | pass |
| 7 — TBD Carry-Forward | **warning** — `BLOCKING-TBD-DEFERRED` |
| 8 — Assembly | pass_with_warnings |

**Final status:** `pass_with_warnings`.

## Expected Output Files

Under `06_traceability_packages/RETURNS/`:

- `traceability-package.yaml`
- `traceability-package.md`
- `coverage-audit.md`
- `traceability-review.md`

Not written: `blocking-findings.yaml` (status is not `blocked`).

## Expected `findings` and TBD Carry-Forward

```yaml
findings:
  blocking: []
  warnings:
    - find_id: "FIND-RETURNS-001"
      rule: "BLOCKING-TBD-DEFERRED"
      severity: "warning"
      step: 7
      points_to:
        - "TBD-RETURNS-002"
        - "05_specs/RETURNS/spec-review.md#sme-decisions"
      detail: "TBD has blocking: true and a named SME deferral with planned date 2026-07-31. Carried forward verbatim into open_questions[]."
      required_remediation:
        responsible_skill: "legacy-spec-writer"
        permitted_actions:
          - "Phase 2: resolve TBD-RETURNS-002 by 2026-07-31 with named SME decision, then re-run packager."
        forbidden_action: "legacy-traceability-packager MUST NOT demote TBD-RETURNS-002.blocking from true to false."
  info: []

open_questions:
  - id: "TBD-RETURNS-002"
    question: "Should partial-refund returns inherit the original order's audit trail or start a new chain?"
    blocking: true
    resolution: "Deferred to Phase 2 by Aisha Khan, Returns Policy Owner."
    resolver: "Aisha Khan"
    planned_resolution_date: "2026-07-31"
    deferral_recorded_in: "05_specs/RETURNS/spec-review.md#sme-decisions"
    category: "downstream_handoff_blockers"
    related_ids: []
    next_routing:
      responsible_skill: "legacy-spec-writer"
      capability_owner: "Aisha Khan"
```

## What a Reviewer Should Verify

1. Four files exist under `06_traceability_packages/RETURNS/`; `blocking-findings.yaml` does not.
2. `traceability-package.yaml.status` is `pass_with_warnings`.
3. `TBD-RETURNS-002` appears under `open_questions[]` with `blocking: true` preserved.
4. The warning's `forbidden_action` is recorded — the packager did not silently demote the TBD.
5. `traceability-review.md` cites the warning and names `legacy-spec-writer` as the Phase 2 owner.
6. If the SME rescinds the deferral before 2026-07-31, the upstream spec is updated and the packager is re-run.
