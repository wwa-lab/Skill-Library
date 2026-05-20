<!--
TEMPLATE NOTE
This file is a structure-and-narrative template. It illustrates a richer
rendering of the same Credit Limit Enforcement capability used by the
companion `sdd-handoff.yaml` template, but the two templates are
intentionally not byte-equivalent: `sdd-handoff.yaml` shows a minimal
structural skeleton (2 BR, 3 AC, 2 DEC, 2 EX, 1 TBD) while this `.md`
template shows the richer narrative (5 BR, 6 AC, 4 DEC, 2 EX, 1 TBD)
that a fully populated handoff would contain.

In a real run, both files are emitted from the same approved spec and BRD,
so their counts and content WILL match. The templates diverge here only
to demonstrate two presentation levels of the same shape.
-->

# SDD Handoff Package — Atlas SDD Chain Input
## Credit Limit Enforcement

**Handoff ID:** `HANDOFF-CREDIT-CHECK-2026-05-16`  
**Capability ID:** `CAP-CREDIT-CHECK-001`  
**Status:** `approved`  
**Prepared:** 2026-05-16 at 14:32 UTC  
**Validator:** Claude Code / legacy-brd-to-sdd-handoff v0.1.0

---

## Executive Summary

The **Credit Limit Enforcement** capability has been analyzed through the
Legacy Spec Factory reverse chain and is ready for consumption by the Atlas
Software Design and Development (SDD) chain.

- **Business Context**: Credit limit enforcement prevents credit exposure on orders by validating that no customer exceeds their authorized credit threshold.
- **Source**: IBM i legacy system CARD-AUTH module (analyzed 2026-05-01 to 2026-05-14)
- **BRD Status**: Approved by John Smith (Credit Policy Manager) on 2026-05-15
- **Spec Status**: Approved by John Smith (Credit Policy Manager) on 2026-05-15
- **Handoff Status**: **APPROVED** — no blocking TBDs, all rules have acceptance criteria, all evidence cleared, SME sign-off present

The Atlas SDD chain may proceed with `req-to-user-story` (or its team's
preferred entry point). All implementation, architecture, and design
decisions are owned by Atlas; this package only carries approved legacy
behaviour and approved `DEC-*` forward.

---

## Capability Scope

### In Scope
- Credit limit validation for online and phone orders
- Rejection of orders that exceed customer credit limit
- Error messaging and transaction logging
- Return codes and error handling

### Out of Scope
- Cash/check orders (no credit limit applies)
- Internal admin overrides (separate process)
- Credit limit modification or adjustment workflows (separate capability)
- Daily credit limits (deferred to Phase 2 per TBD-CREDIT-CHECK-001)

### Business Owner
**John Smith**  
Title: Credit Policy Manager  
Email: john.smith@company.com

---

## Business Rules Summary

**5 approved business rules** govern this capability:

1. **BR-CREDIT-CHECK-001** — Orders exceeding customer's authorized credit limit are rejected with error code 42
   - Evidence: program analysis, flow analysis, runtime evidence
   - Confidence: HIGH
   - Acceptance Criteria: 2 (error code 42, error message "Credit limit exceeded")

2. **BR-CREDIT-CHECK-002** — Credit limit is read from CUSTPF customer master file
   - Evidence: flow analysis, confirmed from code
   - Confidence: HIGH
   - Acceptance Criteria: 1 (correct CUSTPF read)

3. **BR-CREDIT-CHECK-003** — System logs all credit rejections to AUDITPF for audit trail
   - Evidence: program analysis, runtime evidence
   - Confidence: HIGH
   - Acceptance Criteria: 1 (audit log contains required fields)

4. **BR-CREDIT-CHECK-004** — Customer not found errors return code 99
   - Evidence: flow analysis
   - Confidence: MEDIUM
   - Acceptance Criteria: 1 (error code 99 when customer missing)

5. **BR-CREDIT-CHECK-005** — Non-credit orders (cash, check) bypass credit limit check
   - Evidence: inferred from code, needs SME confirmation
   - Confidence: MEDIUM
   - Acceptance Criteria: 1 (non-credit orders always approved)

---

## Acceptance Criteria

All 6 acceptance criteria are **approved** and ready for test case generation:

| AC ID | Rule ID | Criterion | Priority |
| --- | --- | --- | --- |
| AC-CREDIT-CHECK-001 | BR-CREDIT-CHECK-001 | Order rejected with error code 42 when amount exceeds limit | P0 |
| AC-CREDIT-CHECK-002 | BR-CREDIT-CHECK-001 | Error message 'Credit limit exceeded' is returned to caller | P0 |
| AC-CREDIT-CHECK-003 | BR-CREDIT-CHECK-002 | Credit limit correctly read from CUSTPF customer master file | P0 |
| AC-CREDIT-CHECK-004 | BR-CREDIT-CHECK-003 | All credit rejections logged to AUDITPF with timestamp, customer ID, amount, limit | P0 |
| AC-CREDIT-CHECK-005 | BR-CREDIT-CHECK-004 | Missing customer returns error code 99 to caller | P1 |
| AC-CREDIT-CHECK-006 | BR-CREDIT-CHECK-005 | Non-credit orders (cash, check, etc.) always approved regardless of credit limit | P1 |

