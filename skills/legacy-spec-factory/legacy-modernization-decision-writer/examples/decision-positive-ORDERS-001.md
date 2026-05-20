# Example: Good Decision Record

**Status**: ✅ Approved decision record that passes anti-hallucination checks.

---

# Decision Record: `DEC-ORDERS-001`

**Capability**: `CAP-ORDERS-001` (Order Management)
**Category**: `architecture`
**Status**: `approved`

## Decision Statement

> Use async event-driven architecture for order fulfillment processing.

## Context

### Legacy Behavior

- **Observed**: Order fulfillment runs as RPG batch job nightly (22:00–02:00)
- **Evidence**: Job log excerpt `EV-ORDERS-015` (confirmed_from_code)

### Business Requirement

- **Rule**: `BR-ORDERS-004` — "Order entry must complete in <5 seconds without waiting for fulfillment"
- **Evidence**: Clerk workflow notes `EV-ORDERS-016` (confirmed_by_sme)

### Target Platform Constraint

> "Cloud-native Java/Spring microservices on AWS ECS with SQS/SNS messaging"

## Alternatives Considered

### Option 1: Preserve Sync Batch

- **Pros**: Mirrors legacy (SME comfort)
- **Cons**: Violates BR-004 (5-second requirement)
- **Evaluation**: **Rejected** — incompatible with BR requirement

### Option 2: Async Event-Driven (CHOSEN)

- **Pros**: Meets BR-004; leverages AWS SQS (included in platform); decouples services
- **Cons**: Requires queue infrastructure, polling model for clients
- **Evaluation**: **Chosen** — best fit for requirement + platform

### Option 3: Hybrid Sync + Async

- **Pros**: Fast validation + async processing
- **Cons**: Complex; higher operational burden
- **Evaluation**: **Rejected** — over-engineered for MVP

## Rationale

**BR-ORDERS-004 requires <5s order entry completion.** Legacy batch violates this (2–8 hour lag). **Async event-driven satisfies the requirement.** Target platform provides AWS SQS natively, eliminating infrastructure cost. **Events decouple order entry from fulfillment**, enabling independent scaling.

## Linked Business Rules

- ✅ `BR-ORDERS-004`: Order entry <5s (decision enables this)
- ✅ `BR-ORDERS-005`: Fulfillment job can be tracked (queue provides visibility)
- ✅ `BR-ORDERS-006`: Transient failures retry (SQS provides retry)

## Evidence Support

- ✅ `EV-ORDERS-015`: Job log shows 2–8 hour nightly batch
- ✅ `EV-ORDERS-016`: SME confirms clerk cannot wait

## Target Platform Constraints

- ✅ AWS SQS available (message queue)
- ✅ AWS SNS available (notifications)
- ✅ Java/Spring async libraries (built-in)

## Implementation Impact

- **Effort**: 1–2 weeks (queue setup, worker implementation, testing)
- **Dependencies**: SQS provisioned, event schema designed
- **Risks**: Event lag (mitigated: 60-second SLA), job failure (mitigated: dead-letter queue)

## Approvals

| Role | Person | Date | Sign-off |
|------|--------|------|----------|
| IBM i SME | Jane Smith | 2026-05-17 | ✅ Approved |
| Architecture | Bob Jones | 2026-05-18 | ✅ Approved |
| Product | Alice Chen | 2026-05-19 | ✅ Approved |

---

## Why This Decision Is Good

✅ **Grounded in evidence**: References specific EV records (job log, SME notes)
✅ **Grounded in requirements**: Links to approved BR (must complete in <5s)
✅ **Grounded in platform**: References explicit AWS SQS/SNS availability
✅ **Alternatives evaluated**: Shows 3 real options with trade-offs
✅ **Authority clear**: SME + Architecture + Product all signed
✅ **Rationale is evidence-backed**: Does not say "feels like the right choice"
✅ **Risks are explicit**: Dead-letter queue + monitoring mentioned
✅ **Not over-specified**: Defers API design/retry policy to separate DECs

→ **Ready for implementation.**
