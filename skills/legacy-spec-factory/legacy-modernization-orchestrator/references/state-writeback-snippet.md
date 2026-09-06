# Workflow State Write-Back Snippet (for downstream skills)

Every Layer 1 / Layer 2 skill that produces a tracked artifact MUST update
`<repo-root>/docs/<project-name>/workflow-state.yaml` at the end of its
run so the orchestrator (and any peer skill) can resume the chain without
re-deriving stage from artifacts.

This file is the canonical template. Each downstream SKILL.md cites it and
fills in the skill-specific values (`stage_id`, `last_artifact`,
`last_skill`).

## Path conventions

- The state file lives at `docs/<project-name>/workflow-state.yaml`. The
  project name follows the PPCR convention `^[A-Za-z0-9][A-Za-z0-9-]*$`
  (e.g. `XXX260004-demo`).
- `project.root = docs/<project-name>/` is the prefix for every artifact
  path in this file. All `last_artifact`, `next_artifact`, and
  `history[].artifact` values are **relative to `project.root`**, not to
  the repository root.
- Downstream skills that resolve the orchestrator-supplied `current_focus`
  receive paths already relative to `project.root`. When saving artifacts
  to disk, prepend `project.root` to write at the right location.
- Create directories on demand. NEVER pre-create empty stage folders.

The authoritative contract — including write ownership, conflict resolution,
focus switching, rollback, and scan rules — lives at
[`docs/workflow-state-contract.md`](../../../docs/workflow-state-contract.md).
This snippet is the operational copy.

## When to write

Write at the very end of the skill's run, **after** the artifact is saved
to disk and **after** any SME-review status field on the artifact has been
set. If the run is aborted (gate blocked, missing input, SME rejected),
still append a `history[]` entry recording the outcome — but do NOT advance
`stage_id` on the `capabilities[]` entry.

## What to write

Three changes per run. Two overwrites + one append.

### 1. Overwrite the matching `capabilities[]` entry

Locate the entry whose `id` matches your current capability scope (taken
from `current_focus.capability_id`, set by the orchestrator at Step 0.5).
If it does not exist yet (a `new` outcome), append it.

```yaml
capabilities:
  - id: <CAP-* — from current_focus>
    module_slug: <MODULE-SLUG — from current_focus>
    stage_id: "<exact stage id this skill produces — see table in your SKILL.md>"
    last_artifact: <full path to the artifact you just saved>
    last_skill: <your skill name, e.g. legacy-ibmi-flow-analyzer>
    last_updated: <YYYY-MM-DD>
    blocking:
      tbds: [<TBD-* IDs still open in your artifact>]
      sme_pending: [<rule / view / row IDs awaiting SME confirmation>]
      gates: [<gate names still blocking advancement, e.g. "evidence_approval">]
    archived: false
```

Rules:

- `stage_id` MUST come verbatim from
  [`references/stage-identification.md`](stage-identification.md). Each
  downstream SKILL.md lists the exact id(s) its skill can produce.
- A partial run produces an earlier stage id (`3a`, `3c`, `3e`, `8a`) than
  a complete run (`3b`, `3d`, `3f`, `8c`).
- Empty `blocking.*` lists mean "nothing blocking from my perspective" —
  not "I didn't check". Be honest.
- NEVER touch other capabilities' entries. Overwrite only your own.
- NEVER delete an entry. To retire a capability, set `archived: true`.

### 2. Append one `history[]` entry

```yaml
history:
  # ... older entries above (never edit)
  - at: <ISO 8601 timestamp>
    skill: <your skill name>
    capability_id: <CAP-* | null>
    stage_after: <stage_id you just wrote, or the previous one if the run aborted>
    artifact: <full path to the artifact, or null if no artifact was produced>
    note: <one-line, ~120 chars max: outcome, blocked reason, or SME note>
```

Rules:

- Append-only. Newest entry at the bottom. NEVER edit or remove older
  entries.
- `at` is UTC ISO 8601 (e.g. `2026-05-16T14:30:00Z`).
- If you aborted, set `stage_after` to the **prior** `stage_id` for this
  capability and explain in `note`.

### 3. Update `project.last_updated_at` / `project.last_updated_by`

Overwrite both. Use today's date and your skill name.

## What NOT to write

