---
name: legacy-step-validator
description: Use when any Legacy Spec Factory step artifact needs validation against the INPUT → EXECUTION → OUTPUT → VALIDATION contract. Use after a step has produced its draft artifact (inventory, program analysis, flow, module, spec, or handoff bundle) and you need a structured `pass` / `pass_with_warnings` / `blocked` review report with mechanical, semantic, and SME-readiness findings. This skill does not produce business artifacts itself and does not replace SME approval — it surfaces what is mechanically valid, what needs semantic review, and what only an SME can decide.
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

# Legacy Step Validator

## Purpose

Audit one completed step package against the Step Contract (defined in
`../legacy-step-contract/SKILL.md` and
`../legacy-step-contract/references/step-contract.md`) and emit a
structured validation report. The skill works across all reverse-chain
steps:

- inventory (`01_inventory/`)
- program analysis (`program-analysis-<OBJ-ID>.md`)
- flow analysis (`flow-<FLOW-SLUG>.md`)
- module analysis (`04_modules/<MODULE-SLUG>/`)
- spec writing (`05_specs/<CAPABILITY-SLUG>/`)
- forward SDLC handoff (`docs/forward-sdlc-contract.md`)

Spec-review-as-its-own-step is intentionally out of scope until
`legacy-spec-reviewer` exists. Until then, validate `spec-review.md` as part
of the spec-writing package and use the spec-writing checklist as the manual
fallback.

This is a **review skill**. It does not re-derive findings, produce
inventory, write specs, or generate code. It checks what is in front of
it and reports.

## When to Use

Trigger on any of these signals:

- A step skill has produced a draft artifact and the runner wants a
  structured review before SME hand-off.
- An SME or reviewer asks "is this ready?" and needs more than a yes/no.
- `legacy-modernization-orchestrator` is about to route downstream and
  needs a compact gate verdict.
- A revision has landed on an artifact previously marked `blocked` and a
  re-check is needed.
- An audit of an existing repo asks: are all our step artifacts still
  green against the current contract?

## When NOT to Use

Do not trigger when:

- The artifact has not been produced yet. Route to the step's owning
  skill.
- The user wants the business artifact itself (inventory / program /
  flow / module / spec / handoff). Route to the dedicated skill.
- The user wants SME judgment on a business question (rule
  intentionality, archive policy, regulatory scope, etc.). Surface the
  question; do not invent an answer.
- The user wants forward SDLC code generation. Use
  `wwa-lab/build-agent-skill`.

The validator is a **checker**. If you find yourself writing new IBM i
facts, business rules, or modernization decisions, you are in the wrong
skill.

## Role

You are the post-execution auditor for one step package. Your job is to:

- detect which step the package belongs to (inventory / program / flow /
  module / spec / handoff) — conservatively, from the package contents
- apply that step's mechanical, semantic, and SME-readiness checks
- categorize each finding into a layer (mechanical / semantic / SME)
  and a severity (blocking / non-blocking)
- emit one `06_quality/step-validation-report.md` plus an optional
  `06_quality/blocking-findings.yaml`
- yield a single compact result: `pass`, `pass_with_warnings`, or
  `blocked`

You must not:

- promote any artifact's `status` field
- approve an inferred business rule
- decide whether a TBD is blocking — that is SME work; you surface it
- invent IBM i facts, fields, jobs, screens, or rules to fill gaps

## Inputs

Accept:

- **Step package path** — directory or file the validator is reviewing.
  Examples: `01_inventory/`, `04_modules/CARD-AUTH/`,
  `05_specs/CREDIT-LIMIT/`, a single `flow-ONUS-AUTH.md`, a single
  `program-analysis-OBJ-CREDIT-CHECK-003.md`.
- **Step type hint** (optional) — when the path is ambiguous, the user
  can declare `inventory | program | flow | module | spec | handoff`.
- **Capability slug / module slug** (optional) — used in IDs minted by
  the report (`STEP-<SLUG>-<NNN>`).
- **SME context** (optional) — if the SME has already reviewed and
  signed off, cite the SME role, date, and IDs approved.

