# BRD Traceability Report: `<CAPABILITY-NAME>`

**BRD ID:** `BRD-<CAPABILITY-SLUG>-001`  
**Capability ID:** `CAP-<CAPABILITY-SLUG>-001`  
**Generated:** `<YYYY-MM-DD>`

---

## Overview

This report shows the complete traceability between BRD elements (observed
behaviors, inferred rules, open questions) and their supporting evidence.

**Coverage:**
- **Observed Behaviors:** X documented
- **Inferred Business Rules:** Y identified (all `needs_sme_review`)
- **Open Questions (TBDs):** Z defined (A blocking, B non-blocking)
- **Evidence Items:** N collected

---

## 1. Observed Behaviors → Evidence

Every observed behavior must trace to at least one evidence item.

| BEH ID | Behavior | Evidence | Source | Strength |
| --- | --- | --- | --- | --- |
| `BEH-<CAPABILITY-SLUG>-001` | `<Behavior title>` | `EV-<CAPABILITY-SLUG>-001` | flow-<FLOW-SLUG>.md | `confirmed_from_code` |
| `BEH-<CAPABILITY-SLUG>-002` | `<Behavior title>` | `EV-<CAPABILITY-SLUG>-002`, `EV-<CAPABILITY-SLUG>-003` | program-analysis-<OBJ-ID>.md, spool sample | `confirmed_from_code`, `observed_in_runtime` |

**Validation:** All BEH-* items have supporting evidence ✓ / ✗

---

## 2. Inferred Business Rules → Behaviors & Evidence

Every inferred business rule must trace to one or more observed behaviors and
at least one evidence item.

| BR ID | Rule | Supports BEH | Evidence | Support Summary | Review Status | SME Decision |
| --- | --- | --- | --- | --- | --- | --- |
| `BR-<CAPABILITY-SLUG>-001` | `<Rule title>` | `BEH-<CAPABILITY-SLUG>-001`, `BEH-<CAPABILITY-SLUG>-002` | `EV-<CAPABILITY-SLUG>-001`, `EV-<CAPABILITY-SLUG>-002` | direct code/runtime evidence in linked EV records | `needs_sme_review` | `pending` |
| `BR-<CAPABILITY-SLUG>-002` | `<Rule title>` | `BEH-<CAPABILITY-SLUG>-003` | `EV-<CAPABILITY-SLUG>-004` | weak support; needs SME judgment | `needs_sme_review` | `pending` |

**Validation:** All BR-* items have supporting BEH and EV ✓ / ✗

---

## 3. Open Questions (TBDs)

Every open question is categorized and assigned to a resolver.

| TBD ID | Question | Category | Evidence Gap | Resolver | Blocking |
| --- | --- | --- | --- | --- | --- |
| `TBD-<CAPABILITY-SLUG>-001` | `<Question>` | `sme_questions` | Program A vs. Program B behavior unclear | `SME` | Yes (this step) |
| `TBD-<CAPABILITY-SLUG>-002` | `<Question>` | `evidence_gaps` | Missing spool sample for scenario X | `Source Owner` | No (non-blocking) |
| `TBD-<CAPABILITY-SLUG>-003` | `<Question>` | `downstream_handoff_blockers` | Unclear whether this rule applies post-modernization | `Architecture` | No (spec-writer can mark as TBD) |

**Categories:**
- `missing_inputs` — upstream artifact or gate missing
- `evidence_gaps` — evidence itself is missing, unreadable, unredacted
- `contradictory_evidence` — two evidence items conflict
- `sme_questions` — only SME judgment can answer
- `downstream_handoff_blockers` — non-blocking for this step, but needs resolution before next step

**Validation:** All TBD-* items have a category, resolver, and blocking status ✓ / ✗

---

## 4. Evidence Items

Complete list of evidence collected for this capability.

| EV ID | Type | Source | Sensitivity | Redacted? | Strength | Used By |
| --- | --- | --- | --- | --- | --- | --- |
| `EV-<CAPABILITY-SLUG>-001` | flow analysis | `flow-<FLOW-SLUG>.md`, section 3.2 | `public` | N/A | `confirmed_from_code` | BEH-001, BR-001 |
| `EV-<CAPABILITY-SLUG>-002` | program analysis | `program-analysis-<OBJ-ID>.md`, error handler | `public` | N/A | `confirmed_from_code` | BEH-002, BR-001 |
| `EV-<CAPABILITY-SLUG>-003` | spool sample | `evidence/redacted/spool-<SAMPLE-ID>.txt` | `redacted` | Yes | `observed_in_runtime` | BEH-002 |
| `EV-<CAPABILITY-SLUG>-004` | job log | `evidence/redacted/job-<JOB-ID>.log` | `redacted` | Yes | `observed_in_runtime` | BR-002 |

