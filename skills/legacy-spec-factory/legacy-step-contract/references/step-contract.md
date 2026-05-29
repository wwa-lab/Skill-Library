<!--
Legacy Spec Factory
Copyright 2026 Leo L Zhang

Original author: Leo L Zhang
License: Apache License 2.0
-->

# Step Contract Reference

This document is the field-level specification for the Step Contract used by
every step in the Legacy Spec Factory reverse chain. `SKILL.md` cites this
file; do not duplicate field definitions in `SKILL.md`.

The Step Contract has four sections — INPUT, EXECUTION, OUTPUT, VALIDATION —
plus the Compact Validation Result and the Unresolved Items Ledger.

## Section 1 — INPUT

| Field | Required? | Allowed Values / Shape | Notes |
| --- | --- | --- | --- |
| `step_id` | yes | `STEP-<CAPABILITY-SLUG>-<NNN>` per `docs/id-conventions.md`; `STEP-ROUTING-<NNN>` is allowed only for routing decisions before a capability slug exists | Stable across re-runs of the same step instance |
| `step_name` | yes | short human-readable name | e.g. `Inventory for Credit Check` |
| `skill` | yes | canonical skill name or doc path | One of the skills in this repo, or `docs/forward-sdlc-contract.md` |
| `prerequisite_artifacts` | yes | list of `{path, required_status}` | Status from each upstream artifact's own status enum |
| `prerequisite_gates` | yes | list of gate names | Subset of: Evidence Authorization Gate, Inventory Completeness Gate, Evidence Approval Gate, Forward Handoff Gate |
| `evidence_scope` | yes | list of `EV-*` and `OBJ-*` IDs | Plus authorization summary; must not contain `sensitivity: unknown`, missing source-path authorization, or incomplete required redaction |
| `input_readiness` | yes | `{score, status, minimum_pass_met, hard_blockers, optional_missing, quality_boosters_available, quality_ceiling_reason}` | Uses `docs/input-readiness-rubric.md`; tells the user what blocks, what is enough, and what would improve quality |
| `sme_required` | yes | `yes` / `recommended` / `no` | If `yes`, `sme_owner` must be set |
| `sme_owner` | conditional | role or name | Required when `sme_required = yes` |
| `assumptions_recorded` | optional | bullet list | Any assumption used during execution must appear here; silent assumptions are not allowed |
| `out_of_scope` | recommended | bullet list | Items deliberately excluded so the executing skill does not drift |

### Stop Conditions on INPUT

A step **must not start** if any of the following hold:

- a required prerequisite artifact is missing
- a required prerequisite artifact is below its required status
- a prerequisite gate is `blocked`
- any evidence has `sensitivity: unknown`, lacks source-path authorization, or
  requires redaction without an approval record
- `input_readiness.status = blocked` or `input_readiness.minimum_pass_met`
  is false
- `sme_required = yes` and `sme_owner` is empty
- `evidence_scope` is empty for a step whose output must trace to evidence

When a stop condition is hit, do not partially execute the step. Emit a
`blocked` Step Validation Report instead, listing the unresolved INPUT items
under `missing_inputs` or `evidence_gaps`.

## Section 2 — EXECUTION

| Field | Required? | Allowed Values / Shape | Notes |
| --- | --- | --- | --- |
| `procedure_pointer` | yes | path to skill section or `references/*.md` | The Step Contract cites the procedure; it does not re-state it |
| `inputs_to_outputs_mapping` | yes | list of `{input_field → output_field}` | Lets a reviewer trace each output field back to one or more inputs |
| `tools_allowed` | yes | list | e.g. `read_source`, `read_dds`, `read_db2_metadata`, `read_runtime_evidence`, `call_subskill`, `ask_sme` |
| `tools_forbidden` | yes | list | e.g. `generate_java`, `invent_object_names`, `read_unauthorized_evidence`, `call_external_network` |
| `decision_points` | recommended | list of `{decision, alternatives, recorded_as}` | Where the executing skill must choose, the choice must be recorded explicitly |
| `idempotency` | recommended | `idempotent` / `non_idempotent` / `idempotent_with_caveat` | Affects re-execution behavior |
| `id_minting_policy` | yes | list of allowed ID prefixes for this step | See per-step table below |

### Per-Step ID Minting Policy

These are the ID prefixes each step is allowed to mint. A step that uses a
prefix not in its allowed list must reuse an ID minted upstream rather than
creating a new one.