Input readiness scoring:

- `0-5 blocked`: path missing, no recognizable artifact, mixed step types,
  unauthorized production data, or request asks the validator to create the
  artifact rather than review it.
- `6 minimum_pass`: artifact path exists, step type can be identified, and the
  Evidence Authorization Gate can be evaluated.
- `7-8 usable`: step type hint, capability/module slug, and upstream context are
  provided.
- `9-10 strong`: SME context, prior findings, expected downstream consumer, and
  known risk areas are also supplied.
- Missing slug or SME context does not block validation; it may reduce ID
  quality or SME-readiness precision in the report.

Stop and refuse to validate if:

- The path does not exist or contains no recognizable step artifact.
- The artifact mixes two step types (e.g., inventory and module
  contents in one folder) — request scope clarification.
- The artifact contains unauthorized production data (`sensitivity: unknown`,
  missing source-path authorization, or required redaction without approval)
  with raw PII / financial detail — surface an Evidence Authorization Gate
  blocker
  immediately and stop further review.
- The user is asking the validator to produce the step artifact rather
  than check it.

## Output Contract

Produce:

- `06_quality/step-validation-report.md` — required, one per validation
  run.
- `06_quality/blocking-findings.yaml` — optional but recommended when
  status is `pass_with_warnings` or `blocked`; lets downstream automation
  consume findings without parsing prose.

Use:

- `templates/step-validation-report.md` as the report skeleton (this
  skill's template extends the one in
  `../legacy-step-contract/templates/step-validation-report.md` with
  the ten review dimensions below).
- `templates/blocking-findings.yaml` for structured findings.
- `references/validation-checklists.md` for the per-step mechanical
  and semantic check lists.
- `references/finding-taxonomy.md` for the finding severity and
  category model.

Follow:

- `../../docs/evidence-and-knowledge-taxonomy.md` — knowledge type and
  evidence strength rules.
- `../../docs/data-collection-and-redaction.md` — Evidence Authorization Gate
  and governed redaction.
- `../../docs/input-readiness-rubric.md` — input readiness scoring.
- `../../docs/id-conventions.md` — ID prefixes and `STEP-*` /
  `TBD-*` minting.
- `../../docs/skill-review-gate.md` — when the validator is reviewing
  a skill itself; otherwise the skill review gate is out of scope.
- `../../docs/forward-sdlc-contract.md` — Forward Handoff Gate
  conditions.
- `../../templates/skill-review-scorecard.md` — when the validator is
  also producing a skill-level scorecard (rare; usually a separate
  Codex review run).

Examples:

- `examples/pass/` — a complete inventory step with all checks green and
  SME approved.
- `examples/blocked/` — a module step missing one flow approval and one
  evidence-gap TBD; report cites every blocker.

## Workflow

1. **Detect Step Type Conservatively**
   - Inspect the package contents. Match against the directory / file
     fingerprint in `references/validation-checklists.md` (e.g.,
     `inventory.yaml` + `object-map.md` → inventory step;
     `module-overview.md` + four `0N-*.md` views → module step).
   - If two types match, refuse and request clarification.
   - If no type matches, mark the package as unrecognised and stop.

2. **Confirm Evidence Authorization & Sensitivity Safety First**
   - Scan for any `sensitivity: unknown`, unapproved personal / financial
     detail, missing source-path authorization, or missing required redaction
     approval.
   - If any condition fails, status is `blocked` regardless of other
     checks. Emit the report citing the Evidence Authorization Gate and stop.

3. **Run Mechanical Checks**
   - Load the per-step mechanical checklist from
     `references/validation-checklists.md`.
   - For each row, record: pass / fail / not applicable + evidence
     pointer (file + line where possible).
   - If any mechanical row fails as blocking, status will be `blocked`
     unless the user explicitly waives with SME authority; record the
     waiver if applicable.
   - A waiver is valid only when the reviewed artifact or its review file
     records the waived finding ID, SME role/name, date, reason, and the
     specific IDs affected. The validator copies that waiver into
     `06_quality/blocking-findings.yaml`; it does not accept a chat-only
     waiver or invent one.

