# Coverage Audit — Credit Limit Enforcement

**Package ID:** `PKG-CREDIT-CHECK-001`
**Generated:** 2026-05-16 15:00 UTC

## Summary Metrics

| Metric | Value |
| --- | --- |
| Approved `BR-*` closure rate | 100% (2 / 2) |
| `AC-*` approval rate | 100% (3 / 3) |
| `TC-*` to `AC-*` coverage | 33% (1 of 3 `AC-*` exercised by a planned `TC-*`) |
| Evidence usage rate | 100% (4 / 4 `EV-*` referenced ≥1 time) |

> Metrics are descriptive only. The gate status (`pass` / `pass_with_warnings`
> / `blocked`) is determined by the rules in
> `references/output-contract.md`, not by these numbers.

## BRD Functional Coverage

Required when a BRD is supplied. Sections 1-9 must be accepted or accepted with
a named non-blocking / deferred `TBD-*`.

| BRD Section | Required Area | Coverage Decision | Related TBD | Finding |
| --- | --- | --- | --- | --- |
| 1 | Function Purpose | accepted | — | — |
| 2 | Business Scenarios / Use Cases | accepted | — | — |
| 3 | Channels | accepted | — | — |
| 4 | User Interface / User Touchpoints | accepted | — | — |
| 5 | System Interfaces | accepted | — | — |
| 6 | Process Flow | accepted | — | — |
| 7 | Validation Rules | accepted | — | — |
| 8 | Error Handling | accepted | — | — |
| 9 | Dependencies | accepted | — | — |

## Evidence Coverage

| EV ID | Sensitivity | Redaction | Referenced By | Orphan? |
| --- | --- | --- | --- | --- |
| EV-CREDIT-CHECK-001 | public | not_required | BEH-001, BR-001, DEC-001, TC-001 | ❌ |
| EV-CREDIT-CHECK-002 | public | not_required | BEH-001, BR-001 | ❌ |
| EV-CREDIT-CHECK-003 | internal | reviewed | BEH-002, BR-002 | ❌ |
| EV-CREDIT-CHECK-004 | confidential | approved | BEH-002, BR-002, TC-001 | ❌ |

## Behavior Coverage

| BEH ID | Supporting EV | Backs Rules |
| --- | --- | --- |
| BEH-CREDIT-CHECK-001 | EV-001, EV-002 | BR-CREDIT-CHECK-001 |
| BEH-CREDIT-CHECK-002 | EV-003, EV-004 | BR-CREDIT-CHECK-002 |

## Business Rule Coverage

| BR ID | Status | EV | BEH | AC | TC | Closure |
| --- | --- | --- | --- | --- | --- | --- |
| BR-CREDIT-CHECK-001 | approved | EV-001, EV-002 | BEH-001 | AC-001, AC-002 | TC-001 | ✅ closed |
| BR-CREDIT-CHECK-002 | approved | EV-003, EV-004 | BEH-002 | AC-003 | — | ✅ closed |

## Acceptance Criteria Coverage

| AC ID | Validates | Review Status | Tested By |
| --- | --- | --- | --- |
| AC-CREDIT-CHECK-001 | BR-CREDIT-CHECK-001 | approved | TC-CREDIT-CHECK-001 |
| AC-CREDIT-CHECK-002 | BR-CREDIT-CHECK-001 | approved | — |
| AC-CREDIT-CHECK-003 | BR-CREDIT-CHECK-002 | approved | — |

## Test Coverage

| TC ID | Type | Validates | Sample Data EV | Golden Master |
| --- | --- | --- | --- | --- |
| TC-CREDIT-CHECK-001 | golden_master | AC-001, AC-002 | EV-CREDIT-CHECK-004 | true |

## Decision Coverage

| DEC ID | Status | Cites BR | Cites BEH | Cites Constraint |
| --- | --- | --- | --- | --- |
| DEC-CREDIT-CHECK-001 | approved | BR-CREDIT-CHECK-001 | BEH-CREDIT-CHECK-001 | — |

## Open Questions

No open `TBD-*` items.
