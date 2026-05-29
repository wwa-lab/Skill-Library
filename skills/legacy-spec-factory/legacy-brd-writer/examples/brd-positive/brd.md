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

## 1. Function Purpose

### Purpose Statement

Credit Limit Enforcement checks whether a credit order can proceed without
exceeding the customer's authorized credit threshold.

### Business Value

The function prevents avoidable credit exposure during order intake. It helps
credit policy and operations teams reject over-limit orders before fulfillment
continues.

### Scope Boundary

**In Scope:**
- Credit limit validation for online and phone credit orders
- Immediate rejection when the order amount exceeds the customer's credit limit
- Error messaging and rejection audit logging

**Out of Scope:**
- Cash/check orders
- Credit limit maintenance or adjustment workflows
- Internal admin overrides
- Customer risk scoring

### Scope Clarification Need

None identified from approved inputs. The SME confirmed this BRD is limited to
credit-limit validation during order intake and does not include credit-limit
maintenance or override workflows.

---

## 2. Business Scenarios / Use Cases

| Scenario ID | Business Scenario / Use Case | Primary Actor | Trigger | Business Outcome | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| `SCN-CREDIT-LIMIT-001` | Customer places an order using credit terms | Customer / order-entry channel | Order submitted with credit amount | Order proceeds when within authorized limit | `EV-CREDIT-LIMIT-001`, `EV-CREDIT-LIMIT-004` | `confirmed` |
| `SCN-CREDIT-LIMIT-002` | Customer order exceeds authorized credit limit | Customer / order-entry channel | Order submitted with amount above limit | Order is rejected with credit-limit error | `EV-CREDIT-LIMIT-001`, `EV-CREDIT-LIMIT-002`, `EV-CREDIT-LIMIT-003` | `confirmed` |
| `SCN-CREDIT-LIMIT-003` | Customer record cannot be found | Order-entry channel | Customer ID lookup misses customer master | Program returns customer-not-found code; final business handling needs confirmation | `EV-CREDIT-LIMIT-004` | `needs_sme_review` |

---

## 3. Channels

| Channel ID | Channel / Entry Point | Direction | Business Role | Evidence | Confidence / Status |
| --- | --- | --- | --- | --- | --- |
| `CH-CREDIT-LIMIT-001` | Online order entry | `inbound` | Submits credit orders for immediate limit validation | `EV-CREDIT-LIMIT-001` | `confirmed_by_sme` |
| `CH-CREDIT-LIMIT-002` | Phone order entry | `inbound` | Submits credit orders for immediate limit validation | `EV-CREDIT-LIMIT-001` | `confirmed_by_sme` |
| `CH-CREDIT-LIMIT-003` | Order fulfillment / audit consumers | `outbound` | Consume accept/reject decision and rejection audit trail | `EV-CREDIT-LIMIT-005` | `confirmed_from_code` |

---

## 4. User Interface / User Touchpoints

| Touchpoint ID | Touchpoint Type | Business User / Recipient | Purpose | Evidence | Notes |
| --- | --- | --- | --- | --- | --- |
| `UI-CREDIT-LIMIT-001` | `message` | Order-entry caller / customer-facing channel | Receives error message "Credit limit exceeded" for over-limit rejection | `EV-CREDIT-LIMIT-002`, `EV-CREDIT-LIMIT-003` | Exact customer-facing rendering is handled by the caller |
| `UI-CREDIT-LIMIT-002` | `reporting/audit trail` | Credit policy and operations stakeholders | Review rejected over-limit orders and exposure-control activity | `EV-CREDIT-LIMIT-005` | Audit trail includes customer, amount, limit, timestamp, and return code |

---

## 5. System Interfaces

| Interface ID | System / API / Interface | Direction | Business Purpose | Evidence | Confidence / Status |
| --- | --- | --- | --- | --- | --- |
| `IF-CREDIT-LIMIT-001` | Order-entry caller | `inbound` | Provides customer ID and credit amount for validation | `EV-CREDIT-LIMIT-001` | `confirmed_from_code` |
| `IF-CREDIT-LIMIT-002` | Customer master (`CUSTPF`) | `inbound` | Provides the customer's authorized credit limit | `EV-CREDIT-LIMIT-004` | `confirmed_from_code` |
| `IF-CREDIT-LIMIT-003` | Transaction audit file (`AUDITPF`) | `outbound` | Stores credit-limit rejection records for review | `EV-CREDIT-LIMIT-005` | `confirmed_from_code` |
| `IF-CREDIT-LIMIT-004` | Order fulfillment / downstream consumers | `outbound` | Receive accept/reject decision from the order-entry flow | `EV-CREDIT-LIMIT-002` | `confirmed_from_code` |

