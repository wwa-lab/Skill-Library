<!--
Legacy Spec Factory
Copyright 2026 Leo L Zhang

Original author: Leo L Zhang
License: Apache License 2.0

Example: filled Step Contract block for an inventory step that can pass.
-->

# Step Contract — Inventory For Credit Check

- **step_id:** `STEP-CREDIT-CHECK-001`
- **step_name:** Inventory for Credit Check
- **skill:** `legacy-ibmi-inventory`
- **capability_slug:** `CREDIT-CHECK`
- **owner_role:** inventory runner
- **date:** 2026-05-14

## 1. INPUT

```yaml
prerequisite_artifacts:
  - path: evidence/redacted/source/ORDENTR.rpgle
    required_status: redacted
  - path: evidence/redacted/source/ORDSUBMIT.clle
    required_status: redacted
  - path: evidence/redacted/dds/CUSTPF.pf
    required_status: redacted
  - path: evidence/redacted/spool/credit-hold-report-001.txt
    required_status: redacted
prerequisite_gates:
  - Evidence Authorization Gate
evidence_scope:
  evidence_ids:
    - EV-CREDIT-CHECK-001
    - EV-CREDIT-CHECK-002
    - EV-CREDIT-CHECK-003
    - EV-CREDIT-CHECK-004
  object_ids: []
  authorization_summary:
    sensitivity_unknown: no
    source_path_verified: mixed
    redaction_required_unapproved: no
sme_required: yes
sme_owner: Credit Operations SME
assumptions_recorded:
  - Capability scope is limited to credit-check related objects in the supplied bundle.
out_of_scope:
  - card issuance
  - collections workflow
```

### Stop-on-INPUT decisions

| Condition | Outcome |
| --- | --- |
| Any prerequisite artifact missing or below status | `blocked` |
| Any prerequisite gate blocked | `blocked` |
| Any `sensitivity: unknown` in scope | `blocked` |
| Any evidence lacks source-path authorization or required redaction approval | `blocked` |
| `sme_required = yes` and `sme_owner` empty | `blocked` |
| `evidence_scope` empty for evidence-bound step | `blocked` |

No stop condition applies.

## 2. EXECUTION

```yaml
procedure_pointer: skills/legacy-ibmi-inventory/SKILL.md#workflow
inputs_to_outputs_mapping:
  - input: redacted source members
    output: 01_inventory/inventory.yaml.objects
  - input: DDS and spool samples
    output: 01_inventory/inventory.yaml.evidence
  - input: SME owner
    output: 01_inventory/inventory.yaml.sme_review
tools_allowed:
  - read_redacted_source
  - read_dds
  - read_redacted_spool
  - ask_sme
tools_forbidden:
  - read_unauthorized_evidence
  - invent_object_names
  - infer_business_rules
decision_points:
  - decision: classify missing referenced objects as coverage gaps or open questions
    alternatives:
      - coverage_gap
      - open_question
    recorded_as: 01_inventory/inventory.yaml.coverage_gaps
idempotency: idempotent
id_minting_policy:
  allowed_prefixes:
    - OBJ
    - EV
    - TBD
    - STEP
  reused_from_upstream: []
```

## 3. OUTPUT

```yaml
primary_artifacts:
  - path: 01_inventory/inventory.yaml
    template_or_schema: skills/legacy-ibmi-inventory/templates/inventory.yaml
    status_field: sme_review.decision
  - path: 01_inventory/object-map.md
    template_or_schema: skills/legacy-ibmi-inventory/references/output-contract.md
    status_field: n/a
  - path: 01_inventory/inventory-review-checklist.md
    template_or_schema: skills/legacy-ibmi-inventory/examples/redacted-customer-credit-check/inventory-review-checklist.md
    status_field: n/a
id_namespaces:
  - OBJ
  - EV
  - TBD
  - STEP
cross_references:
  - every object links to at least one EV-*
  - every relationship links to at least one EV-*
status_field:
  artifact: 01_inventory/inventory.yaml
  field: sme_review.decision
  allowed_values:
    - pending
    - approved
    - approved_with_non_blocking_tbd
    - blocked
non_outputs:
  - business rules
  - capability specs
  - Java code
human_readable_view: 01_inventory/object-map.md
```

## 4. VALIDATION

### 4a. Mechanical Validation

| Check | Pass? | Evidence / Tool |
| --- | --- | --- |
| Required files exist | yes | filesystem |
| Schema validates | n/a | inventory schema not yet formalized |
| ID prefixes match conventions | yes | `docs/id-conventions.md` |
| No dangling references | yes | all `evidence_ids[]` resolve |
| Evidence authorization resolved | yes | no `sensitivity: unknown`; source paths/redactions approved |
| Status fields in enum | yes | `sme_review.decision: approved` |
| Claims have evidence | yes | all objects and relationships link to `EV-*` |
| Forbidden tools not used | yes | no raw evidence read |
| ID minting policy respected | yes | only `OBJ-*`, `EV-*`, `TBD-*`, `STEP-*` |
| Non-outputs absent | yes | no `BR-*`, `spec.yaml`, or generated code |

### 4b. AI Semantic Review

| Check | Finding | Blocking? |
| --- | --- | --- |
| Claims match evidence | Object list matches supplied source, DDS, and spool evidence | no |
| Knowledge type matches claim shape | Inventory observations stay at object/evidence level | no |
| Evidence strength not overstated | Source listings marked `confirmed_from_code`; spool sample marked `observed_in_runtime` | no |
| No invented facts | No object not present in supplied evidence is listed | no |
| No scope creep | Scope remains credit-check objects only | no |
| TBDs explicit | Two SME questions carried as non-blocking TBDs | no |
| Contradictions surfaced | None found | no |

### 4c. SME / Human Approval

| Check | Required? | Approved By | Date | IDs Approved |
| --- | --- | --- | --- | --- |
| Object coverage approved | yes | Credit Operations SME | 2026-05-13 | OBJ-CREDIT-CHECK-001..009 |
| Inferred business rules approved | no | n/a | n/a | n/a |
| Modernization decisions approved | no | n/a | n/a | n/a |
| Behavior intentionality approved | no | n/a | n/a | n/a |
| TBD blocking/non-blocking decision | yes | Credit Operations SME | 2026-05-13 | TBD-CREDIT-CHECK-001..002 |
| Spec promotion to `approved` | no | n/a | n/a | n/a |
| Forward handoff approved | no | n/a | n/a | n/a |

## Compact Validation Result

```yaml
status: pass
step_id: STEP-CREDIT-CHECK-001
blocking_items: []
warnings: []
sme_decision: approved
downstream_next_step: legacy-ibmi-program-analyzer
remediation_step: none
```

## Unresolved Items Ledger

```yaml
unresolved_items:
  - id: TBD-CREDIT-CHECK-001
    category: sme_questions
    points_to:
      - 01_inventory/inventory.yaml:open_questions[0]
    resolver: sme
    blocks_current_step: no
    blocks_next_step: no
    notes: SME marked month-end override question non-blocking for program analysis.
  - id: TBD-CREDIT-CHECK-002
    category: sme_questions
    points_to:
      - 01_inventory/inventory.yaml:open_questions[1]
    resolver: sme
    blocks_current_step: no
    blocks_next_step: no
    notes: SME marked report activity question non-blocking for program analysis.
```
