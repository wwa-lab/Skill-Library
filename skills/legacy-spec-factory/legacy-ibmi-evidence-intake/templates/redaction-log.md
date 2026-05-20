# Redaction Log: <CAPABILITY-NAME>

## Metadata

- capability_slug:
- evidence_manifest:
- intake_mode: internal_source_review | governed_redaction
- intake_reviewer:
- redaction_owner:
- redaction_owner_role:
- redaction_date:
- review_status: draft | in_review | approved | blocked

## Source Authorization / Redaction Summary

| Evidence ID | File / Item | Sensitivity | Strategy | Status | Owner |
| --- | --- | --- | --- | --- | --- |
| EV-<SLUG>-001 | <source path> | internal | source path verified; no separate redacted copy required for internal analysis | reviewed | <developer/reviewer> |
| EV-<SLUG>-001 | <item> | confidential | stable fake IDs; amounts shape-preserved; rule-critical values labeled if synthetic | pending | <owner> |

## Redaction Actions

Record categories and replacement strategies. Do not record raw sensitive
values in this log.

| Evidence ID | Category | Pattern / Field | Replacement Strategy | Shape Preserved | Semantic Preserved | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| EV-<SLUG>-001 | PII | customer_id | stable fake ID map held by redaction owner | yes | yes | raw mapping not committed |
| EV-<SLUG>-001 | financial_rule | approval_threshold | preserved exact value or synthetic value explicitly labeled | yes | yes / synthetic | do not infer exact legacy threshold from synthetic values |

## Spot Checks

| Evidence ID | Check | Result | Reviewer | Notes |
| --- | --- | --- | --- | --- |
| EV-<SLUG>-001 | PII scan | pass | <reviewer> | no unredacted IDs found |

## Open Issues

| TBD ID | Evidence ID | Issue | Blocking | Owner | Next Step |
| --- | --- | --- | --- | --- | --- |
| TBD-<SLUG>-001 | EV-<SLUG>-001 | <issue> | yes | <owner> | <action> |

## Approval

- intake_reviewer_approval:
- intake_review_date:
- redaction_owner_approval:
- approval_date:
- sme_review_required: yes | no
- sme_reviewer:
- sme_review_date:
- final_decision: pass | pass_with_warnings | blocked
