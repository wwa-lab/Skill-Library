# Workflow State Contract

`workflow-state.yaml` is the Legacy Spec Factory's cross-session "save game".
It records where each capability is in the reverse chain so that the
orchestrator (and any downstream skill, on any LLM, in any new session) can
resume work without re-deriving stage from scratch.

This document is the authoritative contract for **who reads it, who writes
it, and what each writer is allowed to change**. Every skill in the reverse
chain MUST conform.

The canonical template lives at
`skills/legacy-modernization-orchestrator/templates/workflow-state.yaml`.

## Location

- File: `docs/<project-name>/workflow-state.yaml`
- One per project. A single repository may contain **many** projects under
  `docs/`, each fully self-contained.
- `<project-name>` follows the PPCR convention:
  `<PPCR-Number>-<short-description>` (e.g. `XXX260004-demo`,
  `XXX260123-credit-check`). Allowed characters: `[A-Za-z0-9-]`. Must start
  alphanumeric. No spaces, dots, slashes, or other punctuation.
- Safe to commit. Contains only IDs, stage labels, artifact paths, and a
  short audit trail — no source code, no unredacted evidence, no PII.

## Project Root and Path Resolution

Every project's artifacts live under a single root directory:

```
<repo-root>/
  docs/
    XXX260004-demo/                      <-- project.root
      workflow-state.yaml
      01_inventory/inventory.yaml
      02_programs/<MODULE>/<OBJ>/program-analysis.md
      03_flows/<MODULE>/flow-*.md
      04_modules/<MODULE>/...
      05_specs/<CAP-*>/spec.yaml
      06_quality/<CAP-*>/...
      07_runtime-evidence/...
      08_business-understanding/<CAP-*>/...
      09_forward-sdlc/<CAP-*>/...
      evidence/redacted/...
    XXX260123-credit-check/              <-- another project, fully isolated
      workflow-state.yaml
      ...
```

- `project.root` is the prefix every artifact path in this state file is
  resolved against. Default: `docs/<project.name>/`.
- All `last_artifact`, `next_artifact`, `history[].artifact`, and
  `stage_card` paths in this file are **relative to `project.root`** (with
  the single exception of `stage_card`, which is repo-root-relative because
  it points into the orchestrator skill).
- Directories under the project root are **created on demand** — only when
  a skill first writes into them. Do NOT pre-create empty directories
  (they pollute git history).
- Cross-project references are forbidden. A `last_artifact` in project A
  must NOT point into project B's tree.

## Read / Write Roles

| Role | Reads | Writes |
| --- | --- | --- |
| `legacy-modernization-orchestrator` | every turn (Step 0) | every turn (Step 8) — overwrites `current_focus`, overwrites the matching `capabilities[]` entry, appends one `history[]` entry |
| Any Layer 1 / Layer 2 skill (inventory, program / flow / module analyzer, spec-writer, BRD writer, handoff packager, etc.) | start of run (to confirm stage) | end of run — overwrites its `capabilities[]` entry, appends one `history[]` entry; does **not** touch `current_focus` unless explicitly invoked as a router |
| Governance / verification skills (step-validator, traceability-packager, runtime-matrix-tester, SME review facilitator) | start of run | append one `history[]` entry only (no `current_focus`, no `capabilities[]` mutation) |
| User (manual edit) | anytime | discouraged — prefer running the orchestrator. If manually edited, set `last_updated_by: manual` |

## Field-Level Write Rules

### `version`

- Always `1` for this schema generation.
- Never change without bumping the contract doc and notifying every
  downstream skill.

### `project`

- `name`: set on first write, never overwritten after. Must match
  `^[A-Za-z0-9][A-Za-z0-9-]*$` (PPCR convention).
- `root`: set on first write to `docs/<name>/`, never overwritten after.
  Every artifact path in this file is interpreted relative to this root.
- `started_at`: set on first write, never overwritten after.
- `last_updated_at`, `last_updated_by`: overwritten by every writer.

### `current_focus`

- **Owner:** `legacy-modernization-orchestrator` only.
- Overwritten on every orchestrator turn.
- Reflects the most recent **routing decision**, not the most recent skill
  completion.
- Downstream skills MUST NOT touch this block.

### `capabilities[]`

- Keyed by `id` (`CAP-*`). One entry per capability in flight.
- A writer MAY overwrite the entry whose `id` matches its current scope.
- A writer MUST NOT delete an entry. To retire a capability, set
  `archived: true`.
- A writer MUST NOT touch other capabilities' entries.
- `stage_id` must come verbatim from
  `skills/legacy-modernization-orchestrator/references/stage-identification.md`.
- `last_artifact` must be a full path including filename.
- `blocking.tbds`, `blocking.sme_pending`, `blocking.gates` are flat lists
  of IDs / names. Empty list means "nothing blocking from my perspective"
  — not "I didn't check".

### `history[]`

- **Append-only.** Never edit or remove entries.
- Newest entry at the bottom.
- Required fields per entry: `at` (ISO 8601), `skill`, `capability_id` (or
  `null` when not capability-scoped), `stage_after`, `artifact` (or `null`
  if no artifact was produced this turn).
