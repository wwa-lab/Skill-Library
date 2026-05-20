# Multi-User Collaboration

How two or more operators can work on the same Legacy Spec Factory repo
without stepping on each other's `workflow-state.yaml`, artifacts, and
SME decisions.

## Quick rules

1. **One operator per project at a time** is the safest default. Use the
   PPCR project boundary (`docs/<project>/`) as the unit of ownership —
   different operators take different projects.
2. **Coordinate via the picker, not via assumptions.** If you must share
   one project, `git pull` before every orchestrator turn, and run
   `python3 scripts/list-projects.py` to see whose state is current.
3. **Treat `workflow-state.yaml` as merge-aware**, never as a free-for-all
   YAML file. See [Merge Strategy](#merge-strategy) below for the per-key
   rule set.
4. **Artifacts under stage folders are append/edit-only** by their owning
   skill. Two operators editing the same `program-analysis.md`
   simultaneously is the same hazard as in any codebase — coordinate via
   normal git review.

## When conflicts are most likely

- Two operators run the orchestrator on the same project within minutes
  → both write `current_focus` + `history[]`. Merge needed.
- Two operators run **different downstream skills** on different
  capabilities in the same project → both overwrite a different
  `capabilities[]` entry and append `history[]`. Trivially mergeable per
  the rules below.
- Two operators run the **same** downstream skill on the **same**
  capability → genuine conflict; the later run should incorporate the
  earlier run's findings rather than overwrite them.

## Merge Strategy

When git reports a conflict in `docs/<project>/workflow-state.yaml`,
apply these rules **by section**:

### `version`

- Always `1`. If you see a conflict here, something is seriously wrong —
  stop and ask for help before resolving.

### `project`

- `name`, `root`, `started_at`: immutable after creation. Keep the
  pre-existing value; reject any change. If both sides modified these,
  something else is wrong.
- `last_updated_at`, `last_updated_by`: keep the **later** timestamp's
  pair (both fields together).

### `current_focus`

- **Last writer wins** by `project.last_updated_at`. The orchestrator
  overwrites this block every turn; whichever side ran most recently is
  authoritative.
- If both sides ran at the same minute, keep the side whose
  `current_focus.capability_id` matches `project.last_updated_by`'s
  recent `history[]` entries (i.e. follow the active operator's intent).

### `capabilities[]`

- Per-entry merge keyed by `id`:
  - **Both sides modified DIFFERENT entries**: keep both versions
    (additive merge — no real conflict).
  - **Both sides modified the SAME entry**: keep the one with the later
    `last_updated`. If both sides advanced `stage_id`, the **later
    stage** wins (a forward move is harder to undo than a backward one).
  - **One side added a new entry**: keep it.
  - **One side set `archived: true`**: archiving wins (it's a deliberate
    decision; un-archiving would be a follow-up explicit action).
  - **Blocking fields** (`tbds`, `sme_pending`, `gates`): take the union.
    If you're not sure an item is still blocking, leave it in and let
    the next orchestrator turn re-derive from artifacts.

### `history[]`

- **Always union-merge.** History is append-only by contract, so
  divergent appends from two branches must both be preserved.
- After the union, sort the merged list by `at` timestamp ascending
  (oldest first). This restores the contract's "non-decreasing
  timestamps" invariant.
- If two entries have the same timestamp, keep both — order them by
  `skill` name alphabetically as a tiebreaker.

## After resolving — validate

Once the conflict markers are gone, **always** run:

```bash
python3 scripts/check-workflow-state.py docs/<project>/workflow-state.yaml
```

If the lint fails (e.g. duplicate capability IDs, history out of order),
fix the specific finding and re-run. Then regenerate the human snapshot:

```bash
python3 scripts/generate-status.py docs/<project>/
git add docs/<project>/workflow-state.yaml docs/<project>/STATUS.md
git commit
```

## Optional: gitattributes merge driver

A custom merge driver can handle 90% of `workflow-state.yaml` conflicts
without manual intervention. If your team wants this, add to your repo's
`.gitattributes`:

```
docs/*/workflow-state.yaml merge=lsf-workflow-state
docs/*/STATUS.md merge=ours
```

The `STATUS.md merge=ours` line is safe because STATUS.md is always
regenerable from `workflow-state.yaml` — just re-run
`generate-status.py` after the merge to refresh it.

A working `lsf-workflow-state` merge driver is **not** shipped with this
repo yet (would be a Python script implementing the per-section rules
above). It's a planned enhancement; for now use manual merge with the
rules above.

## Coordination patterns that scale

### Pattern A — One project per operator (recommended)

Each operator owns one or more PPCR projects entirely. Different
projects = different `docs/<name>/` folders = zero state conflicts.
Branches per project optional.

### Pattern B — Sequential handoffs on one project

Operator A finishes a stage (commits + pushes), then Operator B picks up
from there (pulls + runs orchestrator). The state file's `current_focus`
+ `history[]` provide a complete handoff record. Useful when work
crosses time zones.

### Pattern C — Parallel capabilities in one project

Operators A and B work on different `CAP-*` within the same project
simultaneously. State file merges cleanly because each operator writes
to a different `capabilities[]` entry. `history[]` interleaves via the
union-merge rule.

### Anti-pattern — Two operators, same capability, same time

Don't. The artifact files themselves (`spec.yaml`, `program-analysis.md`)
will conflict in ways that go deeper than state file merge can fix.
Coordinate via git review or skill-level pairing instead.

## When in doubt

- Open `docs/<project>/STATUS.md` — it shows the post-merge view of
  reality. If it looks wrong, re-run an orchestrator turn to re-derive
  stage from artifacts. The artifact is the source of truth.
- Run `python3 scripts/list-projects.py` to see all projects in the repo
  and who last touched each.
- Per the contract, **artifacts beat state**. A surprising state file is
  an opportunity to re-derive, not a problem to manually patch.

## See also

- [docs/workflow-state-contract.md](workflow-state-contract.md) — the
  authoritative cross-skill contract every writer follows
- [QUICKSTART.md](../QUICKSTART.md) — first-time-user walkthrough
- [scripts/check-workflow-state.py](../scripts/check-workflow-state.py)
  — schema lint
- [scripts/list-projects.py](../scripts/list-projects.py) — repo-wide
  project picker
