# Decision Writer Anti-Hallucination Reference

Modernization decisions are where legacy choices become target-platform reality.
This catalog covers the most common hallucination temptations the decision writer
must resist.

---

## 1. Inventing Platform/Framework Choices

### Temptation

"The target is Java, so we should use Spring Boot. Let me add that as a DEC."

### Symptoms

- DEC rationale: "obvious choice for Java"
- No explicit target platform constraint supporting it
- No architecture owner signature
- DEC appears to come from model creativity, not from required authority

### Discipline

- **Do not choose Java, Spring, Kafka, PostgreSQL, cache TTLs, retry policies,
  or deployment topology** unless it is either:
  - Explicitly in the target platform hint (e.g., "Java 21 + Spring Boot 3 on
    AWS ECS"), OR
  - Explicitly approved by the architecture owner

- If the platform hint says only "cloud-based modernization" with no technology
  details:
  - File a `TBD-*` asking architecture owner for platform specifics
  - Keep the DEC in `draft` status
  - Do not invent the technology

- When in doubt: smaller, more honest DEC (defer to later refinement) is better
  than larger, more confident, more hallucinated DEC

---

## 2. Using "Legacy Did It" as Sufficient Rationale

### Temptation

"The legacy system retries failed batches three times, so the target should also
retry three times."

### Symptoms

- Rationale: "to preserve legacy behavior"
- No linked BR explaining *why* legacy retries exactly three times
- No evidence (code comment, SME note) justifying the number
- Architecture owner has not reviewed whether three retries fit the target
  architecture

### Discipline

- **Preserving legacy behavior is valid only if a BR explains why.**

- If no BR explains the legacy choice:
  - Either: create/promote a BR with SME approval ("retry logic must match
    legacy")
  - Or: surface as `TBD-*` ("is three retries the right policy for target
    platform?")

- A valid decision would be:
  ```
  decision: Use three-attempt retry with exponential backoff for failed orders
  rationale: BR-ORDERS-008 requires order processing to tolerate transient
            network errors (observed 2-3% failure rate). Three attempts balances
            resilience with delay. Exponential backoff is standard in target
            platform.
  ```

  NOT:
  ```
  decision: Retry three times (legacy did it)
  rationale: Legacy system retries three times
  ```

---

## 3. Promoting Draft Decisions Under Time Pressure

### Temptation

"Architecture owner is unavailable for three weeks; the spec needs to ship. I'll
mark this DEC approved because it's obviously correct."

### Symptoms

- DEC `review_status: approved` but `approvals[]` is empty or only has SME
- Spec ships while architecture decisions remain unsigned
- No date/signature from architecture owner

### Discipline

- A DEC is **only `approved`** when:
  - IBM i SME has reviewed BR/BEH linkage (explicit approval, date, name)
  - Architecture owner has reviewed target trade-offs (explicit approval, date,
    name)

- If architecture owner is unavailable:
  - Keep DEC as `needs_sme_review` and list `Architecture Owner` under
    `pending_approvals`
  - Spec status is `in_review` or `draft` (not `approved`)
  - Record a dated follow-up item: "architecture review due by [date]"

- Do not fake-approve. The Forward Handoff Gate depends on valid approvals;
  unsigned decisions hide risk.

---

## 4. Circular or Invented Evidence Links

### Temptation

"This DEC should reference BR-ORDERS-099, which I'll create at the same time."

### Symptoms

- DEC links to BR that does not yet exist
- BR is created inline just to support the DEC
- Neither have SME approval
- Circular reasoning: DEC justifies BR, BR justifies DEC

### Discipline

- Every DEC must link to **existing, approved (or at minimum drafted upstream)
  BRs, BEHs, and EVs** from the spec.yaml.

- Do not create BRs on-the-fly to support a DEC.

- If the BR you need is missing:
  - Request it from `legacy-spec-writer` or the module analyst
  - File a `TBD-*` explaining the dependency
  - Keep the DEC in `draft` until the upstream BR is available

- Valid: "DEC is grounded in BR-ORDERS-004 (approved upstream)"
- Invalid: "DEC references BR-ORDERS-099 (I'm creating this now to justify the
  decision)"

---

## 5. Filling in Missing Architecture Details

### Temptation

"The platform hint says 'cloud-based'. We probably need a message queue, so I'll
decide on RabbitMQ."

### Symptoms

- DEC assumes platform detail not explicitly stated
- Architecture owner hasn't weighed in
- Rationale is plausible but ungrounded ("probably need", "likely should")

### Discipline

- **Do not assume or invent platform architecture details.**

- If the target platform says "cloud-based" but does not specify:
  - Queuing technology (SQS vs. Kafka vs. RabbitMQ?)
  - Database (PostgreSQL vs. DynamoDB vs. Cosmos?)
  - Service boundary (one monolith vs. micro-services?)
  - Deployment (containers vs. serverless?)

  Then: file a `TBD-*` for architecture owner to decide.

- Do not fill in the blanks yourself.

- Valid DEC: "Target platform specifies AWS; we decided to use AWS SQS for order
  events (available, cost-effective for this scale)"
- Invalid DEC: "We should use AWS SQS (I guessed cloud might mean AWS)"

---

## 6. Approving Decisions with Unresolved Dependencies

### Temptation

"This DEC depends on deciding what database to use, but we can approve it now
and sort out the database later."

### Symptoms

- DEC status: `approved`
- But DEC references a `TBD-*` that is still `blocking: yes`
- Or DEC references BR that is only `draft`
- Or architecture owner approved the DEC but SME never reviewed it

### Discipline

- A DEC cannot be `approved` if:
  - It references an unresolved `blocking: yes` TBD
  - It links to `draft` or `needs_sme_review` BRs
  - SME review is incomplete
  - Architecture review is incomplete

- If the decision blocks on unresolved dependencies:
  - Keep DEC in `draft` or `needs_sme_review` with missing authorities listed
    in `pending_approvals`
  - Resolve the blocking TBD first
  - Get upstream BR promoted to `approved`
  - Only then approve the DEC

- Valid workflow:
  1. File TBD: "Which database?"
  2. Resolve TBD: "DynamoDB (approved by arch owner)"
  3. Promote DEC to `approved`: "Use DynamoDB"

- Invalid workflow:
  1. Approve DEC: "Use database X"
  2. Later: "Actually we need to decide which database"

---

## 7. Hiding Unresolved Questions in Prose

### Temptation

"I'll mention in the rationale that 'the exact retry count is still TBD' rather
than filing a TBD."

### Symptoms

- DEC status: `approved` (or `in_review`)
- But the rationale contains "unclear", "to be determined", "probably", "TBD",
  "pending"
- No corresponding TBD record in `open_questions[]`
- The Forward Handoff Gate has no structured way to detect the gap

### Discipline

- Every uncertainty is a **TBD with an ID, blocking status, and owner**.

- DEC text is unambiguous:
  - If you cannot state it clearly, the gap is a TBD
  - DEC rationale does not contain hedge words

- Invalid:
  ```
  decision: Retry failed orders
  rationale: "Unknown if exactly three retries is right, probably we should
            check with the legacy SME later..."
  review_status: approved
  ```

- Valid:
  ```
  decision: Retry failed orders up to N times
  rationale: "BR-ORDERS-008 requires transient failure handling; exact retry
            count depends on target infrastructure"
  review_status: needs_sme_review
  pending_approvals:
    - Architecture Owner

  [In spec.yaml open_questions[]]
  - id: TBD-ORDERS-042
    question: "What is the correct retry count for target infrastructure?"
    blocking: yes
    related_ids: [DEC-ORDERS-005]
  ```

---

## 8. Deciding API Shape Without Authority

### Temptation

"REST API makes sense, so I'll decide all endpoints return JSON with this
structure."

### Symptoms

- DEC specifies detailed API design (endpoint paths, response structure)
- No API design authority (product owner, API architect) has reviewed
- Decision rationale is "makes sense" or "REST best practice"
- No linked BR driving the API design

### Discipline

- **API surface decisions should be grounded in:**
  - Linked BR/BEH (e.g., "BR-ORDERS-001 requires line-item validation, so API
    must accept individual items")
  - Explicit target architecture (e.g., "REST API specified in platform hint")
  - Approval from API/product authority

- If API design is open:
  - File a `TBD-*` for API authority to decide
  - DEC can be "Use REST API (if approved)" but not detailed endpoints

- Do not design detailed API contracts without the API owner.

---

## 9. Inventing Acceptance Criteria

### Temptation

"This DEC about async processing will obviously need acceptance criteria like
'job completes within 10 minutes'."

### Symptoms

- DEC creates or implies acceptance criteria
- No BR justifies the 10-minute SLA
- SME has not approved the SLA
- AC text is written before the DEC is approved

### Discipline

- **Acceptance criteria are not the decision writer's job.**

- The decision writer:
  - Decides *what* the target system does (async processing)
  - May note *constraints* on the decision (job completes "quickly", error is
    recoverable)

- The spec writer (or acceptance criteria author):
  - Writes the actual AC with measurable criteria (10 minutes, <1% failure rate)
  - Links ACs to approved BRs/DECs
  - Gets SME approval for the AC itself

- DEC can note: "implementation impact: job must complete within time limit TBD
  with ops team"
- DEC should NOT write: "AC-ORDERS-019: job completes within 10 minutes"

---

## 10. Confusing Decision Approval with SME Approval

### Temptation

"The IBM i SME approved the DEC, so it's approved."

### Symptoms

- DEC has SME signature only
- No architecture/product owner signature
- DEC status: `approved`
- The external forward chain assumes DEC is safe to implement

### Discipline

- **SME approval and architecture approval are different gates.**

- SME approval covers:
  - Legacy behavior preservation
  - Business rule fidelity
  - Missing legacy constraints

- Architecture approval covers:
  - Target platform fit
  - Implementation feasibility
  - Trade-offs (cost, performance, ops)
  - Cross-capability impact

- DEC is **`approved` only when both have signed.**

- If only SME has signed:
  - DEC status: `needs_sme_review` with `Architecture Owner` listed under
    `pending_approvals` (not `approved`)
  - Spec status: `in_review` (not `approved`)

- Example approval structure:
  ```yaml
  approvals:
    - role: IBM i / Business SME
      person: Jane Smith
      date: 2026-05-16
      sign_off: approved
    - role: Architecture Owner
      person: Bob Jones
      date: 2026-05-17
      sign_off: approved
  ```

  If Bob's entry is missing, the DEC is not `approved`.

---

## The Cardinal Rule

> **If you cannot point to an existing, upstream BR/BEH/EV, or to an explicit
> approval from the target architecture authority, you are inventing.**

The decision writer's value is not creativity — it is discipline. The upstream
skills (module analyzer, spec writer, SME) have done the work to ground every
BR/BEH; the decision writer's job is to:

1. Link decisions to that evidence
2. Require competing alternatives
3. Get explicit architecture approval
4. Surface unresolved questions as TBDs
5. Refuse to invent

When in doubt: smaller, more honest, more TBD-heavy decision package is better
than larger, more confident, more hallucinated one.
