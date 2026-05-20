# Large RPG Context-Window Analysis Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a practical large-program analysis protocol so Legacy Spec Factory can analyze 20k-30k+ line RPG programs without relying on one-pass model context.

**Architecture:** Phase 1 is documentation-and-contract first: introduce a large-program reference, add analysis coverage and routine-card sections to program outputs, propagate coverage risk into flow analysis, and extend validator checklists. This does not require a full RPG parser or graph database; it makes the current skill family enforce structure-first, evidence-backed, local-window analysis.

**Tech Stack:** Markdown skill files, canonical `skills/` directory, runtime skill sync via `scripts/sync-skills.sh`, existing Python verification scripts.

---

## File Structure

- Create `skills/legacy-ibmi-program-analyzer/references/large-program-analysis.md`: Defines large-program mode, source indexing, routine cards, deep-read windows, coverage ledger, and anti-patterns.
- Modify `skills/legacy-ibmi-program-analyzer/SKILL.md`: Wires the new reference into the program analyzer workflow and required outputs.
- Modify `skills/legacy-ibmi-program-analyzer/templates/program-analysis.md`: Adds `Analysis Coverage & Scope`, `Routine Cards`, and `Deep Read Windows` sections after `Metadata`.
- Modify `skills/legacy-ibmi-program-analyzer/references/output-contract.md`: Defines the new sections and the large-program mode rules.
- Modify `skills/legacy-ibmi-program-analyzer/examples/simple-crud-rpgle/program-analysis.md`: Adds a compact standard-mode coverage section.
- Modify `skills/legacy-ibmi-program-analyzer/examples/complex-batch-job/program-analysis.md`: Adds segmented-mode coverage and routine-card examples.
- Modify `skills/legacy-ibmi-flow-analyzer/SKILL.md`: Requires flow analysis to respect upstream program coverage and block or warn when a flow relies on unanalyzed routines.
- Modify `skills/legacy-ibmi-flow-analyzer/templates/flow.md`: Adds coverage status to flow nodes.
- Modify `skills/legacy-ibmi-flow-analyzer/references/output-contract.md`: Defines coverage propagation rules.
- Modify `skills/legacy-step-validator/references/validation-checklists.md`: Adds mechanical and semantic checks for large-program coverage and unsafe promotion.
- Modify `docs/runtime-smoke-tests.md`: Adds smoke expectations for large-program mode.
- Run `scripts/sync-skills.sh`: Propagates canonical skill changes into `.claude/skills`, `.opencode/skills`, `.agents/skills`, and `.codex/skills`.

## Task 1: Add Large-Program Reference

**Files:**
- Create: `skills/legacy-ibmi-program-analyzer/references/large-program-analysis.md`

- [ ] **Step 1: Create the reference file**

Use `apply_patch` to add:

