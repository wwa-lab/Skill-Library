# Spec: <Capability Name> (CAP-<CAP-SLUG>-001)

> Human-readable rendering of `spec.yaml`. The YAML is canonical; this
> file mirrors it for review and discussion.

## Status: draft | in_review | approved | retired

## Business Goal
<one-sentence outcome>

## Capability Owner
<SME name and role>

## Source System
- System: <IBM i / partition>
- Libraries: <list>
- Collection: YYYY-MM-DD

## Target Platform
- Architecture: <stack>
- Service hint: <module/service>

## Scope

**In scope:**
- ...

**Out of scope:**
- ...

## Business Rules

| ID | Rule | Confidence | Status | Evidence | Linked Behaviors |
| --- | --- | --- | --- | --- | --- |
| BR-<CAP-SLUG>-001 | ... | high | approved | EV-..., EV-... | BEH-... |

## Observed Behaviors

| ID | Statement | Confidence | Evidence |
| --- | --- | --- | --- |
| BEH-<CAP-SLUG>-001 | ... | high | EV-... |

## Modernization Decisions

| ID | Decision | Rationale | Impact | Status |
| --- | --- | --- | --- | --- |
| DEC-<CAP-SLUG>-001 | ... | references BR-001 | ... | approved |

## Data Model

### Entity: <Name>

Legacy sources: OBJ-..., OBJ-...

| Field | Legacy Field | Type | Evidence |
| --- | --- | --- | --- |
| ... | ... | ... | EV-... |

## Process Flow

Business-visible steps the target capability must support. Do not copy the
legacy program call chain here; cite legacy program / flow evidence through
`EV-*` references in `spec.yaml` and `traceability.md`.

1. STEP-001 — ...
2. STEP-002 — ...

## Inputs / Outputs / Exceptions

| Type | ID | Name | Source / Target | Evidence |
| --- | --- | --- | --- | --- |
| Input | IN-001 | ... | api | EV-... |
| Output | OUT-001 | ... | api_response | EV-... |
| Exception | EX-001 | ... | severity: warning | EV-... |

## Acceptance Criteria

### AC-<CAP-SLUG>-001 (validates BR-<CAP-SLUG>-001)

```
Given ...
When ...
Then ...
```

## Open Questions

| ID | Question | Blocking | Related |
| --- | --- | --- | --- |
| TBD-001 | ... | yes / no / pending_sme | ... |

## Traceability Summary

See `traceability.md` for the full BR → EV / AC / TC walk.

## SME Sign-Off

See `spec-review.md`.
