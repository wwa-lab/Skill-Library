<!--
Legacy Spec Factory
Copyright 2026 Leo L Zhang

Original author: Leo L Zhang
License: Apache License 2.0
-->

# Output Contract — `traceability-package.yaml` and Sibling Files

This document is the field-level specification for the four output files produced by `legacy-traceability-packager`. `SKILL.md` cites this file; do not duplicate field definitions in `SKILL.md`.

## File Set

| Outcome | Files Written | Files NOT Written |
| --- | --- | --- |
| `pass` | `traceability-package.yaml`, `traceability-package.md`, `coverage-audit.md`, `traceability-review.md` | `blocking-findings.yaml` |
| `pass_with_warnings` | same four | `blocking-findings.yaml` |
| `blocked` | `traceability-review.md`, `blocking-findings.yaml` | the three package files |

The output directory is **always** `06_traceability_packages/<CAPABILITY-SLUG>/`. The skill must not write into `05_specs/`, `05_brds/`, `06_sdd_handoffs/`, or any upstream analysis directory.

## `traceability-package.yaml`

### Top-Level Keys

| Key | Required? | Source | Notes |
| --- | --- | --- | --- |
| `schema_version` | yes | this skill | semver string of the contract; current is `"0.1"` |
| `package_id` | yes | this skill | `PKG-<CAPABILITY-SLUG>-<NNN>`; stable across reruns of the same package instance |
| `package_date` | yes | this skill | ISO 8601 UTC timestamp of the audit run |
| `packager` | yes | this skill | `"legacy-traceability-packager v<version>"` |
| `capability` | yes | `spec.yaml.capability` | copied verbatim — `id`, `name`, `slug`, `owner` |
| `status` | yes | this skill | one of `pass`, `pass_with_warnings`, `blocked` |
| `source_artifacts` | yes | upstream | path + ID + status for every artefact consulted |
| `id_inventory` | yes | this run | counts and full ID lists per prefix |
| `evidence_coverage` | yes | this run | per-`EV-*` reverse index |
| `behavior_coverage` | yes | this run | per-`BEH-*` reverse index |
| `business_rule_coverage` | yes | this run | per-`BR-*` closure record |
| `acceptance_criteria_coverage` | yes | this run | per-`AC-*` validation record |
| `test_coverage` | yes (may be empty) | this run | per-`TC-*` validation record |
| `decision_coverage` | yes (may be empty) | this run | per-`DEC-*` rationale record |
| `open_questions` | yes | spec / BRD | every `TBD-*` carried forward verbatim |
| `findings` | yes | this run | `{ blocking[], warnings[], info[] }`, each entry minted as `FIND-*` |
| `review_sign_offs` | yes | upstream + this run | spec / BRD approvers carried forward; packager + SME sign-offs added |
| `next_routing` | yes | this run | per-finding route to the upstream owning skill |
| `assumptions` | optional | spec / BRD | only assumptions already recorded upstream; this skill never mints |
| `metrics` | optional | this run | descriptive aggregates derived from the coverage tables |

### `source_artifacts`

Required rows when present:

```yaml
source_artifacts:
  spec:
    id: SPEC-<SLUG>-<NNN>
    path: 05_specs/<SLUG>/spec.yaml
    status: approved
    approved_by: { name, role, date }
  brd:                                  # optional
    id: BRD-<SLUG>-<NNN>
    path: 05_brds/<SLUG>/brd.md
    status: approved
    approved_by: { name, role, date }
  module:
    id: MODULE-<SLUG>-<NNN>
    path: 04_modules/<SLUG>/
    status: approved
  flows: [ { id, path, status } ]
  programs: [ { id, path, status } ]
  inventory:
    path: 01_inventory/inventory.yaml
    sme_review_decision: approved
  evidence_manifest:
    path: evidence/manifest.yaml
    package_state: approved_for_inventory
    intake_decision:
      downstream_inventory_allowed: true
  sdd_handoff:                          # optional cross-check
    id: HANDOFF-<SLUG>-<DATE>
    path: 06_sdd_handoffs/<SLUG>/sdd-handoff.yaml
    status: approved | approved_with_non_blocking_tbd | blocked
```

Every path must be relative to the repository root. Statuses must use each artefact's own enum (`spec.yaml.status`, `inventory.sme_review.decision`, etc.).

### `id_inventory`

