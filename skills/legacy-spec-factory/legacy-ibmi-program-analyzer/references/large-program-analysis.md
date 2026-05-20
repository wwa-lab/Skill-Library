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
thresholds but still has dense call/data dependencies. Segmented mode is a
structure-first mode for medium-sized or dense programs where the full source
may fit, but safe analysis still requires routine/call/data segmentation.

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
| Coverage | `indexed_only`, `deep_read`, or `blocked` |
| Open Questions | Source gaps, SME questions, or contradiction references |

SME confirmation belongs in evidence or review fields, not the coverage field.

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
understanding. It is a required output subsection in `Analysis Coverage &
Scope`, not merely an internal note.

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
