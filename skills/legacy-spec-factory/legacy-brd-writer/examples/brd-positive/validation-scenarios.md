# BRD Validation Scenarios: Credit Limit Enforcement

**BRD ID:** `BRD-CREDIT-LIMIT-001`
**Capability ID:** `CAP-CREDIT-LIMIT-001`
**Status:** `approved`
**Owner:** John Smith (Credit Policy Manager)
**Created:** `2026-05-15`
**Last Updated:** `2026-05-21`

---

## Purpose

These `VAL-*` scenario seeds help the SME confirm BRD coverage and help
downstream teams plan acceptance criteria and golden master cases. They are not
formal `AC-*` acceptance criteria or formal `TC-*` test cases.

---

## Scenario Coverage Summary

| Area | Count | Notes |
| --- | ---: | --- |
| Happy path scenarios | 1 | Order within available credit |
| Exception scenarios | 2 | Credit exceeded and missing customer |
| Boundary scenarios | 1 | Order amount equals credit limit |
| Deferred / evidence-missing scenarios | 0 | Runtime evidence is available for listed scenarios |

---

## Scenario Seeds

### VAL-CREDIT-LIMIT-001: Order Within Credit Limit

**Scenario Type:** `happy_path`
**Business Goal:** Confirm that credit orders within the authorized limit can proceed.
**Related Rules:** `BR-CREDIT-LIMIT-001`
**Related Behaviors:** `BEH-CREDIT-LIMIT-001`
**Evidence:** `EV-CREDIT-LIMIT-001`, `EV-CREDIT-LIMIT-004`
**SME Question:** Does this scenario cover the normal credit approval path for the BRD scope?
**Expected Business Outcome:** Order proceeds when available credit is sufficient.
**Data Needed Later:** Redacted accepted-order transaction sample for `TC-*` planning.
**Readiness:** `ready_for_spec`

---

### VAL-CREDIT-LIMIT-002: Order Exceeds Credit Limit

**Scenario Type:** `exception`
**Business Goal:** Confirm that orders exceeding available credit are rejected.
**Related Rules:** `BR-CREDIT-LIMIT-001`, `BR-CREDIT-LIMIT-002`
**Related Behaviors:** `BEH-CREDIT-LIMIT-001`, `BEH-CREDIT-LIMIT-002`
**Evidence:** `EV-CREDIT-LIMIT-001`, `EV-CREDIT-LIMIT-002`, `EV-CREDIT-LIMIT-003`
**SME Question:** Is the rejection behavior a required business policy or only a legacy implementation artifact?
**Expected Business Outcome:** Order is not placed and the business receives a credit-limit rejection.
**Data Needed Later:** Redacted rejected-order transaction and expected legacy output evidence.
**Readiness:** `ready_for_spec`

---

### VAL-CREDIT-LIMIT-003: Customer Record Not Found

**Scenario Type:** `exception`
**Business Goal:** Confirm customer-not-found behavior stays visible during spec-writing.
**Related Rules:** `BR-CREDIT-LIMIT-003`
**Related Behaviors:** `BEH-CREDIT-LIMIT-003`
**Evidence:** `EV-CREDIT-LIMIT-004`
**SME Question:** Should customer-not-found behavior be treated as part of credit limit enforcement or routed to customer validation?
**Expected Business Outcome:** Order does not proceed until customer identity is resolved.
**Data Needed Later:** Runtime sample or SME-approved expected behavior for missing customer.
**Readiness:** `needs_sme_review`

---

### VAL-CREDIT-LIMIT-004: Order Amount Equals Credit Limit

**Scenario Type:** `boundary`
**Business Goal:** Confirm the inclusive/exclusive boundary for the credit limit comparison.
**Related Rules:** `BR-CREDIT-LIMIT-001`
**Related Behaviors:** `BEH-CREDIT-LIMIT-001`
**Evidence:** `EV-CREDIT-LIMIT-001`
**SME Question:** Is an order equal to the credit limit allowed?
**Expected Business Outcome:** Business policy for the exact boundary is confirmed before formal AC/TC generation.
**Data Needed Later:** Redacted boundary transaction or SME-approved expected outcome.
**Readiness:** `needs_sme_review`

---

## Deferred Scenarios

No deferred scenarios for this approved example.
