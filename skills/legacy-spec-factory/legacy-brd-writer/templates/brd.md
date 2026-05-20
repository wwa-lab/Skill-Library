# Business Requirements Document: `<CAPABILITY-NAME>`

**Document ID:** `BRD-<CAPABILITY-SLUG>-001`  
**Capability ID:** `CAP-<CAPABILITY-SLUG>-001`  
**Module ID:** `MODULE-<MODULE-SLUG>-001`  
**Module Analysis Source:** `04_modules/<MODULE-SLUG>/`  
**Status:** `draft` | `in_review` | `approved`  
**Owner:** `<SME Name / Role>`  
**Created:** `<YYYY-MM-DD>`  
**Last Updated:** `<YYYY-MM-DD>`

---

## 1. Capability Overview

### Scope Statement

**In Scope:**
- `<Capability area 1>`
- `<Capability area 2>`

**Out of Scope:**
- `<Related area not included>`

### Business Owner

- **Name / Role:** `<SME Name>`
- **Contact:** `<Email or other contact>`

### Business Value

Briefly describe why this capability matters to the business (customer impact,
revenue, compliance, operational efficiency, etc.). Keep to 2-3 sentences.

---

## 2. Observed Behaviors

Factual statements about what the legacy system demonstrably does, derived from
approved program / flow analyses, data flows, and runtime evidence.

### BEH-<CAPABILITY-SLUG>-001: `<Behavior Title>`

**Statement:** `<Factual description of observed behavior>`

**Evidence:** `EV-<CAPABILITY-SLUG>-001` (source type: flow analysis, program
analysis, spool output, etc.)

**Knowledge Type:** `observed_behavior`  
**Confidence:** `high` | `medium` | `low`

---

### BEH-<CAPABILITY-SLUG>-002: `<Behavior Title>`

**Statement:** `<Factual description>`

**Evidence:** `EV-<CAPABILITY-SLUG>-002`, `EV-<CAPABILITY-SLUG>-003`

**Knowledge Type:** `observed_behavior`  
**Confidence:** `high`

---

## 3. Inferred Business Rules

Rules we infer from the observed system behavior. These are candidates for
promotion to approved requirements in the specification phase.

**Important:** Every BR-* below carries `status: needs_sme_review`. The SME must
confirm whether each is actually a business rule (vs. implementation artifact).

### BR-<CAPABILITY-SLUG>-001: `<Rule Title>`

**Statement:** `<Proposed business rule>`

**Rationale:** Inferred from `BEH-<CAPABILITY-SLUG>-001` and `BEH-<CAPABILITY-SLUG>-002`.

**Evidence:** `EV-<CAPABILITY-SLUG>-001`, `EV-<CAPABILITY-SLUG>-002`

**Knowledge Type:** `inferred_business_rule`  
**Confidence:** `high` | `medium` | `low`  
**Review Status:** `needs_sme_review`  

**SME Decision:** `pending` | `confirmed_for_spec_promotion` | `rejected` |
`needs_evidence`

**SME Notes:** `<Space for reviewer to confirm or reject>`

---

### BR-<CAPABILITY-SLUG>-002: `<Rule Title>`

**Statement:** `<Proposed business rule>`

**Rationale:** `<Why we think this is a rule, based on evidence>`

**Evidence:** `EV-<CAPABILITY-SLUG>-004`

**Knowledge Type:** `inferred_business_rule`  
**Confidence:** `low`  
**Review Status:** `needs_sme_review`  

**SME Decision:** `pending`

**SME Notes:** `<Awaiting SME decision on whether this is real>`

---

## 4. Open Questions & Gaps (TBDs)

Questions that remain unresolved and must be answered before the next phase
(spec-writing).

### TBD-<CAPABILITY-SLUG>-001: `<Question Title>`

**Category:** `sme_questions` | `evidence_gaps` | `contradictory_evidence` |
`downstream_handoff_blockers`  
**Statement:** `<What is unclear or missing?>`  
**Resolver:** `<Role: SME, Source Owner, Architecture team, etc.>`  
**Blocking:** `yes` | `no` (for this step and/or next step)

**Context:** `<Why this matters / where it appears in the BRD>`

---

### TBD-<CAPABILITY-SLUG>-002: `<Question Title>`

**Category:** `contradictory_evidence`  
**Statement:** Program A says X; Program B says Y. Which is correct?  
**Evidence:** `EV-<CAPABILITY-SLUG>-005`, `EV-<CAPABILITY-SLUG>-006`  
**Resolver:** `SME`  
**Blocking:** `yes` (must resolve before spec-writing)

---

## 5. Evidence Index

Summary of all evidence collected for this capability.

| ID | Source | Type | Sensitivity | Strength | Notes |
| --- | --- | --- | --- | --- | --- |
| `EV-<CAPABILITY-SLUG>-001` | `flow-<FLOW-SLUG>.md`, line X | flow analysis | `public` | `confirmed_from_code` | Control flow from RPGLE program X |
| `EV-<CAPABILITY-SLUG>-002` | spool sample, redacted | runtime | `redacted` | `observed_in_runtime` | Sample transaction output |
| `EV-<CAPABILITY-SLUG>-003` | `program-analysis-<OBJ-ID>.md` | program analysis | `public` | `confirmed_from_code` | Error handling branch |
| `EV-<CAPABILITY-SLUG>-004` | SME interview notes | sme | `public` | `confirmed_by_sme` | BAU procedure not in code |

---

## 6. Traceability Summary

See `traceability.md` for the full cross-reference table.

**Quick Summary:**
- X observed behaviors documented
- Y inferred business rules identified (all `needs_sme_review`)
- Z open questions (A blocking, B non-blocking)
- All claims trace to supporting evidence

---

## Appendix: Known Constraints & Conventions

### Capitalization & Terminology

Use terminology as defined by the business SME. Avoid jargon unless it is
standard in the domain.

### Data Sensitivity

All evidence references mark sensitivity level. Raw (non-redacted) evidence is
never included in this document. See `../../../../docs/legacy-spec-factory/data-collection-and-redaction.md`
for redaction policy.

### Cross-References to Upstream Artifacts

- Module analysis: `04_modules/<MODULE-SLUG>/`
- Flow analyses: `02_flows/flow-<FLOW-SLUG>.md`
- Program analyses: `02_programs/program-analysis-<OBJ-ID>.md`
- Inventory: `01_inventory/inventory.yaml`

---

**Document prepared by:** Claude Code (date)  
**Last reviewed by:** `<SME name>` (date, status)
