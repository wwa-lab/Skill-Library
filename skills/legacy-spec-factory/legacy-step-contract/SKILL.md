---
name: legacy-step-contract
description: Governance and quality-contract skill for every step in the Legacy Spec Factory reverse chain. Use when authoring, executing, or reviewing any pipeline step (inventory, program analysis, flow analysis, module analysis, spec writing, spec review, forward SDLC handoff) and you need a shared INPUT → EXECUTION → OUTPUT → VALIDATION contract. This is not a business analyzer — it does not produce inventory, program analyses, specs, or reviews itself. It defines, checks, and reports on the quality contract those skills must satisfy.
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

# Legacy Step Contract

## Purpose

Every step in the Legacy Spec Factory reverse chain follows the same shape:

```
INPUT  →  EXECUTION  →  OUTPUT  →  VALIDATION
```

This skill formalizes that shape into a **portable Step Contract** so that
authors, agents, and reviewers share one vocabulary across:

- `legacy-ibmi-inventory`
- `legacy-ibmi-program-analyzer`
- `legacy-ibmi-flow-analyzer`
- `legacy-ibmi-module-analyzer`
- `legacy-spec-writer`
- `legacy-spec-reviewer` (planned)
- forward SDLC handoff (`docs/forward-sdlc-contract.md`)
- future Layer 1 families (`legacy-cobol-*`, `legacy-mainframe-*`)

The skill defines (or reviews) **Step Contract blocks** and the **Step
Validation Report** shape. `legacy-step-validator` applies this contract to
completed artifacts and emits filled validation reports under `06_quality/`.
This skill does not produce inventory, program analyses, specs, or business
findings.

## When to Use

Trigger on any of these signals:

- An author or agent is **designing** a new pipeline step and needs a contract
  to anchor it.
- A step is **about to execute** and the runner wants to confirm its inputs
  and stop conditions before producing output.
- A step **has produced output** and a reviewer wants a structured pass / warn
  / block decision before downstream handoff.
- A skill review (`docs/skill-review-gate.md`) wants to verify that a skill's
  workflow and output contract are explicit and enforceable.
- An orchestrator (`legacy-modernization-orchestrator`) needs to surface why a
  gate is blocked in a uniform shape.

## When NOT to Use

Do not trigger when:

- The user wants the **business artifact itself** (inventory, program
  analysis, flow, module, spec, review). Route to the dedicated skill.
- The user wants SME interviews, capability discovery, or rule mining.
- The task is forward SDLC code generation. Use `wwa-lab/build-agent-skill`.
- The task is platform-specific extraction. Use the matching Layer 1 skill.

This skill is a **contract** layer. If you find yourself producing IBM i
facts, you are in the wrong skill.

## Role

You are the contract author / contract checker for one pipeline step.

You must:

- restate the step's INPUT, EXECUTION, OUTPUT, and VALIDATION explicitly
- distinguish mechanical validation, AI semantic review, and SME / human
  approval — they are not interchangeable
- produce a compact validation result with one of three statuses
- surface unresolved items by category so the next skill (or human) can act
- refuse to infer step content the upstream artifact does not contain

You must not:

- invent inputs the step does not actually have
- mark a step `pass` because it "looks right" — pass requires the validation
  evidence enumerated below
- collapse SME approval into AI semantic review

## The Step Contract

A Step Contract has four mandatory sections. See
[references/step-contract.md](references/step-contract.md) for the full
field-level specification, defaults, and worked examples.

### 1. INPUT

Required fields:

- `step_id` — stable ID for this step instance (`STEP-<SLUG>-<NNN>` per
  `docs/id-conventions.md`)
- `skill` — the skill or doc that executes the step (e.g.
  `legacy-ibmi-program-analyzer`)
- `prerequisite_artifacts` — list of upstream artifacts with their required
  status (e.g. `inventory.yaml` at `approved` or
  `approved_with_non_blocking_tbd`)
