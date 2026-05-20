# Adversarial Example: Non-Blocking Deferred TBD, Carried Forward

**Expected status:** `pass_with_warnings`  
**Internal status field:** `approved_with_non_blocking_tbd`  
**Triggered gate:** Step 3 — Blocking-TBD Check  
**Finding:** `BLOCKING-TBD-DEFERRED` (warning) — the TBD is *blocking* but
the SME has explicitly deferred it with a named resolver and date.  
**Routing:** none. Handoff proceeds; the TBD is carried verbatim into
`sdd-handoff.yaml.open_questions[]` and surfaced in
`atlas-context-pack.json`.

---

## Scenario

The Returns Processing (`RETURNS`) capability has both an approved BRD
and an approved `spec.yaml`. One open question carries a blocking flag,
but during spec review the capability-owner SME made an explicit decision
to defer it to a later phase, with a named resolver and a target date.

```text
05_specs/RETURNS/spec.yaml
  status: approved
  business_rules_approved: true
  acceptance_criteria_approved: true
  modernization_decisions_approved: true
  open_questions:
    - id: TBD-RETURNS-002
      question: "Should restocking fees apply to electronics returned within 30 days?"
      blocking: true
      resolution: "Deferred to Phase 2 by Aisha Khan (Returns Policy Owner) on 2026-05-15. Phase-2 cutover review will revisit with finance and product."
      resolver: "Aisha Khan"
      planned_resolution_date: "2026-07-31"
```

Compare with `handoff-blocked-blocking-tbd/`: same TBD shape, but here
the SME has done the work — named themselves, written a real resolution,
and committed to a date. The handoff treats this as a warning, not a
blocker.

## Why It Should Pass (with Warning, Not Cleanly)

The forward-SDLC contract permits non-blocking TBDs to be carried into
the handoff, *provided* they are explicit. Without the SME deferral the
TBD would still be blocking; with it, the Atlas chain can plan around the
gap. The gate records this as a `warning` (not `info`) precisely because
the question is *known to be unfinished*. Treating it as `info` would
hide a real future risk; treating it as `blocked` would penalise teams
that handle their open questions responsibly.

## Required Shape of an Acceptable Deferral

For Step 3 to emit `BLOCKING-TBD-DEFERRED` (warning) rather than
`BLOCKING-TBD-UNRESOLVED` (blocking), the TBD record must satisfy **all**
of the following:

| Field | Required value |
| --- | --- |
| `blocking` | `true` (after deferral the flag stays; SME chose not to demote) |
| `resolution` | non-empty, names the SME and the deferral target (phase, milestone, or date) |
| `resolver` | non-empty, names a real person (matches an SME on file for this capability) |
| `planned_resolution_date` | a future ISO 8601 date |

If any of these is missing, the workflow falls back to
`BLOCKING-TBD-UNRESOLVED` and blocks. See
`references/workflow.md#step-3` for the exact predicate.

(A TBD originally created with `blocking: false` is even simpler — it
produces an `info` finding under `NON-BLOCKING-TBD` and still maps to
`pass_with_warnings` overall because the spec carries an open question
into the handoff.)

## Expected Gate Behaviour

```text
Step 1 (BRD)            → pass
Step 2 (Spec)           → pass
Step 3 (Blocking-TBD)   → warning: BLOCKING-TBD-DEFERRED
Step 4 (BR → AC)        → pass
Step 5 (AC approved)    → pass
Step 6 (Evidence)       → pass
Step 7 (Traceability)   → pass
Step 8 (Package)        → assemble all five files
Step 9 (Sign-off)       → recorded by validator + SME handoff approver

Final status            → approved_with_non_blocking_tbd
Display label           → pass_with_warnings
Package files           → ALL FIVE WRITTEN
```

## What the Handoff Carries Forward

In the emitted `sdd-handoff.yaml`:

```yaml
status: "approved_with_non_blocking_tbd"

open_questions:
  - id: "TBD-RETURNS-002"
    question: "Should restocking fees apply to electronics returned within 30 days?"
    blocking: true
    resolution: "Deferred to Phase 2 by Aisha Khan (Returns Policy Owner) on 2026-05-15. Phase-2 cutover review will revisit with finance and product."
    resolver: "Aisha Khan"
    planned_resolution_date: "2026-07-31"
    deferral_recorded_in: "05_specs/RETURNS/spec-review.md#sme-decisions"

findings:
  blocking: []
  warnings:
    - id: "BLOCKING-TBD-DEFERRED"
      tbd_id: "TBD-RETURNS-002"
      severity: "warning"
      step: 3
      detail: "TBD has blocking: true but carries a named SME deferral with a planned resolution date. Carried forward into open_questions[]. Atlas chain should surface as a tagged backlog item with the named resolver and date."
      observed_only: true
  info: []
```

In `atlas-context-pack.json`, the same TBD appears under
`open_questions[]` so downstream agents can tag the corresponding stories
without re-deriving the context. Per the boundary contract
(`references/atlas-contract.md`), the handoff does **not** propose how
Atlas should handle the deferral — only that it exists, is named, and
has a date.

## Files in This Example

- `README.md` — this explanation
- `gate-summary.yaml` — example-only compact view of the warning outcome,
  derived from the five-file package shape

Unlike the blocked cases, this example does **not** ship a full
`blocking-finding.yaml` — there is no block. In a real run, the full
five-file handoff package is produced and no sixth `gate-summary.yaml` output
is written; orchestrators derive compact summaries from `sdd-handoff.yaml` or
`handoff-review.md`. We don't duplicate the full package here because the
canonical templates already illustrate the shape.

## Anti-Pattern Guarded Against

Two opposite mistakes the gate prevents:

1. **Over-blocking.** "There's still a `TBD-*`, so block." That would
   penalise responsibly-deferred work and force SMEs to launder real
   deferrals through cosmetic resolutions.
2. **Under-warning.** "It's just an open question, mark it `info`."
   That would hide a known-incomplete decision inside an otherwise
   green-looking handoff. A deferred blocking TBD is a future commitment
   and must be visible as a `warning`.

The example here is the goldilocks case: the handoff proceeds, the open
question is preserved verbatim, and downstream Atlas agents see it as a
named warning, not a silent risk.
