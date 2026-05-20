---
name: legacy-ibmi-module-analyzer
description: Synthesize a complete IBM i business module from multiple flow analyses and BAU notes, producing the canonical 4-view module analysis (Operation Flow, System Flow, Program Flow, Data Flow). Use when multiple flows belong to the same business module and you need cross-flow synthesis to feed `legacy-spec-writer`. Layer 1.5 (platform-specific) skill. Implements the model defined in `docs/module-analysis-model.md`.
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

# IBM i Legacy Module Analyzer

## Purpose

Synthesize multiple flow analyses, BAU (Business As Usual) notes, and SME
context into one **business module** analysis covering four standard
views: Operation Flow, System Flow, Program Flow, Data Flow.

This skill is the **last platform-specific layer** before `legacy-spec-writer`.
It does not re-analyze flows or programs; it aggregates and synthesizes
what flow-analyzer and program-analyzer produced.

The canonical model is documented in `../../../docs/legacy-spec-factory/module-analysis-model.md` —
read that first if you have not already.

## Inputs

Accept:

- **Module definition** — module slug, business name, scope statement,
  the list of flows that belong to this module
- **Approved flow analyses** for every flow in scope
  (`flow-<FLOW-SLUG>.md`)
- **Approved program analyses** for every program referenced by those flows
- **Approved inventory** with module scope confirmed
- **BAU notes from SME** — operational rhythm, manual processes,
  exception handling, business context not in code
- **Optional:** architecture diagrams (for System Flow), data lineage
  documents, regulatory references
- **Conditionally required from triggers:**
  - When `inventory.yaml.sme_review.downstream_required.screen_report_analyzer.required: true`
    → approved `screen-report-analysis.md` for every triggered DSPF /
    PRTF / menu. View 1 (Operation Flow) consumes these as primary
    sources for screen-driven rules; absence means missing 40% of
    user-facing decisions.
  - When `inventory.yaml.sme_review.downstream_required.data_model_analyzer.required: true`
    → approved `04_modules/<MODULE-SLUG>/data-model/dictionary.md`. View
    4 (Data Flow) populates from this dictionary verbatim instead of
    re-deriving entities from per-program File I/O tables.

Trigger rules and override protocol live in
[`skills/legacy-ibmi-inventory/references/downstream-triggers.md`](../legacy-ibmi-inventory/references/downstream-triggers.md).

Stop and require clarification if:

- Any in-scope flow lacks an approved `flow-<FLOW-SLUG>.md` → route to
  `legacy-ibmi-flow-analyzer`
- A trigger is `required: true` but the corresponding artifact is missing
  → route to the triggered skill (`legacy-ibmi-screen-report-analyzer`
  or `legacy-ibmi-data-model-analyzer`), do NOT begin synthesis
- Module boundary is ambiguous (does flow X belong here or in another
  module?) → SME-only decision
- No SME has confirmed the business name and scope of the module
- BAU notes are absent; the Operation Flow view requires SME input that
  cannot be derived from code alone

## Output Contract

Produce a directory `04_modules/<MODULE-SLUG>/`:

```
04_modules/<MODULE-SLUG>/
├── module-overview.md          ← summary, 4-view index, blocking TBDs, sign-off
├── 01-operation-flow.md        ← View 1: Business view + BAU
├── 02-system-flow.md           ← View 2: Integration view
├── 03-program-flow.md          ← View 3: Application/program view (aggregates flows)
├── 04-data-flow.md             ← View 4: Data view (aggregates Object Dependencies)
└── module-review-checklist.md  ← SME sign-off for the whole module
```

Use:

- `templates/module-overview.md` and `templates/view-template.md` as scaffolding
- `references/output-contract.md` for the file format and required fields for
  module-overview and all four views
- `references/synthesis-rules.md` for how to aggregate across flows
- `../../../docs/legacy-spec-factory/module-analysis-model.md` for the canonical model

Follow:

- `../../../docs/legacy-spec-factory/id-conventions.md` for stable IDs
  (`MODULE-*`, `VIEW-*`, `BR-*`, `ACTOR-*`, `SYS-*`, `DATA-*`)
- `../../../docs/legacy-spec-factory/evidence-and-knowledge-taxonomy.md` for evidence tagging
- `../../../docs/legacy-spec-factory/input-readiness-rubric.md` for input readiness scoring

Examples:

- `examples/module-positive/` — complete CARD-AUTH module with all 4 views
- `examples/incomplete-module-negative/` — module with missing flow / SME gap

## Step Contract

This skill is one step in the Legacy Spec Factory reverse chain. It conforms
to the canonical Step Contract shape — see
`../legacy-step-contract/SKILL.md` and
`../legacy-step-contract/references/step-contract.md` for the full
field-level rules. The summary below is normative for this skill.

