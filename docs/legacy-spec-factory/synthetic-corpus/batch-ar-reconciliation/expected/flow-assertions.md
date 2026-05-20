# Expected Flow Assertions

The flow should be modeled as a **scheduler-driven batch reconciliation path**.

## Expected Trigger Model

- scheduler or nightly batch submission via `SBMJOB`

## Expected High-Level Sequence

1. scheduler submits `ARRECONCL`
2. `ARRECONCL` submits batch driver `ARRECON`
3. `ARRECON` loads checkpoint state from `ARCTRL`
4. `ARRECON` loops through staged transactions in `ARTXN`
5. `ARRECON` compares document and applied amounts
6. non-zero differences are written to exception report `ARERRRPT`
7. batch control row is updated to `COMPLETE`
8. Finance reviews the next-morning exception report

## Expected Business Themes

- restart control affects operational behavior
- non-zero reconciliation difference is a business exception
- spool review is part of the control loop
- cut-off timing matters to downstream operations

## Expected Capability Seed

- one capability centered on nightly accounts-receivable reconciliation and
  exception handling
