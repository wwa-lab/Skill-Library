# Decision Log Rules

This document defines the strict rules for recording decisions in
`sme-decision-log.yaml`. A decision log is the **machine-readable, auditable
record** of SME judgments. It must be:

- **Complete**: every review item has an outcome
- **Accurate**: verbatim SME answers, not paraphrased
- **Traceable**: every decision has SME name, role, and date
- **Structured**: stable IDs, typed outcomes, linked evidence

---

## Mandatory Fields

Every decision entry must have these fields:

```yaml
- item_id: "<stable ID: TBD-*, BR-*, etc.>"
  item_type: "<type: tbd, inferred_rule, behavior_claim, modernization_decision, contradiction>"
  question_posed: "<verbatim question from question pack>"
  sme_answer: "<verbatim SME response>"
  decision_outcome: "<one of: confirmed, rejected, deferred, marked_non_blocking, marked_blocking, split_into_follow_ups, needs_more_evidence>"
  referenced_evidence: ["EV-*", "EV-*"]
  sign_off_flag: "<SME initials + ISO date, or empty if deferred>"
  # OR escalation section if deferred (see below)
```

---

## Field Validation Rules

### `item_id`

**Rule:** Must be a stable ID from the artifact (no invention).

**Valid formats:**
- `TBD-<CAPABILITY>-<NNN>` (three-digit number)
- `BR-<CAPABILITY>-<NNN>`
- `BEH-<CAPABILITY>-<NNN>`
- `DEC-<CAPABILITY>-<NNN>`
- `FIND-<CAPABILITY>-<NNN>` for contradiction or review findings

**Validation:**
- Must exist in the artifact under review
- Capability slug must be consistent across IDs
- Three-digit number must be zero-padded (001, not 1)

**Fail condition:** ID is invented, misspelled, or does not exist in artifact

---

### `item_type`

**Rule:** One of these strings (lowercase):

- `tbd` — Open question or unresolved ambiguity
- `inferred_rule` — Business rule inferred from evidence
- `behavior_claim` — Observed behavior claim
- `modernization_decision` — Target-system design choice
- `contradiction` — Conflicting evidence or behavior

**Validation:**
- Must match the nature of the item
- If `item_id` is `TBD-*`, then `item_type` is `tbd`
- If `item_id` is `BR-*`, then `item_type` is `inferred_rule`
- If `item_id` is `BEH-*`, then `item_type` is `behavior_claim`
- If `item_id` is `DEC-*`, then `item_type` is `modernization_decision`
- If `item_id` is `FIND-*`, then `item_type` is `contradiction` only when the
  source finding category is contradictory evidence; otherwise route it as a
  follow-up finding instead of a decision-log item

**Fail condition:** Type does not match ID prefix and source category

---

### `question_posed`

**Rule:** Verbatim copy of the question from `sme-question-pack.md`.

**Validation:**
- Must match the exact wording in the question pack
- Must be readable and complete (not truncated)
- Must not be edited or paraphrased

**Fail condition:** Question is paraphrased, edited, or does not match question pack

---

### `sme_answer`

**Rule:** Verbatim transcription of the SME's response.

**Validation:**
- Must be the exact words the SME spoke or wrote
- May clean up obvious transcription errors (if SME spoke "wirrite", write "write")
- May add context clarification in square brackets if needed (e.g., "[referring to CREDITPGM]")
- Do not correct grammar, rephrase, or editorialize

**Fail condition:**
- Answer is paraphrased instead of verbatim
- Answer is missing (blank)
- Answer is facilitator's interpretation instead of SME's words

---

### `decision_outcome`

**Rule:** One of these exact strings (lowercase):

| Outcome | Meaning | Use When | Sign-Off? |
| --- | --- | --- | --- |
| `confirmed` | SME agrees with claim or decision | SME confirms the item is correct | YES |
| `rejected` | SME disagrees; item is incorrect | SME says the claim is wrong or misses nuance | YES |
| `deferred` | SME cannot decide now | SME needs more time, data, or stakeholder input | NO (use escalation) |
| `marked_non_blocking` | TBD does not block downstream work | SME says this question is not urgent | YES |
| `marked_blocking` | TBD blocks downstream work | SME says this question must be resolved first | YES |
| `split_into_follow_ups` | Issue is more complex; break into smaller questions | SME's answer reveals multiple sub-questions | NO (list follow-up IDs) |
| `needs_more_evidence` | Cannot decide without additional evidence | SME says we need more data before deciding | NO (specify what evidence is needed) |

**Validation:**
- Must be exactly one of the above (no variations)
- Must match the nature of the SME's response
- If SME says "yes, that's right", outcome is `confirmed` (not "approved")
- If SME says "not quite", outcome is `rejected` (not "needs revision")