- Optional `note` for one-line context (max ~120 chars).

## Focus Switching

`current_focus` may be reassigned at any turn (the user switches from
`CAP-A` to `CAP-B`, or hands an inherited repo to a new operator).

Rules:

- Only the orchestrator may overwrite `current_focus`. Downstream skills
  inherit it as scope; they do not change it.
- A switch MUST NOT mutate the prior focus's `capabilities[]` entry. The
  prior focus stays at whatever `stage_id` it was last left at.
- Every switch appends one `history[]` entry with
  `note: "focus switched from <old CAP-*> to <new CAP-*>"`.
- A switch to a `CAP-*` / `MODULE-*` that does NOT yet exist in
  `capabilities[]` is a `new`, not a `switched`. Create the entry first.
- The orchestrator's focus-resolution algorithm lives in
  `skills/legacy-modernization-orchestrator/references/focus-selection.md`.
  Other skills do not implement focus detection — they receive the
  resolved focus from the orchestrator.

## Rollback

A rollback is a controlled backward move within one capability — for
example, the SME rejects an approved flow and the team needs to redo flow
analysis even though module analysis is already complete.

Rules:

- The new `stage_id` MUST be strictly earlier than the current `stage_id`
  for that capability. Forward moves are not rollbacks.
- The rollback target MUST have been previously reached (must appear in
  `history[]` for this capability). Rolling back to a never-reached stage
  is `new`, not rollback.
- The downstream artifacts (anything later than the rollback target) MUST
  NOT be deleted. They remain as evidence of the previous attempt and
  must be re-validated after the rolled-back stage's output changes.
- Every rollback appends one `history[]` entry with
  `note: "rollback from <previous stage_id> to <target stage_id>: <reason>"`.
- The orchestrator MUST surface to the user that later artifacts need
  re-validation.

## Scan Mode (No Focus Set, Artifacts Exist)

When `workflow-state.yaml` has no `current_focus` (first time on this
repo, lost state, inherited repo) but artifacts already exist, the
orchestrator runs scan mode.

Rules:

- The orchestrator MUST present a picker before routing. It must NOT
  silently pick the "most recent" or "most downstream" capability.
- If only one capability is in flight, the picker still appears — the user
  may want to start a different one.
- After the user picks, the orchestrator re-enters focus resolution
  treating the pick as a named target.
- Scan results MUST come from artifact paths listed in
  `skills/legacy-modernization-orchestrator/references/focus-selection.md`
  → "Scan Mode → Sources to scan". Never infer capabilities from prose,
  filenames outside that table, or LLM intuition.

## Conflict Resolution

- Two skills writing to the same `capabilities[]` entry in close succession:
  last writer wins for `capabilities[]`; both append to `history[]`.
- A skill cannot write a `stage_id` that is **earlier** than the
  previously-recorded `stage_id` for the same capability unless it also
  appends a `history[]` entry with `note: "rolled back: <reason>"`.
- A skill MUST NOT advance `stage_id` past a gate that is still in
  `current_focus.open_gates`.

## When State File Is Missing

- The orchestrator first scans `docs/*/workflow-state.yaml` to enumerate
  existing projects.
- If no project name appears in the user message and no projects exist,
  the orchestrator MUST prompt for one (PPCR convention).
- Once a project name is resolved, the orchestrator emits a populated
  `docs/<name>/workflow-state.yaml` based on whatever artifacts the user
  already has at that path, and asks the user to commit it.
- The orchestrator MUST NOT silently proceed without resolving and
  confirming the project name.
- Directories under the project root are created on demand by downstream
  skills as they write artifacts, never pre-created empty.

## When State File Disagrees With Artifacts

- Artifacts are the source of truth for stage. The state file is a
  convenience cache.
- If `workflow-state.yaml` says `8c Spec Approved` but
  `05_specs/CAP-*/spec.yaml.status` is `draft`, the orchestrator MUST trust
  the artifact, rewrite the state, and append a `history[]` entry with
  `note: "state corrected from artifact"`.

## Why This Contract Exists

- Stateless orchestration forces every turn to re-derive maturity from
  scratch — slow, brittle, and prone to LLM misclassification.
- A small, append-friendly state file lets a weaker LLM resume in one
  read, lets the user audit progress in one file, and lets any skill
  participate as a peer in the chain.

## Version History

- v1.2 (2026-05-16): Added `project.root` field and PPCR-style project
  naming convention. All artifact paths in state are now relative to
  `project.root` (default `docs/<name>/`), enabling many projects per
  repo with full isolation. Directories created on demand only.
- v1.1 (2026-05-16): Added Focus Switching, Rollback, and Scan Mode
  sections to cover mid-chain entry, capability switching, and inherited
  repos. Algorithm details live in
  `skills/legacy-modernization-orchestrator/references/focus-selection.md`;
  this contract defines the cross-skill rules every writer must respect.
- v1 (2026-05-16): Initial contract. Read / write roles, field-level rules,
  conflict resolution, missing-file behavior, artifact-truth rule.