4. **Run AI Semantic Checks**
   - Read claims against linked evidence. Use the semantic checklist
     for the detected step.
   - Categorize each finding as blocking or non-blocking. Default to
     blocking when uncertain.
   - Cite the specific IDs (`EV-*`, `BEH-*`, `BR-*`, `OBJ-*`, `TBD-*`)
     each finding points to. Avoid prose-only findings.

5. **Map to the Ten Review Dimensions**
   - For each finding, tag one of:
     1. Input readiness
     2. Execution traceability
     3. Output contract completeness
     4. Evidence integrity
     5. Knowledge taxonomy correctness
     6. SME review readiness
     7. Downstream handoff readiness
     8. Open TBD handling
     9. Contradiction / missing evidence detection
     10. Redaction and sensitivity safety
   - A finding can only belong to one dimension. If a finding looks
     like it spans two, split it.

6. **Check SME Review Readiness (not approval)**
   - Confirm an SME owner is named for every claim that needs SME
     approval per `../../docs/evidence-and-knowledge-taxonomy.md`.
   - Confirm the artifact carries a review checklist appropriate to the
     step.
   - Do **not** approve on the SME's behalf. If SME approval is
     recorded in the artifact, cite the SME role, date, and IDs
     approved; otherwise flag SME absence as a finding.

7. **Check Downstream Handoff Readiness**
   - Apply the next-step gate per `references/validation-checklists.md`
     (e.g., for spec writing, the Forward Handoff Gate). Report whether
     the package is ready to advance.

8. **Compose the Compact Result**
   - `pass` if all three layers are clean and SME approval is present
     where required.
   - `pass_with_warnings` if mechanical is clean, all semantic findings
     are non-blocking, and any open TBD has been marked non-blocking
     by SME or is explicitly carried forward.
   - `blocked` otherwise.

9. **Emit Outputs**
   - Write `06_quality/step-validation-report.md` from the template.
   - When status is `pass_with_warnings` or `blocked`, also write
     `06_quality/blocking-findings.yaml` (always emit this file in
     `blocked` runs to give downstream automation a machine-readable
     list).
   - Cite the validator skill version in the report header.

10. **Report to the Orchestrator**
    - When asked by `legacy-modernization-orchestrator` or another
      agent, emit the compact handoff block:

      ```
      status: pass | pass_with_warnings | blocked
      step_id: STEP-<SLUG>-<NNN>
      step_type: inventory | program | flow | module | spec | handoff
      blocking_items: [TBD-..., TBD-...]
      warnings: [TBD-...]
      sme_decision: approved | approved_with_non_blocking_tbd | pending | blocked | not_required
      downstream_next_step: <skill-name | doc-path | none>
      remediation_step: <skill-name | doc-path | none>
      report_path: 06_quality/step-validation-report.md
      findings_path: 06_quality/blocking-findings.yaml | none
      ```

      `downstream_next_step` is populated only when the package may safely
      advance. `remediation_step` is populated only when the package is
      blocked and a prerequisite skill or gate should run before re-validation.

## Review Dimensions

The ten dimensions group findings by **what they reveal**, not by which
layer detected them. A single mechanical check failure and a single
semantic finding can both belong to dimension 4 (Evidence integrity).

| # | Dimension | What it covers |
| --- | --- | --- |
| 1 | Input readiness | Were all prerequisite artifacts, gates, and SME ownership in place when the step started? |
| 2 | Execution traceability | Does the artifact cite the procedure it followed? Are decision points recorded? |
| 3 | Output contract completeness | Are all required files / sections / fields present per the step's output contract? |
| 4 | Evidence integrity | Does every claim link to at least one `EV-*` whose content actually supports it? |
| 5 | Knowledge taxonomy correctness | Are observed behaviour, inferred rules, modernization decisions, and unknown TBDs kept distinct per `docs/evidence-and-knowledge-taxonomy.md`? |
| 6 | SME review readiness | Is the artifact framed so an SME can reject bad output — named owner, scoped questions, traceable IDs? |
| 7 | Downstream handoff readiness | Does the artifact satisfy the gate the next step requires? |
| 8 | Open TBD handling | Is every TBD categorized (`missing_inputs`, `evidence_gaps`, `contradictory_evidence`, `sme_questions`, `downstream_handoff_blockers`) and assigned a resolver? |
| 9 | Contradiction / missing evidence | Are conflicting evidence items explicitly surfaced, with a `DEC-*` recording any SME resolution? |
| 10 | Evidence authorization and sensitivity safety | Does every evidence item have known sensitivity plus source-path authorization or completed required redaction? |

