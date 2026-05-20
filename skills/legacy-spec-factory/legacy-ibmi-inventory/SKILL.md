---
name: legacy-ibmi-inventory
description: Inventory IBM i / AS400 legacy assets for modernization. Use when collecting or reviewing RPGLE, CLLE, COBOL, DDS, DB2 for i, jobs, screens, reports, spool, and runtime evidence before generating an evidence-backed spec. Layer 1 (platform-specific) skill of the Legacy Spec Factory reverse chain.
license: Apache-2.0
metadata:
  author: Leo L Zhang
  maintainer: platform-engineering
  source: https://github.com/wwa-lab/legacy-spec-factory
  source_commit: 8871a6b
  domain: legacy-spec-factory
---

<!--
Legacy Spec Factory
Copyright 2026 Leo L Zhang

Original author: Leo L Zhang
License: Apache License 2.0

This skill is part of the Legacy Spec Factory project.
Retain this notice in substantial copies or derived versions.
-->

# IBM i Legacy Inventory

## Purpose

Create a structured inventory of IBM i / AS400 legacy assets for one business
capability. This skill does not infer business rules and does not generate
Java. It establishes the evidence baseline required before deeper analysis or
`spec.yaml` generation.

## Inputs

Accept any combination of:

- source member listings or exported source files
- RPGLE, CLLE, COBOL, DDS source
- DB2 for i table and field metadata
- job descriptions, scheduler notes, or CL command flow
- DSPF, PRTF, spool, report, and screen samples
- SME notes about known programs, files, jobs, reports, or hidden dependencies

If raw production samples, logs, spool, screenshots, or DB extracts are present
without source-path authorization or required redaction approval, stop and route
to `legacy-ibmi-evidence-intake`. Internal source members and metadata may be
used when the evidence manifest records `source_path_verified: true`.

## Output Contract

Produce:

- `01_inventory/inventory.yaml`
- `01_inventory/object-map.md`
- `01_inventory/inventory-review-checklist.md`
- unresolved questions using `TBD-<SLUG>-<NNN>` IDs

Use the templates in:

- `templates/inventory.yaml`
- `templates/inventory-review-checklist.md`

Follow:

- `../../../docs/legacy-spec-factory/id-conventions.md`
- `../../../docs/legacy-spec-factory/evidence-and-knowledge-taxonomy.md`
- `../../../docs/legacy-spec-factory/input-readiness-rubric.md`
- `references/output-contract.md`

Examples:

- `examples/redacted-customer-credit-check/`
- `examples/missing-artifact-negative-case/`

## Step Contract

This skill is one step in the Legacy Spec Factory reverse chain. It conforms
to the canonical Step Contract shape — see
`../legacy-step-contract/SKILL.md` and
`../legacy-step-contract/references/step-contract.md` for the full
field-level rules. The summary below is normative for this skill.

### Input

- **Required**: evidence manifest at `package_state: approved_for_inventory`
  plus approved analysis paths for source members, DDS, DB2 metadata,
  job/scheduler notes, screen/spool/report samples; capability scope
  (name + slug + libraries + collection date); assigned intake reviewer.
- **Optional**: prior shop inventory spreadsheets, wiki references, vendor
  docs (treat as tier 3/4 hints, never as ground truth); assigned SME owner
  when available for inventory completeness review.
- **Input readiness scoring**:
  - `0-5 blocked`: approved manifest missing, required source/object listings
    unavailable, evidence authorization unresolved, scope is the whole
    application, or no stable capability slug exists.
  - `6 minimum_pass`: approved manifest, ground-truth source/object listings,
    approved analysis paths, capability scope, and intake reviewer are present.
  - `7-8 usable`: DDS/DB metadata, job/scheduler notes, and screen/report
    samples are included for most referenced objects.
  - `9-10 strong`: SME hints, prior inventory, runtime/spool samples, hidden
    dependency notes, and downstream focus are also supplied.
  - Missing SME owner does not block starting inventory; it blocks marking
    inventory done if SME completeness review is required.
- **Readiness checks**: Evidence Authorization Gate has cleared each evidence
  item; no `sensitivity: unknown`; capability slug stable; every item has
  either `source_path_verified: true` or completed required redaction.
