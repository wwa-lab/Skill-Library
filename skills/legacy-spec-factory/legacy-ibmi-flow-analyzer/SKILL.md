---
name: legacy-ibmi-flow-analyzer
description: Analyze a complete IBM i call chain — one business transaction end-to-end across all programs it touches. Supports seven trigger models (batch job, interactive menu, subfile dispatch, F-key branch, DB trigger, scheduler, API/remote). Produces a flow analysis covering trigger context, sequence, cross-program data flow, error propagation, commit boundaries, UI surfaces, and business-capability seeds. Use when a single program analysis is insufficient because the business event spans multiple programs. Layer 1.5 (platform-specific) skill of the Legacy Spec Factory reverse chain.
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

# IBM i Legacy Flow Analyzer

## Purpose

Analyze one **call chain** — a complete business transaction that spans
multiple programs, from trigger to final outcome. Where
`legacy-ibmi-program-analyzer` looks inside one program, this skill looks
across programs: how they are stitched together, what data passes between
them, when they branch, and how errors propagate.

The primary orientation view is a **Transaction Call Map**: an RDi-style
cross-program/cross-boundary call map. It is not a statement-level
flowchart. It should preserve the transaction's program and external
dependency structure while keeping full call details in tables.

This skill does **not** re-analyze individual programs. Every program in
the flow must already have an approved
`program-analysis-<OBJ-ID>.md`; if any is missing, route back to
`legacy-ibmi-program-analyzer`.

This skill does **not** infer business rules. It captures the *structure*
of the transaction so that downstream `legacy-spec-writer` (via
`legacy-ibmi-module-analyzer`) can derive business rules with proper SME
involvement.

## Inputs

Accept:

- **Flow definition** — the entry point of the chain, declared as one of
  seven trigger types (see `references/trigger-models.md`):
  - batch job (CL + SBMJOB or direct CALL)
  - interactive menu (`*MENU` option selection)
  - subfile dispatch (option codes 1/4/5/9/etc.)
  - F-key branch (DSPF function-key handling)
  - DB trigger (file trigger program)
  - scheduler (WRKJOBSCDE entry)
  - API / remote (remote PGM call, MQ message, HTTP, IFS drop)
- **Approved program analyses** for every program in the chain
- **Approved inventory** with `relationships` populated for the involved objects
- Optional: SME notes on trigger context, BAU rhythm, known error scenarios
- Optional: DSPF / PRTF / MENU object definitions (for UI-aware flows)

Stop and require clarification if:

- Any program in the chain lacks an approved `program-analysis-<OBJ-ID>.md`
  → route to `legacy-ibmi-program-analyzer`
- A required call edge, data flow, or error path depends on an upstream
  program routine marked `blocked` or `indexed_only` with business state
  impact → route back to `legacy-ibmi-program-analyzer`
- Inventory `sme_review.decision` is `blocked` or `relationships` are
  incomplete → route to `legacy-ibmi-inventory`
- Trigger model cannot be identified from the entry point → require SME
  clarification (do not guess)
- Flow appears to span multiple business modules → narrow scope; one flow
  = one business transaction

## Output Contract

Produce a single artifact:

- `flow-<FLOW-SLUG>.md`

`<FLOW-SLUG>` is uppercase, hyphen-separated, business-event named (e.g.,
`ONUS-AUTH`, `BATCH-RECON`, `CHARGEBACK-INTAKE`), and stable across the
analysis chain.

Use:

- `templates/flow.md` as the starting structure
- `references/output-contract.md` for section definitions and required fields
- `references/trigger-models.md` for trigger-specific analysis guidance
- `references/data-flow-patterns.md` for cross-program data passing
- `references/error-propagation.md` for error-chain analysis

Follow:

- `../../../docs/legacy-spec-factory/id-conventions.md` for stable IDs (`FLOW-*`, `NODE-*`, `EDGE-*`, `DATA-*`)
- `../../../docs/legacy-spec-factory/evidence-and-knowledge-taxonomy.md` for evidence strength tagging
- `../../../docs/legacy-spec-factory/input-readiness-rubric.md` for input readiness scoring

Examples:

