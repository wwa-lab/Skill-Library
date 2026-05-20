# Expected Program Analysis Assertions

Program analysis for `CREDITCHK` should remain `draft` or
`needs_sme_review`, but it should **not** be blocked for missing source.

## What The Analysis Should Recognize

- fixed-format `SQLRPGLE`
- entry procedure `CREDITCHK`
- embedded SQL lookup against `CREDITVW`
- not-found handling via `SQLCOD = 100`
- generic SQL error branch via `SQLCOD <> 0`
- inactive-customer deny path via `Status <> 'A'`
- over-limit path where approved amount is capped to available credit
- printer-output subroutine used for denial or warning messages

## What The Analysis Must Not Miss

- `CRDTCMD` is not the owner of credit rules
- `Decision = 'A'` only occurs when request amount is within available credit
- denied outcomes can still return a non-zero approvable amount
- the logical file matters because it shapes the effective read contract

## Evidence Themes Expected

- direct source evidence for SQL branches and message-writing behavior
- runtime evidence support for the over-limit deny path from sample spool/joblog
- SME confirmation for the business meaning of active/inactive status
