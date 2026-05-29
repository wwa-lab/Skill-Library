# SME Question Pack

**Review ID:** `REVIEW-CREDIT-CHECK-001`
**Artifact:** `05_brds/CREDIT-CHECK/brd.md`
**Capability:** `CREDIT-CHECK`
**Prepared Date:** `2026-05-16`

## BRD Functional Analysis Coverage

| Target | Required Area | Current Coverage | Evidence / TBD | Decision Needed |
| --- | --- | --- | --- | --- |
| `BRD-CREDIT-CHECK-001#section-01` | Function Purpose | Credit check purpose and scope stated | `EV-CREDIT-CHECK-008` | accept |
| `BRD-CREDIT-CHECK-001#section-02` | Business Scenarios / Use Cases | Normal and over-limit scenarios listed | `EV-CREDIT-CHECK-015` | accept |
| `BRD-CREDIT-CHECK-001#section-03` | Channels | Branch and API channels listed; MobileX needs confirmation | `TBD-CREDIT-CHECK-004` | accept with TBD |
| `BRD-CREDIT-CHECK-001#section-04` | User Interface / User Touchpoints | CSR screen and decline message listed | `EV-CREDIT-CHECK-018` | accept |
| `BRD-CREDIT-CHECK-001#section-05` | System Interfaces | Order entry and customer master interfaces listed | `EV-CREDIT-CHECK-012` | accept |
| `BRD-CREDIT-CHECK-001#section-06` | Process Flow | Business phases described without program-chain dependency | `EV-CREDIT-CHECK-015` | accept |
| `BRD-CREDIT-CHECK-001#section-07` | Validation Rules | Observed behavior and inferred rule seeds separated | `BEH-CREDIT-CHECK-006`, `BR-CREDIT-CHECK-003` | accept |
| `BRD-CREDIT-CHECK-001#section-08` | Error Handling | Over-limit handling and customer-not-found paths listed | `EV-CREDIT-CHECK-018` | accept |
| `BRD-CREDIT-CHECK-001#section-09` | Dependencies | Customer master and operations confirmation dependencies listed | `TBD-CREDIT-CHECK-002` | accept with TBD |

**Question for SME**
> Are required BRD sections 1-9 fit for BRD approval, with the named TBDs
> carried forward?

**SME Answer**
Yes. Sections 1-9 are acceptable. Carry MobileX and validation sequence as
non-blocking follow-ups.

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

### `TBD-CREDIT-CHECK-004`: MobileX Channel Applicability

**Context**
BRD section 3 is acceptable for approval, but MobileX channel scope still needs
confirmation.

**Question for SME**
> Does MobileX initiate or consume the Credit Check capability?

**SME Answer**
Accept BRD section 3 with this as a non-blocking channel follow-up. Digital
Channels SME must confirm MobileX scope.

### `TBD-CREDIT-CHECK-002`: Validation Sequence Ownership

**Context**
The BRD treats the validation sequence as unresolved.

**Question for SME**
> Should the legacy validation sequence be preserved exactly, and who can
> confirm the exact order?

**SME Answer**
The sequence is a business rule, not a bug. Ops needs to confirm the exact
order.