```yaml
id_inventory:
  totals:
    CAP: 1
    MODULE: 1
    FLOW: 3
    BR: 5
    BEH: 8
    EV: 12
    AC: 6
    DEC: 4
    TC: 3
    TBD: 1
    # … one row per prefix observed
  ids:
    BR: [ BR-<SLUG>-001, … ]
    BEH: [ … ]
    EV: [ … ]
    # one list per prefix
  sources:
    BR-<SLUG>-001:
      defined_in: 05_specs/<SLUG>/spec.yaml
    EV-<SLUG>-001:
      defined_in: evidence/manifest.yaml
      also_referenced_in: [ 05_specs/<SLUG>/spec.yaml, 05_brds/<SLUG>/brd.md ]
```

Every ID must conform to `docs/id-conventions.md`. The packager must not invent IDs.

### `evidence_coverage`

```yaml
evidence_coverage:
  - evidence_id: EV-<SLUG>-001
    sensitivity: public            # public | internal | confidential | unknown
    redaction_status: not_required
    redacted_filename: 02_programs/<OBJ>/program-analysis.md  # approved analysis path
    source_path_verified: true
    redaction_required: false
    sme_required: false
    sme_approval: false
    referenced_by:
      behaviors: [ BEH-<SLUG>-001 ]
      business_rules: [ BR-<SLUG>-001 ]
      decisions: []
      process_steps: []
      acceptance_criteria: [ AC-<SLUG>-001 ]
      tests: [ TC-<SLUG>-001 ]
      data_model_fields: []
      inputs_outputs_exceptions: []
    is_orphan: false
    orphan_waiver:                # only if SME explicitly waived
      waived_by: { name, role, date }
      reason: <quoted from spec-review.md>
```

`is_orphan: true` requires either an explicit waiver block or a corresponding `ORPHAN-EVIDENCE` finding.

### `business_rule_coverage`

```yaml
business_rule_coverage:
  - rule_id: BR-<SLUG>-001
    review_status: approved        # mirrors spec.yaml.business_rules[].review_status
    knowledge_type: inferred_business_rule
    evidence_ids: [ EV-<SLUG>-001, … ]
    behavior_ids: [ BEH-<SLUG>-001, … ]
    acceptance_criteria_ids: [ AC-<SLUG>-001, AC-<SLUG>-002 ]
    test_ids: [ TC-<SLUG>-001 ]    # optional
    closure_status: closed         # closed | open | retired
    findings: [ ]                  # FIND-* IDs raised against this rule
```

`closure_status: closed` requires `evidence_ids`, `behavior_ids`, and `acceptance_criteria_ids` all non-empty for an approved rule.

### `acceptance_criteria_coverage`

```yaml
acceptance_criteria_coverage:
  - ac_id: AC-<SLUG>-001
    validates: [ BR-<SLUG>-001 ]
    review_status: approved
    tested_by: [ TC-<SLUG>-001, TC-<SLUG>-002 ]
    waiver:                       # only if SME explicitly waived a non-approved state
      waived_by: { name, role, date }
      reason: <quoted from spec-review.md>
    findings: [ ]
```

### `test_coverage`

```yaml
test_coverage:
  - test_id: TC-<SLUG>-001
    type: golden_master           # golden_master | unit | integration | acceptance
    validates: [ AC-<SLUG>-001, AC-<SLUG>-002 ]
    sample_data_evidence_id: EV-<SLUG>-009
    golden_master_enabled: true
    findings: [ ]
```

If `golden_master_enabled: true`, `sample_data_evidence_id` must resolve to a real `EV-*` in the manifest.

### `decision_coverage`

```yaml
decision_coverage:
  - decision_id: DEC-<SLUG>-001
    review_status: approved
    cites_rules: [ BR-<SLUG>-001 ]
    cites_behaviors: [ BEH-<SLUG>-002 ]
    cites_constraints: [ "PCI DSS 3.4" ]
    findings: [ ]                 # DEC-NO-RATIONALE raised here if all three are empty
```

### `open_questions`

```yaml
open_questions:
  - id: TBD-<SLUG>-001
    question: <verbatim from spec.yaml or brd.md>
    blocking: false                  # boolean from upstream
    resolution: <verbatim>
    resolver: <SME name from upstream roster>
    planned_resolution_date: 2026-07-31
    deferral_recorded_in: 05_specs/<SLUG>/spec-review.md#sme-decisions
    category: sme_questions          # mirrors brd-writer category if BRD supplied one
    related_ids: [ … ]
    next_routing:
      responsible_skill: legacy-spec-writer
      capability_owner: <SME name>
```

