# Adversarial Example: Approved BRD, No Approved Spec

**Expected status:** `blocked`  
**Triggered gate:** Step 2 — Validate Spec Status and Sign-Off  
**Finding:** `SPEC-MISSING` (blocking)  
**Routing:** back to `legacy-spec-writer`

---

## Scenario

The Customer Onboarding (`CUST-ONBOARD`) capability has a clean,
SME-approved BRD. A stakeholder asks the orchestrator to "skip the spec
and just package up the BRD for Atlas" because the deadline is tight and
"the BRD already has the business rules in it."

```text
05_brds/CUST-ONBOARD/
  brd.md             status: approved  signed: Priya Patel (Customer Ops Lead) 2026-05-14
  brd-review.md      sign-off block complete

05_specs/CUST-ONBOARD/
  (directory does not exist)
```

This is the most common attempt to bypass `legacy-spec-writer`.

## Why It Must Block

The forward-SDLC contract in `docs/forward-sdlc-contract.md` requires
`spec.yaml`, not the BRD. They are different artefacts with different
ownership:

| Concern | BRD (`05_brds/`) | Spec (`05_specs/`) |
| --- | --- | --- |
| Audience | business stakeholders | engineers + Atlas chain |
| `BR-*` status | seed / `needs_sme_review` | `approved` after rule extraction |
| `AC-*` | not produced | produced and SME-approved here |
| `DEC-*` | not produced | produced and approved here |
| Data model, inputs/outputs, exceptions | informal | structured, schema-conformant |

A BRD is not an acceptable substitute. If the handoff skill accepted the
BRD alone, the Atlas chain would receive un-promoted rule seeds and zero
acceptance criteria. That is the failure mode `BR-MISSING-AC` is
designed to prevent — but here it is prevented one step earlier by
refusing to advance without `spec.yaml`.

## Expected Gate Behaviour

```text
Step 1 (BRD)            → pass
Step 2 (Spec)           → FAIL: SPEC-MISSING (blocking)
Step 3 onward           → not executed (short-circuit per workflow.md)
Package files           → NOT WRITTEN (per workflow Step 9b)
Emitted artefacts       → handoff-review.md, blocking-finding.yaml
```

## Files in This Example

- `README.md` — this explanation
- `blocking-finding.yaml` — machine-readable record of the blocked run

The five package files (`sdd-handoff.yaml`, `sdd-handoff.md`,
`atlas-context-pack.json`, `handoff-review.md`, `traceability.md`) are
deliberately absent. Emitting a partial handoff here would mislead the
Atlas chain into believing the capability was specified.

## Recovery Path

1. Orchestrator routes the request to `legacy-spec-writer` with the
   approved BRD and the upstream module/flow/program analyses.
2. `legacy-spec-writer` produces `spec.yaml`, `spec.md`,
   `spec-review.md`, and `traceability.md` under
   `05_specs/CUST-ONBOARD/`.
3. The SME approves `business_rules`, `acceptance_criteria`, and
   `modernization_decisions`; sets `status: approved`.
4. The handoff is re-run. Step 2 now passes.

## Anti-Pattern Guarded Against

A reader of the prompt might think "the BRD has the business rules, just
ship that to Atlas." The handoff skill is explicitly written to refuse
this. See `SKILL.md` Purpose: *"If `spec.yaml` is not approved, this skill
must not fabricate it or skip ahead. It must block and route back to
`legacy-spec-writer`."*