- **Stop conditions**: unauthorized raw production evidence is present;
  capability is "the whole application" (require a narrower slice);
  ground-truth tier 1 source listings (`WRKOBJ` / `DSPOBJD` /
  source-member listings) are not available.

### Execution

- **Procedure**: see the Workflow section below (7 ordered steps).
- **Allowed inference**: cross-referencing a referenced object against the
  inventory; classifying object types from DDS/source headers; assigning
  evidence IDs.
- **Forbidden assumptions**: inventing libraries, programs, files, fields,
  jobs, reports, or calls; inferring business rules from inventory alone;
  treating source comments or prior spreadsheets as truth without tier-1
  verification.
- **TBD handling**: use `TBD-<SLUG>-<NNN>`. Distinguish `coverage_gaps`
  (artifact missing — a developer can fix) from `open_questions` (only an
  SME can answer) per `references/output-contract.md`.

### Output

- **Canonical artifacts**: `01_inventory/inventory.yaml`,
  `01_inventory/object-map.md`,
  `01_inventory/inventory-review-checklist.md`.
- **Required fields/sections**: capability metadata, evidence ledger, object
  inventory, relationship map, `coverage_gaps`, `open_questions`,
  `sme_review`.
- **Required IDs**: `OBJ-*` for every object; `EV-*` for every evidence
  item; `TBD-*` for every gap or open question. No `BR-*`, `BEH-*`, or
  `DEC-*` minted here.
- **Handoff status**: `sme_review.decision` must be `approved` or
  `approved_with_non_blocking_tbd` before downstream skills run; `blocked`
  halts the chain.

### Validation

- **Mechanical**: every object has `id`, `evidence_ids`, and a non-`unknown`
  sensitivity; every relationship resolves to two `OBJ-*`; every TBD
  carries a category; required files exist.
- **AI semantic**: object scope matches the capability slug; no inferred
  business rules sneaking into `notes`; comments/spreadsheets cited as
  hints, not as ground truth; PRTF/DSPF/PF/LF/job/subroutine gaps surfaced
  as TBDs rather than smoothed over.
- **SME / human approval**: SME records `sme_review.decision`, signed-off
  object coverage, hidden-dependency confirmation, report/spool confirmation,
  and any sensitivity confirmation that required SME judgment. SME review is
  the gate for marking inventory done, not for starting developer-led inventory
  from an approved evidence manifest.
- **Blocking conditions**: any object lacks an ID or evidence link; any
  `sensitivity: unknown` remains; SME marks `decision: blocked`; any
  `coverage_gaps` entry with `blocking: yes` is unresolved.

Emit a Step Validation Report (see
`../legacy-step-contract/templates/step-validation-report.md`) with status
`pass`, `pass_with_warnings`, or `blocked` when reporting upward to the
orchestrator.

## Workflow

1. **Define capability scope**
   Identify the business capability name, slug, source libraries, date of
   collection, and known reviewer/SME owner when available. If the scope is a
   whole application, ask for a narrower slice.

2. **Classify input evidence**
   Assign evidence IDs to each source bundle, metadata export, report sample,
   spool sample, job log, screen sample, and SME note. Mark sensitivity as
   `public`, `internal`, `confidential`, or `unknown`, preserving
   `source_path_verified` / `redaction_required` status from the evidence
   manifest.

3. **Inventory legacy objects**
   Extract or list programs, service programs, CL commands, PF, LF, DSPF, PRTF,
   jobs, reports, data areas, data queues, message queues, copybooks, and
   external interfaces.

4. **Capture relationships**
   Record known or observed relationships:

   - program calls
   - file usage
   - display file usage
   - printer file usage
   - submitted jobs
   - external calls
   - control tables
   - data areas and queues

5. **Identify coverage gaps**
   Create TBDs for missing DDS, missing PRTF, unresolved called programs,
   unknown job flow, unclear screen/report artifacts, or evidence awaiting
   authorization/redaction.

6. **Prepare SME review**
   Generate an inventory review checklist that asks the SME to confirm object
   coverage, hidden dependencies, critical reports, and missing runtime
   evidence.

7. **Gate the output**
   Do not mark the inventory `approved` unless:

   - every listed object has an ID
   - every object links to evidence or SME confirmation
   - missing objects are explicit TBDs
   - sensitivity is not `unknown`
   - PRTF, DSPF, PF/LF, job, and deep subroutine gaps are called out