---

## 6. Process Flow

### Business Trigger

A customer submits an order using credit terms.

### Current-State Flow

1. The order-entry channel submits customer and credit amount information.
2. The system retrieves the customer's authorized credit limit from the customer
   master record.
3. The system compares the order amount with the authorized credit limit.
4. If the order amount is within limit, the order continues through the caller's
   normal fulfillment path.
5. If the order amount exceeds the limit, the order is rejected immediately with
   a credit-limit error.
6. Rejections are logged so credit policy and operations stakeholders can review
   exposure-control activity.

### Business States

| State | Meaning | Entry Condition | Exit Condition | Evidence |
| --- | --- | --- | --- | --- |
| `Submitted` | Credit order has been received for validation | Customer submits order with credit terms | Customer limit lookup begins | `EV-CREDIT-LIMIT-001` |
| `Limit Retrieved` | Customer authorized credit limit is available | Customer master lookup succeeds | Amount comparison occurs | `EV-CREDIT-LIMIT-004` |
| `Accepted` | Order is allowed to continue | Order amount is within limit | Caller continues fulfillment | `EV-CREDIT-LIMIT-001` |
| `Rejected` | Order is blocked for credit-limit reason | Order amount exceeds limit | Error response and audit log are produced | `EV-CREDIT-LIMIT-002`, `EV-CREDIT-LIMIT-005` |
| `Customer Not Found` | Customer master lookup fails | Customer ID is not found | Program returns error code 99; business handling remains SME question | `EV-CREDIT-LIMIT-004` |

### Business Outcomes and Controls

- **Normal outcome:** The order proceeds only when it is within the customer's
  authorized credit limit.
- **Exception outcome:** The order is rejected with a credit-limit error when
  the amount exceeds the authorized threshold.
- **Control or audit point:** Credit-limit rejections are written to the audit
  file with customer, amount, limit, timestamp, and return code.

---

## 7. Validation Rules

### 7.1 Observed Validation Behaviors

#### BEH-CREDIT-LIMIT-001: Order Amount Validation

**Statement:** When an order is submitted with a credit amount, the system
compares the credit amount against the customer's authorized credit limit
retrieved from the customer master file. If the order amount exceeds the limit,
the system rejects the order and returns error code 42.

**Evidence:** `EV-CREDIT-LIMIT-001` (program analysis section 3.2)

**Knowledge Type:** `observed_behavior`
**Confidence:** `high`

---

#### BEH-CREDIT-LIMIT-002: Error Rejection Flow

**Statement:** When an order is rejected due to credit limit, the program writes
the error message "Credit limit exceeded" to the response field and returns
control to the caller with return code 42. The order is not placed.

**Evidence:** `EV-CREDIT-LIMIT-002` (program analysis section 4.1),
`EV-CREDIT-LIMIT-003` (spool sample showing rejection)

**Knowledge Type:** `observed_behavior`
**Confidence:** `high`

---

#### BEH-CREDIT-LIMIT-003: Credit Limit Data Source

**Statement:** The customer's credit limit is read from the customer master file
using the customer ID as the key. If the customer record is not found, the
program returns error code 99.

**Evidence:** `EV-CREDIT-LIMIT-004` (program analysis section 5.0)

**Knowledge Type:** `observed_behavior`
**Confidence:** `high`

---

#### BEH-CREDIT-LIMIT-004: Transaction Logging

**Statement:** When a credit limit rejection occurs, the system writes a log
entry to the transaction audit file including timestamp, customer ID, order
amount, credit limit, and return code.

**Evidence:** `EV-CREDIT-LIMIT-005` (program analysis section 6.2)

**Knowledge Type:** `observed_behavior`
**Confidence:** `high`

---

### 7.2 Inferred Business Rules

#### BR-CREDIT-LIMIT-001: Credit Limit Ceiling

**Statement:** No order with credit amount can exceed the customer's authorized
credit limit as stored in the customer master file.

**Rationale:** Inferred from `BEH-CREDIT-LIMIT-001`,
`BEH-CREDIT-LIMIT-003`, and `BEH-CREDIT-LIMIT-004`.

**Evidence:** `EV-CREDIT-LIMIT-001`, `EV-CREDIT-LIMIT-004`,
`EV-CREDIT-LIMIT-005`

