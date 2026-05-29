# Business Requirements Document: Order Routing (BLOCKED)

**Document ID:** `BRD-ORDER-ROUTING-001`
**Capability ID:** `CAP-ORDER-ROUTING-001`
**Module ID:** `MODULE-ORDER-PROCESS-001`
**Module Analysis Source:** `04_modules/order-process/`
**Status:** `blocked`
**Owner:** Sarah Lee (Order Fulfillment Manager)
**Created:** `2026-05-14`
**Last Updated:** `2026-05-15`

---

This example shows the correct behavior when SME-required sections 1-9 cannot
be safely completed. The BRD keeps the functional-analysis shape visible, but it
does not invent missing channels, interfaces, rules, flow details, errors, or
dependencies.

## 1. Function Purpose

### Purpose Statement

Order Routing is intended to assign submitted orders to an appropriate
fulfillment path. The exact business decision logic is not safe to state from
current evidence.

### Business Value

Orders need a reliable routing decision before fulfillment can proceed. The
available inputs do not yet confirm whether the objective is cost, speed,
capacity, geography, or another fulfillment policy.

### Scope Boundary

**In Scope:**
- Fulfillment-center assignment, pending confirmation
- Shipping-method selection, pending SME scope confirmation

**Out of Scope:**
- Not safe to state until `TBD-ORDER-ROUTING-004` is resolved

### Scope Clarification Need

The SME must confirm whether this BRD covers only fulfillment-center assignment
or also shipping-method selection, manual override, and exception handling.
This is tracked as `TBD-ORDER-ROUTING-004`.

---

## 2. Business Scenarios / Use Cases

| Scenario ID | Business Scenario / Use Case | Primary Actor | Trigger | Business Outcome | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| `SCN-ORDER-ROUTING-001` | Submitted order needs fulfillment routing | Customer / order-entry process | Order submitted | Not safe to state; routing logic missing | `EV-ORDER-ROUTING-001` | `blocked` |
| `SCN-ORDER-ROUTING-002` | Order may need geographic assignment | Customer / order-entry process | Order contains geography-relevant data | Not safe to state; only a code comment mentions geography | `EV-ORDER-ROUTING-002` | `blocked` |

---

## 3. Channels

The order-entry channel is implied by the module seed, but approved flow
analysis is missing. Do not list specific channels until
`TBD-ORDER-ROUTING-003` is resolved.

| Channel ID | Channel / Entry Point | Direction | Business Role | Evidence | Confidence / Status |
| --- | --- | --- | --- | --- | --- |
| `CH-ORDER-ROUTING-001` | Order submission path | `inbound` | Starts routing decision | module seed only | `blocked_missing_flow` |

---

## 4. User Interface / User Touchpoints

No user-facing screen, notification, report, queue, or message is confirmed from
approved inputs. If routing exceptions or manual override screens exist, they
must be supplied by SME or upstream flow/program analysis.

---

## 5. System Interfaces

System interfaces cannot be safely finalized because approved flow analysis is
missing.

| Interface ID | System / API / Interface | Direction | Business Purpose | Evidence | Confidence / Status |
| --- | --- | --- | --- | --- | --- |
| `IF-ORDER-ROUTING-001` | Fulfillment center / shipping operation | `downstream` | Receives or acts on routing decision | not yet evidenced | `blocked_missing_flow` |

---

## 6. Process Flow

### Business Trigger

An order is submitted and needs assignment to a fulfillment path.

### Current-State Flow

1. The order enters the routing capability.
2. The system appears to select a fulfillment center.
3. The business basis for selection is not confirmed from available evidence.

### Business States

Not safe to state. Required control flow and state-transition evidence is
missing; see `TBD-ORDER-ROUTING-001` and `TBD-ORDER-ROUTING-003`.

### Business Outcomes and Controls

- **Normal outcome:** Not safe to state.
- **Exception outcome:** Not confirmed from available evidence.
- **Control or audit point:** Not confirmed from available evidence.

---

## 7. Validation Rules

### 7.1 Observed Validation Behaviors

#### BEH-ORDER-ROUTING-001: Fulfillment Center Selection

**Statement:** The system appears to determine which fulfillment center should
process an order.

**Evidence:** `EV-ORDER-ROUTING-001` (program analysis section 2.1)

**Knowledge Type:** `observed_behavior`
**Confidence:** `low`

**Issue:** The program analysis describes the routine name
`SELECT-FULFILLMENT-CENTER` but does not include the actual control flow logic.
See `TBD-ORDER-ROUTING-001`.

