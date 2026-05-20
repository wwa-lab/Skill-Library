# Expected Flow Assertions

The flow should be modeled as a **menu-driven customer inquiry path**.

## Expected Trigger Model

- user selects option `5` from a customer-service menu

## Expected High-Level Sequence

1. user selects Customer Inquiry from the menu
2. inquiry program displays header and subfile screen
3. user enters or confirms customer number
4. program loads recent transaction history into the subfile
5. user may refresh the subfile with `F5`
6. user returns to the previous menu with `F12`

## Expected Business Themes

- this is an inquiry workflow, not a maintenance workflow
- transaction history is surfaced for review and support operations
- menu context matters to how the business event is named