- `prerequisite_gates` — gates that must already be passing (Evidence
  Authorization, Inventory Completeness, Evidence Approval, Forward Handoff)
- `evidence_scope` — the `EV-*` IDs and `OBJ-*` IDs that are in scope, plus
  authorization fields (`sensitivity`, `source_path_verified`,
  `redaction_required`, `redaction_status`) that must already be resolved
- `sme_availability` — whether an SME owner is required for this step and the
  capability slug they own
- `assumptions_recorded` — assumptions the runner is allowed to make
  explicitly, never silently

Stop and refuse to execute the step if:

- any prerequisite artifact is missing or below the required status
- any prerequisite gate is blocked
- any evidence has `sensitivity: unknown`, lacks source-path authorization, or
  requires redaction without an approval record
- SME is required by the step but not assigned

### 2. EXECUTION

Required fields:

- `procedure` — pointer to the workflow inside the executing skill
  (`SKILL.md` section or `references/` file). The Step Contract does not
  re-describe the procedure; it cites it.
- `inputs_to_outputs_mapping` — which input fields drive which output fields
- `tools_allowed` — what the executing skill is allowed to do (read source,
  read DDS, call sub-skill, call SME, etc.)
- `tools_forbidden` — what the step must refuse (e.g. generating Java,
  inventing object names, reading unauthorized evidence)
- `decision_points` — any branch where the step must choose between
  alternatives, plus how that choice is recorded

Execution rules:

- The step writes its own output. The Step Contract does not.
- The step preserves IDs; it does not renumber on re-execution.
- The step records every assumption inline with the artifact it produces.

### 3. OUTPUT

Required fields:

- `primary_artifacts` — file paths, suggested filenames, and the schema or
  template each one must follow
- `id_namespaces` — which ID prefixes the step is allowed to mint
  (`BEH-*`, `BR-*`, `BR-*` seeds, `STEP-*`, `TBD-*`, etc.) per
  `docs/id-conventions.md`
- `cross_references` — what the output must link back to (every claim links
  to one or more `EV-*`; every `BR-*` links to `BEH-*` and `EV-*`)
- `status_field` — the lifecycle field the artifact carries (`draft`,
  `in_review`, `approved`, `approved_with_non_blocking_tbd`, `blocked`,
  `rejected`, `retired`)
- `non_outputs` — what the step is **not** allowed to produce (e.g. a flow
  analyzer does not produce capability specs)

### 4. VALIDATION

Validation has three distinct layers, in order. None substitutes for another.

#### 4a. Mechanical Validation

What can be checked by a script, a schema, or a deterministic linter:

- required files exist at expected paths
- YAML / JSON validates against `schemas/spec.schema.yaml` (or the relevant
  schema)
- all referenced IDs resolve (no dangling `EV-*`, `BR-*`, `OBJ-*`)
- ID prefixes match `docs/id-conventions.md`
- every claim has at least one linked evidence item
- every `sensitivity: unknown` is resolved and every evidence item has either
  source-path authorization or completed required redaction
- review status fields are in the allowed enum

Mechanical validation **must** be reproducible. If it depends on judgment,
move it to AI semantic review.

#### 4b. AI Semantic Review

What an LLM (or careful reviewer) can check by reading the artifact against
the upstream evidence:

- the artifact's claims are consistent with linked evidence
- knowledge type (`observed_behavior` / `inferred_business_rule` /
  `modernization_decision` / `unknown_tbd`) matches the kind of claim made
- evidence strength is not overstated (no `weakly_inferred` posing as
  `confirmed_from_code`)
- no invented IBM i facts (object names, fields, jobs, screens, reports)
- no scope creep into a different capability
- TBDs are explicit, not hidden inside prose

AI semantic review **must** call out uncertainty rather than smooth it over.

#### 4c. SME / Human Approval

What only a domain expert can decide:

