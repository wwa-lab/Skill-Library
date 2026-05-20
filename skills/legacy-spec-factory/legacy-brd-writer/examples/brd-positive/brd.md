# Business Requirements Document: Credit Limit Enforcement

**Document ID:** `BRD-CREDIT-LIMIT-001`  
**Capability ID:** `CAP-CREDIT-LIMIT-001`  
**Module ID:** `MODULE-CARD-AUTH-001`  
**Module Analysis Source:** `04_modules/card-auth/`  
**Status:** `approved`  
**Owner:** John Smith (Credit Policy Manager)  
**Created:** `2026-05-15`  
**Last Updated:** `2026-05-15`

---

## 1. Capability Overview

### Scope Statement

**In Scope:**
- Credit limit validation for online and phone orders
- Rejection of orders that exceed customer credit limit
- Error messaging and transaction logging

**Out of Scope:**
- Cash/check orders (no credit limit applies)
- Internal admin overrides
- Credit limit modification or adjustment workflows

### Business Owner

- **Name / Role:** John Smith, Credit Policy Manager
- **Contact:** john.smith@company.com

### Business Value

Credit limit enforcement prevents credit exposure on orders. This capability
protects the company's financial position by ensuring no customer exceeds their
authorized credit threshold.

---

## 2. Observed Behaviors

### BEH-CREDIT-LIMIT-001: Order Amount Validation

**Statement:** When an order is submitted with a credit amount, the system
compares the credit amount against the customer's authorized credit limit
retrieved from the CUSTPF (Customer Master File). If the order amount exceeds
the limit, the system rejects the order and returns error code 42.

**Evidence:** `EV-CREDIT-LIMIT-001` (program analysis section 3.2)

**Knowledge Type:** `observed_behavior`  
**Confidence:** `high`

---

### BEH-CREDIT-LIMIT-002: Error Rejection Flow

**Statement:** When an order is rejected due to credit limit (error code 42),
the CREDIT-CHECK program writes an error message to the response field ERRMSG
("Credit limit exceeded") and returns control to the caller with return code 42.
The order is not placed.

**Evidence:** `EV-CREDIT-LIMIT-002` (program analysis section 4.1), `EV-CREDIT-LIMIT-003`
(spool sample showing rejection)

**Knowledge Type:** `observed_behavior`  
**Confidence:** `high`

---

### BEH-CREDIT-LIMIT-003: Credit Limit Data Source

**Statement:** The customer's credit limit is read from the CUSTPF physical
file using the customer ID as the key. The CRDLIM field (numeric, 9 digits, 2
decimal places) is extracted. If the customer record is not found, the program
returns error code 99 (customer not found).

**Evidence:** `EV-CREDIT-LIMIT-004` (program analysis section 5.0 - data
dependency mapping)

**Knowledge Type:** `observed_behavior`  
**Confidence:** `high`

---

### BEH-CREDIT-LIMIT-004: Transaction Logging

**Statement:** When a credit limit rejection occurs (error code 42), the system
writes a log entry to the transaction audit file AUDITPF including: timestamp,
customer ID, order amount, credit limit, and return code.

**Evidence:** `EV-CREDIT-LIMIT-005` (program analysis section 6.2 - audit logging)

**Knowledge Type:** `observed_behavior`  
**Confidence:** `high`

---

## 3. Inferred Business Rules

### BR-CREDIT-LIMIT-001: Credit Limit Ceiling

**Statement:** No order with credit amount can exceed the customer's authorized
credit limit as stored in the customer master file.

**Rationale:** Inferred from BEH-CREDIT-LIMIT-001, BEH-CREDIT-LIMIT-003, and
BEH-CREDIT-LIMIT-004. The control logic, data source, and audit trail all
enforce this single policy.

**Evidence:** `EV-CREDIT-LIMIT-001`, `EV-CREDIT-LIMIT-004`, `EV-CREDIT-LIMIT-005`

**Knowledge Type:** `inferred_business_rule`  
**Confidence:** `high`  
**Review Status:** `needs_sme_review`  
**SME Decision:** `confirmed_for_spec_promotion`

**SME Notes:** ✓ Confirmed by John Smith (2026-05-15). This is the core company
policy. Applies to all order channels (online, phone). No exceptions in the
approval workflow.

---

### BR-CREDIT-LIMIT-002: Real-Time Limit Checking

**Statement:** Credit limit validation occurs at order submission time, not
deferred to a batch process. The system must return accept/reject immediately
to the caller.

**Rationale:** Inferred from BEH-CREDIT-LIMIT-001 and BEH-CREDIT-LIMIT-002. The
program checks and rejects in the same transaction. No batch processing is
evident.

**Evidence:** `EV-CREDIT-LIMIT-001`, `EV-CREDIT-LIMIT-002`

**Knowledge Type:** `inferred_business_rule`  
**Confidence:** `high`  
**Review Status:** `needs_sme_review`  
**SME Decision:** `confirmed_for_spec_promotion`

**SME Notes:** ✓ Confirmed. Customers expect immediate response to credit
checks. No batch deferral.

---

### BR-CREDIT-LIMIT-003: Customer Master is Source of Truth

