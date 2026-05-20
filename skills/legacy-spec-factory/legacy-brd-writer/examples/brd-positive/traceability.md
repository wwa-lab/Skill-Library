# BRD Traceability Report: Credit Limit Enforcement

**BRD ID:** `BRD-CREDIT-LIMIT-001`  
**Capability ID:** `CAP-CREDIT-LIMIT-001`  
**Generated:** `2026-05-15`

---

## Overview

Complete traceability for the Credit Limit Enforcement BRD.

**Coverage:**
- **Observed Behaviors:** 4 documented
- **Inferred Business Rules:** 3 identified (all confirmed by SME)
- **Open Questions (TBDs):** 3 defined (0 blocking, 3 non-blocking)
- **Evidence Items:** 5 collected

---

## 1. Observed Behaviors → Evidence

| BEH ID | Behavior | Evidence | Source | Strength |
| --- | --- | --- | --- | --- |
| `BEH-CREDIT-LIMIT-001` | Order amount compared to credit limit; rejected if exceeded | `EV-CREDIT-LIMIT-001` | `program-analysis-CREDIT-CHECK-001.md`, section 3.2 | `confirmed_from_code` |
| `BEH-CREDIT-LIMIT-002` | Error code 42 and message "Credit limit exceeded" returned on rejection | `EV-CREDIT-LIMIT-002` | `program-analysis-CREDIT-CHECK-001.md`, section 4.1 | `confirmed_from_code` |
| `BEH-CREDIT-LIMIT-002` | (continued) | `EV-CREDIT-LIMIT-003` | spool sample (redacted) | `observed_in_runtime` |
| `BEH-CREDIT-LIMIT-003` | Customer credit limit read from CUSTPF; error 99 if not found | `EV-CREDIT-LIMIT-004` | `program-analysis-CREDIT-CHECK-001.md`, section 5.0 | `confirmed_from_code` |
| `BEH-CREDIT-LIMIT-004` | Rejection logged to AUDITPF with timestamp, IDs, amounts | `EV-CREDIT-LIMIT-005` | `program-analysis-CREDIT-CHECK-001.md`, section 6.2 | `confirmed_from_code` |

**Validation:** ✓ All BEH-* items have supporting evidence

---

## 2. Inferred Business Rules → Behaviors & Evidence

| BR ID | Rule | Supports BEH | Evidence | Support Summary | Review Status | SME Decision |
| --- | --- | --- | --- | --- | --- | --- |
| `BR-CREDIT-LIMIT-001` | No order can exceed customer credit limit | `BEH-CREDIT-LIMIT-001`, `BEH-CREDIT-LIMIT-003`, `BEH-CREDIT-LIMIT-004` | `EV-CREDIT-LIMIT-001`, `EV-CREDIT-LIMIT-004`, `EV-CREDIT-LIMIT-005` | direct code-backed behaviors; SME confirmed business intent | `needs_sme_review` | `confirmed_for_spec_promotion` |
| `BR-CREDIT-LIMIT-002` | Credit limit checking is real-time, not deferred | `BEH-CREDIT-LIMIT-001`, `BEH-CREDIT-LIMIT-002` | `EV-CREDIT-LIMIT-001`, `EV-CREDIT-LIMIT-002` | direct transaction behavior; SME confirmed business intent | `needs_sme_review` | `confirmed_for_spec_promotion` |
| `BR-CREDIT-LIMIT-003` | CUSTPF is the authoritative source of credit limits | `BEH-CREDIT-LIMIT-003` | `EV-CREDIT-LIMIT-004` | direct data-source behavior; SME confirmed with caveat | `needs_sme_review` | `confirmed_for_spec_promotion` |

**Validation:** ✓ All BR-* items have supporting BEH and EV; SME decisions are
recorded for spec-writer promotion

---

## 3. Open Questions (TBDs)

| TBD ID | Question | Category | Resolver | Blocking |
| --- | --- | --- | --- | --- |
| `TBD-CREDIT-LIMIT-001` | Partial credit: are limits checked per-order or per-session? | `sme_questions` | SME | No (future policy decision) |
| `TBD-CREDIT-LIMIT-002` | How often is CUSTPF credit limit updated? Latency? | `sme_questions` | SME / Architecture | No (deferred) |
| `TBD-CREDIT-LIMIT-003` | Customer not found (error 99): reject order or fallback? | `sme_questions` | SME | No (edge case) |

**Validation:** ✓ All TBD-* items have a category and resolver

---

## 4. Evidence Items

| EV ID | Type | Source | Sensitivity | Strength | Used By |
| --- | --- | --- | --- | --- | --- |
| `EV-CREDIT-LIMIT-001` | program analysis | `program-analysis-CREDIT-CHECK-001.md`, section 3.2 | `public` | `confirmed_from_code` | BEH-001, BR-001, BR-002 |
| `EV-CREDIT-LIMIT-002` | program analysis | `program-analysis-CREDIT-CHECK-001.md`, section 4.1 | `public` | `confirmed_from_code` | BEH-002, BR-002 |
| `EV-CREDIT-LIMIT-003` | spool sample | `evidence/redacted/spool-ORDER-2026-05-10-REJECTED.txt` | `redacted` | `observed_in_runtime` | BEH-002 |
| `EV-CREDIT-LIMIT-004` | program analysis | `program-analysis-CREDIT-CHECK-001.md`, section 5.0 | `public` | `confirmed_from_code` | BEH-003, BR-001, BR-003 |
| `EV-CREDIT-LIMIT-005` | program analysis | `program-analysis-CREDIT-CHECK-001.md`, section 6.2 | `public` | `confirmed_from_code` | BEH-004, BR-001 |

