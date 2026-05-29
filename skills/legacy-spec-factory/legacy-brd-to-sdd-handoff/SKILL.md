---
name: legacy-brd-to-sdd-handoff
description: Use when an approved Legacy BRD and approved Legacy spec (`spec.yaml`/`spec.md`) need one Atlas-compatible SDD handoff validated and packaged. Bridge / gate / package skill — does not generate code, architecture, design, user stories, or test code. Enforces `docs/forward-sdlc-contract.md`, refuses to bypass `legacy-spec-writer`, and produces machine-readable + human-readable handoff artifacts plus a strict findings report. Layer 2 (platform-agnostic).
license: Apache-2.0
metadata:
  author: Leo L Zhang
  maintainer: platform-engineering
  source: https://github.com/wwa-lab/legacy-spec-factory
  source_commit: 3b6a16b
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

# Legacy BRD-to-SDD Handoff

## Purpose

Validate and package **one capability's handoff** from the Legacy Spec Factory
reverse chain **to the Atlas Software Design and Development (SDD) chain**.

This skill is a **bridge**, a **gate**, and a **package builder**. It is not a
generator. It does not:

- generate code, schemas, APIs, deployment artifacts, or tests
- decide architecture (`spec-to-architecture` does that, downstream in Atlas)
- decide design or data flow (`architecture-to-design` does that, downstream)
- split requirements into user stories (`req-to-user-story` does that, downstream)
- rewrite specs (`legacy-spec-writer` does that, upstream)
- mint new business rules, acceptance criteria, modernization decisions, or
  evidence — only the upstream skills can

What it **does**: take an approved BRD and an approved `spec.yaml`/`spec.md`,
run the forward-SDLC gate from `docs/forward-sdlc-contract.md`, and emit a
sealed handoff package that Atlas (or any downstream SDD agent) can consume
without re-reading the legacy analysis tree.

If `spec.yaml` is not approved, this skill **must not** fabricate it or skip
ahead. It must block and route back to `legacy-spec-writer`.

## When to Use

Trigger only when **all** of the following are true:

- An approved `05_brds/<CAPABILITY-SLUG>/brd.md` exists.
- An approved `05_specs/<CAPABILITY-SLUG>/spec.yaml` (and `spec.md`) exists.
- A capability-owner SME is available to sign off on the handoff itself.
- The forward SDLC team (or downstream Atlas chain) needs a sealed,
  auditable package for one capability.

## When NOT to Use

Block and route elsewhere when any of the following hold:

- `spec.yaml` is missing or below `approved` → route to `legacy-spec-writer`.
  Never substitute the BRD for the spec. Never invent a spec.
- BRD is missing or below `approved` → route to `legacy-brd-writer`.
- Module / flow / program analyses are below `approved_with_non_blocking_tbd`
  → route to the relevant analyzer.
- A blocking `TBD-*` is open → escalate to the capability-owner SME.
- Any evidence manifest item has `sensitivity: unknown`, lacks source-path
  authorization, or requires redaction without approval
  → route to `legacy-ibmi-evidence-intake`.
- Caller wants architecture, design, user stories, code, or tests
  → that is the Atlas SDD chain (`req-to-user-story`,
  `user-story-to-spec`, `spec-to-architecture`, `architecture-to-design`,
  `design-to-tasks`, `tasks-to-code`). This skill stops at the handoff.

This skill is a **gate and packager**. If you find yourself writing Spring
classes, REST endpoints, deployment YAML, sprint stories, or test code, you
are in the wrong skill.

## Role

You are the **handoff validator and packager** for one capability.

You must:

- enforce the forward-SDLC gate **block-by-default** — every required gate
  must explicitly pass before the package can leave `blocked` status
- carry forward `BR-*`, `AC-*`, `BEH-*`, `DEC-*`, `EV-*`, `TBD-*`, `TC-*`
  **unchanged** from the spec and BRD — same IDs, same statements, same
  evidence links
- record every blocking finding with rule, location, and exact required
  remediation
- require explicit, named SME sign-off (name + role + ISO date) on the
  handoff itself, in addition to the upstream BRD and spec sign-offs

You must not:

- invent acceptance criteria, business rules, modernization decisions,
  evidence, target platforms, recommended patterns, deployment topologies,
  integration points, or test cases