- `examples/batch-job-positive/` — straightforward batch chain (`CL → RPG1 → RPG2 → SQLRPG`)
- `examples/menu-flow-positive/` — interactive flow with `*MENU` + DSPF + subfile dispatch
- `examples/incomplete-flow-negative/` — flow with a missing program-analysis (must route back)

## Step Contract

This skill is one step in the Legacy Spec Factory reverse chain. It conforms
to the canonical Step Contract shape — see
`../legacy-step-contract/SKILL.md` and
`../legacy-step-contract/references/step-contract.md` for the full
field-level rules. The summary below is normative for this skill.

### Input

- **Required**: flow definition (entry point + one of seven trigger
  models); approved `program-analysis-<OBJ-ID>.md` for every program in the
  chain; approved `01_inventory/inventory.yaml` with `relationships`
  populated for the involved objects.
- **Optional**: DSPF / PRTF / `*MENU` definitions (UI-aware flows);
  `WRKJOBSCDE` export (scheduler triggers); trigger-program registration
  (DB triggers); SME notes on BAU rhythm and known error scenarios.
- **Input readiness scoring**:
  - `0-5 blocked`: approved inventory missing, required program analyses
    missing, call-chain root unresolved, trigger model unidentified, or
    evidence authorization unresolved.
  - `6 minimum_pass`: root object, approved inventory, and the program
    analyses needed for the requested chain are present.
  - `7-8 usable`: scheduler/job notes, menu/display/report definitions, and
    object dependencies are available for most chain edges.
  - `9-10 strong`: runtime logs, screen/report samples, SME notes on triggers
    and manual workarounds, and known exception cases are also supplied.
  - Missing runtime samples does not block structural flow analysis; it leaves
    runtime ordering and trigger confidence lower.
- **Readiness checks**: Inventory Completeness Gate passing; every node
  in the chain has an approved program-analysis; trigger model identified
  unambiguously; the flow represents one business transaction.
- **Stop conditions**: any node missing an approved program-analysis;
  a required call edge, data flow, or error path depends on an upstream
  routine marked `blocked` or `indexed_only` with business state impact;
  inventory `sme_review.decision` is `blocked` or relationships are
  incomplete; trigger model cannot be identified from the entry point;
  flow spans multiple business modules.

### Execution

- **Procedure**: see the Workflow section below (10 ordered steps).
- **Allowed inference**: assembling cross-program call edges from
  upstream program analyses; classifying call types (CALL / CALLP /
  CALLPRC / SBMJOB / remote); deriving branch destinations from DSPF
  option tables; reading scheduler / trigger / API configuration exports
  as tier-1 evidence.
- **Forbidden assumptions**: calls not visible in any program-analysis
  External Calls section; data flow whose parameter semantics require
  guessing; branch destinations not in DSPF DDS; trigger conditions
  without configuration export; scheduler frequency without
  `WRKJOBSCDE`; commit boundaries without code or SME confirmation;
  business rules (these are seeds, never facts).
- **TBD handling**: missing program-analysis → `TBD: pending_source`
  routing to `legacy-ibmi-program-analyzer`; ambiguous trigger →
  `TBD: pending_sme_judgment`; unnamed business event → stop and request
  the name from SME (do not autogenerate from program names).
- **Coverage propagation**: consume each upstream program's Analysis
  Coverage & Scope, Routine Cards, and Deep Read Windows before using
  program-level evidence in a flow. If the requested flow relies on a
  routine that was only `indexed_only` and that routine changes state,
  performs external handoff, handles commit/rollback, or controls error
  outcome, flow analysis is blocked until the routine is `deep_read` or a
  named SME waiver is recorded in review metadata.

### Output

- **Canonical artifact**: `flow-<FLOW-SLUG>.md`.
- **Required sections**: trigger model & entry point, transaction call
  map, nodes, edges, common dependencies, cross-program data flow, branch
  points, UI surfaces (or `N/A — non-interactive`), error propagation &
  commit boundaries, capability seeds, SME review checklist.
