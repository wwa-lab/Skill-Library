# Negative Example: Handoff Blocked on Missing Acceptance Criteria

## Scenario

The **ORDER-ENTRY** module analysis is complete and the specification has been drafted. The Business Requirements Document is approved and signed.

However, during handoff validation, a critical gate fails: **one approved business rule has no linked acceptance criteria.**

The handoff package cannot be generated until this gap is resolved.

## Validation Results

Most gates pass, but one **blocking gate fails**:

| Gate | Status | Notes |
| --- | --- | --- |
| BRD approved and signed | ✅ PASS | Approved by Sarah Chen on 2026-05-14 |
| Spec approved and signed | ✅ PASS | Approved by Sarah Chen on 2026-05-14 |
| No blocking TBDs | ✅ PASS | 2 non-blocking TBDs |
| All rules have AC | ❌ **FAIL** | BR-ORDER-ENTRY-003 has no AC |
| Evidence cleared | ✅ PASS | All evidence is public |
| Traceability complete | 🔶 PARTIAL | BR-003 is orphaned from AC |

## Blocking Finding

**Finding ID**: BR-MISSING-AC  
**Severity**: **BLOCKING**  
**Rule Affected**: BR-ORDER-ENTRY-003  
**Rule Title**: "System must apply promotional discounts during order entry"  
**Issue**: No `acceptance_criteria_ids[]` are linked to this approved business rule

### Details

In the spec's `business_rules[]` array:

```yaml
business_rules:
  - id: BR-ORDER-ENTRY-001
    statement: "Customer must provide valid shipping address"
    review_status: approved
    acceptance_criteria_ids: [AC-ORDER-ENTRY-001, AC-ORDER-ENTRY-002]
  
  - id: BR-ORDER-ENTRY-002
    statement: "System calculates order total including tax"
    review_status: approved
    acceptance_criteria_ids: [AC-ORDER-ENTRY-003]
  
  - id: BR-ORDER-ENTRY-003
    statement: "System must apply promotional discounts during order entry"
    review_status: approved
    acceptance_criteria_ids: []  # ❌ EMPTY!
  
  - id: BR-ORDER-ENTRY-004
    statement: "System logs all order entry events"
    review_status: approved
    acceptance_criteria_ids: [AC-ORDER-ENTRY-004, AC-ORDER-ENTRY-005]
```

### Why This Is Blocking

BR-ORDER-ENTRY-003 is **approved**, which means the SME has confirmed that promotional discount logic is a real requirement. However, **there are no acceptance criteria** that define:

- What promotional discounts apply
- How they are calculated
- When they are offered
- How they are validated
- What the system outputs when a discount applies

Without acceptance criteria, the forward SDLC team **cannot write a test** for this rule. The rule will be implemented, but there is **no way to validate** that it is correct.

## Handoff Decision

**STATUS: BLOCKED**

Handoff cannot proceed until this blocking finding is resolved.

## Required Action

**Route back to `legacy-spec-writer`** to add acceptance criteria for BR-ORDER-ENTRY-003.

### What the Spec Writer Must Do

1. Review the BRD section on promotional discounts
2. Examine the evidence (program analysis, flow analysis, runtime evidence)
3. Understand what the legacy system actually does:
   - Which promotional discounts does it apply?
   - Are discounts automatic or manual?
   - Are they time-based, customer-segment based, or volume-based?
   - Are they applied before or after tax?
4. Create acceptance criteria (AC-*) that specify each requirement
5. Link those acceptance criteria to BR-ORDER-ENTRY-003
6. Update the spec's `business_rules` entry to include the new AC IDs
7. Ensure all new AC have `review_status: approved` from the SME

### Example Acceptance Criteria (to be created)

```yaml
acceptance_criteria:
  - id: AC-ORDER-ENTRY-006
    rule_id: BR-ORDER-ENTRY-003
    criterion: "10% discount applied for orders over $1,000"
    how_to_test: "Submit order with amount $1,100; verify discount of $110 is applied"
    priority: P0
    review_status: approved
  
  - id: AC-ORDER-ENTRY-007
    rule_id: BR-ORDER-ENTRY-003
    criterion: "Discounts are calculated before tax"
    how_to_test: "Verify tax is applied to discounted amount, not original amount"
    priority: P0
    review_status: approved
  
  - id: AC-ORDER-ENTRY-008
    rule_id: BR-ORDER-ENTRY-003
    criterion: "Promo code field is optional"
    how_to_test: "Submit order without promo code; system applies default discounts"
    priority: P1
    review_status: approved
```

## Why This Happens

This is a common oversight when specs are large or when rule extraction and criteria generation are done in separate passes. The SME may have approved the rule ("yes, we do discounts") without realizing that **acceptance criteria were not yet written**.

This is exactly the kind of gap the handoff validation gate is designed to catch **before** handoff, rather than discovering it during code generation.

## Prevention

To prevent this situation:

1. **Spec writer**: After extracting business rules, immediately create a skeleton AC for each rule
2. **SME review**: When reviewing the spec, check the `acceptance_criteria_ids[]` count matches the number of rules
3. **Validation**: Use the BR-HAS-AC gate check before attempting handoff

---

## What Happens If This Gate Is Ignored

If the handoff were forced through without acceptance criteria:

- ❌ Forward SDLC team receives an incomplete requirement
- ❌ Team must invent test criteria (guessing business intent)
- ❌ Promotional discount logic is implemented but may not match legacy behavior
- ❌ Golden master test comparison fails because new behavior is untested
- ❌ Production deployment reveals incorrect discount application
- ❌ Customer complaints; reconciliation effort required

The gate exists to prevent this failure mode.

---

## Recovery Path

1. **Identify** that BR-ORDER-ENTRY-003 needs acceptance criteria
2. **Route** back to `legacy-spec-writer` with this finding
3. **Create** acceptance criteria from:
   - Program analysis (what does ORDENTRY program do?)
   - Flow analysis (how do discounts flow through the order process?)
   - Runtime evidence (sample orders with discounts applied)
4. **SME confirms** the criteria match legacy behavior
5. **Update** spec with new AC IDs
6. **Re-run** the handoff validation gate
7. **Proceed** to handoff once the gate passes

---

## Diagnostic Files

This example includes:

- `README.md` — This explanation
- `blocking-finding.yaml` — Machine-readable finding record produced by the
  blocked run (the only structured output written when the gate fails)

The `sdd-handoff.yaml`, `sdd-handoff.md`, `atlas-context-pack.json`, and
`traceability.md` files are **deliberately absent**. The skill does not emit
a partial or "best effort" handoff package when the gate blocks. Writing
those files would mislead the Atlas SDD chain into believing the capability
was approved.

---

**This blocking finding was generated on 2026-05-15 by Claude Code / legacy-brd-to-sdd-handoff v0.1.0.**

**Status**: ❌ BLOCKED — Awaiting spec writer to add missing acceptance criteria.