## Program Criticality Classification

Every program object in `inventory.yaml` MUST carry a `criticality` field
with one of `critical | standard | low_risk`. This drives SME review
routing downstream — without it, every program gets equal review
intensity and the SME bandwidth bottleneck cannot be relieved.

Apply the heuristic in
[`references/criticality-classifier.md`](references/criticality-classifier.md).
Default to `standard` when the heuristic does not match a `critical` or
`low_risk` pattern.

Schema addition to each `objects[]` entry of type `program`:

```yaml
- id: OBJ-<MODULE>-<NAME>
  type: program
  # ... existing fields ...
  criticality: critical | standard | low_risk
  criticality_reason: <one-line why, e.g. "writes ARMAST" or "read-only display program">
  criticality_confirmed_by_sme: false   # flipped to true after SME signoff
```

**SME confirmation is a single batched step**, not per-program:

1. Inventory skill auto-classifies all programs using the heuristic.
2. Inventory skill emits a per-bucket count summary to the SME
   (see `criticality-classifier.md` → "SME confirmation"):
   ```
   critical:  12 programs   (need deep SME review)
   standard:  21 programs   (spot-check sample)
   low_risk:  14 programs   (batch confirm)
   ```
3. SME confirms the partitioning OR names specific programs to reclassify
   with reasons.
4. After SME signoff, set `criticality_confirmed_by_sme: true` on every
   reclassified entry, and record the confirmation moment in
   `inventory.yaml.sme_review.criticality_confirmed_at: <ISO date>`.

Until step 4 completes, downstream skills MUST treat every program as
`standard` (the conservative default) to prevent under-reviewing a
mis-classified `critical` program.

**Anti-pattern:** do NOT use criticality to skip program analysis for
`low_risk` programs. The analysis is still produced at full depth — only
the SME review effort downstream is dialed down.

## Downstream Skill Triggers (DSPF + Data Model)

Two supplemental Layer 1 skills are **optional for tiny modules but
mandatory once inventory contents trigger them**. Without this trigger
mechanism, screen-derived business rules and shared data-model
invariants slip through into ad-hoc program-analysis prose.

Detect during inventory; SME confirms in the same single batched signoff
as criticality.

### Auto-detect rules (apply during inventory)

Set `inventory.yaml.sme_review.downstream_required.screen_report_analyzer.required: true` when ANY of:

- inventory has an object with `subtype ∈ {dspf, display_file, menu}`
- inventory has `subtype: prtf` AND the report carries business
  decisions (totals lines, conditional rows) — not pure output

Set `inventory.yaml.sme_review.downstream_required.data_model_analyzer.required: true` when ANY of:

- count(objects with `subtype ∈ {pf, physical_file, lf, logical_file, sql_table, table}`) ≥ 3
- two files share a key field name (foreign-key-like relation)
- any program writes to ≥ 2 master files (compound transactional update)

Full rule set, examples, and overrides documented in
[`references/downstream-triggers.md`](references/downstream-triggers.md).

### Inventory output additions

Append the trigger block to `inventory.yaml`:

```yaml
sme_review:
  decision: approved
  criticality_summary: { critical: N, standard: M, low_risk: K }
  downstream_required:
    screen_report_analyzer:
      required: true | false
      reason: <one line — why detected or why N/A>
      triggered_by_objects: [OBJ-*, ...]    # objects that triggered the detection
    data_model_analyzer:
      required: true | false
      reason: <one line>
      triggered_by_objects: [OBJ-*, ...]
```

If SME overrides an auto-detection (e.g. a DSPF exists but is dead
code), record `override_reason` + `override_by` + `override_at` per the
schema in `downstream-triggers.md`.

### Why this matters

Once `downstream_required.<skill>.required: true` is committed in
`inventory.yaml`, the orchestrator's `3b Program Analysis Done` gate
will refuse to advance until the triggered artifact (`screen-report-analysis.md`
under `02_programs/<MODULE>/screens/`, or `04_modules/<MODULE>/data-model/dictionary.md`)
is also produced and approved. The trigger turns optional skills into
**mechanically enforced prerequisites** when their inputs are present.

## Workflow State Write-Back

