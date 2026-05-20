# Example Routing: Evidence Ready → Inventory

## User Input

> "I have RPGLE / CLLE source for the credit-check capability, the DDS for
> CUSTPF and CRHOLDP, a sample spool of the credit-hold report, and two
> redacted sample transactions. The customer IDs and amounts have been
> replaced with stable fakes. I have an SME contact from the credit
> operations team. What should I do next?"

## Orchestrator Output

```
## Workflow Decision

- **Current Stage:** Evidence Ready (Stage 1)
- **Desired Outcome:** Start reverse engineering
- **Recommended Next Skill:** `legacy-ibmi-inventory` (status: Implemented v0.1.0)
- **Why:** Evidence is redacted and an SME is available. Inventory is the
  required first call so every downstream skill has an object ledger to
  reference.

## Routing Notes

- **Stage skip safe?** No. Skipping inventory means downstream rule mining
  has no object-to-evidence backbone.
- **Gate check:** Evidence Authorization Gate — passes. All evidence has known
  sensitivity and source-path authorization per the user's note; inventory will
  record the sensitivity decisions.
- **Minimum input needed next:** capability slug (suggest `CREDIT-CHECK`),
  source library name, collection date, and intake reviewer.
- **Route confidence:** High.
- **Next artifact expected:** `01_inventory/inventory.yaml` and
  `01_inventory/object-map.md`.

## Next Step

- **Invoke:** `legacy-ibmi-inventory`
- **Produce:** `inventory.yaml`, `object-map.md`, `inventory-review-checklist.md`
- **Save reminder:** Save the inventory under `01_inventory/` with capability
  slug in the filename if running multiple slices.
- **SME reminder:** After draft, request SME review against the
  inventory-review-checklist before routing to any analyzer skill. SME must
  confirm program coverage, hidden dependencies (data areas, scheduler
  entries), and report/spool completeness.
- **Review/export reminder:** Not applicable yet. No stable human-facing
  Markdown package exists; keep producing canonical Markdown/YAML artifacts
  first.
- **Manual fallback:** Not needed — `legacy-ibmi-inventory` is implemented.
```
