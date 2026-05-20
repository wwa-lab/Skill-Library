# Adversarial Example: Approved Spec with an Unresolved Blocking TBD

**Expected status:** `blocked`  
**Triggered gate:** Step 3 — Blocking-TBD Check  
**Finding:** `BLOCKING-TBD-UNRESOLVED` (blocking)  
**Routing:** escalate to the capability-owner SME

---

## Scenario

The Invoice Reconciliation (`INVOICE-RECON`) capability has both an
approved BRD and an approved `spec.yaml`. The SME signed off all three
spec approval flags. But the spec still carries one open question that
was marked **blocking** during rule extraction and is not resolved.

```text
05_specs/INVOICE-RECON/spec.yaml
  status: approved
  business_rules_approved: true
  acceptance_criteria_approved: true
  modernization_decisions_approved: true
  open_questions:
    - id: TBD-INVOICE-RECON-004
      question: "How are partial payments allocated when an invoice spans two fiscal periods?"
      blocking: true
      resolution: "pending"           # <-- unresolved
      resolver: null
      planned_resolution_date: null
```

This is a realistic safety-net case: the spec-writer marked `status:
approved` because the rule set and acceptance criteria look complete, but
left a blocking TBD un-cleared. The handoff gate catches the slip.

## Why It Must Block

`docs/forward-sdlc-contract.md` requires that *no blocking TBD remains*
before the reverse chain may hand off to forward SDLC. The Atlas chain
will start picking targets, generating user stories, and proposing
architecture — all of which can be invalidated when the deferred decision
finally lands. The cost of blocking now is much smaller than the cost of
unwinding Atlas work later.

A blocking TBD is **never** silently demoted, paraphrased, or "moved to
backlog" by this skill. The decision to demote it belongs to the named
capability-owner SME.

## Expected Gate Behaviour

```text
Step 1 (BRD)            → pass
Step 2 (Spec)           → pass
Step 3 (Blocking-TBD)   → FAIL: BLOCKING-TBD-UNRESOLVED (blocking)
Step 4 onward           → not executed (short-circuit per workflow.md)
Package files           → NOT WRITTEN
Emitted artefacts       → handoff-review.md, blocking-finding.yaml
```

## Three Outcomes the SME May Choose

When the SME is brought in for this finding, exactly three resolutions are
admissible (each requires the SME to record the decision in
`spec-review.md`):

1. **Resolve the question.** Add evidence or a decision, mark the TBD
   `blocking: false`, set `resolution`. Re-run handoff → `pass` or
   `pass_with_warnings`.
2. **Demote to non-blocking with explicit deferral.** Keep
   `blocking: true` but set `resolution: "Deferred to Phase N by <SME>"`,
   set `resolver` and `planned_resolution_date`. Re-run handoff →
   `pass_with_warnings` (finding `BLOCKING-TBD-DEFERRED`).
3. **Pull the affected behaviour out of scope.** Update the spec's
   `scope.out_of_scope`, remove the TBD (or mark it `status: retired`
   per `docs/id-conventions.md`). Re-run handoff → `pass`.

What the SME **may not** do:
- silently delete the TBD without recording the rationale
- ask the handoff skill to ignore the TBD without re-running the spec
  review

## Files in This Example

- `README.md` — this explanation
- `blocking-finding.yaml` — machine-readable record of the blocked run

## Anti-Pattern Guarded Against

"The spec says `status: approved`, so just package it." A blocking TBD
inside an otherwise-approved spec is a real and recurring case; this
gate's job is to catch the spec-writer's slip before Atlas inherits it.
