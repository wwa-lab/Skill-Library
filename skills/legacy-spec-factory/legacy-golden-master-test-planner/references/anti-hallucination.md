<!--
Legacy Spec Factory
Copyright 2026 Leo L Zhang

Original author: Leo L Zhang
License: Apache License 2.0

This skill is part of the Legacy Spec Factory project.
Retain this notice in substantial copies or derived versions.
-->

# Anti-Hallucination Rules for Golden Master Test Planning

The golden master test planner bridges approved legacy specs and redacted
runtime evidence. The temptation to invent sample data, fill gaps with
guesswork, or claim equivalence without proof is high. Discipline is essential.

## Core Rule: No Invention

**Every test case input and expected output must be grounded in redacted,
approved evidence.**

- **Inputs:** Cite redacted sample data from the evidence manifest.
- **Expected outputs:** Cite observed legacy outputs from redacted spool,
  report, log, or DB snapshot.
- **Comparison rules:** Base on the spec's acceptance criteria or SME-approved
  tolerance.

**Do NOT:**

- Create a hypothetical transaction value because it's "a typical case"
- Infer what the legacy system outputs by reading the spec
- Guess at field lengths, null behavior, or rounding
- Assume a comparison rule because it "sounds right"

**Instead:**

- If sample data is missing, mark it as a blocking finding and stop.
- If expected output is not observed, request runtime evidence collection.
- If comparison rule is unclear, escalate to SME or defer the test case.

## Forbidden Invention Categories

### 1. Sample Transaction Data

**WRONG:**
```yaml
test_case:
  id: TC-CREDIT-CHECK-001
  inputs:
    customer_id: 98765  # hypothetical "typical customer"
    credit_limit: 5000  # made up number
    request_amount: 3000  # plausible estimate
```

**RIGHT:**
```yaml
test_case:
  id: TC-CREDIT-CHECK-001
  input_refs:
    - evidence_id: EV-CREDIT-CHECK-001
      redacted_sample_ref: "07_runtime-evidence/sample-transactions/cust-98765-auth.json"
      notes: "Actual redacted transaction from production log 2025-04-15"
```

### 2. Expected Outputs

**WRONG:**
```yaml
test_case:
  id: TC-CREDIT-CHECK-002
  expected_output:
    status: APPROVED  # inferred from the business rule
    amount_approved: 3000  # guessed based on input
    reason: "Within credit limit"  # made up
```

**RIGHT:**
```yaml
test_case:
  id: TC-CREDIT-CHECK-002
  expected_output_refs:
    - evidence_id: EV-CREDIT-CHECK-002
      artifact_ref: "07_runtime-evidence/auth-responses/cust-98765-approved.txt"
      assertion: "Legacy system returned approval with amount 3000"
      source: "Job log from 2025-04-15 15:30:00 UTC"
```

### 3. Field Semantics

**WRONG:**
```
"The approval_date field is YYYY-MM-DD because that makes sense"
```

**RIGHT:**
```
"The approval_date field in the redacted evidence sample is formatted as
YYYY-MM-DD. Legacy system field APPDAT is 8 bytes (YYYYMMDD). Evidence
shows the conversion during redaction."
```

### 4. Comparison Tolerances

**WRONG:**
```yaml
test_case:
  id: TC-INTEREST-CALC-001
  comparison:
    mode: tolerant
    tolerance: +/-0.01  # seems reasonable
```

**RIGHT:**
```yaml
test_case:
  id: TC-INTEREST-CALC-001
  comparison:
    mode: tolerant
    tolerance: +/-0.01
    justification: "Legacy spec section 3.2.1 names rounding rules;
      evidence shows variance in third decimal place due to BCD vs IEEE."
    sme_approval: "Capability owner approved tolerance 2025-05-16"
```

### 5. Edge Case Values

**WRONG:**
```
"Also test with zero amount because that's an edge case"
(without evidence showing the legacy system accepting zero)
```

**RIGHT:**
```
"Test with zero amount: EV-CREDIT-CHECK-003 from 2025-04-18 shows
legacy system received a $0.00 refund request and returned APPROVED."
```

### 6. Missing Scenarios

**WRONG:**
```
"Test will also cover error handling because the spec mentions it"
(without evidence showing what the error looks like)
```

**RIGHT:**
```yaml
test_case:
  id: TC-CREDIT-CHECK-ERR-001
  title: "Insufficient Credit Limit"
  input_refs:
    - evidence_id: EV-CREDIT-CHECK-004
  expected_output_refs:
    - evidence_id: EV-CREDIT-CHECK-005
      artifact_ref: "07_runtime-evidence/auth-responses/rejection-001.txt"
  OR:
  blocking_finding: FIND-CREDIT-CHECK-001
    title: "No runtime evidence for insufficient-credit error path"
    resolver: "Test data team"
```

## Relationship to Spec vs. Evidence

**The spec says:** Business rule BR-CREDIT-CHECK-001 requires approval when
amount < limit.

