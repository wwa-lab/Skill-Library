# Decision Package Review Checklist

**Step**: `STEP-<CAP-SLUG>-001`
**Capability**: `<Capability Name>`
**Review Date**: `YYYY-MM-DD`
**Review Coordinator**: `<name>`

---

## Package Contents

Review that all required artifacts are present:

- [ ] `modernization-decisions.yaml` — consolidated decision metadata
- [ ] `decisions/DEC-<CAP-SLUG>-001.md` — expanded DEC record #1
- [ ] `decisions/DEC-<CAP-SLUG>-002.md` — expanded DEC record #2 (if applicable)
- [ ] `decision-review.md` — this checklist
- [ ] `traceability.md` — BR/BEH/EV cross-reference matrix

---

## Structural Validation

### ID Format & Uniqueness

- [ ] All `DEC-*` IDs follow pattern `DEC-<CAP-SLUG>-<NNN>` (three digits)
- [ ] IDs are stable across revisions (no renumbering)
- [ ] No duplicate IDs within this package or upstream specs

### Evidence Integrity

- [ ] Every DEC links to at least one existing `BR-*` or `BEH-*` from `spec.yaml`
- [ ] Every BR/BEH reference is valid (exists in spec)
- [ ] No circular references (DEC → missing BR → non-existent EV)
- [ ] Every linked `EV-*` is valid (exists in spec evidence list)

### Sensitivity Check

- [ ] No `sensitivity: unknown` fields in linked evidence
- [ ] Redaction log reviewed for any PII/confidential data
- [ ] All sensitive data properly redacted per `docs/data-collection-and-redaction.md`

---

## Decision Rigor

### Alternatives

- [ ] Each DEC articulates **at least 2 real alternatives** (not strawman)
- [ ] Each alternative has pros/cons analysis
- [ ] Chosen option is clearly called out with rationale
- [ ] Rejected options explain why they were dismissed

### Rationale Grounding

- [ ] Rationale references **at least one linked BR/BEH** and at least one
  linked `EV-*`
- [ ] Technology/topology/protocol/runtime choices reference **at least one
  explicit target platform constraint** or named architecture approval
- [ ] Rationale is evidence-backed (not opinion-based)
- [ ] Rationale explains **why target system should work this way**, not just "legacy does it"

### Anti-Hallucination Checks

- [ ] No invented business rules (all linked BRs pre-exist)
- [ ] No unjustified framework/technology choices (Java? Spring? PostgreSQL? All grounded or explicitly deferred)
- [ ] No invocations of "legacy did it" without BR backing
- [ ] No decision presented as `approved` without proper authority sign-off

---

## SME Review (IBM i / Legacy Behavior Verification)

### Legacy Behavior Preservation

- [ ] SME confirmed that linked `BEH-*` records accurately describe legacy system
- [ ] DEC respects observed legacy behavior or explicitly replaces it
- [ ] Missing legacy constraints have been identified (if any)
- [ ] SME is comfortable that target implementation can faithfully execute legacy rules

### Evidence Confidence

- [ ] SME reviewed linked evidence (`EV-*`) for accuracy and completeness
- [ ] Evidence strength ratings are realistic (not inflated)
- [ ] Any weak evidence is flagged with TBD for later confirmation

### Sign-Off

**SME Reviewer**: `<name>`
**Date**: `YYYY-MM-DD`
**Sign-off**: `[ ] approved [ ] requested_changes [ ] deferred`

**Notes**:
```
(Optional notes on review, concerns, or conditions)
```

---

## Architecture / Product Owner Review

### Target Platform Alignment

- [ ] Architecture owner confirmed that every DEC fits declared target platform
- [ ] Technology choices (if any) are available in target platform
- [ ] Scale assumptions are realistic for platform
- [ ] Service boundaries align with microservices (or other) architecture

### Implementation Feasibility

- [ ] Decisions are implementable in target technology stack
- [ ] Effort estimates are reasonable
- [ ] Dependencies are identified and resolvable
- [ ] No "nice to have" features disguised as decisions

### Trade-Offs

- [ ] Architecture owner explicitly evaluated trade-offs (cost vs. performance vs. simplicity)
- [ ] Trade-offs are documented in decision record
- [ ] Chosen option represents acceptable balance
- [ ] Cross-capability impacts are identified

