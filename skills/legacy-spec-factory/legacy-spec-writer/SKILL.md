---
name: legacy-spec-writer
description: "Use when teams need to produce evidence-backed `spec.yaml` and `spec.md` artifacts from approved module + flow + program analyses. One spec per business capability (CAP-*). Layer 2 (platform-agnostic) skill — sits at the boundary between reverse engineering and forward SDLC, producing the contract that `build-agent-skill` consumes. Implements `schemas/spec.schema.yaml`."
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

# Legacy Spec Writer

## Purpose

Synthesize one **business capability spec** from approved upstream
analyses. The output is a structured, evidence-backed `spec.yaml` (plus a
human-readable `spec.md`) that the forward SDLC (`build-agent-skill`)
can consume to generate target-platform code.

This skill is the **first platform-agnostic layer**. It does not look at
IBM i source code directly — only at the analyses produced by
`legacy-ibmi-module-analyzer`, `legacy-ibmi-flow-analyzer`, and
`legacy-ibmi-program-analyzer`.

One capability = one `spec.yaml`. A module typically produces multiple
specs (one per capability identified in the module overview's "Capability
Seeds" section).

## Inputs

Accept:

- **Approved module analysis** (`04_modules/<MODULE-SLUG>/` with all four
  views at `approved` or `approved_with_non_blocking_tbd`)
- **All approved flow analyses** referenced by that module
- **All approved program analyses** referenced by those flows
- **All approved inventory** (`01_inventory/inventory.yaml`)
- **Capability seed** — one specific `CAP-*` from the module overview;
  the SME has confirmed this is a distinct capability worth specifying
- **Target platform hint** (optional) — Java/Spring, Java/Quarkus,
  serverless, etc. Used to inform `target_platform` and `modernization_decisions`
- **SME availability** — capability owner who will approve `business_rules`,
  `acceptance_criteria`, and resolve open `TBD-*`
- **Conditionally required from inventory triggers:**
  - When `inventory.yaml.sme_review.downstream_required.data_model_analyzer.required: true`
    → approved `04_modules/<MODULE-SLUG>/data-model/dictionary.md`.
    `spec.yaml.data_model.entities` MUST be populated by reading this
    dictionary verbatim (entities, fields, types, relationships).
    Do NOT re-derive entities by recomputing across `program-analysis.md`
    File I/O rows — cross-program invariants get lost that way.
  - When `inventory.yaml.sme_review.downstream_required.screen_report_analyzer.required: true`
    → the approved `screen-report-analysis.md` artifacts contribute to
    the UI-driven `behaviors` and `business_rules` of the spec (already
    surfaced via View 1 of the module analyzer, but spec-writer should
    cite them as evidence_ids in the spec's UI-facing rules).

Trigger rules:
[`skills/legacy-ibmi-inventory/references/downstream-triggers.md`](../legacy-ibmi-inventory/references/downstream-triggers.md).

Stop and require clarification if:

- Module status is not `approved` or `approved_with_non_blocking_tbd` →
  route to `legacy-ibmi-module-analyzer`
- The chosen capability seed has unresolved blocking TBDs in the module
  analysis
- No SME owns the capability (without SME, `business_rules` cannot move
  beyond `draft`)
- Target platform is completely unspecified and decisions cannot be
  framed → request platform hint

## Output Contract

Produce a directory `05_specs/<CAPABILITY-SLUG>/`:

```
05_specs/<CAPABILITY-SLUG>/
├── spec.yaml              ← canonical machine-readable contract (schemas/spec.schema.yaml)
├── spec.md                ← human-readable rendering of the same content
├── spec-review.md         ← SME review checklist and sign-off page
└── traceability.md        ← cross-reference report (BR→EV→AC→TC)
```

Use:

- `../../../schemas/legacy-spec-factory/spec.schema.yaml` as the authoritative format
- `templates/spec.yaml`, `templates/spec.md`, `templates/spec-review.md`,
  `templates/traceability.md` as starting structure
- `references/synthesis-rules.md` for how to derive each field
- `references/rule-extraction-protocol.md` for promoting capability seeds
  to approved `BR-*` (the most delicate step)
- `references/anti-hallucination.md` for what the writer must refuse to invent

Follow:

- `../../../docs/legacy-spec-factory/id-conventions.md` for stable IDs (`CAP-*`, `BR-*`, `BEH-*`,
  `DEC-*`, `IN-*`, `OUT-*`, `EX-*`, `STEP-*`, `AC-*`, `TC-*`, `TBD-*`)
- `../../../docs/legacy-spec-factory/evidence-and-knowledge-taxonomy.md` for the
  knowledge-type / evidence-strength model
- `../../../docs/legacy-spec-factory/forward-sdlc-contract.md` for the handoff contract to
  `build-agent-skill`
- `../../../docs/legacy-spec-factory/input-readiness-rubric.md` for input readiness scoring

Examples:

- `examples/spec-positive/` — one approved capability spec (Credit Limit
  Enforcement, derived from CARD-AUTH module)

## Step Contract

This skill is one step in the Legacy Spec Factory reverse chain. It conforms
to the canonical Step Contract shape — see
`../legacy-step-contract/SKILL.md` and
`../legacy-step-contract/references/step-contract.md` for the full
field-level rules. The summary below is normative for this skill.

### Input

- **Required**: approved `04_modules/<MODULE-SLUG>/` (all four views at
  `approved` or `approved_with_non_blocking_tbd`); approved
  `flow-<FLOW-SLUG>.md` for every flow the module references; approved
  `program-analysis-<OBJ-ID>.md` for every program in those flows;
  approved `01_inventory/inventory.yaml`; one `CAP-*` capability seed
  from the module overview; named capability-owner SME.
- **Optional**: target platform hint (Java/Spring, Java/Quarkus,
  serverless, etc.) — informs `target_platform` and
  `modernization_decisions`.
- **Input readiness scoring**:
  - `0-5 blocked`: approved module missing, capability seed unresolved,
    blocking TBDs remain, no capability-owner SME, required triggered artifact
    missing, or evidence authorization unresolved.
  - `6 minimum_pass`: approved module/upstream analyses, one SME-confirmed
    `CAP-*`, named SME owner, and required triggered data/screen/report outputs
    are present.
  - `7-8 usable`: target platform hint, BAU notes, and related BRD/module
    context are supplied.
  - `9-10 strong`: acceptance examples, negative cases, runtime observations,
    platform constraints, and modernization decision context are also supplied.
  - Missing target platform hint does not block observed-behavior/spec drafting
    unless modernization decisions must be framed in the same run.
- **Readiness checks**: Inventory Completeness Gate and Evidence Approval
  Gate passing; no `sensitivity: unknown` evidence in scope; SME owner
  available to approve `BR-*` and `AC-*`.
- **Stop conditions**: module status below `approved_with_non_blocking_tbd`
  (route back to `legacy-ibmi-module-analyzer`); selected `CAP-*` has
  unresolved blocking TBDs in the module; no SME owns the capability;
  target platform completely unspecified when decisions are required.

### Execution

- **Procedure**: see the Workflow section below (11 ordered steps).
- **Allowed inference**: lifting `BEH-*` from flow control flow / branch
  points / error propagation; aggregating evidence from upstream
  artifacts; mapping legacy data objects to target entities; sketching
  modernization decisions whose rationale ties back to `BR-*`, `BEH-*`,
  or platform constraints.
- **Forbidden assumptions**: inventing business rules beyond upstream
  seeds + SME confirmation; promoting a "weak" `BR-*` to `approved`
  without explicit SME approval; generating `AC-*` for unapproved `BR-*`;
  filling data-model field meanings from field names alone; reading raw
  IBM i source (this skill consumes upstream analyses only); specifying
  target architecture without rationale.
- **TBD handling**: unconfirmed business rule → `BR-*` with
  `review_status: needs_sme_review` (no `AC-*` generated); platform
  unspecified → `DEC-*` in `draft` with rationale noting uncertainty;
  unclear field semantics → entity field carries a TBD on semantics.

### Output

- **Canonical directory**: `05_specs/<CAPABILITY-SLUG>/` containing
  `spec.yaml`, `spec.md`, `spec-review.md`, `traceability.md`.
- **Required sections/fields**: `spec_id`, `capability.{id,name,slug,owner}`,
  `scope`, `evidence[]`, `behaviors[]` (`BEH-*`), `business_rules[]`
  (`BR-*`), `modernization_decisions[]` (`DEC-*`), `data_model`,
  `process_flow.steps[]` (`STEP-*`), `inputs[]` (`IN-*`), `outputs[]`
  (`OUT-*`), `exceptions[]` (`EX-*`), `acceptance_criteria[]` (`AC-*`),
  optional `test_cases[]` (`TC-*`), `tbds[]` (`TBD-*`).
- **Required IDs**: mints final `BR-*`, `DEC-*`, `IN-*`, `OUT-*`,
  `STEP-*`, `AC-*`, `TC-*`, `TBD-*`. Reuses `CAP-*`, `OBJ-*`, `EV-*`,
  `BEH-*` from upstream. `spec.yaml` must validate against
  `../../../schemas/legacy-spec-factory/spec.schema.yaml`.
- **Handoff status**: `status: draft` → `in_review` → `approved`
  (capability-owner SME sign-off). Forward Handoff Gate consumes
  `approved`; `rejected` or `retired` halt forward SDLC.

### Validation

- **Mechanical**: `spec.yaml` validates against
  `../../../schemas/legacy-spec-factory/spec.schema.yaml`; every `BEH-*`, `BR-*`, `DEC-*` links
  to ≥1 `EV-*`; every `BR-*` links to ≥1 `BEH-*`; every `approved`
  `BR-*` has ≥1 `AC-*`; every `AC-*` carries `validates: [BR-*]`; every
  TBD has a category and resolver; no `sensitivity: unknown` in `evidence[]`.
- **AI semantic**: each `BR-*` is supported by its linked `BEH-*` and
  `EV-*` content (not just ID reference); `modernization_decisions`
  are explicitly separated from `observed_behavior`; no invented Java
  target details; data-model field semantics never come from field names
  alone; tier 3/4 backing (comments, wikis, prior specs) does not raise
  a `BR-*` past `needs_sme_review`.
- **SME / human approval**: capability-owner SME approves every `BR-*`
  reaching `approved`, every `AC-*`, every `DEC-*` rationale, the data
  model, and the transition `in_review` → `approved`. Modernization
  decisions also need architecture / product authority where target
  platform is concerned.
- **Blocking conditions**: any business-critical `BR-*` unapproved; any
  `approved` `BR-*` missing `AC-*`; any `AC-*` missing
  `validates: [BR-*]`; any `evidence[]` row with `sensitivity: unknown`;
  any blocking TBD; spec arrives at `build-agent-skill` with silent
  gaps.

Emit a Step Validation Report (see
`../legacy-step-contract/templates/step-validation-report.md`) with
status `pass`, `pass_with_warnings`, or `blocked` when reporting upward
to the orchestrator. The Forward Handoff Gate
(`../../../docs/legacy-spec-factory/forward-sdlc-contract.md`) is the next gate after `pass`.

## Workflow

1. **Confirm Capability Scope**
   - Take one `CAP-*` from the module overview's Capability Seeds
   - Validate with SME: is this a distinct capability worth its own spec?
   - Assign `spec_id` and confirm `capability.{id,name,slug,owner}`
   - Define `scope.in_scope` and `scope.out_of_scope` from SME

2. **Collect Evidence Bundle**
   - Gather every `EV-*` referenced by any flow / program analysis that
     touches this capability
   - Populate `evidence[]` array — every `EV-*` becomes one row
   - Confirm `sensitivity` is set; if any `sensitivity: unknown` exists,
     stop and request evidence authorization review

3. **Lift Observed Behaviors (BEH-*)**
   - From flow analyses' control flow + branch points + error propagation
     (factual statements about what the legacy system does)
   - Each BEH must trace to ≥1 EV-*
   - These are *factual* — what the system does, not why

4. **Lift Business Rules (BR-*)**
   - From module analysis's BR-* seeds (View 1) + cross-checked against
     flow analyses' SEED-* + SME confirmation
   - This is the most delicate step — see `references/rule-extraction-protocol.md`
   - Each BR must:
     - Be confirmed by SME (or explicitly marked `needs_sme_review`)
     - Reference ≥1 BEH it abstracts
     - Reference ≥1 EV that supports it
   - **A BR with no SME confirmation cannot be `approved` — only `draft`**

5. **Record Modernization Decisions (DEC-*)**
   - For each significant choice the target system must make (e.g.,
     "store transaction log in append-only table vs event store"),
     record a DEC-*
   - Decisions must have a `rationale` tied to BR or BEH or to
     `target_platform` constraints
   - Decisions are *forward-looking* — they tell `build-agent-skill` how
     to implement, not what the legacy does

6. **Define Data Model**
   - For each target entity, map to legacy `OBJ-*` (the originating PF/LF)
   - For each entity field, map to legacy field name + target type
   - Use the module's View 4 (Data Flow) as primary input
   - Capture lifecycle hints (immutable / mutable / append-only)

7. **Define Process Flow, Inputs, Outputs, Exceptions**
   - `process_flow.steps[]` from the relevant flow analysis Transaction Call Map
   - `inputs[]` from flow analysis Trigger Context + UI surfaces' input fields
   - `outputs[]` from flow analysis exit nodes + Cross-Program Data Flow
     carriers with `external handoff`, `creates`, or `updates` state impact
   - `exceptions[]` from flow analysis Error Propagation + program analyses'
     error handling

8. **Write Acceptance Criteria (AC-*)**
   - For each `approved` BR, produce at least one AC
   - Prefer Gherkin (`given/when/then`) when behavior is procedural
   - Use checklist when behavior is declarative
   - `validates: [BR-*]` is mandatory
   - SME must approve each AC

9. **Optional: Sketch Test Cases (TC-*)**
   - Only if the spec is moving toward field pilot
   - Golden-master and equivalence tests defer to future skills; the spec
     writer may sketch identifiers and intent only

10. **Build Traceability**
    - Generate `traceability.md` with the full chain:
      `BR-* → EV-* → AC-* (→ TC-* if defined)`
    - Verify every approved BR has at least one supporting EV and one AC
    - Verify every AC traces to an approved BR

11. **Prepare for SME Approval**
    - Mark `status: in_review`
    - Capture open `TBD-*` with `blocking` status
    - Generate `spec-review.md` checklist
    - The capability owner SME approves; the spec is then `status: approved`

## Workflow State Write-Back

At the end of a spec-writing run, update
`<project-root>/workflow-state.yaml` per
[`docs/workflow-state-contract.md`](../../../docs/legacy-spec-factory/workflow-state-contract.md).
Template: [`skills/legacy-modernization-orchestrator/references/state-writeback-snippet.md`](../legacy-modernization-orchestrator/references/state-writeback-snippet.md).

**Stage this skill produces (mirrors `spec.yaml.status`):**

- `8c Spec Approved` when `spec.yaml.status: approved` AND every rule has
  `acceptance_criteria` AND no rule with
  `knowledge_type: inferred_business_rule` is at
  `review_status: needs_sme_review` AND no blocking `TBD-*` remains
- `8b Spec In Review` when `spec.yaml.status: in_review`
- `8a Spec Drafted` when `spec.yaml.status: draft`

**Last artifact path pattern:** `05_specs/<CAP-*>/spec.yaml`
(sibling: `spec.md`, `traceability.md`, optional `review-report.md`)

**Writes per run:**

1. Overwrite `capabilities[<CAP-* from current_focus>]` with stage id
   (matching `spec.yaml.status`), `spec.yaml` path, `last_skill:
   legacy-spec-writer`, and blocking IDs (`tbds`, `sme_pending` for any
   `inferred_business_rule` not yet confirmed, `gates: ["evidence_approval"]`
   if any rule still has unlinked evidence).
2. Append one `history[]` entry with `note` summarizing the spec event
   (e.g. `"draft saved"`, `"promoted to in_review"`, `"SME approved"`).
3. Overwrite `project.last_updated_at` / `project.last_updated_by`.

Never touch `current_focus`, other capabilities' entries, or past
`history[]` rows. The `8c → 8b` transition (e.g. SME later rescinds
approval) is a **rollback** — surface to the orchestrator and request the
Rollback Protocol rather than silently lowering `stage_id`.

## Anti-Hallucination Rules

This is the layer where business rules become formal — the temptation to
"smooth out" gaps is highest. The discipline is the strictest.

**Code is ground truth.** See `../../../docs/legacy-spec-factory/code-as-ground-truth.md`. A BR
can only be `approved` when it is grounded in:
- **Tier 1** (currently-deployed source code) — for what the system does, or
- **Tier 2** (named, date-stamped SME confirmation) — for why the system
  does it / what business policy applies

Tier 3 (comments, flow headers, prior specs) and tier 4 (wikis, vendor docs)
are hypotheses, never evidence. If a candidate BR has only tier 3/4 backing,
it stays in `needs_sme_review`. The rule-extraction protocol
(`references/rule-extraction-protocol.md`) enforces this through the
A/B/C/D classification.

**Do NOT:**

- **Invent business rules** beyond what is suggested by upstream BR seeds
  *and* confirmed by SME
- **Promote a "weak" BR to `approved`** without explicit SME approval
- **Generate ACs for unapproved BRs** — every AC must validate an approved BR
- **Include in the spec any fact** that doesn't trace to an EV-* in `evidence[]`
- **Specify target architecture details** that have no rationale tied to BRs,
  BEHs, or platform constraints
- **Fill data-model field meanings** from field names alone (e.g., a field
  called `STATUS` does not imply the spec should say "status is one of
  ACTIVE, INACTIVE, CLOSED" without evidence)
- **Pretend ambiguity is resolved** by picking one interpretation when SME
  hasn't confirmed → mark as TBD

**Instead:**

- If a BR seed seems important but SME hasn't confirmed → BR with
  `review_status: needs_sme_review`, do not generate AC for it
- If `target_platform` is hinted but not committed → DEC entries are
  `draft`; rationale acknowledges uncertainty
- If a field's meaning is unclear → entity field carries a TBD on
  semantics; type is best-effort with `needs_sme_review` evidence

**The contract with `build-agent-skill`:**

- Every `approved` BR has ≥1 AC → testable
- Every `approved` AC has explicit `validates: [BR]` → traceable
- Every `approved` DEC has explicit rationale → reviewable
- Every TBD is explicit → no silent gaps

If a spec arrives at `build-agent-skill` with silent gaps, the modernization
will encode the gaps as defects. The whole skill family exists to prevent
this.

## SME Review Questions

The capability owner SME must validate:

- [ ] Capability name, slug, scope reflect business reality
- [ ] All BR-* are accurate; no invented rules
- [ ] All BEH-* match observed legacy behavior
- [ ] All DEC-* rationale make sense to business + tech
- [ ] Data model fields map correctly to legacy
- [ ] Process flow matches actual legacy sequence
- [ ] Inputs / Outputs / Exceptions are complete
- [ ] Acceptance criteria are testable and meaningful
- [ ] Open TBDs are tracked with named owners
- [ ] No silent gap — spec can be implemented without re-interrogating SME

## Runtime Portability

Canonical: `skills/legacy-spec-writer/SKILL.md`

Synced to all four runtime adapters.

## Version History

- v0.1.0 (2026-05-14): Initial release
  - 11-step workflow producing spec.yaml + spec.md + spec-review.md + traceability.md
  - Strict anti-hallucination at the rule-promotion step
  - Forward-handoff gate with `build-agent-skill`
  - Example: Credit Limit Enforcement capability from CARD-AUTH module
