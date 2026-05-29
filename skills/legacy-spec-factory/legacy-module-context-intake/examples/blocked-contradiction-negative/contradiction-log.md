# Contradiction Log - PAYMENT-MATCH

## Summary

- status: open_contradictions
- evaluated_checks_present: true

## Open Contradictions

| Conflict ID | Type | Summary | Evidence A | Evidence B | Owner | Blocking |
| --- | --- | --- | --- | --- | --- | --- |
| RAG-CONFLICT-PAYMENT-MATCH-001 | frequency | SME states matching runs daily EOD; runtime job log shows weekly batch schedule. | SME-PAYMENT-MATCH-001 | RUN-PAYMENT-JOBLOG-001 | AR Operations SME | yes |

## Evaluated Checks

| Check | Result | Notes |
| --- | --- | --- |
| SME note vs runtime schedule | conflict_found | SME says daily; job log shows weekly. Cannot resolve without SME ruling. |
| Source vs runtime outcome | no_conflict_found | Source snippet behavior (match / suspense routing) aligns with runtime spool output. |
| Dictionary vs source usage | no_conflict_found | `PMTINPUT.PMTAMT` usage consistent with dictionary mapping DD-PAYMENT-AMOUNT. |
| ARCAD vs source relationship | not_evaluated | Synthetic fixture does not include a real ARCAD export. |

## Routing

RAG-CONFLICT-PAYMENT-MATCH-001 must be resolved by AR Operations SME before
module analysis or BRD writing can proceed. Route to the SME for a ruling on
matching frequency. After ruling, update this log, clear the blocking item in
`context-index.yaml`, and re-run the validator before routing to
`legacy-ibmi-module-analyzer`.

Do not resolve the contradiction by choosing one evidence source over the other
without explicit SME authorization.