### Input

- **Required**: module definition (slug + business name + scope statement
  + list of in-scope flows); approved `flow-<FLOW-SLUG>.md` for every
  in-scope flow; approved `program-analysis-<OBJ-ID>.md` for every
  program referenced by those flows; approved
  `01_inventory/inventory.yaml`; BAU notes from SME covering operational
  rhythm and manual procedures.
- **Optional**: architecture diagrams (View 2), data lineage docs
  (View 4), regulatory references.
- **Input readiness scoring**:
  - `0-5 blocked`: module scope unresolved, approved upstream analyses
    missing, triggered data/screen/report analysis missing, evidence links
    broken, or evidence authorization unresolved.
  - `6 minimum_pass`: approved inventory, required flows, required program
    analyses, module slug/name/scope, and SME BAU notes are present.
  - `7-8 usable`: triggered data/screen/report outputs, architecture notes,
    data lineage, and known TBD ledgers are supplied.
  - `9-10 strong`: SME edge cases, exception examples, sample transactions,
    regulatory context, and modernization decision context are also supplied.
  - Missing architecture diagrams or regulatory references does not block the
    module analysis unless the module scope specifically depends on them.
- **Readiness checks**: every in-scope flow is `approved` or
  `approved_with_non_blocking_tbd`; SME has confirmed the module's
  business name and boundary; BAU notes are present (View 1 requires
  SME input that code alone cannot supply).
- **Stop conditions**: any in-scope flow lacks an approved analysis;
  module boundary is ambiguous (which module owns flow X); no SME has
  confirmed module identity; BAU notes are absent.

### Execution

- **Procedure**: see the Workflow section below (9 ordered steps).
- **Allowed inference**: aggregating across approved flow/program/
  inventory artifacts; cross-view consistency checking; computing data
  lifecycle and coupling score from existing Object Dependency data.
- **Forbidden assumptions**: inventing business actors, upstream /
  downstream systems, BAU rhythm, regulatory requirements, manual
  intervention procedures, cross-module dependencies, or business rules
  (these remain seeds). Tier-2 SME claims that contradict tier-1 code
  become TBDs, not overrides.
- **TBD handling**: missing flow analysis → `TBD: pending_source`
  routing to `legacy-ibmi-flow-analyzer`; business context absent from
  BAU notes → `TBD: pending_sme_judgment`; ambiguous module boundary
  → `TBD: pending_sme_judgment`; incomplete data lifecycle →
  `TBD: pending_sme` (archive/purge ownership).

### Output

- **Canonical directory**: `04_modules/<MODULE-SLUG>/` containing
  `module-overview.md`, `01-operation-flow.md`, `02-system-flow.md`,
  `03-program-flow.md`, `04-data-flow.md`, `module-review-checklist.md`.
- **Required sections**: 4-view index with per-view status, top blocking
  TBDs, module-level capability seeds, per-view review checklists.
- **Required IDs**: mints `MODULE-*`, `VIEW-*`, `ACTOR-*`, `SYS-*`,
  module-level `BR-*` **seeds**, module-level `CAP-*` **seeds**, and
  `TBD-*`. Reuses `OBJ-*`, `EV-*`, `FLOW-*`, `NODE-*`, `EDGE-*`,
  `DATA-*`. Final promotion of `BR-*` happens in `legacy-spec-writer`.
- **Handoff status**: each view independently `draft` → `in_review` →
  `approved` or `approved_with_non_blocking_tbd`. Module is approved
  only when **all four views** are at least
  `approved_with_non_blocking_tbd`. `blocked_pending_source` /
  `blocked_pending_sme` halt spec-writer.

### Validation

- **Mechanical**: all four views plus overview present; every claim
  traces to source artifact or named SME note; every cross-view
  reference resolves; every TBD carries a category and ID; capability
  seeds carry IDs.
- **AI semantic**: cross-flow synthesis matches the flow analyses (no
  new IBM i facts introduced); cross-view consistency holds (every View 1
  actor appears in View 3 or is tagged manual; every View 2 system
  appears in View 3; every View 4 data object traces to a flow); seeds
  are questions, not approved rules; tier-2 claims contradicting tier-1
  are surfaced as TBDs.
- **SME / human approval**: View 1 by business owner, View 2 by
  integration architect, View 3 by dev lead, View 4 by data analyst.
  All four sign-offs are required to promote the module past
  `approved_with_non_blocking_tbd` for spec-writer consumption.
- **Blocking conditions**: any view lacks an SME sign-off; any
  cross-view inconsistency unresolved; any in-scope flow missing or
  unapproved; any capability seed contradicts the underlying flows;
  BAU notes still absent.

