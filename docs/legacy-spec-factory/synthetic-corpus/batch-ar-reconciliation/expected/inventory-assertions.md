# Expected Inventory Assertions

The inventory for this fixture should be considered **ready for downstream
program and flow analysis**.

## Expected Objects

- `OBJ-AR-RECON-ARRECONCL` — `ARRECONCL` — `CLLE`
- `OBJ-AR-RECON-ARRECON` — `ARRECON` — `SQLRPGLE`
- `OBJ-AR-RECON-ARTXN` — `ARTXN` — `PF`
- `OBJ-AR-RECON-ARCTRL` — `ARCTRL` — `PF`
- `OBJ-AR-RECON-ARERRRPT` — `ARERRRPT` — `PRTF`

## Expected Relationships

- scheduler triggers `ARRECONCL`
- `ARRECONCL` submits batch job for `ARRECON`
- `ARRECON` reads staged transactions from `ARTXN`
- `ARRECON` reads and updates checkpoint state in `ARCTRL`
- `ARRECON` writes exception output to `ARERRRPT`

## Gate Expectation

- no source-coverage blocker should prevent batch-flow analysis
- runtime evidence should be considered available and relevant