| Step | Allowed to Mint | Reused From Upstream |
| --- | --- | --- |
| Evidence intake | `EV-*`, `TBD-*`, `STEP-*` | — |
| Inventory | `OBJ-*`, `EV-*`, `TBD-*`, `STEP-*` | — |
| Program analysis | `BEH-*` (program-local), `EX-*` (program-local), `TBD-*`, `STEP-*` | `OBJ-*`, `EV-*` |
| Flow analysis | `FLOW-*`, `NODE-*`, `EDGE-*`, `DATA-*`, `SEED-*`, `TBD-*` | `OBJ-*`, `EV-*`, program-level `BEH-*` |
| Module context intake | `TBD-*` | `RAG-*`, `SNP-*`, `RUN-*`, `DD-*`, `EV-*`, `OBJ-*`, `FLOW-*`, `MODULE-*`, `VIEW-*` |
| Module analysis | `MODULE-*`, `VIEW-*`, `ACTOR-*`, `SYS-*`, `BR-*` (seeds only — promotion happens in spec-writer), `CAP-*` (seeds only), `TBD-*` | `OBJ-*`, `EV-*`, `BEH-*`, `FLOW-*`, `NODE-*`, `EDGE-*`, `DATA-*` |
| Spec writing | `BR-*` (final), `DEC-*`, `STEP-*`, `IN-*`, `OUT-*`, `AC-*`, `TC-*`, `TBD-*` | `OBJ-*`, `EV-*`, `BEH-*`, `FLOW-*`, `NODE-*`, `EDGE-*`, `DATA-*`, `CAP-*` |
| Modernization decision writing (optional) | `DEC-*`, `TBD-*`, `STEP-*` | `CAP-*`, `BR-*`, `BEH-*`, `EV-*`, `OBJ-*`, `FLOW-*`, `AC-*`, existing `DEC-*` |
| Spec review | none — only review status changes | all of the above |
| Forward SDLC handoff | none — handoff is read-only on the spec | all of the above |
| Step validation | `FIND-*`, `TBD-*` (validation report only; owning artifacts must adopt unresolved items before promotion) | all of the above |

### Execution Stop Conditions

The executing skill must stop and surface a TBD (rather than fabricate) when:

- a required source member is unreadable
- evidence is contradictory and no SME is available to resolve
- a downstream ID is referenced but cannot be resolved
- a `tools_forbidden` action would be required to continue

## Section 3 — OUTPUT

| Field | Required? | Allowed Values / Shape | Notes |
| --- | --- | --- | --- |
| `primary_artifacts` | yes | list of `{path, template_or_schema, status_field}` | One row per file the step produces |
| `id_namespaces` | yes | must match `id_minting_policy` from EXECUTION | Mechanical validation checks this |
| `cross_references` | yes | list of required link types | e.g. every `BR-*` links to ≥1 `BEH-*` and ≥1 `EV-*` |
| `status_field` | yes | enum, varies per artifact | See "Artifact Status Enums" below |
| `non_outputs` | recommended | list | Explicitly states what the step must not produce |
| `human_readable_view` | recommended | path | A `.md` view of any structured output, for SME review |

### Artifact Status Enums

Different artifacts use slightly different status fields. The Step Contract
must use the artifact's own enum, not a generic one.