```markdown
# Large Program Analysis

This reference defines how `legacy-ibmi-program-analyzer` handles large IBM i
programs when the full source cannot safely fit in model context.

## When To Use Large-Program Mode

Use large-program mode when any of these are true:

- source length is greater than 10,000 lines
- routine count is greater than 25 internal subroutines/procedures
- external call count is greater than 20
- file/object dependency count is greater than 25
- the analyzer cannot keep the full program, call graph, and evidence windows in
  context together

Use segmented mode for medium programs when the program is smaller than these
thresholds but still has dense call/data dependencies.

## Operating Rule

Do not summarize the whole program directly from raw source. First build a
structure index, then analyze semantic units, then synthesize.

The safe pipeline is:

1. Source size and structure preflight.
2. Deterministic source index.
3. Routine-level cards.
4. Program Call Map.
5. Data Touch Map.
6. Deep-read windows for hot paths, state changers, external boundaries, and
   error handling.
7. Coverage ledger.
8. Evidence-backed synthesis.

## Source Index

The source index is a compact inventory, not a business interpretation.

Capture:

- source line count
- declared files and F-spec / DCL-F entries
- copybooks and `/COPY` directives
- mainline range
- `BEGSR` / `ENDSR` subroutines
- procedures and prototype definitions
- `EXSR`, `CALL`, `CALLP`, `CALLPRC`, `PERFORM`, and CL `CALLSUBR` sites
- file operations: `CHAIN`, `SETLL`, `READE`, `READ`, `WRITE`, `UPDATE`,
  `DELETE`
- display/report operations: `EXFMT`, `WRITE` to DSPF/PRTF, printer overflow
- commit and rollback operations
- message/data-queue/API operations
- indicators and error handlers that affect branching or I/O outcome

## Routine Card

Each routine card records one semantic unit:

| Field | Meaning |
| --- | --- |
| Routine | Subroutine, procedure, paragraph, or mainline segment |
| Location | Source line range |
| Called By | Immediate inbound callers |
| Calls Out | Internal and external calls made by this routine |
| Data Touches | Files, queues, screens, reports, parameters, and critical fields |
| State Impact | `read-only`, `creates`, `updates`, `deletes`, `external handoff`, `unknown` |
| Error Handling | Local monitor, indicator checks, message writes, propagated status |
| Evidence | Source evidence IDs and line ranges |
| Coverage | `indexed_only`, `deep_read`, or `blocked`; SME confirmation belongs in review/sign-off metadata |
| Open Questions | Source gaps, SME questions, or contradiction references |

## Deep-Read Window Selection

Deep-read windows should prioritize:

- entry mainline and trigger handling
- routines on hot call paths
- routines with external calls
- routines that write, update, delete, commit, roll back, send messages, or send
  queue payloads
- routines touching money, account/customer IDs, inventory, approval/decline
  state, posting flags, audit IDs, or error/return codes
- routines involved in contradictions or flow-header drift

Do not deep-read every technical utility routine if it is structurally indexed
and has no business state impact.

## Coverage Ledger

The coverage ledger prevents partial analysis from masquerading as full
understanding.

Required fields:

| Metric | Meaning |
| --- | --- |
| Source Lines | Total source lines analyzed |
| Routines Found | Count from source index |
| Routines Deep-Read | Count and percentage |
| Routines Indexed Only | Count and reason |
| External Edges Resolved | Count and percentage |
| Data Touches Resolved | Count and percentage |
| Blocking Gaps | Source gaps that block flow/spec use |
| Non-Blocking Gaps | Known gaps that can proceed with warning |

## Forbidden Pattern

Do not split a 30k-line RPG program into fixed line chunks and summarize each
chunk independently. Fixed chunks destroy call relationships, state transitions,
and cross-routine data flow.

If chunking is required, chunk by semantic unit: mainline segment, routine,
procedure, copybook, object cluster, or call/data-flow path.
```

- [ ] **Step 2: Verify the file exists**

Run: `test -f skills/legacy-ibmi-program-analyzer/references/large-program-analysis.md`

Expected: command exits with status 0.

## Task 2: Wire Large-Program Mode Into Program Analyzer

**Files:**
- Modify: `skills/legacy-ibmi-program-analyzer/SKILL.md`
- Modify: `skills/legacy-ibmi-program-analyzer/references/output-contract.md`

- [ ] **Step 1: Add the reference to the skill's Use list**

In `skills/legacy-ibmi-program-analyzer/SKILL.md`, add this bullet after `references/output-contract.md`:

```markdown
- `references/large-program-analysis.md` for large-program, segmented, and context-window-safe analysis
```

- [ ] **Step 2: Update required output sections**

In the `### Output` section, replace the required sections sentence with:

```markdown
- **Required sections**: metadata, analysis coverage & scope, program call
  map (visual overview + node inventory + call tree + call edge table +
  reverse caller index), routine cards, deep read windows, entry points &
  parameters, control flow, object dependencies, data touch map, file I/O,
  external calls, error handling, TBD ledger, SME review checklist.
```

- [ ] **Step 3: Add large-program execution rule**

In the `### Execution` section, add this paragraph after the procedure bullet:

```markdown
- **Large-program mode**: when the source is larger than 10,000 lines,
  has more than 25 routines, has more than 20 external calls, or cannot
  safely fit in context with its evidence windows, run the structure-first
  process in `references/large-program-analysis.md`. Do not produce a
  whole-program business narrative until the source index, routine cards,
  Program Call Map, Data Touch Map, and coverage ledger exist.
```

