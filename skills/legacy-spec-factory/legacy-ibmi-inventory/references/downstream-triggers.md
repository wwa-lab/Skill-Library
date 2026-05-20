# Downstream Skill Triggers

Some Layer 1 skills are **optional supplemental** for small modules but
**mandatory** when inventory contents trigger them. Without this trigger
mechanism, screen-derived business rules and shared data models slip
through the cracks — they land randomly in `program-analysis.md` or get
re-derived by `legacy-spec-writer` from incomplete sources.

This doc defines the trigger conditions. The inventory skill detects them
during inventory, declares the result in `inventory.yaml.sme_review.downstream_required`,
and the SME confirms during the same single batched signoff (no extra
review round). Downstream gates then enforce them mechanically.

## Trigger 1 — `legacy-ibmi-screen-report-analyzer`

### When required

The skill becomes **required** for this module's `3b Program Analysis
Done` gate when ANY of:

| Signal | Source | Heuristic |
| --- | --- | --- |
| Any `OBJ-*` with `type: file, subtype: dspf` (display file) | inventory | unconditional |
| Any `OBJ-*` with `type: file, subtype: display_file` (alternate naming) | inventory | unconditional |
| Any `OBJ-*` with `type: menu` | inventory | unconditional |
| Any `OBJ-*` with `type: file, subtype: prtf` AND module has business rules influenced by report formats (totals lines, conditional rows) | inventory + program-analysis hint | only when reports drive business decisions; pure-output reports are not enough |
| SME flags "UI behavior carries rules" during inventory walkthrough | `EV-SME-*` | unconditional |

### Why mandatory when triggered

DSPF members carry business rules that DO NOT appear in RPG source:

- F-key bindings (F4=lookup, F9=update, F12=cancel) — what each key means
  in the business workflow
- Conditional field attributes (DSPATR(*PR) protect, DSPATR(*HI) highlight)
  driven by indicators — encode visibility / edit eligibility rules
- Subfile control specs (SFLNXTCHG, SFLINZ, SFLCLR) — drive list-edit
  semantics that the operator relies on
- Function-key text overrides — sometimes the only place a workflow's
  decision tree is documented

Letting program-analyzer infer these from RPGLE alone misses ~40% of
real screen-driven rules.

### What it produces (when triggered)

- `02_programs/<MODULE-SLUG>/screens/screen-report-analysis.md` (per
  DSPF / PRTF member)
- BR seeds tagged `knowledge_type: confirmed_from_code` (when the rule is
  pure DDS) or `inferred_business_rule` (when DSPF intent isn't obvious)

### Consumed by

- `legacy-ibmi-module-analyzer` View 1 (Operation Flow) — screen rules are
  central to user-facing operation
- `legacy-spec-writer` — UI surface section + behaviors

## Trigger 2 — `legacy-ibmi-data-model-analyzer`

### When required

The skill becomes **required** for this module's `3b Program Analysis
Done` gate when ANY of:

| Signal | Source | Heuristic |
| --- | --- | --- |
| `count(objects[].subtype ∈ {pf, physical_file, lf, logical_file, sql_table, table})` ≥ N (default N=3) | inventory | once you have 3+ files, the data model needs explicit modeling |
| Any two files share a key field (foreign-key-like relation) | inventory + DDS evidence | inferred from key field name overlap |
| Any program writes to ≥ 2 master files (compound transactional update) | program-analysis hint | compound writes imply transactional invariants worth modeling |
| SME flags "data model is non-trivial" during inventory walkthrough | `EV-SME-*` | unconditional |

For 1-2 file modules (like EXAMPLE-tutorial's `PRICE-CALC` which has just
`PRICEFL`), the trigger is NOT met and a separate data-model artifact
adds no value — spec-writer derives entities directly from inventory.

### Why mandatory when triggered

Once a module touches 3+ files with relationships, the spec's
`data_model.entities` becomes load-bearing. Without an upstream
data-model artifact:

- `legacy-spec-writer` re-derives entities from `program-analysis.md`
  File I/O rows scattered across N programs — incomplete and inconsistent
- Cross-program CRUD invariants are lost (program A writes ARMAST.BAL
  on credit memo; program B writes the same field on payment posting —
  no single artifact captures both, so the modernized data model loses
  the invariant)
- Index / access path decisions are invisible to forward SDLC

### What it produces (when triggered)

- `04_modules/<MODULE-SLUG>/data-model/dictionary.md` — entities,
  fields, types, relationships
- `04_modules/<MODULE-SLUG>/data-model/access-paths.md` — key fields,
  logical files, common joins
- `04_modules/<MODULE-SLUG>/data-model/crud-matrix.md` — per-program
  CRUD on each entity
- `04_modules/<MODULE-SLUG>/data-model/sme-checklist.md`

### Consumed by

- `legacy-ibmi-module-analyzer` View 4 (Data Flow)
- `legacy-spec-writer` `spec.yaml.data_model.entities` — populated from
  dictionary.md verbatim instead of re-derived
- `legacy-golden-master-test-planner` — test data shapes

## How inventory declares the triggers

After auto-detection, inventory adds a block to `inventory.yaml`:

```yaml
sme_review:
  decision: approved
  at: 2026-05-16
  by: "Jane Doe"
  criticality_confirmed_at: 2026-05-16
  criticality_summary: { critical: 12, standard: 21, low_risk: 14 }

  downstream_required:
    screen_report_analyzer:
      required: true
      reason: "Found 3 DSPF members: ORDENTRD, CUSTINQD, INVQRYD"
      triggered_by_objects: [OBJ-ORDER-ORDENTRD, OBJ-CUST-CUSTINQD, OBJ-INV-INVQRYD]
    data_model_analyzer:
      required: true
      reason: "Module touches 7 PF/LF files with shared key CUSTNO; 2 programs write ARMAST.BAL"
      triggered_by_objects: [OBJ-AR-ARMAST, OBJ-AR-PAYHIST, OBJ-CUST-CUSTMAST, OBJ-ORDER-ORDHDR, OBJ-ORDER-ORDDTL, OBJ-INV-INVMAST, OBJ-INV-PRICEFL]