Emit a Step Validation Report (see
`../legacy-step-contract/templates/step-validation-report.md`) with
status `pass`, `pass_with_warnings`, or `blocked` when reporting upward
to the orchestrator.

## Workflow

1. **Confirm Module Scope**
   - Validate the module slug, business name, and scope statement with SME
   - List in-scope flows; check every one has an approved analysis
   - Confirm no in-scope flow actually belongs to a different module
   - Assign `MODULE-<SLUG>-001`

2. **Aggregate Inventory of Programs & Objects**
   - List every program touched by any flow in scope (from each flow's
     Nodes section)
   - List every object touched (from each program's Object Dependencies
     section)
   - Cross-check against `01_inventory/inventory.yaml`; create
     `pending_source` TBDs for gaps

3. **Build View 1 — Operation Flow / Business Background**
   - Use the View 1 section in `references/output-contract.md` and the
     aggregation rules in `references/synthesis-rules.md`
   - **Primary source: SME interviews + BAU notes.** Code is secondary.
   - Capture: business scope, actors, business events, BAU rhythm,
     manual intervention points, exception lifecycle, business-rule seeds
   - Do **not** derive business rules from field names
   - Output: `01-operation-flow.md`

4. **Build View 2 — System Flow**
   - Use the View 2 section in `references/output-contract.md` and the
     aggregation rules in `references/synthesis-rules.md`
   - **Primary source: architecture diagrams, integration specs, SME.**
     Code (especially API/MQ/IFS code in flows) confirms.
   - Capture: upstream systems, downstream systems, external interfaces,
     integration patterns, sync/async boundaries, SLA constraints,
     security boundaries
   - Output: `02-system-flow.md`

5. **Build View 3 — Program Flow (Aggregate)**
   - Use the View 3 section in `references/output-contract.md` and the
     aggregation rules in `references/synthesis-rules.md`
   - **Primary source: all `flow-<FLOW-SLUG>.md` documents.**
   - Aggregate per-flow summaries; identify cross-flow dependencies and
     shared sub-programs
   - Do **not** re-derive control flow; reference the flow / program
     analyses
   - Output: `03-program-flow.md`

6. **Build View 4 — Data Flow (Aggregate)**
   - Use the View 4 section in `references/output-contract.md` and the
     aggregation rules in `references/synthesis-rules.md`
   - **Primary source: every flow's Cross-Program Data Flow section,
     backed by every program's Data Touch Map and Object Dependencies.**
   - Compute data lifecycle per object (created / updated / read /
     archived / purged) by walking flows
   - Compute coupling score (number of flows touching each object)
   - Identify coupling hotspots, cross-module data dependencies, DB
     table relationships
   - Output: `04-data-flow.md`

7. **Cross-View Consistency Check**
   - Every business actor in View 1 should map to at least one entry node
     in View 3 (or be tagged "manual actor — no code path")
   - Every upstream/downstream system in View 2 should appear at least
     once in View 3 as a trigger or external call
   - Every business-rule seed in View 1 must reference at least one
     program / file in View 3 / View 4
   - Every data object in View 4 must trace to at least one flow / program
     in View 3
   - Mismatches → cross-view TBDs

8. **Write module-overview.md**
   - 4-view index with status per view
   - Top blocking TBDs surfaced from any view
   - Module-level capability seeds (which capabilities live in this module,
     to be developed by `legacy-spec-writer`)
   - Module-level review checklist

9. **Prepare for SME Review**
   - Each view independently goes to its appropriate SME (business owner
     for View 1, integration architect for View 2, dev lead for View 3,
     data analyst for View 4)
   - Module is approved only when **all four views** are at least
     `approved_with_non_blocking_tbd`

## Workflow State Write-Back

At the end of a module-analysis run, update
`<project-root>/workflow-state.yaml` per
[`docs/workflow-state-contract.md`](../../../docs/legacy-spec-factory/workflow-state-contract.md).
Template: [`skills/legacy-modernization-orchestrator/references/state-writeback-snippet.md`](../legacy-modernization-orchestrator/references/state-writeback-snippet.md).

**Stage this skill produces:**

- `3f Module Analysis Done` when all 4 views (Operation / System / Program
  / Data) and `module-overview.md` are approved, capability seeds (`CAP-*`)
  are listed in the overview, and View 1 business rule seeds (`BR-*`)
  carry `evidence_id` + `knowledge_type`
- `3e Module Analysis In Progress` when one or more views are still draft
  or any required section is missing

**Last artifact path pattern:**
`04_modules/<MODULE-SLUG>/module-overview.md` (with sibling view files)

