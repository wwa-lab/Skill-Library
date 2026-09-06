# BRD Validation Scenarios: Order Routing (INCOMPLETE)

**BRD ID:** `BRD-ORDER-ROUTING-001`
**Capability ID:** `CAP-ORDER-ROUTING-001`
**Status:** `blocked`
**Owner:** Sarah Lee (Order Fulfillment Manager)
**Created:** `2026-05-15`
**Last Updated:** `2026-05-21`

---

## Purpose

This file shows how the BRD writer should handle validation scenarios when
module evidence is insufficient. It does not invent formal `AC-*` or `TC-*`
items.

---

## Scenario Coverage Summary

| Area | Count | Notes |
| --- | ---: | --- |
| Happy path scenarios | 0 | Blocked by missing fulfillment selection logic |
| Exception scenarios | 0 | No approved exception evidence |
| Boundary scenarios | 0 | No approved threshold or geography evidence |
| Deferred / evidence-missing scenarios | 2 | Require SME and source evidence before scenario drafting |

---

## Scenario Seeds

No `VAL-*` scenario seed is safe to draft yet. The available evidence does not
support a concrete business validation scenario without inventing routing logic.

---

## Deferred Scenarios

| Deferred Scenario | Related BR/BEH | Blocking Reason | Resolver | Next Step |
| --- | --- | --- | --- | --- |
| Fulfillment center selection | `BR-ORDER-ROUTING-001`, `BEH-ORDER-ROUTING-001` | `missing_control_flow_evidence` | Source Owner + SME | Provide approved program flow or SME-confirmed routing rule |
| Geographic assignment | `BEH-ORDER-ROUTING-002` | `comment_only_evidence` | SME | Confirm whether geography is policy, implementation note, or obsolete behavior |

---

## SME Review Checklist

- [ ] Resolve `TBD-ORDER-ROUTING-001` before drafting `VAL-*` scenario seeds.
- [ ] Resolve `TBD-ORDER-ROUTING-002` before drafting geography-based scenarios.
- [ ] Do not create formal `AC-*` or `TC-*` until source evidence and BRD
      scope are approved.
