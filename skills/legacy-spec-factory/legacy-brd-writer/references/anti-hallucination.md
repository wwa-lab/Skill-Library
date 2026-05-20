# Anti-Hallucination Rules for BRD Writing

The BRD is the **first business-facing layer** of the modernization pipeline. It
is tempting to "fill in the blanks" or make reasonable-sounding inferences. This
document lists specific traps and how to avoid them.

---

## Core Principle: Ground Truth is Evidence

A claim is only safe to include in the BRD if it traces back to **evidence** (EV-*)
from one of these sources:

1. **Tier 1 (Strong)**: Source code, data structure, runtime behavior
2. **Tier 2 (Strong)**: Named, date-stamped SME confirmation
3. **Higher Tiers** (Weak or Invalid): Comments, field names, inferred naming,
   wikis, prior specs

**If you cannot link a claim to Tier 1 or Tier 2 evidence, it must be a TBD,
not a confident statement in the BRD.**

---

## Hallucination Traps

### 1. Inventing Business Rules from Naming

**Trap:**
```
A field is called `IS_APPROVED`. 
Inference: "The system tracks approval status."
```

**Why it's wrong:**
- The field might always be 'Y' (set once, never read)
- It might be vestigial code (left over from a feature that was never completed)
- The actual approval logic might be elsewhere

**What to do instead:**
1. Check if the field is read in any conditional logic
2. Check if the field is written to or only populated once
3. If the approval logic is unclear, create a TBD-*:
   ```yaml
   id: TBD-<CAPABILITY-SLUG>-001
   category: sme_questions
   statement: "Is IS_APPROVED field actively used for approval decisions, 
              or is it legacy?"
   resolver: SME
   blocking: yes
   ```

---

### 2. Assuming Code Comments Are Accurate

**Trap:**
```
Code has comment: "// Check credit limit"
Inference: "The system enforces credit limits"
Without checking: Does the code actually check? Is it a TODO? Outdated?
```

**Why it's wrong:**
- Comments can be outdated
- Comments can describe intent, not actual behavior
- Comments might say "check X" but code checks "not X"

**What to do instead:**
1. Read the code logic, not the comment
2. If comment contradicts code, mark as TBD-*
3. Cite evidence as `confirmed_from_code` only if you read the actual logic

---

### 3. Assuming Field Names Imply Semantics

**Trap:**
```
Data model has fields: CRDAMT, CRDLIM, CRDSTS
Inference: "Credit amount, credit limit, credit status are tracked"
Without evidence: What do these fields contain? What are their valid values?
```

**Why it's wrong:**
- A field named `CRDAMT` might actually hold "credit account manager ID" (CRDT+A+MT)
- Without seeing the field definition or sample data, you cannot know the meaning
- Abbreviations are ambiguous

**What to do instead:**
1. Check the data definition (DDS, DDL, or DSPFFD output)
2. Check sample transaction data to see real values
3. If meaning is unclear, mark as TBD-* on semantics:
   ```yaml
   id: TBD-<CAPABILITY-SLUG>-002
   category: evidence_gaps
   statement: "Field CRDSTS: Is this credit status (ACTIVE/INACTIVE) 
              or something else?"
   evidence_gap: "Field definition not extracted; sample data ambiguous"
   resolver: SME / Source Owner
   blocking: no (spec-writer can make best-effort guess)
   ```

---

### 4. Assuming All Branches Are Equal

**Trap:**
```
Program has:
  IF error THEN write_error_message
  ELSE continue_processing

Inference: "The system handles errors gracefully"
Without evidence: Are errors common? Do they stop the transaction?
```

**Why it's wrong:**
- An error branch that is never exercised (dead code) is not a rule
- An error that is logged but ignored is different from an error that stops
  processing
- You need runtime evidence or SME confirmation to understand the intent