**Knowledge Type:** `inferred_business_rule`
**Confidence:** `high`
**Review Status:** `needs_sme_review`
**SME Decision:** `confirmed_for_spec_promotion`

**SME Notes:** Confirmed by John Smith (2026-05-15). This is the core company
policy and applies to online and phone order channels.

---

#### BR-CREDIT-LIMIT-002: Real-Time Limit Checking

**Statement:** Credit limit validation occurs at order submission time, not
deferred to a batch process.

**Rationale:** Inferred from `BEH-CREDIT-LIMIT-001` and
`BEH-CREDIT-LIMIT-002`.

**Evidence:** `EV-CREDIT-LIMIT-001`, `EV-CREDIT-LIMIT-002`

**Knowledge Type:** `inferred_business_rule`
**Confidence:** `high`
**Review Status:** `needs_sme_review`
**SME Decision:** `confirmed_for_spec_promotion`

**SME Notes:** Confirmed. Customers expect immediate response to credit checks.

---

#### BR-CREDIT-LIMIT-003: Customer Master is Source of Truth

**Statement:** The authorized credit limit for each customer is the value stored
in the customer master file at order time.

**Rationale:** Inferred from `BEH-CREDIT-LIMIT-003`. Every credit check reads
from the customer master directly; no cache or order-level override is evident.

**Evidence:** `EV-CREDIT-LIMIT-004`

**Knowledge Type:** `inferred_business_rule`
**Confidence:** `medium`
**Review Status:** `needs_sme_review`
**SME Decision:** `confirmed_for_spec_promotion`

**SME Notes:** Confirmed with caveat: credit limits can be updated by a separate
workflow that is out of scope for this BRD.

---

## 8. Error Handling

| Error / Exception ID | Condition | Observed Handling | Business Impact | User/System Response | Evidence | SME Focus |
| --- | --- | --- | --- | --- | --- | --- |
| `ERR-CREDIT-LIMIT-001` | Order amount exceeds customer credit limit | System rejects order and returns code 42 | Prevents over-limit credit exposure | Caller receives "Credit limit exceeded"; rejection is logged | `EV-CREDIT-LIMIT-002`, `EV-CREDIT-LIMIT-003`, `EV-CREDIT-LIMIT-005` | Confirm message and no-overrides policy |
| `ERR-CREDIT-LIMIT-002` | Customer ID not found in customer master | Program returns code 99 | Order cannot be validated against a customer limit | Final business handling is unclear | `EV-CREDIT-LIMIT-004` | Confirm whether caller rejects order or routes for follow-up |

---

## 9. Dependencies

| Dependency ID | Dependency Type | Dependency | Role in Function | Evidence | Status / Risk |
| --- | --- | --- | --- | --- | --- |
| `DEP-CREDIT-LIMIT-001` | `data` | Customer master file | Authoritative source of credit limit at order time | `EV-CREDIT-LIMIT-004` | `confirmed` |
| `DEP-CREDIT-LIMIT-002` | `upstream_system` | Order-entry caller | Supplies customer ID and order credit amount | `EV-CREDIT-LIMIT-001` | `confirmed` |
| `DEP-CREDIT-LIMIT-003` | `reporting/audit` | Transaction audit file | Stores rejection trail for credit policy and operations review | `EV-CREDIT-LIMIT-005` | `confirmed` |
| `DEP-CREDIT-LIMIT-004` | `policy` | Credit limit maintenance workflow | Updates customer limits outside this capability | SME notes in `BR-CREDIT-LIMIT-003` | `out_of_scope_dependency` |

---

## 11. Supporting Workflow or Design Notes (Optional)

- **Workflow reference:** `flow-CARD-AUTH.md`
- **Business interpretation:** Order-entry submits credit orders for immediate
  validation; the credit-check function returns an accept/reject decision to the
  caller.
- **Evidence:** `EV-CREDIT-LIMIT-001`, `EV-CREDIT-LIMIT-002`
- **Limitations / TBDs:** Customer-not-found handling remains open as
  `TBD-CREDIT-LIMIT-003`.

---

## 12. Source Document Mapping (Optional)

