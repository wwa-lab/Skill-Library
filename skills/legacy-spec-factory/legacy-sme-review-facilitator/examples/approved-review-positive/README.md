# Positive Case: Completed SME Review

Capability: `CREDIT-CHECK`

Artifact reviewed: `05_brds/CREDIT-CHECK/brd.md`

Review outcome: completed with SME sign-off, one confirmed behavior, one
rejected inferred rule with SME correction, one non-blocking channel follow-up
routed to Digital Channels, and one deferred validation TBD routed to
Operations. BRD required functional-analysis sections 1-9 are reviewed
explicitly; two sections are accepted with named TBDs.

## Files

- `review-session.md` records scope, participants, materials, and session status.
- `question-pack.md` shows the questions presented to the SME.
- `sme-decision-log.yaml` records signed, typed decisions.
- `sme-signoff.md` records the SME sign-off and routing conditions.
- `follow-up-findings.yaml` routes the rule revision, channel follow-up, and
  deferred validation TBD.

## What This Example Proves

- A facilitator can record SME confirmation without promoting the artifact
  itself.
- A rejected `BR-*` is routed to the owning skill with `suggested_revision`.
- Deferred `TBD-*` items stay unresolved and appear in follow-up findings.
- BRD section coverage is reviewed before item-level rule / behavior questions.
- Every decision references stable IDs and SME sign-off or escalation details.