**What to do instead:**
1. Check if the error branch is reachable (code analysis, test cases, logs)
2. Check what happens after the error (does processing stop?)
3. Ask SME: "Is this error expected? How often does it occur?"
4. If unclear, mark as TBD-*

---

### 5. Inventing Cross-Program Rules from Similar Code

**Trap:**
```
Program A has: IF CRDAMT > CRDLIM THEN REJECT
Program B has: IF CRDAMT > CRDLIM THEN REJECT

Inference: "The company has a universal rule: no orders over credit limit"
Without evidence: Do all programs implement this? Are there exceptions?
```

**Why it's wrong:**
- Similar code in two programs might be coincidence (copy-paste, independent
  implementations)
- A rule needs evidence from multiple perspectives, not just code pattern
  matching
- There might be programs that *skip* this check

**What to do instead:**
1. Check how many programs implement the rule (2/10? 10/10?)
2. Ask SME: "Is this a company-wide policy?"
3. Check if there are documented exceptions
4. If pattern is inconsistent, mark as TBD-*:
   ```yaml
   id: TBD-<CAPABILITY-SLUG>-003
   category: sme_questions
   statement: "Is credit limit enforcement a universal rule applied across 
              all order types, or are there exceptions?"
   evidence: "Programs A and B enforce it; coverage unclear"
   resolver: SME
   blocking: no (can proceed with "most programs enforce it")
   ```

---

### 6. Promoting Unconfirmed Rules to "Approved"

**Trap:**
```
Module analysis lists: BR-CREDIT-CHECK-001 (candidate, needs_sme_review)
BRD synthesis marks it: BR-CREDIT-CHECK-001 (approved)
```

**Why it's wrong:**
- Only the SME can promote a rule to `approved`
- The BRD is an SME *input*, not SME approval
- Prematurely marking a rule as approved skips the validation step

**What to do instead:**
1. Keep all BR-* at status `needs_sme_review` in the BRD
2. Add SME notes field in the BRD for feedback
3. Let the SME (via brd-review.md) confirm each rule
4. Spec-writer handles promotion from `needs_sme_review` → `approved`

---

### 7. Assuming Program Purpose from Name

**Trap:**
```
Program named: PAYMENT-PROCESSOR
Inference: "This program processes all payments"
Without evidence: What types of payments? What is its actual scope?
```

**Why it's wrong:**
- Program names are aspirational or legacy (original intent may have changed)
- A program called PAYMENT-PROCESSOR might only handle refunds, not all payments
- Without reading the program, you don't know its scope

**What to do instead:**
1. Extract program behavior from program analysis, not name
2. Ask SME to clarify program scope if unclear
3. If program scope is ambiguous, mark TBD-*

---

### 8. Inventing Evidence

**Trap:**
```
Module analysis doesn't mention a specific behavior.
BRD author: "This is probably handled in PAYMENT-PROCESSOR, let me note it as 
   BEH-001"
```

**Why it's wrong:**
- You cannot invent evidence that doesn't exist upstream
- BRD consumes module analysis; it doesn't re-analyze programs
- You are creating a false claim with no backing

**What to do instead:**
1. Only extract BEH-* from module analysis, flow analysis, or program analysis
2. If behavior is mentioned but not fully explained, create TBD-*
3. Never claim a behavior without pointing to upstream artifact

---

### 9. Assuming Modernization Decisions Belong in BRD

**Trap:**
```
BRD author: "We should store credit limits in a database table instead of 
   reading from CUSTPF"
```

**Why it's wrong:**
- Modernization decisions (DEC-*) are spec-writer's job, not BRD
- BRD documents *what the system does now*, not *how we'll build it differently*
- Mixing business rules with tech decisions confuses the artifact's purpose

**What to do instead:**
1. Keep BRD focused on observed behaviors and inferred business rules
2. Do NOT include target platform, architecture, or implementation decisions
3. If a decision is implied by the legacy behavior, mark as TBD-* for spec-writer
   to address:
   ```yaml
   id: TBD-<CAPABILITY-SLUG>-004
   category: downstream_handoff_blockers
   statement: "Decision needed: how to modernize credit limit checks from 
              CUSTPF file read to scalable microservice?"
   resolver: Architecture / Spec-writer
   blocking: no (for BRD; blocking for spec-writer)
   ```

