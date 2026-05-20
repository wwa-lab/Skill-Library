# Decision Package Traceability Matrix

**Step**: `STEP-<CAP-SLUG>-001`
**Capability**: `<Capability Name>`
**Generated**: `YYYY-MM-DD`

---

## DEC ↔ BR/BEH Linkage

Shows which business rules and observed behaviors each decision supports or
affects.

| DEC | Category | Decision | Linked BRs | Linked BEHs | Evidence |
|-----|----------|----------|-----------|-------------|----------|
| `DEC-<CAP-SLUG>-001` | architecture | async event-driven | `BR-<CAP-SLUG>-004`, `BR-<CAP-SLUG>-005` | `BEH-<CAP-SLUG>-007` | `EV-<CAP-SLUG>-015`, `EV-<CAP-SLUG>-016` |
| `DEC-<CAP-SLUG>-002` | data | normalize customer into order | `BR-<CAP-SLUG>-007` | `BEH-<CAP-SLUG>-002` | `EV-<CAP-SLUG>-008` |
| `DEC-<CAP-SLUG>-003` | compatibility | 6-month FTP adapter | `BR-<CAP-SLUG>-013` | | `EV-<CAP-SLUG>-017` |

---

## BR/BEH ↔ DEC Coverage

Shows which business rules and observed behaviors are addressed by decisions,
and which remain unaddressed.

### Business Rules Coverage

| BR | Rule | DEC(s) Implementing | Coverage | Status |
|----|------|------------------|----------|--------|
| `BR-<CAP-SLUG>-001` | Order validation per line item | `DEC-<CAP-SLUG>-004` | API design | `needs_sme_review` |
| `BR-<CAP-SLUG>-002` | Inventory reservation atomicity | (none) | **UNCOVERED** | `draft` (TBD-?)  |
| `BR-<CAP-SLUG>-003` | Error notification to store | `DEC-<CAP-SLUG>-005` | Event-driven notification | `approved` |
| `BR-<CAP-SLUG>-004` | Order entry <5 seconds | `DEC-<CAP-SLUG>-001` | Async fulfillment | `approved` |

### Observed Behavior Coverage

| BEH | Observed Legacy Behavior | DEC(s) Replacing/Preserving | Coverage | Status |
|-----|-------------------------|---------------------------|----------|--------|
| `BEH-<CAP-SLUG>-001` | Nightly batch fulfillment job | `DEC-<CAP-SLUG>-001` | Replaced with async | `approved` |
| `BEH-<CAP-SLUG>-002` | Phone number copied to order | `DEC-<CAP-SLUG>-002` | Preserved via denormalization | `approved` |
| `BEH-<CAP-SLUG>-003` | FTP file upload integration | `DEC-<CAP-SLUG>-003` | Preserved via adapter (6 mo) | `approved` |

**Summary**: 3 BRs covered, 1 uncovered (TBD). 3 BEHs preserved/addressed.
Decision package remains blocked until the uncovered rule and blocking TBDs are
resolved.

---

## DEC ↔ Evidence Grounding

Shows which evidence records support each decision's rationale.

### DEC-001: Async Event-Driven

| Evidence | Type | Source | Strength | Used For | Status |
|----------|------|--------|----------|----------|--------|
| `EV-<CAP-SLUG>-015` | job log | legacy CLTL batch log excerpt | confirmed_from_code | "nightly batch takes 2-8 hours" | ✅ |
| `EV-<CAP-SLUG>-016` | sme_note | Jane Smith workflow notes | confirmed_by_sme | "clerk can't wait for fulfillment" | ✅ |
| `EV-<CAP-SLUG>-020` | db2 | ORDER_HEADER table | observed_in_runtime | (not used — data model DEC, not arch) | — |

### DEC-002: Denormalize Customer into Order Events

