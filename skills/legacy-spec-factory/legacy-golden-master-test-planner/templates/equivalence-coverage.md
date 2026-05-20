# Equivalence Coverage Matrix: <Capability Name>

## Business Rule Coverage

| Business Rule | Criticality | Acceptance Criteria | Test Cases | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| `BR-<CAPABILITY-SLUG>-001` | P0 | `AC-<CAPABILITY-SLUG>-001` | `TC-<CAPABILITY-SLUG>-001` | pending |  |

## Acceptance Criteria Coverage

| Acceptance Criterion | Test Cases | Input Evidence | Expected-Output Evidence | Status |
| --- | --- | --- | --- | --- |
| `AC-<CAPABILITY-SLUG>-001` | `TC-<CAPABILITY-SLUG>-001` | `EV-<CAPABILITY-SLUG>-001` | `EV-<CAPABILITY-SLUG>-002` | pending |

## Evidence-to-Test Trace

| Evidence | Used As | Test Cases | Sensitivity / Redaction |
| --- | --- | --- | --- |
| `EV-<CAPABILITY-SLUG>-001` | input | `TC-<CAPABILITY-SLUG>-001` | pending |
| `EV-<CAPABILITY-SLUG>-002` | expected output | `TC-<CAPABILITY-SLUG>-001` | pending |

## Coverage Gaps

| Finding ID | Gap | Related IDs | Blocking? | Resolver |
| --- | --- | --- | --- | --- |
| `FIND-<CAPABILITY-SLUG>-001` | <missing sample or expected output> | `BR-*`, `AC-*` | yes | <role/name> |