- whether an inferred rule is actually a business rule
- whether a behavior the code shows is intentional or a bug
- whether a modernization decision is acceptable
- whether a TBD is blocking or non-blocking
- whether the step's output is safe to promote to `approved`

SME approval is a **control point**, not a rubber stamp. The Step Validation
Report must record the SME's name (or role), the date, and the specific
decision against the specific IDs.

## Compact Validation Result

Every step run must produce one of three statuses:

| Status | Meaning | Downstream Effect |
| --- | --- | --- |
| `pass` | Mechanical validation passes, AI semantic review finds no blocking issues, and (if applicable for this step) SME approval is recorded | The step's output may be consumed by the next step |
| `pass_with_warnings` | Mechanical validation passes; AI semantic review found non-blocking issues OR SME approved with non-blocking TBDs | Output may be consumed downstream, but the carried warnings must travel with it |
| `blocked` | At least one mechanical, semantic, or SME blocker exists | Output must not be consumed downstream until the blocker is resolved or explicitly waived by an SME |

A step is **not** allowed to self-promote past `blocked` without resolving or
explicitly waiving the blocker.

`pass_with_warnings` is for non-blocking items only; if you find yourself
adding a "warning" that is actually critical, the status is `blocked`.

## Surfacing Unresolved Items

Every Step Validation Report must categorize unresolved items into:

| Category | Definition | Typical Resolver |
| --- | --- | --- |
| `missing_inputs` | A required upstream artifact, status, or gate is absent | Run or finish the upstream skill / gate |
| `evidence_gaps` | An artifact reference exists but the evidence itself is missing, unreadable, or unauthorized | Source owner provides, authorizes, redacts, or formally waives the artifact |
| `contradictory_evidence` | Two or more evidence items disagree about behavior, rule, or field shape | SME decides which evidence holds; record the decision with a `DEC-*` |
| `sme_questions` | A judgment-only question that only a domain expert can answer | SME records the answer in the artifact's review section |
| `downstream_handoff_blockers` | An item that does not block this step's draft but will block the next step | Resolve before next step, or mark non-blocking with SME approval and forward |

Each item must carry:

- a stable ID (`TBD-<SLUG>-<NNN>`)
- the category above
- the artifact(s) it points to
- the resolver role
- whether it is blocking the current step, the next step, or both

Do **not** mix these categories together in a single bucket — that hides
which role can resolve which item.

## How the Contract Applies to Each Step

See [references/step-contract.md](references/step-contract.md) for the full
matrix. Summary:

| Step | Skill | Primary Input | Primary Output | SME Required At Pass? |
| --- | --- | --- | --- | --- |
| Inventory | `legacy-ibmi-inventory` | approved evidence manifest with source-path authorization or required redaction | `inventory.yaml`, `object-map.md` | Yes for inventory completion — `sme_review.decision` must be `approved` or `approved_with_non_blocking_tbd`; no for starting developer-led inventory |
| Program analysis | `legacy-ibmi-program-analyzer` | approved inventory + program source | `program-analysis.md` per program | Recommended; required if program affects money, inventory, compliance, or customer status |
| Flow analysis | `legacy-ibmi-flow-analyzer` | approved program analyses for chain | `flow-<FLOW-SLUG>.md` | Recommended; required if cross-program rule emerges |
| Module analysis | `legacy-ibmi-module-analyzer` | approved flow analyses + BAU notes | 4-view module package | Yes — for module-level capability seeds and BR-* seeds |
| Spec writing | `legacy-spec-writer` | approved module + flow + program + inventory | `spec.yaml`, `spec.md`, `spec-review.md`, `traceability.md` | Yes — `business_rules[*].review_status = approved` requires SME |
| Spec review | `legacy-spec-reviewer` (planned) | drafted spec | `review-report.md` | Yes — SME sign-off transitions spec from `in_review` to `approved` |
| Forward SDLC handoff | doc-only gate (`docs/forward-sdlc-contract.md`) | approved spec | handoff bundle to `wwa-lab/build-agent-skill` | Yes — gate is the SME-recognized contract |

