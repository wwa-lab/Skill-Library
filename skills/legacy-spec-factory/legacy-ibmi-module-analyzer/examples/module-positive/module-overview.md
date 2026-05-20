# Module: Card Authorization (MODULE-CARD-AUTH-001)

## Metadata
- **Module ID:** MODULE-CARD-AUTH-001
- **Business Name:** Card Authorization
- **Scope Statement:** Processes on-us card authorization requests from external networks (Visa, Mastercard), supports manual authorization via CSR menu, and performs nightly reconciliation against GL. Excludes settlement (handled by separate module SETTLEMENT) and dispute handling (CHARGEBACK module).
- **Module Owner:** Anna Chen (Card Operations Lead) — confirmed scope and boundaries 2026-05-12
- **In-scope Flows:**
  - FLOW-ONUS-AUTH-001 — On-us authorization request (API/MQ)
  - FLOW-MANUAL-AUTH-001 — Manual authorization via CSR menu
  - FLOW-NIGHTLY-RECON-001 — Nightly reconciliation (Scheduler+Batch)
- **Status:** draft → needs_sme_review

## View Index
| View | File | Status | Reviewer |
| --- | --- | --- | --- |
| 1. Operation Flow | 01-operation-flow.md | draft | Anna Chen (Card Ops) |
| 2. System Flow | 02-system-flow.md | draft | David Park (Integration Architect) |
| 3. Program Flow | 03-program-flow.md | draft | Liu Wei (Dev Lead) |
| 4. Data Flow | 04-data-flow.md | draft | Maria Lopez (Data Analyst) |

## Top Blocking TBDs (aggregated across all views)

- **TBD-CARD-AUTH-001** (pending_source): GL system's downstream consumer
  not in this repo; need cross-module agreement on GLPOSTPF schema
- **TBD-CARD-AUTH-002** (pending_sme): Confirm whether RC=-2 threshold in
  nightly reconciliation is regulatory or operational policy
- **TBD-CARD-AUTH-003** (pending_sme): CVV verification — required for
  all auths or only ATMP? (capability seed BR-02)

## Capability Seeds For spec-writer

| CAP Seed | Suggested By | SME Question |
| --- | --- | --- |
| CAP-CARD-AUTH-001 | View 1 actors + View 3 entry programs | Is "On-Us Authorization" a distinct capability or part of broader "Authorization"? |
| CAP-CARD-AUTH-002 | View 1 BAU + View 3 nightly recon flow | Is "Daily Reconciliation" a separate capability or part of "Authorization"? |
| CAP-CARD-AUTH-003 | View 1 BR seeds | Is "Credit Limit Enforcement" its own capability or a rule within "Authorization"? |

## Module Review Checklist

- [ ] All four views are at least `approved_with_non_blocking_tbd`
- [ ] Cross-view consistency check passed
  - [X] Every actor in View 1 maps to entry node in View 3 — Cardholder/Merchant → Visa MQ entry, Risk Officer → manual_actor: yes
  - [X] Every system in View 2 appears in View 3 — Visa, GL, Risk Monitoring all referenced
  - [X] Every BR seed in View 1 references program/file — all 4 seeds traced
  - [X] Every data object in View 4 traces to flow in View 3 — all traced
- [ ] No blocking TBDs remain — 3 blocking TBDs pending
- [ ] Capability seeds list is complete and SME-confirmed
- [ ] Module ready for spec-writer

## Sign-Off
- **Module Owner:** Anna Chen — pending
- **Date:** —
- **Decision:** pending (3 blocking TBDs)
