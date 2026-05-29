# View 4: Data Flow - Payment Matching

## Intake Status
- status: draft
- source_state: rag_hydrated
- primary_sources:
  - SNP-PAYMENT-001
  - SNP-PAYMENT-002
  - DD-PAYMENT-AMOUNT

## Summary

Three data objects are identified: `PMTINPUT` (input flat file), `INVOICEDB`
(invoice lookup), and `PMTSUSP` (suspense). The AR balance table target is
referenced in the SME note but not yet confirmed in source snippets.

## Evidence-Linked Details

| Claim ID | Knowledge Type | Statement | Evidence | Strength | Review Status |
| --- | --- | --- | --- | --- | --- |
| VIEW4-PMATCH-001 | observed_behavior | `PMTINPUT` fields include payment amount and customer number. | SNP-PAYMENT-001 | confirmed_from_code | needs_sme_review |
| VIEW4-PMATCH-002 | observed_behavior | `PMTSUSP` stores unmatched payment records with reason code. | SNP-PAYMENT-002 | confirmed_from_code | needs_sme_review |
| VIEW4-PMATCH-003 | dictionary_term | `DD-PAYMENT-AMOUNT` maps to `PMTINPUT.PMTAMT`. | DD-PAYMENT-AMOUNT | approved_dictionary | needs_sme_review |

## Candidate Seeds

| Candidate ID | Candidate Statement | Business Signal | Evidence Basis | Required Review |
| --- | --- | --- | --- | --- |
| RAG-GAP-PAYMENT-MATCH-002 | The AR balance write target must be confirmed before data-flow approval. | Posting accuracy and reconciliation ownership depend on the exact ledger target. | SME-PAYMENT-MATCH-001 | needs_sme_review |

## Gaps For Module Analyzer

| TBD ID | Category | Question | Evidence | Owner | Blocking |
| --- | --- | --- | --- | --- | --- |
| TBD-PAYMENT-MATCH-003 | data_object | Which physical file or table is the AR balance write target? | SME-PAYMENT-MATCH-001 | Data owner | no |
