# View 1: Operation / Business Flow - Payment Matching

## Intake Status
- status: blocked
- source_state: mixed
- primary_sources:
  - SME-PAYMENT-MATCH-001
  - SNP-PAYMENT-001

## Summary

Payment matching receives incoming bank payment files, looks up open invoices for
each payment, and posts matched amounts to the account receivable ledger. Unmatched
or partial payments are held in a suspense queue for manual review.

**This view is blocked pending resolution of RAG-CONFLICT-PAYMENT-MATCH-001.**
The matching frequency (daily EOD vs weekly batch) materially changes the business
flow and cannot be assumed.

## Evidence-Linked Details

| Claim ID | Knowledge Type | Statement | Evidence | Strength | Review Status |
| --- | --- | --- | --- | --- | --- |
| VIEW1-PMATCH-001 | observed_behavior | Incoming bank payment records are received for matching. | SNP-PAYMENT-001 | confirmed_from_code | needs_sme_review |
| VIEW1-PMATCH-002 | observed_behavior | Unmatched payments are routed to suspense for manual review. | SNP-PAYMENT-002 | confirmed_from_code | needs_sme_review |
| VIEW1-PMATCH-003 | sme_stated | SME states all payments must be matched and posted before EOD each business day. | SME-PAYMENT-MATCH-001 | sme_unconfirmed | contradicted_by_runtime |
| VIEW1-PMATCH-004 | observed_behavior | Runtime job log shows batch job `PMTMATCH` scheduled weekly, not daily. | RUN-PAYMENT-JOBLOG-001 | confirmed_from_runtime | contradicts_sme |

## Candidate Seeds

| Candidate ID | Candidate Statement | Business Signal | Evidence Basis | Required Review |
| --- | --- | --- | --- | --- |
| RAG-CAND-PAYMENT-MATCH-001 | Matching frequency is daily EOD. | Payment posting SLA and operational staffing depend on how often matching runs. | SME-PAYMENT-MATCH-001; RUN-PAYMENT-JOBLOG-001 | blocked_pending_contradiction_review |
| RAG-CAND-PAYMENT-MATCH-002 | Suspense items must be cleared within 2 business days. | Exception backlog timing affects AR follow-up and customer account accuracy. | SME-PAYMENT-MATCH-001 | needs_sme_review |

## Gaps For Module Analyzer

| TBD ID | Category | Question | Evidence | Owner | Blocking |
| --- | --- | --- | --- | --- | --- |
| TBD-PAYMENT-MATCH-001 | frequency | Is matching run daily EOD or weekly? SME note conflicts with runtime job log. | SME-PAYMENT-MATCH-001, RUN-PAYMENT-JOBLOG-001 | AR Operations SME | yes |