**Fail condition:**
- Outcome is a variation (e.g., "confirmled", "not_blocking", "TBD")
- Outcome does not match the SME's response
- Outcome is blank or missing

---

### `sign_off_flag`

**Rule:** SME initials + ISO date, or empty if deferred.

**Format:** `<SME-initials> <YYYY-MM-DD>`

**Examples:**
- `JDM 2026-05-16` (Jane D. Miller, May 16, 2026)
- `AAB 2026-05-17` (Aaron A. Brown, May 17, 2026)

**Validation:**
- Initials should be 2-3 characters (SME's actual initials)
- Date is ISO format (YYYY-MM-DD)
- If outcome is `confirmed`, `rejected`, `marked_non_blocking`, or `marked_blocking`: this field must be filled
- If outcome is `deferred` or `needs_more_evidence`: this field must be empty (use `escalation` instead)

**Fail condition:**
- Sign-off flag is filled but outcome is `deferred`
- Sign-off flag is empty but outcome is `confirmed`
- Date is missing or in wrong format
- Initials are placeholder text (e.g., "[SME-INITIALS]")

---

### `referenced_evidence`

**Rule:** Array of `EV-*` IDs that the SME considered when making the decision.

**Format:**
```yaml
referenced_evidence:
  - EV-<CAPABILITY>-<NNN>
  - EV-<CAPABILITY>-<NNN>
```

**Validation:**
- Every listed `EV-*` must exist in the evidence manifest
- Every listed `EV-*` should appear in the artifact under review
- List the evidence the SME actually referenced, not all possible evidence
- If SME did not mention evidence, list evidence from the artifact that the question was based on

**Fail condition:**
- An `EV-*` ID is invented or does not exist
- An `EV-*` is listed but has `sensitivity: unknown` or `redaction_status: unknown`
- Referenced evidence is missing entirely (blank array)

---

### `escalation` (if deferred)

**Rule:** If outcome is `deferred` or `needs_more_evidence`, include escalation section:

```yaml
escalation:
  reason: "<Why SME could not decide>"
  owner: "<Name or role of person responsible>"
  target_date: "<YYYY-MM-DD when decision is expected>"
  next_step: "<What needs to happen, e.g., 'Gather production logs'>"
```

**Validation:**
- All four fields must be filled
- `reason` explains why SME deferred (e.g., "needs Operations approval", "missing data")
- `owner` is a real person's name or role (not placeholder)
- `target_date` is a future date in ISO format
- `next_step` describes concrete action (not vague like "decide later")

**Fail condition:**
- Escalation is missing but outcome is `deferred`
- Any field is placeholder text or blank
- Target date has passed

---

### `suggested_revision` (if rejected rule)

**Rule:** If outcome is `rejected` and item is a rule (`BR-*`), include suggested revision:

```yaml
suggested_revision: |
  <SME's proposed correction to the rule>
```

**Validation:**
- Only included for rejected rules
- Contains SME's exact revision (not facilitator's)
- Is actionable (spec-writer can use it to update the rule)

**Fail condition:**
- Suggested revision is missing for rejected rule
- Revision is facilitator's invention, not SME's wording

---

## Decision Entry Patterns

### Pattern 1: Confirmed Decision

```yaml
- item_id: "BEH-CREDIT-006"
  item_type: "behavior_claim"
  question_posed: "We observed that transactions are blocked when the credit limit is exceeded. Is this the intended system behavior, or a known issue?"
  sme_answer: "That's the intended behavior. The CREDCHK program enforces the limit strictly."
  decision_outcome: "confirmed"
  referenced_evidence:
    - "EV-CREDIT-015"
    - "EV-CREDIT-008"
  sign_off_flag: "JDM 2026-05-16"
```

---

### Pattern 2: Rejected Decision (Rule)

```yaml
- item_id: "BR-CREDIT-003"
  item_type: "inferred_rule"
  question_posed: "We inferred from the analysis: 'Interest is compounded daily on unpaid balances.' Does this rule accurately reflect business intent?"
  sme_answer: "Not quite. It's compounded daily only if the balance exceeds $10k. Below that, it's simple interest."
  decision_outcome: "rejected"
  referenced_evidence:
    - "EV-CREDIT-012"
  suggested_revision: |
    Interest is compounded daily only on balances > $10,000;
    simple interest applies to balances $10,000 or less.
  sign_off_flag: "JDM 2026-05-16"
```

---

### Pattern 3: Deferred Decision

```yaml
- item_id: "TBD-CREDIT-004"
  item_type: "tbd"
  question_posed: "Is customer validation based on a blocked-customer list, an approved-customer list, or another policy?"
  sme_answer: "I need to check with the Operations team. The business rules were defined before my time, and I want to make sure I give you the right answer."
  decision_outcome: "deferred"
  referenced_evidence: []
  sign_off_flag: ""
  escalation:
    reason: "SME needs to consult with Operations for historical context"
    owner: "Operations Manager (Tom Wilson)"
    target_date: "2026-05-23"
    next_step: "Gather evidence from Operations, update decision log, route to spec-writer"
```

