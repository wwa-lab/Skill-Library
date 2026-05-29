# SME Question Pack

**Review ID:** REVIEW-`<CAPABILITY-SLUG>`-`<NNN>`
**Artifact:** `<path/to/artifact.md or .yaml>`
**Capability:** `<CAPABILITY-SLUG>`
**Prepared By:** `<facilitator name>`
**Prepared Date:** `YYYY-MM-DD`

---

## Instructions for SME

This document contains questions compiled from the artifact under review. For
each question:

1. **Read the question and context** (including evidence strength and prior
   claims)
2. **Reply in chat with the target ID and your choice** (for example:
   `BR-001 confirm` or `VAL-004 needs evidence`)
3. **Confirm or revise** any inferences or claims
4. **Note any caveats** or conditions
5. **Mark decision outcome** (confirmed / rejected / deferred / etc.)

All answers will be recorded in the decision log with your name, role, and date.
AI suggestions are prefilled only to reduce review effort; they are not SME
approval until you confirm or revise them.

Questions should be phrased in business language first. Program names, file
names, field names, and node IDs may appear under evidence, but the question
itself should ask about business intent, policy, outcome, exception handling, or
control ownership unless the SME explicitly owns the technical implementation.

---

## BRD Functional Analysis Coverage

Use this section only when reviewing a BRD Package. Confirm required BRD
sections 1-9 before reviewing individual rules and scenarios. Use target IDs
such as `BRD-<CAPABILITY>-001#section-03`; these are review targets, not new
repository IDs.

| Target | Required Area | Current Coverage | Evidence / TBD | Decision Needed |
| --- | --- | --- | --- | --- |
| `BRD-<CAPABILITY>-001#section-01` | Function Purpose | `<summary>` | `EV-...` / `TBD-...` | accept / revise / block |
| `BRD-<CAPABILITY>-001#section-02` | Business Scenarios / Use Cases | `<summary>` | `EV-...` / `TBD-...` | accept / revise / block |
| `BRD-<CAPABILITY>-001#section-03` | Channels | `<summary>` | `EV-...` / `TBD-...` | accept / revise / block |
| `BRD-<CAPABILITY>-001#section-04` | User Interface / User Touchpoints | `<summary>` | `EV-...` / `TBD-...` | accept / revise / block |
| `BRD-<CAPABILITY>-001#section-05` | System Interfaces | `<summary>` | `EV-...` / `TBD-...` | accept / revise / block |
| `BRD-<CAPABILITY>-001#section-06` | Process Flow | `<summary>` | `EV-...` / `TBD-...` | accept / revise / block |
| `BRD-<CAPABILITY>-001#section-07` | Validation Rules | `<summary>` | `EV-...` / `TBD-...` | accept / revise / block |
| `BRD-<CAPABILITY>-001#section-08` | Error Handling | `<summary>` | `EV-...` / `TBD-...` | accept / revise / block |
| `BRD-<CAPABILITY>-001#section-09` | Dependencies | `<summary>` | `EV-...` / `TBD-...` | accept / revise / block |

**Question for SME:**
> Are all required functional-analysis areas covered well enough for BRD
> approval and spec-writing? For any weak area, should we revise it now, carry a
> named non-blocking `TBD-*`, or block approval?

**Chat Reply Options:**
- `BRD section 1 accept`
- `BRD section 3 revise: <missing channel>`
- `BRD section 5 block: <reason>`
- `BRD section 9 accept with TBD-<CAPABILITY>-NNN`

**SME Answer:**

(Space for SME response)

---

## Open TBDs

### TBD-`<CAPABILITY>`-`<NNN>`: `<question title>`

**Context:**
(Brief description of why this question is open)

**Previous Claim:**
(What the artifact currently states as uncertain)

**Evidence Strength:** `missing` / `weakly_inferred` / `contradictory`

**Related Evidence:**
- `EV-<CAPABILITY>-NNN`: (brief note on what this shows)
- `EV-<CAPABILITY>-NNN`: (brief note)

**Question for SME:**
> Does the system actually [claim]? Or is the behavior different?

**SME Answer:**

(Space for SME response)

---

