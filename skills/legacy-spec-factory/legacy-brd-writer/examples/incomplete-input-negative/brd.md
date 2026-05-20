# Business Requirements Document: Order Routing (INCOMPLETE)

**Document ID:** `BRD-ORDER-ROUTING-001`  
**Capability ID:** `CAP-ORDER-ROUTING-001`  
**Module ID:** `MODULE-ORDER-PROCESS-001`  
**Module Analysis Source:** `04_modules/order-process/`  
**Status:** `blocked`  
**Owner:** Sarah Lee (Order Fulfillment Manager)  
**Created:** `2026-05-14`  
**Last Updated:** `2026-05-15`

---

## 1. Capability Overview

### Scope Statement

**In Scope:**
- Order routing to fulfillment centers
- Shipping method selection

**Out of Scope:**
- `<To be confirmed with SME>`

### Business Owner

- **Name / Role:** Sarah Lee, Order Fulfillment Manager
- **Contact:** sarah.lee@company.com

### Business Value

Orders must be routed efficiently to the appropriate fulfillment center to
minimize shipping cost and delivery time.

---

## 2. Observed Behaviors

### BEH-ORDER-ROUTING-001: Fulfillment Center Selection

**Statement:** When an order is submitted, the system determines which
fulfillment center should process the order.

**Evidence:** `EV-ORDER-ROUTING-001` (program analysis section 2.1)

**Knowledge Type:** `observed_behavior`  
**Confidence:** `medium`

**Issue:** The program analysis describes the routine name
(`SELECT-FULFILLMENT-CENTER`) but does not include the actual control flow
logic. See TBD-001.

---

### BEH-ORDER-ROUTING-002: Geographic Assignment

**Statement:** Orders are assigned based on geographic location.

**Evidence:** `EV-ORDER-ROUTING-002` (program analysis section 2.2 - comment
mentions "geographic logic")

**Knowledge Type:** `unknown_tbd`  
**Confidence:** `low`

**Issue:** Only a code comment supports this. No actual logic or data lookup is
documented. See TBD-002.

---

## 3. Inferred Business Rules

### BR-ORDER-ROUTING-001: Fulfillment Center Optimization

**Statement:** The system should assign orders to the fulfillment center that
minimizes total shipping cost and delivery time.

**Rationale:** Inferred from module overview's capability seed and business
context.

**Evidence:** Module BR-* seed; no specific EV support yet.

**Knowledge Type:** `inferred_business_rule`  
**Confidence:** `low`  
**Review Status:** `needs_sme_review`

**SME Notes:** Awaiting SME confirmation — is this a real business rule or an
aspiration?

---

## 4. Open Questions & Gaps (TBDs)

### TBD-ORDER-ROUTING-001: Missing Program Flow Details

**Category:** `evidence_gaps`  
**Statement:** The program analysis for `SELECT-FULFILLMENT-CENTER` routine
only provides a routine name and a comment. The actual control flow logic
(which attributes drive routing? what is the algorithm?) is not extracted.

**Evidence:** `EV-ORDER-ROUTING-001` is incomplete.

**Resolver:** `Program Analyzer` (needs to run detailed analysis)  
**Blocking:** `yes` (cannot write BRD without understanding the logic)

**Context:** This blocks understanding observed behavior. Need either:
1. Detailed program analysis with control flow, or
2. SME confirmation of the routing logic if program is too complex to analyze

---

### TBD-ORDER-ROUTING-002: Geographic Logic Not Evidenced

**Category:** `evidence_gaps`  
**Statement:** The claim that orders are assigned by "geographic location" is
based only on a code comment. No actual geographic lookup logic is visible
(e.g., ZIP code comparison, regional database query).

**Evidence:** Only `EV-ORDER-ROUTING-002` (comment); no logic evidence.

**Resolver:** `Program Analyzer` or `SME`  
**Blocking:** `yes` (cannot claim behavior without code evidence)

**Context:** Either:
1. Program analysis should show the actual geographic lookup logic, or
2. SME should confirm whether geographic assignment is real or a comment error

---

### TBD-ORDER-ROUTING-003: Missing Flow Analysis

**Category:** `missing_inputs`  
**Statement:** Module analysis references flow `flow-ORDER-ROUTING` but no
approved flow analysis has been provided. Without the flow, we cannot
understand cross-program data flow or error handling.

**Evidence:** Module overview cites `FLOW-ORDER-ROUTING-001` but file not found.

**Resolver:** `Flow Analyzer` (needs to complete flow-ORDER-ROUTING.md)  
**Blocking:** `yes` (missing upstream input; BRD cannot proceed)

**Context:** Wait for flow analysis before completing BRD.

---

### TBD-ORDER-ROUTING-004: Shipping Method vs. Fulfillment Center

**Category:** `sme_questions`  
**Statement:** Is "shipping method selection" (in-scope per BRD) the same
routing algorithm as "fulfillment center selection", or are they separate
decisions?

**Evidence:** Scope statement lists shipping method, but BRD behaviors only
mention fulfillment center.

**Resolver:** `SME`  
**Blocking:** `yes` (scope ambiguity)

**Context:** Need SME to clarify scope before BRD can be completed.

---

### TBD-ORDER-ROUTING-005: Performance or Cost Optimization

**Category:** `sme_questions`  
**Statement:** Is the routing rule "minimize cost", "minimize delivery time",
or "balance both"? BR-001 is unclear on the optimization objective.

**Evidence:** BR-001 mentions both; module seed does not specify.

**Resolver:** `SME`  
**Blocking:** `yes` (business rule cannot be approved without clarity)

**Context:** SME must specify the business objective before BRD can move to
approved.

---

## 5. Evidence Index

| ID | Source | Type | Sensitivity | Strength | Notes |
| --- | --- | --- | --- | --- | --- |
| `EV-ORDER-ROUTING-001` | `program-analysis-ORDER-ROUTING-001.md`, section 2.1 | program analysis | `public` | `confirmed_from_code` | Incomplete; only routine name and comment extracted |
| `EV-ORDER-ROUTING-002` | `program-analysis-ORDER-ROUTING-001.md`, section 2.2 | program analysis | `public` | `weakly_inferred` | Code comment only; no logic shown |

---

## 6. Traceability Summary

**Status:** `BLOCKED — cannot proceed to SME review**

**Blocking Issues:**
1. Flow analysis not provided (TBD-003) — missing upstream input
2. Program flow logic not detailed (TBD-001) — insufficient evidence
3. Geographic logic not shown (TBD-002) — comment only, no code evidence
4. Scope ambiguity (TBD-004) — SME must clarify
5. Business rule unclear (TBD-005) — SME must specify optimization objective

**Next Steps:**
1. Obtain approved `flow-ORDER-ROUTING.md` from flow analyzer
2. Request detailed program analysis for `SELECT-FULFILLMENT-CENTER` with
   control flow
3. Escalate to SME to clarify scope and optimization objective
4. Do NOT proceed to SME review until blocking TBDs are resolved

---

**Document prepared by:** Claude Code (2026-05-14)  
**Last reviewed by:** None (blocked before SME review)  
**Status:** `blocked`
