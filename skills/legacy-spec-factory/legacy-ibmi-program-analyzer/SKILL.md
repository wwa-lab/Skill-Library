---
name: legacy-ibmi-program-analyzer
description: Analyze individual IBM i programs (RPGLE, CLLE, COBOL) to extract control flow, file I/O, external calls, and error handling with evidence backing. Use when diving deep into one program's behavior from an approved inventory. Layer 1 (platform-specific) skill of the Legacy Spec Factory reverse chain.
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

# IBM i Legacy Program Analyzer

## Purpose

Create a detailed analysis of one IBM i program (RPGLE, CLLE, or COBOL)
documenting its RDi-style program call map, control flow, file I/O
operations, external calls, and error handling. This skill does not infer
business rules and does not generate modernization code. It produces
evidence-backed analysis ready for SME validation and downstream spec
generation.

## Inputs

Accept:

- One RPGLE, CLLE, or COBOL source file (the program to analyze)
- Optional: DDS copybook definitions (DSPF, PRTF, PF, LF) referenced by the program
- Optional: SME notes on entry points, quirks, or runtime behavior
- **Required:** Program must be referenced in an approved `01_inventory/inventory.yaml` via program ID (OBJ-*)

Stop and require clarification if:

- Program source is missing or incomplete (create a `blocked_pending_source`
  artifact or TBD routing note instead of guessing)
- Program is marked `blocked` in the inventory
- Program ID (OBJ-*) cannot be located in inventory
- Source contains raw, unredacted production data (require redaction review per `../../../docs/legacy-spec-factory/data-collection-and-redaction.md`)

## Output Contract

Produce:

- `program-analysis-<OBJ-ID>.md` per program (one file per analysis session)

Use:

- `templates/program-analysis.md` as starting point
- `references/output-contract.md` for field definitions and evidence tagging
- `references/large-program-analysis.md` for large-program, segmented, and context-window-safe analysis
- `references/control-flow-patterns.md` for language-specific pattern recognition
- `references/error-handling-taxonomy.md` for error detection
- `references/evidence-tagging.md` for evidence strength levels and tagging methodology
- `templates/evidence-tags.md` as a quick reference card for inline evidence annotation

Follow:

- `../../../docs/legacy-spec-factory/id-conventions.md` for stable IDs (OBJ-*, EV-*, TBD-*)
- `../../../docs/legacy-spec-factory/evidence-and-knowledge-taxonomy.md` for evidence strength labels
- `../../../docs/legacy-spec-factory/input-readiness-rubric.md` for input readiness scoring

Examples:

- `examples/simple-crud-rpgle/` — straightforward CRUD program, high-confidence analysis
- `examples/complex-batch-job/` — multi-subroutine batch job, moderate complexity
- `examples/incomplete-source-negative/` — negative case: missing source, TBD handling

## Step Contract

This skill is one step in the Legacy Spec Factory reverse chain. It conforms
to the canonical Step Contract shape — see
`../legacy-step-contract/SKILL.md` and
`../legacy-step-contract/references/step-contract.md` for the full
field-level rules. The summary below is normative for this skill.

### Input

- **Required**: one RPGLE / CLLE / COBOL source program; the program's
  `OBJ-*` ID located in an `approved` (or
  `approved_with_non_blocking_tbd`) `01_inventory/inventory.yaml`.
- **Optional**: DDS copybook source (DSPF, PRTF, PF, LF) for files the
  program touches; SME notes on entry points, quirks, or runtime behavior.
- **Input readiness scoring**:
  - `0-5 blocked`: program source missing/incomplete, `OBJ-*` not found,
    inventory status blocked, or evidence authorization unresolved.
  - `6 minimum_pass`: one current program source and its approved inventory
    `OBJ-*` link are present; missing copybooks/runtime details become TBDs.
  - `7-8 usable`: referenced DDS/copybooks and object metadata are available
    for most file and display/report interactions.
  - `9-10 strong`: runtime logs, screen/report samples, SME notes, known
    edge cases, and parameter/interface notes are also supplied.
  - Missing runtime samples or SME notes does not block static program
    analysis; it limits confidence for business meaning and exception realism.
- **Readiness checks**: Inventory Completeness Gate passing; program is
  not marked `blocked` in inventory; source is current production (tier 1)
  rather than archival; evidence authorization is resolved.