- **Required IDs**: mints `FLOW-*`, `NODE-*`, `EDGE-*`, `DATA-*`,
  `SEED-*`, `TBD-*`; reuses `OBJ-*`, `EV-*`, and program-level `BEH-*`
  from upstream. Flow analysis does not mint `BR-*`; branch points are
  represented by `NODE-*` / `EDGE-*` entries and capability questions by
  `SEED-*`.
- **Handoff status**: `status: draft` → `needs_sme_review` →
  `approved` or `approved_with_non_blocking_tbd`.
  `blocked_pending_source` and `blocked_pending_sme` halt
  module-analyzer.

### Validation

- **Mechanical**: every edge traces to evidence type 1, 2, or 3 (source
  statement, config export, or integration contract); every data exchange
  traces to a source line; every UI surface traces to a DSPF/PRTF/`*MENU`
  in inventory; every trigger has evidence type 2 plus SME confirmation
  of business meaning; every node carries upstream coverage state and
  any blocking coverage gaps; all required sections populated.
- **AI semantic**: edges match upstream program-analyses (no invented
  calls); branch destinations match DSPF option tables; error
  propagation matches each node's program-analysis; commit boundaries
  are evidenced, not assumed; flow evidence is not taken from
  `indexed_only` or `blocked` routines when those routines have business
  state impact unless a named SME waiver is recorded; capability seeds
  are *questions*, not rule claims.
- **SME / human approval**: SME confirms trigger model, business event
  name, node/edge correctness, branch points, UI surfaces (interactive
  flows), error propagation realism, commit boundaries, and that seeds
  are reasonable questions. Required when a cross-program rule emerges
  or when the flow touches money, inventory, compliance, or customer
  status.
- **Blocking conditions**: any node lacks an approved program-analysis;
  any edge has no evidence; trigger model unresolved; business event
  name unnamed by SME; ambiguous module boundary; required flow evidence
  depends on `blocked` coverage or `indexed_only` state-impacting
  routines without a named SME waiver; SME absence when the flow's risk
  class requires SME.

Emit a Step Validation Report (see
`../legacy-step-contract/templates/step-validation-report.md`) with
status `pass`, `pass_with_warnings`, or `blocked` when reporting upward
to the orchestrator.

## Workflow

1. **Identify Trigger Model & Entry Point**
   - Determine which of the seven trigger models applies (see
     `references/trigger-models.md`). If unsure, ask the SME — do not guess.
   - Document the trigger object:
     - batch job → CL program + direct CALL from another program or operator
     - menu → `*MENU` object name + option number
     - subfile dispatch → DSPF subfile + option-code table
     - F-key → DSPF + function-key handler
     - DB trigger → file name + trigger program + event (insert/update/delete)
     - scheduler → WRKJOBSCDE entry + frequency (may submit a batch job via SBMJOB)
     - API / remote → remote-call mechanism + parameter contract
   - **Note:** Scheduler-submitted batch jobs form a single flow: the scheduler
     entry is the primary trigger, SBMJOB is the submission mechanism, and the
     CL/RPG program(s) are the nodes. This is one trigger model, not two.
   - Assign `FLOW-<SLUG>-<NNN>` ID.
   - Capture the **business event name** the SME uses for this flow
     (e.g., "Customer authorization request", not "RPG1 call").

2. **Enumerate Nodes (Programs in the Chain)**
   - List every program the flow touches, in call order.
   - For each node:
     - assign `NODE-<SLUG>-<NNN>` (sequence-numbered)
     - reference the program's `OBJ-*` (from inventory) and approved
       `program-analysis-<OBJ-ID>.md`
     - record the program's role in the flow (entry / orchestrator /
       worker / data-access / reporter / exit)
     - carry forward the program's Analysis Coverage & Scope, Routine
       Cards, and Deep Read Windows; record node coverage status as
       `deep_read`, `indexed_only`, or `blocked` plus flow readiness
       (`approved`, `warning`, or `blocked`)
     - record blocking coverage gaps when a required call edge, data
       exchange, branch, error path, or commit boundary depends on a
       routine that is `blocked` or is `indexed_only` with business state
       impact
   - If a node has no approved `program-analysis`, **stop** and create
     `TBD-<SLUG>-<NNN>: pending_source` routing back to
     `legacy-ibmi-program-analyzer`.
   - If a node's required state-impacting routine is only `indexed_only`,
     **stop** until `legacy-ibmi-program-analyzer` deep-reads it or a
     named SME waiver is recorded in evidence/review/sign-off metadata.

