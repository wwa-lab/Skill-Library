# SQLRPGLE Credit Check Blocked Path

A compact **synthetic negative fixture** paired with
[`sqlrpgle-credit-check-happy`](../sqlrpgle-credit-check-happy/README.md).

## Scenario

This scenario uses the same business slice as the happy path:

- a CLLE wrapper triggers a fixed-format `SQLRPGLE` program
- the program appears to read customer credit status
- runtime evidence suggests a deny path exists

But one critical source artifact is missing and one control meaning is not yet
confirmed by SME review. The correct repository behavior is to **stop cleanly**
instead of filling the gaps with guesses.

## Why This Fixture Matters

This is the kind of incomplete pilot input we should expect in real work:

- source export is partial
- DDS is present for the PF but not for the LF that shapes the read path
- comments imply a branch, but the branch meaning is not fully confirmed

If the skills still produce a confident inventory, flow, or spec from this
input, that is a defect in the methodology.

## Included Assets

```text
sqlrpgle-credit-check-blocked/
  README.md
  source/
    CREDITCHK.SQLRPGLE
    CRDTCMD.CLLE
  dds/
    CUSTMAST.PF
  runtime/
    sample-joblog.txt
  sme/
    sme-notes.md
  expected/
    expected-review-notes.md
```

## Intended Skill Coverage

- `legacy-modernization-orchestrator`
- `legacy-ibmi-evidence-intake`
- `legacy-ibmi-inventory`
- `legacy-ibmi-program-analyzer`
- `legacy-ibmi-flow-analyzer`

## Blocking Conditions

1. The logical file `CREDITVW.LF` is referenced in embedded SQL but its source
   is missing.
2. SME review has not yet confirmed whether `STATUS = 'H'` means hold, hard
   stop, or manual-review pending.

These are not cosmetic gaps. They affect both the effective access path and
the business meaning of a decision branch.

## Correct Behavior

Good output should:

- mark the slice as blocked
- request the missing LF source or approved surrogate evidence
- record an SME clarification TBD for `STATUS = 'H'`
- refuse to mint an approved business rule for the hold path
- refuse to continue to spec generation

## Wrong Behavior

Bad output would:

- assume the LF is equivalent to direct PF access
- invent a full meaning for `STATUS = 'H'`
- produce a completed flow or approved spec anyway
