# Question Taxonomy

This document provides a framework for organizing and categorizing SME review
questions. Use this to structure the question pack and ensure no review items are
missed or miscategorized.

## Categories

### 0. BRD Functional Analysis Coverage (`BRD-*#section-*`)

**Purpose:** Confirm that a BRD Package covers the SME-required functional
analysis areas before item-level rule and scenario review.

Use this category only when the artifact under review is
`05_brds/<CAPABILITY-SLUG>/brd.md`.

**Required Areas:**
- Section 1 — Function Purpose
- Section 2 — Business Scenarios / Use Cases
- Section 3 — Channels
- Section 4 — User Interface / User Touchpoints
- Section 5 — System Interfaces
- Section 6 — Process Flow
- Section 7 — Validation Rules
- Section 8 — Error Handling
- Section 9 — Dependencies

**Review Target IDs:**
Use a stable BRD-section target rather than minting a new repository ID:
`BRD-<CAPABILITY-SLUG>-001#section-01` through
`BRD-<CAPABILITY-SLUG>-001#section-09`.

If a required area is missing or weak, create or reference a `TBD-*` and record
the section decision as `accepted_with_tbd` or `blocked`.

**Questions to Ask:**
- "Does this section correctly describe the function from a business
  perspective?"
- "Is anything important missing for this required SME review area?"
- "Can this gap be carried forward as non-blocking, or does it block BRD
  approval / spec-writing?"

**SME Outcomes:**
- `accepted`: Section is fit for BRD approval.
- `accepted_with_tbd`: Section is usable, but the named `TBD-*` must be carried
  forward.
- `blocked`: Section is missing, unsupported, or inaccurate enough to block the
  BRD.
- `needs_more_evidence`: SME cannot decide until more evidence is collected.

**Recording in Question Pack:**
```markdown
### BRD-CREDIT-CHECK-001#section-03: Channels

**Current BRD Coverage:**
The BRD lists branch, batch, and API entry points for the Credit Check function.

**Evidence Basis:**
- `EV-CREDIT-012`: Flow trigger context
- `EV-CREDIT-018`: SME BAU note

**Question for SME:**
> Are these all channels that can start or consume Credit Check, or is any
> channel missing?

**SME Answer:**

(Space for response)
```

---

### 1. Open TBDs (`TBD-*`)

**Purpose:** Collect SME judgment on unresolved questions or ambiguities.

**Characteristics:**
- Artifact explicitly marks item as `TBD-*` (open question)
- Business intent is unclear, contradicted, or missing
- Current status: `open`, `blocking`, or `non_blocking` (per artifact)

**Questions to Ask:**
- "Can you clarify [what we don't understand]?"
- "Is the system supposed to [claim], or is this a bug?"
- "Do we need to resolve this before moving forward, or can it wait?"

**SME Outcomes:**
- `confirmed`: SME provides clear answer; item is resolved
- `marked_blocking`: SME confirms this blocks downstream work
- `marked_non_blocking`: SME confirms this can be deferred
- `deferred`: SME cannot decide now; needs more time/data/stakeholder input
- `split_into_follow_ups`: Item is more complex; break into sub-questions

**Recording in Question Pack:**
```markdown
### TBD-CREDIT-004: Validation Against Blacklist or Whitelist

**Context:**  
Customer-account validation occurs before the request can continue. Evidence
shows the validation path, but not whether the business policy is a blocked
customer list or an approved customer list.

**Question for SME:**  
> Is customer-account validation based on a blocked-customer list, an
> approved-customer list, or another policy?

**SME Answer:**

(Space for response)
```

---

### 2. Inferred Business Rules (`BR-*` seeds)

**Purpose:** Validate inferred business rules before promoting them to approved
status.

**Characteristics:**
- Artifact includes `BR-*` with status `draft` or `needs_sme_review`
- Rule is inferred from code, data, behavior, or context
- Has linked evidence, but confidence may be medium or low

**Questions to Ask:**
- "We inferred from [evidence]: [rule]. Is this correct?"
- "Should we refine this rule, or does it match your understanding?"
- "Any edge cases or exceptions to this rule?"

**SME Outcomes:**
- `confirmed`: SME agrees with rule as stated
- `rejected`: SME disagrees; rule does not reflect business intent
- `rejected`: Rule is wrong or incomplete; record SME correction in
  `suggested_revision`
- `deferred`: SME needs to consult with others before confirming

**Recording in Question Pack:**
```markdown
### BR-CREDIT-003: Interest Compounding

**Rule Statement:**  
> Interest is compounded daily on unpaid balances.

**Evidence Basis:**
- `EV-CREDIT-012`: Control table extract (strength: `confirmed_from_code`)
- `EV-CREDIT-015`: Sample calculation showing daily compounding (strength: `observed_in_runtime`)

**Current Status:** `draft`

**Question for SME:**  
> Does interest actually compound daily on all unpaid balances?

**SME Answer:**

(Space for response)
```

