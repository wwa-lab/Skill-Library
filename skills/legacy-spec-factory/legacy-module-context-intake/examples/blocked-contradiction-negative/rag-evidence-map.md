# RAG Evidence Map - PAYMENT-MATCH

## RAG Runs

| Run ID | Source Snapshot | Dictionary Version | Sensitivity | Status |
| --- | --- | --- | --- | --- |
| RAG-20260521-002 | synthetic-rpgle-payment-match-2026-05-21 | synthetic-dict-v1 | synthetic_non_production | blocked_pending_contradiction_review |

## Source Snippets

| Evidence ID | Artifact | Lines | Summary | Strength | Used In |
| --- | --- | ---: | --- | --- | --- |
| SNP-PAYMENT-001 | SRC-PAYMENT-MATCH-PMTMATCH-001 | 1-30 | `PMTMATCH` reads `PMTINPUT`, performs invoice lookup, posts matches. | confirmed_from_code | 01-operation-business-flow.md, 02-system-flow.md, 03-program-flow.md, 04-data-flow.md |
| SNP-PAYMENT-002 | SRC-PAYMENT-MATCH-PMTMATCH-001 | 31-50 | Unmatched records written to `PMTSUSP` with reason code. | confirmed_from_code | 01-operation-business-flow.md, 03-program-flow.md, 04-data-flow.md |

## Runtime Observations

| Evidence ID | Source | Lines | Observed Detail | Used In |
| --- | --- | ---: | --- | --- |
| RUN-PAYMENT-JOBLOG-001 | runtime/sample-joblog.txt | 1-12 | Batch job `PMTMATCH` appears in weekly schedule; no daily scheduling found. | 01-operation-business-flow.md, 02-system-flow.md |

## Dictionary Mappings

| Standard Field ID | Legacy Reference | Meaning | Owner | Status | Used In |
| --- | --- | --- | --- | --- | --- |
| DD-PAYMENT-AMOUNT | PMTINPUT.PMTAMT | Total amount of incoming payment transaction. | AR Operations | approved_dictionary | 04-data-flow.md |

## Impact Scope

| Target | Impact Type | Evidence | Confidence | Used In |
| --- | --- | --- | --- | --- |
| PROGRAM-PMTMATCH | Reads `PMTINPUT`, writes `PMTSUSP`. | SNP-PAYMENT-001, SNP-PAYMENT-002 | high | 02-system-flow.md, 03-program-flow.md |

## Candidate Facts

| Candidate ID | Statement | Business Signal | Evidence Basis | Promotion Status | Required Review |
| --- | --- | --- | --- | --- | --- |
| RAG-CAND-PAYMENT-MATCH-001 | Matching frequency is daily EOD. | Payment posting SLA and operational staffing depend on how often matching runs. | SME-PAYMENT-MATCH-001; RUN-PAYMENT-JOBLOG-001 | blocked_pending_contradiction_review | AR Operations SME |
| RAG-CAND-PAYMENT-MATCH-002 | Suspense items must be cleared within 2 business days. | Exception backlog timing affects AR follow-up and customer account accuracy. | SME-PAYMENT-MATCH-001 | needs_sme_review | AR Operations SME |
| RAG-CAND-PAYMENT-MATCH-003 | Trigger model is scheduled batch rather than event-driven. | Payment posting timeliness, interface design, and SLA expectations depend on the trigger model. | RUN-PAYMENT-JOBLOG-001; `PMTMATCH` | blocked_pending_contradiction_review | AR Operations SME |
| RAG-CONFLICT-PAYMENT-MATCH-001 | BLOCKED: matching frequency conflict between SME note and runtime evidence. | The business process cadence cannot be approved until daily vs weekly operation is resolved. | SME-PAYMENT-MATCH-001, RUN-PAYMENT-JOBLOG-001 | blocked | AR Operations SME |
| RAG-ASM-PAYMENT-MATCH-001 | Full program analysis should confirm whether matching logic is inline or delegated elsewhere. | Modernization scope depends on whether invoice matching, posting, and suspense routing are isolated or spread across callers. | `PMTMATCH`; SNP-PAYMENT-001 | needs_sme_review | IBM i developer |
| RAG-GAP-PAYMENT-MATCH-002 | The AR balance write target must be confirmed before data-flow approval. | Posting accuracy and reconciliation ownership depend on the exact ledger target. | SME-PAYMENT-MATCH-001 | deferred | Data owner |
