# Expected Inventory Assertions

The inventory for this fixture should be considered **ready for downstream
program analysis**.

## Expected Objects

- `OBJ-CREDIT-CHECK-CRDTCMD` — `CRDTCMD` — `CLLE`
- `OBJ-CREDIT-CHECK-CREDITCHK` — `CREDITCHK` — `SQLRPGLE`
- `OBJ-CREDIT-CHECK-CUSTMAST` — `CUSTMAST` — `PF`
- `OBJ-CREDIT-CHECK-CREDITVW` — `CREDITVW` — `LF`
- `OBJ-CREDIT-CHECK-QSYSPRT` — `QSYSPRT` / report output — `PRTF or printer usage`

## Expected Relationships

- `CRDTCMD` submits or calls `CREDITCHK` as the operational entry path.
- `CREDITCHK` reads customer credit status through `CREDITVW`.
- `CREDITVW` is derived from or keyed over `CUSTMAST`.
- `CREDITCHK` writes operator-facing or review-facing message text to printer
  output.

## Gate Expectation

- Coverage should be treated as complete enough to proceed to
  `legacy-ibmi-program-analyzer`.
- No blocking TBD should remain for missing source in this fixture.
