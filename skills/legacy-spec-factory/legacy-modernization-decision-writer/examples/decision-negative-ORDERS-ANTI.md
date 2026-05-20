# Example: Anti-Pattern Decision Records

**Status**: ❌ These decision records fail anti-hallucination checks. Do NOT follow these patterns.

---

## Anti-Pattern #1: "Obvious Choice" Without Evidence

### Bad Decision Record

```
Decision: Use Spring Boot for order service

Context: We're building a Java microservice

Chosen Rationale: Spring Boot is the obvious choice for Java cloud services

Review Status: approved
```

### Problems

- ❌ **No evidence link**: Does not reference any EV or BR
- ❌ **No platform constraint**: Assumes target platform without checking
- ❌ **No alternatives**: Does not consider Quarkus, Micronaut, etc.
- ❌ **"Obvious" rationale**: Opinion-based, not grounded
- ❌ **No architecture approval**: Treats tech choice as trivial when it's critical

### Correct Version

```
Decision: Use Spring Boot 3.2 for order service (as specified in target platform)

Context: Target platform constraint is "Java 21 + Spring Boot 3 on AWS ECS"

Alternatives Considered:
  - Quarkus (faster startup, lower memory)
  - Micronaut (lightweight, cloud-native)
  - Spring Boot (mature, large ecosystem, required by platform)

Chosen Rationale: Target platform explicitly specifies Spring Boot 3.2
  (see platform constraint document). Alternatives not viable given
  platform mandate.

Linked Rules: BR-ORDERS-XYZ (requires Java 21 compatibility)

Target Platform Constraints:
  - "Java 21 + Spring Boot 3.2"
  - "Deployed on AWS ECS"

Review Status: approved (Architecture team signed off that Spring 3.2
  meets all requirements)
```

---

## Anti-Pattern #2: "Because Legacy Did It"

### Bad Decision Record

```
Decision: Retry failed orders exactly 3 times

Rationale: The legacy system retries 3 times, so the target should too

Review Status: approved
```

### Problems

- ❌ **No business rule**: Does not explain why legacy chose 3
- ❌ **No evidence**: No EV supporting the 3-retry policy
- ❌ **No alternatives**: Does not consider 2, 5, or exponential backoff
- ❌ **Blindly preserves legacy**: Without understanding the reason
- ❌ **Architecture didn't review**: No sign-off on whether 3 is right for cloud

### Correct Version

```
Decision: Use up to 3 retry attempts with exponential backoff for
  transient failures

Context: Legacy batch retries failed orders up to 3 times. Target is async
  queue-driven.

Linked Rule: BR-ORDERS-008 "Order processing must tolerate transient
  network errors (observed 2-3% failure rate in legacy logs)"

Evidence: EV-ORDERS-021 (legacy job log showing 2-3% network errors)

Alternatives Considered:
  - 1 attempt only (fails on any transient error — unacceptable)
  - 3 attempts linear backoff (legacy approach, predictable delay)
  - 3 attempts exponential backoff (recommended for cloud, reduces
    overwhelming target on recovery)
  - 5+ attempts (too lenient, increases latency)

Chosen: 3 attempts with exponential backoff (1s, 2s, 4s)

Rationale: BR-ORDERS-008 requires handling 2-3% failure rate. 3 attempts
  addresses this without excessive delay. Exponential backoff is cloud
  best practice for SQS queues.

Review Status: approved
  - SME approved: "3 retries matches legacy behavior"
  - Architecture approved: "Exponential backoff appropriate for SQS"
```

---

## Anti-Pattern #3: Invented Technology Without Authority

### Bad Decision Record

```
Decision: Use PostgreSQL for order database

Rationale: PostgreSQL is modern and widely used

Target Platform Constraints: (empty)

Review Status: approved
```

### Problems

- ❌ **No platform constraint**: PostgreSQL not mentioned in platform hint
- ❌ **No evidence**: No EV saying legacy uses relational DB (might be DB2, IDMS, etc.)
- ❌ **No alternatives**: Does not consider DynamoDB, RDS, etc.
- ❌ **Opinion-based**: "Modern and widely used" is not a decision
- ❌ **No architecture approval**: Someone just invented a database choice

### Correct Version