The Step Contract block format is identical across all rows; only the field
values change. That is the point — one contract shape, every step.

## Workflow

### A. Authoring a Step Contract

1. Identify the step (inventory, program analysis, flow, module, spec, etc.).
2. Copy [templates/step-contract-block.md](templates/step-contract-block.md).
3. Fill INPUT, EXECUTION, OUTPUT, VALIDATION with the values for that step
   instance. Do not invent fields — use [references/step-contract.md](references/step-contract.md).
4. Cite the executing skill's procedure; do not re-describe it.
5. Record the SME role expected at pass, even if pass is not yet reached.

### B. Pre-Execution Check

1. Confirm every INPUT field has a concrete value.
2. Score input readiness using
   [`docs/input-readiness-rubric.md`](../../docs/input-readiness-rubric.md):
   identify hard blockers, minimum-pass inputs, optional missing inputs, and
   quality boosters before execution.
3. Confirm prerequisite gates are passing (do not assume).
4. If any INPUT field cannot be resolved, mark the step `blocked` immediately
   and surface the unresolved item under the correct category.
5. Only when INPUT is at least `minimum_pass`, hand control to the executing
   skill. A `minimum_pass` score may proceed with warnings; a `blocked` score
   must not.

### C. Post-Execution Validation

1. Run mechanical validation (4a). If anything fails, status is `blocked`.
2. Run AI semantic review (4b). Distinguish blocking findings from non-blocking.
3. Verify SME approval (4c) if the step requires it. SME absence at a step
   that needs SME is itself a blocker.
4. Apply `legacy-step-validator` to emit a
   [templates/step-validation-report.md](templates/step-validation-report.md)
   shaped report with status, findings by layer, and unresolved items by
   category.
5. If `pass_with_warnings`, the warnings travel with the artifact to the next
   step. Do not silently drop them.

### D. Reporting to the Orchestrator

When `legacy-modernization-orchestrator` asks "can this step's output be
consumed downstream?", answer in this exact shape:

```
status: pass | pass_with_warnings | blocked
step_id: STEP-<SLUG>-<NNN>
blocking_items: [TBD-..., TBD-...]
warnings: [TBD-...]
sme_decision: approved | approved_with_non_blocking_tbd | pending | blocked | not_required
downstream_next_step: <skill-name | doc-path | none>
remediation_step: <skill-name | doc-path | none>
```

Anything more verbose belongs in the full Step Validation Report.

## Workflow State Write-Back (history only)

This is a meta / contract skill — it defines the INPUT → EXECUTION →
OUTPUT → VALIDATION contract that other skills follow. It rarely runs
standalone. When it does, it produces a contract-conformance report and
does NOT mutate `capabilities[].stage_id` or `current_focus`.

After a run, append one `history[]` entry to
`<project-root>/workflow-state.yaml` per
[`docs/workflow-state-contract.md`](../../docs/workflow-state-contract.md):

```yaml
history:
  - at: <ISO 8601>
    skill: legacy-step-contract
    capability_id: <CAP-* from current_focus, or null>
    stage_after: <UNCHANGED stage_id, or null>
    artifact: <path to the conformance report, or null>
    note: "contract conformance check — <step-id>: pass | warnings | blocked"
```

Also overwrite `project.last_updated_at` / `project.last_updated_by`.

If `workflow-state.yaml` does not exist, this skill does NOT create it.

## Anti-Hallucination Rules

- Do not invent IBM i object names, field names, program names, job names, or
  capability slugs. The Step Contract carries IDs; it does not mint legacy
  facts.
- Do not promote a status. Only the executing skill plus its SME may promote
  an artifact from `draft` to `in_review` to `approved`.
- Do not collapse layers. Mechanical, semantic, and SME are not
  interchangeable.
- Do not paper over `unknown_tbd`. If evidence is missing, the answer is a
  `TBD-*` plus a category, not a confident summary.
