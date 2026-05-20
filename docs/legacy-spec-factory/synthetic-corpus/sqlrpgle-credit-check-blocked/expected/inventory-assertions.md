# Expected Inventory Assertions

The inventory for this fixture should remain **blocked**.

## What Can Be Registered

- `CRDTCMD` as `CLLE`
- `CREDITCHK` as `SQLRPGLE`
- `CUSTMAST` as `PF`

## What Must Remain Unresolved

- `CREDITVW` is referenced but its `LF` source is missing
- any claim about the full derived-field contract for `AVAIL_CREDIT`

## Gate Expectation

- do not mark source coverage complete
- create a blocking gap for missing logical-file evidence before downstream
  analysis proceeds
