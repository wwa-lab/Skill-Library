# Focus Selection Reference

Resolves "what is the user trying to work on **this turn**?" from three
inputs: natural-language user message, `workflow-state.yaml`, and what
artifacts exist on disk.

The orchestrator's **Step 0.5** invokes this reference. The output is a
resolved `(capability_id, module_slug, focus_intent)` tuple that Steps 1–8
use as their scope. Without this step, multi-capability projects, mid-chain
entry, and rollback all degrade to guesswork.

## Five Focus Outcomes

| Outcome | When | What changes in `workflow-state.yaml` |
| --- | --- | --- |
| `continued` | User implicitly continues the existing focus; no `CAP-*` / `MODULE-*` named | nothing in `current_focus`; routing decision still appends to `history[]` |
| `switched` | User names a different `CAP-*` / `MODULE-*` that already exists in `capabilities[]` | `current_focus` overwritten to the new target; old `capabilities[]` entry preserved |
| `new` | User starts a brand-new capability / module not yet in `capabilities[]` | `current_focus` overwritten; one new entry appended to `capabilities[]` |
| `scan` | No `current_focus` set (first time on this repo, inherited repo, or state empty) and artifacts exist | scan artifacts, present a picker, then re-enter the tree with the picked target |
| `rollback` | User asks to redo or revert to an earlier stage within current focus | `stage_id` rewound for the focused capability; one `history[]` entry with `rollback` note |

## Signal Detection

Scan the user message for these patterns. **First match wins** for the
focus target; rollback verbs are detected independently and can co-occur.

| Pattern | Signal | Notes |
| --- | --- | --- |
| Literal `CAP-[A-Z0-9-]+` | named capability | exact case-insensitive match |
| Literal `MODULE-[A-Z0-9-]+` OR any known `module_slug` from `state.capabilities[].module_slug` | named module | match against known slugs to avoid false positives |
| File path matching `01_inventory/...`, `02_programs/<MODULE>/...`, `03_flows/<MODULE>/...`, `04_modules/<MODULE>/...`, `05_specs/<CAP>/...` | named module or capability | extract from path |
| Verbs: `重做`, `redo`, `回到`, `rollback`, `back to`, `撤回`, `revert`, `回滚` | rollback intent | combine with target stage if user names one |
| Verbs: `继续`, `next`, `下一步`, `接着`, `继续做` | continue intent | default when no target named |
| Verbs: `新的`, `another`, `start new`, `开新`, `切换到`, `switch to` | new / switch intent | `switched` if target exists, `new` if not |
| No matched signal | default | if `current_focus` set → `continued`; else → `scan` (artifacts present) or cold start (no artifacts) |

## Decision Tree

Pseudocode. Run top to bottom; first triggered branch wins.

```text
state = read_workflow_state()
focus = state.current_focus
msg   = user.natural_language_input

1. If msg contains a rollback verb:
     outcome = rollback
     target_stage = extract_target_stage(msg) or ASK user
     target_cap   = extract_named_cap(msg) or focus.capability_id
     -> run Rollback Protocol below
     STOP

2. If msg names a CAP / MODULE / path:
     named_target = first_match(msg)
     if named_target.cap == focus.capability_id:
       outcome = continued
     elif named_target in state.capabilities[]:
       outcome = switched
       -> run Switch Protocol below
     else:
       outcome = new
       -> create capabilities[] entry, set current_focus
     STOP

3. If msg has a continue verb AND focus is set:
     outcome = continued
     STOP

4. If focus is set AND no contrary signal:
     outcome = continued
     STOP

5. If focus is unset AND artifacts exist on disk:
     outcome = scan
     -> run Scan Mode, present picker, re-enter tree with user pick
     STOP

6. If focus is unset AND no artifacts exist:
     outcome = new (cold start)
     -> route to legacy-ibmi-evidence-intake
     STOP
```

## Scan Mode

When `current_focus` is unset but the project already contains artifacts
(the "inherited repo" / "first time on this project" / "lost state" case),
enumerate every capability under the resolved `project.root` and present a
picker.

Scan is project-scoped — it never crosses into another project's
`docs/<other>/` tree.

### Sources to scan

All paths are **relative to `project.root`** (`docs/<project-name>/`).
Step 0.b resolves the project root before this table is consulted.

| Source path (relative to project.root) | Yields | Implied stage |
| --- | --- | --- |
| `05_specs/CAP-*/spec.yaml` | `capability_id` + `spec.yaml.status` | `8a` / `8b` / `8c` |
| `04_modules/<MODULE>/module-overview.md` | `module_slug` + `CAP-*` seeds + view count | `3e` / `3f` |
| `00_context_packages/<MODULE>/context-index.yaml` | `module_slug` + intake status + RAG run IDs | `0m` / `0n` |
| `03_flows/<MODULE>/flow-*.md` | `module_slug` + flow count + `status` | `3c` / `3d` |
| `02_programs/<MODULE>/<OBJ>/program-analysis.md` | `module_slug` + per-program coverage | `3a` / `3b` |
| `01_inventory/inventory.yaml` | `module_slug` + `sme_review.decision` + `coverage_gaps[]` | `2a` / `2b` / `2c` |
| `evidence/redacted/evidence-manifest.yaml` | bundle id + sensitivity rollup | `1` (only if no inventory) |
| `06_quality/CAP-*/golden-master-tests.md` | `capability_id` | `9` |
| `09_forward-sdlc/CAP-*/` | `capability_id` | `10` |