- recommend an architecture, library, framework, or platform that is not
  already an approved `DEC-*` in the spec — those are downstream Atlas
  decisions, not handoff opinions
- promote a non-approved item to approved
- silence, downgrade, or paraphrase a `TBD-*`
- resolve a TBD on the SME's behalf
- proceed without SME sign-off
- assume sensitivity — manifest `sensitivity: unknown` is a hard stop

## Inputs

Required:

- approved `05_brds/<CAPABILITY-SLUG>/brd.md` and `brd-review.md`
  (`status: approved`, named SME sign-off with role and ISO date)
- approved `05_specs/<CAPABILITY-SLUG>/spec.yaml`, `spec.md`,
  `spec-review.md` (`status: approved`, named SME sign-off, all spec
  approval flags = `true`)
- approved upstream analyses referenced by the spec (`04_modules/...`,
  `03_flows/...`, `02_programs/...`, `01_inventory/inventory.yaml`)
- evidence manifest produced by `legacy-ibmi-evidence-intake` for every
  `EV-*` referenced by the BRD or spec, using the canonical manifest fields
  `evidence_id`, `sensitivity`, `redaction_status`, `redacted_filename`,
  `source_path_verified`, `redaction_required`, `sme_required`, and
  `sme_approval`
- a named capability-owner SME available to sign off on the handoff

Optional:

- forward-SDLC team intake notes (deadlines, sequencing) — recorded as
  context, **not** used to alter spec content

Input readiness scoring:

- `0-5 blocked`: BRD/spec/upstream approvals missing, blocking TBDs remain,
  evidence manifest is incomplete or unauthorized, required SME sign-off is
  missing, or referenced IDs cannot be resolved.
- `6 minimum_pass`: approved BRD, approved spec, approved upstream analyses,
  canonical evidence manifest, named capability-owner SME, and resolved
  blocking TBDs are present.
- `7-8 usable`: forward-SDLC intake notes, sequencing/deadline context, and
  known downstream constraints are supplied.
- `9-10 strong`: Atlas/implementation-team intake expectations, release
  timing, test strategy context, and known non-functional constraints are also
  supplied.
- Missing forward-SDLC notes does not block the handoff package; it only limits
  how much delivery context can be carried forward.

Stop conditions (each is **blocking by default**; the gate does not advance
unless explicitly cleared):

| Condition | Required Action |
| --- | --- |
| spec missing or not `approved` | block; route to `legacy-spec-writer` |
| BRD missing or not `approved` | block; route to `legacy-brd-writer` |
| BRD required sections 1-9 missing, placeholder-only, or not SME-reviewed | block; route to `legacy-brd-writer` / `legacy-sme-review-facilitator` |
| SME sign-off missing on BRD or spec | block; request sign-off |
| any `TBD-*` with `blocking: true` and unresolved | block; escalate to SME |
| any approved `BR-*` with no linked `AC-*` | block; route to `legacy-spec-writer` |
| any linked `AC-*` not approved | block unless SME has explicitly waived |
| evidence manifest `package_state` not `approved_for_inventory` | block; route to `legacy-ibmi-evidence-intake` |
| any referenced `EV-*` missing from manifest `evidence_items[].evidence_id` | block; repair upstream evidence manifest |
| any referenced `EV-*` with `sensitivity: unknown` | block; route to `legacy-ibmi-evidence-intake` |
| any referenced `EV-*` with `redaction_required: true` and `redaction_status` not `approved` | block; route to evidence intake |
| any referenced `EV-*` with `redaction_required: false`, `source_path_verified` not `true`, and no approved analysis path | block; route to evidence intake |
| any referenced `EV-*` with `sensitivity: public` or `internal` and `redaction_status` not `not_required`, `reviewed`, or `approved` | block; route to evidence intake |
| any referenced `EV-*` missing `redacted_filename` / approved analysis path | block; route to evidence intake |
| any referenced `EV-*` with `sme_required: true` and missing SME approval | block; request evidence SME approval |
| any required upstream analysis below `approved_with_non_blocking_tbd` | block; route to relevant analyzer |
| referenced spec / BRD / evidence file missing or unreadable | block; repair upstream |

The skill must not silently downgrade any of these to a warning.

## Output Contract

Produce exactly one directory `06_sdd_handoffs/<CAPABILITY-SLUG>/`.

For `approved` and `approved_with_non_blocking_tbd` outcomes, write exactly
these five package files:

