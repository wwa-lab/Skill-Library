# SME Question Pack

**Review ID:** `REVIEW-CREDIT-CHECK-001`
**Artifact:** `05_brds/CREDIT-CHECK/brd.md`
**Capability:** `CREDIT-CHECK`
**Prepared Date:** `2026-05-16`

## Behavior Confirmations

### `BEH-CREDIT-CHECK-006`: Transaction Blocking When Limit Exceeded

**Claim**
> Transactions over the customer credit limit are blocked.

**Evidence**
- `EV-CREDIT-CHECK-015`: runtime job log, strength `observed_in_runtime`
- `EV-CREDIT-CHECK-008`: source excerpt, strength `confirmed_from_code`

**Question for SME**
> Is blocking transactions over the credit limit intended business behavior?

**SME Answer**
Yes, that's correct. CREDCHK enforces the limit strictly.

## Inferred Business Rules Needing SME Confirmation

### `BR-CREDIT-CHECK-003`: Interest Compounding

**Rule Statement**
> Interest is compounded daily on unpaid balances.

**Evidence Basis**
- `EV-CREDIT-CHECK-012`: control table extract, strength `confirmed_from_code`

**Question for SME**
> Does this rule accurately reflect business intent?

**SME Answer**
Not quite. It's only compounded daily if balance exceeds $10k.

## Open TBDs

### `TBD-CREDIT-CHECK-002`: Validation Sequence Ownership

**Context**
The BRD treats the validation sequence as unresolved.

**Question for SME**
> Should the legacy validation sequence be preserved exactly, and who can
> confirm the exact order?

**SME Answer**
The sequence is a business rule, not a bug. Ops needs to confirm the exact
order.
