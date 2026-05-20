# SME Notes

Reviewer: Liu Wei  
Role: Customer Service Operations SME  
Review Date: 2026-05-20

## Confirmed Business Meaning

- Menu option `5` is the standard entry path for customer inquiry.
- This function is inquiry-only; it does not update customer records.
- The subfile exists to let reps review recent transaction history quickly.
- `F5` refreshes the transaction list for the current customer.
- `F12` exits back to the calling menu.

## Open Questions For Later Expansion

- Some shops use option values in the subfile to open transaction detail; this
  compact fixture does not yet model that branch fully.
- A later variant could add an exception-status color or hold-status indicator.