---

### Pattern 4: Marked Non-Blocking TBD

```yaml
- item_id: "TBD-CREDIT-005"
  item_type: "tbd"
  question_posed: "Should we migrate the REPORTPGM rounding bug, or fix it in the new system?"
  sme_answer: "That's not critical to the immediate migration. We can fix it post-launch. It's a cosmetic issue in reports."
  decision_outcome: "marked_non_blocking"
  referenced_evidence:
    - "EV-CREDIT-021"
  sign_off_flag: "JDM 2026-05-16"
```

---

### Pattern 5: Marked Blocking TBD

```yaml
- item_id: "TBD-CREDIT-006"
  item_type: "tbd"
  question_posed: "When does daily reconciliation happen, and who triggers it?"
  sme_answer: "This is critical. The daily reconciliation must happen every night at 11:30 PM, and it's the most important job in the system. If it fails, we have serious compliance issues."
  decision_outcome: "marked_blocking"
  referenced_evidence:
    - "EV-CREDIT-025"
  sign_off_flag: "JDM 2026-05-16"
  escalation:
    reason: "This TBD blocks SDD handoff until we understand the full reconciliation workflow"
    owner: "Finance Team Lead"
    target_date: "2026-05-20"
    next_step: "Provide detailed reconciliation spec with timing, validation rules, and error handling"
```

---

### Pattern 6: Split Into Follow-Ups

```yaml
- item_id: "TBD-CREDIT-007"
  item_type: "tbd"
  question_posed: "How does the system handle credit-limit exceptions?"
  sme_answer: |
    That's actually three separate cases:
    1. Legacy accounts (before 2010) are always allowed
    2. VIP customers have a higher limit
    3. Seasonal patterns require temporary limit adjustments
  decision_outcome: "split_into_follow_ups"
  referenced_evidence:
    - "EV-CREDIT-030"
  sign_off_flag: "JDM 2026-05-16"
  new_follow_up_ids:
    - "TBD-CREDIT-007A"
    - "TBD-CREDIT-007B"
    - "TBD-CREDIT-007C"
```

---

## Metadata Fields

Every decision log must include header fields:

```yaml
review_id: "REVIEW-CREDIT-001"
review_date: "2026-05-16"
artifact_under_review: "05_brds/CREDIT-CHECK/brd.md"
capability_slug: "CREDIT-CHECK"

sme_reviewer:
  name: "Jane D. Miller"
  role: "Accounts Payable Team Lead"
  organization: "Finance Department"
  date: "2026-05-16"

decisions:
  # ... decision entries ...

escalations:
  # ... escalation summary ...

signoff_summary: |
  I, Jane D. Miller, have reviewed the decisions recorded in this log and
  confirm that they accurately reflect my judgments.
  
  Date: 2026-05-16
  Signature: JDM
```

---

## Sign-Off Requirements

The decision log is not valid until signed off by the SME.

**Sign-Off Checklist:**

- [ ] All decisions are recorded with SME name and date
- [ ] All contradictions are recorded verbatim (not resolved by facilitator)
- [ ] All TBDs are marked `blocking` or `non_blocking`
- [ ] All deferred items have owner and target date
- [ ] No invented facts or evidence
- [ ] SME signature (or initials) on `signoff_summary`
- [ ] `signoff_summary` contains explicit approval language

**Example Approval Language:**

> I, [SME name], confirm that all decisions recorded in this log accurately
> reflect my judgment and the business intent. I approve the confirmed
> outcomes for advancement to [next skill].

---

## Validation Checklist

Before releasing the decision log:

- [ ] **Completeness**: Every review item has exactly one decision outcome
- [ ] **Traceability**: Every decision has SME name, role, and ISO date
- [ ] **Accuracy**: Answers are verbatim, not paraphrased
- [ ] **Evidence**: All referenced `EV-*` IDs exist and have valid redaction status
- [ ] **No Fabrication**: No invented facts, evidence, or behavior
- [ ] **No Silence**: Contradictions are recorded, not erased
- [ ] **Escalation**: All deferred items have owner and target date
- [ ] **Sign-Off**: SME has signed off on the log with explicit approval
- [ ] **Routing**: Follow-up findings and next steps are clear

**Fail if:**
- Any decision lacks SME name or date
- Any contradiction is silenced or "resolved" by facilitator
- Any TBD or rule is approved without SME sign-off
- Any `EV-*` reference is broken, has unknown sensitivity, or has unknown
  redaction status
- Sign-off is missing or placeholder text

---