| Artifact | Status Field | Allowed Values |
| --- | --- | --- |
| `inventory.yaml` | `sme_review.decision` | `pending`, `approved`, `approved_with_non_blocking_tbd`, `blocked` |
| `program-analysis.md` | `status` | `draft`, `in_review`, `approved`, `approved_with_non_blocking_tbd`, `blocked` |
| `flow-<SLUG>.md` | `status` | `draft`, `in_review`, `approved`, `approved_with_non_blocking_tbd`, `blocked` |
| `04_modules/<MODULE-SLUG>/` views | `status` | `draft`, `in_review`, `approved`, `approved_with_non_blocking_tbd`, `blocked` |
| `spec.yaml` | `status` | `draft`, `in_review`, `approved`, `rejected`, `retired` |
| `05_decisions/<CAPABILITY-SLUG>/modernization-decisions.yaml` | `status` | `draft`, `in_review`, `approved`, `rejected`, `retired` |
| `review-report.md` | `decision` | `pass`, `pass_with_warnings`, `blocked` (this skill's compact result) |
| Per-claim review | `review_status` | `draft`, `needs_sme_review`, `approved`, `rejected`, `retired` |

### Non-Output Rules

Each step has things it must not produce. Examples:

- Inventory must not infer business rules.
- Program analysis must not write a `spec.yaml`.
- Flow analysis must not promote `BR-*` to `approved` (that is spec-writer +
  SME).
- Module analysis must not produce Java.
- Spec writer must not read raw IBM i source (it consumes upstream
  analyses).
- Spec review must not edit the spec; it produces a review record.

These belong in the `non_outputs` field so reviewers can catch scope creep.

## Section 4 — VALIDATION

Validation has three distinct layers. They are ordered (mechanical first,
SME last), but none substitutes for another.

### 4a — Mechanical Validation Checklist

These checks must be deterministic and reproducible:

| Check | Example |
| --- | --- |
| Required files exist | `inventory.yaml`, `object-map.md`, `inventory-review-checklist.md` are all present |
| Schema validates | `spec.yaml` matches `schemas/spec.schema.yaml` |
| ID prefixes match conventions | No `OBJ-*` in a field that requires `EV-*` |
| No dangling references | Every `evidence_ids` value resolves to a real `EV-*` in `evidence[]` |
| Evidence authorization resolved | No item has `sensitivity: unknown`; every item has `source_path_verified: true` or completed required redaction |
| Input readiness scored and minimum pass met | `input_readiness.score >= 6` and hard blockers are empty before execution |
| Status fields in enum | `review_status` only contains values from the allowed enum |
| Claims have evidence | Every `BEH-*`, `BR-*`, `DEC-*` has ≥1 linked `EV-*` |
| Forbidden tools not used | Step did not call `generate_java`, read unauthorized evidence, etc. |
| ID minting policy respected | A flow analysis did not mint `BR-*` |
| Non-outputs absent | Inventory did not produce `spec.yaml` |

If any mechanical check fails, the overall status is locked to `blocked`
regardless of later layers. The validator may continue with AI semantic and
SME-readiness checks only to collect advisory findings when redaction is safe;
later layers cannot rescue the status.

### 4b — AI Semantic Review Checklist

These checks require reading the artifact against its sources:

| Check | What "good" looks like |
| --- | --- |
| Claims match evidence | Each `BEH-*` statement is supported by the linked `EV-*` content, not just an ID reference |
| Knowledge type matches the claim shape | An "observed" statement is not silently treated as a "rule" |
| Evidence strength not overstated | A rule linked only to `weakly_inferred` evidence does not claim `confirmed_from_code` |
| No invented facts | All object names, fields, jobs, screens, reports appear in the upstream artifacts |
| No scope creep | The artifact does not address a different capability or step |
| TBDs are explicit | Ambiguity surfaces as `TBD-*`, not as smoothed prose |
| Contradictions surfaced | When two evidence items disagree, both are cited and the disagreement is recorded |

Findings from this layer are either **blocking** or **non-blocking**:

- Blocking → status becomes `blocked` (or stays `blocked`).
- Non-blocking → status becomes `pass_with_warnings` (unless SME later
  resolves them).

When in doubt about blocking vs non-blocking, default to blocking. The next
step pays for false negatives.

### 4c — SME / Human Approval Checklist

These checks require a domain expert. The Step Validation Report must record
SME name (or role), date, and the specific IDs approved.

| Check | Required When |
| --- | --- |
| Object coverage approved | Before inventory is marked complete; not required to start developer-led inventory from an approved evidence manifest |
| Inferred business rules approved | Always, before `BR-*` → `approved` in spec-writer |
| Modernization decisions approved | Always, before `DEC-*` → `approved` (architecture/product authority, not just IBM i SME) |
| Behavior intentionality approved | When a `BEH-*` is being promoted into a `BR-*` |
| TBD blocking/non-blocking decision | When a TBD will remain unresolved at handoff |
| Spec promotion to `approved` | Always, transition from `in_review` to `approved` |
| Forward handoff approved | Always, at the Forward Handoff Gate |

SME absence at a step that requires SME is itself a blocker. Record the
absence under `sme_questions` (with an "SME owner not assigned" item), not
under `pass_with_warnings`.

## Compact Validation Result

Every step run must emit one of:

```
status: pass
status: pass_with_warnings
status: blocked
```

Promotion rules:

- `pass` requires all three layers to be clean. If SME is required and
  approved, that approval must be cited.
- `pass_with_warnings` requires mechanical to be clean. Semantic findings
  must be non-blocking, and any open `TBD-*` must be marked non-blocking by
  SME or carried forward explicitly.
- `blocked` covers any mechanical failure, any blocking semantic finding,
  any missing-but-required SME approval, or any unresolved blocker from
  upstream.

A step does not promote its own status past `blocked`. The owning skill plus
its SME do.

## Unresolved Items Ledger

Every Step Validation Report carries a ledger with one row per unresolved
item:

```yaml
unresolved_items:
  - id: TBD-<SLUG>-<NNN>
    category: missing_inputs | evidence_gaps | contradictory_evidence | sme_questions | downstream_handoff_blockers
    points_to: [<artifact path or ID>, ...]
    resolver: source_owner | sme | architecture | reviewer | runner
    blocks_current_step: yes | no
    blocks_next_step: yes | no
    notes:
```

Rules:

- One TBD = one category. Do not place a single TBD in two categories.
- `missing_inputs` resolves by upstream skill / gate.
- `evidence_gaps` resolves by source owner (provide, redact, or formally
  waive).
- `contradictory_evidence` resolves by SME; record the decision as a
  `DEC-*`.
- `sme_questions` resolves by SME judgment; record in artifact review
  section.
- `downstream_handoff_blockers` resolves at the next step's gate; surface it
  early so the next step does not get surprised.

## Worked Step Bindings

The same Step Contract shape applies to every step. Below is a thumbnail of
how the fields bind for each one. See per-skill `SKILL.md` files for the
authoritative procedure.

### Inventory (`legacy-ibmi-inventory`)

- INPUT: approved evidence manifest with source-path authorization or required
  redaction, capability slug, intake reviewer, optional SME owner
- EXECUTION: inventory procedure in the skill's workflow section
- OUTPUT: `01_inventory/inventory.yaml`, `object-map.md`,
  `inventory-review-checklist.md`
- VALIDATION:
  - mechanical: every object has an ID and `evidence_ids`; no
    `sensitivity: unknown`; evidence authorization is complete
  - semantic: object scope matches capability slug; no inferred rules
    sneaking in
  - SME: `sme_review.decision` ∈ `approved`, `approved_with_non_blocking_tbd`

### Program Analysis (`legacy-ibmi-program-analyzer`)

- INPUT: approved inventory + program source + DDS for files it touches
- EXECUTION: program-analyzer workflow
- OUTPUT: `program-analysis.md` per program
- VALIDATION:
  - mechanical: every `BEH-*` and `EX-*` links to `EV-*`; control flow
    references real subroutines
  - semantic: no invented subroutine names; error paths reflect actual code
  - SME: recommended; required if program affects money, inventory,
    compliance, or customer status

### Flow Analysis (`legacy-ibmi-flow-analyzer`)

- INPUT: approved program analyses for every program in the chain; trigger
  context (one of the seven trigger models)
- EXECUTION: flow-analyzer workflow
- OUTPUT: `flow-<FLOW-SLUG>.md`
- VALIDATION:
  - mechanical: every `STEP-*` and cross-program data hop links to `EV-*`
  - semantic: commit boundaries and error propagation match what the
    program analyses say
  - SME: recommended; required if a cross-program rule emerges

### Flow Context Normalization (`legacy-flow-context-normalizer`)

- INPUT: authorized scattered Visio / Word / Excel / PDF / PowerPoint / RAG /
  SME-note documents, module identity, draft scope, and source-document
  authorization metadata
- EXECUTION: normalize scattered documents into the draft four-view context package
  shape defined by
  `skills/legacy-flow-context-normalizer/references/output-contract.md`
- OUTPUT: `00_context_packages/<MODULE-SLUG>/flow-normalization/` with source
  document index, four draft view files, evidence map, contradiction log, open
  questions, and SME review pack
- VALIDATION:
  - mechanical: all ten files present; every view evidence ID appears in the
    evidence map; source-document authorization and readable status are visible
  - semantic: draft document-derived flow steps remain candidates and are not
    promoted to approved `BR-*`; contradictions and obsolete-document signals
    are not hidden
  - SME: SME or accountable owner confirms context-view correctness before the
    package can route to `legacy-module-context-intake`

### Module Context Intake (`legacy-module-context-intake`)

- INPUT: external RAG / code-knowledge-graph output, human-confirmed or draft
  four-view module context, source snippets, dictionary mappings,
  contradictions, retrieval gaps, and evidence authorization metadata
- EXECUTION: normalize module-first context into the package shape defined by
  `skills/legacy-module-context-intake/references/output-contract.md`
- OUTPUT: `00_context_packages/<MODULE-SLUG>/` with context index, four view
  context files, evidence map, contradiction log, and open questions
- VALIDATION:
  - mechanical: all eight files present; every view evidence ID appears in the
    evidence map; contradictions and gaps are carried forward
  - semantic: RAG candidates remain candidates and are not promoted to
    approved `BR-*`; no hidden contradiction or source-authorization gap
  - SME: module owner confirms business name and scope before downstream
    module analysis

### Module Analysis (`legacy-ibmi-module-analyzer`)

- INPUT: approved flow analyses for every flow in the module, BAU notes,
  inventory, or a ready `00_context_packages/<MODULE-SLUG>/` package for
  module-first runs
- EXECUTION: module-analyzer 4-view synthesis per
  `docs/module-analysis-model.md`
- OUTPUT: `04_modules/<MODULE-SLUG>/` with the four views plus overview
- VALIDATION:
  - mechanical: all four views present; capability seeds carry IDs
  - semantic: cross-flow synthesis matches the flow analyses or supplied
    context package; no new IBM i facts that did not exist in upstream inputs
  - SME: required for capability seeds and `BR-*` seeds

### Spec Writing (`legacy-spec-writer`)

- INPUT: approved module + flow + program + inventory; one `CAP-*`; SME
  owner of the capability
- EXECUTION: spec-writer workflow
- OUTPUT: `05_specs/<CAPABILITY-SLUG>/spec.yaml`, `spec.md`,
  `spec-review.md`, `traceability.md`
- VALIDATION:
  - mechanical: `spec.yaml` validates against `schemas/spec.schema.yaml`;
    every `BR-*` links to `BEH-*` and `EV-*`; every approved `BR-*` has at
    least one `AC-*`
  - semantic: no invented Java target; modernization decisions explicitly
    separated from observed legacy behavior
  - SME: required for every `BR-*` reaching `approved` and for transition
    `in_review` → `approved`

### Spec Review (`legacy-spec-reviewer`, planned)

- INPUT: drafted `spec.yaml` + supporting traceability
- EXECUTION: spec-reviewer workflow (planned; until then, use the
  spec-writer review templates with SME)
- OUTPUT: `review-report.md`
- VALIDATION:
  - mechanical: every spec field carries a finding decision (`accept`,
    `revise`, `block`)
  - semantic: findings cite specific IDs, not prose summaries
  - SME: required for sign-off

### Forward SDLC Handoff (`docs/forward-sdlc-contract.md`)

- INPUT: approved `spec.yaml`, `spec.md`, traceability, acceptance criteria
- EXECUTION: handoff is a gate, not a skill — it confirms the contract
- OUTPUT: handoff bundle consumed by `wwa-lab/build-agent-skill`
- VALIDATION:
  - mechanical: `spec.yaml.status = approved`; every approved `BR-*` has
    `AC-*`; no blocking TBD remains; data sensitivity reviewed
  - semantic: modernization decisions explicitly separated from observed
    legacy behavior
  - SME: required for handoff sign-off

## Anti-Patterns

- **Collapsing layers**: writing one big "validation" section that mixes
  mechanical, semantic, and SME. Each layer must be its own list with its
  own resolver.
- **Status laundering**: tagging an artifact `pass_with_warnings` to avoid
  asking the SME. If SME is required, the absence is a blocker.
- **Generic TBDs**: a TBD with no category, no resolver, and no pointer.
  Such items go to nobody and resolve never.
- **Re-describing the procedure**: writing the executing skill's workflow
  inside the Step Contract. The contract cites; it does not re-implement.
- **Inventing IBM i facts**: any object name, field, job, screen, or report
  that does not appear in the upstream artifact is a hallucination, no
  matter how plausible it looks.

## Glossary

- **Step**: one execution of one skill (or gate) on one capability slice.
- **Step Contract block**: the four-section markdown / YAML block that
  captures INPUT, EXECUTION, OUTPUT, VALIDATION for a step.
- **Step Validation Report**: the post-execution report carrying the
  compact validation result plus the unresolved items ledger.
- **Mechanical validation**: deterministic, automatable checks.
- **AI semantic review**: judgment-based reading of artifact against
  upstream evidence.
- **SME approval**: domain-expert decision recorded with role, date, and
  IDs.
- **Compact validation result**: one of `pass`, `pass_with_warnings`,
  `blocked`.