3. **Trace Edges (Calls Between Nodes)**
   - For every call between two nodes, document an edge:
     - `EDGE-<SLUG>-<NNN>: NODE-A → NODE-B`
     - Call type (CALL, CALLP, CALLPRC, EXSR-not-applicable-cross-program,
       SBMJOB, remote-call)
     - Call site (source program + line number) — from the caller's
       `program-analysis`
     - `Via` routine/procedure — the internal node from the caller's
       Program Call Map where the edge exits the program, when visible
     - Call condition (always / conditional / loop / error path)
   - Build the **Transaction Call Map** (see
     `references/output-contract.md` for format). The map shows
     cross-program and cross-boundary structure; detailed call conditions
     remain in the edge table.

4. **Classify Common Dependencies**
   - If multiple nodes call the same common program, service program, API,
     data queue, message queue, or wrapper, keep every inbound call in the
     edge table and summarize the target in Common Dependencies.
   - Keep common nodes expanded as formal flow nodes when they write
     business files, change customer/account/inventory/money state,
     decide approve/decline outcomes, control commit/rollback, or call an
     external business system.
   - Fold common nodes in the visual map only when they are technical
     utilities such as logging, message formatting, date/time,
     delay/wait, or wrapper code. Folding is visual only; evidence and
     edge rows remain complete.
   - Do not infer a Java service boundary from shared usage alone. That is
     a modernization decision for module/spec stages with SME review.

5. **Cross-Program Data Flow**
   - For each edge, document what data passes (see
     `references/data-flow-patterns.md`):
     - parameters passed in the CALL
     - shared data area (`*DTAARA`) updates / reads
     - data queue (`*DTAQ`) messages
     - shared file writes/reads (program A writes, program B reads)
     - temporary work files / spool / IFS files
     - signal flags (return codes, indicators, error fields)
   - For each `DATA-*`, capture carrier, producer, consumer, mechanism,
     payload/key fields, direction and timing, state impact, and
     evidence. A carrier can be an `EDGE-*`, PF/LF, data area, data
     queue, message queue, spool, IFS file, DSPF field set, or manual
     handoff.
   - Track object / record / critical-field granularity. Critical fields
     include money, account/customer/card/inventory identifiers,
     approval/decline/status/posting flags, return/error codes, audit
     IDs, and external payload fields. Do not trace every temporary work
     variable.
   - Add short critical trails for business-important records or
     messages, such as `request -> DTAQ -> program -> log PF -> batch
     posting`.
   - Assign `DATA-<SLUG>-<NNN>` for each distinct data exchange.
   - Tag evidence; cross-reference to source line numbers via EV-\*.

6. **Branch Points & Decision Nodes**
   - Identify points where the flow forks (subfile option, F-key,
     conditional CALL, trigger event).
   - For each branch point:
     - the deciding artifact (which field / which key / which condition)
     - the alternatives and which target node each leads to
     - whether unhandled options/keys exist (silently dropped vs. error)

7. **UI Surfaces (interactive flows only)**
   - List every DSPF / PRTF / MENU the user sees during the flow.
   - For each:
     - object name + `OBJ-*`
     - which node displays it
     - key fields shown / entered
     - F-keys handled
     - branch destination per F-key / option
   - For non-interactive flows (batch, trigger, scheduler, API), this
     section may be `N/A — non-interactive flow`.

8. **Error Propagation**
   - For each node, summarise (from its `program-analysis` Error Handling
     section) what happens when each error condition occurs.
   - Trace propagation: does the error abort the whole flow, roll back to
     a checkpoint, log-and-continue, or branch to an error handler?
   - Identify **commit boundaries**: where does the flow consider work
     "committed" vs "rolled back"?
   - Identify **unhandled error windows**: nodes where an unhandled
     error would crash the entire flow without recovery (create TBD).
   - See `references/error-propagation.md`.

