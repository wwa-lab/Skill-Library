# Decision Record: `DEC-<CAP-SLUG>-001`

**Step**: `STEP-<CAP-SLUG>-001`
**Capability**: `CAP-<CAP-SLUG>-001` (`<Capability Name>`)
**Category**: `architecture | data | api_surface | error_handling | async_boundary | compatibility | audit | security | observability`
**Review Status**: `draft | needs_sme_review | approved | rejected | retired`
**Last Updated**: `YYYY-MM-DD`

---

## Decision Statement

`<Concise target-system choice. Do not include implementation tasks or code.>`

## Context

### Legacy Behavior

| ID | Statement | Evidence |
| --- | --- | --- |
| `BEH-<CAP-SLUG>-NNN` | `<observed legacy behavior affected by this decision>` | `EV-<CAP-SLUG>-NNN` |

### Business Rules

| ID | Rule | Review Status | Evidence |
| --- | --- | --- | --- |
| `BR-<CAP-SLUG>-NNN` | `<approved or in-review rule this decision supports>` | `approved | needs_sme_review` | `EV-<CAP-SLUG>-NNN` |

### Target Platform Constraints

Only list constraints that are explicitly supplied by an approved platform
brief, architecture note, or named authority.

| Constraint | Source | Required? |
| --- | --- | --- |
| `<platform constraint, or "None supplied">` | `<source or authority>` | `yes | no` |

## Alternatives Considered

At least two real alternatives are required. "Do nothing" or "preserve legacy
behavior" is valid only when it is a real option.

| Option | Description | Pros | Cons | Evaluation |
| --- | --- | --- | --- | --- |
| `<Option 1>` | `<summary>` | `<advantages>` | `<disadvantages>` | `chosen | rejected | deferred` |
| `<Option 2>` | `<summary>` | `<advantages>` | `<disadvantages>` | `chosen | rejected | deferred` |

## Chosen Option And Rationale

**Chosen option**: `<selected option>`

**Rationale**:

`<Explain why this option should be used in the target system. Ground the
rationale in linked BR/BEH/EV records and explicit target constraints when the
decision chooses technology, topology, protocol, or runtime. Do not use "legacy
did it" as sufficient rationale.>`

## Rejected Options

| Option | Reason Rejected | Evidence Or Constraint |
| --- | --- | --- |
| `<rejected option>` | `<why it was rejected>` | `BR/BEH/EV/TBD or target constraint` |

## Traceability

### Linked Rules And Behaviors

| ID | Type | Relationship To Decision |
| --- | --- | --- |
| `BR-<CAP-SLUG>-NNN` | business_rule | `<supports / constrains / affected by>` |
| `BEH-<CAP-SLUG>-NNN` | observed_behavior | `<preserved / replaced / intentionally changed>` |

### Evidence

| Evidence ID | Strength | Used For |
| --- | --- | --- |
| `EV-<CAP-SLUG>-NNN` | `confirmed_from_code | observed_in_runtime | confirmed_by_sme | strongly_inferred | weakly_inferred | needs_sme_review | contradictory | missing` | `<claim supported>` |

### Related TBDs

| TBD | Blocking? | Owner | Required Resolution |
| --- | --- | --- | --- |
| `TBD-<CAP-SLUG>-NNN` | `yes | no` | `<role/person>` | `<what must be decided>` |

## Impact

### Implementation Impact

`<Describe impact, dependencies, and risk at decision level. Do not create task
breakdowns, code steps, API contracts, deployment topology, or test cases here.>`

### Compatibility Impact

`<Describe migration, coexistence, partner, data-format, or cross-capability
impact.>`

### Risks And Mitigations

| Risk | Severity | Mitigation | Owner | Status |
| --- | --- | --- | --- | --- |
| `<risk>` | `low | medium | high | critical` | `<mitigation>` | `<role/person>` | `open | mitigated | accepted | retired` |

## Approvals

A DEC cannot be `approved` unless required approvals are present. SME approval
covers legacy fidelity; architecture/product approval covers target-system fit.

| Role | Person | Date | Sign-Off | Notes |
| --- | --- | --- | --- | --- |
| IBM i / Business SME | `<name>` | `YYYY-MM-DD` | `approved | requested_changes | needs_discussion | deferred` | `<legacy-fidelity notes>` |
| Architecture Owner | `<name>` | `YYYY-MM-DD` | `approved | requested_changes | needs_discussion | deferred` | `<target-system notes>` |
| Product Owner | `<name or not required>` | `YYYY-MM-DD` | `approved | requested_changes | needs_discussion | deferred | not_required` | `<business-impact notes>` |

### Pending Approvals

| Role | Reason Needed | Blocks Approval? |
| --- | --- | --- |
| `<role>` | `<why this authority must decide>` | `yes | no` |

## Reconciliation Back To `spec.yaml`

Only schema-compliant fields are copied back into
`spec.yaml.modernization_decisions[]`. Detailed alternatives and approvals stay
in this decision package. The decision-writer does not mint AC-*; any missing
acceptance criteria must be routed back to `legacy-spec-writer`.

```yaml
id: DEC-<CAP-SLUG>-001
knowledge_type: modernization_decision
decision: "<schema-compliant decision text>"
rationale: "<schema-compliant rationale text>"
evidence_ids:
  - EV-<CAP-SLUG>-NNN
impact: "<implementation/testing impact summary>"
review_status: draft # draft | needs_sme_review | approved | rejected | retired
```

## References

- **Spec**: `05_specs/<CAP-SLUG>/spec.yaml`
- **Decision package**: `05_decisions/<CAP-SLUG>/modernization-decisions.yaml`
- **Related decisions**: `DEC-<CAP-SLUG>-NNN`
- **Related TBDs**: `TBD-<CAP-SLUG>-NNN`
