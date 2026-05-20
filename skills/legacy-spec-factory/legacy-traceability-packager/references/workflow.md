<!--
Legacy Spec Factory
Copyright 2026 Leo L Zhang

Original author: Leo L Zhang
License: Apache License 2.0
-->

# Traceability Packager Workflow — Eight Ordered Steps

This document is the executable procedure for `legacy-traceability-packager`. It is referenced from `SKILL.md` and from `references/output-contract.md`.

The workflow is **block-by-default**. Each step ends either in `pass`, `warning`, or a `blocking` finding. A blocking finding does not automatically short-circuit the audit: continue collecting findings when the remaining checks can be evaluated safely from redacted, resolved inputs. If a failed gate makes later checks unreliable or unsafe, mark those later gates `not_evaluated`. A blocked status locks the final outcome regardless of later passes, and only `traceability-review.md` + `blocking-findings.yaml` are written.

---

## Step 1 — Intake and Source Resolution

1. Resolve the capability slug from the caller or from `05_specs/<CAPABILITY-SLUG>/spec.yaml.capability.slug`.
2. Confirm `05_specs/<CAPABILITY-SLUG>/spec.yaml` and `spec.md` exist and are readable.
3. Confirm `spec.yaml.status` is `approved`. If not, demand an explicit `status_override: blocked_audit` from the caller; otherwise raise `SPEC-NOT-APPROVED`.
4. Resolve optional artefacts and record presence flags:
   - `05_brds/<CAPABILITY-SLUG>/brd.md` + `brd-review.md`
   - `06_sdd_handoffs/<CAPABILITY-SLUG>/sdd-handoff.yaml` (cross-check only — never overwritten)
   - golden master test plan, if produced by `legacy-golden-master-test-planner`
5. Resolve required upstream chain:
   - `01_inventory/inventory.yaml`
   - every `02_programs/<OBJ-ID>/program-analysis.md` referenced by the spec
   - every `03_flows/<FLOW-SLUG>/flow.md` referenced by the spec
   - the `04_modules/<MODULE-SLUG>/` directory whose `MODULE-*` ID seeded the capability
6. Resolve the evidence manifest from `legacy-ibmi-evidence-intake` (typically `evidence/manifest.yaml`). Capture `package_state`, `intake_decision.downstream_inventory_allowed`, and the full `evidence_items[]` list.

Findings:

| Condition | Finding | Severity | Action |
| --- | --- | --- | --- |
| `spec.yaml` missing | `SPEC-MISSING` | blocking | route to `legacy-spec-writer`; never substitute the BRD or analyses |
| `spec.yaml.status` below `approved` and no `blocked_audit` override | `SPEC-NOT-APPROVED` | blocking | route to `legacy-spec-writer` |
| any required upstream artefact missing or below `approved_with_non_blocking_tbd` | `UPSTREAM-NOT-APPROVED` | blocking | route to the named owning analyzer |
| evidence manifest `package_state` ≠ `approved_for_inventory` | `EVIDENCE-PACKAGE-NOT-APPROVED` | blocking | route to `legacy-ibmi-evidence-intake` |
| BRD referenced but `status` below `approved` | `BRD-NOT-APPROVED` | blocking | route to `legacy-brd-writer` |
| pre-existing `06_sdd_handoffs/<CAP>/sdd-handoff.yaml` has `status: blocked` | `HANDOFF-PREVIOUSLY-BLOCKED` | info | record for cross-reference |

---

## Step 2 — ID Inventory

Build a deterministic inventory of every ID that appears in any source artefact:

- `CAP-*`, `BRD-*`, `MODULE-*`, `FLOW-*`, `NODE-*`, `EDGE-*`, `DATA-*`, `VIEW-*`, `ACTOR-*`, `SYS-*`, `OBJ-*` (carried for context)
- `EV-*`, `BEH-*`, `BR-*`, `DEC-*`, `STEP-*`, `IN-*`, `OUT-*`, `EX-*`, `AC-*`, `TC-*`, `TBD-*`, `SEED-*`

