---
name: legacy-modernization-decision-writer
description: "Use when teams need to produce, expand, review, and validate modernization decision records (DEC-*) when decisions become too large or risky to keep only inside spec-writer. Optional Governance / BRD skill for structured decision packages. Bridges between approved BRD/spec and target-platform authority approval. Does not recreate Atlas SDD architecture/design artifacts."
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

# Legacy Modernization Decision Writer

## Purpose

Produce, expand, review, and validate **modernization decision records** (`DEC-*`)
when decisions become too large, high-risk, or cross-cutting to handle inside
`legacy-spec-writer` alone.

This is an **optional governance skill** positioned around spec review, before
forward SDLC handoff. It:

- **Does not fork the source of truth**: `spec.yaml`'s `modernization_decisions[]`
  remains the authoritative list
- **Produces structured decision packages** for complex capabilities that need
  explicit architecture/product approval before external forward SDLC work
- **Expands and reviews** existing draft/in-review `DEC-*` records with full
  context, evidence links, and alternatives
- **Validates** that decisions are grounded in approved BRs/BEHs or explicit
  target-platform constraints
- **Surfaces unresolved choices** as `TBD-*` rather than fake-approving them

The skill separates:

- **Observed legacy behavior** (`BEH-*`)
- **Inferred business rules** (`BR-*`)
- **Modernization decisions** (`DEC-*` — target-system architectural choices)

Each has distinct evidence, approval authority, and impact scope.

## When to Use This Skill

Trigger on any of these signals:

- A capability has **many `DEC-*` records** (3+) or decisions are **cross-cutting**
  across multiple capabilities
- Modernization decisions are **high-risk** or require **explicit
  architecture/product approval** (not just SME sign-off on legacy behavior)
- `spec.yaml` is **draft, in review, or approved with deferred decisions** and contains
  **unresolved platform, data, API, async, compatibility, audit, or error-handling
  choices** that need a structured decision package
- A BRD/spec review identifies **gaps in decision rationale** requiring evidence
  traceability and alternative analysis
- Target platform constraints exist but **decision ownership** is unclear
  (IBM i SME ≠ target architecture authority)
- You need **decision-record governance** before forwarding to the forward SDLC
  agent

## When NOT to Use This Skill

Do not trigger when:

- A **simple `modernization_decisions[]` entry** inside `legacy-spec-writer` is
  sufficient (most capabilities)
- You want **implementation architecture/design artifacts** (Atlas SDD skills own
  `spec-to-architecture`, `architecture-to-design`, implementation planning)
- You are generating **business rules, acceptance criteria, or target code**
  (spec-writer + forward SDLC own those)
- **Required evidence, approved BRs, or decision authorities are missing** →
  first complete the upstream capability spec
- Decision authority is **unclear** — if no product/architecture owner can sign
  off, decisions cannot move to `approved`

This skill is a **decision governance and expansion layer**. If you need target
code, route to `legacy-spec-writer` then forward SDLC. If you need implementation
architecture diagrams, route to Atlas SDD skills.

## Input Contract

Accept:

- **Draft, in-review, or approved `spec.yaml`** for one capability (from
  `legacy-spec-writer`). Draft/in-review specs are valid when modernization
  decisions are the reason the spec cannot yet be approved.
- **Approved module/flow/program analyses** as evidence for decision rationale
- **Existing draft or `needs_sme_review` `DEC-*` records** from spec or
  `05_decisions/` folder