### Operational Readiness

- [ ] Ops/DevOps team has reviewed deployment & monitoring implications
- [ ] SLA/SLI are defined (if decision affects performance)
- [ ] Alert/escalation strategy is documented (if risk is present)

### Sign-Off

**Architecture Reviewer**: `<name>`
**Date**: `YYYY-MM-DD`
**Sign-off**: `[ ] approved [ ] requested_changes [ ] deferred`

**Notes**:
```
(Optional notes on review, concerns, or conditions)
```

---

## Product Owner / Business Review

### Business Alignment

- [ ] Decisions support approved business rules (`BR-*`)
- [ ] Decisions do not introduce new acceptance criteria (ACs stay in spec-writer)
- [ ] Impact on customer/partner workflows is documented
- [ ] Backward compatibility strategy is clear (if legacy coexistence required)

### Stakeholder Communication

- [ ] Decisions are written for non-technical stakeholder consumption
- [ ] Business impact (effort, timeline, risk) is visible
- [ ] No technical jargon without explanation

### Sign-Off (Optional for MVP)

**Product Reviewer**: `<name>`
**Date**: `YYYY-MM-DD`
**Sign-off**: `[ ] approved [ ] requested_changes [ ] deferred`

**Notes**:
```
(Optional notes on review, concerns, or conditions)
```

---

## Traceability Validation

### Cross-Reference Completeness

- [ ] `traceability.md` shows all DEC → BR/BEH/EV links
- [ ] No orphaned evidence (EVs in spec but not referenced by any DEC)
- [ ] No orphaned decisions (DECs that don't link to any rule)

### Forward SDLC Compatibility

- [ ] Existing AC links are copied from `spec.yaml`; decision-writer did not
  mint new `AC-*`
- [ ] DECs are sufficiently specific for downstream design without becoming
  design or task artifacts
- [ ] No "design it during implementation" vague decisions

### Integration Back to Spec

- [ ] Plan documented for reconciling approved DECs back to `spec.yaml`
- [ ] Spec update process is clear (who, when, how)

---

## Blocking Issues

Check if any blocking issues prevent approval:

- [ ] Missing SME sign-off (cannot approve without SME review of legacy fidelity)
- [ ] Missing architecture sign-off (cannot approve without arch review of target fit)
- [ ] Unresolved blocking TBD (decision depends on TBD that hasn't been resolved)
- [ ] Evidence integrity failure (broken links, invalid IDs)
- [ ] Clear hallucination (invented rule, unjustified tech choice)

**If any blocking issue is checked, package cannot be approved. Return to decision writer with remediation list.**

---

## Improvement Recommendations

(Non-blocking suggestions for enhancement)

| Finding | Suggested Change |
|---------|------------------|
| | |
| | |
| | |

---

## Final Disposition

### Package Status

**Current Status**: `[ ] draft [ ] in_review [ ] approved [ ] rejected`

**Transition to**: `[ ] in_review [ ] approved [ ] rejected [ ] retired`

### Summary

```
(1-2 sentence summary of review outcome)
```

### Approval Timeline

- [ ] Structural validation: YYYY-MM-DD
- [ ] SME review: YYYY-MM-DD (or "awaiting SME availability")
- [ ] Architecture review: YYYY-MM-DD (or "awaiting arch review")
- [ ] Product review: YYYY-MM-DD (optional, or "not required for MVP")

---

## Reconciliation And Handoff Readiness

If approved, check readiness for reconciliation into the canonical spec and
later Forward Handoff Gate:

- [ ] All DECs are reconciled back to approved `spec.yaml`
- [ ] Decision package is exported to `05_decisions/<CAP-SLUG>/`
- [ ] Traceability matrix is published and accessible to dev teams
- [ ] Decision-level impact (effort signal, dependencies, risks) is visible
- [ ] Open TBDs are escalated with resolution owner & deadline

**Reconciliation Date**: `YYYY-MM-DD` (or "pending TBD resolution")

---

## Reviewer Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Review Coordinator | | | |
| SME (IBM i Legacy) | | | |
| Architecture Owner | | | |
| Product Owner | | | |

---

## Revision History

| Date | Reviewer | Change |
|------|----------|--------|
| | | |
| | | |