**Validation:** ✓ No `sensitivity: unknown` items

---

## 5. Cross-Reference Matrix

### Behaviors

- **`BEH-CREDIT-LIMIT-001`**
  - Mentioned in: `brd.md`, section 2.1
  - Backed by: `EV-CREDIT-LIMIT-001` (confirmed_from_code)
  - Used in rules: `BR-CREDIT-LIMIT-001`, `BR-CREDIT-LIMIT-002`

- **`BEH-CREDIT-LIMIT-002`**
  - Mentioned in: `brd.md`, section 2.2
  - Backed by: `EV-CREDIT-LIMIT-002` (code), `EV-CREDIT-LIMIT-003` (runtime)
  - Used in rules: `BR-CREDIT-LIMIT-002`

- **`BEH-CREDIT-LIMIT-003`**
  - Mentioned in: `brd.md`, section 2.3
  - Backed by: `EV-CREDIT-LIMIT-004` (confirmed_from_code)
  - Used in rules: `BR-CREDIT-LIMIT-001`, `BR-CREDIT-LIMIT-003`

- **`BEH-CREDIT-LIMIT-004`**
  - Mentioned in: `brd.md`, section 2.4
  - Backed by: `EV-CREDIT-LIMIT-005` (confirmed_from_code)
  - Used in rules: `BR-CREDIT-LIMIT-001`

### Rules

- **`BR-CREDIT-LIMIT-001`** (Review Status: `needs_sme_review`)
  - Mentioned in: `brd.md`, section 3.1
  - Based on: `BEH-CREDIT-LIMIT-001`, `BEH-CREDIT-LIMIT-003`, `BEH-CREDIT-LIMIT-004`
  - Backed by: `EV-CREDIT-LIMIT-001`, `EV-CREDIT-LIMIT-004`, `EV-CREDIT-LIMIT-005`
  - Confidence: `high`
  - SME Decision: `confirmed_for_spec_promotion` — core company policy

- **`BR-CREDIT-LIMIT-002`** (Review Status: `needs_sme_review`)
  - Mentioned in: `brd.md`, section 3.2
  - Based on: `BEH-CREDIT-LIMIT-001`, `BEH-CREDIT-LIMIT-002`
  - Backed by: `EV-CREDIT-LIMIT-001`, `EV-CREDIT-LIMIT-002`
  - Confidence: `high`
  - SME Decision: `confirmed_for_spec_promotion` — real-time feedback required

- **`BR-CREDIT-LIMIT-003`** (Review Status: `needs_sme_review`)
  - Mentioned in: `brd.md`, section 3.3
  - Based on: `BEH-CREDIT-LIMIT-003`
  - Backed by: `EV-CREDIT-LIMIT-004`
  - Confidence: `medium`
  - SME Decision: `confirmed_for_spec_promotion` with caveat — limits can be updated elsewhere

### Questions

- **`TBD-CREDIT-LIMIT-001`**
  - Mentioned in: `brd.md`, section 4.1; `brd-review.md`, reviewer notes
  - Resolver: `SME (John Smith)`
  - Blocking: `no` (future policy decision)
  - Action: Preserve per-order legacy behavior; carry aggregate exposure as optional product question

- **`TBD-CREDIT-LIMIT-002`**
  - Mentioned in: `brd.md`, section 4.2
  - Resolver: `SME / Architecture`
  - Blocking: `no` (deferred to modernized system design)
  - Action: Can be carried as TBD in spec

- **`TBD-CREDIT-LIMIT-003`**
  - Mentioned in: `brd.md`, section 4.3
  - Resolver: `SME`
  - Blocking: `no` (edge case)
  - Action: Can be noted as edge case; requires edge case test in spec

---

## 6. Validation Checklist

- [x] **All BEH-* items have ≥1 supporting EV-***
- [x] **All BR-* items have ≥1 supporting BEH-* and ≥1 supporting EV-***
- [x] **No dangling references** (all IDs in brd.md appear here)
- [x] **All TBD-* items have a category and resolver**
- [x] **No `sensitivity: unknown` in evidence items**
- [x] **Traceability table is consistent** with brd.md section 5

---

## Summary

**BRD Status:** `approved` (SME sign-off 2026-05-15)

**Readiness for Spec-Writer:**
- All three business rules are confirmed by SME and remain `needs_sme_review`
  until spec-writer promotes them in `spec.yaml`
- Three TBDs identified: zero blocking, three non-blocking / deferred
- No silent gaps — spec-writer has complete visibility

**Next Phase:**
- Route to `legacy-spec-writer` with this BRD plus module analysis
- Spec-writer will generate acceptance criteria for BR-001/002/003
- Spec-writer may carry TBD-001/002/003 as non-blocking design questions
- Modernization will preserve all three SME-confirmed business rules

---

**Report Generated By:** Claude Code  
**Report Date:** `2026-05-15`  
**Status:** `approved`