The packager never rewrites the `question` text. It never demotes a `blocking: true` TBD to `blocking: false`. Status decisions live in `findings`, not in this field.

### `findings`

```yaml
findings:
  blocking:
    - find_id: FIND-<SLUG>-001
      rule: BR-DANGLING-IN-AC
      severity: blocking
      step: 3
      points_to:
        - 05_specs/<SLUG>/spec.yaml#acceptance_criteria[3]
        - AC-<SLUG>-004
        - BR-<SLUG>-007         # does not exist in business_rules[]
      detail: AC-<SLUG>-004 validates BR-<SLUG>-007 but BR-<SLUG>-007 is not defined in spec.yaml.business_rules[].
      required_remediation:
        responsible_skill: legacy-spec-writer
        permitted_actions:
          - Add BR-<SLUG>-007 to business_rules[] with evidence + behavior links, then re-run packager.
          - Update AC-<SLUG>-004 to validate an existing approved BR, then re-run packager.
        forbidden_action: legacy-traceability-packager MUST NOT mint BR-<SLUG>-007 or rewrite AC-<SLUG>-004.
  warnings: [ … ]
  info: [ … ]
```

Every finding row has a `find_id` minted as `FIND-<CAPABILITY-SLUG>-<NNN>` and a `rule` from the catalog below.

### Finding Catalog

#### Blocking

| Rule | Step | Description |
| --- | --- | --- |
| `SPEC-MISSING` | 1 | `spec.yaml` not found |
| `SPEC-NOT-APPROVED` | 1 | `spec.yaml.status` below `approved` and no `blocked_audit` override |
| `BRD-NOT-APPROVED` | 1 | BRD referenced but below `approved` |
| `UPSTREAM-NOT-APPROVED` | 1 | required inventory / program / flow / module below `approved_with_non_blocking_tbd` |
| `EVIDENCE-PACKAGE-NOT-APPROVED` | 1 | manifest `package_state` ≠ `approved_for_inventory` |
| `ID-FORMAT-INVALID` | 2 | an ID does not conform to `docs/id-conventions.md` |
| `EV-DANGLING-IN-BR` | 3 | `business_rules[].evidence_ids[]` references a missing `EV-*` |
| `BEH-DANGLING-IN-BR` | 3 | `business_rules[].linked_behaviors[]` references a missing `BEH-*` |
| `AC-DANGLING-IN-BR` | 3 | `business_rules[].acceptance_criteria_ids[]` references a missing `AC-*` |
| `BR-DANGLING-IN-AC` | 3 | `acceptance_criteria[].validates[]` references a missing `BR-*` |
| `EV-DANGLING-IN-BEH` | 3 | behavior references missing `EV-*` |
| `EV-DANGLING-IN-DEC` | 3 | decision references missing `EV-*` |
| `OBJ-DANGLING-IN-DATA-MODEL` | 3 | `data_model.entities[].legacy_sources[]` references missing `OBJ-*` |
| `EV-DANGLING-IN-DATA-MODEL` | 3 | data-model field references missing `EV-*` |
| `EV-DANGLING-IN-STEP` | 3 | `process_flow.steps[].evidence_ids[]` references missing `EV-*` |
| `EV-DANGLING-IN-IO` | 3 | inputs / outputs / exceptions reference missing `EV-*` |
| `TC-DANGLING-VALIDATES` | 3 | `tests[].validates[]` references missing `AC-*` or `BR-*` |
| `EV-DANGLING-IN-TC` | 3 | `tests[].sample_data_ref` is an `EV-*` that does not exist |
| `TRACE-DANGLING-REF` | 3 | `traceability[]` rows reference IDs that do not exist |
| `HANDOFF-ID-MISMATCH` | 3 | pre-existing `sdd-handoff.yaml` carries a `BR-*` / `AC-*` / `EV-*` whose wording differs from the spec |
| `EVIDENCE-MANIFEST-MISS` | 4 | spec / BRD references an `EV-*` absent from manifest |
| `EVIDENCE-SENSITIVITY-UNKNOWN` | 4 | manifest `sensitivity: unknown` |
| `EVIDENCE-AWAITING-REDACTION` | 4 | manifest marks `redaction_required: true` but redaction is not `approved` |
| `EVIDENCE-SOURCE-NOT-AUTHORIZED` | 4 | manifest marks `redaction_required: false` but `source_path_verified` is not `true` |
| `EVIDENCE-APPROVED-PATH-MISSING` | 4 | manifest missing `redacted_filename` / approved analysis path |
| `EVIDENCE-SME-APPROVAL-MISSING` | 4 | manifest marks `sme_required: true` but `sme_approval` is not `true` |
| `BR-NO-EVIDENCE` | 5 | approved `BR-*` with empty `evidence_ids[]` |
| `BR-NO-BEHAVIOR` | 5 | approved `BR-*` with empty `linked_behaviors[]` |
| `BR-MISSING-AC` | 5 | approved `BR-*` with no linked `AC-*` |
| `BR-RETIRED-BUT-LINKED` | 5 | retired / rejected `BR-*` still referenced by an `AC-*` |
| `AC-NO-RULE` | 5 | `AC-*` with empty or unresolved `validates[]` |
| `AC-VALIDATES-UNAPPROVED-BR` | 5 | `AC-*` validates a non-approved `BR-*` (warning only if SME-waived) |
| `AC-NOT-APPROVED` | 5 | linked `AC-*` not `approved` (warning only if SME-waived) |
| `ORPHAN-EVIDENCE-IN-CLOSURE-PACKAGE` | 6 | orphan `EV-*` where spec / BRD claims full evidence closure |
| `COVERAGE-DATA-MISSING` | 6 | a coverage row would require new content not in upstream artefacts |
| `BLOCKING-TBD-UNRESOLVED` | 7 | blocking TBD without satisfied deferral predicate |

