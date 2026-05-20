# Stage 04: Flow Analysis (one business transaction at a time)

**You are here if:** every in-scope program has an approved
`program-analysis.md` AND you want to trace one complete business
transaction end-to-end across all the programs it touches.

You will produce **one flow file per business transaction** (e.g. "submit
order", "post AR invoice"). A flow may cover one of seven trigger models:
batch job, interactive menu, subfile dispatch, F-key branch, DB trigger,
scheduler, API/remote.

## Need before starting

- `02_programs/<MODULE>/<OBJ>/program-analysis.md` for every program the
  flow touches (all at `approved` or `approved_with_non_blocking_tbd`)
- `01_inventory/inventory.yaml` (approved)
- The trigger artifact for this flow: the menu, scheduler entry, DB trigger
  binding, API surface, or batch JOBSCDE entry
- SME contact for cross-program data flow questions

## Run

- **Skill:** `legacy-ibmi-flow-analyzer` (Implemented v0.1.0)
- **Manual fallback:** Use the flow skeleton in
  `skills/legacy-ibmi-flow-analyzer/references/` and synthesize across the
  per-program analyses

## Produce

- **Artifact:** `flow-<FLOW-SLUG>.md`
- **Save under:**
  `03_flows/<MODULE-SLUG>/flow-<FLOW-SLUG>.md`
  *(relative to your `project.root`)*
  e.g. `docs/XXX260004-demo/03_flows/CREDIT-CHECK/flow-submit-order.md`
- **Consumed by:** `legacy-ibmi-module-analyzer`

Required sections: Trigger Context, Sequence, Cross-Program Data Flow, Error
Propagation, Commit Boundaries, UI Surfaces, Business-Capability Seeds
(`CAP-*`).

## Gate before advancing

- **Name:** (none specific) — advancement is gated by **flow coverage**:
  every business transaction the module supports must have an approved
  flow before module analysis is complete
- **Check:** `flow-*.md` files cover every named transaction the SME lists
  for this module
- **Blocks if:** a known business transaction has no flow, OR any flow is
  at `status: draft` with money / inventory / compliance impact

## SME action

- **Required:** to confirm trigger context, commit boundaries, and which
  flows count as "the module's business"
- **Ask:** "Is this the complete sequence under trigger X? What happens on
  error after step N? Is the commit boundary at step M correct?"
- **Recorded in:** `flow-<slug>.md` → `status` and the per-step
  `review_status` columns

## Next card

[`05-module-analysis.md`](05-module-analysis.md) — once all the module's
flows are approved.
