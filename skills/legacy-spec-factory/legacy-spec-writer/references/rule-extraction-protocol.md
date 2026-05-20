# Rule Extraction Protocol

Promoting a "capability seed" (a question for SME) to a formal,
approved `BR-*` is the single most dangerous step in the whole skill
family. Bad rule extraction is how modernization projects ship the
wrong business logic.

This document defines a strict protocol the spec-writer must follow.

## The Three Sources of a Business Rule

A BR can only become `approved` when at least one of these is true:

1. **Confirmed from code** — the legacy source explicitly encodes the
   rule (e.g., `IF Amount > CredLimit; return 'D'; endif;`), and SME has
   confirmed the rule is *intended* (not a bug).
2. **Confirmed by SME** — the rule lives in human practice / business
   policy, not necessarily in code, and the SME explicitly confirms it
   in writing.
3. **Strongly inferred + SME approval** — multiple evidence points
   converge on the same conclusion, *and* the SME has reviewed and
   approved the inference.

A BR sourced from "common knowledge" or "obviously" or "industry
standard" without one of the three above **cannot become `approved`** —
it stays `draft` or `needs_sme_review`.

## The Protocol

### Step 1: Collect Candidates

Start from the module overview's "Capability Seeds" section. Each
`CAP-*` seed has 0 or more underlying `BR-*` seeds in its module
View 1 + each constituent flow's `SEED-*`.

For the target capability, collect all candidate BR seeds:
- Every BR-* from module View 1 mapping to this capability
- Every SEED-* from any in-scope flow that has been flagged as a
  rule-candidate (vs. a process-only seed)

### Step 2: For Each Candidate, Classify

| Class | What | Action |
| --- | --- | --- |
| **A. Code-encoded** | Rule is literally in source code as conditional logic | BR draft + SME confirmation needed; usually approvable |
| **B. Operational policy** | Rule exists in human practice (BAU, manual procedure, SOP) | BR draft + SME interview; SME is sole confirmation source |
| **C. Inferred** | Rule is suggested by multiple weak signals (call pattern, field names, comments) but not directly encoded | BR draft + explicit SME review; cannot be approved without SME |
| **D. Speculative** | Rule sounds reasonable but has no direct evidence | Do not create a BR; raise as TBD or discard |

### Step 3: Draft the BR Statement

A BR statement must be:
- **Declarative** (says *what*, not *how*)
- **Testable** (you can write at least one AC for it)
- **Atomic** (one rule per BR; if it conjoins multiple, split)
- **Free of implementation details** (no mention of program names,
  field names, RPGLE-specific constructs — those go in BEH or evidence)

**Good BR:**

> "An authorization request whose amount exceeds the cardholder's
> credit limit must be declined and an audit row written with reason
> 'CREDIT_LIMIT_EXCEEDED'."

**Bad BR (mixes how with what):**

> "Program CU110A calls CREDITCHK which returns 'D' when CREDFILE.CREDLIMIT
> is exceeded."

(That belongs in BEH or evidence summary.)

### Step 4: Link Evidence

Every BR must list `evidence_ids` of:
- Code locations that demonstrate the rule (if Class A)
- SME notes confirming the rule (if Class B)
- Pattern evidence (if Class C — usually multiple EVs)

If `evidence_ids` is empty, the BR is not yet a BR; it's a TBD.

### Step 5: Link BEH

Every BR should also list `linked_behaviors[]` — the factual
observed-behaviors it abstracts. This is what lets you verify the rule
is grounded.

If you cannot find any BEH that the BR abstracts, the rule is purely
prescriptive (Class B), which is fine — just note it explicitly.

### Step 6: Set `confidence`

| Class | Default Confidence |
| --- | --- |
| A. Code-encoded + SME approved | high |
| A. Code-encoded but SME not yet reviewed | medium |
| B. SME-confirmed operational | high (SME is authoritative) |
| C. Inferred + SME approved | medium |
| C. Inferred without SME | low |

### Step 7: Set `review_status`

