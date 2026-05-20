# Stage 02: Inventory (In Progress / Blocked / Done)

**You are here if:** `01_inventory/inventory.yaml` exists in any state — draft,
blocked, or approved. This card covers all three sub-stages (2a, 2b, 2c).

Use it to (a) finish the inventory, (b) unblock a blocked inventory, or (c)
confirm the inventory is approved and move on.

## Need before starting

- `01_inventory/inventory.yaml` (any status)
- `evidence/redacted/evidence-manifest.yaml` referenced by inventory objects
- SME contact

## Run

Depends on inventory status:

| inventory.yaml status | What to run |
| --- | --- |
| no `sme_review` field, partial objects | re-invoke `legacy-ibmi-inventory` to extend coverage |
| `sme_review.decision: blocked` OR blocking `coverage_gaps[]` | resolve each `TBD-*` / gap with the SME, then re-invoke `legacy-ibmi-inventory` to update |
| `sme_review.decision: approved` or `approved_with_non_blocking_tbd` | move to the next card |

- **Skill:** `legacy-ibmi-inventory` (Implemented v0.1.0)
- **Manual fallback:** Edit `inventory.yaml` by hand following
  `docs/id-conventions.md` and the inventory review checklist

## Produce

- **Artifact:** updated `01_inventory/inventory.yaml` + `object-map.md`
- **Save under:** `01_inventory/` *(relative to your `project.root`, e.g.
  `docs/XXX260004-demo/01_inventory/inventory.yaml`)*
- **Required field on every program:** `criticality: critical | standard | low_risk`
  with `criticality_reason`. SME confirms the partition ONCE during this
  stage (batched, not per-program). See
  [`skills/legacy-ibmi-inventory/references/criticality-classifier.md`](../../../legacy-ibmi-inventory/references/criticality-classifier.md)
  — this is what lets the SME bandwidth scale to 200-program modules.
- **Consumed by:** `legacy-ibmi-program-analyzer`,
  `legacy-ibmi-flow-analyzer`, `legacy-ibmi-module-analyzer`

## Gate before advancing

- **Name:** Inventory Completeness Gate
- **Check:** `sme_review.decision ∈ {approved, approved_with_non_blocking_tbd}`
  AND every `coverage_gaps[].blocking: yes` is closed
- **Blocks if:** decision is `blocked`, or any blocking gap remains, or
  `sme_review` is absent

When blocked, the orchestrator **must refuse** to route to any downstream
skill until the gap is closed.

## SME action

- **Required:** yes — every inventory must be SME-approved before analysis
- **Ask:** "Confirm the in-scope object list. Are any objects missing? Which
  TBDs block progress vs. which are non-blocking?"
- **Recorded in:** `inventory.yaml.sme_review`,
  `inventory.yaml.coverage_gaps[]`

## Next card

- Inventory done → [`03-program-analysis.md`](03-program-analysis.md)
- Inventory blocked → stay on this card; do not advance.
