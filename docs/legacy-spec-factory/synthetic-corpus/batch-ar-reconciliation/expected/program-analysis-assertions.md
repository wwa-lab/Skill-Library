# Expected Program Analysis Assertions

Program analysis for `ARRECON` should recognize a **batch-driver program**
rather than an interactive business transaction.

## What The Analysis Should Recognize

- fixed-format `SQLRPGLE`
- startup control-load subroutine
- restart-flag branch
- sequential transaction loop over `ARTXN`
- embedded SQL read of applied amount
- exception-only reporting branch when difference is non-zero
- end-of-job checkpoint update in `ARCTRL`

## Important Interpretation Points

- `ARRECONCL` is orchestration glue, not the reconciliation rules owner
- `ARCTRL` is operationally significant because it governs restart semantics
- spool output is a business control artifact, not merely debug output
- completion status update is part of the batch contract

## What The Analysis Must Not Miss

- this is a nightly or scheduled path, not user-initiated menu logic
- restart behavior changes interpretation of the run
- exception rows represent unresolved financial differences requiring review