- **Stop conditions**: source missing or incomplete; program marked
  `blocked` in inventory; `OBJ-*` not found in inventory; raw unredacted
  production data present.

### Execution

- **Procedure**: see the Workflow section below (10 ordered steps).
- **Large-program mode**: when source is greater than 10,000 lines,
  contains more than 25 routines, contains more than 20 external calls,
  or cannot safely fit in context with evidence windows, use
  `references/large-program-analysis.md`. Do not produce whole-program
  business narrative until the source index, routine cards, Program Call
  Map, Data Touch Map, and coverage ledger exist.
- **Allowed inference**: control flow extracted from EXSR/CALL/PERFORM;
  file I/O from F-spec and I/O statements; error paths from MONITOR/
  MONMSG/ON-ERROR; pattern-based labeling tagged `strongly_inferred` or
  `medium_confidence` with explicit notes.
- **Forbidden assumptions**: inventing subroutines, file access beyond
  what I/O statements show, business meaning from field names, external
  call parameters absent from source or copybooks, error codes not
  explicitly caught or returned; reading non-redacted evidence.
- **TBD handling**: missing DDS → `TBD: pending_source`; undefined
  subroutine reference → `TBD: pending_source`; unclear error path →
  `TBD: pending_sme_judgment`; non-blocking gaps tagged `non_blocking`.

### Output

- **Canonical artifact**: `program-analysis-<OBJ-ID>.md` (one per program).
- **Required sections**: `Metadata`, `Analysis Coverage & Scope`,
  `Program Call Map`, `Routine Cards`, `Deep Read Windows`,
  `Entry Points & Parameters`, `Object Dependencies`, `Data Touch Map`,
  `Control Flow`, `File I/O`, `External Calls`, `Error Handling`,
  `TBDs & Blocking Status`, `Review Checklist`.
- **Required IDs**: reuses `OBJ-*` and `EV-*` from inventory; mints
  program-local `BEH-*`, `EX-*`, and `TBD-*`. Does not mint `BR-*`,
  `CAP-*`, `DEC-*`.
- **Handoff status**: `status: draft` until SME review; `approved` or
  `approved_with_non_blocking_tbd` is required before
  `legacy-ibmi-flow-analyzer` runs against the chain that includes this
  program.

### Validation

- **Mechanical**: every non-trivial behavior has ≥1 `EV-*` link; every
  call/object reference resolves against inventory; every TBD has a
  blocking-status tag; required sections all present.
- **AI semantic**: behaviors are consistent with the linked source lines;
  no invented subroutines, fields, files, or error codes; evidence
  strength not overstated (no `weakly_inferred` posing as
  `confirmed_from_code`); flow header (if present) reconciled against
  the code-derived program call map.
- **SME / human approval**: SME signs entry points, parameter contracts,
  file I/O semantics, external interface contracts, and error handling
  realism. Required when the program affects money, inventory,
  compliance, or customer status; recommended otherwise.
- **Blocking conditions**: any `BEH-*` without evidence; any invented
  IBM i fact; any unresolved `pending_source` TBD on a section that is
  load-bearing for the next flow analysis; SME absence when SME is
  required by the program's risk class.

Emit a Step Validation Report (see
`../legacy-step-contract/templates/step-validation-report.md`) with
status `pass`, `pass_with_warnings`, or `blocked` when reporting upward
to the orchestrator.

## Workflow

1. **Size & Structure Preflight**
   - Count approximate source lines, routine definitions, external calls,
     and object dependencies before writing business summary prose
   - Select analysis mode: `standard`, `segmented`, or `large_program`
   - For `segmented` or `large_program`, build the structure index before
     any business summary prose
   - Create Analysis Coverage & Scope and initialize the coverage ledger
   - Prevent claims of complete understanding until coverage supports
     them with indexed routines, deep-read windows, resolved call/data
     edges, and explicit gaps

2. **Select Program & Verify Inventory**
   - Accept program ID (OBJ-*) from approved `01_inventory/inventory.yaml`
   - Confirm program name, type (RPGLE / CLLE / COBOL), and library
   - Stop if program is marked `blocked` or inventory is not approved
   - Document source location and collection date