---

### 3. Contradictions

**Purpose:** Resolve conflicting evidence or behavior claims.

**Characteristics:**
- Two or more evidence items or behaviors appear to contradict
- Example: two programs implement the same logic differently
- Unclear which is correct, when each applies, or if both are valid

**Questions to Ask:**
- "Which is the intended behavior, or when does each apply?"
- "Is one of these a bug, or are they both correct under different conditions?"
- "Should we keep both behaviors or standardize on one?"

**SME Outcomes:**
- `confirmed`: SME chooses one as correct; other is error/legacy/deprecated
- `confirmed`: Both are valid under different conditions; record the SME's
  conditions in the decision notes
- `split_into_follow_ups`: Contradiction is complex; break into smaller questions
- `deferred`: Need more evidence before SME can decide

**Recording in Question Pack:**
```markdown
### FIND-CREDIT-001: Rounding in Credit Programs

**Position A (from evidence):**  
> CREDITPGM rounds unpaid balances to nearest cent  
> Evidence: `EV-CREDIT-020` (source code, strength: `confirmed_from_code`)

**Position B (from evidence):**  
> REPORTPGM truncates (does not round) balances  
> Evidence: `EV-CREDIT-021` (source code, strength: `confirmed_from_code`)

**Question for SME:**  
> These two programs implement rounding differently. Which is the correct business behavior?

**SME Answer:**

(Space for response)
```

---

### 4. Behavior Confirmations (`BEH-*`)

**Purpose:** Verify that observed behavior is intentional, not a bug or
workaround.

**Characteristics:**
- Item represents observed behavior (from logs, runtime, execution)
- Behavior is implemented, but we don't know if it's intentional
- Artifact includes `BEH-*` with status and evidence

**Questions to Ask:**
- "We observed [behavior]. Is this the intended system behavior?"
- "Is this a known issue, or is this how the system is supposed to work?"
- "Is this a legacy workaround we should preserve or fix?"

**SME Outcomes:**
- `confirmed`: Behavior is intentional and correct
- `rejected`: Behavior is a bug; system should work differently
- `confirmed`: Behavior is correct under specific conditions; record the
  conditions in decision notes
- `deferred`: Need more context before SME can confirm

**Recording in Question Pack:**
```markdown
### BEH-CREDIT-006: Transaction Blocking When Limit Exceeded

**Claim:**  
> When a customer's balance exceeds their credit limit, the system blocks any
> new transactions.

**Evidence:**
- `EV-CREDIT-015`: Job log showing "TRANSACTION BLOCKED - LIMIT EXCEEDED"
- `EV-CREDIT-008`: CREDCHK source code excerpt with limit-check logic

**Question for SME:**  
> We observed that transactions are blocked when the credit limit is exceeded.
> Is this the intended system behavior, or a known issue?

**SME Answer:**

(Space for response)
```

---

### 5. Modernization Decisions (`DEC-*`)

**Purpose:** Get SME acceptance or feedback on target-system design choices.

**Characteristics:**
- Represents a modernization choice (not legacy behavior)
- Example: "In the new system, we will use real-time processing instead of batch"
- SME approval is required before advancing to SDD handoff

**Questions to Ask:**
- "We propose [decision]. Does this align with your business goals?"
- "Any concerns or conditions on this approach?"
- "Are there exceptions or edge cases we should handle differently?"

**SME Outcomes:**
- `confirmed`: SME accepts decision
- `rejected`: SME does not accept; prefers different approach
- `confirmed`: SME accepts with explicit conditions; record conditions in
  decision notes and sign-off conditions
- `deferred`: Decision requires stakeholder input beyond SME

**Recording in Question Pack:**
```markdown
### DEC-CREDIT-001: Credit Check Timing (Batch vs. Real-Time)

**Decision Statement:**  
> In the modernized system, we will implement real-time credit checks
> (validate on each transaction) instead of batch validation.

**Rationale:**  
Current batch process causes delays and sometimes allows transactions above the limit
before the daily check. Real-time validation would eliminate this risk.

**Tradeoff:**  
Real-time is more responsive but requires stronger integration with the transaction
system. Batch is simpler but less responsive.

**Question for SME:**  
> Does this real-time approach align with your business goals? Any concerns?

**SME Answer:**

(Space for response)
```

---

### 6. Validation Scenario Seeds (`VAL-*`)

**Purpose:** Confirm whether BRD-stage validation scenario seeds are useful,
accurate, and ready to feed acceptance criteria, golden master planning, or SOW
scope discussion.