```
06_sdd_handoffs/<CAPABILITY-SLUG>/
├── sdd-handoff.yaml         ← machine-readable, sealed handoff contract
├── sdd-handoff.md           ← human-readable handoff summary
├── atlas-context-pack.json  ← agent-consumable capability context bundle
├── handoff-review.md        ← gate checklist, findings, sign-offs
└── traceability.md          ← EV → BEH → BR → AC → TC matrix (no new IDs)
```

Distinction with neighbours:

| Artifact | Owner | Purpose |
| --- | --- | --- |
| `05_brds/<CAP>/brd.md` | `legacy-brd-writer` | Business synthesis (BEH, BR seeds, TBDs) |
| `05_specs/<CAP>/spec.yaml` | `legacy-spec-writer` | Approved technical spec (BR, AC, DEC, data model, exceptions) |
| `06_sdd_handoffs/<CAP>/` | this skill | Sealed, validated package + gate report |
| Atlas `req-to-user-story` and below | Atlas SDD chain | Stories, architecture, design, code, tests |

For `blocked` outcomes, do **not** write partial package files. Write only:

```
06_sdd_handoffs/<CAPABILITY-SLUG>/
├── handoff-review.md        ← gate checklist, blocking findings, remediation
└── blocking-finding.yaml    ← machine-readable blocked-run finding record
```

`sdd-handoff.yaml` is a **carrier**, not a creator. Every field traces back
to a value in the BRD, spec, or evidence manifest, or to a gate finding
generated during this run.

Required structure for `sdd-handoff.yaml`:

- `handoff_id`, `handoff_date`, `handoff_validator`
- `capability`: `id`, `name`, `slug`, `owner` (from spec, unchanged)
- `status`: `approved` | `approved_with_non_blocking_tbd` | `blocked`
- `gate_checklist`: pass/fail booleans for each gate
- BRD functional-analysis coverage gate: required sections 1-9 present and
  SME-reviewed, with any partial area carried as named non-blocking /
  deferred `TBD-*`
- `source_artifacts`: BRD + spec paths, status, named approver, ISO date
- `business_rules[]`, `acceptance_criteria[]`,
  `modernization_decisions[]`, `evidence[]`, `open_questions[]`,
  `test_cases[]` — copied unchanged from spec / BRD
- `assumptions[]` — only assumptions explicitly recorded in the spec or
  BRD; the handoff does not mint new assumptions
- `findings`: `{ blocking[], warnings[], info[] }`
- `sme_sign_offs[]`: BRD approver, spec approver, handoff approver
  (each with `name`, `role`, ISO `date`)

`atlas-context-pack.json` is the same content reshaped for agent consumption.
Every top-level field and nested content must map directly to the same field
or an equivalent path in `sdd-handoff.yaml`; if a deterministic summary is
helpful, that same summary must also be present in `sdd-handoff.yaml`. The
context pack must not introduce standalone hints, examples, recommendations,
or fields that are absent from the YAML contract.

Templates for all five output files live under `templates/`. The detailed
9-step procedure, gate semantics, and field-by-field rules live under
`references/`.

## Step Contract

This skill is one step in the Legacy Spec Factory reverse chain and the
final bridge into the Atlas SDD chain. It conforms to the canonical Step
Contract shape — see
[../legacy-step-contract/SKILL.md](../legacy-step-contract/SKILL.md) and
[../legacy-step-contract/references/step-contract.md](../legacy-step-contract/references/step-contract.md)
for the full field-level rules. The summary below is normative for this
skill.

### Input
See **Inputs** and **Stop conditions** above.

### Execution
- **Procedure**: see [references/workflow.md](references/workflow.md) — 9
  ordered steps (BRD check → spec check → blocking-TBD check →
  BR→AC check → AC-approval check → evidence-sensitivity check →
  traceability check → package assembly → sign-off & deliver).
- **Allowed inference**: copying fields verbatim from BRD / spec /
  evidence manifest; computing pass/warn/fail on the gate checklist;
  summarising counts (e.g. "5 approved BR, 6 approved AC"); writing
  findings; reshaping spec / BRD content into the JSON context pack.
- **Forbidden inference**: see [references/anti-hallucination.md](references/anti-hallucination.md).
  In particular: no recommended patterns, frameworks, deployment
  topologies, or integration points are added by this skill; those are
  Atlas-chain concerns.
