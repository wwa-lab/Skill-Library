# Evidence Intake Review Checklist

## Scope

- capability_slug:
- manifest_path:
- redaction_log_path:
- package_state: draft | blocked | approved_for_inventory
- intake_mode: internal_source_review | governed_redaction
- reviewer:
- review_date:

## Checklist

- [ ] Capability scope is narrow enough for inventory analysis.
- [ ] Data owner approved evidence export.
- [ ] Every evidence item has an `EV-<SLUG>-NNN` ID.
- [ ] Every evidence item has a type and source location.
- [ ] No item has `sensitivity: unknown`.
- [ ] Every item has either `source_path_verified: true` with an approved
      analysis path, or a completed redaction record.
- [ ] Items with `redaction_required: true` have redaction status `approved`.
- [ ] Redaction/source-authorization log records strategy without exposing raw
      sensitive values.
- [ ] Rule-critical constants, thresholds, coefficients, and amounts are
      preserved or explicitly labeled as synthetic.
- [ ] Field shape, control flow, timestamps, and error codes are preserved where
      downstream analysis needs them.
- [ ] Missing evidence is recorded as `TBD-*`.
- [ ] Contradictory evidence is recorded and routed to SME decision.
- [ ] Intake reviewer is named.
- [ ] Redaction owner is named when redaction is required.
- [ ] SME owner is named only when SME review is required for Step 0; otherwise
      SME review is recorded as deferred/not required for inventory.
- [ ] Manifest package state and intake decision allow or block
      `legacy-ibmi-inventory` consistently.

## Findings

| ID | Severity | Evidence ID | Finding | Required Action | Blocking |
| --- | --- | --- | --- | --- | --- |
| FIND-<SLUG>-001 | blocking | EV-<SLUG>-001 | <finding> | <action> | yes |

## Inventory Gate Decision

- decision: pass | pass_with_warnings | blocked
- downstream_inventory_allowed: yes | no
- blocking_items:
- non_blocking_items:
- next_step: legacy-ibmi-inventory | evidence-intake rework
