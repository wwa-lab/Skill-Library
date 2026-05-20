# Golden Master Sample Data Manifest: <Capability Name>

## Redaction Summary

| Field | Value |
| --- | --- |
| Evidence manifest | `<path>` |
| Redaction log | `<path>` |
| Raw evidence excluded from repo | yes |
| Any `sensitivity: unknown` | yes |
| Data owner approval | pending |

## Samples

| Sample Ref | Evidence ID | Used As | Test Cases | Source Type | Redaction Status | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `07_runtime-evidence/sample-transactions/<sample>.json` | `EV-<CAPABILITY-SLUG>-001` | input | `TC-<CAPABILITY-SLUG>-001` | sample_transaction | pending |  |
| `07_runtime-evidence/spool-samples/<sample>.txt` | `EV-<CAPABILITY-SLUG>-002` | expected_output | `TC-<CAPABILITY-SLUG>-001` | spool | pending |  |

## Preservation Requirements

- Preserve field lengths, decimal scale, signs, null/blank distinctions, and ordering when they are behaviorally relevant.
- Replace production identifiers with stable fake IDs.
- Do not include credentials, hostnames, IPs, tokens, or operational secrets.
- Mask financial amounts unless exact arithmetic is required for the approved test case.
