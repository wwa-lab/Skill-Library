---
name: legacy-brd-writer
description: "Use when teams need to produce evidence-backed Business Requirements Document from approved module analysis, making inferred rules, observed behaviors, and open gaps visible to stakeholders. Business-facing, SME-reviewable artifact positioned between reverse engineering and technical spec-writing. Does not produce acceptance criteria or modernization decisions (legacy-spec-writer's job). Layer 1.5 business-synthesis skill."
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

# Legacy BRD Writer

## Purpose

Synthesize one **Business Requirements Document (BRD)** from an approved module
analysis, making the distinction between observed behaviors, inferred rules, SME
decisions, and open gaps **visible and reviewable** by non-technical stakeholders
before technical spec-writing.

The BRD is a **business synthesis layer**, not a technical specification. It shows:

- What the legacy system **demonstrably does** (`BEH-*`)
- What business rules we **infer from evidence** (`BR-*` seeds from module, status
  `needs_sme_review` or `draft`)
- What questions remain **unresolved** (`TBD-*`)
- **How confident** each claim is, derived from linked evidence records

The BRD consumes module analysis, flow analyses, and program analyses. It does
**not** produce acceptance criteria, modernization decisions, or target-platform
choices — those are the responsibility of `legacy-spec-writer`.

## When to Use

Trigger on any of these signals:

- Module analysis is **approved** or **approved_with_non_blocking_tbd** and
  stakeholders need a **business-readable artifact** for scope review
- SME owner wants to **validate business scope and rules** before forwarding to
  `legacy-spec-writer`
- You are **orchestrating a discovery phase** and need a non-technical bridge
  artifact between reverse engineering and forward SDLC
- Legal, compliance, or product stakeholders need **clear visibility** into what
  rules are observed vs. inferred vs. uncertain

## When NOT to Use

Do not trigger when:

- You are going **directly from module analysis to spec-writing** (spec-writer
  consumes module directly; BRD is optional workflow)
- The output is **code** or **target-platform implementation** (use
  `legacy-spec-writer` then `build-agent-skill`)
- You only need the **technical specification** (`spec.yaml`) (route directly
  to `legacy-spec-writer`)
- No **SME is available** to review and approve the BRD
- The module analysis is **below `approved_with_non_blocking_tbd`** status (route
  back to `legacy-ibmi-module-analyzer`)

This skill is a **business synthesis layer**. If you find yourself writing
acceptance criteria, minting `DEC-*` ids, or specifying target architecture,
you are in the wrong skill. Route to `legacy-spec-writer`.

## Role

You are the **business requirements synthesizer** for one capability.

You must:

- extract observed behaviors (`BEH-*`) from flow and program analyses without
  invention or inference
- aggregate inferred rules (`BR-*` seeds) from the module analysis; keep their
  status as `needs_sme_review` (do not promote to `approved`)
- distinguish **knowledge type** (observed_behavior / inferred_business_rule)
  on every claim, and link each claim to evidence records whose strength is
  recorded in the evidence index per
  `docs/evidence-and-knowledge-taxonomy.md`
- surface unresolved items (`TBD-*`) with category and resolver
- refuse to produce acceptance criteria, modernization decisions, or platform
  choices — those belong in `legacy-spec-writer`
- require SME sign-off before the BRD leaves `in_review` status

You must not:

- invent business rules beyond what the module analysis suggests + SME
  confirmation
- promote a `BR-*` seed to `approved` status in the BRD; SME confirmation is
  recorded as review input, and `legacy-spec-writer` performs the final rule
  promotion in `spec.yaml`