For each prefix record:

- count of distinct IDs
- list of IDs (kept verbatim, no renumbering)
- source artefact for each ID (`spec.yaml`, `brd.md`, `inventory.yaml`, etc.)

Mechanical rule: every ID must conform to `docs/id-conventions.md`. IDs that do not conform raise `ID-FORMAT-INVALID` (blocking, route to the owning skill).

The inventory is the only structure the rest of the workflow walks. Subsequent steps never re-read the upstream artefacts for content; they query this inventory plus the manifest.

---

## Step 3 — Cross-Reference Walk (Dangling-ID Check)

For every cross-reference field in the spec and BRD, confirm the target ID exists in Step 2's inventory:

| Field | Target prefix | Finding on miss |
| --- | --- | --- |
| `business_rules[].evidence_ids[]` | `EV` | `EV-DANGLING-IN-BR` (blocking) |
| `business_rules[].linked_behaviors[]` | `BEH` | `BEH-DANGLING-IN-BR` (blocking) |
| `business_rules[].acceptance_criteria_ids[]` (or `acceptance_criteria[].validates[]` inverse) | `AC` | `AC-DANGLING-IN-BR` (blocking) |
| `acceptance_criteria[].validates[]` | `BR` | `BR-DANGLING-IN-AC` (blocking) |
| `observed_behaviors[].evidence_ids[]` | `EV` | `EV-DANGLING-IN-BEH` (blocking) |
| `modernization_decisions[].evidence_ids[]` | `EV` | `EV-DANGLING-IN-DEC` (blocking) |
| `modernization_decisions[].rationale` references | `BR`, `BEH`, or constraint | `DEC-NO-RATIONALE` (warning) |
| `data_model.entities[].legacy_sources[]` | `OBJ` | `OBJ-DANGLING-IN-DATA-MODEL` (blocking) |
| `data_model.entities[].fields[].evidence_ids[]` | `EV` | `EV-DANGLING-IN-DATA-MODEL` (blocking) |
| `process_flow.steps[].evidence_ids[]` | `EV` | `EV-DANGLING-IN-STEP` (blocking) |
| `inputs[].evidence_ids[]`, `outputs[].evidence_ids[]`, `exceptions[].evidence_ids[]` | `EV` | `EV-DANGLING-IN-IO` (blocking) |
| `tests[].validates[]` | `AC` or `BR` | `TC-DANGLING-VALIDATES` (blocking) |
| `tests[].sample_data_ref` (when stated as an `EV-*`) | `EV` | `EV-DANGLING-IN-TC` (blocking) |
| `open_questions[].related_ids[]` | any | `TBD-DANGLING-REF` (warning) |
| `traceability[].from_id`, `traceability[].to_ids[]` | any | `TRACE-DANGLING-REF` (blocking) |

A single dangling ID is **enough** to block the package — even if everything else passes. The packager records all dangling IDs in one pass so the upstream skill can fix them in one revision.

If `06_sdd_handoffs/<CAP>/sdd-handoff.yaml` exists, cross-check that every ID it carries appears in the spec / BRD with identical wording. Mismatches raise `HANDOFF-ID-MISMATCH` (blocking — route to `legacy-brd-to-sdd-handoff` and `legacy-spec-writer` to reconcile).

---

## Step 4 — Evidence Sensitivity and Manifest Check

For every `EV-*` in the inventory, look it up in the evidence manifest:

| Manifest condition | Finding | Severity | Action |
| --- | --- | --- | --- |
| `EV-*` not found in `evidence_items[].evidence_id` | `EVIDENCE-MANIFEST-MISS` | blocking | repair upstream manifest |
| `sensitivity: unknown` | `EVIDENCE-SENSITIVITY-UNKNOWN` | blocking | route to `legacy-ibmi-evidence-intake` |
| `redaction_required: true` and `redaction_status: approved` | `EVIDENCE-REDACTED` | pass | continue |
| `redaction_required: true` and `redaction_status` is anything else | `EVIDENCE-AWAITING-REDACTION` | blocking | route to `legacy-ibmi-evidence-intake` |
| `redaction_required: false` and `source_path_verified: true` and `redaction_status: not_required`, `reviewed`, or `approved` | `EVIDENCE-SOURCE-AUTHORIZED` | pass | continue |
| `redaction_required: false` and `source_path_verified` is not `true` | `EVIDENCE-SOURCE-NOT-AUTHORIZED` | blocking | route to `legacy-ibmi-evidence-intake` |
| `redacted_filename` missing or null | `EVIDENCE-APPROVED-PATH-MISSING` | blocking | route to `legacy-ibmi-evidence-intake` |
| `sme_required: true` and `sme_approval` not `true` | `EVIDENCE-SME-APPROVAL-MISSING` | blocking | request evidence SME approval |

`sensitivity: unknown` is **always** blocking. The packager never assumes a
default sensitivity. SME approval is required only when the evidence manifest
marks `sme_required: true`; internal source-review evidence with
`sme_required: false` must not be blocked for missing SME approval.

Also build `evidence_coverage` for Step 6: for every `EV-*`, list the IDs that reference it (`BEH-*`, `BR-*`, `DEC-*`, `STEP-*`, `AC-*`, `TC-*`, `IN-*`, `OUT-*`, `EX-*`, data-model fields).

An `EV-*` that is **not** referenced by any other ID is an **orphan**:

- Default severity: `warning` (`ORPHAN-EVIDENCE`).
- Promoted to `blocking` (`ORPHAN-EVIDENCE-IN-CLOSURE-PACKAGE`) when the spec / BRD claims full evidence closure (e.g. spec-review.md asserts "every EV used"), since an orphan contradicts that claim.
- Demoted to `info` only when `spec-review.md` records an explicit SME waiver naming the `EV-*` and reason.

---

## Step 5 — Business Rule Closure Check

For each `BR-*`:

1. If `review_status` is `draft` or `needs_sme_review`, record `BR-PENDING-SME-REVIEW` (info — the spec is responsible, not the packager).
2. If `review_status` is `approved`:
   - confirm ≥1 `EV-*` linked → else `BR-NO-EVIDENCE` (blocking)
   - confirm ≥1 `BEH-*` linked → else `BR-NO-BEHAVIOR` (blocking)
   - confirm ≥1 `AC-*` linked (either via `business_rules[].acceptance_criteria_ids[]` or via `acceptance_criteria[].validates[]` reverse lookup) → else `BR-MISSING-AC` (blocking)
3. If `review_status` is `rejected` or `retired` but still referenced by an `AC-*`, raise `BR-RETIRED-BUT-LINKED` (blocking).

For each `AC-*`:

1. Confirm `validates[]` is non-empty and resolves to existing `BR-*` records → else `AC-NO-RULE` (blocking).
2. If `validates[]` points to a `BR-*` whose `review_status` is not `approved`:
   - default severity: `AC-VALIDATES-UNAPPROVED-BR` (blocking)
   - demoted to `warning` only when `spec-review.md` records an explicit named SME waiver for this AC, quoting the AC ID and reason
3. Confirm `review_status: approved` for every AC referenced from an approved `BR-*` → else `AC-NOT-APPROVED` (blocking unless SME-waived).

For each `DEC-*`:

1. Rationale must mention at least one of `BR-*`, `BEH-*`, or an explicit platform / regulatory constraint → else `DEC-NO-RATIONALE` (warning).
2. `review_status` ≠ `approved` is recorded as `DEC-NOT-APPROVED` (info — `legacy-spec-writer` and the architecture / product authority own this).

---

