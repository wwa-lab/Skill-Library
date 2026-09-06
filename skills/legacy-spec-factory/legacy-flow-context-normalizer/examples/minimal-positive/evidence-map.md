# Evidence Map - CREDIT-CHECK

## Documents
| Evidence ID | Source Document | Locator | Summary | Strength | Used In |
| --- | --- | --- | --- | --- | --- |
| DOC-CREDIT-CHECK-001 | source-docs/credit-check-process.vsdx | Main Process | Process diagram for credit check submission and recommendation. | high | 01-operation-business-flow.md; 02-system-flow.md; 03-program-flow.md |
| DOC-CREDIT-CHECK-002 | source-docs/credit-check-data.xlsx | Fields sheet | Data field list for application status recommendation. | high | 04-data-flow.md |

## Extracted Fragments
| Evidence ID | Document ID | Locator | Extracted Detail | Strength | Used In |
| --- | --- | --- | --- | --- | --- |
| FRAG-CREDIT-CHECK-001 | DOC-CREDIT-CHECK-001 | Main Process shape Submit Application | Branch staff submit a credit application. | high | 01-operation-business-flow.md |
| FRAG-CREDIT-CHECK-002 | DOC-CREDIT-CHECK-001 | Main Process connector Host Credit Check | Core banking sends application to host credit checking. | high | 02-system-flow.md |
| FRAG-CREDIT-CHECK-003 | DOC-CREDIT-CHECK-001 | Main Process note CCHK100 | Diagram labels CCHK100 as host credit check program. | medium | 03-program-flow.md |
| FRAG-CREDIT-CHECK-004 | DOC-CREDIT-CHECK-002 | Fields row 7 | APPLICPF application status is updated with recommendation. | high | 04-data-flow.md |
| PGM-CREDIT-CHECK-001 | DOC-CREDIT-CHECK-001 | Main Process note CCHK100 | CCHK100 is the SME-confirmed IBM i program-analysis focus. | medium | 03-program-flow.md |
| DATA-CREDIT-CHECK-001 | DOC-CREDIT-CHECK-002 | Fields row 7 | APPLICPF is the SME-confirmed IBM i application status file updated by the recommendation result. | high | 04-data-flow.md |

## Cross-Document Corroboration
| Topic | Evidence A | Evidence B | Agreement | Notes |
| --- | --- | --- | --- | --- |
| Recommendation result updates application status | FRAG-CREDIT-CHECK-001 | FRAG-CREDIT-CHECK-004 | partial | Process and data docs agree on approve/decline result; retention remains open. |

## Candidate Facts
| Candidate ID | Statement | Business Signal | Evidence Basis | Promotion Status | Required Review |
| --- | --- | --- | --- | --- | --- |
| CAND-CREDIT-CHECK-001 | The module should distinguish approved and declined recommendation outcomes. | Credit operations needs both positive and negative outcomes reviewed before BRD drafting. | DOC-CREDIT-CHECK-001; FRAG-CREDIT-CHECK-001 | sme_confirmed | Carry into context intake |
| CAND-CREDIT-CHECK-002 | Interface timing should be verified before SLA commitments are written. | Customer waiting time may depend on whether the check is synchronous or deferred. | DOC-CREDIT-CHECK-001; FRAG-CREDIT-CHECK-002 | needs_sme_review | Carry as non-blocking TBD |
| CAND-CREDIT-CHECK-003 | Source verification should confirm which program paths produce approval and decline recommendations. | BRD scenarios need both outcome paths before acceptance criteria are drafted. | DOC-CREDIT-CHECK-001; FRAG-CREDIT-CHECK-003 | needs_sme_review | Route later if high risk |
| CAND-CREDIT-CHECK-004 | Data retention ownership must be clarified before modernization decisions are finalized. | Retention affects compliance, purge behavior, and downstream audit evidence. | DOC-CREDIT-CHECK-002; FRAG-CREDIT-CHECK-004 | needs_sme_review | Carry as non-blocking TBD |