---

## Data Model

### Customer (legacy: CUSTPF)

| Legacy Field | Target Field | Type | Notes |
| --- | --- | --- | --- |
| CUSTID | customer_id | varchar(10) | Customer identifier; primary key |
| CRDLIM | credit_limit | decimal(9,2) | Authorized credit limit |
| CRDUSD | credit_used | decimal(9,2) | Amount currently in use (open orders + invoices) |

---

## Inputs and Outputs

### Input: Order Request
- **Source**: order-entry-service
- **Format**: JSON
- **Required Fields**: customer_id, order_amount, order_type
- **Example**: `{ "customer_id": "C001234", "order_amount": 5000.00, "order_type": "CREDIT" }`

### Output: Credit Decision
- **Target**: order-entry-service
- **Format**: JSON
- **Fields**: decision (approve|reject), reason (if rejected), available_credit
- **Example**: `{ "decision": "reject", "reason": "Credit limit exceeded", "available_credit": 0.00 }`

---

## Exceptions and Error Codes

Carried forward verbatim from the spec's `exceptions[]`. Only exceptions
present in the approved spec appear here — this skill does not invent
additional error cases (HTTP status codes, retry policies, circuit-breaker
behaviour, etc. are Atlas-chain concerns).

| Exception | Condition | Expected Behavior | Severity |
| --- | --- | --- | --- |
| EX-CREDIT-CHECK-001 | Customer record not found in CUSTMSTR | Return error code 99 (customer not found) to caller | error |
| EX-CREDIT-CHECK-002 | Order amount is zero or negative | Treat as non-credit; approve without limit check | info |

---

## Modernization Decisions

**4 approved architectural decisions** have been recorded:

1. **DEC-CREDIT-CHECK-001** — Implement as reusable Spring Boot service
   - Rationale: Allows order-entry, billing, and other contexts to call independently
   - Trade-off: Service boundary adds network hop vs. monolithic
   - Impact: Enables independent scaling and testing

2. **DEC-CREDIT-CHECK-002** — Use PostgreSQL CUSTMSTR table for credit limits
   - Rationale: CUSTMSTR is the master data source in legacy; preserved for accuracy
   - Trade-off: Synchronization required if limits changed outside system
   - Impact: Simplifies data migration; one source of truth

3. **DEC-CREDIT-CHECK-003** — Implement distributed tracing for audit trail
   - Rationale: Modern audit service replaces AUDITPF; provides real-time visibility
   - Trade-off: Legacy AUDITPF queries no longer available; new audit search UI required
   - Impact: Improved compliance reporting; no batch audit runs needed

4. **DEC-CREDIT-CHECK-004** — Implement caching for credit limits with 5-minute TTL
   - Rationale: Reduces database load; acceptable staleness for most orders
   - Trade-off: Cache-miss scenarios must handle stale data gracefully
   - Impact: Improved performance; must handle cache invalidation on limit changes

---

## Test Plan

**3 golden master test cases** are planned to compare legacy and new-system behavior:

| Test Case | Title | Acceptance Criteria | Golden Master |
| --- | --- | --- | --- |
| TC-CREDIT-CHECK-001 | Order approved when amount below limit | AC-CREDIT-CHECK-001, AC-CREDIT-CHECK-003 | yes |
| TC-CREDIT-CHECK-002 | Order rejected when amount exceeds limit | AC-CREDIT-CHECK-001 | yes |
| TC-CREDIT-CHECK-003 | Customer not found error | AC-CREDIT-CHECK-005 | no (error path) |

Additional test cases for edge cases (negative amounts, zero amounts, currency rounding) will be generated by the Atlas SDD chain.

---

## Known Issues and Open Questions

**1 non-blocking open question is deferred to Phase 2:**

**TBD-CREDIT-CHECK-001**: Should the system apply a daily credit limit in addition to the per-order limit?
- **Current Status**: Deferred to Phase 2
- **Deferred By**: John Smith, Credit Policy Manager
- **Planned Resolution Date**: 2026-06-30
- **Notes**: Not in scope for Phase 1; current legacy system has no daily limit; revisit after Go-Live and collect user feedback

---

## Evidence and Traceability

All 8 evidence records satisfy the approved evidence-manifest contract:

| Evidence ID | Type | Source | Sensitivity | Redaction |
| --- | --- | --- | --- | --- |
| EV-CREDIT-CHECK-001 | program_analysis | 02_programs/CREDIT-CHECK/program-analysis.md | public | not_required |
| EV-CREDIT-CHECK-002 | flow_analysis | 03_flows/CREDIT-CHECK/credit-check-auth/flow.md | public | not_required |
| EV-CREDIT-CHECK-003 | runtime_evidence | sample transaction logs | confidential | approved |
| EV-CREDIT-CHECK-004 | data_dictionary | CUSTPF DDS | public | not_required |
| EV-CREDIT-CHECK-005 | inventory | 01_inventory/CREDIT-CHECK/inventory.yaml | internal | reviewed |
| ... | ... | ... | ... | ... |

**Traceability Matrix**: See `traceability.md` for complete cross-reference mapping.

---

## Handoff Checklist

All handoff gate checks have **PASSED**:

- ✅ BRD approved and signed by SME
- ✅ Spec approved and signed by SME
- ✅ No blocking TBDs
- ✅ Every approved BR has acceptance criteria
- ✅ All acceptance criteria approved
- ✅ All evidence satisfies the approved evidence-manifest contract
- ✅ Traceability matrix is complete
- ✅ Assumptions documented
- ✅ Modernization decisions recorded
- ✅ Test cases identified

---

## Assumptions Carried Forward

Only assumptions explicitly recorded in the approved spec or BRD appear here.
The handoff validator does **not** mint new assumptions.

1. **Assumption**: CUSTPF contains all active and inactive customer records; service will query live
   - **Rationale**: Customer master is System of Record; all credit decisions depend on CUSTPF
   - **Impact**: Downstream service must handle missing customer gracefully (error code 99)
   - **Source**: spec.yaml#assumptions[0]

2. **Assumption**: Credit limit values in CUSTPF are always valid decimal(9,2)
   - **Rationale**: Observed in all analyzed transactions; DDS confirms numeric(9,2)
   - **Impact**: No currency conversion needed; all comparisons are numeric
   - **Source**: spec.yaml#assumptions[1]

---

## Notes for the Atlas SDD Chain

This handoff intentionally does **not** recommend frameworks, deployment
topologies, or integration patterns. Architecture, design, and code are
owned by the Atlas SDD chain (`spec-to-architecture`,
`architecture-to-design`, `tasks-to-code`).

The only forward-looking content carried into the package is the set of
approved modernization decisions (`DEC-*`) listed above. If a topic is not
covered by a `DEC-*`, it has not yet been decided. The Atlas chain will
either make the decision or surface it back to `legacy-spec-writer` as a
new `TBD-*`.

Practical guidance the Atlas chain may safely rely on:

- every approved `BR-*` has at least one approved `AC-*` (suitable seed for
  `req-to-user-story`)
- every approved `BR-*` traces back to legacy evidence via `EV-*`
- non-blocking `TBD-*` items are explicit, named, and dated — they should
  appear as tagged backlog items, not as silent risk
- evidence manifest status is approved for inventory; the handoff is safe to
  share with downstream agents

---

## Sign-Offs

### Business Requirements Document (BRD)
- **Approved By**: John Smith, Credit Policy Manager
- **Date**: 2026-05-15
- **Status**: Approved

### Technical Specification (Spec)
- **Approved By**: John Smith, Credit Policy Manager  
- **Date**: 2026-05-15
- **Status**: Approved
- **All Required Approvals**: business_rules ✅ | acceptance_criteria ✅ | modernization_decisions ✅

### Handoff Package
- **Validated By**: Claude Code / legacy-brd-to-sdd-handoff v0.1.0
- **Validation Date**: 2026-05-16 at 14:32 UTC
- **Approved By**: John Smith, Credit Policy Manager
- **Approval Date**: 2026-05-16
- **Status**: **APPROVED**
- **Routing**: Ready for Atlas SDD chain

---

## Next Steps

The Atlas SDD chain takes ownership at this point. This skill does not
orchestrate, decide, or shortcut the steps below — it only delivers the
sealed package they consume.

1. Atlas `req-to-user-story` reads `atlas-context-pack.json` and seeds
   stories from approved `BR-*` and `AC-*`.
2. Atlas `user-story-to-spec`, `spec-to-architecture`, and
   `architecture-to-design` decide framework, deployment, and integration
   topology, honouring any approved `DEC-*` already carried in this
   package (e.g. `DEC-CREDIT-CHECK-001` if present).
3. Atlas `design-to-tasks` and `tasks-to-code` produce the implementation
   and the test suite.
4. Golden-master comparison uses the `TC-*` listed in this package to
   validate equivalence against the legacy system.
5. The capability owner revisits deferred `TBD-*` items
   (e.g. TBD-CREDIT-CHECK-001) on their named resolution dates.

---

## Appendix: Handoff Package Contents

This handoff package includes:

- `sdd-handoff.yaml` — Canonical machine-readable contract (this file)
- `sdd-handoff.md` — Human-readable handoff summary (this document)
- `atlas-context-pack.json` — Agent-consumable capability context bundle
- `handoff-review.md` — Detailed gate checklist and findings
- `traceability.md` — Complete cross-reference matrix

All files are derived from and consistent with the approved BRD and Spec.