9. **Business Capability Seeds**
   - Extract `SEED-*` candidates (business rule seeds) that this flow
     plausibly enforces — **without inventing rules**.
   - Each seed is a *question* for SME review (e.g., "Does the rule
     'credit limit must not be exceeded' live in this flow?"), with
     pointers to the program(s) and field(s) that suggest it.
   - The spec-writer skill will resolve seeds into approved rules; the
     flow analyzer never approves rules itself.
   - **Note:** flow analysis does not mint `BR-*` IDs. Branch points are
     represented by `NODE-*` / `EDGE-*` entries; capability seeds use
     `SEED-*` IDs.

10. **Prepare for SME Review**
   - Consolidate all TBDs grouped by blocking status (`pending_source` /
     `pending_sme_judgment` / `non_blocking`).
   - **If any blocking TBDs exist:**
     - Mark flow as `blocked_pending_source` (missing program-analysis, missing DSPF, etc.)
       or `blocked_pending_sme` (ambiguous trigger, unclear error handling, missing business context)
     - Do not complete the full required analysis; provide partial flow stub
     - Route to `legacy-ibmi-program-analyzer` or SME assignment process
     - Do not proceed to module-analyzer
   - **If no blocking TBDs:**
     - Confirm every node's `program-analysis` is approved.
     - Generate the flow review checklist (see `templates/trigger-checklist.md`).
     - Mark flow as `draft` and route to SME.
   - **Gate:** the flow is ready for module-analyzer when:
     - all required sections populated
     - every node has an approved `program-analysis`
     - no blocking TBDs (or SME has explicitly waived them)
     - SME has signed off on the trigger model + business event name +
       capability seeds

## Workflow State Write-Back

At the end of a flow-analysis run, update
`<project-root>/workflow-state.yaml` per
[`docs/workflow-state-contract.md`](../../../docs/legacy-spec-factory/workflow-state-contract.md).
Template: [`skills/legacy-modernization-orchestrator/references/state-writeback-snippet.md`](../legacy-modernization-orchestrator/references/state-writeback-snippet.md).

**Stage this skill produces:**

- `3d Flow Analysis Done` when **every** business transaction the SME lists
  for this module has an approved `flow-*.md`
- `3c Flow Analysis In Progress` when one or more in-scope flows are still
  draft, blocked, or missing

**Last artifact path pattern:**
`03_flows/<MODULE-SLUG>/flow-<FLOW-SLUG>.md`

**Writes per run:**

1. Overwrite `capabilities[<CAP-* from current_focus>]` with stage id, the
   path of the flow you just saved, `last_skill: legacy-ibmi-flow-analyzer`,
   and blocking IDs (`tbds`, `sme_pending` for trigger context / commit
   boundary questions).
2. Append one `history[]` entry with `note` naming the flow
   (e.g. `"analyzed flow-submit-order"`).
3. Overwrite `project.last_updated_at` / `project.last_updated_by`.

Never touch `current_focus`, other capabilities' entries, or past
`history[]` rows. A re-run on the same flow is allowed; a re-run that
would lower `stage_id` requires the orchestrator's Rollback Protocol.

## Anti-Hallucination Rules

**Code is ground truth.** See `../../../docs/legacy-spec-factory/code-as-ground-truth.md`. Every
edge in this flow must trace to **evidence** from authoritative sources
(see `references/output-contract.md` Evidence Taxonomy). Authoritative
evidence includes:

- **Source statements** (CALL, CALLP, SBMJOB in code)
- **Configuration exports** (WRKJOBSCDE, DSPF DDS, trigger registration)
- **Integration contracts** (MQ queue configs, API gateway definitions, DDM registrations)
- **SME confirmation** (documented procedures, business event naming, SLA agreement)

Shop documentation, prior architecture diagrams, and SME recollection are
navigation aids; they do not become evidence until **tier-1 authoritative
confirmation** exists. If SME claims a flow path the code does not contain,
both observations are recorded and a TBD blocks the flow until SME reconciles them.

**Do NOT invent:**

- **Calls** not visible in any program's `program-analysis` External Calls section
- **Data flow** that requires guessing parameter semantics (use only what
  source explicitly shows or SME confirms)
- **Branch destinations** for F-keys / options not visible in DSPF DDS
- **Trigger conditions** for DB triggers without seeing trigger configuration export
- **Scheduler frequency or submitted command** without WRKJOBSCDE evidence
- **Commit boundaries** if neither code nor SME has confirmed them
- **Business capabilities or rules** — these are seeds (questions), not
  facts; spec-writer resolves them

**Instead:**

- If a node's `program-analysis` is missing → `TBD: pending_source` →
  route to `legacy-ibmi-program-analyzer`
- If configuration evidence is missing → `TBD: pending_source` → request
  WRKJOBSCDE export, DDS listing, or trigger configuration
- If a trigger model is ambiguous → `TBD: pending_sme_judgment`
- If the SME cannot name the business event → stop and request a name
  (do not autogenerate from program names)
- If error propagation is unclear → tag `needs_sme_review`; do not assume
  commit / rollback behavior

**Evidence minimum** (see Evidence Taxonomy):

- Every edge must trace to evidence type 1, 2, or 3 (source statement, config export, or integration contract)
- Every data exchange must trace to source (parameter, data area, queue,
  file, screen field, message, IFS file, or SME note)
- Every UI surface must trace to a DSPF / PRTF / MENU object in inventory
- Every trigger must have evidence type 2 (config export) + evidence type 4 (SME confirmation of business meaning)

## SME Review Questions

The generated `flow-<FLOW-SLUG>.md` must include a review checklist
covering:

- [ ] Trigger model correctly identified (batch / menu / subfile /
      F-key / trigger / scheduler / API)
- [ ] Business event name accurately reflects what the business calls this
      transaction
- [ ] All nodes (programs) in scope are correct; no missing programs and
      no extra programs
- [ ] All edges (calls) reflect actual production behavior
- [ ] Cross-program data flow captures carriers, producers, consumers,
      timing, state impacts, and no undocumented shared files or data areas
- [ ] Branch points correctly capture user-visible decision points
- [ ] UI surfaces match production screens (interactive flows only)
- [ ] Error propagation matches operational reality (what actually
      happens when this fails in prod)
- [ ] Commit boundaries are correct (one transaction vs. multiple)
- [ ] Capability seeds are reasonable questions, not invented rules

## Runtime Portability

Canonical source: `skills/legacy-ibmi-flow-analyzer/SKILL.md`

Runtime adapters are synced via `scripts/sync-skills.sh`:

- Codex: `.codex/skills/legacy-ibmi-flow-analyzer/SKILL.md`
- Claude Code: `.claude/skills/legacy-ibmi-flow-analyzer/SKILL.md`
- OpenCode: `.opencode/skills/legacy-ibmi-flow-analyzer/SKILL.md`
- Agents: `.agents/skills/legacy-ibmi-flow-analyzer/SKILL.md`

No runtime-specific assumptions are embedded in the canonical source.

## Version History

- v0.1.1 (2026-05-14): Field-pilot hardening
  - Added smoke test prompts and evidence taxonomy
  - Clarified trigger model rules: Scheduler + SBMJOB is one trigger (not composite)
  - Added blocked status values (blocked_pending_source, blocked_pending_sme) with routing rules
  - Standardized capability seed IDs on SEED-* and clarified that flow analysis does not mint BR-* IDs
  - Added evidence taxonomy: 4 types (source statement, IBM i config, integration contract, SME confirmation)
  - Updated anti-hallucination rules to allow config and contract evidence, not just source code
  - All 5 review blockers (FLOW-REV-001 to FLOW-REV-005) resolved
  - Ready for smoke test execution in Codex CLI, Claude Code, and OpenCode

- v0.1.0 (2026-05-14): Initial release
  - 9-step workflow
  - 7 trigger-model support (batch / menu / subfile / F-key / trigger /
    scheduler / API)
  - Cross-program data flow analysis
  - Error propagation and commit boundary detection
  - UI-surface mapping for interactive flows
  - Business capability seed extraction (no rule invention)
  - Feedback loop to `legacy-ibmi-program-analyzer` and
    `legacy-ibmi-inventory`
  - Examples: batch positive, menu positive, incomplete-flow negative