- `current_focus` — owned solely by the orchestrator. Do not touch.
- Other capabilities' entries. Overwrite only your own.
- `version` — bumped only when the contract changes.
- Past `history[]` entries. Append-only.

## Backward Moves (Skill Re-Run)

If your skill re-runs on a capability that already reached a later stage
(e.g. the user invoked you again because of an SME rejection), do not
silently lower `stage_id` on `capabilities[]`. This is a **rollback** and
must be initiated by the orchestrator's Rollback Protocol, not by a
downstream skill writing a lower stage. Surface the situation in your run
output and ask the orchestrator (or user) to invoke rollback explicitly.

The append to `history[]` is still allowed and required, with
`note: "re-run requested but stage_id not lowered — orchestrator rollback needed"`.

## Missing State File

If `workflow-state.yaml` does not exist when your skill runs:

1. Create it from
   [`skills/legacy-modernization-orchestrator/templates/workflow-state.yaml`](../templates/workflow-state.yaml).
2. Populate `project.*`, one `capabilities[]` entry for your current
   capability, and one `history[]` entry for this run.
3. Leave `current_focus` empty (`null` fields) — only the orchestrator may
   set it.
4. Tell the user (in your skill's prose output) that the file was created
   and should be committed.

## Conflict With Existing State

If your skill's view of the artifact disagrees with `workflow-state.yaml`
(e.g. state says `8c Spec Approved` but `spec.yaml.status: draft`):

1. Trust the artifact.
2. Overwrite the `capabilities[]` entry to match the artifact.
3. Append a `history[]` entry with
   `note: "state corrected from artifact"`.

## Quick Reference Per Skill

| Skill | stage_id on full run | last_artifact path pattern |
| --- | --- | --- |
| `legacy-ibmi-evidence-intake` | `1 Evidence Ready` | `evidence/redacted/evidence-manifest.yaml` |
| `legacy-ibmi-inventory` | `2c Inventory Done` | `01_inventory/inventory.yaml` |
| `legacy-ibmi-program-analyzer` | `3b Program Analysis Done` (or `3a` if partial) | `02_programs/<MODULE>/<OBJ>/program-analysis.md` |
| `legacy-ibmi-flow-analyzer` | `3d Flow Analysis Done` (or `3c` if partial) | `03_flows/<MODULE>/flow-<slug>.md` |
| `legacy-ibmi-module-analyzer` | `3f Module Analysis Done` (or `3e` if partial) | `04_modules/<MODULE>/module-overview.md` |
| `legacy-brd-writer` | (does not advance numeric stage; records BRD Review Gate status) | `05_brds/<CAP-*>/brd.md` |
| `legacy-spec-writer` | `8c Spec Approved` / `8b Spec In Review` / `8a Spec Drafted` (matches `spec.yaml.status`) | `05_specs/<CAP-*>/spec.yaml` |
| `legacy-brd-to-sdd-handoff` | `10 Forward Handoff Ready` | `09_forward-sdlc/<CAP-*>/handoff-bundle.yaml` |
| `legacy-golden-master-test-planner` | `9 Equivalence Pack Ready` | `06_quality/<CAP-*>/golden-master-tests.md` |
| `legacy-ibmi-runtime-evidence-miner` | `5 Runtime Evidence Mined` | `07_runtime-evidence/runtime-evidence.jsonl` |
| `legacy-ibmi-batch-digest` | (does not advance stage; supplemental) | `02_programs/<MODULE>/programs-batch-digest.md` |

Skills not in this table (`legacy-step-validator`,
`legacy-traceability-packager`, `legacy-sme-review-facilitator`,
`legacy-runtime-matrix-tester`, `legacy-step-contract`,
`legacy-ibmi-screen-report-analyzer`,
`legacy-ibmi-data-model-analyzer`,
`legacy-modernization-decision-writer`) — plus `legacy-brd-writer` and
`legacy-ibmi-batch-digest` which ARE in the table but are also history-only — are
governance / supplemental: **append `history[]` only, do not advance
`stage_id`**. Some may make scoped edits to `capabilities[<CAP-*>].blocking.*`
(e.g. `legacy-sme-review-facilitator` updates `sme_pending`,
`legacy-traceability-packager` may add to `gates`) — those exceptions are
documented in each skill's own SKILL.md.

Validate any `workflow-state.yaml` against this contract with:

```bash
python3 scripts/check-workflow-state.py [<path-to-workflow-state.yaml>]
```
