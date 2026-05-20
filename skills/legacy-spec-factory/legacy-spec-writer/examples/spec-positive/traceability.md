# Traceability: SPEC-CARD-AUTH-CREDLIM-001

Cross-reference report. Every approved Business Rule must trace to at
least one Evidence item and at least one Acceptance Criterion.

## BR → EV / BEH / AC / TC Walk

### BR-CARD-AUTH-CREDLIM-001 — Credit limit decline (approved)
- **Supporting Evidence:**
  - EV-CARD-AUTH-CREDLIM-001 (code: CREDITCHK validation logic) — `confirmed_from_code`
  - EV-CARD-AUTH-CREDLIM-003 (DDS: CREDLIMIT field type) — `confirmed_from_code`
  - EV-CARD-AUTH-CREDLIM-004 (SME: Anna Chen) — `confirmed_by_sme`
- **Linked Behaviors:**
  - BEH-CARD-AUTH-CREDLIM-001 (CREDITCHK compares amount vs limit)
- **Validating Acceptance Criteria:**
  - AC-CARD-AUTH-CREDLIM-001 (60000 > 50000 → DECLINED with reason 51, audit)
- **Tests (sketch):** TC pending; will be implemented in equivalence-test layer
- **Verdict:** ✅ approvable — multiple confirmed evidence + 1 AC

### BR-CARD-AUTH-CREDLIM-002 — Audit before response (approved)
- **Supporting Evidence:**
  - EV-CARD-AUTH-CREDLIM-002 (code: CU110A audit WRITE) — `confirmed_from_code`
  - EV-CARD-AUTH-CREDLIM-004 (SME: Anna Chen) — `confirmed_by_sme`
- **Linked Behaviors:**
  - BEH-CARD-AUTH-CREDLIM-002 (CU110A always writes TXNLOGPF before response)
- **Validating Acceptance Criteria:**
  - AC-CARD-AUTH-CREDLIM-001 (audit before response, decline path)
  - AC-CARD-AUTH-CREDLIM-002 (audit before response, approve path)
  - AC-CARD-AUTH-CREDLIM-003 (audit-write-failure handling)
- **Verdict:** ✅ approvable — confirmed evidence + 3 ACs covering happy/decline/failure

### BR-CARD-AUTH-CREDLIM-003 — ISO 8583 code 51 mapping (needs_sme_review)
- **Supporting Evidence:**
  - EV-CARD-AUTH-CREDLIM-005 (code: CU110A response-builder) — `confirmed_from_code`
- **Linked Behaviors:**
  - BEH-CARD-AUTH-CREDLIM-003
- **Validating Acceptance Criteria:**
  - none yet (BR not approved → AC not written)
- **Blocking TBDs:**
  - TBD-CARD-AUTH-CREDLIM-001 (per-network universality unclear)
- **Verdict:** ⏸ on hold — cannot promote to approved until TBD-001 resolved

## DEC Walk

### DEC-CARD-AUTH-CREDLIM-001 — sync gRPC + fallback (draft)
- **Rationale ties to:** BR-001 (real-time enforcement)
- **Reviewer pending:** David Park (Integration Architect)
- **Blocking TBD:** TBD-002 (fallback policy)

### DEC-CARD-AUTH-CREDLIM-002 — Kafka audit log (draft)
- **Rationale ties to:** BR-002 (durable audit before response)
- **Reviewer pending:** Maria Lopez (Data Architect)

## Evidence Coverage Audit

| EV ID | Used By |
| --- | --- |
| EV-001 | BR-001, BEH-001, STEP-001, STEP-003, IN-001 |
| EV-002 | BR-002, BEH-002, STEP-004, DEC-002, OUT-002, EX-002 |
| EV-003 | BR-001, BEH-001, STEP-002, data_model |
| EV-004 | BR-001, BR-002, EX-001 |
| EV-005 | BR-003, BEH-003, STEP-005, OUT-001 |

✅ No orphan evidence; every EV referenced by ≥1 spec element.

## AC Coverage Audit

| AC ID | Validates | BR Status |
| --- | --- | --- |
| AC-001 | BR-001, BR-002 | both approved |
| AC-002 | BR-002 | approved |
| AC-003 | BR-002 | approved |

✅ No orphan ACs; every AC validates approved BRs only.

## BR → AC Coverage Audit

| BR ID | Has ≥1 AC? | Status OK? |
| --- | --- | --- |
| BR-001 | ✅ AC-001 | approved + AC = OK |
| BR-002 | ✅ AC-001, AC-002, AC-003 | approved + AC = OK |
| BR-003 | ❌ | needs_sme_review → not yet required to have AC |

✅ Every approved BR has at least one AC.

## Forward-Handoff Gate Verdict

To reach `status: approved`:

- [X] Every approved BR has ≥1 confirmed-strength evidence
- [X] Every approved BR has ≥1 approved AC
- [X] Every approved AC validates an approved BR
- [ ] No `blocking: yes` TBD without SME waiver — **NO**, TBD-001 is blocking and not waived
- [X] No `evidence_strength: missing` in data model
- [X] Capability owner SME signed off — yes for BR-001/002; pending for BR-003

**Verdict:** ⏸ blocked on TBD-001 (BR-003 universality). Spec remains
`in_review` until TBD-001 is resolved.

When TBD-001 resolves and BR-003 is either:
- approved → write AC-004 validating BR-003 → traceability rerun → status `approved`
- rejected → remove BR-003 and BEH-003 → traceability rerun → status `approved`