```
Decision: Use Amazon RDS PostgreSQL for order persistence

Context: Target platform specifies "AWS managed database". Legacy uses
  DB2 for i (relational, ACID).

Linked Rule: BR-ORDERS-012 "Order data must be consistent; no stale
  reads between order entry and fulfillment"

Evidence: EV-ORDERS-050 (DB2 schema for ORDERS table)

Alternatives Considered:
  - RDS PostgreSQL (relational, ACID, AWS managed, requires migration)
  - RDS MySQL (relational, less mature, requires migration)
  - DynamoDB (NoSQL, eventual consistency — violates ACID requirement)
  - Amazon Aurora Serverless (relational, auto-scaling, higher cost)

Chosen: RDS PostgreSQL

Rationale: BR-ORDERS-012 requires consistency. DynamoDB violates ACID.
  PostgreSQL and Aurora both work; PostgreSQL is lower-cost for initial
  scale. Migration path exists (legacy DB2 → PostgreSQL mapping is
  straightforward).

Target Platform Constraints:
  - "AWS managed database"
  - "ACID requirements for order transaction integrity"

Review Status: approved
  - SME approved: "DB2 schema migrates cleanly to PostgreSQL"
  - Architecture approved: "RDS PostgreSQL meets scale + cost targets"
```

---

## Anti-Pattern #4: Decision Approved Without SME or Architecture Review

### Bad Decision Record

```
Decision: Use Kafka for real-time order events

Status: approved

Approvals: (empty)
```

### Problems

- ❌ **No SME review**: Did not validate against legacy behavior
- ❌ **No architecture review**: Did not evaluate Kafka vs. SQS/SNS
- ❌ **No alternative analysis**: Kafka assumed without consideration
- ❌ **Fake approval**: Marked "approved" with no signatures

### Correct Version

```
Decision: Use AWS SNS for order event notifications (deferred Kafka
  evaluation)

Status: needs_sme_review

Pending Approvals:
  - Architecture Owner

Approvals:
  - SME (Jane Smith): not yet reviewed
  - Architecture (Bob Jones): not yet reviewed

Notes: Queuing technology (SQS vs. Kafka vs. SNS) is critical for scale.
  Deferring specific technology choice until architecture team evaluates
  throughput, cost, and operational burden. Request review by 2026-05-25.

Related TBD: TBD-ORDERS-031 "Which message queue technology (Kafka vs.
  SQS vs. SNS)?"
```

---

## Anti-Pattern #5: Unresolved Dependencies Approved Anyway

### Bad Decision Record

```
Decision: Defer customer deduplication to async batch job

Rationale: Will figure out dedup logic during implementation

Related TBD: TBD-ORDERS-015 "How to deduplicate customers
  across legacy and cloud?"

Status: approved

Blocking: yes
```

### Problems

- ❌ **Decision depends on unresolved TBD**
- ❌ **TBD is marked blocking (cannot proceed)**
- ❌ **Still marked "approved" anyway**
- ❌ **Forward SDLC will be blocked by this**

### Correct Version

```
Decision: [HOLD] Customer deduplication strategy

Status: draft (blocked)

Blocking Issue: TBD-ORDERS-015 "How to deduplicate customers across
  legacy and cloud?" must be resolved before deciding how dedup is
  executed (sync during entry, async batch, real-time cache, etc.)

Action:
  1. Resolve TBD-ORDERS-015 (architecture + SME decision on dedup
     semantics)
  2. Once TBD resolved, re-enter DEC workflow
  3. Write DEC with grounded rationale, then get approval
  4. Only then can forward SDLC proceed

Owner: Architecture team (Bob Jones)
Target Resolution: 2026-05-22
```

---

## Summary: How to Spot Bad Decisions

Red flags:

- ❌ Rationale contains "obvious", "clearly", "obviously", "must be"
- ❌ No linked BR/BEH or evidence
- ❌ No alternative options considered
- ❌ Target platform constraints are empty or vague
- ❌ Marked "approved" with no signature
- ❌ Depends on blocking TBD but still "approved"
- ❌ Technology choices (framework, database, queue) with no justification
- ❌ "Legacy did it" is the entire rationale
- ❌ Implementation details (API endpoints, retry counts) without grounding

If you see these, send the DEC back to decision writer with remediation notes.
