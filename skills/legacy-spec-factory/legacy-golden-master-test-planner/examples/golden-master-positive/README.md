<!--
Legacy Spec Factory
Copyright 2026 Leo L Zhang

Original author: Leo L Zhang
License: Apache License 2.0

This skill is part of the Legacy Spec Factory project.
Retain this notice in substantial copies or derived versions.
-->

# Golden Master Test Plan: Positive Example

This directory contains an **approved golden master test plan** for the
Credit Limit Enforcement capability.

## Contents

- `golden-master-tests.yaml` - canonical machine-readable test plan
- `golden-master-tests.md` - human-readable test plan
- `equivalence-coverage.md` - BR/AC/EV to TC coverage matrix
- `sample-data-manifest.md` - redacted sample and expected-output references
- `test-plan-review.md` - review checklist, findings, and SME sign-off

## What This Example Shows

1. **Complete coverage:** Every business-critical rule has at least one test
   case.
2. **Evidence-backed cases:** Each test case cites redacted, approved runtime
   samples.
3. **Clear comparison rules:** Each case specifies whether comparison is exact,
   normalized, tolerant, or presence-based.
4. **SME approval:** The capability-owner SME has reviewed and approved all
   cases.
5. **No invented data:** All inputs and expected outputs come from redacted
   production evidence.

## Key Patterns

### Pattern 1: Happy Path with Exact Comparison

```yaml
- id: TC-CREDIT-LIMIT-001
  title: "Valid order within credit limit"
  validates:
    - BR-CREDIT-LIMIT-001
    - AC-CREDIT-LIMIT-001
  input_refs:
    - evidence_id: EV-CREDIT-LIMIT-001  # actual redacted txn
  expected_output_refs:
    - evidence_id: EV-CREDIT-LIMIT-002  # actual legacy response
  comparison:
    mode: exact  # legacy amounts must match exactly
```

### Pattern 2: Business Rejection with Presence Check

```yaml
- id: TC-CREDIT-LIMIT-002
  title: "Order rejected: credit limit exceeded"
  validates:
    - BR-CREDIT-LIMIT-002
    - AC-CREDIT-LIMIT-002
  input_refs:
    - evidence_id: EV-CREDIT-LIMIT-003
  expected_output_refs:
    - evidence_id: EV-CREDIT-LIMIT-004
  comparison:
    mode: presence
    assertions:
      - "Response contains 'CREDIT_LIMIT_EXCEEDED'"
```

### Pattern 3: Boundary Case with Normalized IDs

```yaml
- id: TC-CREDIT-LIMIT-003
  title: "Order at exact credit limit"
  validates:
    - AC-CREDIT-LIMIT-003  # boundary condition
  input_refs:
    - evidence_id: EV-CREDIT-LIMIT-005
  expected_output_refs:
    - evidence_id: EV-CREDIT-LIMIT-006
  comparison:
    mode: normalized
    normalization_rules:
      - field: customer_id
        rule: "Map via redaction log"
```

## What NOT to Do (Anti-Patterns)

### Anti-Pattern 1: Invented Test Case

```yaml
# WRONG - no evidence
- id: TC-CREDIT-LIMIT-998
  title: "Order with negative amount"
  inputs:
    amount: -100  # made up; no evidence shows this
```

### Anti-Pattern 2: Inferred Expected Output

```yaml
# WRONG - guessed from spec, not observed
- id: TC-CREDIT-LIMIT-999
  expected_output:
    status: APPROVED  # not from evidence
    reason: "Should succeed per business rule"  # not observed
```

### Anti-Pattern 3: Unjustified Tolerance

```yaml
# WRONG - tolerance without justification
comparison:
  mode: tolerant
  tolerance: +/-0.01  # no spec or evidence backing
```

## SME Approval Record

The test plan is approved when the capability-owner SME signs:

```
Approver: Jane Smith (Credit Card Auth SME)
Date: 2025-05-16
Approved IDs: TC-CREDIT-LIMIT-001, TC-CREDIT-LIMIT-002, TC-CREDIT-LIMIT-003
Deferred: none
Caveats: All comparison rules assume production redaction log dated 2025-05-01
```

## Ready for Handoff

Once approved, this test plan is ready for:

1. **Forward SDLC:** IDs can be copied to the SDD or test-generation harness.
2. **Implementation:** Developers can use the `TC-*` IDs to link their target
   code to legacy expectations.
3. **Test automation:** A test harness can execute legacy and new system with
   the same inputs and compare outputs using the specified comparison rules.

---

For more information, see the skill's main documentation:
`skills/legacy-golden-master-test-planner/SKILL.md`
