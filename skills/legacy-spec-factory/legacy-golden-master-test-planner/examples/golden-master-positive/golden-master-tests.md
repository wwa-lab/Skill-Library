# Golden Master Test Plan: Credit Limit Enforcement

## Status

| Field | Value |
| --- | --- |
| Capability | `CAP-CREDIT-LIMIT-001` |
| Plan ID | `STEP-CREDIT-LIMIT-001` |
| Status | `approved` |
| SME owner | Jane Smith (Credit Card Auth SME) |
| Spec source | `05_specs/CREDIT-LIMIT/spec.yaml` |

## Readiness Gate

| Gate | Status | Evidence |
| --- | --- | --- |
| Spec approved | pass | `05_specs/CREDIT-LIMIT/spec-review.md` |
| Business-critical rules approved | pass | `BR-CREDIT-LIMIT-001`, `BR-CREDIT-LIMIT-002` |
| Acceptance criteria approved | pass | `AC-CREDIT-LIMIT-001`, `AC-CREDIT-LIMIT-002`, `AC-CREDIT-LIMIT-003` |
| Runtime samples redacted | pass | `07_runtime-evidence/redaction-log-2025-05-01.md` |
| Expected outputs observed | pass | `EV-CREDIT-LIMIT-002`, `EV-CREDIT-LIMIT-004`, `EV-CREDIT-LIMIT-006` |

## Test Cases

### `TC-CREDIT-LIMIT-001` - Valid Order Within Credit Limit

| Field | Value |
| --- | --- |
| Priority | `P0` |
| Review status | `approved` |
| Validates | `BR-CREDIT-LIMIT-001`, `AC-CREDIT-LIMIT-001` |
| Legacy execution path | screen, `FLOW-CREDIT-LIMIT-001` |
| Input refs | `EV-CREDIT-LIMIT-001` |
| Expected-output refs | `EV-CREDIT-LIMIT-002` |
| Comparison mode | `exact` |

**Intent:** Protect the normal approval path for an order below available credit.

### `TC-CREDIT-LIMIT-002` - Credit Limit Exceeded Rejection

| Field | Value |
| --- | --- |
| Priority | `P0` |
| Review status | `approved` |
| Validates | `BR-CREDIT-LIMIT-002`, `AC-CREDIT-LIMIT-002` |
| Legacy execution path | screen, `FLOW-CREDIT-LIMIT-001` |
| Input refs | `EV-CREDIT-LIMIT-003` |
| Expected-output refs | `EV-CREDIT-LIMIT-004` |
| Comparison mode | `presence` |

**Intent:** Preserve the observed rejection message when the order exceeds
available credit.

### `TC-CREDIT-LIMIT-003` - Exact Limit Boundary

| Field | Value |
| --- | --- |
| Priority | `P1` |
| Review status | `approved` |
| Validates | `BR-CREDIT-LIMIT-001`, `AC-CREDIT-LIMIT-003` |
| Legacy execution path | screen, `FLOW-CREDIT-LIMIT-001` |
| Input refs | `EV-CREDIT-LIMIT-005` |
| Expected-output refs | `EV-CREDIT-LIMIT-006` |
| Comparison mode | `exact` |

**Intent:** Preserve the observed boundary behavior when amount equals available
credit.

## Deferrals and Gaps

No deferrals or blocking gaps.

## SME Sign-Off

| Role | Name | Date | Decision | IDs approved |
| --- | --- | --- | --- | --- |
| Capability-owner SME | Jane Smith | 2025-05-16 | approved | `TC-CREDIT-LIMIT-001`, `TC-CREDIT-LIMIT-002`, `TC-CREDIT-LIMIT-003` |