**But** we must also have runtime evidence that shows:
- The legacy system actually implements this rule
- An actual sample transaction that exercises it
- The actual legacy output for that sample

If evidence is missing, we do not invent a test case. We mark a finding.

## Three Classes of Claims

### Class A: Observed (Strongest)

"The legacy system output shows field X = value Y"

- Source: Redacted spool, job log, DB snapshot, screen capture
- Validation: Compare against spec's acceptance criteria
- Acceptable as: Expected outputs, actual behavior
- Status: Ready for test plan without SME re-validation (if evidence is
  already approved for agent use)

### Class B: Inferred from Evidence (Weaker)

"Evidence strongly suggests the system behaves like this"

- Source: Multiple evidence points (e.g., code inspection + job log)
- Validation: Must be cross-checked with SME
- Acceptable as: Comparison rule guidance, not expected outputs
- Status: Requires SME approval before test plan acceptance

### Class C: Inferred from Spec (Weakest)

"The business rule implies the system should behave like this"

- Source: Reading the spec, not observing legacy
- Validation: Not acceptable without runtime evidence
- Acceptable as: Nothing in golden master tests
- Status: Halt; request runtime evidence or defer test case

**In this skill, only Class A and approved Class B claims are allowed in test
plans. Class C claims are marked as findings and blocked.**

## Blocked Findings

If you find yourself about to invent:

1. **Stop immediately.**
2. **Document the gap as a `FIND-*` or `TBD-*` finding.**
3. **Name the resolver** (evidence team, test data owner, SME, spec writer).
4. **Mark the finding as blocking** if it affects business-critical coverage.
5. **Do not add placeholder test cases.**

Example:

```yaml
blocking_findings:
  - id: FIND-CREDIT-CHECK-001
    severity: blocking
    layer: evidence
    title: "No redacted runtime evidence for credit-limit-exceeded path"
    related_ids:
      - BR-CREDIT-CHECK-001
      - AC-CREDIT-CHECK-003
    problem: "Acceptance criterion AC-CREDIT-CHECK-003 requires 'rejection
      when credit limit exceeded', but no job log, spool, or DB extract shows
      this scenario."
    required_remediation: "Collect and redact a production transaction that
      triggers the rejection, OR obtain SME-recorded expected output, OR defer
      this AC from golden master testing."
    resolver: "Test data owner"
    downstream_next_step: "legacy-ibmi-evidence-intake"
```

## What to Challenge in Review

When reviewing a test plan, watch for:

- [ ] Test case inputs are cited to evidence, not invented
- [ ] Expected outputs are observed from redacted samples, not inferred
- [ ] Comparison rules are grounded in spec or SME approval
- [ ] Edge cases are covered only when evidence exists
- [ ] Tolerances are justified by spec or evidence, not guesses
- [ ] Field semantics trace back to actual legacy output, not interpretation
- [ ] Missing evidence is marked as findings, not hidden
- [ ] No test case quietly changes an approved business rule
- [ ] No test case assumes target-system behavior

## SME Role in Validation

The capability-owner SME must validate:

- [ ] The selected test cases are representative of real legacy usage
- [ ] Expected outputs (from evidence) match the SME's understanding of what
  the legacy system should do
- [ ] Any inferred comparison rules (Class B) are correct
- [ ] Tolerances are realistic given the legacy implementation
- [ ] Deferrals or gaps are acceptable

The SME is the **control point** for distinguishing real legacy behavior from
invented or misunderstood behavior.

## Common Traps

### Trap 1: "The Spec Says It, So It Must Be Observable"

```
Spec: "Orders with amount >= $10,000 require supervisory approval."
Assumption: "Let's create a test with amount $10,001."
```

**Fix:** Find a redacted transaction where amount was $10,001 or higher and
the legacy system actually processed it. If no evidence exists, mark it as
blocking and stop.

### Trap 2: "The Field Name Implies Meaning"

```
Legacy DB field: APSTTS
Assumption: "This must be approval status. Let's test values 'A', 'R', 'P'."
```

**Fix:** Find actual legacy output showing what values APSTTS contains in
redacted evidence. Do not guess from field names.

### Trap 3: "We Can Infer Tolerance from Industry Standards"

```
Assumption: "Floating-point calculations typically differ by +/-0.0001, so
let's allow that."
```

**Fix:** Show evidence that the legacy system actually differs by that amount.
Or get SME approval of the tolerance. Do not apply industry defaults.

### Trap 4: "The Error Case Must Exist"

```
Spec mentions error: "Customer not found"
Assumption: "Let's plan a test for this even though we have no sample."
```

**Fix:** If no evidence, do not create the test. Mark a blocking finding and
request evidence or SME approval to defer.

## Closure

A test plan is **never complete** if it contains invented data, inferred
outputs, or unjustified tolerances. The review checklist must pass:

- [ ] Every input cites evidence
- [ ] Every expected output is observed
- [ ] Every comparison rule is justified
- [ ] Every gap is marked as a finding, not hidden
- [ ] SME has approved the plan's claims
