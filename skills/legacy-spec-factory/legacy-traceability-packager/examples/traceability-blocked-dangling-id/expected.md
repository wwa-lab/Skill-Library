# Example: Traceability Blocked — Dangling ID

## Scenario

Capability **Order Entry** (`CAP-ORDER-ENTRY-001`) has all upstream artefacts approved:

- `01_inventory/inventory.yaml` — approved
- `04_modules/order-entry/` — approved
- `05_brds/ORDER-ENTRY/brd.md` — approved (SME: Sarah Chen, 2026-05-13)
- `05_specs/ORDER-ENTRY/spec.yaml` — `status: approved` (SME: Sarah Chen, 2026-05-15)
- `evidence/manifest.yaml` — `approved_for_inventory`

…**but** the spec contains an inconsistency:

```yaml
# 05_specs/ORDER-ENTRY/spec.yaml (excerpt)
business_rules:
  - id: BR-ORDER-ENTRY-001
    review_status: approved
    # …
  - id: BR-ORDER-ENTRY-002
    review_status: approved
    # … (no BR-ORDER-ENTRY-007 exists)

acceptance_criteria:
  - id: AC-ORDER-ENTRY-004
    validates: [BR-ORDER-ENTRY-007]    # ← dangling: no BR-ORDER-ENTRY-007 in business_rules[]
    review_status: approved
```

The dangling reference was overlooked during SME review. `legacy-traceability-packager` catches it during Step 3 (Cross-Reference Walk).

## Expected Gate Result

| Step | Result |
| --- | --- |
| 1 — Intake | pass |
| 2 — ID Inventory | pass (`BR-ORDER-ENTRY-007` is referenced but not defined, recorded only) |
| 3 — Cross-Reference Walk | **FAIL** — `BR-DANGLING-IN-AC` |
| 4 — Evidence Sensitivity | not evaluated (dangling-ID failure makes downstream closure checks unreliable) |
| 5 — BR Closure | not evaluated |
| 6 — Coverage Tables | not evaluated |
| 7 — TBD Carry-Forward | not evaluated |
| 8 — Assembly | blocked-route |

**Final status:** `blocked`.

## Expected Output Files

Under `06_traceability_packages/ORDER-ENTRY/`:

- `traceability-review.md` (gate checklist + blocking findings + remediation)
- `blocking-findings.yaml` (machine-readable — see `templates/blocking-findings.yaml` for the exact shape, reused here verbatim)

Not written:

- `traceability-package.yaml`
- `traceability-package.md`
- `coverage-audit.md`

## Expected Blocking Finding

```yaml
findings:
  blocking:
    - find_id: "FIND-ORDER-ENTRY-001"
      rule: "BR-DANGLING-IN-AC"
      severity: "blocking"
      step: 3
      points_to:
        - "05_specs/ORDER-ENTRY/spec.yaml#acceptance_criteria[3]"
        - "AC-ORDER-ENTRY-004"
        - "BR-ORDER-ENTRY-007"
      detail: "AC-ORDER-ENTRY-004.validates references BR-ORDER-ENTRY-007 but BR-ORDER-ENTRY-007 is not defined in spec.yaml.business_rules[]."
      required_remediation:
        responsible_skill: "legacy-spec-writer"
        permitted_actions:
          - "Add BR-ORDER-ENTRY-007 to business_rules[] with evidence + behavior links, then re-run packager."
          - "Update AC-ORDER-ENTRY-004.validates to point to an existing approved BR-*, then re-run packager."
          - "If AC-ORDER-ENTRY-004 is out of scope, retire it per docs/id-conventions.md and re-run packager."
        forbidden_action: "legacy-traceability-packager MUST NOT mint BR-ORDER-ENTRY-007 or rewrite AC-ORDER-ENTRY-004."
```

## What a Reviewer Should Verify

1. Only two files exist under `06_traceability_packages/ORDER-ENTRY/`: `traceability-review.md` and `blocking-findings.yaml`. No `traceability-package.yaml`, no `traceability-package.md`, no `coverage-audit.md`.
2. `traceability-review.md` clearly states `Overall Status: ❌ blocked` and quotes the finding.
3. `next_routing.primary_next_skill` is `legacy-spec-writer`.
4. The packager did **not** invent `BR-ORDER-ENTRY-007` or rewrite `AC-ORDER-ENTRY-004`.
5. Spec `status` remained `approved` upstream — the packager did not modify it.
6. Re-running the packager after `legacy-spec-writer` resolves the dangling reference should yield `pass` (or `pass_with_warnings` if other warnings appear).
