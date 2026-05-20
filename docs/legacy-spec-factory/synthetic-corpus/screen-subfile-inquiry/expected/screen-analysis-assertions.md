# Expected Screen Analysis Assertions

The screen analysis should classify this as a **DSPF interactive inquiry screen
with subfile**.

## What The Analysis Should Recognize

- menu-driven inquiry context
- one header record format plus one subfile and one subfile-control format
- customer header fields displayed as output after lookup
- transaction-history rows displayed in the subfile
- `F5` refresh behavior
- `F12` return/back behavior
- inquiry-first interaction rather than update-heavy maintenance

## Important Interpretation Points

- the screen intent is to view recent transactions for one customer
- subfile rows are informational unless program logic proves update behavior
- function keys are operational navigation, not necessarily business commits

## What The Analysis Must Not Invent

- record-update semantics not supported by source or SME notes
- delete or maintenance behavior
- transaction-detail branch semantics beyond what runtime evidence supports