Pick the **most downstream** stage that has an artifact for each
capability. Mention upstream stages only when the SME has not approved them.

### Picker output

```
I found these in-flight capabilities. Which do you want to work on this turn?

  1. CAP-ORDER-PRICING       (module: CREDIT-CHECK)   stage: 8c Spec Approved
  2. CAP-CREDIT-CHECK        (module: CREDIT-CHECK)   stage: 3b Program Analysis Done
  3. CAP-AR-POSTING          (module: AR)             stage: 2c Inventory Done

  4. (work on a module, not a single capability) — pick from: CREDIT-CHECK, AR
  5. (start a brand-new capability — name it: CAP-?)
  6. (start a brand-new module — name it: MODULE-?)
```

After the user picks, re-enter the decision tree treating the pick as a
`named_target` signal (branch 2).

If the picker would have **zero** entries (no in-flight artifacts at all),
fall through to branch 6 (cold start).

## Switch Protocol

A switch changes `current_focus` without losing the previous focus.

1. Verify `state.capabilities[<new-target>]` exists. If not, treat as `new`,
   not `switched`.
2. Overwrite `state.current_focus` with the new target's identifiers.
3. Re-derive `stage_id` from the new target's artifacts (Step 1 of Core
   Process).
4. Append a `history[]` entry:
   ```yaml
   - at: <ISO 8601>
     skill: legacy-modernization-orchestrator
     capability_id: <new CAP-*>
     stage_after: <newly derived stage_id>
     artifact: null
     note: "focus switched from <old CAP-*> to <new CAP-*>"
   ```
5. Do NOT mutate the old `capabilities[]` entry. The old focus stays at
   whatever stage it was last left at.

## Rollback Protocol

A rollback is a controlled backward move within ONE capability. It must
never silently overwrite a later `stage_id`.

1. Identify the rollback target stage (from user message; otherwise ASK).
2. Verify the target is **strictly earlier** than the current `stage_id`.
   If not, this is `continued`, not rollback — say so.
3. Verify the rollback target was **previously reached** (look at
   `history[]`). If not, this is `new` (cold start for that capability),
   not rollback.
4. Overwrite `state.capabilities[<cap>].stage_id` to the target stage.
5. Append a `history[]` entry:
   ```yaml
   - at: <ISO 8601>
     skill: legacy-modernization-orchestrator
     capability_id: <CAP-*>
     stage_after: <target stage_id>
     artifact: null
     note: "rollback from <previous stage_id> to <target stage_id>: <reason>"
   ```
6. Do NOT delete downstream artifacts. They remain on disk as evidence of
   the previous attempt and must be re-validated once the rolled-back
   stage's output changes. Surface this to the user in the prose section
   above the Quick Card:
   > Rolling back from `<X>` to `<Y>`. Artifacts at stages later than `<Y>`
   > remain on disk and must be re-validated after `<Y>` changes.
7. Route to the skill that produces the rolled-back stage's artifact.

## Mid-Chain Entry Cheat Sheet

The single biggest UX pain is "I show up holding artifact `X`, where do I
plug in?" Quick lookup:

| User holds... | Likely outcome | Likely route |
| --- | --- | --- |
| Just raw source / job log | cold start (`new`) | `legacy-ibmi-evidence-intake` |
| `evidence-manifest.yaml` approved, no inventory | `new` (capability not yet scoped) | `legacy-ibmi-inventory` |
| `inventory.yaml` (approved), nothing else | `new` per-module | `legacy-ibmi-program-analyzer` |
| `program-analysis.md` for some programs | `continued` if in `capabilities[]`; else `scan` then `continued` | continue program analysis or move to `legacy-ibmi-flow-analyzer` |
| `flow-*.md` for some flows | same | continue flows or move to `legacy-ibmi-module-analyzer` |
| `module-overview.md` + 4 views approved, no approved BRD Package | `continued` (one CAP-* per BRD) | `legacy-brd-writer` |
| `module-overview.md` + 4 views approved + approved BRD Package | `continued` (one CAP-* per spec) | `legacy-spec-writer` |
| `spec.yaml` (`status: draft`) | `continued` | finish spec, then SME review |
| `spec.yaml` (`status: approved`) but no equivalence pack | `continued` | `legacy-golden-master-test-planner` |
| Approved spec + equivalence pack, no handoff | `continued` | `legacy-brd-to-sdd-handoff` |
| Someone else's repo, no `workflow-state.yaml` | `scan` | run Scan Mode → picker → re-enter tree |

## Anti-Hallucination Rules

- Never invent a `CAP-*` or `MODULE-*` ID that has no evidence in
  artifacts, `workflow-state.yaml`, or the user message.
- When ambiguous (e.g. user says "the order one" and two capabilities
  match), ASK; do not pick.
- When a natural-language verb conflicts with state (user says "continue"
  but `current_focus` is blocked at a gate), surface the conflict — do not
  pretend the gate is open.
- Rollback to a stage that was never reached is not a rollback. Treat it
  as cold start (`new`) for that stage.
- Do not run scan mode silently. Always show the picker so the user can
  confirm — even if there's only one capability in flight.
- Do not assume the most recent `history[]` entry is the user's intended
  focus. The user may have come back to work on something older.