**Characteristics:**
- Item represents a review scenario, not a formal `TC-*` test case
- Scenario links to existing `BR-*`, `BEH-*`, and `EV-*`
- Scenario may be `ready_for_spec`, `needs_sme_review`, or
  `needs_runtime_evidence`

**Questions to Ask:**
- "Is this a valid business scenario for reviewing the BRD?"
- "Should this become an acceptance-criteria candidate, golden-master
  candidate, SOW scope note, or be deferred?"
- "What evidence is missing before this can become a formal test case?"

**SME Outcomes:**
- `confirmed`: Scenario is valid and can feed downstream planning
- `rejected`: Scenario is not meaningful for this capability
- `needs_more_evidence`: Scenario is valid but needs runtime/sample evidence
- `deferred`: Scenario depends on another owner or later scope decision
- `split_into_follow_ups`: Scenario should be split into smaller cases

**Recording in Question Pack:**
```markdown
### VAL-CREDIT-004: Order Amount Equals Credit Limit

**Scenario Summary:**
> Confirm the inclusive/exclusive boundary for the credit limit comparison.

**Related BR/BEH:** `BR-CREDIT-LIMIT-001`, `BEH-CREDIT-LIMIT-001`
**Evidence:** `EV-CREDIT-LIMIT-001`
**AI Suggested Decision:** `needs_sme_review`

**Question for SME:**
> If order amount equals credit limit, is the order allowed, rejected, or
> conditionally allowed?

**SME Answer:**

(Space for response)
```

---

### 6. Evidence Strength Assessment

**Purpose:** Validate that evidence strength assessment is accurate before
downstream skills rely on rules tied to that evidence.

**Characteristics:**
- Evidence is weak, contradictory, or insufficient to approve a rule
- Confidence level is medium or low
- Rule confirmation or downstream promotion depends on additional evidence

**Questions to Ask:**
- "The evidence for this rule is [weak/contradictory]. Do we need more
  evidence before approving it?"
- "Can we proceed with this rule, or should we collect more data?"

**SME Outcomes:**
- `confirmed`: Evidence is sufficient for downstream skills to rely on, subject
  to normal owning-skill approval
- `needs_more_evidence`: More evidence is needed (record what)
- `deferred`: Need to gather evidence; will revisit later

**Recording in Question Pack:**
```markdown
### EV-CREDIT-018: Interest Compounding Threshold

**Current Assessment:**  
- Strength: `weakly_inferred`
- Confidence: `low`
- Evidence is based on one isolated calculation; not confirmed in other sources

**Question for SME:**  
> Before downstream skills rely on a rule about the $10k threshold for interest
> compounding, should we collect more evidence, or is this sufficient?

**SME Answer:**

(Space for response)
```

---

## Organization Strategy

### By Type (Recommended)

Organize the question pack by **type** (not by ID), so the SME answers
questions in a logical flow:

1. **Open TBDs** — what must we understand?
2. **Inferred Rules** — what rules do we think we found?
3. **Contradictions** — where does evidence conflict?
4. **Behavior Confirmations** — are observed behaviors intentional?
5. **Decisions** — do you accept the target-system choices recorded in the
   artifact?
6. **Evidence Assessment** — do we have enough evidence?

**Rationale:** This flow moves from understanding legacy behavior → validating
understanding → proposing new system choices. SME can build context as they
answer.

### By Artifact Section (Not Recommended)