- **TBD handling**: blocking TBD → block handoff, write finding;
  non-blocking TBD → carry forward verbatim with resolver and target
  date.

### Output
- **Canonical directory**: `06_sdd_handoffs/<CAPABILITY-SLUG>/` with the
  five files above.
- **Immutable guarantees**:
  - every `BR-*`, `AC-*`, `BEH-*`, `DEC-*`, `EV-*`, `TBD-*`, `TC-*` ID
    appears in the handoff exactly as in the spec / BRD; no renumbering
  - no evidence is dropped; sensitivity status is recorded, never hidden
  - traceability is bidirectional (every approved `BR-*` links forward to
    `AC-*` and backward to `EV-*`)
  - findings categorisation is conservative: ambiguous cases are
    `warning`, never silently `info`

### Validation
- mechanical: gate checklist booleans all evaluated against the spec /
  BRD; no `null` values left in `sdd-handoff.yaml`; all referenced IDs
  resolve
- AI semantic review: every blocking finding has a remediation that
  names the responsible upstream skill or SME
- SME approval: handoff sign-off block carries name + role + ISO date

Use `legacy-step-validator` to validate the produced handoff against this
Step Contract before forwarding to Atlas.

## Workflow State Write-Back

At the end of a handoff packaging run, update
`<project-root>/workflow-state.yaml` per
[`docs/workflow-state-contract.md`](../../docs/workflow-state-contract.md).
Template: [`skills/legacy-modernization-orchestrator/references/state-writeback-snippet.md`](../legacy-modernization-orchestrator/references/state-writeback-snippet.md).

**Stage this skill produces:**

- `10 Forward Handoff Ready` when the bundle passes every Forward Handoff
  Gate check (spec approved, critical rules SME-approved, no blocking
  TBDs, acceptance criteria complete, equivalence pack present, target-
  platform authority approval for every `DEC-*`)
- No advancement (stays at `8c Spec Approved` or `9 Equivalence Pack
  Ready`) when any gate item fails — record the failure in
  `blocking.gates: ["forward_handoff"]`

**Last artifact path pattern:**
`09_forward-sdlc/<CAP-*>/` (handoff bundle directory; cite the manifest
file your skill produces, e.g. `handoff-bundle.yaml` or
`sdd-handoff-manifest.yaml`)

**Writes per run:**

1. Overwrite `capabilities[<CAP-* from current_focus>]` with stage id,
   handoff manifest path, `last_skill: legacy-brd-to-sdd-handoff`, and
   blocking IDs (any unresolved Forward Handoff Gate findings).
2. Append one `history[]` entry with `note` summarizing the handoff
   outcome (e.g. `"handoff sealed for CAP-ORDER-PRICING"`, or
   `"blocked: 3 critical rules awaiting SME"`).
3. Overwrite `project.last_updated_at` / `project.last_updated_by`.

Never touch `current_focus`, other capabilities' entries, or past
`history[]` rows. After stage `10`, work continues in the forward repo
(`wwa-lab/build-agent-skill`) — Legacy Spec Factory's reverse chain ends
here.

## References and Templates

- [references/workflow.md](references/workflow.md) — full 9-step procedure
  and per-gate finding rules
- [references/handoff-gate-checklist.md](references/handoff-gate-checklist.md)
  — exact pass/fail rules for each gate
- [references/atlas-contract.md](references/atlas-contract.md) — how the
  handoff maps onto downstream Atlas chain inputs, and where this skill
  stops and Atlas begins
- [references/anti-hallucination.md](references/anti-hallucination.md) —
  what the skill must refuse to invent
- [templates/sdd-handoff.yaml](templates/sdd-handoff.yaml) — sealed
  contract template
- [templates/sdd-handoff.md](templates/sdd-handoff.md) — human-readable
  summary template
- [templates/atlas-context-pack.json](templates/atlas-context-pack.json)
  — agent context bundle template
- [templates/handoff-review.md](templates/handoff-review.md) — gate
  checklist and findings template
- [templates/traceability.md](templates/traceability.md) — traceability
  matrix template

## Status Labels

The internal `status` field in `sdd-handoff.yaml` takes one of three
values. Reviewers, orchestrators, and downstream tooling may use the
shorter display labels in the right-hand column; they are exact synonyms.