#### Warnings

| Rule | Step | Description |
| --- | --- | --- |
| `ORPHAN-EVIDENCE` | 6 | `EV-*` referenced by nothing; not a closure claim |
| `DEC-NO-RATIONALE` | 3 / 5 | `DEC-*` whose rationale cites no `BR-*`, `BEH-*`, or constraint |
| `BLOCKING-TBD-DEFERRED` | 7 | blocking TBD with all four deferral fields satisfied + `deferral_recorded_in` pointer |
| `AC-NOT-APPROVED` (SME-waived) | 5 | warning version when `spec-review.md` records a named waiver |
| `AC-VALIDATES-UNAPPROVED-BR` (SME-waived) | 5 | warning version when `spec-review.md` records a named waiver |
| `TBD-DANGLING-REF` | 3 | `TBD-*.related_ids[]` references a missing ID (warning unless the TBD is itself blocking) |

#### Info

| Rule | Step | Description |
| --- | --- | --- |
| `NON-BLOCKING-TBD` | 7 | `TBD-*` with `blocking: false`; carry forward |
| `BR-PENDING-SME-REVIEW` | 5 | `BR-*` with `review_status` other than `approved` / `rejected` / `retired` |
| `DEC-NOT-APPROVED` | 5 | `DEC-*` not yet approved (architecture / product authority owns this) |
| `HANDOFF-PREVIOUSLY-BLOCKED` | 1 | pre-existing handoff is blocked; recorded for cross-reference |
| `SME-OWNERSHIP-MISMATCH` | 1 | BRD owner ≠ spec owner; recorded only |
| `ORPHAN-EVIDENCE` (SME-waived) | 6 | orphan evidence explicitly waived by SME; still prevents a clean `pass` |

### `review_sign_offs`

```yaml
review_sign_offs:
  - approval_scope: spec
    name: <from spec-review.md>
    role: <from spec-review.md>
    date: <ISO from spec-review.md>
    source: 05_specs/<SLUG>/spec-review.md
    status: approved
  - approval_scope: brd            # optional
    name: <from brd-review.md>
    role: <from brd-review.md>
    date: <ISO from brd-review.md>
    source: 05_brds/<SLUG>/brd-review.md
    status: approved
  - approval_scope: traceability-package
    name: <capability-owner SME>
    role: <SME role>
    date: <ISO>
    source: 06_traceability_packages/<SLUG>/traceability-review.md
    status: approved | approved_with_non_blocking_tbd
  - approval_scope: packager-validator
    name: legacy-traceability-packager
    role: automated validator
    date: <package_date>
    source: this run
    status: validated
```

`status: approved` for `traceability-package` requires the package's `status` to be `pass`. `approved_with_non_blocking_tbd` is the corresponding sign-off shape for `pass_with_warnings`. A `blocked` package does not record a `traceability-package` sign-off.

### `next_routing`