- [ ] **Step 4: Add workflow preflight**

In `## Workflow`, insert this new step before the existing `1. Select Program & Verify Inventory` and renumber the existing steps:

```markdown
1. **Size & Structure Preflight**
   - Count approximate source lines, routine definitions, external calls,
     and object dependencies.
   - Select analysis mode: `standard`, `segmented`, or `large_program`.
   - For `segmented` and `large_program`, build the structure index before
     writing business summary prose.
   - Create the Analysis Coverage & Scope section and initialize the
     coverage ledger.
   - Do not claim complete program understanding until the coverage ledger
     supports that claim.
```

- [ ] **Step 5: Update output contract file structure**

In `skills/legacy-ibmi-program-analyzer/references/output-contract.md`, update the file structure block so it starts:

```markdown
# Program Analysis: [Program Name] (OBJ-*)

## Metadata
## Analysis Coverage & Scope
## Program Call Map
## Routine Cards
## Deep Read Windows
## Entry Points & Parameters
## Object Dependencies
## Data Touch Map
## Control Flow
## File I/O
## External Calls
## Error Handling
## TBDs & Blocking Status
## Review Checklist
```

- [ ] **Step 6: Add contract text for coverage sections**

Add this section after `## Metadata Section`:

```markdown
## Analysis Coverage & Scope Section

This section records how much of the program was indexed, deep-read, and left
for SME/source follow-up. It is mandatory for every program. Small programs can
mark `Analysis Mode` as `standard`.

Required tables:

1. Source Size & Strategy
2. Coverage Ledger
3. Routine Coverage Summary

Large-program and segmented-mode analyses must not proceed to business summary
prose until this section exists.
```

- [ ] **Step 7: Add routine-card contract text**

Add this section after the Program Call Map section in `output-contract.md`:

```markdown
## Routine Cards Section

Routine Cards are required for segmented and large-program mode. They are
recommended for all programs with more than five routines.

Each card must include: routine name, line range, called by, calls out, data
touches, state impact, error handling, evidence, coverage, and open questions.

The allowed coverage values are `indexed_only`, `deep_read`, and `blocked`.
SME confirmation belongs in evidence, review, or sign-off metadata, not in the
coverage enum.
```

## Task 3: Update Program Analysis Template

**Files:**
- Modify: `skills/legacy-ibmi-program-analyzer/templates/program-analysis.md`

- [ ] **Step 1: Add Analysis Coverage & Scope after Metadata**

Insert after the first `---` following metadata:

```markdown
## Analysis Coverage & Scope

### Source Size & Strategy

| Metric | Value |
| --- | --- |
| Source Lines | [count or collection estimate] |
| Analysis Mode | standard / segmented / large_program |
| Mode Reason | [why this mode was selected] |
| Structure Index Built | yes / no |
| Full Source In Context | yes / no |
| Business Narrative Allowed | yes / no |

### Coverage Ledger

| Coverage Area | Count / Status | Evidence | Notes |
| --- | --- | --- | --- |
| Routines Found | [N] | [EV-*] | [source index pointer] |
| Routines Deep-Read | [N of N] | [EV-*] | [coverage percentage] |
| Routines Indexed Only | [N] | [EV-*] | [why not deep-read] |
| External Edges Resolved | [N of N] | [EV-*] | [coverage percentage] |
| Data Touches Resolved | [N of N] | [EV-*] | [coverage percentage] |
| Blocking Gaps | none / [TBD-*] | [EV-*] | [impact] |
| Non-Blocking Gaps | none / [TBD-*] | [EV-*] | [impact] |

### Source Index Summary

| Index Item | Count | Notes | Evidence |
| --- | --- | --- | --- |
| Mainline Segments | [N] | [notes] | [EV-*] |
| Subroutines / Procedures | [N] | [notes] | [EV-*] |
| External Calls | [N] | [notes] | [EV-*] |
| File Operations | [N] | [notes] | [EV-*] |
| Display / Report Operations | [N] | [notes] | [EV-*] |
| Commit / Rollback Points | [N] | [notes] | [EV-*] |
```

