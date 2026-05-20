# Equivalence Coverage Matrix: Credit Limit Enforcement

## Business Rule Coverage

| Business Rule | Criticality | Acceptance Criteria | Test Cases | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| `BR-CREDIT-LIMIT-001` | P0 | `AC-CREDIT-LIMIT-001`, `AC-CREDIT-LIMIT-003` | `TC-CREDIT-LIMIT-001`, `TC-CREDIT-LIMIT-003` | covered | Approval and exact-limit boundary |
| `BR-CREDIT-LIMIT-002` | P0 | `AC-CREDIT-LIMIT-002` | `TC-CREDIT-LIMIT-002` | covered | Rejection path |

## Acceptance Criteria Coverage

| Acceptance Criterion | Test Cases | Input Evidence | Expected-Output Evidence | Status |
| --- | --- | --- | --- | --- |
| `AC-CREDIT-LIMIT-001` | `TC-CREDIT-LIMIT-001` | `EV-CREDIT-LIMIT-001` | `EV-CREDIT-LIMIT-002` | covered |
| `AC-CREDIT-LIMIT-002` | `TC-CREDIT-LIMIT-002` | `EV-CREDIT-LIMIT-003` | `EV-CREDIT-LIMIT-004` | covered |
| `AC-CREDIT-LIMIT-003` | `TC-CREDIT-LIMIT-003` | `EV-CREDIT-LIMIT-005` | `EV-CREDIT-LIMIT-006` | covered |

## Evidence-to-Test Trace

| Evidence | Used As | Test Cases | Sensitivity / Redaction |
| --- | --- | --- | --- |
| `EV-CREDIT-LIMIT-001` | input | `TC-CREDIT-LIMIT-001` | approved |
| `EV-CREDIT-LIMIT-002` | expected output | `TC-CREDIT-LIMIT-001` | approved |
| `EV-CREDIT-LIMIT-003` | input | `TC-CREDIT-LIMIT-002` | approved |
| `EV-CREDIT-LIMIT-004` | expected output | `TC-CREDIT-LIMIT-002` | approved |
| `EV-CREDIT-LIMIT-005` | input | `TC-CREDIT-LIMIT-003` | approved |
| `EV-CREDIT-LIMIT-006` | expected output | `TC-CREDIT-LIMIT-003` | approved |

## Coverage Gaps

None.
