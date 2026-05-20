<!--
Legacy Spec Factory
Copyright 2026 Leo L Zhang

Original author: Leo L Zhang
License: Apache License 2.0

Step Contract Block — fill one per step instance.
See ../references/step-contract.md for field-level rules.
-->

# Step Contract — <STEP-NAME>

- **step_id:** `STEP-<CAPABILITY-SLUG>-<NNN>`
- **step_name:** <human-readable name>
- **skill:** <canonical skill name or doc path>
- **capability_slug:** <CAPABILITY-SLUG>
- **owner_role:** <runner / SME / orchestrator>
- **date:** <YYYY-MM-DD>

## 1. INPUT

```yaml
prerequisite_artifacts:
  - path:
    required_status:
prerequisite_gates:
  - <Evidence Authorization Gate | Inventory Completeness Gate | Evidence Approval Gate | Forward Handoff Gate>
evidence_scope:
  evidence_ids: []
  object_ids: []
  authorization_summary:
    sensitivity_unknown: <yes | no>
    source_path_verified: <yes | no | mixed>
    redaction_required_unapproved: <yes | no>
input_readiness:
  score: <0-10>
  status: <blocked | minimum_pass | usable | strong>
  minimum_pass_met: <true | false>
  hard_blockers: []
  optional_missing: []
  quality_boosters_available: []
  quality_ceiling_reason:
sme_required: <yes | recommended | no>
sme_owner: <role or name when required>
assumptions_recorded:
  -
out_of_scope:
  -
```

### Stop-on-INPUT decisions

| Condition | Outcome |
| --- | --- |
| Any prerequisite artifact missing or below status | `blocked` |
| Any prerequisite gate blocked | `blocked` |
| Any `sensitivity: unknown` in scope | `blocked` |
| Any evidence lacks source-path authorization or required redaction approval | `blocked` |
| `input_readiness.status = blocked` or `minimum_pass_met = false` | `blocked` |
| `sme_required = yes` and `sme_owner` empty | `blocked` |
| `evidence_scope` empty for evidence-bound step | `blocked` |

If any row above applies, do not execute. Invoke `legacy-step-validator` (or
the equivalent manual validator workflow) to emit a Step Validation Report with
status `blocked` and the unresolved items listed under the correct category.

## 2. EXECUTION

```yaml
procedure_pointer: <SKILL.md section or references/*.md path>
inputs_to_outputs_mapping:
  - input: <input field or artifact>
    output: <output field or artifact>
tools_allowed:
  -
tools_forbidden:
  -
decision_points:
  - decision: <what is being chosen>
    alternatives: []
    recorded_as: <artifact field where the choice is captured>
idempotency: <idempotent | non_idempotent | idempotent_with_caveat>
id_minting_policy:
  allowed_prefixes:
    -
  reused_from_upstream:
    -
```

## 3. OUTPUT

```yaml
primary_artifacts:
  - path:
    template_or_schema:
    status_field:
id_namespaces:
  -
cross_references:
  -
status_field:
  artifact:
  field:
  allowed_values: []
non_outputs:
  -
human_readable_view:
```

## 4. VALIDATION

### 4a. Mechanical Validation

| Check | Pass? (yes / no / n/a) | Evidence / Tool |
| --- | --- | --- |
| Required files exist |  |  |
| Schema validates |  |  |
| ID prefixes match conventions |  |  |
| No dangling references |  |  |
| Evidence authorization resolved |  |  |
| Input readiness scored and minimum pass met |  |  |
| Status fields in enum |  |  |
| Claims have evidence |  |  |
| Forbidden tools not used |  |  |
| ID minting policy respected |  |  |
| Non-outputs absent |  |  |

If any check above is `no`, status is `blocked`. If redaction is safe, the
validator may still collect advisory semantic and SME-readiness findings, but
later layers cannot change the blocked status.

### 4b. AI Semantic Review

| Check | Finding | Blocking? |
| --- | --- | --- |
| Claims match evidence |  |  |
| Knowledge type matches claim shape |  |  |
| Evidence strength not overstated |  |  |
| No invented facts |  |  |
| No scope creep |  |  |
| TBDs explicit |  |  |
| Contradictions surfaced |  |  |

Default unclear findings to blocking; the next step pays for false negatives.

### 4c. SME / Human Approval

| Check | Required? | Approved By | Date | IDs Approved |
| --- | --- | --- | --- | --- |
| Object coverage approved |  |  |  |  |
| Inferred business rules approved |  |  |  |  |
| Modernization decisions approved |  |  |  |  |
| Behavior intentionality approved |  |  |  |  |
| TBD blocking/non-blocking decision |  |  |  |  |
| Spec promotion to `approved` |  |  |  |  |
| Forward handoff approved |  |  |  |  |

SME absence at a step that requires SME is itself a blocker. Surface it
under `sme_questions`.

## Compact Validation Result

```yaml
status: <pass | pass_with_warnings | blocked>
step_id: STEP-<SLUG>-<NNN>
blocking_items: []
warnings: []
sme_decision: <approved | approved_with_non_blocking_tbd | pending | blocked | not_required>
downstream_next_step: <skill-name | doc-path | none>
remediation_step: <skill-name | doc-path | none>
```

## Unresolved Items Ledger

```yaml
unresolved_items:
  - id: TBD-<SLUG>-<NNN>
    category: <missing_inputs | evidence_gaps | contradictory_evidence | sme_questions | downstream_handoff_blockers>
    points_to: []
    resolver: <source_owner | sme | architecture | reviewer | runner>
    blocks_current_step: <yes | no>
    blocks_next_step: <yes | no>
    notes:
```

One TBD = one category. Do not split a single concern across categories.
