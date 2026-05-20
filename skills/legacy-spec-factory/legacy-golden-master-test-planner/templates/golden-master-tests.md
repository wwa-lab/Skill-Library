# Golden Master Test Plan: <Capability Name>

## Status

| Field | Value |
| --- | --- |
| Capability | `CAP-<CAPABILITY-SLUG>-001` |
| Plan ID | `STEP-<CAPABILITY-SLUG>-001` |
| Status | `draft` |
| SME owner | `<name / role>` |
| Spec source | `05_specs/<CAPABILITY-SLUG>/spec.yaml` |

## Readiness Gate

| Gate | Status | Evidence |
| --- | --- | --- |
| Spec approved | pending | `05_specs/<CAPABILITY-SLUG>/spec-review.md` |
| Business-critical rules approved | pending | `BR-*` list |
| Acceptance criteria approved | pending | `AC-*` list |
| Runtime samples redacted | pending | `<redaction log>` |
| Expected outputs observed | pending | `EV-*` list |

## Test Cases

### `TC-<CAPABILITY-SLUG>-001` - <Short Behavior Name>

| Field | Value |
| --- | --- |
| Priority | `P0` |
| Review status | `draft` |
| Validates | `BR-<CAPABILITY-SLUG>-001`, `AC-<CAPABILITY-SLUG>-001` |
| Legacy execution path | `<batch / screen / report / integration>` |
| Input refs | `EV-<CAPABILITY-SLUG>-001` |
| Expected-output refs | `EV-<CAPABILITY-SLUG>-002` |
| Comparison mode | `exact` |

**Intent:** <why this case protects important legacy behavior>

**Preconditions:**

- <required state>

**Inputs:**

- <redacted sample reference and field-shape notes>

**Expected outputs:**

- <observed legacy output reference>

**Comparison rules:**

- <exact / normalized / tolerant / presence / ordering-insensitive rule>

## Deferrals and Gaps

| Finding ID | Severity | Related IDs | Required remediation |
| --- | --- | --- | --- |
| `FIND-<CAPABILITY-SLUG>-001` | blocking | `BR-*`, `AC-*`, `EV-*` | <action> |

## SME Sign-Off

| Role | Name | Date | Decision | IDs approved |
| --- | --- | --- | --- | --- |
| Capability-owner SME |  |  | pending |  |