| Source ID | Source Document / Section | Used For | BRD Section | Evidence ID | Notes |
| --- | --- | --- | --- | --- | --- |
| `SRC-CREDIT-LIMIT-001` | `program-analysis-CREDIT-CHECK-001.md`, section 3.2 | Amount comparison behavior | 7.1 | `EV-CREDIT-LIMIT-001` | Confirms limit comparison and rejection code |
| `SRC-CREDIT-LIMIT-002` | `program-analysis-CREDIT-CHECK-001.md`, section 4.1 | Rejection response | 8 | `EV-CREDIT-LIMIT-002` | Confirms return code and error message |
| `SRC-CREDIT-LIMIT-003` | redacted rejected-order spool sample | Runtime rejection example | 2, 4, 8 | `EV-CREDIT-LIMIT-003` | Confirms observed rejection output |
| `SRC-CREDIT-LIMIT-004` | `program-analysis-CREDIT-CHECK-001.md`, section 5.0 | Customer master lookup | 5, 6, 7.1, 9 | `EV-CREDIT-LIMIT-004` | Confirms customer ID lookup |
| `SRC-CREDIT-LIMIT-005` | `program-analysis-CREDIT-CHECK-001.md`, section 6.2 | Audit logging | 4, 6, 8, 9 | `EV-CREDIT-LIMIT-005` | Confirms rejection log write |

---

## 13. Open Questions & Gaps (TBDs)

### TBD-CREDIT-LIMIT-001: Partial Credit Scenarios

**Category:** `sme_questions`
**Statement:** If a customer has a credit limit of $1,000 and orders $900, can a
second $200 order be placed in the same session, or is the limit checked against
total pending orders?
**Evidence:** No behavior observed for multi-order sessions.
**Resolver:** `SME (John Smith)`
**Blocking:** `no`

**Context:** SME confirmed the legacy behavior is per-order. Aggregate pending
order exposure is a possible future policy decision.

---

### TBD-CREDIT-LIMIT-002: Credit Limit Update Cadence

**Category:** `sme_questions`
**Statement:** How frequently is the customer master credit limit updated, and
what latency is expected between a limit change and order-time validation?
**Evidence:** Module analysis does not cover credit limit maintenance workflows.
**Resolver:** `SME (John Smith)` or `Architecture`
**Blocking:** `no`

**Context:** This affects future caching or consistency decisions, not the
current BRD boundary.

---

### TBD-CREDIT-LIMIT-003: Customer-Not-Found Handling

**Category:** `sme_questions`
**Statement:** When a customer ID is not found, does the caller reject the order
or route it to a different follow-up path?
**Evidence:** Program returns error code 99; final caller handling is not shown.
**Resolver:** `SME (John Smith)`
**Blocking:** `no`

**Context:** Edge case for downstream spec and test planning.

---

## 14. Validation Scenario Summary

See `validation-scenarios.md` for SME-reviewable `VAL-*` scenario seeds. These
are not formal `AC-*` acceptance criteria or formal `TC-*` test cases.

| Scenario ID | Scenario Type | Related BR/BEH | Evidence | Readiness | SME Focus |
| --- | --- | --- | --- | --- | --- |
| `VAL-CREDIT-LIMIT-001` | `happy_path` | `BR-CREDIT-LIMIT-001`, `BEH-CREDIT-LIMIT-001` | `EV-CREDIT-LIMIT-001`, `EV-CREDIT-LIMIT-004` | `ready_for_spec` | Normal approval path |
| `VAL-CREDIT-LIMIT-002` | `exception` | `BR-CREDIT-LIMIT-001`, `BR-CREDIT-LIMIT-002` | `EV-CREDIT-LIMIT-001`, `EV-CREDIT-LIMIT-002`, `EV-CREDIT-LIMIT-003` | `ready_for_spec` | Credit exceeded rejection |
| `VAL-CREDIT-LIMIT-003` | `exception` | `BR-CREDIT-LIMIT-003`, `BEH-CREDIT-LIMIT-003` | `EV-CREDIT-LIMIT-004` | `needs_sme_review` | Missing customer routing |
| `VAL-CREDIT-LIMIT-004` | `boundary` | `BR-CREDIT-LIMIT-001`, `BEH-CREDIT-LIMIT-001` | `EV-CREDIT-LIMIT-001` | `needs_sme_review` | Equal-to-limit boundary |

---

## 15. Traceability Summary

See `traceability.md` for the full cross-reference table and evidence index.

**Summary:**
- 3 business scenarios documented
- 3 channels, 2 user touchpoints, and 4 system interfaces documented
- 4 observed validation behaviors documented
- 3 inferred business rules identified and confirmed by SME for spec promotion
- 4 validation scenario seeds drafted
- 3 open questions (0 blocking, 3 non-blocking)
- All claims trace to supporting evidence
- No `sensitivity: unknown` evidence

---

**Document prepared by:** Claude Code (2026-05-15)
**Last reviewed by:** John Smith, Credit Policy Manager (2026-05-15, status: approved)
