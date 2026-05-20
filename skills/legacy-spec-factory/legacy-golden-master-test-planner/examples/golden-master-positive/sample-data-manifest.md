# Golden Master Sample Data Manifest: Credit Limit Enforcement

## Redaction Summary

| Field | Value |
| --- | --- |
| Evidence manifest | `07_runtime-evidence/evidence-manifest.yaml` |
| Redaction log | `07_runtime-evidence/redaction-log-2025-05-01.md` |
| Raw evidence excluded from repo | yes |
| Any `sensitivity: unknown` | no |
| Data owner approval | approved |

## Samples

| Sample Ref | Evidence ID | Used As | Test Cases | Source Type | Redaction Status | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `07_runtime-evidence/sample-transactions/valid-order-001.json` | `EV-CREDIT-LIMIT-001` | input | `TC-CREDIT-LIMIT-001` | sample_transaction | approved | Redacted customer and order IDs |
| `07_runtime-evidence/auth-responses/valid-order-001-approved.txt` | `EV-CREDIT-LIMIT-002` | expected_output | `TC-CREDIT-LIMIT-001` | job_log | approved | Approval response |
| `07_runtime-evidence/sample-transactions/rejected-order-001.json` | `EV-CREDIT-LIMIT-003` | input | `TC-CREDIT-LIMIT-002` | sample_transaction | approved | Redacted customer and order IDs |
| `07_runtime-evidence/auth-responses/rejected-order-001-denied.txt` | `EV-CREDIT-LIMIT-004` | expected_output | `TC-CREDIT-LIMIT-002` | job_log | approved | Rejection response |
| `07_runtime-evidence/sample-transactions/boundary-order-001.json` | `EV-CREDIT-LIMIT-005` | input | `TC-CREDIT-LIMIT-003` | sample_transaction | approved | Exact-limit input |
| `07_runtime-evidence/auth-responses/boundary-order-001-approved.txt` | `EV-CREDIT-LIMIT-006` | expected_output | `TC-CREDIT-LIMIT-003` | job_log | approved | Boundary approval response |

## Preservation Requirements

- Preserve amount scale, sign, blank/null distinctions, and approval status.
- Use stable fake IDs from the redaction log.
- Do not restore raw customer or order identifiers.