- `draft` — initial entry, no SME contact yet
- `needs_sme_review` — drafted, SME interview scheduled / pending
- `approved` — SME has signed off with name + date in `spec-review.md`
- `rejected` — SME explicitly rejected the rule as inaccurate
- `retired` — was approved historically but no longer applies

### Step 8: Write the AC (only after BR is approved)

ACs follow BRs. Do not write ACs for `draft` or `needs_sme_review` BRs —
the rule may change. Once `approved`, every BR gets ≥1 AC.

## Examples

### Example: Class A (Code-Encoded)

```yaml
business_rules:
  - id: BR-CARD-AUTH-CREDLIM-001
    knowledge_type: inferred_business_rule
    rule: |
      An authorization request whose amount exceeds the cardholder's
      credit limit must be declined and the decision logged with reason
      'CREDIT_LIMIT_EXCEEDED'.
    evidence_ids:
      - EV-FLOW-ONUS-AUTH-007   # CALLP CREDITCHK + IF Decision='D'
      - EV-PROG-CREDITCHK-003   # source line: IF RequestAmt > CredLimit
      - EV-SME-ANNA-001         # SME confirmation 2026-05-12
    confidence: high
    review_status: approved
    linked_behaviors:
      - BEH-CARD-AUTH-007
      - BEH-CARD-AUTH-009
```

### Example: Class B (SME-Confirmed Only)

```yaml
business_rules:
  - id: BR-CARD-AUTH-OVRRIDE-001
    knowledge_type: inferred_business_rule
    rule: |
      Manual override of a declined authorization requires supervisor
      approval; the supervisor must be a different user from the
      requesting CSR.
    evidence_ids:
      - EV-SME-ANNA-002          # SME interview 2026-05-12, confirmed dual-control rule
    confidence: high
    review_status: approved
    linked_behaviors:
      - BEH-CARD-AUTH-MANUAL-005 # F-key F9 = supervisor approval indicator
```

Note: no code-only evidence — the rule lives in operational practice;
the F-key signal is just the surface.

### Example: Class C (Inferred — Stays Draft Until SME)

```yaml
business_rules:
  - id: BR-CARD-AUTH-CVV-001
    knowledge_type: inferred_business_rule
    rule: |
      CVV / CVC verification is required for all on-us authorization
      requests carrying CVV in the payload.
    evidence_ids:
      - EV-FLOW-ONUS-AUTH-012    # NODE-05 (CU130A) always called
      - EV-PROG-CU130A-001       # internal validation logic
    confidence: medium
    review_status: needs_sme_review
    linked_behaviors:
      - BEH-CARD-AUTH-CVV-001
```

Until SME confirms whether CVV is *required* (vs. just *checked when
present*), this BR is not approved. Therefore no AC is written yet.

### Example: Class D (Speculative — Do Not Create BR)

> "The legacy decline message must be in English."

Source: nothing. Speculation. **Do not create a BR.** Either:
- Discard
- File as TBD if it's a relevant open question

## Common Failure Modes

### Failure 1: Promoting a Class C rule because the spec "looks empty"

If only 3 BRs are confirmed but the SME has gone on vacation, **don't pad
the spec** by promoting Class C inferences. Ship the spec with 3 approved
BRs and the rest in `needs_sme_review`.

### Failure 2: Mixing rule and implementation

"The credit check must use CREDITCHK program" is not a BR — it's a
modernization constraint. If preservation of CREDITCHK as a separate
service is intentional, capture it as a DEC, not a BR.

### Failure 3: Multi-rule conjunction

"Credit limit must be enforced AND audit row written AND response time
< 1s" is three rules. Split.

### Failure 4: Tautological rules

"Authorization must be processed correctly" is not a rule. Define what
"correctly" means or discard.

## The Test

Before approving any BR, ask:

1. Can a developer implement this without asking the SME another question?
2. Can a tester write at least one Gherkin scenario for it?
3. Is there at least one EV that grounds the rule (not just hand-waving)?
4. Has the named capability owner SME approved it in writing?

If any answer is "no", the rule is not yet ready for `approved`.
