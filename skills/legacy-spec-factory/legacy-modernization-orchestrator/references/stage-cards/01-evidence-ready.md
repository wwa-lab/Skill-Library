# Stage 01: Evidence Ready

**You are here if:** `evidence-manifest.yaml` exists, every item has
known `sensitivity`, an approved analysis path, and either source-path
authorization or completed redaction approval, and you have not yet produced
`inventory.yaml`.

This is the **first safe starting point** for reverse engineering. If you
arrived here from raw evidence, the Evidence Authorization Gate is now closed
behind you.

## Need before starting

- `evidence/redacted/evidence-manifest.yaml` or
  `evidence/intake/evidence-manifest.yaml` (approved)
- `redaction-log.md` or source-authorization log
- The approved source / metadata bundle referenced by the manifest
- SME contact for the module under review, if already known; otherwise capture
  SME questions during inventory

## Run

- **Skill:** `legacy-ibmi-inventory` (Implemented v0.1.0)
- **Manual fallback:** Use the `inventory.yaml` skeleton in
  `skills/legacy-ibmi-inventory/references/` and fill it by hand against
  `docs/id-conventions.md`

## Produce

- **Artifact:** `inventory.yaml` + `object-map.md`
- **Save under:** `01_inventory/` *(relative to your `project.root`, e.g.
  `docs/XXX260004-demo/01_inventory/inventory.yaml`)*
- **Consumed by:** `legacy-ibmi-program-analyzer`, `legacy-ibmi-flow-analyzer`,
  `legacy-ibmi-module-analyzer`

Every object must carry an `OBJ-*` id, `type`, `source_member`, and a link to
at least one evidence id from `evidence-manifest.yaml`.

## Gate before advancing

- **Name:** Inventory Completeness Gate
- **Check:** `inventory.yaml.sme_review.decision ∈ {approved,
  approved_with_non_blocking_tbd}` AND no `coverage_gaps[].blocking: yes`
- **Blocks if:** decision is `blocked`, or any blocking coverage gap is
  unresolved

## SME action

- **Required:** yes — to confirm scope and unblock coverage gaps
- **Ask:** "Is this list of objects the complete in-scope set? Are any
  missing programs / files / data areas? Which TBDs are blocking?"
- **Recorded in:** `inventory.yaml.sme_review` + `coverage_gaps[]`

## Next card

[`02-inventory.md`](02-inventory.md) — if your inventory is **in progress**
or **blocked**, stay there until SME approval.

Otherwise (inventory approved): [`03-program-analysis.md`](03-program-analysis.md).
