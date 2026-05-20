# Expected Runtime Evidence Assertions

Runtime evidence mining should be able to produce **draft observations** from
the supplied joblog and spool sample.

## Observations That Should Be Extractable

- batch submission message from `ARRECONCL`
- restart-path observation driven by control state
- at least one exception event tied to a document mismatch
- batch-complete observation tied to control-file update
- report-structure observation from the exception spool layout

## Confidence Expectation

- low or medium confidence only from a single observed run
- no high-confidence schedule or performance claims from one joblog

## What The Miner Must Not Invent

- exact scheduler definition beyond what SME notes and joblog support
- extra downstream posting steps not visible in source or runtime evidence
- variance or SLA claims from a single run