**Validation:** No `sensitivity: unknown` items ✓ / ✗

---

## 5. Cross-Reference Matrix

Quick lookup: for each BRD element, what evidence backs it?

### Behaviors

- **`BEH-<CAPABILITY-SLUG>-001`**
  - Mentioned in: `brd.md`, section 2.1
  - Backed by: `EV-<CAPABILITY-SLUG>-001` (confirmed_from_code)
  - Used in rules: `BR-<CAPABILITY-SLUG>-001`

- **`BEH-<CAPABILITY-SLUG>-002`**
  - Mentioned in: `brd.md`, section 2.2
  - Backed by: `EV-<CAPABILITY-SLUG>-002`, `EV-<CAPABILITY-SLUG>-003` (confirmed_from_code, observed_in_runtime)
  - Used in rules: `BR-<CAPABILITY-SLUG>-001`, `BR-<CAPABILITY-SLUG>-002`

### Rules

- **`BR-<CAPABILITY-SLUG>-001`**
  - Mentioned in: `brd.md`, section 3.1
  - Based on: `BEH-<CAPABILITY-SLUG>-001`, `BEH-<CAPABILITY-SLUG>-002`
  - Backed by: `EV-<CAPABILITY-SLUG>-001`, `EV-<CAPABILITY-SLUG>-002`
  - Confidence: `high` — ready for SME decision before spec promotion

- **`BR-<CAPABILITY-SLUG>-002`**
  - Mentioned in: `brd.md`, section 3.2
  - Based on: `BEH-<CAPABILITY-SLUG>-003`
  - Backed by: `EV-<CAPABILITY-SLUG>-004`
  - Confidence: `low` — needs SME confirmation before spec-writer

### Questions

- **`TBD-<CAPABILITY-SLUG>-001`**
  - Mentioned in: `brd.md`, section 4.1; `brd-review.md`, section 3
  - Resolver: `SME`
  - Blocking: `yes` for this step (must resolve before BRD is approved)

- **`TBD-<CAPABILITY-SLUG>-002`**
  - Mentioned in: `brd.md`, section 4.2
  - Resolver: `Source Owner`
  - Blocking: `no` (non-blocking; can proceed with best-effort evidence)

---

## 6. Validation Checklist

Run before SME approval:

- [ ] **All BEH-* items have ≥1 supporting EV-***
- [ ] **All BR-* items have ≥1 supporting BEH-* and ≥1 supporting EV-***
- [ ] **No dangling references** (all IDs in brd.md appear here)
- [ ] **All TBD-* items have a category and resolver**
- [ ] **No `sensitivity: unknown` in evidence items**
- [ ] **Traceability table is consistent** with brd.md section 4 (Evidence Index)

---

## Appendix: ID Reference

### All IDs in This BRD

**Behaviors:**
- `BEH-<CAPABILITY-SLUG>-001` through `BEH-<CAPABILITY-SLUG>-<N>`

**Rules:**
- `BR-<CAPABILITY-SLUG>-001` through `BR-<CAPABILITY-SLUG>-<N>`

**Open Questions:**
- `TBD-<CAPABILITY-SLUG>-001` through `TBD-<CAPABILITY-SLUG>-<N>`

**Evidence:**
- `EV-<CAPABILITY-SLUG>-001` through `EV-<CAPABILITY-SLUG>-<N>`

**Upstream Artifacts (reused):**
- Capability: `CAP-<CAPABILITY-SLUG>-001`
- Module: `MODULE-<MODULE-SLUG>-001`
- Flows: `FLOW-<FLOW-SLUG>-001`, ...
- Programs/Objects: `OBJ-<OBJECT-ID>-<NNN>`, ...

---

**Report Generated By:** Claude Code / Agent name  
**Report Date:** `<YYYY-MM-DD>`  
**Status:** `draft` | `in_review` | `approved`
