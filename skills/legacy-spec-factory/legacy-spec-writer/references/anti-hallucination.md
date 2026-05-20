# Spec Writer Anti-Hallucination Reference

The spec is the last artifact before code generation. Any invention here
becomes a bug in the modernized system. This document catalogs the most
common hallucination temptations the spec-writer must resist.

---

## 1. Inventing Business Rules

### Temptation
"There must be a rule about [X]. Let me add it as a BR."

### Symptoms
- BR has no `evidence_ids`
- BR's `linked_behaviors` is empty
- The "rule" was suggested by no one — neither code nor SME

### Discipline
- If no EV supports it → not a BR; either discard or file as TBD
- If only weak signals (field name, comment) support it → BR `draft` /
  `needs_sme_review`, never `approved`
- See `rule-extraction-protocol.md`

---

## 2. Promoting Draft Rules Under Time Pressure

### Temptation
"SME is unavailable for two weeks; the spec needs to ship. I'll mark this
BR approved because it's obviously correct."

### Symptoms
- BR `review_status: approved` but no SME entry in `spec-review.md`
- Spec ships with capability "complete" when actually 30% of BRs are
  speculative

### Discipline
- A BR is only `approved` when a named SME has signed off (date + signature
  in `spec-review.md`)
- Ship the spec with `status: in_review` and BRs in `needs_sme_review`
  rather than fake-approving

---

## 3. Filling in Data Model Field Meanings

### Temptation
"This field is called `STATUS`; it must hold values like ACTIVE, INACTIVE,
CLOSED."

### Symptoms
- Data model `fields[]` has type / semantics not sourced from DDS or SQL
  definitions
- Enum values listed without evidence

### Discipline
- Field semantics come from DDS / SQL / SME — never from the field name
- If the meaning is unclear → field carries an open question / TBD
- If the source DDS is incomplete → escalate as inventory gap

---

## 4. Inventing Modernization Decisions

### Temptation
"The target should be a microservice with REST API and event-driven
async processing."

### Symptoms
- DEC entries with rationale that doesn't tie to any BR / BEH /
  `target_platform` constraint
- Target architecture more detailed than the platform hint warranted

### Discipline
- Each DEC must have a rationale grounded in:
  - A BR that the decision serves
  - A BEH that the decision preserves or intentionally replaces
  - A `target_platform` constraint (concrete, not generic)
- If no grounding exists → either skip the decision or mark it `draft`

---

## 5. Smoothing Over Inconsistent Flows

### Temptation
"Flow A says credit is checked before lookup; flow B says credit is
checked after lookup. They probably meant the same thing — I'll pick
one."

### Symptoms
- BEHs claim consistency where flows actually diverge
- TBDs hidden / omitted

### Discipline
- Inconsistent legacy is a fact — record both BEHs and flag a TBD
- The SME may explain (different channels have different policies) or
  may admit one is a bug; both are valid outcomes but only after SME
  weighs in

---

## 6. Padding Evidence Bundles

### Temptation
"This rule looks lonely with only one EV. Let me add a related EV to make
it look better-grounded."

### Symptoms
- BR's `evidence_ids` contains EVs whose relevance is tangential
- Reviewer can't follow why each EV supports the rule

### Discipline
- Add only EVs that *directly* support the BR
- If only one EV genuinely supports the rule, that's one EV; don't pad
- A weakly-evidenced BR should stay `medium` or `low` confidence rather
  than acquire fake supporting evidence

---

## 7. Generating Acceptance Criteria for Unapproved Rules

### Temptation
"BR is `needs_sme_review`, but I'll write the AC now to save time later."

### Symptoms
- AC `validates: [BR-X]` where BR-X is `draft` or `needs_sme_review`
- AC text contains assumptions the BR doesn't yet justify

### Discipline
- Write ACs *only* for `approved` BRs
- If the BR changes after SME review, the AC may also change — don't
  prematurely lock in test scenarios

---

## 8. Asserting Acceptance Criteria Beyond the BR

### Temptation
"The BR says credit limit must be respected. Let me add an AC that also
specifies response time under load."

### Symptoms
- AC contains assertions not in the BR text
- AC `validates` a single BR but the AC is multi-rule

### Discipline
- ACs are evidence that BRs are satisfied — they cannot test more than
  the BR claims
- If an AC tests additional behavior, the additional behavior should
  itself be a BR, then a separate AC

---

## 9. Hiding TBDs in Free Text

### Temptation
"I'll mention in the BR text that 'the exact threshold is unclear' rather
than filing a TBD."

### Symptoms
- `open_questions[]` is short while the spec contains many "unclear",
  "to be determined", "subject to confirmation" phrases
- Downstream `build-agent-skill` has no way to detect the embedded gaps

### Discipline
- Every uncertainty is a TBD with an ID, blocking status, and owner
- BR text is unambiguous; if it can't be made unambiguous, the gap is a
  TBD that prevents `approved` status

---

## 10. Approving the Spec Without Cross-Checking Traceability

### Temptation
"All BRs look approved. Let me mark the spec approved."

### Symptoms
- An approved BR has no AC
- An AC points to a non-existent or non-approved BR
- An EV is in `evidence[]` but nothing references it
- A `blocking: yes` TBD remains in `open_questions[]`

### Discipline
- Generate `traceability.md` and verify:
  - Every approved BR → ≥1 EV
  - Every approved BR → ≥1 AC
  - Every AC → exactly the approved BRs it validates
  - No orphan ACs / unused EVs
  - No `blocking: yes` TBDs without SME waiver
- Only then mark `status: approved`

---

## The Cardinal Rule

> **If you cannot point to a specific upstream artifact (EV, BEH, flow,
> module view, SME note) for every claim in the spec, you are inventing.**

The spec writer's value is not creativity — it is faithfulness. The
upstream skills have done the work to ground every claim; the spec
writer's job is to organize and refine that grounding into a buildable
contract, not to fill in gaps that the SME hasn't filled.

When in doubt: smaller, more honest, more TBD-heavy spec is better than
larger, more confident, more hallucinated spec.
