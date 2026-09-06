# Module Review Checklist — Card Authorization

## Module-Level Sign-Off

- [ ] All four views are approved (or approved_with_non_blocking_tbd)
  - View 1: draft → needs_sme_review (2 pending SME)
  - View 2: draft → needs_sme_review (1 pending source for GL contract)
  - View 3: draft → needs_sme_review (1 pending SME on cross-module CREDITCHK)
  - View 4: draft → needs_sme_review (2 pending source/SME)

- [X] Cross-view consistency verified
  - [X] Every actor (View 1) maps to a node (View 3) OR `manual_actor: yes` — Cardholder/Merchant → ACTOR-01/02 → Visa entry in View 3; CSR → ACTOR-04 → MANAUTH; Risk/Ops/Finance → manual_actor
  - [X] Every system (View 2) appears in View 3 — Visa, Mastercard, CSR Workstation, Scheduler, GL, Risk Monitoring, Compliance — all match flow triggers/exits
  - [X] Every BR seed (View 1) references supporting evidence (View 3/4 or SME note) — all 6 seeds traced
  - [X] Every data object (View 4) traces to a flow (View 3) — all 8 objects traced
  - [X] Every flow (View 3) touches at least one data object (View 4) — confirmed

- [ ] No blocking TBDs remain — 3 blocking TBDs across views
- [ ] Capability seeds list is complete and SME-confirmed
- [ ] Module ready for BRD writer — not yet (blockers above)

## Per-View Reviewers

- **View 1 (Business):** Anna Chen — pending — needs_sme_review
- **View 2 (Integration):** David Park — pending — needs_sme_review
- **View 3 (Application):** Liu Wei — pending — needs_sme_review
- **View 4 (Data):** Maria Lopez — pending — needs_sme_review

## Module Owner Sign-Off

- **Anna Chen (Module Owner):** pending
- **Date:** —
- **Decision:** pending until per-view reviews complete

## Next Steps

1. Each SME reviews their view independently
2. Resolve 3 blocking TBDs:
   - GL system schema contract (TBD-CARD-AUTH-001) → cross-team coordination
   - BR-01 regulatory framing (TBD-CARD-AUTH-002) → Anna Chen + compliance
   - CVV scope (TBD-CARD-AUTH-003) → Anna Chen + Risk Officer
3. Once all four views are at least `approved_with_non_blocking_tbd`,
   module is ready for `legacy-brd-writer` to produce one BRD Package per
   selected capability seed before spec-writing.