3. **Extract Entry Points & Parameters**
   - Identify main entry point (program parameter list, return value or status code)
   - Identify callable sub-procedures:
     - RPGLE procedures: Fixed-form `P ... B` / `P ... E` or free-form `dcl-proc` / `end-proc`; both callable via CALL statement
     - RPGLE subroutines: `BEGSR` / `ENDSR` blocks (internal subroutines, callable only from within same program)
     - CLLE: `SUBR` label blocks and `CALLSUBR` invocations (internal subroutines); external procedures via CALL
     - COBOL: ENTRY statements, PERFORM … UNTIL / VARYING
   - Document parameter types, expected ranges, and direction (input/output/both)
   - Tag with evidence: `confirmed_from_code` (from source headers or RPGLE specifications)
   - Create TBD if parameter contract is undocumented or unclear

4. **Trace Main Control Flow**
   - Document procedure call sequence (what calls what, in what order)
   - Identify conditional branching:
     - RPGLE: IF, SELECT, indicator-driven branching
     - CLLE: IF, ELSE, GOTO
     - COBOL: IF, EVALUATE, PERFORM … UNTIL
   - Identify loops and exit conditions (DO, DOWHILE, PERFORM, VARYING)
   - Document handled vs. unhandled paths
   - Tag each non-trivial control structure: `confirmed_from_code` or `medium_confidence` if inferred
   - Create TBD for unclear program flow (missing subroutines, undefined labels)

5. **Build Program Call Map**
   - Treat the call map as the default entry view for every program,
     regardless of size. It should resemble an IBM RDi call-hierarchy
     view: routines and external boundaries connected by call edges,
     not a statement-level flowchart.
   - **First, look for a source-level flow header** at the top of the program. Many IBM i shops embed an ASCII tree comment like:
     ```
     Main line                Main flow control
     |-- SR990                First time initialization
     |-- SR100                Card validation
     |    |-- SR110           Currency conversion
     |    |    |-- SR111      Convert transaction amount
     ```
     If present, capture it verbatim — it is the program author's documented intent (tier 3 evidence per `../../../docs/legacy-spec-factory/code-as-ground-truth.md`). Useful as a navigation aid, **not authoritative** when it disagrees with actual EXSR/CALL statements.
   - **Independently derive a program call map from code** by scanning
     for EXSR / CALLP / CALL / PERFORM / CALLPRC statements and
     BEGSR-ENDSR / BEGPR-ENDPR / paragraph definitions.
   - **Compare header vs. code-derived graph:**
     - If they match → tag `confirmed_from_code` (with source-level flow header as evidence)
     - If header exists but code differs → create TBD (comment drift, dead code, or missing subroutine)
     - If no header exists → use code-derived graph, tag `confirmed_from_code` (from EXSR/CALL/PERFORM statements)
   - Produce five views (see `references/output-contract.md`):
     - **Visual overview** (RDi-style orientation graph; compact by design)
     - **Node inventory** (mainline, internal routines, procedures, external programs, APIs, queues, services)
     - **Call tree** (matches the IBM i flow-header convention)
     - **Call edge table** (from, to, line, call condition such as "in DOWHILE loop" or "only if approved")
     - **Reverse caller index** (for each node, who calls it)
   - Identify hub/common candidates and orphaned routines. A hub/common
     label is structural only; do not promote it into a business service
     or modernization boundary without flow/module evidence and SME
     confirmation.

6. **List Object Dependencies (flat reference inventory)**
   - Match the shop's `F5-OBJREF TREE` output format: enumerate **every external object** referenced by the program, regardless of how it is used.
   - Object types to cover:
     - Files: PF (physical), LF (logical), DSPF (display), PRTF (printer)
     - Data: \*DTAARA (data area), \*DTAQ (data queue), \*MSGF (message file)
     - Programs: \*PGM (called program), \*SRVPGM (bound service program)
     - Source-level: Copybooks / `/COPY` directives, data-structure includes
   - Capture columns: object name, type, version (if shop tracks one), description, inventory ID (OBJ-\*), evidence
   - Cross-reference each entry against `01_inventory/inventory.yaml`:
     - If a matching OBJ-\* exists → link it
     - If not → create TBD: inventory gap (the inventory missed this object)
   - This section is the **flat parent list**; deeper per-object analysis happens in steps 7 (Data Touch Map + File I/O) and 8 (External Calls).
   - Tag: `confirmed_from_code` (visible in F-spec, D-spec, /COPY, or CALL statement)

