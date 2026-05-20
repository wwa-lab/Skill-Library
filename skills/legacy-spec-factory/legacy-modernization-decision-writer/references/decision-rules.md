# Decision Synthesis Rules

Guidance for expanding, grounding, and validating modernization decision
records.

## Decision Structure

Every `DEC-*` record must include:

```yaml
id: DEC-<CAP-SLUG>-<NNN>
knowledge_type: modernization_decision
category: <one of the categories below>
decision: <target-system choice>
context: <business reason + legacy scenario>
alternatives_considered:
  - <option 1>
  - <option 2>
  - <option 3>  # at least two real alternatives required
chosen_option: <selected option + brief why>
rejected_options:
  - <option>: <reason for rejection>
rationale: <evidence-backed explanation>
linked_rules:
  - BR-<CAP-SLUG>-NNN
  - BEH-<CAP-SLUG>-NNN
target_platform_constraints:
  - <explicit constraint from approved target platform hint>
implementation_impact: <effort, dependencies, risk>
compatibility_impact: <effects on other capabilities>
risks_and_mitigations:
  - risk: <unresolved issue>
    mitigation: <plan to address>
review_status: draft | needs_sme_review | approved | rejected | retired
pending_approvals:
  - <role still required before approval>
approvals:
  - role: <IBM i SME | Architecture Owner | Product Owner>
    person: <name>
    date: YYYY-MM-DD
    sign_off: <approved | requested_changes | needs_discussion>
```

## Decision Categories

### Architecture

**When to use**: decisions about service boundaries, orchestration patterns,
synchronous vs. asynchronous processing, deployment units, domain model
structure.

**Example DEC**:

```
decision: Use async event-driven architecture for customer order notifications
context: Legacy system uses synchronous RPG batch jobs; target may be
         real-time cloud SaaS. Affects customer experience and integration points.
alternatives_considered:
  - Preserve synchronous batch (legacy-like) — limits real-time visibility
  - Async event-driven (RabbitMQ/Kafka style) — improves latency & scale
  - Hybrid (sync for critical paths, async elsewhere) — operational complexity
chosen_option: Async event-driven, publish order events and let subscribers
              handle fulfillment notification in parallel
rationale: BR-ORDERS-004 requires notification within 5 minutes; legacy batch
          takes 8+ hours. Target platform supports message queues. Events
          decouple order entry from fulfillment.
linked_rules:
  - BR-ORDERS-004  # notifications within 5 min
  - BEH-ORDERS-003 # legacy batch runs nightly
target_platform_constraints:
  - "AWS SQS / SNS available"
  - "Event-driven microservices architecture"
```

### Data

**When to use**: decisions about entity relationships, data normalization,
temporal data handling, aggregation strategies, data ownership across services.

**Example DEC**:

```
decision: Denormalize customer contact info into order events
context: Legacy system copies customer phone into order header for fulfillment
         reference. Target breaks customer and order into separate services.
alternatives_considered:
  - Normalize (fetch from customer service on demand) — adds network calls
  - Denormalize (copy into event) — duplicates data but self-contained event
  - Handle by ID only (no phone) — loses legacy behavior
chosen_option: Denormalize; include customer phone in order.created event
rationale: BR-ORDERS-007 requires fulfillment team to have phone number without
          calling back. Denormalization is acceptable because phone doesn't
          change mid-fulfillment; eventual consistency OK.
linked_rules:
  - BR-ORDERS-007  # fulfillment must have phone
  - BEH-ORDERS-002 # legacy copies phone into ORDHEAD
```

### API Surface

**When to use**: decisions about REST endpoint design, gRPC vs. REST, request/
response structure, backward compatibility, API versioning, deprecation strategy.

**Example DEC**:

```
decision: Order creation API accepts individual line items, not batch upload
context: Legacy accepts batch file upload via FTP. Target is REST API.
         Affects integration partner workflows.
alternatives_considered:
  - Single-item POST (simpler validation, higher latency for bulk)
  - Batch POST (one call, higher validation complexity, backward compatible)
  - Support both (more API surface, maintenance burden)
chosen_option: Single-item POST with bulk upload helper library
rationale: BR-ORDERS-001 requires line-by-line validation and audit trail;
          batch upload would hide which line failed. Single-item API is
          clearer for cloud services. Helper library eases integration partner
          migration.
linked_rules:
  - BR-ORDERS-001  # line-by-line validation
target_platform_constraints:
  - "REST API microservice"
```

### Error Handling

**When to use**: decisions about error codes, retry semantics, circuit breakers,
exception mapping, logging/alerting strategy, degraded-mode behavior.

**Example DEC**:

