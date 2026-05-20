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
2. **Provide your answer in verbatim form** (use the space provided)
3. **Confirm or revise** any inferences or claims
4. **Note any caveats** or conditions
5. **Mark decision outcome** (confirmed / rejected / deferred / etc.)

All answers will be recorded in the decision log with your name, role, and date.

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
