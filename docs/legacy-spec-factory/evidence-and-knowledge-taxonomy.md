# Evidence and Knowledge Taxonomy

Legacy Spec Factory separates two dimensions that are easy to confuse:

1. **Knowledge type**: what kind of claim is being made.
2. **Evidence strength**: how strongly the claim is supported.

Both dimensions must be present before a claim can become an approved
requirement.

## Knowledge Type

| Type | Meaning | Can Become Requirement? |
| --- | --- | --- |
| `observed_behavior` | The legacy system demonstrably behaves this way | Yes, after SME review when needed |
| `inferred_business_rule` | A business rule inferred from code, data, or behavior | Only after SME confirmation |
| `modernization_decision` | A target-system design decision, not necessarily legacy behavior | Yes, after architecture/product approval |
| `unknown_tbd` | Evidence is missing, contradictory, or unclear | No |

## Evidence Strength

| Strength | Meaning | Example |
| --- | --- | --- |
| `confirmed_from_code` | Directly supported by source logic | RPGLE branch, CL command flow, DDS keyword |
| `observed_in_runtime` | Seen in runtime output or execution evidence | job log, spool output, transaction sample |
| `confirmed_by_sme` | Confirmed by an IBM i or business SME | SME review note or approval |
| `strongly_inferred` | Strong inference from multiple evidence points | control table plus repeated program usage |
| `weakly_inferred` | Plausible but under-supported inference | isolated naming or comment |
| `needs_sme_review` | Requires human judgment before use | unclear business intent |
| `contradictory` | Conflicting evidence exists | two programs implement different rounding |
| `missing` | Required evidence has not been collected | referenced PRTF unavailable |

## Approval Rule

A claim may be approved only when:

- `knowledge_type` is not `unknown_tbd`
- at least one linked evidence item has `evidence_strength` of:
  - `confirmed_from_code`
  - `observed_in_runtime`
  - `confirmed_by_sme`
- or linked evidence is `strongly_inferred` with explicit SME approval
- all linked TBDs are either resolved or marked non-blocking by an SME

## Required Fields

Every behavior, rule, and decision should include linked `evidence_ids`.
Do not duplicate `evidence_strength` on the claim; derive support level from
the linked evidence records to avoid drift.

```yaml
id:
knowledge_type:
statement:
evidence_ids:
confidence:
review_status:
review_notes:
```

## Confidence Scale

Use confidence as a supporting signal, not as approval.

| Confidence | Meaning |
| --- | --- |
| `high` | Evidence is direct and complete |
| `medium` | Evidence is plausible but incomplete |
| `low` | Weak support or unresolved ambiguity |

`high` confidence does not bypass SME review when the behavior is business
critical.
