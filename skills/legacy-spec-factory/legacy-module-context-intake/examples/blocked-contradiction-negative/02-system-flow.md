# View 2: System Flow - Payment Matching

## Intake Status
- status: blocked
- source_state: rag_hydrated
- primary_sources:
  - SNP-PAYMENT-001
  - RUN-PAYMENT-JOBLOG-001

## Summary

The payment matching subsystem sits between the bank file ingest and the AR
ledger update. `PMTMATCH` reads from `PMTINPUT`, joins against open invoice
records in `INVOICEDB`, and writes to the AR balance table and suspense file.

**This view is blocked pending resolution of RAG-CONFLICT-PAYMENT-MATCH-001.**
Trigger model (scheduled batch vs event-driven) affects interface and SLA design.

## Evidence-Linked Details

| Claim ID | Knowledge Type | Statement | Evidence | Strength | Review Status |
| --- | --- | --- | --- | --- | --- |
| VIEW2-PMATCH-001 | observed_behavior | `PMTMATCH` is the entry program and calls no external services. | SNP-PAYMENT-001 | confirmed_from_code | needs_sme_review |
| VIEW2-PMATCH-002 | observed_behavior | Bank payment flat file `PMTINPUT` is the only upstream input. | SNP-PAYMENT-001 | confirmed_from_code | needs_sme_review |
| VIEW2-PMATCH-003 | observed_behavior | Job `PMTMATCH` appears in weekly schedule in runtime job log. | RUN-PAYMENT-JOBLOG-001 | confirmed_from_runtime | contradicts_sme |

## Candidate Seeds

| Candidate ID | Candidate Statement | Business Signal | Evidence Basis | Required Review |
| --- | --- | --- | --- | --- |
| RAG-CAND-PAYMENT-MATCH-003 | Trigger model is scheduled batch rather than event-driven. | Payment posting timeliness, interface design, and SLA expectations depend on the trigger model. | RUN-PAYMENT-JOBLOG-001; `PMTMATCH` | blocked_pending_contradiction_review |

## Gaps For Module Analyzer

| TBD ID | Category | Question | Evidence | Owner | Blocking |
| --- | --- | --- | --- | --- | --- |
| TBD-PAYMENT-MATCH-001 | frequency | Daily vs weekly trigger affects SLA and interface design. | SME-PAYMENT-MATCH-001, RUN-PAYMENT-JOBLOG-001 | AR Operations SME | yes |