- [ ] **Step 2: Add Routine Cards before Entry Points**

Insert after `## Program Call Map` section:

```markdown
---

## Routine Cards

Purpose: compact semantic cards for routines/procedures, especially when full
source cannot fit in context.

| Routine | Location | Called By | Calls Out | Data Touches | State Impact | Error Handling | Evidence | Coverage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [MAIN] | lines [XX-YY] | entry | [SRxxx / external] | [carrier/object] | read-only / creates / updates / deletes / external handoff / unknown | [local / propagated / none] | [EV-*] | indexed_only / deep_read / blocked |

**Open routine questions:**
- [TBD-*]: [specific source or SME question]
```

- [ ] **Step 3: Add Deep Read Windows before Entry Points**

Insert after `## Routine Cards`:

```markdown
---

## Deep Read Windows

Purpose: source windows that were read in detail to support high-risk claims.

| Window ID | Source Range | Reason Selected | Routines Covered | Claims Supported | Evidence |
| --- | --- | --- | --- | --- | --- |
| WIN-[SLUG]-01 | lines [XX-YY] | entry / state change / external call / error handling / contradiction | [routines] | [BEH-* / EX-* / DATA-*] | [EV-*] |

**Windows not deep-read:**
- [routine/range]: indexed only because [technical utility / no state impact / deferred by SME]
```

- [ ] **Step 4: Add checklist items**

In `## Review Checklist`, add:

```markdown
- [ ] Analysis Coverage & Scope honestly states whether this was standard, segmented, or large-program mode
- [ ] Routine Cards cover every routine that affects calls, data, errors, or external boundaries
- [ ] Deep Read Windows support all high-risk claims and state-changing behavior
- [ ] Indexed-only routines are either technical utilities or routed to explicit review items
- [ ] No whole-program business summary exceeds the documented coverage
```

## Task 4: Update Program Examples

**Files:**
- Modify: `skills/legacy-ibmi-program-analyzer/examples/simple-crud-rpgle/program-analysis.md`
- Modify: `skills/legacy-ibmi-program-analyzer/examples/complex-batch-job/program-analysis.md`

- [ ] **Step 1: Add standard-mode coverage to simple CRUD example**

Add after metadata:

```markdown
## Analysis Coverage & Scope

### Source Size & Strategy

| Metric | Value |
| --- | --- |
| Source Lines | 240 |
| Analysis Mode | standard |
| Mode Reason | Small program; all routines and I/O statements fit safely in context |
| Structure Index Built | yes |
| Full Source In Context | yes |
| Business Narrative Allowed | yes |

### Coverage Ledger

| Coverage Area | Count / Status | Evidence | Notes |
| --- | --- | --- | --- |
| Routines Found | 3 | EV-CRUD-001 | all routines indexed |
| Routines Deep-Read | 3 of 3 | EV-CRUD-001 | 100% |
| Routines Indexed Only | 0 | EV-CRUD-001 | none |
| External Edges Resolved | 1 of 1 | EV-CRUD-004 | external message call resolved |
| Data Touches Resolved | 4 of 4 | EV-CRUD-005 | all PF/DSPF touches resolved |
| Blocking Gaps | none | EV-CRUD-001 | no source-blocking gaps |
| Non-Blocking Gaps | none | EV-CRUD-001 | no deferred items |
```

- [ ] **Step 2: Add segmented-mode coverage to complex batch example**

Add after metadata:

```markdown
## Analysis Coverage & Scope

### Source Size & Strategy

| Metric | Value |
| --- | --- |
| Source Lines | 18,420 |
| Analysis Mode | segmented |
| Mode Reason | Source exceeds safe one-pass context; analysis used source index, routine cards, and deep-read windows |
| Structure Index Built | yes |
| Full Source In Context | no |
| Business Narrative Allowed | yes, limited to deep-read and evidence-backed areas |

### Coverage Ledger

| Coverage Area | Count / Status | Evidence | Notes |
| --- | --- | --- | --- |
| Routines Found | 42 | EV-BATCH-001 | source index derived from BEGSR/ENDSR and procedure boundaries |
| Routines Deep-Read | 18 of 42 | EV-BATCH-002 | hot path, state changers, external calls, commit/error handling |
| Routines Indexed Only | 24 | EV-BATCH-003 | technical formatting and report-layout routines |
| External Edges Resolved | 12 of 12 | EV-BATCH-004 | all CALL/CALLP targets captured |
| Data Touches Resolved | 31 of 34 | EV-BATCH-005 | three report-only payload fields left for SME review |
| Blocking Gaps | none | EV-BATCH-006 | no missing source blocks the batch flow |
| Non-Blocking Gaps | TBD-BATCH-007 | EV-BATCH-005 | confirm report-only payload labels |
```

- [ ] **Step 3: Add two routine-card rows to complex batch example**

Add under the new `## Routine Cards` section:

```markdown
| Routine | Location | Called By | Calls Out | Data Touches | State Impact | Error Handling | Evidence | Coverage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MAIN | lines 100-380 | entry | SR010, SR200, SR900 | CTLFILE, RUNLOG | updates | propagates status code | EV-BATCH-002 | deep_read |
| SR900 | lines 9200-9480 | MAIN, SR200 | WRKMSG, COMMIT | RUNLOG, ERRQ | updates / external handoff | MONITOR + message queue | EV-BATCH-006 | deep_read |
```

## Task 5: Propagate Coverage Into Flow Analysis

**Files:**
- Modify: `skills/legacy-ibmi-flow-analyzer/SKILL.md`
- Modify: `skills/legacy-ibmi-flow-analyzer/templates/flow.md`
- Modify: `skills/legacy-ibmi-flow-analyzer/references/output-contract.md`

- [ ] **Step 1: Add upstream coverage rule to flow analyzer**

In `skills/legacy-ibmi-flow-analyzer/SKILL.md`, add to stop conditions:

```markdown
- A required call edge, data flow, or error path depends on an upstream
  program routine marked `blocked` or `indexed_only` with business state
  impact → route back to `legacy-ibmi-program-analyzer`
```

- [ ] **Step 2: Add coverage propagation to flow execution**

In the `### Execution` section, add:

```markdown
- **Coverage propagation**: consume each upstream program's Analysis
  Coverage & Scope, Routine Cards, and Deep Read Windows. If the requested
  flow relies on a routine that was only indexed and that routine changes
  state, performs external handoff, handles commit/rollback, or controls
  error outcome, the flow is blocked until that routine is deep-read or SME
  waived.
```

- [ ] **Step 3: Update flow Nodes table**

In `skills/legacy-ibmi-flow-analyzer/templates/flow.md`, replace the Nodes table header with:

```markdown
| Node ID | Program (OBJ-*) | Role | Program Analysis | Coverage Status | Blocking Coverage Gaps | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| NODE-[SLUG]-01 | [PROGRAM] (OBJ-[SLUG]-[NNN]) | entry / orchestrator / worker / data-access / reporter / exit | `program-analysis-OBJ-[SLUG]-[NNN].md` | standard / segmented / large_program; approved / warning / blocked | none / [TBD-*] | [notes] |
```

- [ ] **Step 4: Add output-contract rules**

In `skills/legacy-ibmi-flow-analyzer/references/output-contract.md`, add this section near the Nodes section:

```markdown
### Program Coverage Propagation

Every flow node must carry the upstream program's coverage state. A flow cannot
use an edge, data exchange, branch, error path, or commit boundary from a routine
that is only `indexed_only` when that routine has business state impact.

Allowed outcomes:

| Upstream Coverage | Flow Action |
| --- | --- |
| `deep_read` | May use as flow evidence |
| `indexed_only` + technical utility | May use with non-blocking warning |
| `indexed_only` + state impact | Block and route back to program analyzer |
| `blocked` | Block flow analysis |
```

## Task 6: Extend Validator Checklists

**Files:**
- Modify: `skills/legacy-step-validator/references/validation-checklists.md`

- [ ] **Step 1: Update program mechanical checks**