**Statement:** The authorized credit limit for each customer is the value
stored in the CUSTPF (Customer Master File). This value is the authoritative
source and is never overridden by order-level settings or cached values.

**Rationale:** Inferred from BEH-CREDIT-LIMIT-003. Every credit check reads
from CUSTPF directly; no caching logic is evident in the program flow.

**Evidence:** `EV-CREDIT-LIMIT-004`

**Knowledge Type:** `inferred_business_rule`  
**Confidence:** `medium`  
**Review Status:** `needs_sme_review`  
**SME Decision:** `confirmed_for_spec_promotion`

**SME Notes:** Confirmed with caveat: CUSTPF is the master at order time.
However, credit limits can be updated by a separate workflow (out of scope).
TBD-002 covers this.

---

## 4. Open Questions & Gaps (TBDs)

### TBD-CREDIT-LIMIT-001: Partial Credit Scenarios

**Category:** `sme_questions`  
**Statement:** If a customer has a credit limit of $1,000 and orders $900, can
a second $200 order be placed in the same session, or is the limit checked
against total pending orders?

**Evidence:** No behavior observed in the program for multi-order sessions.
Unclear if CREDIT-CHECK knows about prior orders.

**Resolver:** `SME (John Smith)`  
**Blocking:** `no` (not required to preserve current per-order legacy behavior)

**Context:** SME confirmed the legacy behavior is per-order. Aggregate pending
order exposure is a possible future policy decision, not a blocker for
preserving the current capability.

---

### TBD-CREDIT-LIMIT-002: Credit Limit Update Cadence

**Category:** `sme_questions`  
**Statement:** How frequently is the CUSTPF credit limit updated? What is the
expected latency between a credit limit change and its visibility to the
CREDIT-CHECK program?

**Evidence:** Module analysis does not cover credit limit maintenance workflows
(out of scope for CARD-AUTH module).

**Resolver:** `SME (John Smith)` or `Architecture`  
**Blocking:** `no` (non-blocking for BRD; may be important for spec-writer)

**Context:** Affects decision on caching, refresh intervals, or eventual
consistency in modernized design.

---

### TBD-CREDIT-LIMIT-003: Customer-Not-Found Handling

**Category:** `sme_questions`  
**Statement:** When a customer ID is not found in CUSTPF (error code 99), is
this an error condition that rejects the order, or does the system allow the
order with a fallback behavior?

**Evidence:** Program returns error code 99, but BRD does not clarify whether
this results in order rejection or a different flow.

**Resolver:** `SME (John Smith)`  
**Blocking:** `no` (non-blocking for BRD; spec-writer can address)

**Context:** Edge case for error handling in modernized system.

---

## 5. Evidence Index

| ID | Source | Type | Sensitivity | Strength | Notes |
| --- | --- | --- | --- | --- | --- |
| `EV-CREDIT-LIMIT-001` | `program-analysis-CREDIT-CHECK-001.md`, section 3.2 | program analysis | `public` | `confirmed_from_code` | Control flow IF CRDAMT > CRDLIM |
| `EV-CREDIT-LIMIT-002` | `program-analysis-CREDIT-CHECK-001.md`, section 4.1 | program analysis | `public` | `confirmed_from_code` | Error return code 42, error message |
| `EV-CREDIT-LIMIT-003` | `evidence/redacted/spool-ORDER-2026-05-10-REJECTED.txt` | spool sample | `redacted` | `observed_in_runtime` | Sample transaction rejection with code 42 |
| `EV-CREDIT-LIMIT-004` | `program-analysis-CREDIT-CHECK-001.md`, section 5.0 | program analysis | `public` | `confirmed_from_code` | CUSTPF key lookup on customer ID |
| `EV-CREDIT-LIMIT-005` | `program-analysis-CREDIT-CHECK-001.md`, section 6.2 | program analysis | `public` | `confirmed_from_code` | Audit log write to AUDITPF |

---

## 6. Traceability Summary

See `traceability.md` for the full cross-reference table.

**Summary:**
- 4 observed behaviors documented
- 3 inferred business rules identified (all confirmed by SME as accurate)
- 3 open questions (0 blocking, 3 non-blocking)
- All claims trace to supporting evidence
- No `sensitivity: unknown` evidence

---

## Appendix: Known Constraints

### Terminology

Terms used as defined by the business:
- **Credit Limit**: Maximum amount a customer is authorized to order on credit
- **CUSTPF**: IBM i Physical File containing customer master data
- **Error Code 42**: Standard code for "credit limit exceeded"

### Scope Notes

This BRD covers the **credit limit enforcement logic** only. It does not cover:
- Credit limit modification workflows
- Customer credit score or risk assessment
- Manual override or exception processes (different module)
- Pricing or discount calculations

### Cross-References to Upstream Artifacts

- Module: `04_modules/card-auth/`
- Program Analysis: `02_programs/program-analysis-CREDIT-CHECK-001.md`
- Flow: `02_flows/flow-CARD-AUTH.md`

---

**Document prepared by:** Claude Code (2026-05-15)  
**Last reviewed by:** John Smith, Credit Policy Manager (2026-05-15, status: approved)