```

The SME confirms the triggers in the same one-shot signoff that confirms
criticality. No extra review round.

If a trigger is auto-detected but SME explicitly overrides
(`required: false` with a reason), record the override:

```yaml
    screen_report_analyzer:
      required: false
      auto_detected: true
      override_reason: "DSPF exists but never used in production — display panel deprecated 2024"
      override_by: "Jane Doe"
      override_at: 2026-05-16
```

## Gate enforcement

`3b Program Analysis Done` requires:

- Every in-scope program has approved `program-analysis.md` (existing rule)
- IF `downstream_required.screen_report_analyzer.required: true` → every
  triggered DSPF/PRTF/menu has an approved `screen-report-analysis.md`
- IF `downstream_required.data_model_analyzer.required: true` →
  `04_modules/<MODULE-SLUG>/data-model/dictionary.md` exists at
  `review_status: approved` or `approved_with_non_blocking_tbd`

Orchestrator's Step 4B (Apply Hard Gates) reads these fields and refuses
to advance `stage_id` to `3b` until all triggered downstream artifacts
are present.

## Anti-patterns

- **Don't trigger screen-report-analyzer for pure output reports** that
  carry no business decisions (e.g. a monthly statement print that just
  reformats already-decided data). The trigger is for screens / reports
  that *encode* rules.
- **Don't trigger data-model-analyzer for 1-2 file modules**. Overhead
  exceeds value; spec-writer can handle it.
- **Don't let auto-detection silently override SME**. If SME says
  `required: false`, record their reason — don't quietly enable the
  trigger anyway.
- **Don't skip the SME confirmation step** for triggers. Auto-detection
  proposes; SME decides. Same one-shot batched signoff as criticality.