7. **Document Data Touch Map & File I/O**
   - Build a program-local **Data Touch Map** before the detailed File
     I/O table. This is the data companion to the Program Call Map: it
     shows which routines touch which data carriers and where state
     enters, changes, leaves, or persists.
   - Track object / record / critical-field level movement. Do **not**
     enumerate every temporary RPG work variable.
   - Critical fields include money/amount fields, account/customer IDs,
     inventory quantities, approval/decline decisions, posting flags,
     status fields, return codes, error codes, audit IDs, and external
     message payload fields.
   - For every data carrier, capture:
     - carrier/object (PF, LF, DSPF, PRTF, `*DTAARA`, `*DTAQ`, `*MSGQ`,
       CALL parameter list, copybook/data structure, IFS file)
     - routine/procedure touching it
     - operation (read, write, update, delete, send, receive, parameter
       in/out/inout)
     - key/payload fields
     - state impact (`read-only`, `creates`, `updates`, `deletes`,
       `async send`, `async receive`, `external handoff`)
     - evidence and TBDs for unclear payload structure or direction
   - For each file from step 6 (PF / LF / DSPF / PRTF), classify operations:
     - Sequential read: READ (next record), READP / READPE (read previous)
     - Random read: SETLL (set lower limit), READE (read equal), CHAIN (random access)
     - Write operations: WRITE (add new record), UPDATE (modify record), DELETE
     - Display file: EXFMT (format + read interaction with DSPF for menus, input screens)
     - Embedded SQL / SQLRPGLE: EXEC SQL blocks, cursor operations, SQLCODE / SQLSTATE error handling
     - Note key fields used in each operation (e.g., CHAIN on CUSTID)
   - Reference file definitions from inventory via evidence ID (EV-\*)
   - Tag evidence: `confirmed_from_code` (from file specifications or I/O statements)
   - Create TBD if DDS is missing, key field unclear, or SQL schema is not documented

8. **Identify External Calls**
   - List all external program calls:
     - RPGLE: CALL, CALLP (procedure call)
     - CLLE: CALL, CALLPRC
     - COBOL: CALL, CICS, MQ, REST
   - List external service program calls (binding)
   - List external interfaces: IFS, HTTP, message queues, data queues
   - Document parameter contract if visible in source (call statement, copybook)
   - Tag: `confirmed_from_code` (source statement visible) or `needs_sme_review` (undocumented)
   - Create TBD if external interface is unknown or network-dependent

9. **Document Error Handling**
   - List monitored errors:
     - RPGLE: MONITOR / ON-ERROR block, escape messages
     - CLLE: MONMSG (monitor message)
     - COBOL: ON ERROR, error flag checking
   - Document error codes and recovery paths (retry, log, return error)
   - Document logged errors or message writes (DSPLY, message queue, spool)
   - Document unhandled exceptions (crash, abort)
   - Tag: `confirmed_from_code` (explicit error block) or `strongly_inferred` (pattern-based)
   - Create TBD if error handling is unclear or context-dependent

10. **Prepare for SME Review**
   - Consolidate all TBDs created in steps 3–9 with clear blocking status:
     - `pending_source` — missing DDS, incomplete source
     - `pending_sme_judgment` — behavior unclear from source alone
     - `non_blocking` — known gaps that don't affect downstream analysis
   - Generate review checklist for SME validation
   - Mark analysis as `blocked_pending_source` when missing or incomplete
     source prevents safe analysis; otherwise mark as `draft` (ready for
     review)
   - Gate: Analysis artifact is ready when every non-TBD behavior has an evidence_strength of `confirmed_from_code`, `strongly_inferred`, or `medium_confidence` (the latter two only when an SME review note is attached)

## Workflow State Write-Back

At the end of a program-analysis run, update
`<project-root>/workflow-state.yaml` per
[`docs/workflow-state-contract.md`](../../../docs/legacy-spec-factory/workflow-state-contract.md).
Template: [`skills/legacy-modernization-orchestrator/references/state-writeback-snippet.md`](../legacy-modernization-orchestrator/references/state-writeback-snippet.md).

