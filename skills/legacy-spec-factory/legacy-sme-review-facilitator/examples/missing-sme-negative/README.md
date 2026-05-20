# Negative Case: Blocked SME Review

Capability: `ORDER-ENTRY`

Artifact attempted: `04_modules/ORDER-ENTRY/module-overview.md`

Review outcome: blocked before question-pack creation.

## Blocking Conditions

- No named SME owner is assigned.
- Evidence has `sensitivity: unknown` and `redaction_status: unknown`.

## Files

- `review-session.md` records the attempted scope and stop reason.
- `blocked-findings.yaml` records machine-readable blockers and remediation.

## What This Example Proves

- The facilitator does not proceed without a named SME.
- Unknown evidence sensitivity blocks review.
- A blocked review does not emit `question-pack.md`, `sme-decision-log.yaml`,
  `sme-signoff.md`, or `follow-up-findings.yaml`.
- Remediation is routed to the capability owner and
  `legacy-ibmi-evidence-intake`.