You could organize by the artifact section (e.g., "Questions from BRD Section 2:
Rules"), but this breaks the natural flow of reasoning and may miss questions
from other artifact sections.

### By Priority (Optional)

If the review must be time-boxed, prioritize:
1. **Blocking TBDs** — must be resolved before SDD handoff
2. **Critical inferred rules** — core business logic
3. **Contradictions** — data integrity, reconciliation, calculations
4. **Modernization decisions** — architecture, platform choices
5. **Non-blocking TBDs** — nice-to-know but not blocking

---

## Evidence Strength Reference

When recording evidence in the question pack, include strength so SME understands
the support level for the question:

| Strength | Meaning | SME Consideration |
| --- | --- | --- |
| `confirmed_from_code` | Directly in source code | High confidence; SME should validate intent |
| `observed_in_runtime` | Seen in runtime (logs, spool, transaction) | High confidence; SME should validate if intentional |
| `confirmed_by_sme` | SME has confirmed this previously | Already validated; may not need re-review |
| `strongly_inferred` | Strong inference from multiple sources | Moderate confidence; SME should validate |
| `weakly_inferred` | Plausible but under-supported | Low confidence; SME should confirm or reject |
| `contradictory` | Conflicting evidence exists | SME must choose/clarify |
| `missing` | Required evidence not available | Cannot rely on without additional collection |

---

## Confidence vs. Knowledge Type

Do not confuse confidence level with knowledge type:

| Knowledge Type | Meaning | Example |
| --- | --- | --- |
| `observed_behavior` | The system demonstrably does this | "System blocks transactions over limit" |
| `inferred_business_rule` | Rule inferred from code/data | "Interest compounds daily" |
| `modernization_decision` | Target-system choice | "Use real-time validation" |
| `unknown_tbd` | Evidence missing or contradictory | "Unclear when rounding applies" |

A `high_confidence` `inferred_business_rule` still needs SME validation.  
A `low_confidence` `observed_behavior` might not need SME validation (if the
observation is correct).

---

## Anti-Patterns in Question Phrasing

### ❌ Leading Question

**Wrong:**
```
"It's clear from the code that interest compounds daily, right?"
```

**Right:**
```
"Does interest compound daily on all unpaid balances, or only under certain conditions?"
```

### ❌ Multiple Questions in One

**Wrong:**
```
"Does the system validate against a blacklist or whitelist, and if it's a blacklist,
are there any exceptions?"
```

**Right:**
```
(First question)
"Is customer validation based on a blocked-customer list, an
approved-customer list, or another policy?"

(If SME answers "blacklist", follow up with:)
"Are there any exceptions or edge cases to the blocked-customer policy?"
```

### ❌ Asking SME to Code-Read

**Wrong:**
```
"Looking at CRDJOB, can you explain what lines 50-60 do?"
```

**Right:**
```
"The evidence shows a customer-account validation step before the request can
continue. What business policy is being checked?"
```

### ❌ Collapsing Multiple Artifacts

**Wrong:**
```
"Looking at the BRD, spec, and flow analysis, what do you think about the
overall architecture?"
```

**Right:**
```
(Ask about one specific item:)
"The BRD lists three validation checks. Are all three necessary, or can we
simplify?"
```

---

## Handling Unexpected Responses

### SME Adds New Information

**Situation:** SME's answer reveals a new rule, behavior, or contradiction not
in the artifact.

**Action:**
1. Record SME's answer verbatim
2. Ask follow-up: "Should the artifact owner add a new `BR-*` or `TBD-*` for
   this?"
3. Create a follow-up finding for the artifact owner; the facilitator does not
   mint the new rule ID directly

**Example:**
```yaml
question_posed: "Is customer validation based on a blocked-customer list, an approved-customer list, or another policy?"
sme_answer: |
  Whitelist. But there's also an exception: legacy accounts from before 2010
  are always allowed, blacklist or not.
new_follow_up: "Request artifact owner add a new rule/TBD for legacy account exemption"
```

### SME Disputes Artifact Content

**Situation:** SME says something in the artifact is wrong.

**Action:**
1. Record disagreement verbatim
2. Ask: "Should we revise the artifact?"
3. Mark decision as `rejected` and suggest revision
4. Route to artifact owner for correction

**Example:**
```yaml
item_id: BR-CREDIT-003
decision_outcome: rejected
sme_answer: |
  That's not right. Interest compounds daily only on balances over $10k.
  Below that, it's simple interest.
suggested_revision: |
  Interest is compounded daily only on balances > $10,000;
  simple interest applies to balances $10,000 or less.
```

### SME Defers Part of Question

**Situation:** SME can answer part of the question but not all.

**Action:**
1. Record what SME can answer
2. Defer the rest (mark owner, target date)
3. Create separate follow-up item if needed

**Example:**
```yaml
question_posed: "Does the system enforce the credit limit, and are there any business exceptions to that enforcement?"
sme_answer: |
  Yes, it enforces the limit. The CREDCHK program blocks any transaction over
  the limit. As for whether there are any exceptions, I need to check with
  Operations; will get back to you by EOW.
decision_outcome: deferred
escalation:
  owner: Operations Manager
  reason: "Need to verify if there are any exceptions to limit enforcement"
  target_date: "2026-05-23"
```

---

## Question Quality Checklist

Before sending the question pack to the SME, verify:

- [ ] Every open `TBD-*` in artifact has a corresponding question
- [ ] Every `BR-*` seed has a corresponding question
- [ ] Every contradiction is listed as a question
- [ ] Every behavior claim is listed
- [ ] Every `DEC-*` has a corresponding question
- [ ] Each question is neutral (not leading)
- [ ] Each question cites evidence with strength noted
- [ ] No question assumes an answer
- [ ] No question requires SME to code-read or analyze
- [ ] Each question can be answered in a sentence or two (complex questions are split)
- [ ] Response space is provided below each question

---
