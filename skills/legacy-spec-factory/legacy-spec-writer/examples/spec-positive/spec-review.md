# Spec Review: Credit Limit Enforcement (SPEC-CARD-AUTH-CREDLIM-001)

## Status: in_review

## Capability Owner
Anna Chen (Card Operations, AMH partition) — confirmed scope and BR-001/BR-002 on 2026-05-12.

## Review Pass Status

| Section | Reviewer | Date | Decision | Notes |
| --- | --- | --- | --- | --- |
| Capability scope | Anna Chen | 2026-05-12 | approved | Confirmed boundaries vs SETTLEMENT and CHARGEBACK |
| Evidence bundle | Anna Chen | 2026-05-12 | approved | All EV present, no sensitive raw data inlined |
| BR-001 (credit limit decline) | Anna Chen | 2026-05-12 | **approved** | "This is the core rule. Required by PBOC consumer-lending regulation." |
| BR-002 (audit before response) | Anna Chen | 2026-05-12 | **approved** | "Hard requirement; compliance audit relies on log being complete." |
| BR-003 (ISO 8583 code 51) | Anna Chen | 2026-05-12 | **needs_sme_review** | Anna referred to David Park; possible per-network nuance |
| DEC-001 (sync gRPC + cache fallback) | TBD | — | draft | Awaiting integration architect (David Park) |
| DEC-002 (Kafka audit log) | TBD | — | draft | Awaiting data architect (Maria Lopez) |
| Acceptance criteria | Anna Chen | 2026-05-12 | approved (AC-001, AC-002, AC-003) | All testable; gherkin shape matches existing test culture |
| Process flow | Anna Chen | 2026-05-12 | approved | 5 steps map to operational understanding |
| Data model | Maria Lopez | 2026-05-12 | approved | AuthorizationDecision entity matches TXNLOGPF; no missing fields |
| Exceptions | Anna Chen | 2026-05-12 | approved | EX-001 and EX-002 reflect real production failure modes |

## Blocking Open Questions

- **TBD-001 (BR-003 universality):** Anna needs David Park to confirm
  whether all external networks use ISO 8583 code 51, or there's
  per-network nuance. Until resolved, BR-003 stays `needs_sme_review` and
  no AC has been written for it.
- **TBD-002 (Customer Master fallback policy):** Anna needs SME (probably
  herself + risk team) to decide between strict decline vs. cache fallback.

## Non-Blocking Notes

- BR-001 implicitly assumes "outstanding balance < credit limit" semantics.
  Anna confirmed: yes, balance includes all currently in-flight
  authorizations not yet settled — this is the legacy behavior and the
  target must match.

## Sign-Off

- **Anna Chen (Capability Owner):** approved with 2 blocking TBDs noted
- **Date:** 2026-05-12
- **Decision:** in_review (cannot move to `approved` until TBD-001 + TBD-002 resolved)

## Next Steps

1. David Park to confirm BR-003 (ISO 8583 code 51 universality)
2. Anna + Risk team to decide on fallback policy (TBD-002)
3. David Park to approve DEC-001 (sync gRPC pattern)
4. Maria Lopez to approve DEC-002 (Kafka audit log)
5. Once all approved, spec status → `approved` and ready for `build-agent-skill`
