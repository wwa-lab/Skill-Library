# Source Snippets

This file is the RAG evidence map seed. Snippets preserve source path, line
range, relationship bindings, and evidence strength so downstream skills can
audit every candidate fact.

## Snippet Index

| Snippet ID | Artifact | Lines | Summary | Strength |
| --- | --- | ---: | --- | --- |
| `SNP-CREDIT-CHECK-001` | `SRC-CREDIT-CHECK-CRDTCMD-001` | 7 | `CRDTCMD` calls `CREDITCHK` with customer number, requested amount, and approved amount. | confirmed_from_code |
| `SNP-CREDIT-CHECK-002` | `SRC-CREDIT-CHECK-CREDITCHK-001` | 1-17 | `CREDITCHK` declares printer output, working fields, and interface parameters. | confirmed_from_code |
| `SNP-CREDIT-CHECK-003` | `SRC-CREDIT-CHECK-CREDITCHK-001` | 29-36 | `CREDITCHK` reads `STATUS` and `AVAIL_CREDIT` from `CREDITVW` by customer number. | confirmed_from_code |
| `SNP-CREDIT-CHECK-004` | `SRC-CREDIT-CHECK-CREDITCHK-001` | 38-67 | Denial, approval, over-limit cap, and return-value behavior. | confirmed_from_code |
| `SNP-CREDIT-CHECK-005` | `SRC-CREDIT-CHECK-CREDITCHK-001` | 69-74 | Denial/error message text is written to `QSYSPRT`. | confirmed_from_code |
| `SNP-CREDIT-CHECK-006` | `DDS-CREDIT-CHECK-CREDITVW-001` | 1-5 | `CREDITVW` is based on `CUSTMAST` and exposes `CUSTNO`, `STATUS`, `AVAIL_CREDIT`. | confirmed_from_code |

## Relationship Bindings

```yaml
relationships:
  - edge_id: EDGE-CREDIT-CHECK-001
    from: PROGRAM-CRDTCMD
    relation: calls
    to: PROGRAM-CREDITCHK
    evidence:
      snippet_id: SNP-CREDIT-CHECK-001
      artifact_id: SRC-CREDIT-CHECK-CRDTCMD-001
      line_start: 7
      line_end: 7
    confidence: confirmed_from_code

  - edge_id: EDGE-CREDIT-CHECK-002
    from: PROGRAM-CREDITCHK
    relation: reads
    to: TABLE_OR_FILE-CREDITVW
    evidence:
      snippet_id: SNP-CREDIT-CHECK-003
      artifact_id: SRC-CREDIT-CHECK-CREDITCHK-001
      line_start: 29
      line_end: 36
    confidence: confirmed_from_code

  - edge_id: EDGE-CREDIT-CHECK-003
    from: PROGRAM-CREDITCHK
    relation: validates
    to: FIELD-CREDITVW-STATUS
    evidence:
      snippet_id: SNP-CREDIT-CHECK-004
      artifact_id: SRC-CREDIT-CHECK-CREDITCHK-001
      line_start: 50
      line_end: 54
    confidence: confirmed_from_code

  - edge_id: EDGE-CREDIT-CHECK-004
    from: PROGRAM-CREDITCHK
    relation: compares
    to: FIELD-CREDITVW-AVAIL-CREDIT
    evidence:
      snippet_id: SNP-CREDIT-CHECK-004
      artifact_id: SRC-CREDIT-CHECK-CREDITCHK-001
      line_start: 56
      line_end: 64
    confidence: confirmed_from_code

  - edge_id: EDGE-CREDIT-CHECK-005
    from: PROGRAM-CREDITCHK
    relation: writes
    to: REPORT-QSYSPRT-CREDIT-CHECK-MESSAGE
    evidence:
      snippet_id: SNP-CREDIT-CHECK-005
      artifact_id: SRC-CREDIT-CHECK-CREDITCHK-001
      line_start: 69
      line_end: 74
    confidence: confirmed_from_code
```

## Runtime Corroboration

| Runtime Evidence ID | Source | Lines | Observed detail | Linked snippets |
| --- | --- | ---: | --- | --- |
| `RUN-CREDIT-CHECK-JOBLOG-001` | `runtime/sample-joblog.txt` | 1-9 | Wrapper completion and over-limit diagnostic message. | `SNP-CREDIT-CHECK-001`, `SNP-CREDIT-CHECK-004` |
| `RUN-CREDIT-CHECK-SPOOL-001` | `runtime/sample-spool.txt` | 1-9 | Denied request: requested `1200.00`, available `1000.00`, decision `D`, approved amount `1000.00`. | `SNP-CREDIT-CHECK-004`, `SNP-CREDIT-CHECK-005` |
