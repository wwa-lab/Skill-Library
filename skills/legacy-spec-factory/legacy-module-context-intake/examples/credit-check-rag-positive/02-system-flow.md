# View 2: System Flow - Credit Check

## Intake Status
- status: ready_for_module_analysis
- source_state: rag_hydrated
- primary_sources:
  - RAG-20260521-001
  - SNP-CREDIT-CHECK-001
  - SNP-CREDIT-CHECK-003
  - RUN-CREDIT-CHECK-JOBLOG-001

## Summary

The operational wrapper `CRDTCMD` calls `CREDITCHK`. `CREDITCHK` reads credit
status and available credit from `CREDITVW`, writes denial or error messages to
`QSYSPRT`, sets the approved amount output parameter, and returns a decision.
Whether the wrapper captures the returned decision is not proven by the wrapper
source.

## Evidence-Linked Details

| Claim ID | Knowledge Type | Statement | Evidence | Strength | Review Status |
| --- | --- | --- | --- | --- | --- |
| CTX-CREDIT-CHECK-SYS-001 | observed_behavior | `CRDTCMD` calls `CREDITCHK`. | SNP-CREDIT-CHECK-001 | confirmed_from_code | needs_sme_review |
| CTX-CREDIT-CHECK-SYS-002 | observed_behavior | `CREDITCHK` reads status and available credit from `CREDITVW`. | SNP-CREDIT-CHECK-003 | confirmed_from_code | needs_sme_review |
| CTX-CREDIT-CHECK-SYS-003 | unknown_tbd | It is not visible whether `CRDTCMD` captures the RPG return decision. | RAG-GAP-CREDIT-CHECK-005 | missing | needs_sme_review |

## Candidate Seeds

| Candidate ID | Candidate Statement | Business Signal | Evidence Basis | Required Review |
| --- | --- | --- | --- | --- |
| RAG-ASM-CREDIT-CHECK-002 | Full program analysis should confirm where the credit decision is made and whether the wrapper preserves that decision. | Credit approval behavior may be owned downstream of the operational wrapper. | `CREDITCHK`, `CRDTCMD`; SNP-CREDIT-CHECK-003, SNP-CREDIT-CHECK-004 | IBM i developer |

## Gaps For Module Analyzer

| TBD ID | Category | Question | Evidence | Owner | Blocking |
| --- | --- | --- | --- | --- | --- |
| TBD-CREDIT-CHECK-002 | pending_source | Does the wrapper use or discard the returned credit decision? | RAG-GAP-CREDIT-CHECK-005; `CREDITCHK` | IBM i developer | yes |