```yaml
next_routing:
  primary_next_skill: legacy-brd-to-sdd-handoff   # or none / blocked-route
  rationale: <one short sentence>
  per_finding:
    - find_id: FIND-<SLUG>-001
      responsible_skill: legacy-spec-writer
      capability_owner: <SME>
      re_run_packager_after: true
```

When `status: pass`, `primary_next_skill` is typically `legacy-brd-to-sdd-handoff` (if the handoff is not yet packaged) or `none`. When `status: pass_with_warnings`, `primary_next_skill` may be `legacy-brd-to-sdd-handoff` only if every warning has been explicitly accepted by the SME. When `status: blocked`, `primary_next_skill` must name the owning upstream skill.

## `blocking-findings.yaml`

Written **only** on `blocked`. Mirrors the structure used by `legacy-step-validator` and `legacy-brd-to-sdd-handoff` so the orchestrator can ingest all three identically.

Required top-level fields:

```yaml
schema_version: "0.1"
package_id: PKG-<SLUG>-<NNN>
attempt_number: <NN>
attempt_date: <ISO>
packager: "legacy-traceability-packager v<version>"

capability: { id, name, slug, owner }
status: blocked

source_artifacts: { … }                  # same shape as in traceability-package.yaml

gate_results:
  intake_resolved: pass | FAIL | not_evaluated
  id_inventory_clean: pass | FAIL | not_evaluated
  cross_reference_walk: pass | FAIL | not_evaluated
  evidence_sensitivity: pass | FAIL | not_evaluated
  business_rule_closure: pass | FAIL | not_evaluated
  coverage_tables: pass | FAIL | not_evaluated
  tbd_carry_forward: pass | FAIL | not_evaluated
  package_assembly: not_evaluated

findings:
  blocking: [ … ]                        # full FIND-* records as above
  warnings: [ … ]
  info: [ … ]

package_written: false
files_written:
  - 06_traceability_packages/<SLUG>/traceability-review.md
  - 06_traceability_packages/<SLUG>/blocking-findings.yaml
files_not_written:
  - 06_traceability_packages/<SLUG>/traceability-package.yaml
  - 06_traceability_packages/<SLUG>/traceability-package.md
  - 06_traceability_packages/<SLUG>/coverage-audit.md

next_routing:
  primary_next_skill: <upstream skill>
  rationale: <quoted from the first blocking finding>
  per_finding: [ … ]                     # same shape as in traceability-package.yaml
```

The `files_written` and `files_not_written` lists are part of the contract: orchestrators check them to confirm the gate honoured its block-by-default discipline.

## `traceability-package.md` (Human Rendering)

The markdown file is a deterministic rendering of the YAML. Required sections:

1. Header — capability, package ID, date, packager, status, sign-offs.
2. Source artefacts — same paths and statuses as `source_artifacts`.
3. ID inventory summary — totals table.
4. Evidence walk — one section per `EV-*` with referenced-by list.
5. Business rule walk — one section per `BR-*` with EV / BEH / AC / TC links and closure status.
6. AC walk — table of `AC-*` → `BR-*` → `TC-*` with review status.
7. Decision walk — `DEC-*` → cited `BR-*` / `BEH-*` / constraint.
8. TBD ledger — every `TBD-*` carried forward verbatim.
9. Findings — grouped by severity, citing `FIND-*` IDs.
10. Next routing — verbatim from `next_routing`.

No prose may introduce content absent from the YAML.

## `coverage-audit.md`

Tabular rendering of the six coverage tables (EV, BEH, BR, AC, TC, DEC). One markdown table per coverage type. Includes the four metrics from Step 6 in a summary block at the top.

## `traceability-review.md`

Mirrors `legacy-brd-to-sdd-handoff/templates/handoff-review.md` in shape:

- gate checklist (one box per workflow Step 1–7);
- findings grouped by severity;
- carried-forward items (TBDs, waivers);
- sign-off block (packager + spec SME + BRD SME + capability-owner SME);
- a clear note explaining why this is **not** an SDD handoff and naming `legacy-brd-to-sdd-handoff` as the next gate.

## Anti-Field Drift Rules

- the skill must not add a field to `traceability-package.yaml` that is not listed in this document;
- the skill must not extend the finding catalog at runtime — new rules are added by editing this file;
- if downstream consumers ask for a new field, the canonical source under `skills/legacy-traceability-packager/` is updated first, then synced via `scripts/sync-skills.sh`.