## Inferred Business Rules Needing SME Confirmation

### BR-`<CAPABILITY>`-`<NNN>`: `<rule title>`

**Rule Statement:**
> [The inferred rule as stated in artifact]

**Evidence Basis:**
- `EV-<CAPABILITY>-NNN`: (evidence strength: `confirmed_from_code` / `observed_in_runtime` / `weakly_inferred`)
- `EV-<CAPABILITY>-NNN`: (evidence strength)

**Current Status:** `draft` / `needs_sme_review`

**Question for SME:**
> Does this rule accurately reflect the business intent? Should we confirm it,
> reject it with a correction, defer it, or request more evidence?

**SME Answer:**

(Space for SME response)

---

## Contradictions Requiring SME Clarification

### FIND-`<CAPABILITY>`-`<NNN>`: `<contradiction title>`

**Position A (from evidence):**
> [First observed behavior or rule]
> Evidence: `EV-<CAPABILITY>-NNN` (source, strength)

**Position B (from evidence):**
> [Second observed behavior or rule]
> Evidence: `EV-<CAPABILITY>-NNN` (source, strength)

**Question for SME:**
> These two pieces of evidence seem to contradict. Which is correct, or are both legitimate under different circumstances?

**SME Answer:**

(Space for SME response)

---

## Validation Scenario Seeds

### VAL-`<CAPABILITY>`-`<NNN>`: `<scenario title>`

**Scenario Summary:**
> [The BRD-stage validation scenario seed]

**Scenario Type:** `happy_path` / `exception` / `boundary` / `negative` /
`manual_review`

**Related BR/BEH:**
- `BR-<CAPABILITY>-NNN`
- `BEH-<CAPABILITY>-NNN`

**Evidence:**
- `EV-<CAPABILITY>-NNN`: (source, type, strength)

**AI Suggested Decision:** `confirm` / `revise` / `needs_evidence` / `defer`

**Question for SME:**
> Is this a valid business validation scenario for the BRD? Should it become an
> acceptance-criteria candidate, golden-master candidate, SOW scope note, or be
> deferred?

**Chat Reply Options:**
- `VAL-NNN confirm`
- `VAL-NNN revise: <correction>`
- `VAL-NNN needs evidence: <what evidence>`
- `VAL-NNN defer: <owner / next step>`

**SME Answer:**

(Space for SME response)

---

## Behavior Confirmations

### BEH-`<CAPABILITY>`-`<NNN>`: `<observed behavior title>`

**Claim:**
> [The behavior we observed or inferred]

**Evidence:**
- `EV-<CAPABILITY>-NNN`: (source, type)

**Question for SME:**
> We observed [behavior]. Is this the intended system behavior, or a known issue / workaround?

**SME Answer:**

(Space for SME response)

---

## Modernization Decisions Requiring SME Acceptance

### DEC-`<CAPABILITY>`-`<NNN>`: `<decision title>`

**Decision Statement:**
> [The modernization or architectural decision]

**Rationale:**
(Why this decision was proposed)

**Tradeoff:**
(What we are gaining / losing with this choice)

**Question for SME:**
> Does this decision align with your business goals for modernization? Any concerns?

**SME Answer:**

(Space for SME response)

---

## Evidence Quality Questions

(Optional: if evidence is weak or incomplete)

### EV-`<CAPABILITY>`-`<NNN>`: `<evidence assessment>`

**Current Assessment:**
- Strength: `strongly_inferred` / `weakly_inferred` / `missing`
- Confidence: `high` / `medium` / `low`

**Question for SME:**
> Before downstream skills rely on rules that depend on this evidence, do we
> need to collect more evidence, or can we proceed with the evidence cited?

**SME Answer:**

(Space for SME response)

---

## Session Summary

**Total Questions:** `<count>`
**Questions Confirmed:** `<count>`
**Questions Rejected:** `<count>`
**Questions Deferred:** `<count>`
**New Issues Uncovered:** `<count>`

**SME Sign-Off:**

I have reviewed all questions and provided answers. I confirm that my responses
are accurate and reflect the business intent.

Signature/Initials: _______________
Date: _______________
Name (printed): _______________
Role: _______________
