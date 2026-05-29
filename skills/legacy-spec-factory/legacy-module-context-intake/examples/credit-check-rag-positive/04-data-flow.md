# View 4: Data Flow - Credit Check

## Intake Status
- status: ready_for_module_analysis
- source_state: mixed
- primary_sources:
  - RAG-20260521-001
  - DDS-CREDIT-CHECK-CUSTMAST-001
  - DDS-CREDIT-CHECK-CREDITVW-001
  - DD-CREDIT-AVAILABLE-AMOUNT

## Summary

`CREDITVW` exposes `CUSTNO`, `STATUS`, and `AVAIL_CREDIT`. The logical file is
based on `CUSTMAST`, whose physical fields include `CUSTNO`, `STATUS`,
`CRDLMT`, and `USEDAMT`. The supplied DDS does not prove how `AVAIL_CREDIT` is
derived, so the derivation remains open for data owner review.

## Evidence-Linked Details

| Claim ID | Knowledge Type | Statement | Evidence | Strength | Review Status |
| --- | --- | --- | --- | --- | --- |
| CTX-CREDIT-CHECK-DATA-001 | observed_behavior | `CREDITVW` exposes fields used by `CREDITCHK`. | DDS-CREDIT-CHECK-CREDITVW-001 | confirmed_from_code | needs_sme_review |
| CTX-CREDIT-CHECK-DATA-002 | observed_behavior | `CUSTMAST` contains customer credit fields. | DDS-CREDIT-CHECK-CUSTMAST-001 | confirmed_from_code | needs_sme_review |
| CTX-CREDIT-CHECK-DATA-003 | unknown_tbd | The derivation of `CREDITVW.AVAIL_CREDIT` is not proven by the supplied DDS. | RAG-GAP-CREDIT-CHECK-001 | missing | needs_sme_review |

## Candidate Seeds

| Candidate ID | Candidate Statement | Business Signal | Evidence Basis | Required Review |
| --- | --- | --- | --- | --- |
| DD-CREDIT-AVAILABLE-AMOUNT | Available Credit Amount is approved dictionary terminology. | Business users need a stable term for the maximum amount that may be approvable. | field-dictionary-context.md | Data owner confirmation in target project |

## Gaps For Module Analyzer

| TBD ID | Category | Question | Evidence | Owner | Blocking |
| --- | --- | --- | --- | --- | --- |
| TBD-CREDIT-CHECK-004 | pending_source | How is available credit derived from physical customer credit fields? | RAG-GAP-CREDIT-CHECK-001; `CREDITVW.AVAIL_CREDIT` | Data owner | yes |