- **Existing `BR-*`, `BEH-*`, `EV-*`, `TBD-*`** to establish rationale links
- **Target platform constraints** (explicit, not vague — e.g., "Java 21 + Spring
  Boot 3.2 on AWS ECS" not "cloud-based")
- **Named decision authorities**:
  - IBM i / business SME (for legacy behavior preservation and BRs)
  - Architecture / product owner (for target platform decisions)

Input readiness scoring:

- `0-5 blocked`: spec missing, rationale IDs unresolved, no SME for legacy
  behavior, no architecture/product authority for target choices, unresolved
  blocking TBDs, or evidence authorization unresolved.
- `6 minimum_pass`: draft/in-review/approved spec, grounded BR/BEH/EV/TBD
  records, and named decision authorities are present.
- `7-8 usable`: approved module/flow/program analyses, explicit platform
  constraints, and existing DEC drafts are supplied.
- `9-10 strong`: tradeoff notes, non-functional constraints, operational
  constraints, incident history, and downstream architecture context are also
  supplied.
- Missing existing DEC drafts does not block; vague platform constraints lower
  decision quality and may keep DEC records in `draft`.

Stop and require clarification if:

- The capability spec is missing or does not contain the BR/BEH/EV records
  needed to ground the requested decision → route to `legacy-spec-writer`
- No **SME owns the legacy behavior** understanding → cannot ground decisions
  in evidence
- No **architecture/product owner** for target choices → cannot approve `DEC-*`
  beyond `draft`
- Decisions reference **unresolved `TBD-*`** without resolution path → escalate
  TBD first
- **Evidence linking is circular** (DEC references non-existent BR/BEH/EV) →
  request spec repair

## Output Contract

Produce a directory `05_decisions/<CAPABILITY-SLUG>/`:

```text
05_decisions/<CAPABILITY-SLUG>/
├── modernization-decisions.yaml        ← consolidated DEC records + metadata
├── decisions/
│   ├── DEC-<CAP-SLUG>-001.md
│   ├── DEC-<CAP-SLUG>-002.md
│   └── DEC-<CAP-SLUG>-NNN.md
├── decision-review.md                   ← governance review checklist & sign-offs
└── traceability.md                      ← DEC→BR/BEH/EV cross-reference matrix
```

Each `DEC-*` record includes:

- **id**: `DEC-<CAPABILITY-SLUG>-<NNN>` (stable, three-digit)
- **knowledge_type**: `modernization_decision` (constant)
- **category**: one of `architecture`, `data`, `api_surface`, `error_handling`,
  `async_boundary`, `compatibility`, `audit`, `security`, `observability`
- **decision**: concise target-system choice (e.g., "Use Spring Boot REST API for
  inventory sync")
- **context**: business reason + legacy scenario that prompted the decision
- **alternatives_considered**: ≥2 paths evaluated (including "do nothing" /
  "preserve legacy")
- **chosen_option**: which alternative, and why
- **rejected_options**: why others were dismissed
- **rationale**: evidence-backed explanation grounded in BR/BEH or explicit
  target constraint
- **linked_rules**: IDs of BRs/BEHs that the decision serves or affects
- **target_platform_constraints**: explicit platform facts the decision respects
  when the decision chooses a target technology, topology, protocol, or runtime
- **implementation_impact**: effort, dependencies, risk
- **compatibility_impact**: effects on other capabilities, backwards compatibility
- **risks_and_mitigations**: unresolved items and mitigation plans
- **review_status**: `draft | needs_sme_review | approved | rejected |
  retired`
- **pending_approvals**: roles still required before approval, especially
  architecture/product authority
- **approvals**: structured sign-offs by role/person/date

Use:

- `templates/modernization-decisions.yaml` as the root structure
- `templates/decision-record.md` for each DEC markdown expansion
- `templates/decision-review.md` for governance sign-offs
- `templates/traceability.md` for BR/BEH/EV mapping
- `references/decision-rules.md` for synthesis guidance
- `references/anti-hallucination.md` for invention boundaries

Follow:

- `../../../docs/legacy-spec-factory/id-conventions.md` for stable IDs
- `../../../docs/legacy-spec-factory/evidence-and-knowledge-taxonomy.md` for knowledge types and
  evidence strength
- `../../../docs/legacy-spec-factory/forward-sdlc-contract.md` for handoff compatibility

## Position In Chain

This skill is **optional** within the Layer 2 synthesis chain:

```text
[Layer 1 — IBM i Extraction]
   legacy-ibmi-inventory
        ↓
   legacy-ibmi-program-analyzer
        ↓
   legacy-ibmi-flow-analyzer
        ↓
   legacy-ibmi-module-analyzer
        ↓
[Layer 2 — Platform-Agnostic Synthesis]
   legacy-spec-writer
        ├─→ spec.yaml (with draft/in-review DEC records)
        │
        └─→ [OPTIONAL] legacy-modernization-decision-writer
              ├─→ expanded DEC package (05_decisions/)
              └─→ reconcile back to spec.yaml
        │
   [SME + ARCH APPROVAL GATE]
        │
   legacy-equivalence-test-generator
        ↓ (planned)
   [FORWARD HANDOFF GATE]
        ↓
External forward SDLC chain (outside this repository)
```

After decision package is approved, `legacy-spec-writer` may incorporate the
approved `DEC-*` records back into the canonical, schema-compliant
`spec.yaml.modernization_decisions[]` before forward handoff. The detailed
approval notes remain in `05_decisions/<CAPABILITY-SLUG>/`.

## Step Contract

This skill conforms to the Legacy Spec Factory Step Contract shape. See
`../legacy-step-contract/SKILL.md` and
`../legacy-step-contract/references/step-contract.md` for full field-level
rules.

### Input

- **Required**: one capability-level `05_specs/<CAPABILITY-SLUG>/spec.yaml`
  at `draft`, `in_review`, or `approved`; existing `CAP-*`, `BR-*`, `BEH-*`,
  `EV-*`, and relevant `TBD-*` records; named IBM i / business SME; named
  architecture or product decision authority for every target-system choice.
- **Optional**: approved BRD, approved module/flow/program analyses, target
  platform constraints, existing `05_decisions/<CAPABILITY-SLUG>/` package.
- **Input readiness scoring**: apply
  `../../../docs/legacy-spec-factory/input-readiness-rubric.md`; platform context and existing DEC
  drafts are quality boosters unless a target-system choice is being approved.
- **Readiness checks**: no `sensitivity: unknown` evidence; referenced IDs resolve;
  every decision candidate has at least one linked BR or BEH and at least one
  linked EV or explicit target-platform constraint; decision authorities are
  named before any `DEC-*` can be approved.
- **Stop conditions**: missing/invalid spec; dangling BR/BEH/EV/TBD references;
  evidence with unknown sensitivity; no SME owner; no architecture/product
  authority for a target-system choice; unresolved blocking TBD with no owner.

### Execution

- **Procedure**: use the Workflow below and `references/decision-rules.md`.
- **Allowed inference**: expanding a draft DEC into context, alternatives,
  impact, risks, and approval needs; linking decisions to existing BR/BEH/EV/TBD
  records; identifying missing authority or evidence as `TBD-*`.
- **Forbidden assumptions**: minting new BRs or ACs; inventing technologies,
  cache TTLs, retry policies, deployment topology, API shapes, or implementation
  tasks; approving a decision without SME plus architecture/product authority;
  treating a legacy behavior as a target decision without explicit rationale.
- **ID minting policy**: may mint `DEC-*`, `TBD-*`, and `STEP-*`. Must reuse
  upstream `CAP-*`, `BR-*`, `BEH-*`, `EV-*`, `OBJ-*`, `FLOW-*`, `AC-*`, and
  related IDs. Must not mint `BR-*`, `AC-*`, `IN-*`, `OUT-*`, `TC-*`, or
  implementation task IDs.

### Output

- **Canonical directory**: `05_decisions/<CAPABILITY-SLUG>/` containing
  `modernization-decisions.yaml`, `decisions/DEC-<CAP-SLUG>-NNN.md`,
  `decision-review.md`, and `traceability.md`.
- **Status fields**: package `status` uses `draft | in_review | approved |
  rejected | retired`; per-DEC `review_status` uses `draft |
  needs_sme_review | approved | rejected | retired`.
- **Non-outputs**: no implementation architecture document, design document,
  task breakdown, code, test cases, or acceptance criteria.
- **Reconciliation**: approved decisions must be copied back into
  `spec.yaml.modernization_decisions[]` using fields allowed by
  `../../../schemas/legacy-spec-factory/spec.schema.yaml`; detailed alternatives and approvals remain
  in the decision package.

### Validation

- **Mechanical**: required files exist; every ID follows
  `../../../docs/legacy-spec-factory/id-conventions.md`; no `DECPKG-*` or unregistered status values;
  no dangling references; no linked evidence has `sensitivity: unknown`; no AC,
  TC, implementation task, or code artifact is minted.
- **AI semantic**: DEC records are clearly separated from observed behavior and
  inferred business rules; rationale is grounded in linked BR/BEH/EV or explicit
  target constraints; alternatives are real; unresolved uncertainty is a
  structured `TBD-*`.
- **Human approval**: `approved` DEC records require IBM i / business SME review
  for legacy fidelity and architecture/product review for target-system fit.

## Role

You are the **decision architect and governance specialist** for one capability's
modernization choices.

You must:

- **Separate observed legacy from modernization decisions**: never confuse what
  the legacy system *does* with what the target system *should do*
- **Ground decisions in evidence**: every DEC rationale must reference at least
  one existing BR or BEH and at least one EV; target-platform constraints are
  required whenever the decision chooses a target technology, topology, protocol,
  or runtime
- **Require competing alternatives**: every decision must articulate at least two
  real paths and explain why the chosen one wins
- **Reject invented facts**: do not choose databases, frameworks, API shapes,
  retry policies, cache TTLs, or deployment topology without explicit
  authority or evidence
- **Require explicit authority**: DEC approval needs product/architecture owner,
  not just IBM i SME
- **Surface unresolved questions**: when decision ownership or grounding is
  unclear, file a `TBD-*` instead of fake-approving
- **Validate traceability**: confirm every DEC traces bidirectionally to BR/BEH
  and evidence, and to ACs only when the spec already contains them

## Workflow

### Phase 1 — Intake & Validation

1. **Receive** spec with draft/in-review `DEC-*` records (or request one)
2. **Validate input**:
   - Spec has ≥1 `DEC-*` entry
   - Each DEC has `id`, `decision`, `rationale` (even if draft)
   - Each DEC references at least one BR or BEH plus at least one EV, unless the
     decision is purely a target-platform constraint with explicit authority
   - No circular references (DEC → non-existent BR/EV)
3. **Stop if validation fails**: request spec repair and re-trigger

### Phase 2 — Expansion (Per DEC)

For each `DEC-*` record:

1. **Unpack the decision**: extract context, current rationale, implicit
   assumptions
2. **Identify alternatives**: what else could the system do?
   - Preserve legacy behavior as-is (if valid)
   - Adopt a different target framework/architecture
   - Defer the decision to runtime configuration
   - Accept an acceptable trade-off (speed vs. complexity)
3. **Gather evidence**: which BR/BEH/EV supports each option?
4. **Evaluate criteria**:
   - Does the chosen option satisfy the linked BR?
   - Does it respect the target platform constraint?
   - What is the implementation cost?
   - What new risks emerge?
5. **Document the decision** in `decision-record.md` template
6. **Surface TBDs**: if alternatives are unclear or authority is missing, file a
   `TBD-<CAP-SLUG>-NNN` instead of fake-approving

### Phase 3 — Review & Approval

1. **Generate `decision-review.md`**: checklist of approval gates
2. **Require SME review**:
   - IBM i SME verifies BR/BEH linkage and legacy preservation concerns
   - SME does NOT approve target architecture (outside scope)
3. **Require Architecture/Product review**:
   - Architecture owner evaluates target trade-offs and implementation impact
   - Arch owner explicitly approves or rejects each DEC
   - Arch owner signs off with date and role
4. **Reconcile back to spec**: if the decision package is approved, update only
   schema-compliant `spec.yaml.modernization_decisions[]` fields
   (`decision`, `rationale`, `evidence_ids`, `impact`, `review_status`). Keep
   alternatives and approval details in `05_decisions/`.

### Phase 4 — Traceability & Handoff

1. **Generate `traceability.md`**: cross-reference matrix showing:
   - Every DEC → linked BRs/BEHs
   - Every DEC → target platform constraints
   - Every DEC → affected acceptance criteria, when ACs already exist
   - Every DEC → handoff impact (e.g., "requires downstream database design")
2. **Verify no orphans**: all approved DEC records are reconciled to
   `spec.yaml` or explicitly deferred; all legacy BEHs affected by decisions are
   documented
3. **Prepare for external handoff**: after the Forward Handoff Gate passes, the
   external forward SDLC chain consumes approved DEC records from `spec.yaml`
   plus decision package context when supplied

## Workflow State Write-Back (history only)

This is a governance skill — it formalizes large / risky `DEC-*`
modernization decisions into standalone records. It does NOT advance
`capabilities[].stage_id` (decisions can be authored at any stage from
BRD onward) and does NOT mutate `current_focus`.

After a run, append one `history[]` entry to
`<project-root>/workflow-state.yaml` per
[`docs/workflow-state-contract.md`](../../../docs/legacy-spec-factory/workflow-state-contract.md):

```yaml
history:
  - at: <ISO 8601>
    skill: legacy-modernization-decision-writer
    capability_id: <CAP-* from current_focus, or null if cross-capability>
    stage_after: <UNCHANGED stage_id>
    artifact: <path to the DEC-* record, e.g. 08_business-understanding/decisions/DEC-001.md>
    note: "authored DEC-<NNN> — <one-line decision>: status <draft | proposed | approved>"
```

Also overwrite `project.last_updated_at` / `project.last_updated_by`.

**Permitted side-effect:** if the decision is `proposed` but lacks
target-platform authority approval (required by the Forward Handoff
Gate), append `"forward_handoff"` to
`capabilities[<CAP-*>].blocking.gates`. You MUST NOT change `stage_id`,
`last_artifact`, or `last_skill`.

If `workflow-state.yaml` does not exist, this skill does NOT create it.

## Anti-Hallucination Boundaries

See `references/anti-hallucination.md` for the exhaustive list. Core rules:

- **Do not invent business rules**. DEC decisions must be grounded in existing BR
  or explicit target constraint, not speculation.
- **Do not choose Java, Spring, Kafka, PostgreSQL, cache TTLs, retry policies,
  service boundaries, deployment topology, or API shape** without explicit
  approval from the target platform authority. Reference the decision
  `target_platform_constraints` field when the choice depends on target
  technology — if that field is empty for a technology choice, the choice is
  ungrounded.
- **Do not use "the legacy system did it" as sufficient rationale** for the new
  system. The decision must explain *why the new system should do it* given the
  new architecture.
- **Do not approve decisions when decision authority is missing**. If the
  architecture owner hasn't signed off, the DEC stays `draft` or
  `needs_sme_review` with `pending_approvals` listing the missing
  architecture/product authority — it doesn't ship as `approved`.
- **Do not hide unresolved questions in prose**. Surface every "unclear",
  "probably", "to be determined" phrase as a TBD with ID and blocking status.

## Examples

- `examples/decision-positive-ORDERS-001.md`: one approved decision record
- `examples/decision-negative-ORDERS-ANTI.md`: concrete anti-patterns
  (invented rationale, missing authority, unresolved choices presented as
  approved)

## References

- `references/decision-rules.md` — synthesis guidance per decision category
- `references/anti-hallucination.md` — invention boundaries specific to decisions
- `../../../docs/legacy-spec-factory/id-conventions.md` — stable ID format and uniqueness rules
- `../../../docs/legacy-spec-factory/evidence-and-knowledge-taxonomy.md` — knowledge types and evidence
  strength scoring
- `../../../docs/legacy-spec-factory/forward-sdlc-contract.md` — handoff expectations
- `../../AGENTS.md` — skill portability and authorship

## Version History

- v0.1.0 (2026-05-16): Runtime smoke test passed in Codex CLI
  (`gpt-5.4-mini`), Claude Code (`haiku`), and OpenCode
  (`opencode/minimax-m2.5-free`) with positive and negative no-write
  scenarios. Runtime cap lifted from 9.0 to 9.56.