- Do not approve based on confidence. `high` confidence does not bypass SME
  for business-critical claims (see
  `docs/evidence-and-knowledge-taxonomy.md`).
- Do not treat SME review as a rubber stamp. SME approval must name the SME,
  the date, and the specific IDs approved.

## Quality Checklist

Before emitting a Step Contract block, or before reviewing a Step Validation
Report emitted by `legacy-step-validator`, confirm:

- [ ] All four sections (INPUT, EXECUTION, OUTPUT, VALIDATION) are present
- [ ] Required fields per [references/step-contract.md](references/step-contract.md) are filled
- [ ] Mechanical, AI semantic, and SME approval are written as separate
      checks
- [ ] Status is `pass`, `pass_with_warnings`, or `blocked` — no third option
- [ ] Every unresolved item carries an ID, a category, an artifact pointer,
      and a resolver
- [ ] No IBM i facts have been invented; all object names come from upstream
      artifacts
- [ ] SME role is named when SME approval is required
- [ ] Cross-references (`EV-*`, `BR-*`, `OBJ-*`, `STEP-*`) resolve

## Relationship to Other Legacy Spec Factory Skills

- **`legacy-modernization-orchestrator`** consumes the compact validation
  result format to decide routing and gate state. The orchestrator does not
  re-derive validation; it reads reports emitted by `legacy-step-validator`.
- **Layer 1 skills** (`legacy-ibmi-inventory`,
  `legacy-ibmi-program-analyzer`, `legacy-ibmi-flow-analyzer`,
  `legacy-ibmi-module-analyzer`) and **Layer 2 skills**
  (`legacy-spec-writer`, future `legacy-spec-reviewer`) each have their own
  output contract; this skill wraps a portable Step Contract around them so
  that gates, reviews, and handoffs share one vocabulary.
- **`docs/skill-review-gate.md`** uses the same vocabulary when scoring a
  skill's workflow completeness and output contract.
- **`docs/forward-sdlc-contract.md`** is itself a Step Contract for the
  final crossing into `wwa-lab/build-agent-skill`.

This skill does not replace any of the above. It gives them a shared shape.

## Runtime Portability

The canonical skill source lives under:

```text
skills/legacy-step-contract/SKILL.md
skills/legacy-step-contract/references/step-contract.md
skills/legacy-step-contract/templates/step-contract-block.md
skills/legacy-step-contract/templates/step-validation-report.md
skills/legacy-step-contract/examples/inventory-pass/
```

Runtime copies may be synced to:

```text
.claude/skills/legacy-step-contract/
.opencode/skills/legacy-step-contract/
.agents/skills/legacy-step-contract/
.codex/skills/legacy-step-contract/
```

From the repository root, use `scripts/sync-skills.sh` to create or check
runtime copies. Do not edit adapter copies directly.

No runtime-specific assumptions are baked into this canonical source.

## Version History

- v0.1.2 (2026-05-29): Renamed flow-context-normalizer Step Contract wording
  from "draft four-flow package" to "draft four-view context package" so
  upstream context views are not confused with canonical module-analysis
  flow artifacts.
- v0.1.1 (2026-05-14): Added worked inventory-pass Step Contract and Step
  Validation Report examples. Reconciled compact validation result fields
  (`downstream_next_step`, `remediation_step`) and clarified that
  `legacy-step-validator` emits filled reports. Runtime smoke tests passed in
  Codex CLI (gpt-5.4-mini), Claude Code (haiku), and OpenCode
  (opencode/minimax-m2.5-free).
- v0.1.0 (2026-05-14): Initial Step Contract skill. Formalizes
  INPUT → EXECUTION → OUTPUT → VALIDATION across all reverse-chain steps.
  Distinguishes mechanical validation, AI semantic review, and SME approval.
  Defines compact validation result (`pass`, `pass_with_warnings`,
  `blocked`) and the five unresolved-item categories. Portable across Codex,
  Claude Code, and OpenCode.
