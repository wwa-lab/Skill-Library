---
name: legacy-golden-master-test-planner
description: "Produce an evidence-backed old-vs-new golden master test plan from an approved Legacy spec, approved acceptance criteria, and redacted runtime evidence. Use when a capability has `spec.yaml.status: approved` and the team needs `TC-*` golden master cases, sample-data references, expected-output references, and equivalence coverage before forward SDLC or implementation validation. Planning skill only: it does not generate executable test code, run comparisons, collect raw production data, or invent expected outputs."
license: Apache-2.0
metadata:
  author: Leo L Zhang
  maintainer: platform-engineering
  source: https://github.com/wwa-lab/legacy-spec-factory
  source_commit: 8871a6b
  domain: legacy-spec-factory
---

<!--
Legacy Spec Factory
Copyright 2026 Leo L Zhang

Original author: Leo L Zhang
License: Apache License 2.0

This skill is part of the Legacy Spec Factory project.
Retain this notice in substantial copies or derived versions.
-->

# Legacy Golden Master Test Planner

## Purpose

Plan one capability's **golden master equivalence tests** so the target
Java/cloud implementation can later be compared against approved legacy
behavior.

The planner turns an approved `spec.yaml` plus redacted runtime evidence into a
reviewable `TC-*` test catalog. Each test case identifies:

- the approved `BR-*` / `AC-*` it validates
- the legacy transaction, screen path, batch job, report, spool, or data
  scenario it represents
- the redacted input sample reference
- the legacy expected-output reference
- the comparison rules needed to decide whether the new system is equivalent

This skill is a **planner**, not a harness generator. It does not write JUnit,
execute the legacy system, execute the new system, or decide that a target
implementation is correct.

## When to Use

Trigger when:

- `05_specs/<CAPABILITY-SLUG>/spec.yaml` is approved and contains approved
  `BR-*` and `AC-*` IDs.
- The forward SDLC handoff or implementation team needs golden master cases for
  old-vs-new comparison.
- Runtime evidence is already collected, redacted, and approved for agent use.
- A capability-owner SME is available to approve test selection and expected
  outputs.
- Existing spec `tests[]` are sketches and need to be expanded into an
  auditable equivalence plan.

## When NOT to Use

Block and route elsewhere when:

- `spec.yaml` is missing, below `approved`, or has unapproved business-critical
  `BR-*` / `AC-*` IDs -> route to `legacy-spec-writer` or spec review.
- Expected outputs are not backed by runtime evidence -> request runtime
  evidence collection; do not guess.
- Evidence has `sensitivity: unknown`, unresolved required redaction, missing
  source-path authorization, or raw production payload -> route to
  `legacy-ibmi-evidence-intake`.
- The caller wants executable unit, integration, API, or harness code -> route
  to the downstream SDLC/test-generation chain.
- The caller wants to change acceptance criteria, business rules, or
  modernization decisions -> route to the owning upstream skill.

If you find yourself inventing sample data, rewriting `BR-*`, or choosing a
target test framework, you are in the wrong skill.

## Role

You are the **equivalence test planner** for one approved capability.

You must:

- preserve existing `CAP-*`, `BR-*`, `AC-*`, `BEH-*`, `EV-*`, `DEC-*`, and
  `TBD-*` IDs unchanged
- mint `TC-*` IDs only for planned golden master test cases
- require each `TC-*` to validate at least one approved `AC-*` or approved
  business-critical `BR-*`
- require every input and expected output to cite redacted, approved evidence
- distinguish exact comparisons from normalized, tolerant, or presence-based
  comparisons
- surface coverage gaps as `FIND-*` or `TBD-*` instead of hiding them
- require SME sign-off before marking the plan `approved`

You must not:

- invent expected outputs from business rules, code reading, or field names
- use unredacted production samples
- promote a test case to approved without SME review
- create new `BR-*`, `AC-*`, `DEC-*`, `EV-*`, `BEH-*`, or implementation tasks
- claim the target system is equivalent; this skill only plans comparison

## Inputs

Required:

- Approved `05_specs/<CAPABILITY-SLUG>/spec.yaml` and `spec.md`.
- Approved `spec-review.md` showing capability-owner sign-off.
- Approved `acceptance_criteria[]` and business-critical `business_rules[]`.
- Redacted runtime evidence for selected cases, such as:
  - sample transactions
  - job logs
  - spool outputs
  - report outputs
  - screen captures or screen-flow notes
  - DB before/after snapshots
  - message queue or integration payload samples
- Evidence manifest / redaction log proving every sample is approved for agent
  processing.
- Named capability-owner SME for test-plan approval.

Optional:

- Approved BRD for business-language context.
- Existing `spec.yaml.tests[]` sketches.
- Forward SDLC handoff notes that state which cases are mandatory for the first
  implementation milestone.

Stop and require remediation if:

| Condition | Required action |
| --- | --- |
| Spec missing or not `approved` | Block; route to `legacy-spec-writer` / spec review |
| Business-critical `BR-*` lacks approved `AC-*` | Block; route to `legacy-spec-writer` |
| No redacted runtime evidence for expected outputs | Block; request runtime evidence collection |
| Evidence sensitivity is `unknown` or redaction is not approved | Block; route to `legacy-ibmi-evidence-intake` |
| Expected output is inferred instead of observed | Block; request runtime evidence or SME-recorded waiver |
| SME owner unavailable | Produce draft only; cannot mark approved |
| Contradictory legacy outputs for same scenario | Mark blocked unless SME records the intended behavior |

## Output Contract

Produce one directory:

```text
06_quality/<CAPABILITY-SLUG>/
+-- golden-master-tests.yaml     # canonical machine-readable test plan
+-- golden-master-tests.md       # human-readable plan
+-- equivalence-coverage.md      # BR/AC/EV to TC coverage matrix
+-- sample-data-manifest.md      # redacted sample and expected-output refs
+-- test-plan-review.md          # review checklist, findings, sign-offs
```

For a blocked run, do not emit an approved test catalog. Produce:

```text
06_quality/<CAPABILITY-SLUG>/
+-- test-plan-review.md
+-- blocking-findings.yaml
```

Use the templates in `templates/` as starting structure:

- `templates/golden-master-tests.yaml`
- `templates/golden-master-tests.md`
- `templates/equivalence-coverage.md`
- `templates/sample-data-manifest.md`
- `templates/test-plan-review.md`
- `templates/blocking-findings.yaml`

Use the reference files only when needed:

- `references/test-case-selection.md` when deciding which `BR-*` / `AC-*`
  need golden master coverage.
- `references/comparison-modes.md` when choosing exact, normalized, tolerant,
  presence, or ordering-insensitive comparison rules.
- `references/anti-hallucination.md` when reviewing whether a test input,
  expected output, tolerance, ignored field, or edge case was invented.

Follow:

- `../../../docs/legacy-spec-factory/id-conventions.md` for stable IDs (`TC-*`, `FIND-*`, `TBD-*`)
- `../../../docs/legacy-spec-factory/evidence-and-knowledge-taxonomy.md` for evidence strength and
  knowledge type
- `../../../docs/legacy-spec-factory/data-collection-and-redaction.md` for sample-data safety
- `../../../docs/legacy-spec-factory/forward-sdlc-contract.md` for handoff readiness
- `../../../docs/legacy-spec-factory/input-readiness-rubric.md` for input readiness scoring
- `../legacy-step-contract/SKILL.md` for the shared Step Contract

Examples:

- `examples/golden-master-positive/` - approved CREDIT-LIMIT test plan with
  evidence-backed `TC-*`, coverage, sample manifest, and sign-offs.
- `examples/blocked-missing-runtime-evidence/` - blocked run where an approved
  AC lacks redacted runtime evidence for expected outputs.

## Step Contract

This skill is one step in the Legacy Spec Factory reverse chain. It conforms to
the canonical Step Contract shape.

### Input

- **Required**: approved spec package; approved `BR-*` and `AC-*`; redacted
  runtime evidence; evidence manifest / redaction log; capability-owner SME.
- **Optional**: approved BRD, existing `tests[]` sketches, forward SDLC intake
  notes.