---

#### BEH-ORDER-ROUTING-002: Geographic Assignment

**Statement:** Not safe to claim as observed behavior. Available evidence only
contains a comment that mentions geographic logic.

**Evidence:** `EV-ORDER-ROUTING-002` (comment only)

**Knowledge Type:** `unknown_tbd`
**Confidence:** `low`

**Issue:** No actual geographic lookup logic is documented. See
`TBD-ORDER-ROUTING-002`.

---

### 7.2 Inferred Business Rules

#### BR-ORDER-ROUTING-001: Fulfillment Center Optimization

**Statement:** The routing objective is not safe to state. It may be cost,
delivery time, capacity, geography, or a balanced policy.

**Rationale:** Module overview suggests routing exists, but it does not define
the business objective.

**Evidence:** Module `BR-*` seed; no specific `EV-*` support yet.

**Knowledge Type:** `inferred_business_rule`
**Confidence:** `low`
**Review Status:** `needs_sme_review`

**SME Notes:** Awaiting SME confirmation. See `TBD-ORDER-ROUTING-005`.

---

## 8. Error Handling

Error handling cannot be safely documented. Approved flow analysis is missing,
and the available program analysis does not show exception branches, fallback
rules, manual override paths, or routing failure handling.

---

## 9. Dependencies

| Dependency ID | Dependency Type | Dependency | Role in Function | Evidence | Status / Risk |
| --- | --- | --- | --- | --- | --- |
| `DEP-ORDER-ROUTING-001` | `missing_input` | Approved flow analysis | Needed to understand cross-program flow and error handling | module references `FLOW-ORDER-ROUTING-001` | `blocking` |
| `DEP-ORDER-ROUTING-002` | `program_analysis` | Detailed routine control flow | Needed to confirm routing attributes and algorithm | `EV-ORDER-ROUTING-001` incomplete | `blocking` |
| `DEP-ORDER-ROUTING-003` | `sme_decision` | Scope and optimization objective | Needed to distinguish fulfillment-center assignment from shipping-method selection and define rule intent | current scope / BR seed | `blocking` |

---

## 13. Open Questions & Gaps (TBDs)

### TBD-ORDER-ROUTING-001: Missing Program Flow Details

**Category:** `evidence_gaps`
**Statement:** The program analysis for `SELECT-FULFILLMENT-CENTER` provides a
routine name and comment, but not the actual routing control flow.
**Evidence:** `EV-ORDER-ROUTING-001` is incomplete.
**Resolver:** `Program Analyzer`
**Blocking:** `yes`

---

### TBD-ORDER-ROUTING-002: Geographic Logic Not Evidenced

**Category:** `evidence_gaps`
**Statement:** The claim that orders are assigned by geography is based only on
a code comment. No geographic lookup logic is visible.
**Evidence:** `EV-ORDER-ROUTING-002` is comment-only evidence.
**Resolver:** `Program Analyzer` or `SME`
**Blocking:** `yes`

---

### TBD-ORDER-ROUTING-003: Missing Flow Analysis

**Category:** `missing_inputs`
**Statement:** Module analysis references `FLOW-ORDER-ROUTING-001`, but no
approved flow analysis has been provided.
**Evidence:** Missing upstream artifact.
**Resolver:** `Flow Analyzer`
**Blocking:** `yes`

---

### TBD-ORDER-ROUTING-004: Shipping Method vs. Fulfillment Center

**Category:** `sme_questions`
**Statement:** Is shipping-method selection part of this capability, or is it a
separate decision from fulfillment-center assignment?
**Evidence:** Scope statement lists shipping method, but observed behavior only
mentions fulfillment center.
**Resolver:** `SME`
**Blocking:** `yes`

---

### TBD-ORDER-ROUTING-005: Performance or Cost Optimization

**Category:** `sme_questions`
**Statement:** Is the routing rule to minimize cost, minimize delivery time,
balance both, or use another objective?
**Evidence:** Module seed is ambiguous.
**Resolver:** `SME`
**Blocking:** `yes`

---

## 14. Validation Scenario Summary

No `VAL-*` scenario seed is safe to draft yet because available evidence does
not support a business validation scenario without inventing routing logic.
Deferred scenario ideas are captured in `validation-scenarios.md`.

---

## 15. Traceability Summary

See `traceability.md` for the partial cross-reference table. This BRD is
blocked because required sections 1-9 cannot be completed safely from current
evidence.

---

**Document prepared by:** Claude Code (2026-05-15)
**Last reviewed by:** Not reviewed; blocked before SME review
