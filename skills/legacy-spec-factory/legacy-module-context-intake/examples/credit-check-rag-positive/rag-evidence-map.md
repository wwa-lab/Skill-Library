# RAG Evidence Map - CREDIT-CHECK

## RAG Runs

| Run ID | Source Snapshot | Dictionary Version | Sensitivity | Status |
| --- | --- | --- | --- | --- |
| RAG-20260521-001 | synthetic-sqlrpgle-credit-check-happy-2026-05-21 | synthetic-dict-v1 | synthetic_non_production | ready_with_warnings |

## Source Snippets

| Evidence ID | Artifact | Lines | Summary | Strength | Used In |
| --- | --- | ---: | --- | --- | --- |
| SNP-CREDIT-CHECK-001 | SRC-CREDIT-CHECK-CRDTCMD-001 | 7 | `CRDTCMD` calls `CREDITCHK`. | confirmed_from_code | 02-system-flow.md, 03-program-flow.md |
| SNP-CREDIT-CHECK-003 | SRC-CREDIT-CHECK-CREDITCHK-001 | 29-36 | `CREDITCHK` reads `STATUS` and `AVAIL_CREDIT` from `CREDITVW`. | confirmed_from_code | 02-system-flow.md, 03-program-flow.md |
| SNP-CREDIT-CHECK-004 | SRC-CREDIT-CHECK-CREDITCHK-001 | 38-67 | Denial, approval, over-limit cap, and return-value behavior. | confirmed_from_code | 01-operation-business-flow.md, 03-program-flow.md |
| SNP-CREDIT-CHECK-005 | SRC-CREDIT-CHECK-CREDITCHK-001 | 69-74 | Denial/error message text is written to `QSYSPRT`. | confirmed_from_code | 03-program-flow.md |
| DDS-CREDIT-CHECK-CUSTMAST-001 | DDS-CREDIT-CHECK-CUSTMAST-001 | 1-6 | Physical customer credit fields. | confirmed_from_code | 04-data-flow.md |
| DDS-CREDIT-CHECK-CREDITVW-001 | DDS-CREDIT-CHECK-CREDITVW-001 | 1-5 | Logical view fields used by `CREDITCHK`. | confirmed_from_code | 04-data-flow.md |

## Runtime Observations

| Evidence ID | Source | Lines | Observed Detail | Used In |
| --- | --- | ---: | --- | --- |
| RUN-CREDIT-CHECK-JOBLOG-001 | runtime/sample-joblog.txt | 1-9 | Wrapper completion and over-limit diagnostic message. | 02-system-flow.md |
| RUN-CREDIT-CHECK-SPOOL-001 | runtime/sample-spool.txt | 1-9 | Denied over-limit scenario with approved amount capped to available credit. | 01-operation-business-flow.md |

## Dictionary Mappings

| Standard Field ID | Legacy Reference | Meaning | Owner | Status | Used In |
| --- | --- | --- | --- | --- | --- |
| DD-CUSTOMER-NUMBER | CUSTMAST.CUSTNO, CREDITVW.CUSTNO, CREDITCHK.CustNo | Stable customer identifier used for credit lookup. | Credit Operations | approved_dictionary | 04-data-flow.md |
| DD-CREDIT-AVAILABLE-AMOUNT | CREDITVW.AVAIL_CREDIT, CREDITCHK.AvailCredit | Amount currently available for order approval. | Credit Operations | approved_dictionary | 04-data-flow.md |
| DD-CREDIT-DECISION-CODE | CREDITCHK.Decision | Legacy approve/deny indicator returned by credit checking. | Credit Operations | approved_dictionary | 01-operation-business-flow.md |

## Impact Scope

| Target | Impact Type | Evidence | Confidence | Used In |
| --- | --- | --- | --- | --- |
| PROGRAM-CREDITCHK | Reads `CREDITVW.STATUS` and `CREDITVW.AVAIL_CREDIT`. | SNP-CREDIT-CHECK-003 | high | 02-system-flow.md, 03-program-flow.md |
| PROGRAM-CREDITCHK | Compares requested amount to available credit. | SNP-CREDIT-CHECK-004 | high | 01-operation-business-flow.md, 03-program-flow.md |
| TABLE_OR_FILE-CUSTMAST | Physical base file for `CREDITVW`. | DDS-CREDIT-CHECK-CUSTMAST-001 | medium | 04-data-flow.md |

## Candidate Facts

| Candidate ID | Statement | Business Signal | Evidence Basis | Promotion Status | Required Review |
| --- | --- | --- | --- | --- | --- |
| RAG-CAND-CREDIT-CHECK-001 | Missing customers are denied by default. | Customer service cannot continue order release when the account cannot be resolved. | SNP-CREDIT-CHECK-003, SNP-CREDIT-CHECK-004 | needs_sme_review | Credit Operations SME |
| RAG-CAND-CREDIT-CHECK-002 | Inactive customers are denied even if credit exists. | Customer eligibility status can override available credit. | SNP-CREDIT-CHECK-004, SME-CREDIT-CHECK-001 | needs_sme_review | Credit Operations SME |
| RAG-CAND-CREDIT-CHECK-004 | Requests over available credit are denied and return available credit as the maximum approvable amount. | Over-limit orders are blocked, but the response exposes the amount that may be approvable. | SNP-CREDIT-CHECK-004, RUN-CREDIT-CHECK-SPOOL-001 | needs_sme_review | Credit Operations SME |
| RAG-ASM-CREDIT-CHECK-001 | Business-rule ownership appears to sit in the credit decision routine rather than the operational wrapper. | Modernization scope should focus the component that determines approval, denial, and amount behavior. | `CRDTCMD`; SME-CREDIT-CHECK-001 | deferred | IBM i developer / SME |
| RAG-ASM-CREDIT-CHECK-002 | Full program analysis should prioritize the credit decision routine. | Approval, denial, over-limit, and returned-amount behavior appear concentrated in one routine. | `CREDITCHK`; SNP-CREDIT-CHECK-004 | deferred | IBM i developer |
| RAG-GAP-CREDIT-CHECK-001 | Available credit derivation is not proven by the supplied DDS. | Data ownership and calculation semantics must be clear before approving credit-amount behavior. | `CREDITVW.AVAIL_CREDIT`; DDS-CREDIT-CHECK-CUSTMAST-001, DDS-CREDIT-CHECK-CREDITVW-001 | deferred | Data owner |
| RAG-GAP-CREDIT-CHECK-003 | The full caller scope for the credit decision routine is not proven by the synthetic fixture. | Reuse outside the sampled path could expand modernization scope. | `CREDITCHK`; SNP-CREDIT-CHECK-001 | deferred | IT SME |
| RAG-GAP-CREDIT-CHECK-004 | No evidence shows whether over-limit denials are queued, audited, or rejected inline. | Exception handling affects operations, auditability, and customer follow-up. | SME-CREDIT-CHECK-001 | deferred | Credit Operations SME |
| RAG-GAP-CREDIT-CHECK-005 | The supplied wrapper does not visibly capture the return decision. | The calling path may ignore or transform the approval decision. | `CRDTCMD`, `CREDITCHK`; SNP-CREDIT-CHECK-001, SNP-CREDIT-CHECK-004 | deferred | IBM i developer |