```
decision: Use HTTP 422 (Unprocessable Entity) for business rule violations
context: Legacy returns detailed error text in file. Target is REST API.
         Must distinguish validation errors from system errors.
alternatives_considered:
  - 400 (Bad Request) for all errors — unclear semantics
  - 422 for validation, 500 for system — clear semantics, REST-standard
  - Custom 4XX codes — nonstandard, harder for integrations
chosen_option: 422 for rule violations (missing field, invalid amount),
              500 for system errors (database down), log details server-side
rationale: BR-ORDERS-009 specifies validation rules (amount > 0, status in
          enum); these are predictable and fixable by the caller. Distinguishing
          them from infrastructure errors helps partners retry intelligently.
linked_rules:
  - BR-ORDERS-009  # validation rules
  - BR-ORDERS-012  # error logging requirements
```

### Async Boundary

**When to use**: decisions about where work is enqueued, how long callers wait,
how results are delivered back, timeout and failure semantics, exactly-once vs.
at-least-once guarantees.

**Example DEC**:

```
decision: Order fulfillment runs as async background job; caller gets
         job ID immediately
context: Legacy batch job runs nightly and takes 2 hours; caller (store clerk)
         doesn't wait. Target must support same UX.
alternatives_considered:
  - Synchronous blocking call (2 hour wait — unacceptable UX)
  - Async with polling (caller polls job status)
  - Async with webhook callback (system calls back when done)
chosen_option: Async job queue; caller polls status via /order/{id}/fulfillment-status
rationale: BR-ORDERS-006 requires store clerk to proceed after order created;
          2-hour processing time is unacceptable to block. Polling is compatible
          with browser clients. Webhook requires integration partner stability
          (not guaranteed in MVP).
linked_rules:
  - BR-ORDERS-006  # async processing required
target_platform_constraints:
  - "Job queue (e.g., AWS SQS, Redis Bull)"
implementation_impact: "Order creation endpoint must enqueue job and return
                        immediately; job workers handle the 2-hour processing"
```

### Compatibility

**When to use**: decisions about backward compatibility with legacy systems,
migration path, deprecation timeline, data format compatibility, versioning.

**Example DEC**:

```
decision: Support legacy FTP batch upload via adapter for 6 months; remove
         when all partners migrate to REST
context: Some partners still send FTP files nightly. Target is REST API.
         Full cutover is planned but staged.
alternatives_considered:
  - Immediate REST-only (breaks partners, high risk)
  - Indefinite FTP support (indefinite tech debt)
  - 6-month transition (balanced risk)
chosen_option: FTP → REST adapter running as separate service for 6 months;
              partner migration roadmap published
rationale: BR-ORDERS-013 requires backward compatibility during initial launch;
          6 months allows partners to adopt REST API at their pace. Adapter
          isolates legacy protocol translation from core service.
linked_rules:
  - BR-ORDERS-013  # backward compatibility required
implementation_impact: "Develop FTP listener → REST translator; publish
                        partner migration guide"
compatibility_impact: "All external integrations must migrate from FTP to REST
                       within 6 months"
```

### Audit

**When to use**: decisions about audit trail (who, what, when), compliance
logging, evidence retention, tamper-proofing, integration with compliance systems.

**Example DEC**:

```
decision: Every order state change is immutable audit event; never updated
         or deleted
context: Legacy allows order correction via UPDATE (no trail); compliance
         requires 7-year retention and tamper-proof audit.
alternatives_considered:
  - Event sourcing (full audit, high operational complexity)
  - Audit table + business table (dual maintenance, risk of divergence)
  - Immutable events only (single source of truth)
chosen_option: Immutable event-only persistence; "current state" is computed
              from event stream
rationale: BR-ORDERS-017 requires non-repudiation (cannot deny actions taken);
          BR-ORDERS-018 requires 7-year retention. Immutable events satisfy
          both with single source of truth. Avoids audit/business table
          divergence.
linked_rules:
  - BR-ORDERS-017  # non-repudiation
  - BR-ORDERS-018  # 7-year audit retention
target_platform_constraints:
  - "Compliance system integration (e.g., IBM Cloud Compliance)"
implementation_impact: "Implement event store with append-only semantics; all
                        reads compute state from event stream"
risks_and_mitigations:
  - risk: "Event stream grows unbounded; queries slow"
    mitigation: "Implement periodic snapshot; queries read latest snapshot +
                 delta events"
```

### Security

**When to use**: decisions about authentication/authorization, secret management,
encryption at rest/in transit, API security (rate limiting, OAuth), sensitive
data handling.

**Example DEC**:

```
decision: Use OAuth 2.0 with client credentials for service-to-service auth;
         bearer tokens in Authorization header
context: Legacy uses API key in X-APIKey header (no expiration, no revocation).
         Target must support temporary access and audit.
alternatives_considered:
  - API keys (simple but no revocation)
  - OAuth 2.0 (industry standard, expiration & audit)
  - mTLS (secure but high PKI overhead)
chosen_option: OAuth 2.0 with 1-hour token expiration; integration partners
              exchange client credentials for access token
rationale: BR-ORDERS-021 requires audit trail of access (who called what, when);
          OAuth supports token revocation and audit logging. 1-hour expiration
          balances security and usability.
linked_rules:
  - BR-ORDERS-021  # access audit trail
target_platform_constraints:
  - "OAuth 2.0 provider (e.g., AWS Cognito, Auth0)"
security_impact: "All external API calls must use OAuth bearer token;
                  tokens expire after 1 hour; revocation takes 15 minutes
                  to propagate"
```

### Observability

**When to use**: decisions about metrics, logging, tracing, alerting, dashboards,
SLO/SLI definitions.

**Example DEC**:

```
decision: Every API call and async job is traced end-to-end with distributed
         trace ID
context: Legacy has no end-to-end tracing; support team cannot correlate
         orders across systems. Target must support fast troubleshooting.
alternatives_considered:
  - Logs only (no correlation across services)
  - Distributed tracing (e.g., Jaeger, DataDog) — correlates all calls
  - Custom correlation (reinvent the wheel)
chosen_option: Distributed tracing (e.g., AWS X-Ray); every order gets unique
              trace ID; all microservices emit spans
rationale: BR-ORDERS-025 requires support team to debug issues in <5 minutes.
          End-to-end tracing cuts troubleshooting time by ~70% (industry data).
          AWS X-Ray is included in target platform.
linked_rules:
  - BR-ORDERS-025  # fast troubleshooting
target_platform_constraints:
  - "AWS X-Ray or equivalent distributed tracing"
implementation_impact: "Add tracing library to all services; configure span
                        emitters; build dashboards for order flow visualization"
```

## Rationale Grounding

Every decision rationale must be grounded in:

1. **At least one linked business rule or behavior** (BR-* / BEH-*):
   - "BR-X requires Y, so we decided Z"
   - "BEH-X observed that legacy does Y, so target should Z"

2. **At least one evidence record** (`EV-*`):
   - Evidence supporting the linked BR/BEH
   - Evidence showing the legacy behavior affected by the decision

3. **At least one target platform constraint** when the decision chooses a
   target technology, topology, protocol, runtime, or deployment model:
   - "Target platform includes AWS SQS, so we chose async events"
   - "Target platform is Java/Spring, so we chose REST over gRPC"

4. **Evidence of evaluation** (at least 2 alternatives considered):
   - What else could we do?
   - Why did we reject it?
   - This shows decision rigor, not invented choice

If a decision is grounded only in opinion ("feels like the right choice"), it
stays `draft` or `needs_sme_review` with `pending_approvals` listing the missing
authority until the proper authority approves it explicitly.

## Approval Rules

### IBM i SME Approval

IBM i SME reviews `DEC-*` for:

- **Legacy behavior preservation**: does the decision respect observed BEH?
- **Business rule fidelity**: does the decision preserve BR semantics?
- **Missing SME knowledge**: are there unstated legacy constraints the decision
  overlooks?

SME can:

- Approve: "I confirm legacy behavior is preserved"
- Request changes: "The legacy system also does X; the decision should address
  it"
- Defer to architecture: "That's a target-platform choice; I can't approve"

**SME does NOT approve target architecture decisions.**

### Architecture / Product Owner Approval

Architecture / Product owner reviews `DEC-*` for:

- **Target platform alignment**: does the decision fit the declared architecture?
- **Implementation feasibility**: is it buildable in the target platform?
- **Trade-offs**: cost, performance, maintenance burden — are the trade-offs
  acceptable?
- **Cross-capability impact**: does the decision create coupling or conflict with
  other decisions?
- **Operational readiness**: can the ops team support it?

Architecture owner must **explicitly approve or reject** each `DEC-*` and sign
with date and role.

**If both SME and architecture/product authority have not signed, the DEC stays
`draft` or `needs_sme_review` with `pending_approvals` — never `approved`.**

## Unresolved Decisions

If a decision is unresolved:

- **Authority is unclear** ("should we choose A or B?")
- **Evidence is incomplete** ("we don't know if legacy does X")
- **Trade-offs need negotiation** ("cost vs. performance")

**Do NOT fake-approve the decision.** Instead:

1. File a `TBD-<CAP-SLUG>-NNN` linking to the decision
2. Describe the unresolved question and who needs to decide
3. Mark the TBD as `blocking: yes` if the decision must be resolved before code
   generation
4. Keep the DEC in `draft` or `needs_sme_review` status with
   `pending_approvals` populated

This makes the gap visible at the Forward Handoff Gate instead of hiding it
inside an "approved" decision.
