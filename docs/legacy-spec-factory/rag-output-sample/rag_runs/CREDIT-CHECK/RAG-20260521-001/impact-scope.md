# Impact Scope

This sample impact scope is field- and module-centered. It is useful for
review planning, but it is not a final modernization decision.

## Direct Impact

| Target | Impact type | Evidence | Confidence |
| --- | --- | --- | --- |
| `PROGRAM-CREDITCHK` | Reads `CREDITVW.STATUS` and `CREDITVW.AVAIL_CREDIT`. | `SNP-CREDIT-CHECK-003` | confirmed_from_code |
| `PROGRAM-CREDITCHK` | Validates active customer status. | `SNP-CREDIT-CHECK-004` | confirmed_from_code |
| `PROGRAM-CREDITCHK` | Compares requested amount to available credit. | `SNP-CREDIT-CHECK-004` | confirmed_from_code |
| `PROGRAM-CREDITCHK` | Writes denial/error messages to `QSYSPRT`. | `SNP-CREDIT-CHECK-005` | confirmed_from_code |

## Indirect Impact

| Target | Impact type | Evidence | Confidence |
| --- | --- | --- | --- |
| `PROGRAM-CRDTCMD` | Calls `CREDITCHK` as operational wrapper. | `SNP-CREDIT-CHECK-001` | confirmed_from_code |
| `TABLE_OR_FILE-CUSTMAST` | Physical base file for `CREDITVW`. | `SNP-CREDIT-CHECK-006` | confirmed_from_code |

## User-Visible Impact

| Surface | Observed behavior | Evidence | Confidence |
| --- | --- | --- | --- |
| Job message | Wrapper completion message after credit check call. | `RUN-CREDIT-CHECK-JOBLOG-001` | observed_in_runtime |
| Spool/report output | Over-limit request reports decision `D`, approved amount capped to available credit, and reason text. | `RUN-CREDIT-CHECK-SPOOL-001` | observed_in_runtime |

## Data Impact

| Standard field | Legacy references | Direction | Notes |
| --- | --- | --- | --- |
| `DD-CUSTOMER-NUMBER` | `CUSTMAST.CUSTNO`, `CREDITVW.CUSTNO`, `CREDITCHK.CustNo` | input/read | Lookup key |
| `DD-CUSTOMER-ACCOUNT-STATUS` | `CREDITVW.STATUS`, `CREDITCHK.Status` | read/validate | `A` is SME-confirmed as active |
| `DD-CREDIT-AVAILABLE-AMOUNT` | `CREDITVW.AVAIL_CREDIT`, `CREDITCHK.AvailCredit` | read/compare/return-derived | Derivation is a retrieval gap |
| `DD-REQUESTED-ORDER-AMOUNT` | `CREDITCHK.ReqAmt` | input/compare | Request amount from caller |
| `DD-APPROVED-CREDIT-AMOUNT` | `CREDITCHK.ApprAmt`, `CREDITCHK.pApprAmt` | output | Returned amount may equal request or available credit |
| `DD-CREDIT-DECISION-CODE` | `CREDITCHK.Decision` | output | `A` and `D` candidate values |

## Suggested Downstream Checks

1. Confirm whether any other callers invoke `CREDITCHK`.
2. Resolve how `CREDITVW.AVAIL_CREDIT` is derived.
3. Confirm whether over-limit denials create any queue, audit, or supervisor
   review record outside this fixture.
4. Decide whether `QSYSPRT` output is operational logging or a business-facing
   control report.