- generate acceptance criteria (spec-writer's job)
- include target platform or modernization decisions
- collapse observed behavior into inferred rules without marking the
  distinction
- treat high-confidence inferences as facts without SME validation

## Inputs

Accept:

- **Approved module analysis** (`04_modules/<MODULE-SLUG>/` with all four views
  at `approved` or `approved_with_non_blocking_tbd`)
- **One or more capability seeds** — selected from the module overview's
  Capability Seeds; the SME has confirmed each is a distinct, in-scope business
  capability
- **Capability-owner SME** (required for sign-off)
- **Optional:** BAU notes or additional context from the SME

Stop and require clarification if:

- Module status is below `approved_with_non_blocking_tbd` → route back to
  `legacy-ibmi-module-analyzer`
- The selected capability seed has **blocking TBDs** in the module analysis →
  escalate to SME for resolution before proceeding
- No **SME owner is assigned** → stop; cannot proceed to review without SME
- The capability **boundary is ambiguous** (does flow X belong here or to another
  capability?) → SME must decide

## Output Contract

Produce a directory `05_brds/<CAPABILITY-SLUG>/`:

```
05_brds/<CAPABILITY-SLUG>/
├── brd.md                    ← canonical business requirements document
├── brd-review.md            ← SME review checklist and sign-off page
└── traceability.md          ← cross-reference report (BRD req → EV/BEH/TBD)
```

Use:

- `templates/brd.md`, `templates/brd-review.md`, `templates/traceability.md` as
  starting structure
- `references/synthesis-rules.md` for how to extract behaviors and aggregate
  rules
- `references/anti-hallucination.md` for what the BRD must refuse to invent

Follow:

- `../../../docs/legacy-spec-factory/id-conventions.md` for stable IDs (`CAP-*`, `BEH-*`, `BR-*`,
  `TBD-*`, etc.)
- `../../../docs/legacy-spec-factory/evidence-and-knowledge-taxonomy.md` for knowledge-type /
  evidence-strength distinction
  - Use only these evidence strength values in evidence records:
    `confirmed_from_code`, `observed_in_runtime`, `confirmed_by_sme`,
    `strongly_inferred`, `weakly_inferred`, `needs_sme_review`,
    `contradictory`, `missing`
- `../../../docs/legacy-spec-factory/data-collection-and-redaction.md` for evidence sensitivity
  checks
- `../../../docs/legacy-spec-factory/input-readiness-rubric.md` for input readiness scoring

Examples:

- `examples/brd-positive/` — one approved BRD (Credit Limit Enforcement from
  CARD-AUTH module)
- `examples/incomplete-input-negative/` — BRD with non-blocking TBDs (awaiting
  SME decision on open questions)

## Step Contract

This skill is one step in the Legacy Spec Factory reverse chain. It conforms to
the canonical Step Contract shape — see
`../legacy-step-contract/SKILL.md` and
`../legacy-step-contract/references/step-contract.md` for full field-level rules.
The summary below is normative for this skill.

### Input

- **Required**: approved `04_modules/<MODULE-SLUG>/` (all four views at
  `approved` or `approved_with_non_blocking_tbd`); one or more `CAP-*`
  capability seeds from the module overview, validated by SME; named
  capability-owner SME; all referenced `flow-<FLOW-SLUG>.md` and
  `program-analysis-<OBJ-ID>.md` at `approved` or
  `approved_with_non_blocking_tbd`; approved `01_inventory/inventory.yaml`.
- **Optional**: BAU notes, supplemental context.
- **Input readiness scoring**:
  - `0-5 blocked`: approved module missing, selected `CAP-*` unresolved,
    blocking TBDs remain, capability boundary ambiguous, no SME owner, or
    evidence authorization unresolved.
  - `6 minimum_pass`: approved module, selected SME-confirmed capability seed,
    named capability-owner SME, and approved upstream analyses are present.
  - `7-8 usable`: BAU notes, supplemental SME context, and related open-TBD
    history are supplied.
  - `9-10 strong`: examples of real scenarios, exception cases, runtime
    observations, policy notes, and downstream reader context are also supplied.
  - Missing supplemental context does not block BRD drafting; it should produce
    clearer SME questions instead of invented rules.
- **Readiness checks**: module and all upstream analyses at required status; no
  `sensitivity: unknown` evidence in scope; SME owner available to approve BRD.
- **Stop conditions**: module below `approved_with_non_blocking_tbd` (route back
  to `legacy-ibmi-module-analyzer`); capability seed has blocking TBDs (escalate
  to SME); no SME owner assigned; capability boundary ambiguous.

### Execution

- **Procedure**: see the Workflow section below (7 ordered steps).
- **Allowed inference**: lifting `BEH-*` from flow control flow, program branch
  points, and error handling (factual statements about what the legacy system
  does); aggregating `BR-*` seeds from module overview and cross-checking
  against program/flow context; computing confidence levels based on evidence
  strength; surfacing contradictions as TBDs.
- **Forbidden assumptions**: inventing business rules beyond module BR-* seeds +
  SME confirmation; promoting a BR-* seed to `approved` status (only
  `legacy-spec-writer` may do that); generating acceptance criteria;
  specifying target platform or modernization decisions; reading raw IBM i
  source code (consume upstream analyses only); treating weak inferences as
  facts.
- **TBD handling**: unconfirmed rule → `BR-*` seed with `status: needs_sme_review`
  (marked in BRD); contradictory evidence → `TBD-*` with `category:
  contradictory_evidence` and resolver; missing context → `TBD-*` with
  `category: sme_questions` or `category: evidence_gaps`.

### Output

- **Canonical directory**: `05_brds/<CAPABILITY-SLUG>/` containing `brd.md`,
  `brd-review.md`, `traceability.md`.
- **Required sections/fields** (see `templates/brd.md`): capability overview,
  scope statement, observed behaviors, inferred business rules (with status),
  open questions (TBDs), evidence index.
- **Required IDs**: mints `BRD-*` for the document and `TBD-*` for open
  questions. Reuses `CAP-*`, `OBJ-*`, `EV-*`, `BEH-*`, `BR-*` seeds,
  `MODULE-*`, `FLOW-*` from upstream. If a new candidate rule appears during
  BRD review and has no upstream `BR-*`, record it as a `TBD-*` requiring
  module/spec review instead of minting a new `BR-*` here. Does NOT mint
  `DEC-*`, `AC-*`, `IN-*`, `OUT-*`, `STEP-*`, `TC-*`, or new `BR-*`.
- **Handoff status**: `status: draft` → `in_review` → `approved` (SME sign-off).
  `legacy-spec-writer` may consume `approved` BRD; spec-writer can also consume
  module analysis directly (BRD is optional artifact in the workflow).

### Validation

Validation has three distinct layers, in order. None substitutes for another.

#### 4a. Mechanical Validation

What can be checked by a script, schema, or deterministic linter:

- required files exist at expected paths
- all referenced IDs resolve (no dangling `EV-*`, `BEH-*`, `BR-*`, `CAP-*`,
  `TBD-*`)
- ID prefixes match `docs/id-conventions.md`
- every claim has at least one linked evidence item (`EV-*` or `BEH-*`)
- no `sensitivity: unknown` in evidence references
- traceability table is complete and consistent (all claims appear in
  `traceability.md`)
- BRD does not include acceptance criteria, modernization decisions, or target
  platform details

Mechanical validation **must** be reproducible. If it depends on judgment, move
it to AI semantic review.

#### 4b. AI Semantic Review

What an LLM (or careful reviewer) can check by reading the artifact against
upstream evidence:

- observed behaviors (`BEH-*`) are factual statements about what the code / data /
  logs show, not inferences
- inferred business rules (`BR-*` seeds) are supported by `BEH-*` and linked
  `EV-*` content (not just ID reference)
- knowledge type (observed_behavior / inferred_business_rule) is correctly
  marked for every claim
- evidence support is not overstated (no weak evidence record used as if it
  were direct code/runtime/SME confirmation)
- no invented IBM i facts (object names, fields, programs, jobs)
- no scope creep into other capabilities
- no acceptance criteria or platform decisions hidden in prose
- TBDs are explicit, not hidden inside prose

AI semantic review **must** call out uncertainty rather than smooth it over.

#### 4c. SME / Human Approval

What only a domain expert can decide:

- are the observed behaviors accurate to legacy system reality?
- are the inferred rules actually business rules, or are they implementation
  artifacts?
- is the capability scope and boundary correct?
- are there unspoken business rules the code doesn't show?
- are TBDs blocking or non-blocking for the next step (spec-writer)?
- is the BRD safe to promote to `approved` and forward to spec-writer?

SME approval is a **control point**, not a rubber stamp. The Step Validation
Report must record the SME's name (or role), the date, and the specific
decision.

## Workflow

1. **Confirm Capability Scope**
   - Take one or more `CAP-*` seeds from the module overview's Capability Seeds
   - Validate with SME: is each a distinct capability worth its own BRD?
   - Assign `brd_id` and confirm `capability.{id, name, slug, owner}`
   - Define `scope.in_scope` and `scope.out_of_scope` from SME

2. **Collect Evidence Bundle**
   - Gather every `EV-*` referenced by flows / programs / module that touch this
     capability
   - Populate evidence index with source, type, sensitivity, and confidence
   - Confirm `sensitive` flag is set on all evidence; if any `sensitive:
     unknown`, stop and request redaction review

3. **Lift Observed Behaviors (BEH-*)**
   - From flow analyses' control flow points, branch conditions, error handlers
     (factual statements about legacy system behavior)
   - Each BEH must trace to ≥1 `EV-*`
   - These are *factual* — what the system does, not why or whether it's correct

4. **Aggregate Business Rules (BR-*)**
   - From module analysis's `BR-*` seeds (View 1 / Capability Seeds)
   - Cross-check against flow / program analyses
   - Keep each BR-* at status `needs_sme_review` (do NOT promote to `approved`);
     that is spec-writer's job
   - Reuse upstream `BR-*` seeds only. If BRD review reveals a candidate rule
     with no upstream `BR-*`, record a `TBD-*` for module/spec review instead
     of minting a new `BR-*`
   - Each BR must:
     - Reference ≥1 `BEH-*` it abstracts
     - Reference ≥1 `EV-*` that supports it
     - Be marked `knowledge_type: inferred_business_rule`

5. **Surface Open Questions (TBD-*)**
   - Contradictory evidence → `TBD-*` with category `contradictory_evidence`
   - Missing context → `TBD-*` with category `sme_questions`
   - Ambiguous scope → `TBD-*` with category `sme_questions`
   - Each TBD must name a resolver and indicate whether it blocks spec-writing

6. **Build Traceability**
   - Generate `traceability.md` cross-reference table
   - Every BEH-* and BR-* must have ≥1 supporting EV-*
   - Every TBD must be listed with category and resolver
   - Verify complete coverage (no claim is missing from the table)

7. **Prepare for SME Approval**
   - Mark `status: in_review`
   - Generate `brd-review.md` checklist
   - Capability owner SME approves the BRD; BRD is then `status: approved`
   - Keep `BR-*` review status as `needs_sme_review` in the BRD even when SME
     notes confirm it for later spec promotion
   - If SME finds issues, mark `status: blocked` with specific findings

## Workflow State Write-Back (history only — supplemental)

This is a supplemental Layer 1.5 skill. It produces a business-facing BRD
between module analysis and spec writing, but does NOT advance the linear
`stage_id` (BRD is parallel to the technical spec, not a stage on its
path). It does NOT mutate `current_focus`.

After a run, append one `history[]` entry to
`<project-root>/workflow-state.yaml` per
[`docs/workflow-state-contract.md`](../../../docs/legacy-spec-factory/workflow-state-contract.md):

```yaml
history:
  - at: <ISO 8601>
    skill: legacy-brd-writer
    capability_id: <CAP-* from current_focus>
    stage_after: <UNCHANGED stage_id>
    artifact: <path to brd.md, e.g. 08_business-understanding/<CAP-*>/brd.md>
    note: "BRD authored for <CAP-*> — status: draft | in_review | approved"
```

Also overwrite `project.last_updated_at` / `project.last_updated_by`.

**Permitted side-effect:** if BRD authoring surfaces inferred business
rules or open gaps not already in `capabilities[<CAP-*>].blocking.*`, you
MAY append them to `blocking.sme_pending` (rule IDs) or `blocking.tbds`.
You MUST NOT change `stage_id`, `last_artifact`, or `last_skill` — the
linear stage owner remains `legacy-ibmi-module-analyzer` or
`legacy-spec-writer`.

If `workflow-state.yaml` does not exist, this skill does NOT create it.

## Anti-Hallucination Rules

The BRD is the first **business-facing** artifact. The temptation to "smooth out"
gaps or invent business logic is high. Discipline is essential.

**Observed behavior is ground truth.** A BEH can only be claimed when it is
grounded in:

- **Tier 1** (upstream flow / program analysis) — for what the system does, or
- **Tier 2** (named, date-stamped SME confirmation) — for context the code
  doesn't show (manual procedures, business policy)

**Do NOT:**

- **Invent business rules** beyond what module BR-* seeds suggest + SME
  confirmation
- **Promote a BR-* seed to `approved`** (only `legacy-spec-writer` may do that)
- **Generate acceptance criteria** (spec-writer's job)
- **Include target platform or modernization decisions** (spec-writer's job)
- **Claim behavior from field names or comments alone** (factual evidence
  required)
- **Pretend ambiguity is resolved** by picking one interpretation when SME
  hasn't confirmed → mark as TBD instead
- **Include any fact** that doesn't trace to an `EV-*` in the evidence index

**Instead:**

- If a BR seed is plausible but SME hasn't confirmed → keep it at
  `needs_sme_review`, do not hide uncertainty
- If evidence is contradictory → create a `TBD-*`, mark the category, and name
  a resolver
- If a field's meaning is unclear → create a `TBD-*` on semantics; do not guess
- If scope is contested → create a `TBD-*` on boundary; let SME decide

## Quality Checklist

Before marking the BRD `approved`, confirm:

- [ ] All three files exist at correct paths (`brd.md`, `brd-review.md`,
      `traceability.md`)
- [ ] Every claim in `brd.md` appears in `traceability.md`
- [ ] Every `BEH-*` and `BR-*` links to ≥1 `EV-*`
- [ ] No invented IBM i facts; all object names come from upstream artifacts
- [ ] Knowledge type (observed_behavior / inferred_business_rule) is marked for
      every claim
- [ ] `BR-*` seeds carry `status: needs_sme_review` (not promoted to `approved`)
- [ ] No acceptance criteria, modernization decisions, or platform details in
      BRD
- [ ] All `TBD-*` items carry a category (missing_inputs, evidence_gaps,
      contradictory_evidence, sme_questions, downstream_handoff_blockers)
- [ ] SME has reviewed and approved the BRD
- [ ] Capability scope and boundaries are validated by SME

## Relationship to Other Skills

- **`legacy-ibmi-module-analyzer`** (upstream): produces module analysis with
  BR-* seeds and capability seeds. BRD consumes this output.
- **`legacy-spec-writer`** (downstream): consumes module analysis directly OR
  module + approved BRD. If BRD is provided, spec-writer uses it as the
  business context layer for rule promotion. BRD is an optional artifact in
  the workflow.
- **`legacy-step-contract`** (parallel): defines the Step Contract shape that
  this skill conforms to.
- **`legacy-modernization-orchestrator`** (meta): may route to BRD-writer as an
  optional business review gate before spec-writing.

## Runtime Portability

The canonical skill source lives under:

```
skills/legacy-brd-writer/SKILL.md
skills/legacy-brd-writer/templates/
skills/legacy-brd-writer/references/
skills/legacy-brd-writer/examples/
```

Runtime copies may be synced to:

```
.claude/skills/legacy-brd-writer/
.opencode/skills/legacy-brd-writer/
.agents/skills/legacy-brd-writer/
.codex/skills/legacy-brd-writer/
```

From the repository root, use `scripts/sync-skills.sh` to create or check
runtime copies. Do not edit adapter copies directly.

No runtime-specific assumptions are baked into this canonical source.

## Version History

- v0.1.1 (2026-05-16): Runtime smoke test hardening
  - Clarified BRD writer reuses upstream `BR-*` seeds only; new candidate
    rules become `TBD-*` for module/spec review
  - Normalized ambiguous-scope TBDs to `sme_questions`
  - Pinned the allowed evidence-strength enum in the core instructions
  - Passed smoke tests in Codex CLI (gpt-5.4-mini), Claude Code (haiku), and
    OpenCode (minimax-m2.5-free)

- v0.1.0 (2026-05-15): Initial BRD Writer skill
  - 7-step workflow producing brd.md + brd-review.md + traceability.md
  - Strict anti-hallucination at the business rule synthesis step
  - Clear role separation from spec-writer (BRD = business layer, spec =
    technical layer)
  - Optional artifact in the workflow (module → spec is the direct path)
  - Portable across Codex, Claude Code, and OpenCode (awaiting runtime
    smoke-test validation)