## Step 6 — Coverage Tables (EV, BEH, BR, AC, TC, DEC)

Assemble the structured coverage tables required by `traceability-package.yaml`:

- `evidence_coverage[]`: one row per `EV-*` with `referenced_by[]` and `is_orphan` boolean.
- `behavior_coverage[]`: one row per `BEH-*` with `supporting_evidence_ids[]` and `backs_rules[]`.
- `business_rule_coverage[]`: one row per `BR-*` with `evidence_ids[]`, `behavior_ids[]`, `acceptance_criteria_ids[]`, `review_status`, and `closure_status` (`closed | open | retired`).
- `acceptance_criteria_coverage[]`: one row per `AC-*` with `validates[]`, `tested_by[]` (the `TC-*` IDs that exercise it), and `review_status`.
- `test_coverage[]`: one row per `TC-*` with `type`, `validates[]`, `sample_data_evidence_id`, and `golden_master_enabled`.
- `decision_coverage[]`: one row per `DEC-*` with `cites_rules[]`, `cites_behaviors[]`, `cites_constraints[]`, and `review_status`.

Every row must be derivable from upstream content. If a row would require a new fact, raise `COVERAGE-DATA-MISSING` (blocking — route to the owning skill).

Aggregate coverage metrics for the human view:

- approved `BR-*` closure rate = `count(BR with EV ∧ BEH ∧ AC) / count(approved BR)`
- AC approval rate = `count(approved AC) / count(AC referenced by approved BR)`
- TC-to-AC coverage = `count(AC with ≥1 TC) / count(approved AC)`
- evidence usage rate = `count(EV referenced ≥1 time) / count(EV in inventory)`

These metrics are descriptive. They do not change the status — only the gate rules above do.

---

## Step 7 — TBD Carry-Forward

Apply the deferral predicate (identical to `legacy-brd-to-sdd-handoff` Step 3):

A `TBD-*` with `blocking: true` is treated as a **warning** only when **every** condition is met:

| Field | Requirement |
| --- | --- |
| `blocking` | `true` (SME chose not to demote) |
| `resolution` | non-empty string naming the SME and the deferral target |
| `resolver` | non-empty; must name a real SME from the spec / BRD roster |
| `planned_resolution_date` | an ISO 8601 date that is not earlier than the package audit date |
| `deferral_recorded_in` | pointer such as `spec-review.md#sme-decisions` |

Severity table:

| `blocking` | Predicate satisfied? | Finding | Severity |
| --- | --- | --- | --- |
| `true` | n/a, `resolution` unset / `pending` | `BLOCKING-TBD-UNRESOLVED` | blocking |
| `true` | all fields satisfied | `BLOCKING-TBD-DEFERRED` | warning (status becomes `pass_with_warnings`) |
| `true` | partially satisfied | `BLOCKING-TBD-UNRESOLVED` | blocking (no silent upgrade) |
| `false` | n/a | `NON-BLOCKING-TBD` | info |

All TBDs that survive Step 7 flow into `traceability-package.yaml.open_questions[]` **verbatim**. The packager never edits, paraphrases, merges, or demotes TBDs.

For each TBD also record `next_routing.responsible_skill` (typically `legacy-spec-writer` or `legacy-brd-writer`) and `next_routing.capability_owner` (the SME).

---

## Step 8 — Assemble and Sign-Off

### 8a. Pass / Pass-with-warnings path

Entered only when **zero blocking findings** remain after Steps 1–7.

1. Mint `package_id = PKG-<CAPABILITY-SLUG>-<NNN>`.
2. Populate `traceability-package.yaml` from `templates/traceability-package.yaml`. Every field draws from:
   - upstream artefacts (spec / BRD / module / flows / programs / inventory / evidence manifest), or
   - this run's coverage tables, or
   - this run's `FIND-*` records.