- **Input readiness scoring**:
  - `0-5 blocked`: approved spec missing, business-critical `BR-*` lacks
    approved `AC-*`, expected-output runtime evidence missing, evidence
    authorization unresolved, contradictory outputs lack SME decision, or no
    SME can approve the plan.
  - `6 minimum_pass`: approved spec, approved critical rules and ACs, observed
    runtime evidence for selected cases, evidence manifest, and SME owner are
    present.
  - `7-8 usable`: approved BRD, existing test sketches, and forward-SDLC intake
    notes are supplied.
  - `9-10 strong`: boundary/negative cases, period-end examples, before/after
    DB snapshots, spool/report samples, and integration payload samples are
    also supplied.
  - Missing BRD or test sketches does not block when runtime expected outputs
    are present; missing observed expected output does block.
- **Readiness checks**: spec approved; no blocking TBDs; every business-critical
  rule has at least one AC; evidence sensitivity reviewed; sample data approved
  for agent use.
- **Stop conditions**: missing approved spec, missing expected-output evidence,
  sensitivity unknown, contradictory outputs without SME decision, or no SME for
  approval.

### Execution

- **Procedure**: see the Workflow section below.
- **Allowed inference**: selecting representative and edge cases from approved
  rules and ACs; classifying comparison type; identifying coverage gaps.
- **Forbidden assumptions**: inventing test input values, legacy outputs,
  field meanings, error messages, ordering rules, tolerances, or downstream
  framework choices.
- **TBD handling**: missing sample -> `TBD-*` or `FIND-*` with resolver;
  contradictory output -> blocking finding; non-critical untestable AC -> SME
  waiver or deferred test note.

### Output

- **Canonical directory**: `06_quality/<CAPABILITY-SLUG>/`.
- **Required IDs**: mint `TC-*` for test cases; mint `FIND-*` for validation
  findings; mint `TBD-*` only for unresolved questions not already present.
- **Reused IDs**: `CAP-*`, `BR-*`, `AC-*`, `BEH-*`, `EV-*`, `DEC-*`, `OBJ-*`,
  `FLOW-*`, `STEP-*`.
- **Non-outputs**: no executable tests, code, harness configuration, generated
  target-system expectations, architecture decisions, or rewritten specs.
- **Status**: `draft` -> `in_review` -> `approved` or `blocked`.

### Validation

Mechanical validation:

- required files exist for non-blocked outcomes
- every `TC-*` uses the correct capability slug and validates at least one
  approved `AC-*` or approved business-critical `BR-*`
- every `TC-*` cites input evidence and expected-output evidence
- no referenced evidence has `sensitivity: unknown`
- every `BR-*` / `AC-*` marked business-critical is covered by at least one
  `TC-*` or has an SME-approved deferral
- coverage matrix and YAML catalog contain the same `TC-*` IDs

AI semantic review:

- chosen tests cover happy path, negative path, edge/boundary path, exception
  behavior, and important report/spool/batch side effects where applicable
- expected outputs are observed from runtime evidence, not inferred from the
  spec
- comparison rules preserve legacy semantics without overfitting volatile
  fields such as timestamps, job numbers, sequence IDs, or redacted identifiers
- weak or contradictory evidence remains visible as findings
- no test case quietly changes an approved business rule or acceptance
  criterion

SME / human approval:

- capability-owner SME approves selected cases, expected outputs, comparison
  rules, and any deferrals
- test data owner confirms sample use is approved
- forward SDLC/test owner confirms the plan is consumable by the future harness
- approval records include name, role, ISO date, and IDs approved

## Workflow

1. **Confirm Scope and Gates**
   - Load one approved spec package for one `CAP-*`.
   - Confirm no blocking TBDs remain.
   - Identify all business-critical `BR-*` and approved `AC-*`.
   - Stop immediately on redaction or approval failures.

2. **Build the Coverage Inventory**
   - List every `BR-*`, linked `AC-*`, `BEH-*`, `EV-*`, exception, input, and
     output relevant to equivalence.
   - Mark each item as `must_test`, `should_test`, `defer_with_reason`, or
     `not_golden_master_candidate`.
   - A business-critical rule defaults to `must_test`.

3. **Collect Runtime Evidence References**
   - Use only redacted, approved sample references.
   - Separate input samples from expected-output samples.
   - Preserve field shape, decimal scale, sign, ordering, and edge-case values.
   - Record missing evidence as a finding; do not create placeholder values.

