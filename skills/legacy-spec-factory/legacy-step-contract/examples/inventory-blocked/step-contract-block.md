<!--
Legacy Spec Factory
Copyright 2026 Leo L Zhang

Original author: Leo L Zhang
License: Apache License 2.0

Example: filled Step Contract block for an inventory step that exits as
`blocked` at the INPUT pre-flight because `sme_required: yes` but
`sme_owner` is empty. Sister of `../inventory-pass/step-contract-block.md`.
IDs, capability slug, and SME role are illustrative.
-->

# Step Contract — Inventory For Credit Check (Blocked, SME Owner Missing)

- **step_id:** `STEP-CREDIT-CHECK-002`
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
sme_owner: ""        # blocker: Credit Operations SME not yet assigned
assumptions_recorded:
  - Capability scope is limited to credit-check related objects in the supplied bundle.
  - Tier-1 source listings (WRKOBJ / DSPOBJD or source-member listings) are available.
out_of_scope:
  - card issuance
  - collections workflow
```

### Stop-on-INPUT decisions

| Condition | Outcome | Triggered? |
| --- | --- | --- |
| Any prerequisite artifact missing or below status | `blocked` | no |
| Any prerequisite gate blocked | `blocked` | no |
| Any `sensitivity: unknown` in scope | `blocked` | no |
| Any evidence lacks source-path authorization or required redaction approval | `blocked` | no |
| `sme_required = yes` and `sme_owner` empty | `blocked` | **yes** |
| `evidence_scope` empty for evidence-bound step | `blocked` | no |

**INPUT pre-flight verdict:** `blocked` — `sme_required: yes` but
`sme_owner` is empty. Per
`skills/legacy-step-contract/references/step-contract.md` line 192–194,
record the missing SME owner under `sme_questions` (not
`pass_with_warnings`, not `missing_inputs`).

The executing skill (`legacy-ibmi-inventory`) MUST NOT proceed to its
workflow until the blocker is resolved. The EXECUTION and OUTPUT sections
below describe the contract the step would honor on re-entry; they are not
a record of work performed.

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
execution_status: not_started   # blocked at INPUT pre-flight
```

## 3. OUTPUT

```yaml
primary_artifacts:
  - path: 01_inventory/inventory.yaml
    template_or_schema: skills/legacy-ibmi-inventory/templates/inventory.yaml
    status_field: sme_review.decision
    actually_produced: no       # blocked at INPUT
  - path: 01_inventory/object-map.md
    template_or_schema: skills/legacy-ibmi-inventory/references/output-contract.md
    status_field: n/a
    actually_produced: no
  - path: 01_inventory/inventory-review-checklist.md
    template_or_schema: skills/legacy-ibmi-inventory/examples/redacted-customer-credit-check/inventory-review-checklist.md
    status_field: n/a
    actually_produced: no
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
  current_value: blocked        # no SME means no possible promotion
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
| INPUT pre-flight: `sme_owner` present when `sme_required = yes` | **fail** | this contract block, INPUT section |
| Required files exist | n/a | step did not execute |
| Schema validates | n/a | step did not execute |
| ID prefixes match conventions | n/a | step did not execute |
| No dangling references | n/a | step did not execute |
| Evidence authorization resolved | yes | all evidence authorized or redacted |
| Status fields in enum | n/a | step did not execute |
| Claims have evidence | n/a | step did not execute |
| Forbidden tools not used | n/a | step did not execute |
| ID minting policy respected | n/a | step did not execute |
| Non-outputs absent | n/a | step did not execute |

**Mechanical verdict:** `blocked` — INPUT pre-flight failure short-circuits
every downstream mechanical check. Re-run mechanical validation only after
the blocker is resolved.

### 4b. AI Semantic Review

| Check | Finding | Blocking? |
| --- | --- | --- |
| Claims match evidence | not applicable; no claims produced | n/a |
| Knowledge type matches claim shape | not applicable; no claims produced | n/a |
| Evidence strength not overstated | not applicable; no claims produced | n/a |
| No invented facts | not applicable; no claims produced | n/a |
| No scope creep | not applicable; no claims produced | n/a |
| TBDs explicit | yes — missing SME is explicitly tracked, not hidden | no |
| Contradictions surfaced | not applicable; no claims produced | n/a |

**Semantic verdict:** `not_evaluated` — AI semantic review is meaningful
only against produced artifacts.

### 4c. SME / Human Approval

| Check | Required? | Approved By | Date | IDs Approved | Status |
| --- | --- | --- | --- | --- | --- |
| Object coverage approved | yes | unassigned | n/a | n/a | **blocked** |
| Inferred business rules approved | no | n/a | n/a | n/a | not_required |
| Modernization decisions approved | no | n/a | n/a | n/a | not_required |
| Behavior intentionality approved | no | n/a | n/a | n/a | not_required |
| TBD blocking/non-blocking decision | yes | unassigned | n/a | n/a | **blocked** |
| Spec promotion to `approved` | no | n/a | n/a | n/a | not_required |
| Forward handoff approved | no | n/a | n/a | n/a | not_required |

**SME verdict:** `blocked` — `sme_required: yes` but no Credit Operations
SME has been assigned. SME absence at a step that requires SME is itself a
blocker (per `references/step-contract.md` line 192).

## Compact Validation Result

```yaml
status: blocked
step_id: STEP-CREDIT-CHECK-002
blocking_items:
  - TBD-CREDIT-CHECK-010
warnings: []
sme_decision: pending
downstream_next_step: none
remediation_step: legacy-ibmi-inventory
```

`remediation_step: legacy-ibmi-inventory` means: once the capability owner
assigns a Credit Operations SME and records the role in `sme_owner`,
re-enter the inventory step's INPUT pre-flight. Mechanical, semantic, and
SME layers can then be evaluated against produced artifacts.

`downstream_next_step` stays `none` while the package is blocked.
`legacy-ibmi-program-analyzer` MUST NOT be invoked against this capability
until this step exits `blocked`.

## Unresolved Items Ledger

```yaml
unresolved_items:
  - id: TBD-CREDIT-CHECK-010
    category: sme_questions
    points_to:
      - skills/legacy-step-contract/examples/inventory-blocked/step-contract-block.md:INPUT.sme_owner
      - 01_inventory/inventory.yaml:sme_review.sme_owner
    resolver: sme
    blocks_current_step: yes
    blocks_next_step: yes
    notes: >-
      Credit Operations SME owner has not been assigned. Per
      references/step-contract.md line 192, SME absence at a step that
      requires SME is recorded under `sme_questions` (not
      `missing_inputs`, not a `pass_with_warnings` carry-forward). Resolver
      is the capability owner identifying the right Credit Operations SME
      and recording the role in `sme_owner`; once recorded, the inventory
      runner re-enters INPUT pre-flight.
```
