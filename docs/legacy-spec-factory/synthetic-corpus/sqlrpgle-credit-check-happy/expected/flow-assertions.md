# Expected Flow Assertions

The flow should be treated as a **simple synchronous credit-check path**.

## Expected Trigger Model

- operational wrapper / direct program call through `CRDTCMD`

## Expected High-Level Sequence

1. caller provides customer number and requested amount
2. `CRDTCMD` invokes `CREDITCHK`
3. `CREDITCHK` reads customer status and available credit from `CREDITVW`
4. missing, inactive, or over-limit conditions produce a deny outcome
5. in-range request produces approve outcome
6. denial or warning text may be written to printer output

## Expected Business Themes

- active status is a gate before monetary approval
- available credit is the effective comparison value
- over-limit requests are denied but still return maximum approvable amount

## Expected Capability Seed

- one capability centered on customer credit decisioning for order entry or
  pre-order validation
