# Conversation Review Mode

Conversation Review Mode is the default SME interaction model for module-first
BRD work.

The user should be able to stay in one chat, provide RAG output, reviewed
flows when available, historical specs/documents, or SME notes, answer guided
review questions, and receive a completed BRD Package. Files are the audit
record; chat is the interaction surface.

## Default Flow

```text
RAG / retrieval output + reviewed flows or normalized docs/specs + SME notes
  -> context package
  -> module analysis
  -> draft BRD Package
  -> chat-driven SME review
  -> final BRD Package
```

## Review Loop

The assistant presents 3-7 review items at a time, prioritized by risk:

1. blocking `TBD-*`
2. contradictions
3. low-confidence `BR-*`
4. high-risk business rules
5. `VAL-*` boundary / exception scenarios
6. remaining behavior confirmations

Each item includes:

- target ID (`BR-*`, `TBD-*`, `BEH-*`, `VAL-*`, `FIND-*`, or `DEC-*`)
- short business question
- evidence IDs and confidence
- AI suggested decision, clearly labeled as a suggestion
- compact choices the SME can answer in chat
- optional free-form comment

Example:

```text
BR-CREDIT-LIMIT-001
Question: Is "orders above available credit are rejected" a real business rule?
Evidence: EV-CREDIT-LIMIT-001, EV-CREDIT-LIMIT-003
AI suggestion: confirm_for_spec_promotion

Reply with one:
1 confirm
2 reject
3 needs evidence
4 not a business rule
Optional comment:
```

The SME can answer tersely:

```text
BR-001 confirm
VAL-004 allowed
TBD-002 non-blocking, cache latency is downstream design
BR-003 reject, this is only a legacy workaround
```

## Write-Back Rules

Chat answers are not the source of truth until written back into artifacts.
After each review batch, the facilitator records decisions in:

```text
07_sme_reviews/<CAPABILITY-SLUG>/<REVIEW-SLUG>/
  review-session.md
  question-pack.md
  sme-decision-log.yaml
  sme-signoff.md
  follow-up-findings.yaml

05_brds/<CAPABILITY-SLUG>/
  review-decision.yaml
```

For BRD Package review, the facilitator also updates review-facing sections in
`brd-review.md`, `validation-scenarios.md`, and `traceability.md` when the SME
decision changes item status.

## Boundary Rules

- AI may prefill `ai_suggested_decision`; it must not write
  `sme_decision` until the SME answers in chat or another explicit review
  channel.
- `VAL-*` items are BRD-stage validation scenario seeds, not formal `TC-*`
  test cases.
- Formal `AC-*` acceptance criteria are produced by `legacy-spec-writer`.
- Formal `TC-*` golden master cases are produced by
  `legacy-golden-master-test-planner`.
- Email, meetings, and offline checklists are optional export channels, not the
  default review workflow.
