# Evidence Map - PAYMENT-RECON

## Documents
| Evidence ID | Source Document | Locator | Summary | Strength | Used In |
| --- | --- | --- | --- | --- | --- |
| DOC-PAYMENT-RECON-001 | source-docs/payment-recon-prod-deck.pptx | not inspected | Source exists but authorization is unknown. | blocked | all views as blocker only |

## Extracted Fragments
| Evidence ID | Document ID | Locator | Extracted Detail | Strength | Used In |
| --- | --- | --- | --- | --- | --- |
| FRAG-PAYMENT-RECON-001 | DOC-PAYMENT-RECON-001 | not inspected | No content extracted due to authorization block. | blocked | all views as blocker only |

## Cross-Document Corroboration
| Topic | Evidence A | Evidence B | Agreement | Notes |
| --- | --- | --- | --- | --- |
| Evidence authorization | DOC-PAYMENT-RECON-001 | N/A | blocked | Authorization must be resolved first. |

## Candidate Facts
| Candidate ID | Statement | Business Signal | Evidence Basis | Promotion Status | Required Review |
| --- | --- | --- | --- | --- | --- |
| CAND-PAYMENT-RECON-001 | Evidence authorization must be approved before flow normalization. | The team must avoid exposing production reconciliation details before redaction. | DOC-PAYMENT-RECON-001; FRAG-PAYMENT-RECON-001 | blocked | Route to evidence intake |
| CAND-PAYMENT-RECON-002 | Source approval is required before identifying systems or interfaces. | System names may expose sensitive reconciliation architecture. | DOC-PAYMENT-RECON-001; FRAG-PAYMENT-RECON-001 | blocked | Route to evidence intake |
| CAND-PAYMENT-RECON-003 | Source approval is required before identifying jobs or programs. | Program names may expose sensitive payment reconciliation internals. | DOC-PAYMENT-RECON-001; FRAG-PAYMENT-RECON-001 | blocked | Route to evidence intake |
| CAND-PAYMENT-RECON-004 | Source approval is required before identifying reconciliation data objects. | Data object names may expose payment or customer-sensitive evidence. | DOC-PAYMENT-RECON-001; FRAG-PAYMENT-RECON-001 | blocked | Route to evidence intake |
