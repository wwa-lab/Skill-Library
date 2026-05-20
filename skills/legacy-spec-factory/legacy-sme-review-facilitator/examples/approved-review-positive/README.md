# Positive Case: Completed SME Review

Capability: `CREDIT-CHECK`

Artifact reviewed: `05_brds/CREDIT-CHECK/brd.md`

Review outcome: completed with SME sign-off, one confirmed behavior, one
rejected inferred rule with SME correction, and one deferred TBD routed to
Operations.

## Files

- `review-session.md` records scope, participants, materials, and session status.
- `question-pack.md` shows the questions presented to the SME.
- `sme-decision-log.yaml` records signed, typed decisions.
- `sme-signoff.md` records the SME sign-off and routing conditions.
- `follow-up-findings.yaml` routes the rule revision and deferred TBD.

## What This Example Proves

- A facilitator can record SME confirmation without promoting the artifact
  itself.
- A rejected `BR-*` is routed to the owning skill with `suggested_revision`.
- A deferred `TBD-*` stays unresolved and appears in follow-up findings.
- Every decision references stable IDs and SME sign-off or escalation details.