Per-step dimension-to-check mappings live in
`references/validation-checklists.md`.

## Validation Result Enum

The validator emits exactly one status:

| Status | Meaning | When to emit |
| --- | --- | --- |
| `pass` | Mechanical, semantic, and SME-readiness checks are clean. SME approval is recorded where required. | All ten dimensions clear; no blocking finding. |
| `pass_with_warnings` | Mechanical is clean. Semantic findings exist but are non-blocking. Open TBDs are SME-marked non-blocking. | Use sparingly. If you are tempted to call something a warning but it is critical, the status is `blocked`. |
| `blocked` | Any mechanical failure, any blocking semantic finding, any missing-but-required SME approval, or any evidence authorization issue. | Default on uncertainty. The downstream cost of a false `pass` is higher than a false `blocked`. |

The validator never self-promotes a `blocked` package to `pass`. Only
the step's owning skill plus its SME can revise the artifact and
re-submit for validation.

## Finding Taxonomy

Every finding carries:

```yaml
finding_id: FIND-<SLUG>-<NNN>
dimension: 1..10
layer: mechanical | semantic | sme_readiness
severity: blocking | non_blocking
points_to:
  - <artifact path or ID>
resolver: source_owner | sme | architecture | reviewer | runner
recommended_action: <one short sentence>
notes:
```

Severity rules:

- `blocking` → contributes to `blocked` status.
- `non_blocking` → contributes at most to `pass_with_warnings`.

Layer rules:

- `mechanical` findings are reproducible by a script or schema check.
- `semantic` findings require reading the artifact against evidence.
- `sme_readiness` findings indicate the artifact is not yet in a shape
  an SME can review — they are not SME *decisions*.

See `references/finding-taxonomy.md` for the full model.

## Workflow State Write-Back (history only)

This is a governance / verification skill. It does NOT mutate
`capabilities[].stage_id` or `current_focus`. After a validation run,
append one `history[]` entry to `<project-root>/workflow-state.yaml` per
[`docs/workflow-state-contract.md`](../../docs/workflow-state-contract.md).

**Report path pattern:** alongside the validated artifact, e.g.
`02_programs/<MODULE>/<OBJ>/program-analysis.review.md`,
`05_specs/<CAP-*>/spec.review-report.md`

**Per-run write:**

```yaml
history:
  # ... older entries above (never edit)
  - at: <ISO 8601>
    skill: legacy-step-validator
    capability_id: <CAP-* from current_focus, or null>
    stage_after: <the capability's current stage_id — UNCHANGED>
    artifact: <path to the validation report>
    note: "validated <step-id> — result: pass | pass_with_warnings | blocked"
```

Also overwrite `project.last_updated_at` / `project.last_updated_by`.

**Permitted side-effect:** if the validation result is `blocked`, you MAY
append items to `capabilities[<CAP-*>].blocking.tbds` and
`blocking.sme_pending` listing the unresolved findings. You MUST NOT
change `stage_id`, `last_artifact`, or `last_skill` — the Tier 1 skill
that produced the artifact remains its owner.

If `workflow-state.yaml` does not exist, this skill does NOT create it.
Tell the user (in your prose output) to invoke the orchestrator first.

## Anti-Hallucination Rules

- Do not invent IBM i facts. The validator reads what is in front of it
  and cites IDs. It does not mint `OBJ-*`, `BR-*`, `BEH-*`, `DEC-*`.