3. Render `traceability-package.md` from `templates/traceability-package.md`. Prose summaries cite IDs only; no architecture, framework, or platform recommendations.
4. Render `coverage-audit.md` from `templates/coverage-audit.md` using the Step 6 tables.
5. Render `traceability-review.md` from `templates/traceability-review.md` with the gate checklist (one row per Step 1–7), findings grouped by severity, and the sign-off block.
6. Set `status`:
   - `pass` if zero blocking, warning, and info findings are present;
   - `pass_with_warnings` if any warning or info finding is present.
7. Record `review_sign_offs[]`:
   - spec approver (copied from `spec-review.md`)
   - BRD approver (copied from `brd-review.md`, if present)
   - packager validator (this skill + version)
   - packager SME approver (capability-owner SME, with name, role, ISO date, and `approval_scope: traceability-package`)
8. Write all four files atomically into `06_traceability_packages/<CAPABILITY-SLUG>/`. Do **not** write a fifth file.
9. Notify `legacy-modernization-orchestrator` (or the caller) that the package is ready. If `06_sdd_handoffs/<CAP>/` does not yet exist, suggest `legacy-brd-to-sdd-handoff` as the next skill; if it does, suggest `legacy-step-validator` for an independent step audit.

### 8b. Blocked path

Entered when **any** blocking finding is recorded by Steps 1–7.

1. Do **not** write `traceability-package.yaml`, `traceability-package.md`, or `coverage-audit.md`.
2. Write only:
   - `traceability-review.md` — gate checklist with every blocking row flagged, finding list grouped by severity, and required remediation per finding (with named upstream skill);
   - `blocking-findings.yaml` — machine-readable record matching `templates/blocking-findings.yaml`.
3. Set `status: blocked`.
4. For every blocking finding, set `next_routing.responsible_skill` and quote the exact remediation text from the rules table above.
5. Return control to the named upstream skill (`legacy-spec-writer`, `legacy-brd-writer`, `legacy-ibmi-evidence-intake`, `legacy-ibmi-inventory`, `legacy-ibmi-program-analyzer`, `legacy-ibmi-flow-analyzer`, `legacy-ibmi-module-analyzer`, or `legacy-brd-to-sdd-handoff`) with the exact remediation quoted from the finding. The skill is responsible for re-running the packager after the upstream artefact is fixed.

A blocked traceability package is a normal outcome, not an error. The audit's job is to fail loudly and early so forward SDLC never consumes a hidden gap.

---

## Output Status Decision Table

| Findings present | Final `status` | Display label |
| --- | --- | --- |
| only `pass`-level rows | `pass` | `pass` |
| `pass` + `BLOCKING-TBD-DEFERRED` and/or `NON-BLOCKING-TBD` only | `pass_with_warnings` | `pass_with_warnings` |
| `pass` + `ORPHAN-EVIDENCE` warning or SME-waived info | `pass_with_warnings` | `pass_with_warnings` |
| `pass` + `DEC-NO-RATIONALE` (warning) | `pass_with_warnings` | `pass_with_warnings` |
| `pass` + explicit SME-waived `AC-NOT-APPROVED` or `AC-VALIDATES-UNAPPROVED-BR` | `pass_with_warnings` | `pass_with_warnings` |
| any other warning without SME waiver | `blocked` | `blocked` |
| any blocking finding | `blocked` | `blocked` |

The skill must not invent a fourth status. Ambiguous cases default to `blocked`.

---

## Worked Examples

| Example | Step that fires | Finding | Final status | Display |
| --- | --- | --- | --- | --- |
| `examples/traceability-positive/` | none beyond pass | — | `pass` | `pass` |
| `examples/traceability-blocked-dangling-id/` | Step 3 | `BR-DANGLING-IN-AC` | `blocked` | `blocked` |
| `examples/traceability-warning-deferred-tbd/` | Step 7 | `BLOCKING-TBD-DEFERRED` | `pass_with_warnings` | `pass_with_warnings` |
