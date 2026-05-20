# BRD Review Checklist: Credit Limit Enforcement

**BRD ID:** `BRD-CREDIT-LIMIT-001`  
**Capability Owner (SME):** John Smith (Credit Policy Manager)  
**Review Date:** `2026-05-15`  
**Status:** `approved`

---

## Observed Behaviors

### BEH-CREDIT-LIMIT-001: Order Amount Validation

- [x] **Yes** — accurate, can forward to spec-writer

**Reviewer Notes:**
This is exactly how the system works. CREDIT-CHECK reads the limit from CUSTPF
and rejects orders that exceed it. The implementation is straightforward and
matches business requirement.

---

### BEH-CREDIT-LIMIT-002: Error Rejection Flow

- [x] **Yes** — accurate

**Reviewer Notes:**
Error code 42 is standard for credit limit rejections. Customers see the
"Credit limit exceeded" message. This is correct.

---

### BEH-CREDIT-LIMIT-003: Credit Limit Data Source

- [x] **Yes** — accurate

**Reviewer Notes:**
CUSTPF is the master for credit limits. No caching or override logic in the
production flow.

---

### BEH-CREDIT-LIMIT-004: Transaction Logging

- [x] **Yes** — accurate

**Reviewer Notes:**
All rejections are logged to AUDITPF for compliance and troubleshooting.

---

## Inferred Business Rules

### BR-CREDIT-LIMIT-001: Credit Limit Ceiling

- [x] **Yes** — this is a real business rule; mark for promotion in spec phase

**Reviewer Decision:** `approve`

**Reviewer Notes:**
This is our core policy. No customer order can exceed their credit limit. We
need to preserve this in any modernization.

---

### BR-CREDIT-LIMIT-002: Real-Time Limit Checking

- [x] **Yes** — this is a business rule

**Reviewer Decision:** `approve`

**Reviewer Notes:**
Customers expect immediate feedback. We cannot defer this to batch.

---

### BR-CREDIT-LIMIT-003: Customer Master is Source of Truth

- [x] **Yes** — this is a real business rule (with caveat below)

**Reviewer Decision:** `approve`

**Reviewer Notes:**
CUSTPF is the source of truth at order time. However, I flagged TBD-002
because credit limits ARE updated by a separate workflow. The modernized
system needs to handle credit limit changes. This is a bigger topic for the
architecture team.

---

## Scope & Boundaries

### Is the capability scope correct?

- [x] **Yes** — in_scope and out_of_scope are accurate

**Reviewer Notes:**
The BRD correctly focuses on the credit limit **enforcement** logic, not the
credit limit maintenance workflow. Those are separate capabilities and should
be handled in different specs.

---

### Are there unspoken business rules or BAU procedures not captured?

- [x] **No** — everything material is captured

**Reviewer Notes:**
This is a fairly clean, code-driven capability. No hidden BAU procedures. The
only unclear item is the partial credit scenario, which I flagged in TBD-001.

---

## Open Questions (TBDs)

### Are the TBDs correctly categorized and achievable?

- [x] **All TBDs are valid** — correctly categorized, achievable

**Reviewer Notes:**

- **TBD-001 (Partial Credit)**: Real question, but not blocking. The legacy
  behavior is per-order. Aggregating pending orders across a session would be a
  new product policy decision, not required to preserve current behavior.

- **TBD-002 (Limit Update Cadence)**: This is important for the new system
  design (caching, refresh). Can be deferred to spec-writer.

- **TBD-003 (Customer Not Found)**: Edge case. We rarely hit this in
  production, but spec-writer should know the expected behavior.

---

## Completeness & Handoff Readiness

### Is the BRD ready to forward to the specification phase?

- [x] **Yes** — all facts validated, no silent gaps, spec-writer can proceed

**Readiness Assessment:**

The BRD is accurate and complete. All three BR-* have been confirmed as real
business rules for spec-writer promotion. The three TBDs are legitimate
non-blocking questions that spec-writer may carry forward. No silent gaps.

The BRD gives spec-writer everything needed to design the modern system while
preserving the business intent of credit limit enforcement.

---

## Final Decision

**Current Status:** `in_review`

**Final Status:**

- [x] `approved` — Forward to spec-writer with confidence

**Non-Blocking TBDs:** TBD-001, TBD-002, TBD-003

---

## Sign-Off

**Capability Owner (SME):**

- **Name:** John Smith
- **Role:** Credit Policy Manager
- **Date:** `2026-05-15`
- **Signature / Approval:** Electronically signed (john.smith@company.com)

**Author/Synthesizer:**

- **Name:** Claude Code
- **Date:** `2026-05-15`

---

## Next Steps

**Forward to spec-writer:**
- The BRD is approved and ready to drive the specification
- Spec-writer may promote BR-CREDIT-LIMIT-001/002/003 from
  `needs_sme_review` to `approved`
- Spec-writer will generate acceptance criteria for each rule
- Spec-writer may carry TBD-001, TBD-002, and TBD-003 as non-blocking open
  questions in the spec
- Modernized system must preserve the three confirmed business rules
