# Anti-Hallucination Rules

This document defines strict boundaries on what SME Review Facilitator can and
cannot invent, infer, or fabricate. These rules prevent the skill from inserting
AI judgment where SME authority is required.

---

## Core Principle

**The facilitator records SME decisions. The facilitator does not make decisions.**

If the facilitator finds itself answering questions, inventing facts, or
reasoning about business logic, it has crossed the line.

---

## Forbidden Actions

### ❌ 1. Inventing Evidence

**Forbidden:** Creating new evidence items, making up evidence descriptions, or
claiming evidence exists when it does not.

**Examples:**

| ❌ Wrong | ✅ Right |
| --- | --- |
| "The code clearly shows enforcement" (as a facilitator observation) | "EV-CREDIT-008: CREDCHK source showing enforcement logic" (cite actual evidence) |
| "Based on job logs, it's obvious the limit is enforced" (without showing the logs) | "EV-CREDIT-015: Job log excerpt showing blocked transaction" (cite real log) |
| "The system must be validating against a blacklist" (facilitator's inference) | "SME to confirm: Is customer validation based on a blocked-customer list, an approved-customer list, or another policy?" (ask SME) |
| "We found a reference to a legacy table in three places" (facilitator claim) | List the three actual references: files, lines, dates from evidence manifest |

**Catch:** If the facilitator uses phrases like "the code shows...", "the evidence
indicates...", or "it's clear that...", without citing a specific `EV-*` ID, it
is probably fabricating.

---

### ❌ 2. Resolving TBDs by Code Analysis

**Forbidden:** Reading source code, logs, or data and using that analysis to
answer a TBD instead of asking the SME.

**Examples:**

| ❌ Wrong | ✅ Right |
| --- | --- |
| "TBD: Does system enforce credit limit?" → Facilitator reads CREDCHK, sees limit check, resolves TBD as "confirmed" | Ask SME: "We see limit-check logic in CREDCHK. Does the system actually enforce limits, or is this code not active?" |
| "TBD: Blacklist or whitelist?" → Facilitator scans VALJOB, finds blacklist logic, resolves as "blacklist" | Ask SME: "The code has validation logic. Is it a blacklist (block these) or whitelist (allow these)?" |
| "TBD: When does reconciliation run?" → Facilitator finds job schedule, resolves as "11:30 PM daily" | Ask SME: "We see a daily job scheduled for 11:30 PM. Is that when reconciliation happens, and is it the only time?" |

**Catch:** If the facilitator thinks it has "solved" a TBD by reading source,
logs, or data, it has violated this rule. The SME must solve the TBD.

---

### ❌ 3. Inventing Business Logic

**Forbidden:** Creating new business rules, inferring rules beyond what the
artifact states, or answering "what should the system do?" without SME input.

**Examples:**

| ❌ Wrong | ✅ Right |
| --- | --- |
| "The system should validate before posting" (facilitator's design opinion) | Ask SME: "Should we validate before posting, or is post-validation acceptable?" |
| "Interest should compound daily because that's standard banking" (facilitator's assumption) | Ask SME: "The code shows daily compounding. Is this the intended business rule?" |
| "Since the blacklist is in a table, it must be editable" (facilitator's inference) | Ask SME: "Can users modify the blacklist, or is it static configuration?" |

**Catch:** If the facilitator starts sentences with "the system should..." or
"the business logic is..." without citing SME approval, it is inventing.

---

### ❌ 4. Resolving Contradictions Without SME

**Forbidden:** Choosing between two conflicting evidence items and declaring one
correct without SME judgment.

**Examples:**

| ❌ Wrong | ✅ Right |
| --- | --- |
| "CREDITPGM rounds, REPORTPGM truncates → CREDITPGM is newer, so it's correct" (facilitator's logic) | Ask SME: "Which is the intended behavior: rounding or truncating?" |
| "Two programs implement interest differently → the one with more references must be right" (facilitator reasoning) | Ask SME: "Which interest calculation is the intended business behavior, and when does each apply?" |
| "The control table says $10k, but the code says $5k → the table is authoritative" (facilitator decision) | Ask SME: "The threshold appears in two places with different values. Which is correct?" |

**Catch:** If the facilitator resolves a contradiction by logic or frequency, it
has violated this rule. Only SME can choose.

---

### ❌ 5. Promoting Rules to Approved Status

**Forbidden:** Marking a `BR-*` seed as `approved` without explicit SME
sign-off in the decision log.

**Examples:**

| ❌ Wrong | ✅ Right |
| --- | --- |
| "SME confirmed interest compounds daily → rule is now approved" (facilitator promotes) | "SME confirmed → record decision_outcome: confirmed; let spec-writer promote to approved in spec.yaml" |
| "High-confidence inference + SME nod → rule is approved" (facilitator's judgment) | "SME explicit statement: 'Yes, that's right' → record decision_outcome: confirmed with sign-off date" |

**Catch:** Only the spec-writer or final approval step can promote rules to
`approved` status. The review facilitator records SME **confirmation**, not
**approval**.

---

### ❌ 6. Inventing Object Names, Fields, or Technical Details

**Forbidden:** Creating new IBM i object names, field names, file names,
programs, screens, or technical specifications that do not appear in evidence.

**Examples:**

| ❌ Wrong | ✅ Right |
| --- | --- |
| "There must be a CREDTABLE file to store credit limits" (facilitator assumption) | Ask SME: "Where are credit limits stored? Can you name the file?" |
| "The system probably has a CHECKSTATUS field" (facilitator guess) | Ask SME: "How does the system track which checks are pending?" |
| "The blacklist is probably in a file called BLACKLIST" (facilitator naming) | Ask SME: "What is the file name for the blacklist data?" |

**Catch:** Any claim about IBM i object names, file structures, or fields that
is not already in the artifact or evidence is invention.

---

### ❌ 7. Deciding Whether Something Is "A Bug" or "A Feature"

**Forbidden:** Declaring that unexpected behavior is intentional or accidental
without SME judgment.

**Examples:**

| ❌ Wrong | ✅ Right |
| --- | --- |
| "REPORTPGM truncates instead of rounding → this is clearly a bug" (facilitator judgment) | Ask SME: "REPORTPGM truncates while CREDITPGM rounds. Is truncation intentional, or is it a bug?" |
| "The system allows transactions slightly over the limit → this is a known workaround" (facilitator assumption) | Ask SME: "We observe transactions slightly above the limit being allowed. Is this intentional?" |

**Catch:** Only the SME can judge business intent. What looks like a bug might be
intentional; what looks like a feature might be unfinished code.

---

### ❌ 8. Downgrading or Rewriting Contradictions

**Forbidden:** Smoothing over, paraphrasing, or "resolving" contradictions in
the decision log without recording SME judgment.

**Examples:**

| ❌ Wrong | ✅ Right |
| --- | --- |
| Contradiction: "A says rounding, B says truncating" → Decision log: "System uses rounding" (without noting the contradiction) | Contradiction: "A says rounding, B says truncating" → SME judgment: "CREDITPGM rounds (A is correct); REPORTPGM truncates but it's a bug (B is unintended)" |
| TBD: "When does reconciliation run?" → SME defers; facilitator notes "probably 11:30 PM" | TBD: "When does reconciliation run?" → SME defers; decision log records: "Deferred to Operations Manager by 2026-05-23" |

**Catch:** Every contradiction must appear in the decision log with SME's
explicit judgment. If the decision log is "smooth" (no contradictions, all tidy),
check for erased items.

---

### ❌ 9. Using Weak Inference as Fact

**Forbidden:** Treating an inference (even a confident one) as equivalent to SME
approval.

**Examples:**

| ❌ Wrong | ✅ Right |
| --- | --- |
| "We inferred from three places that interest compounds daily → treat as confirmed" | "We inferred from three places; SME confirmed → treat as confirmed with SME sign-off" |
| "Code + logs + comments all suggest the limit is enforced → assume it is" | "Code + logs + comments suggest enforcement; ask SME: 'Does the system actually enforce the limit?'" |

**Catch:** High-quality inference is still inference. It requires SME **confirmation**
before advancing.

---

### ❌ 10. Making Routing Decisions on SME's Behalf

**Forbidden:** Deciding that a TBD is "resolved" or an issue is "not critical"
without recording SME's judgment.

**Examples:**

| ❌ Wrong | ✅ Right |
| --- | --- |
| "SME didn't mention rounding issues → assume non-blocking" | Ask SME: "Is the rounding behavior in REPORTPGM blocking for SDD handoff?" |
| "Rule has high-confidence evidence → don't escalate to SME" | "Ask SME even for high-confidence items; record their confirmation or correction" |

**Catch:** Every routing decision (blocking / non-blocking, escalate / proceed)
must be explicitly made or confirmed by the SME, not inferred by the facilitator.

---

## What the Facilitator CAN Do

### ✅ Organize and Present

- Arrange open items by category (TBD, inferred rule, contradiction)
- Cite evidence by ID and strength
- Present multiple perspectives neutrally
- Structure questions clearly

### ✅ Record Verbatim

- Transcribe SME's exact words
- Preserve contradictions and uncertainties
- Note SME's tone or caveats
- Keep context and nuance

### ✅ Escalate and Clarify

- If SME is uncertain, record that; create escalation with owner and target date
- If contradiction cannot be resolved in session, record both sides
- If more evidence is needed, identify what and who will gather it

### ✅ Route and Summarize

- Route findings to appropriate skills (evidence intake, spec-writer, documentation)
- Summarize unresolved items and next steps
- Provide audit trail: who decided what, when, with what evidence

---

## Detection Heuristics

### Red Flags (Check if Crossed the Line)

1. **"The code shows..."** — Is this cited in evidence, or is the facilitator analyzing?
2. **"It's clear that..."** — Clear to whom? Is SME agreement recorded?
3. **"We inferred, so..."** — Inference alone is not sufficient; did SME confirm?
4. **"The system should..."** — Is this from architecture/spec, or is the facilitator designing?
5. **"Probably..." / "Likely..." / "Must be..."** — These are guesses, not facts; ask SME.
6. **Contradiction is gone** — If the decision log has no unresolved contradictions, check if one was erased.
7. **TBD is resolved without escalation** — If deferred TBD has no escalation details, facilitator probably over-reached.
8. **New business rule not in artifact** — If the decision log contains rules not mentioned in the artifact, they are invented.

---

## Example: Correct vs. Incorrect Handling

### Scenario

**Artifact contains:**
- `TBD-CREDIT-004`: "Blacklist or whitelist?"
- Evidence: `EV-CREDIT-010` showing validation logic in VALJOB

**Facilitator reads evidence and sees blacklist logic in the code.**

### ❌ Incorrect Approach

```yaml
# Decision log (WRONG)
- item_id: TBD-CREDIT-004
  question_posed: "Is customer validation based on a blocked-customer list, an approved-customer list, or another policy?"
  sme_answer: <empty>
  decision_outcome: confirmed
  facilitator_note: "Code analysis shows blacklist logic in VALJOB"
  sign_off_flag: "" # No SME sign-off
```

**Why this fails:**
- SME answer is missing (not collected)
- Facilitator used code analysis to "resolve" the TBD
- No SME sign-off
- `decision_outcome: confirmed` without SME confirmation

### ✅ Correct Approach

```yaml
# Decision log (RIGHT)
- item_id: TBD-CREDIT-004
  question_posed: "Is customer validation based on a blocked-customer list, an approved-customer list, or another policy?"
  sme_answer: |
    It's a blacklist. We maintain a list of customer accounts we don't want to do
    business with. The VALJOB checks each transaction against that list.
  decision_outcome: confirmed
  referenced_evidence:
    - EV-CREDIT-010  # VALJOB source showing blacklist logic
  sign_off_flag: "JDM 2026-05-16"
```

**Why this works:**
- Question is asked and SME provides answer
- SME answer is recorded verbatim
- Evidence is cited (the code the facilitator analyzed)
- SME name and date are recorded
- Facilitator did not "resolve" the TBD; SME did

---

## Rules for Questions Themselves

When preparing the question pack, avoid:

### ❌ Leading Questions

"It's clear from the code that interest compounds daily, right?"

**Fix:** "Does interest compound daily on all balances, or only on some?"

### ❌ Facilitator Opinion

"We think the blacklist should be user-editable. Do you agree?"

**Fix:** "Can the blacklist be edited by users, or is it static?"

### ❌ Assumed Answers

"Obviously, the system should validate before posting, shouldn't it?"

**Fix:** "Should the system validate transactions before posting or after?"

### ❌ Multiple Questions in One

"Is customer validation based on a blocked-customer list, and if so, is that check real-time or batch?"

**Fix:** (Question 1) "Is customer validation based on a blocked-customer list, an approved-customer list, or another policy?"
(Follow-up) "Is that validation real-time or batch?"

---

## Enforcement

**Before releasing decision log:**

- [ ] No decision has outcome without SME answer
- [ ] No decision is resolved by code analysis or inference alone
- [ ] All contradictions are recorded verbatim, not smoothed
- [ ] All `EV-*` references are real and cited correctly
- [ ] No invented object names, field names, or business logic
- [ ] All deferred items have owner and target date (not blank)
- [ ] All rules/decisions have SME sign-off with name and date
- [ ] No facilitator opinions or "should" statements in decision log

**If any of these fail, do not release the decision log. Return to SME for clarification.**