**Writes per run:**

1. Overwrite `capabilities[<CAP-* from current_focus>]` (or, for each
   `CAP-*` seeded in `module-overview.md` if the orchestrator scoped the
   module rather than a single capability) with stage id, overview path,
   `last_skill: legacy-ibmi-module-analyzer`, and blocking IDs (`tbds`,
   `sme_pending` for every `inferred_business_rule`).
2. Append one `history[]` entry with `note` naming the module
   (e.g. `"synthesized CREDIT-CHECK 4 views"`).
3. Overwrite `project.last_updated_at` / `project.last_updated_by`.

If this module yields multiple `CAP-*` seeds and the orchestrator scoped
the entire module (not a single capability), write one `capabilities[]`
entry per seed at the same `stage_id: "3f Module Analysis Done"`. Do not
silently collapse them into one entry.

Never touch `current_focus`, other capabilities' entries beyond your
module's seeds, or past `history[]` rows.

## Anti-Hallucination Rules

**Code is ground truth.** See `../../../docs/legacy-spec-factory/code-as-ground-truth.md`.
View 1 (Operation Flow) and View 2 (System Flow) **necessarily** rely on
SME and integration documentation (tier 2/3) because business "why" and
architectural intent live outside code. However, any tier-2 claim that
contradicts tier-1 evidence (e.g., SME says "we no longer use path X"
but code still has the path; SME says "every transaction is logged" but
the log write is conditional in code) **does not override the code**.
The spec records what code does; the SME claim becomes a TBD requiring
SME to confirm whether the code is dead, drifted, or correct.

Views 3 and 4 are tier-1-grounded by construction (they aggregate
code-derived flow / program analyses).

**Do NOT invent:**

- **Business actors** not named by SME (no inferring "the marketing team
  uses this" from code)
- **Upstream/downstream systems** not visible in any flow's Trigger
  Context or External Calls section
- **BAU rhythm** (cut-off times, peak hours) — must come from SME
- **Regulatory requirements** — must come from SME or referenced doc
- **Manual intervention procedures** — must come from SME
- **Cross-module data dependencies** without seeing the consuming module's
  inventory or SME confirmation
- **Business rules** — only seeds (questions); the spec-writer resolves
  them with SME

**Instead:**

- If View 1 needs business context not in BAU notes → TBD: pending_sme_judgment
- If View 2 needs integration detail not in any flow → TBD: pending_source
  (request integration spec) or pending_sme
- If a flow seems to belong to multiple modules → TBD: pending_sme_judgment
  on module boundary
- If a data object's lifecycle is incomplete → TBD: pending_sme
  (who archives / purges this?)

**Evidence minimum:**

- Every claim in every view must trace to either source (flow / program /
  inventory) or to a named SME / SME note.
- "Confirmed by SME [name] on [date]" is valid evidence; "common knowledge"
  is not.

## SME Review Questions

Per view:

**View 1 (Operation Flow):**
- Are the business actors complete? Any missing roles?
- Is the BAU rhythm correct? Cut-off times, peak hours, seasonal patterns?
- Are exception-handling procedures accurate?
- Are the business-rule seeds reasonable questions?

**View 2 (System Flow):**
- All upstream and downstream systems listed?
- Integration patterns correct?
- SLAs accurate?

**View 3 (Program Flow):**
- All flows in scope? Any missing or extra flows?
- Cross-flow dependencies correct?
- Shared sub-programs correctly identified?

**View 4 (Data Flow):**
- Data lifecycle correct for each major object?
- Coupling hotspots match operational reality (which files are "scary
  to change")?
- Cross-module data dependencies correctly identified?

## Runtime Portability

Canonical source: `skills/legacy-ibmi-module-analyzer/SKILL.md`

Synced via `scripts/sync-skills.sh` to all four runtime adapters.

## Version History

- v0.1.1 (2026-05-14): Post-review hardening
  - Fixed broken reference links in SKILL.md (nonexistent per-view methodology files)
  - Added `blocked_pending_source` and `blocked_pending_sme` status values
  - Added per-view review checklists (View 1–4) to output contract
  - Strengthened evidence traceability (TBD ID and Evidence Ref columns)
  - Added positive and negative smoke test prompts to runtime-smoke-tests.md
  - Ready for smoke testing in Codex CLI, Claude Code, OpenCode

- v0.1.0 (2026-05-14): Initial release
  - 9-step workflow
  - 4-view synthesis (Operation / System / Program / Data)
  - Cross-view consistency checks
  - Module-level capability seeds (for spec-writer)
  - Feedback loops to flow-analyzer, program-analyzer, inventory
  - Examples: complete module (CARD-AUTH), incomplete module (missing flow)