**Stage this skill produces:**

- `3b Program Analysis Done` when **every** in-scope program in
  `inventory.yaml` has an approved `program-analysis.md`
- `3a Program Analysis In Progress` when one or more in-scope programs
  still lack an analysis

**Last artifact path pattern:**
`02_programs/<MODULE-SLUG>/<OBJ-PROGRAM>/program-analysis.md`

**Writes per run:**

1. Overwrite `capabilities[<CAP-* from current_focus>]` with stage id,
   the path of the analysis you just saved, `last_skill:
   legacy-ibmi-program-analyzer`, and blocking IDs (`tbds`, `sme_pending`
   for any money / inventory / compliance branch awaiting SME).
2. Append one `history[]` entry with `note` naming the program analyzed
   (e.g. `"analyzed ORDENTR"`).
3. Overwrite `project.last_updated_at` / `project.last_updated_by`.

Never touch `current_focus`, other capabilities' entries, or past
`history[]` rows. A re-run on the same program is allowed; a re-run that
would lower `stage_id` requires the orchestrator's Rollback Protocol.

## Anti-Hallucination Rules

**Code is ground truth.** See `../../../docs/legacy-spec-factory/code-as-ground-truth.md` for
the full principle. When source code disagrees with comments,
source-level flow headers, shop tool outputs, or SME recollection,
**the code wins** for behavioral claims. The disagreement itself
becomes a TBD asking the SME to confirm whether the secondary source
is stale or the code drifted from intent — but until then, the
analysis describes what the code actually does.

**Do NOT invent:**

- **Subroutine entry points** not directly visible in source (no inventing BEGPR blocks or subroutine labels)
- **File access** beyond what I/O statements (SETLL, READE, CHAIN, WRITE, UPDATE, DELETE) directly show
- **Business logic** from field names alone (e.g., a field named CREDLIMIT does not explain *why* the limit exists or how it's used)
- **External call parameters** if not visible in source headers, copybooks, or CALL statements
- **Error codes** if not explicitly caught or returned

**Instead:**

- If DDS is missing, create `TBD-<SLUG>-NNN: Confirm field meaning from [file-name] DDS`
- If subroutine is referenced but undefined, create `TBD-<SLUG>-NNN: Locate subroutine definition [name]`
- If error handling is unclear, tag `needs_sme_review` instead of inventing error recovery
- If external interface parameters are unknown, create `TBD-<SLUG>-NNN: Confirm parameter contract for [program-name]`

**Evidence minimum:**

- Every non-trivial behavior must have ≥1 evidence link, even if evidence_strength is low
- Do not document "likely" behavior without explicit evidence tag
- TBD questions count as evidence of a gap, not coverage

## SME Review Questions

The generated `program-analysis-<OBJ-ID>.md` must include a checklist. Before approval, SME must validate:

- [ ] Entry points are correct and complete (no missing callable subroutines)
- [ ] Parameter contracts match actual usage (no invented parameters)
- [ ] Data Touch Map captures critical carriers, keys, payloads, and state impacts
- [ ] File I/O matches job design (no hallucinated key fields or unobserved operations)
- [ ] External calls match system interfaces (especially for undocumented calls)
- [ ] Error handling aligns with production reliability requirements
- [ ] TBDs are non-blocking or properly flagged for follow-up
- [ ] Analysis contains no invented subroutines or undocumented file access

## Runtime Portability

Canonical source: `skills/legacy-ibmi-program-analyzer/SKILL.md`

Runtime adapters are synced via `scripts/sync-skills.sh`:

- Codex: `.codex/skills/legacy-ibmi-program-analyzer/SKILL.md`
- Claude Code: `.claude/skills/legacy-ibmi-program-analyzer/SKILL.md`
- OpenCode: `.opencode/skills/legacy-ibmi-program-analyzer/SKILL.md`

No runtime-specific assumptions are embedded in the canonical version.

## Version History

- v0.1.0 (2026-05-14): Initial release
  - 10-step workflow for RPGLE, CLLE, COBOL (with Program Call Map extraction and flat object-dependency listing)
  - Entry point extraction, control flow tracing, file I/O documentation
  - External call and error handling detection
  - Evidence tagging and TBD handling
  - SME review checklist
  - Positive and negative examples
