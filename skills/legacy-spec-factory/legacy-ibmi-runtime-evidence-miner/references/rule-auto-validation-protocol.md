# Rule Auto-Validation Protocol

When `runtime-evidence.jsonl` contains samples that corroborate an
already-extracted `inferred_business_rule`, the runtime miner MAY
auto-promote the rule's `review_status` from `needs_sme_review` to
`auto_validated_spot_check_only`. SMEs then sample-check this bucket
instead of confirming every entry one-by-one.

**Why this matters.** A typical capability has 20–80 inferred rules.
Roughly 30–60% of them are "the code says X, runtime samples also show X
behavior" — these are low-controversy and waste SME bandwidth when
reviewed individually. Auto-validation surfaces them as a batch the SME
can spot-check, freeing time for the genuinely ambiguous rules.

## What this protocol is NOT

- **Not a replacement for SME review.** Auto-validated rules still
  require SME spot-check before the spec advances to `8c Spec Approved`.
- **Not for `modernization_decision` rules.** Those represent a proposed
  change; runtime data of legacy behavior cannot validate a forward
  decision.
- **Not for rules with `low` confidence on the source side.** If the
  program analyzer was unsure to begin with, runtime corroboration alone
  is not enough.

## Eligibility — rule must be ALL of:

| Field | Required value |
| --- | --- |
| `knowledge_type` | `inferred_business_rule` |
| Source-side `confidence` (from program-analysis.md) | `medium` or `high` (NOT `low`) |
| Linked `evidence_ids` | at least one `EV-SRC-*` (code-side) |
| `review_status` (current) | `needs_sme_review` |
| Rule has at least one **measurable outcome** (a field value, branch taken, file written, error code emitted) | yes |

If any of these fail, the rule stays at `needs_sme_review` for SME
review. Do not auto-validate.

## Corroboration threshold

Take the rule's measurable outcome. Search `runtime-evidence.jsonl` for
records whose conditions match the rule's antecedents.

| Matching runtime records | Outcome match | Action |
| --- | --- | --- |
| ≥ N (default N=3) | All match | promote to `auto_validated_spot_check_only` |
| ≥ N | Some match, some don't | flag as `runtime_conflict_with_inference` — keep at `needs_sme_review` and add to `blocking.sme_pending` with a note |
| < N | — | not enough runtime evidence; keep at `needs_sme_review` |
| 0 | — | no runtime evidence; keep at `needs_sme_review` |

`N=3` is the default; raise to 5 or 10 for `critical` programs (see
`legacy-ibmi-inventory/references/criticality-classifier.md`).

## What gets recorded

For each rule that crosses the threshold, the runtime miner writes back:

```yaml
review_status: auto_validated_spot_check_only
evidence_ids: [<existing EV-SRC-*>, <new EV-RUN-*>, ...]   # runtime evidence appended
auto_validation:
  matched_records: <count>
  runtime_evidence_ids: [EV-RUN-001, EV-RUN-007, EV-RUN-012, ...]
  validated_at: <ISO date>
  validated_by: legacy-ibmi-runtime-evidence-miner
  protocol_version: 1
```

The protocol entry is auditable: the SME (or anyone) can trace which
runtime samples corroborated the rule and re-run the check later.

## What gets surfaced to SME

`legacy-sme-review-facilitator` queries `inventory.yaml` +
`capabilities[].blocking.sme_pending` for each capability and partitions
rules into three review buckets:

| Bucket | Source filter | Default SME effort |
| --- | --- | --- |
| **Full review** | `review_status: needs_sme_review` AND criticality is `critical` (or runtime corroboration failed) | per-rule SME decision |
| **Spot-check** | `review_status: auto_validated_spot_check_only` | SME samples ~10–20% of rules in the bucket; if sample passes, batch-approves the rest |
| **Batch confirm** | rules from `low_risk` programs with auto-validation passed | single signoff on the whole batch |

The facilitator's `sme-review-email.md` and
`sme-review-checklist.md` templates render these as separate sections so
the SME sees the workload clearly:

```
You have 47 inferred rules to confirm:
  - Full review (CRITICAL): 8 rules — please decide each
  - Spot-check sample (STANDARD): pick 6 of 28 to verify
  - Batch confirm (LOW_RISK): 11 rules — single signoff if sample passes
Estimated SME time: 60-90 minutes total (vs. 5+ hours if reviewed individually)
```

## When auto-validation must NOT trigger

| Situation | Why |
| --- | --- |
| Runtime sample matches the antecedent but yields a DIFFERENT outcome | This is evidence the inference is WRONG, not evidence to skip review. Flag as `runtime_conflict_with_inference` and escalate to SME. |
| All matched samples come from a single date / batch run | One bad day in production should not validate a rule. Require samples spanning ≥ 2 distinct runs or ≥ 2 distinct days. |
| Rule depends on date/time, seasonality, or a configuration value | Runtime corroboration may reflect the current config only; SME must confirm the rule generalizes. Keep at `needs_sme_review`. |
| The capability's `criticality` is `critical` AND the rule affects money / posting / compliance | Default to per-rule SME review regardless of runtime corroboration. Auto-validation is a bandwidth-saver, not a safety bypass. |

## Spec schema impact

Add `auto_validated_spot_check_only` to the allowed values for
`review_status` in `schemas/spec.schema.yaml` and in every
`spec.yaml.rules[].review_status` consumer.

Promotion to `8c Spec Approved` requires:

- All `needs_sme_review` rules → SME decision (approved or rejected)
- All `auto_validated_spot_check_only` rules → at least one SME
  spot-check pass on the bucket (recorded in
  `08_business-understanding/<CAP-*>/sme-review-<date>.md`)
- No rules left in `runtime_conflict_with_inference`

## Audit trail

Every promotion writes one `history[]` entry to `workflow-state.yaml`:

```yaml
- at: <ISO 8601>
  skill: legacy-ibmi-runtime-evidence-miner
  capability_id: <CAP-*>
  stage_after: <unchanged stage_id>
  artifact: 07_runtime-evidence/runtime-evidence.jsonl
  note: "auto-validated N inferred rules against runtime samples (M still need SME)"
```

This lets the SME and orchestrator see at a glance how many rules were
auto-validated vs. still pending.