- Do not approve a `BR-*` or transition a `status` field. Approval is
  the SME's decision; transitions are the owning skill's job.
- Do not collapse layers. Mechanical, semantic, and SME-readiness are
  distinct.
- Do not paper over uncertainty. If a check cannot be performed because
  evidence is missing, that is a finding under dimension 4 or 10, not a
  silent skip.
- Do not promote `blocked` to `pass_with_warnings` to be helpful. If the
  user wants to override, they record a named SME waiver in the
  artifact and re-run the validator.
- Do not treat the Skill Review Gate (`docs/skill-review-gate.md`) as
  this validator's job. That gate scores **skills**; this validator
  scores **step artifacts**.

## Quality Checklist

Before emitting a report, confirm:

- [ ] Step type detected unambiguously
- [ ] Redaction & sensitivity safety verified before any other check
- [ ] All ten review dimensions evaluated
- [ ] Every finding carries dimension, layer, severity, pointers, and
      resolver
- [ ] Status is exactly one of `pass` / `pass_with_warnings` /
      `blocked`
- [ ] Compact handoff block produced for the orchestrator
- [ ] `06_quality/step-validation-report.md` written
- [ ] `06_quality/blocking-findings.yaml` written when status is not
      `pass`
- [ ] No business artifact produced; no SME approval simulated; no
      IBM i facts invented

## Relationship to Other Legacy Spec Factory Skills

- **`legacy-step-contract`** defines the Step Contract. This validator
  applies it. Where step-contract is the rulebook, step-validator is
  the inspector.
- **Step skills** (`legacy-ibmi-inventory`,
  `legacy-ibmi-program-analyzer`, `legacy-ibmi-flow-analyzer`,
  `legacy-ibmi-module-analyzer`, `legacy-spec-writer`) own their own
  output contract; this validator reads those contracts and confirms
  the produced artifact satisfies them.
- **`legacy-modernization-orchestrator`** consumes the validator's
  compact result to decide routing and gate state.
- **Skill review gate** (`docs/skill-review-gate.md`) is a different
  layer: it scores skills, not step artifacts. The validator does not
  replace Codex's skill review run.
- **Forward SDLC handoff** (`docs/forward-sdlc-contract.md`) is the
  next gate after a `pass` on a `spec.yaml`. The validator checks the
  handoff readiness but does not perform the handoff itself.

## Runtime Portability

Canonical source:

```text
skills/legacy-step-validator/SKILL.md
skills/legacy-step-validator/references/validation-checklists.md
skills/legacy-step-validator/references/finding-taxonomy.md
skills/legacy-step-validator/templates/step-validation-report.md
skills/legacy-step-validator/templates/blocking-findings.yaml
skills/legacy-step-validator/examples/pass/
skills/legacy-step-validator/examples/blocked/
```

Runtime copies may be synced to:

```text
.claude/skills/legacy-step-validator/
.opencode/skills/legacy-step-validator/
.agents/skills/legacy-step-validator/
.codex/skills/legacy-step-validator/
```

From the repository root, use `scripts/sync-skills.sh` to create or
check runtime copies. Do not edit adapter copies directly.

No runtime-specific assumptions are baked into this canonical source.

## Version History

- v0.1.1 (2026-05-14): Fixed compact result semantics by splitting
  downstream advancement from remediation (`downstream_next_step`,
  `remediation_step`), aligned blocked example findings, documented SME
  waiver source requirements, and clarified spec-review fallback while
  `legacy-spec-reviewer` is planned. Runtime smoke tests passed in Codex CLI
  (gpt-5.4-mini), Claude Code (haiku), and OpenCode
  (opencode/minimax-m2.5-free).
- v0.1.0 (2026-05-14): Initial release. Validates inventory, program
  analysis, flow, module, spec, and handoff artifacts against the
  Step Contract. Produces `06_quality/step-validation-report.md` and
  optional `06_quality/blocking-findings.yaml`. Emits the compact
  status `pass` / `pass_with_warnings` / `blocked` plus the ten
  review-dimension findings. Portable across Codex, Claude Code, and
  OpenCode.
