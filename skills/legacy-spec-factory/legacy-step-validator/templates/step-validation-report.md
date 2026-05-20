<!--
Legacy Spec Factory
Copyright 2026 Leo L Zhang

Original author: Leo L Zhang
License: Apache License 2.0

Step Validation Report — produced by legacy-step-validator.
This template extends ../../legacy-step-contract/templates/step-validation-report.md
with the ten review dimensions.
-->

# Step Validation Report — <STEP-NAME>

## Header

- **report_path:** `06_quality/step-validation-report.md`
- **findings_path:** `06_quality/blocking-findings.yaml` (when status is not `pass`)
- **validator_skill:** `legacy-step-validator` v0.1.0
- **step_type:** `inventory | program | flow | module | spec | handoff`
- **step_id:** `STEP-<CAPABILITY-SLUG>-<NNN>`
- **package_path:** <directory or file reviewed>
- **executed_by:** <runner / agent / human>
- **executed_at:** <YYYY-MM-DD HH:MM ZZZ>
- **upstream_contract:** `../legacy-step-contract/references/step-contract.md`

## Compact Result

```yaml
status: <pass | pass_with_warnings | blocked>
step_id: STEP-<SLUG>-<NNN>
step_type: <inventory | program | flow | module | spec | handoff>
blocking_items: []
warnings: []
sme_decision: <approved | approved_with_non_blocking_tbd | pending | blocked | not_required>
downstream_next_step: <skill-name | doc-path | none>
remediation_step: <skill-name | doc-path | none>
input_readiness:
  score: <0-10>
  status: <blocked | minimum_pass | usable | strong>
  minimum_pass_met: <true | false>
  hard_blockers: []
  optional_missing: []
  quality_boosters_available: []
  quality_ceiling_reason:
report_path: 06_quality/step-validation-report.md
findings_path: 06_quality/blocking-findings.yaml | none
```

`pass` requires all three layers clean and SME approval recorded where
required. `pass_with_warnings` requires mechanical clean, only
non-blocking semantic findings, and any open `TBD-*` SME-marked
non-blocking. `blocked` covers any mechanical failure, any blocking
semantic finding, any missing-but-required SME approval, any redaction
issue, or any next-step gate failure.

## Pre-flight

| Check | Result | Evidence |
| --- | --- | --- |
| Evidence authorization complete |  |  |
| No raw production PII / financial detail outside redacted samples |  |  |
| Redaction record exists for every production-sourced `EV-*` |  |  |
| ID prefixes conform to `docs/id-conventions.md` |  |  |
| All cross-referenced IDs resolve |  |  |
| Knowledge type labels within allowed enum |  |  |
| Evidence strength labels within allowed enum |  |  |
| Input readiness score recorded with blockers/optional gaps/quality boosters |  |  |

If a redaction or sensitivity pre-flight row fails, status is `blocked` and
the validator stops. For other pre-flight failures, status is locked to
`blocked`; the validator may continue collecting advisory semantic and
SME-readiness findings when doing so does not expose unsafe data.

## 1. Mechanical Layer

| Check | Result | Evidence / Tool | Dimension |
| --- | --- | --- | --- |
|  |  |  |  |

Mechanical verdict: `pass` | `blocked`

## 2. AI Semantic Layer

| Check | Finding | Blocking? | Linked IDs | Dimension |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

Semantic verdict: `pass` | `pass_with_warnings` | `blocked`

## 3. SME Readiness Layer

This layer checks **readiness for SME review**, not SME approval
itself. The validator never approves on the SME's behalf.

| Check | Result | Recorded SME role / date / IDs | Dimension |
| --- | --- | --- | --- |
|  |  |  |  |

SME readiness verdict: `ready` | `not_ready` | `recorded_approval_present`

## Findings by Review Dimension

For each of the ten dimensions, list the findings that mapped to it.
Dimensions with zero findings are listed as `none`.

### 1. Input readiness

Record whether the step had the smallest safe input set, which inputs were
hard blockers, which missing inputs were harmless, and which extra inputs would
raise output quality.

| Finding ID | Severity | Layer | Points to | Resolver | Recommended action |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

### 2. Execution traceability

| Finding ID | Severity | Layer | Points to | Resolver | Recommended action |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

### 3. Output contract completeness

| Finding ID | Severity | Layer | Points to | Resolver | Recommended action |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

### 4. Evidence integrity

| Finding ID | Severity | Layer | Points to | Resolver | Recommended action |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

### 5. Knowledge taxonomy correctness

| Finding ID | Severity | Layer | Points to | Resolver | Recommended action |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

### 6. SME review readiness

| Finding ID | Severity | Layer | Points to | Resolver | Recommended action |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

### 7. Downstream handoff readiness

| Finding ID | Severity | Layer | Points to | Resolver | Recommended action |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

### 8. Open TBD handling

| Finding ID | Severity | Layer | Points to | Resolver | Recommended action |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

### 9. Contradiction / missing evidence detection

| Finding ID | Severity | Layer | Points to | Resolver | Recommended action |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

### 10. Redaction and sensitivity safety

| Finding ID | Severity | Layer | Points to | Resolver | Recommended action |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

## Unresolved Items Ledger

```yaml
unresolved_items:
  - id: TBD-<SLUG>-<NNN>
    category: missing_inputs | evidence_gaps | contradictory_evidence | sme_questions | downstream_handoff_blockers
    points_to: []
    resolver: source_owner | sme | architecture | reviewer | runner
    blocks_current_step: yes | no
    blocks_next_step: yes | no
    notes:
```

Categories come from
`../legacy-step-contract/references/step-contract.md`. One TBD = one
category. Do not split a single concern across categories.

## Handoff Note

- **Next step in chain:** <skill name | doc | gate>
- **What carries forward:** <artifacts and IDs the next step will consume>
- **Warnings carried forward:** <non-blocking warnings the next step must not silently drop>
- **Gate impact:** <which gate this result advances or blocks>

## Validator Self-Check

Confirm before emitting:

- [ ] Step type detected unambiguously
- [ ] Pre-flight executed before any other layer
- [ ] All ten review dimensions evaluated (each section present, even if `none`)
- [ ] Every finding carries dimension, layer, severity, pointers, resolver, recommended action
- [ ] Status is exactly one of `pass` / `pass_with_warnings` / `blocked`
- [ ] No business artifact produced
- [ ] No SME approval simulated
- [ ] No IBM i facts invented
- [ ] `06_quality/blocking-findings.yaml` written when status is not `pass`

## Revision History

| Revision | Date | Author | Change | New Status |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
