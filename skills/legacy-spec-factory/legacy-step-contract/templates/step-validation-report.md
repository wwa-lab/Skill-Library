<!--
Legacy Spec Factory
Copyright 2026 Leo L Zhang

Original author: Leo L Zhang
License: Apache License 2.0

Step Validation Report template — filled reports are emitted by
legacy-step-validator under 06_quality/ during real validation runs.
See ../references/step-contract.md for the validation layer rules.
-->

# Step Validation Report — <STEP-NAME>

## Header

- **step_id:** `STEP-<CAPABILITY-SLUG>-<NNN>`
- **skill:** <canonical skill name>
- **capability_slug:** <CAPABILITY-SLUG>
- **executed_by:** <runner / agent / human>
- **executed_at:** <YYYY-MM-DD HH:MM ZZZ>
- **contract_block:** <path to the corresponding Step Contract block>
- **artifacts_produced:**
  -

## Compact Validation Result

```yaml
status: <pass | pass_with_warnings | blocked>
step_id: STEP-<SLUG>-<NNN>
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
```

`pass` requires all three validation layers to be clean. `pass_with_warnings`
requires mechanical clean, only non-blocking semantic findings, and any open
`TBD-*` marked non-blocking by SME. `blocked` covers any mechanical failure,
any blocking semantic finding, or any missing-but-required SME approval.

## 1. Mechanical Validation

| Check | Result | Evidence / Tool | Note |
| --- | --- | --- | --- |
| Required files exist |  |  |  |
| Schema validates |  |  |  |
| ID prefixes match `docs/id-conventions.md` |  |  |  |
| No dangling references |  |  |  |
| Evidence authorization resolved |  |  |  |
| Input readiness scored and minimum pass met |  |  |  |
| Status fields in enum |  |  |  |
| Every claim has linked evidence |  |  |  |
| Forbidden tools not used |  |  |  |
| ID minting policy respected |  |  |  |
| Non-outputs absent |  |  |  |

**Mechanical verdict:** `pass` | `blocked`

If `blocked`, list failing check IDs. When redaction is safe, later semantic
and SME-readiness sections may still collect advisory findings, but they
cannot change the blocked status.

## 2. AI Semantic Review

| Check | Finding | Blocking? | Linked IDs |
| --- | --- | --- | --- |
| Claims match evidence |  |  |  |
| Knowledge type matches claim shape |  |  |  |
| Evidence strength not overstated |  |  |  |
| No invented facts |  |  |  |
| No scope creep |  |  |  |
| TBDs explicit |  |  |  |
| Contradictions surfaced |  |  |  |

**Semantic verdict:** `pass` | `pass_with_warnings` | `blocked`

When uncertain whether a finding is blocking, default to blocking.

## 3. SME / Human Approval

| Check | Required? | Approved By | Date | IDs Approved | Status |
| --- | --- | --- | --- | --- | --- |
| Object coverage approved |  |  |  |  |  |
| Inferred business rules approved |  |  |  |  |  |
| Modernization decisions approved |  |  |  |  |  |
| Behavior intentionality approved |  |  |  |  |  |
| TBD blocking/non-blocking decision |  |  |  |  |  |
| Spec promotion to `approved` |  |  |  |  |  |
| Forward handoff approved |  |  |  |  |  |

**SME verdict:** `approved` | `approved_with_non_blocking_tbd` | `pending` |
`blocked` | `not_required`

If SME is required for this step and `sme_owner` is absent or has not signed
off, the verdict is `blocked`. Surface it under `sme_questions` in the
unresolved items ledger.

## 4. Unresolved Items Ledger

```yaml
unresolved_items:
  - id: TBD-<SLUG>-<NNN>
    category: missing_inputs
    points_to: []
    resolver: source_owner | sme | architecture | reviewer | runner
    blocks_current_step: yes | no
    blocks_next_step: yes | no
    notes:
  - id: TBD-<SLUG>-<NNN>
    category: evidence_gaps
    points_to: []
    resolver:
    blocks_current_step:
    blocks_next_step:
    notes:
  - id: TBD-<SLUG>-<NNN>
    category: contradictory_evidence
    points_to: []
    resolver:
    blocks_current_step:
    blocks_next_step:
    notes:
  - id: TBD-<SLUG>-<NNN>
    category: sme_questions
    points_to: []
    resolver:
    blocks_current_step:
    blocks_next_step:
    notes:
  - id: TBD-<SLUG>-<NNN>
    category: downstream_handoff_blockers
    points_to: []
    resolver:
    blocks_current_step:
    blocks_next_step:
    notes:
```

Rules:

- One TBD = one category.
- Every TBD must name a resolver role.
- `blocks_current_step` and `blocks_next_step` must be answered explicitly.
- A TBD in `downstream_handoff_blockers` may have `blocks_current_step: no`
  but `blocks_next_step: yes` — surface it now so the next step is not
  surprised.

## 5. Handoff Note

- **Next step in chain:** <skill name | doc | gate>
- **What carries forward:** <artifacts and IDs the next step will consume>
- **Warnings carried forward:** <non-blocking warnings the next step must
  not silently drop>
- **Gate impact:** <which gate this result advances or blocks>

## 6. Revision History

| Revision | Date | Author | Change | New Status |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

Do not renumber prior `STEP-*` IDs across revisions. If a step is split or
re-scoped, mint a new `STEP-*` and reference the prior one in `notes`.