4. **Select Golden Master Cases**
   - Cover at least one normal success path for each critical capability.
   - Cover business rejection paths, exception paths, boundaries, rounding,
     missing-record behavior, duplicate/idempotency behavior, report/spool
     outputs, and batch restart behavior where the spec says they matter.
   - Load `references/test-case-selection.md` for detailed selection rules when
     the capability has many `BR-*` / `AC-*` candidates.
   - Avoid redundant cases that validate the same AC with the same evidence.

5. **Define Each `TC-*`**
   - Assign a stable `TC-<CAPABILITY-SLUG>-NNN`.
   - State intent, priority, validated `BR-*` / `AC-*`, legacy execution path,
     preconditions, input refs, expected-output refs, comparison mode,
     normalization rules, data reset needs, and review status.
   - Use exact comparison by default unless evidence proves normalization or
     tolerance is required.

6. **Classify Comparison Rules**
   - `exact`: values and ordering must match.
   - `normalized`: compare after documented transformations such as date format
     or redacted ID mapping.
   - `tolerant`: numeric or time tolerance explicitly approved by SME.
   - `presence`: output must contain or omit specified records/messages.
   - `ordering_insensitive`: same logical rows may appear in any order.
   - Load `references/comparison-modes.md` before using anything other than
     `exact`.

7. **Record Gaps and Deferrals**
   - Missing runtime sample -> blocking for business-critical coverage.
   - Non-critical AC without sample -> warning only if SME signs deferral.
   - Contradictory outputs -> blocking until SME selects intended behavior.
   - Unclear expected output -> block; never infer.
   - Load `references/anti-hallucination.md` when reviewing suspected invented
     sample data, expected outputs, tolerances, ignored fields, or edge cases.

8. **Write the Test Plan Package**
   - Fill `golden-master-tests.yaml` first as the canonical artifact.
   - Render `golden-master-tests.md` from the same content.
   - Generate `equivalence-coverage.md` and `sample-data-manifest.md`.
   - Prepare `test-plan-review.md` with findings and sign-off rows.

9. **Prepare Handoff**
   - If approved, note which `TC-*` IDs should be copied into `spec.yaml.tests[]`
     or the SDD handoff package by the owning handoff/spec process.
   - If blocked, emit `blocking-findings.yaml` with exact remediation steps.
   - Do not silently edit an already approved spec unless the user explicitly
     asks and the repository workflow allows reopening the spec for review.

## Workflow State Write-Back

At the end of a test-planning run, update
`<project-root>/workflow-state.yaml` per
[`docs/workflow-state-contract.md`](../../../docs/legacy-spec-factory/workflow-state-contract.md).
Template: [`skills/legacy-modernization-orchestrator/references/state-writeback-snippet.md`](../legacy-modernization-orchestrator/references/state-writeback-snippet.md).

**Stage this skill produces:**

- `9 Equivalence Pack Ready` when the test plan covers every approved rule
  in `spec.yaml` with `TC-*` cases, sample-data references, and
  expected-output references — and every reference resolves
- No advancement (stays at `8c Spec Approved`) when coverage gaps remain;
  record blockers in `blocking.gates: ["forward_handoff"]` plus the
  uncovered rule IDs in `blocking.sme_pending`

**Last artifact path pattern:** `06_quality/<CAP-*>/golden-master-tests.md`

**Writes per run:**

1. Overwrite `capabilities[<CAP-* from current_focus>]` with stage id, the
   test-plan path, `last_skill: legacy-golden-master-test-planner`, and
   blocking IDs (uncovered rule IDs / missing samples).
2. Append one `history[]` entry with `note` summarizing coverage
   (e.g. `"golden-master plan covers 12 of 12 approved rules"`).
3. Overwrite `project.last_updated_at` / `project.last_updated_by`.

Never touch `current_focus`, other capabilities' entries, or past
`history[]` rows. A re-run on the same capability is allowed; a re-run
that would lower `stage_id` requires the orchestrator's Rollback Protocol.

## Completion Checklist

Before calling the work done, confirm:

- every business-critical approved `BR-*` has golden master coverage or a
  named SME deferral
- every `TC-*` has input and expected-output evidence IDs
- sample sensitivity and redaction status are explicitly reviewed
- comparison rules are concrete enough for a downstream harness to implement
- the plan does not contain generated test code or target-system assumptions
- SME approval status is visible and not implied