In the Program analysis mechanical checklist, replace the required sections row with:

```markdown
| Analysis Coverage & Scope, Program Call Map (visual overview + node inventory + call tree + call edge table + reverse caller index), Routine Cards, Deep Read Windows, entry points, control flow, object dependencies, Data Touch Map, file I/O, external calls, error handling, TBDs, SME checklist sections present | 3 | blocking |
```

- [ ] **Step 2: Add program coverage checks**

Add these rows to Program analysis mechanical checks:

```markdown
| Analysis mode is one of `standard`, `segmented`, or `large_program` | 3 | blocking |
| Coverage Ledger records routines found, routines deep-read, external edges resolved, data touches resolved, blocking gaps, and non-blocking gaps | 3 | blocking |
| Segmented or large-program mode includes Routine Cards and Deep Read Windows | 3 | blocking |
```

- [ ] **Step 3: Add program semantic checks**

Add these rows to Program analysis semantic checks:

```markdown
| Whole-program summary does not claim more certainty than the coverage ledger supports | 5 | blocking |
| State-changing or external-boundary routines are not left `indexed_only` without a blocking or non-blocking review item | 4 | blocking |
| Fixed line-chunk summaries are not used as the source of business facts without routine/call/data evidence | 5 | blocking |
```

- [ ] **Step 4: Add flow coverage checks**

Add this row to Flow analysis mechanical checks:

```markdown
| Every node records upstream program coverage status and blocking coverage gaps | 3 | blocking |
```

Add this row to Flow analysis semantic checks:

```markdown
| Flow edges, data exchanges, branch decisions, error paths, and commit boundaries do not depend on `indexed_only` state-changing routines | 4 | blocking |
```

## Task 7: Update Runtime Smoke Expectations

**Files:**
- Modify: `docs/runtime-smoke-tests.md`

- [ ] **Step 1: Add large-program smoke expectation**

Add a short expectation under the program-analyzer smoke section:

```markdown
Large-program prompts should not produce a one-pass business summary. Expected
output includes Analysis Coverage & Scope, source index summary, Routine Cards,
Deep Read Windows, Program Call Map, Data Touch Map, and explicit blocking or
non-blocking gaps for any unanalyzed state-changing routine.
```

- [ ] **Step 2: Add negative smoke expectation**

Add:

```markdown
Negative large-program smoke: if a prompt asks the analyzer to summarize a
30k-line RPG program from fixed 1,000-line chunks, the expected response rejects
chunk-summary synthesis as insufficient and switches to structure-first
routine/call/data indexing.
```

## Task 8: Sync and Verify

**Files:**
- Runtime copies generated by `scripts/sync-skills.sh`

- [ ] **Step 1: Sync runtime skills**

Run: `scripts/sync-skills.sh`

Expected: runtime copies under `.claude/skills`, `.opencode/skills`, `.agents/skills`, and `.codex/skills` update from canonical `skills/`.

- [ ] **Step 2: Check sync drift**

Run: `scripts/sync-skills.sh --check`

Expected: success with no drift.

- [ ] **Step 3: Verify skill claims**

Run: `python3 scripts/verify-skill-claims.py`

Expected: success.

- [ ] **Step 4: Verify spec contract**

Run: `python3 scripts/check-spec-contract.py`

Expected: success.

- [ ] **Step 5: Check for stale old wording**

Run: `rg -n "fixed line chunks|whole-program business narrative|Full Source In Context|Routine Cards|Deep Read Windows" skills docs`

Expected: new protocol wording appears in the intended canonical and runtime files after sync; no wording instructs agents to summarize large programs from fixed line chunks.

## Self-Review

- Spec coverage: This plan implements context-safe large RPG analysis by adding a large-program reference, coverage ledger, routine cards, deep-read windows, flow coverage propagation, validator checks, and smoke expectations.
- Placeholder scan: The plan uses `TBD-*` only as a domain artifact name from the repository workflow, not as an unfinished placeholder.
- Scope check: Phase 1 intentionally avoids a full parser or graph database. A future Phase 2 may add deterministic source-index scripts if field pilots show repeated manual indexing friction.
