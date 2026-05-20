# Negative Example: Partial Intake

## Situation

The bundle contains RPGLE source and DB metadata, but the DSPF source and a
sample spool report are expected and missing. One transaction sample has
`sensitivity: unknown`.

## Expected Result

- status: `blocked`
- do not route to `legacy-ibmi-inventory`
- create `TBD-*` entries for the missing DSPF, missing spool sample, and
  unknown-sensitivity transaction sample
- require redaction owner and SME review before downstream analysis

## Required Findings

| TBD ID | Finding | Blocking | Resolver |
| --- | --- | --- | --- |
| TBD-INVENTORY-SYSTEM-001 | DSPF source missing | yes | source owner |
| TBD-INVENTORY-SYSTEM-002 | spool report sample missing | yes | operations SME |
| TBD-INVENTORY-SYSTEM-003 | transaction sample sensitivity unknown | yes | redaction owner |