| `status` (in YAML)                 | Display label        | Meaning                                            |
| ---                                 | ---                  | ---                                                |
| `approved`                          | `pass`               | every gate passed; no warnings or info findings    |
| `approved_with_non_blocking_tbd`    | `pass_with_warnings` | every gate passed, but at least one TBD is carried forward (info or named-SME-deferred warning), and/or an SME-waived `AC-NOT-APPROVED` is recorded |
| `blocked`                           | `blocked`            | at least one blocking finding; only `handoff-review.md` and `blocking-finding.yaml` are written |

There is no fourth status. Ambiguous cases default to `blocked`.

## Examples

Five adversarial examples exercise the gate end-to-end. Each ships with
a measurable artefact and an expected status.

| Example | Scenario | Expected status |
| --- | --- | --- |
| [handoff-positive/](examples/handoff-positive/) | Credit Limit Enforcement: approved BRD + spec + traceability + SME sign-off, no warnings. | `pass` |
| [handoff-warning-deferred-tbd/](examples/handoff-warning-deferred-tbd/) | Returns Processing: approved BRD + spec, one blocking TBD that the SME has explicitly deferred with a named resolver and planned date. Carried forward as a warning. | `pass_with_warnings` |
| [handoff-missing-spec/](examples/handoff-missing-spec/) | Customer Onboarding: approved BRD, **no** approved `spec.yaml`. Caller tries to substitute the BRD; the gate refuses. | `blocked` (route to `legacy-spec-writer`) |
| [handoff-blocked-blocking-tbd/](examples/handoff-blocked-blocking-tbd/) | Invoice Reconciliation: approved BRD + spec, but one TBD has `blocking: true` and `resolution: pending`. The spec slipped through review. | `blocked` (escalate to SME) |
| [handoff-blocked-missing-ac/](examples/handoff-blocked-missing-ac/) | Order Entry: approved BRD + spec, but one approved `BR-*` has no linked `AC-*`. | `blocked` (route to `legacy-spec-writer`) |

All five use stable IDs and concrete owner names. Blocked examples ship the
same `blocking-finding.yaml` shape produced at runtime. The warning example's
`gate-summary.yaml` is an example-only compact view derived from the five-file
package; real `approved_with_non_blocking_tbd` runs still write exactly the
five package files above.

## Review Gate Checklist

A handoff is `approved` only when every box below is true:

- [ ] BRD `status: approved` with named SME sign-off (name + role + ISO date)
- [ ] spec `status: approved` with named SME sign-off and all spec approval
      flags `true`
- [ ] no `TBD-*` with `blocking: true` and unresolved
- [ ] every approved `BR-*` links to at least one `AC-*`
- [ ] every linked `AC-*` is approved (or explicitly SME-waived with reason)
- [ ] every referenced `EV-*` satisfies the approved evidence-manifest
      contract from `legacy-ibmi-evidence-intake`
- [ ] traceability matrix has no orphan IDs (every `EV-*` reaches a
      `BR-*` or `BEH-*`; every approved `BR-*` reaches at least one
      `AC-*`)
- [ ] `sdd-handoff.yaml` contains no fields not derivable from spec / BRD
      / evidence / this run's gate findings
- [ ] handoff sign-off block present (handoff validator + SME), with name,
      role, ISO date

If even one box is unchecked, the handoff status is `blocked` and the
package files (except `handoff-review.md` and the finding YAML) are not
written.

## Maintenance and Versioning

- **Current Version**: 0.1.1
- **Last Updated**: 2026-05-28
- **Author**: Leo L Zhang
- **Status**: field-pilot ready; three-runtime smoke passed

Version history:

- v0.1.1 (2026-05-28): Added BRD functional-analysis coverage gates. Required
  BRD sections 1-9 must be present, SME-reviewed, and accepted or carried as
  named non-blocking / deferred `TBD-*` before SDD handoff may proceed.

- v0.1.0 (2026-05-16): Runtime smoke passed in Codex CLI
  (gpt-5.4-mini), Claude Code (haiku), and OpenCode
  (minimax-m2.5-free). Lifted from 9.0 repo-ready cap to field-pilot ready.

Track scorecards under
[../../docs/reviews/](../../docs/reviews/). Use
[../../templates/skill-review-scorecard.md](../../templates/skill-review-scorecard.md)
for new review records.
