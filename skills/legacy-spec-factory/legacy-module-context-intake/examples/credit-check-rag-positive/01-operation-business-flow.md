# View 1: Operation / Business Flow - Credit Check

## Intake Status
- status: ready_for_module_analysis
- source_state: mixed
- primary_sources:
  - RAG-20260521-001
  - SNP-CREDIT-CHECK-004
  - RUN-CREDIT-CHECK-SPOOL-001
  - SME-CREDIT-CHECK-001

## Summary

Customer service submits a customer number and requested order amount for credit
evaluation. The supplied context says the observed legacy path returns an
approve or deny decision and an approved amount. The over-limit runtime sample
shows a denied request with the available credit amount returned for reference.

## Evidence-Linked Details

| Claim ID | Knowledge Type | Statement | Evidence | Strength | Review Status |
| --- | --- | --- | --- | --- | --- |
| CTX-CREDIT-CHECK-OP-001 | observed_behavior | The decision path compares requested amount to available credit. | SNP-CREDIT-CHECK-004 | confirmed_from_code | needs_sme_review |
| CTX-CREDIT-CHECK-OP-002 | observed_behavior | One runtime sample denied an over-limit request and returned the available amount. | RUN-CREDIT-CHECK-SPOOL-001 | observed_in_runtime | needs_sme_review |
| CTX-CREDIT-CHECK-OP-003 | inferred_business_rule | Missing, inactive, and over-limit outcomes are candidate rule areas only. | RAG-CAND-CREDIT-CHECK-001, RAG-CAND-CREDIT-CHECK-002, RAG-CAND-CREDIT-CHECK-004 | needs_sme_review | needs_sme_review |

## Candidate Seeds

| Candidate ID | Candidate Statement | Business Signal | Evidence Basis | Required Review |
| --- | --- | --- | --- | --- |
| RAG-CAND-CREDIT-CHECK-001 | Missing customers are denied by default. | Customer service cannot continue order release when the account cannot be resolved. | SNP-CREDIT-CHECK-003, SNP-CREDIT-CHECK-004 | Credit Operations SME |
| RAG-CAND-CREDIT-CHECK-002 | Inactive customers are denied even if credit exists. | Customer eligibility status can override available credit. | SNP-CREDIT-CHECK-004, SME-CREDIT-CHECK-001 | Credit Operations SME |
| RAG-CAND-CREDIT-CHECK-004 | Requests over available credit are denied and return available credit as the maximum approvable amount. | Over-limit orders are blocked, but the response exposes the amount that may be approvable. | SNP-CREDIT-CHECK-004, RUN-CREDIT-CHECK-SPOOL-001 | Credit Operations SME |

## Gaps For Module Analyzer

| TBD ID | Category | Question | Evidence | Owner | Blocking |
| --- | --- | --- | --- | --- | --- |
| TBD-CREDIT-CHECK-001 | pending_sme_judgment | Are over-limit denials audited, queued, or simply rejected inline? | RAG-GAP-CREDIT-CHECK-004 | Credit Operations SME | no |