---

### 10. Assuming Weak Inferences Are Strong

**Trap:**
```
Module analysis says: BR-CREDIT-CHECK-001 (weakly_inferred)
BRD author marks it: confidence: high
```

**Why it's wrong:**
- Evidence strength is assigned by the evidence itself, not by your confidence
  in the inference
- Marking weak evidence as high confidence masks the uncertainty from the SME
- The SME needs to see weak inferences so they can investigate

**What to do instead:**
1. Mark confidence based on evidence strength, not your judgment
2. If evidence is weak, mark `confidence: low` or `medium`
3. Add SME notes: "Needs clarification — only one code path shows this"
4. The SME can then decide: confirm it or mark as TBD

---

### 11. Hiding TBDs in Prose

**Trap:**
```
BRD prose: "The system probably validates the credit limit in most cases"
```

**Why it's wrong:**
- "Probably" and "most cases" are uncertainty markers that hide from readers
- The SME cannot approve an artifact if TBDs are hidden in prose
- Downstream (spec-writer) doesn't know what to ask about

**What to do instead:**
1. If uncertain, be explicit:
   ```
   The system validates credit limits (BEH-001).
   
   TBD-001: Does this validation apply to all customer types, 
            or only standard customers?
   ```
2. Use structured TBD-* items, not hedging language in prose
3. The SME can then validate or request investigation

---

### 12. Treating SME Silence as Approval

**Trap:**
```
SME doesn't respond to draft BRD.
BRD author: "No feedback means approval; I'll mark it approved"
```

**Why it's wrong:**
- SME silence is not approval
- SME might be busy, might not understand the artifact, might disagree silently
- Approval must be explicit and named

**What to do instead:**
1. BRD must be marked `in_review`, not `approved`, until SME explicitly signs off
2. SME approval must include:
   - SME name / role
   - Date of review
   - Decision (approved / approved_with_non_blocking_tbd / needs_revision / rejected)
3. If SME is unavailable, the BRD is blocked until they engage

---

## Checklist: Before Handing BRD to SME

- [ ] Every BEH-* statement is observable fact (not interpretation)
- [ ] Every BEH-* links to ≥1 EV-* (never invented)
- [ ] Every BR-* abstracts ≥1 BEH-* (never invented beyond module seeds)
- [ ] Every BR-* is marked `needs_sme_review` (never `approved` before SME signs off)
- [ ] Every confidence level matches evidence strength (not your judgment)
- [ ] No acceptance criteria in BRD (that's spec-writer)
- [ ] No modernization decisions in BRD (that's spec-writer)
- [ ] No target platform or architecture in BRD (that's spec-writer)
- [ ] Every uncertain claim is surfaced as TBD-*, not hidden in prose
- [ ] No IBM i facts invented (all programs, fields, files come from upstream)
- [ ] Traceability is complete (every claim traces to evidence)

---

## Escalation: When in Doubt

If you cannot confidently ground a claim in evidence, the safe path is:

1. **Create a TBD-***
   - Category: sme_questions (if only SME can answer)
   - Or: evidence_gaps (if evidence is missing)
2. **Mark as blocking or non-blocking**
   - Blocking: must resolve before BRD is approved
   - Non-blocking: can be carried forward as open question
3. **Assign resolver** (SME, Source Owner, Architecture, etc.)
4. **Let the SME decide** whether to investigate or defer

A BRD with TBDs is better than a BRD with hidden hallucinations.

---

## See Also

- `synthesis-rules.md` — how to do it right
- `SKILL.md` → Anti-Hallucination Rules section
- `docs/evidence-and-knowledge-taxonomy.md` (global)