| Evidence | Type | Source | Strength | Used For | Status |
|----------|------|--------|----------|----------|--------|
| `EV-<CAP-SLUG>-008` | rpgle | ORDFILL program | confirmed_from_code | "PHONE field copied into ORDHEAD" | ✅ |
| `EV-<CAP-SLUG>-010` | sme_note | fulfillment team notes | confirmed_by_sme | "need phone for fulfillment reference" | ✅ |

**Summary**: All decisions have sufficient evidence grounding. No orphaned evidence.

---

## DEC ↔ Acceptance Criteria (If Present)

Shows which existing acceptance criteria in `spec.yaml` are affected by each
decision. Decision-writer does not mint new `AC-*`.

| DEC | Category | Target Decision | AC(s) Validating | Status |
|-----|----------|-----------------|------------------|--------|
| `DEC-<CAP-SLUG>-001` | architecture | async fulfillment | `AC-<CAP-SLUG>-004` (order entry <5s), `AC-<CAP-SLUG>-005` (job status polling) | `draft` (pending DEC approval) |
| `DEC-<CAP-SLUG>-002` | data | denormalized customer | `AC-<CAP-SLUG>-006` (event includes phone) | `draft` (pending DEC approval) |
| `DEC-<CAP-SLUG>-003` | compatibility | FTP adapter | `AC-<CAP-SLUG>-007` (legacy uploads work), `AC-<CAP-SLUG>-008` (migration roadmap published) | `draft` (pending DEC approval) |

**Action**: If ACs are missing or need revision, route back to
`legacy-spec-writer`. AC authorship is spec-writer's responsibility, not
decision-writer's.

---

## TBD Status (Blocking Issues)

Shows open questions that block decision approval.

| TBD | Question | Depends On | Status | Owner | Target Resolution |
|-----|----------|------------|--------|-------|-------------------|
| `TBD-<CAP-SLUG>-018` | "What is max acceptable lag between order & fulfillment start?" | `DEC-<CAP-SLUG>-001` | `blocking: yes` | Product Owner (Alice Chen) | 2026-05-25 |
| `TBD-<CAP-SLUG>-019` | "Can legacy RPG batch logic be decomposed into async steps?" | `DEC-<CAP-SLUG>-001` | `blocking: yes` | SME + Dev (Jane Smith, Bob Jones) | 2026-05-24 |
| `TBD-<CAP-SLUG>-020` | "Should inventory services tolerate eventual consistency?" | `DEC-<CAP-SLUG>-001` (cross-capability) | `pending_sme_judgment` | Inventory PM | 2026-05-26 |

**Blocking TBDs**: Cannot mark package as `approved` until R18 and R19 are resolved.

---

## Risk ↔ Mitigation Traceability

Shows how risks identified in decisions map to mitigations.

| DEC | Risk | Severity | Mitigation | Owner | Status |
|-----|------|----------|-----------|-------|--------|
| `DEC-<CAP-SLUG>-001` | Event queue lag > 5 min | high | Monitor SQS; auto-scale workers | Ops (Bob) | active |
| `DEC-<CAP-SLUG>-001` | Fulfillment job fails silently | high | Dead-letter queue + alerting | Dev (Alice) | active |
| `DEC-<CAP-SLUG>-001` | Legacy logic doesn't decompose | critical | Code review + refactoring + SME sign-off | SME + Dev | **blocking** |
| `DEC-<CAP-SLUG>-002` | Inventory drift (eventual consistency) | medium | SLA + consistency tests | Dev | active |
| `DEC-<CAP-SLUG>-003` | Integration partner adoption lag | medium | Migration roadmap + training | PO (Alice) | active |

**Critical Risks**: Risk #3 (legacy decomposition) must be de-risked before implementation. Recommend prototype + code review in week 1.

---

## Spec Reconciliation And Forward Handoff Checklist

**Readiness for spec reconciliation and later external forward-chain handoff**:

- [ ] All approved DECs exported to `05_decisions/<CAP-SLUG>/`
- [ ] Traceability matrix published (this document)
- [ ] All blocking TBDs resolved (R18, R19 → closed)
- [ ] All critical risks have mitigation plans (R3 → prototype done)
- [ ] SME sign-offs in decision records
- [ ] Architecture approvals in decision records
- [ ] Existing acceptance criteria links are preserved, or missing ACs are routed
  back to `legacy-spec-writer`
- [ ] Decision package has impact context (effort signal, dependencies, risks)

**Handoff Status**: `[ ] ready [ ] pending_tbd_resolution [ ] pending_risk_mitigation [ ] not_ready`

**Estimated Handoff Date**: `2026-05-27` (pending TBD resolution)

---

## Cross-Reference Index

Quick lookup for navigating between artifacts:

### By Decision ID

- **DEC-<CAP-SLUG>-001** (async):
  - Decision record: `decisions/DEC-<CAP-SLUG>-001.md`
  - Linked BRs: `BR-<CAP-SLUG>-004`, `BR-<CAP-SLUG>-005`
  - Linked BEHs: `BEH-<CAP-SLUG>-007`
  - Linked TBDs: `TBD-<CAP-SLUG>-018`, `TBD-<CAP-SLUG>-019`
  - Acceptance criteria: `AC-<CAP-SLUG>-004`, `AC-<CAP-SLUG>-005`

- **DEC-<CAP-SLUG>-002** (data model):
  - Decision record: `decisions/DEC-<CAP-SLUG>-002.md`
  - Linked BRs: `BR-<CAP-SLUG>-007`
  - Linked BEHs: `BEH-<CAP-SLUG>-002`
  - Acceptance criteria: `AC-<CAP-SLUG>-006`

- **DEC-<CAP-SLUG>-003** (compatibility):
  - Decision record: `decisions/DEC-<CAP-SLUG>-003.md`
  - Linked BRs: `BR-<CAP-SLUG>-013`
  - Linked TBDs: `TBD-<CAP-SLUG>-020`
  - Acceptance criteria: `AC-<CAP-SLUG>-007`, `AC-<CAP-SLUG>-008`

### By Business Rule ID

- **BR-<CAP-SLUG>-001**: Implemented by `DEC-<CAP-SLUG>-004` (API design)
- **BR-<CAP-SLUG>-002**: **Not addressed** — TBD
- **BR-<CAP-SLUG>-004**: Implemented by `DEC-<CAP-SLUG>-001` (async)
- **BR-<CAP-SLUG>-007**: Implemented by `DEC-<CAP-SLUG>-002` (data model)
- **BR-<CAP-SLUG>-013**: Implemented by `DEC-<CAP-SLUG>-003` (compatibility)

### By Evidence ID

- **EV-<CAP-SLUG>-008**: Supports `DEC-<CAP-SLUG>-002` (legacy phone field)
- **EV-<CAP-SLUG>-015**: Supports `DEC-<CAP-SLUG>-001` (batch job latency)
- **EV-<CAP-SLUG>-016**: Supports `DEC-<CAP-SLUG>-001` (SME workflow notes)

---

## Summary

| Metric | Count |
|--------|-------|
| Total DECs in package | 3 |
| Approved DECs | 2 |
| In-review DECs | 1 |
| Total BRs covered | 5 of 6 (**83%**) |
| Total BEHs addressed | 3 of 3 (**100%**) |
| Evidence grounding | all DECs have ≥2 EV |
| Blocking TBDs | 2 (must resolve before handoff) |
| Critical risks | 1 (legacy decomposition) |
| Readiness for handoff | pending TBD resolution (ETA 2026-05-27) |

---

## Document Metadata

- **Generated by**: legacy-modernization-decision-writer skill
- **Generated**: YYYY-MM-DD
- **Last Updated**: YYYY-MM-DD by `<name>`
- **Spec Version**: `05_specs/<CAP-SLUG>/spec.yaml` (v0.1)
- **Schema**: `schemas/spec.schema.yaml` (v0.1)