At the end of an inventory run, update `<project-root>/workflow-state.yaml`
per [`docs/workflow-state-contract.md`](../../../docs/legacy-spec-factory/workflow-state-contract.md).
Template: [`skills/legacy-modernization-orchestrator/references/state-writeback-snippet.md`](../legacy-modernization-orchestrator/references/state-writeback-snippet.md).

**Stage this skill produces:**

- `2c Inventory Done` when `inventory.yaml.sme_review.decision ∈ {approved,
  approved_with_non_blocking_tbd}` AND no `coverage_gaps[].blocking: yes`
  remains
- `2b Inventory Blocked` when `sme_review.decision: blocked` OR any
  blocking `coverage_gaps[]` is unresolved
- `2a Inventory In Progress` when the inventory is partial and `sme_review`
  is absent

**Last artifact path pattern:** `01_inventory/inventory.yaml`

**Writes per run:**

1. Overwrite `capabilities[<CAP-* from current_focus>]` (or the entry keyed
   by module slug if no CAP-* yet) with stage id, artifact path,
   `last_skill: legacy-ibmi-inventory`, and blocking IDs (`tbds`,
   `sme_pending`, `gates: ["inventory_completeness"]` if 2b).
2. Append one `history[]` entry with the run's outcome and SME decision.
3. Overwrite `project.last_updated_at` / `project.last_updated_by`.

Never touch `current_focus`, other capabilities' entries, or past
`history[]` rows. If you re-run inventory on a capability already at a
later stage, do not lower `stage_id` — surface and ask the orchestrator
to run the Rollback Protocol.

## Anti-Hallucination Rules

**Code is ground truth.** See `../../../docs/legacy-spec-factory/code-as-ground-truth.md`. The
inventory enumerates objects that actually exist in the production
library — confirmed via current `WRKOBJ` / `DSPOBJD` / source-member
listings (tier 1). Prior inventory spreadsheets, shop catalogs, wikis,
and SME recollection are starting points (tier 3/4); every entry must
be verified against tier 1 before being recorded.

- Do not invent libraries, programs, files, fields, jobs, reports, or calls.
- If a referenced object is not present in current production, create a TBD instead of filling it in (it may be deprecated, renamed, or never have existed).
- Do not infer business rules from inventory alone.
- Do not treat source comments as truth without tier-1 verification or SME review.
- Keep `observed`, `inferred`, and `unknown` separate.

## SME Review Questions

Ask the SME to confirm:

- Are all expected programs and called routines listed?
- Are any CL-submitted jobs, job scheduler entries, or overrides missing?
- Are all PF/LF, DSPF, and PRTF objects accounted for?
- Are there control files, data areas, data queues, or message queues?
- Are reports and spool outputs tied to the correct printer files?
- Are there shop-specific naming conventions or copybooks that affect analysis?
- Which missing items block downstream program analysis or spec generation?

## Runtime Portability

The canonical skill source lives under:

```text
skills/legacy-ibmi-inventory/SKILL.md
```

Runtime copies may be synced to:

```text
.claude/skills/legacy-ibmi-inventory/SKILL.md
.opencode/skills/legacy-ibmi-inventory/SKILL.md
.agents/skills/legacy-ibmi-inventory/SKILL.md
.codex/skills/legacy-ibmi-inventory/SKILL.md
```

Use `../../../scripts/legacy-spec-factory/sync-skills.sh` to create or check runtime copies.

## Version History

- v0.3.0 (2026-05-16): Added `downstream_required` block to
  `sme_review`. Inventory now auto-detects when
  `legacy-ibmi-screen-report-analyzer` and
  `legacy-ibmi-data-model-analyzer` should be MANDATORY (not optional)
  for this module, declares the requirement in inventory.yaml, and SME
  confirms in the same batched signoff. Orchestrator's `3b Program
  Analysis Done` gate now mechanically enforces these triggers — turning
  optional supplemental skills into prerequisites when their inputs are
  present. Trigger rules in `references/downstream-triggers.md`.
- v0.2.0 (2026-05-16): Added program criticality classification
  (`critical | standard | low_risk` with `criticality_reason`) and the
  single-batched SME confirmation workflow. Drives downstream review
  routing in `legacy-sme-review-facilitator` so 200-program modules no
  longer require 200 separate SME reviews. Heuristic + anti-patterns
  documented in `references/criticality-classifier.md`.
- v0.1.0 (2026-05-13): Initial reference implementation for the Legacy Spec
  Factory review gate.
