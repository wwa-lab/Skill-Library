---
name: legacy-ibmi-batch-digest
description: Use when every per-program analysis under one module should be aggregated into a single SME-friendly batch digest table (`programs-batch-digest.md`). Reduces SME review friction for medium/large modules — a 50-program module turns from 50 files to one scannable page grouped by criticality (critical / standard / low_risk), with one-line roles, key pending decisions, TBD counts, and links to detail. Trigger when the user says "give me the SME-facing program review", "我要给 SME 看程序清单", "batch review the programs in this module", or after a batch of new program-analysis.md files lands. Supplemental skill — does not advance the linear stage_id; co-exists with `legacy-ibmi-program-analyzer` (which produces the detail) and `legacy-sme-review-facilitator` (which builds the active decision queue).
license: Apache-2.0
metadata:
  author: Leo L Zhang
  maintainer: platform-engineering
  source: https://github.com/wwa-lab/legacy-spec-factory
  source_commit: 3b6a16b
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

# Legacy IBM i — Programs Batch Digest

Aggregate every `02_programs/<MODULE>/<OBJ>/program-analysis.md` under one
module into a single page the SME can scan in 30 minutes instead of
opening 50+ files. Groups programs by `criticality` so the SME's eye lands
on the rows that matter most.

## Purpose

A typical AS400 module yields 20–200 program-analysis files after the
program-analyzer skill finishes. Asking the SME to open each one is the
biggest single source of "SME bandwidth is the bottleneck" friction. This
digest:

- Lists every analyzed program on one page
- Groups by `criticality` (critical first; standard; low_risk last)
- For each row: one-line role, ≤ 3 key pending decisions, TBD count,
  approval status, link to the detail
- Surfaces aggregate counts so SME knows the workload up front
- Co-locates the SME's batch signoff at the bottom of the same file

The detail files (`program-analysis.md`) remain the source of truth. The
digest is a navigation index, not a replacement.

## When to Use

Trigger on any of these signals:

- A module has ≥ N (default 5) `program-analysis.md` files (draft or
  approved) and no current digest exists
- The orchestrator just advanced a capability to
  `3b Program Analysis Done`
- The user asks "give me the SME-facing program list", "我要给 SME 看程序",
  "batch digest", or names a module with many programs
- A new batch of program analyses just landed and the existing digest is
  > 24h stale (compare `last_updated_at` vs each program-analysis.md's
  `mtime`)

**Do NOT trigger** when:

- Fewer than 2 programs have analyses (no aggregation value)
- The user is mid-flow on a single program analysis (interrupting their
  flow)
- A digest exists and is current (re-running adds churn)

## Layer Position

Supplemental Layer 1 skill. Lives alongside `legacy-ibmi-program-analyzer`
in the pipeline but does NOT advance the linear `stage_id`. Per
`docs/workflow-state-contract.md`, it appends `history[]` only — it does
not own `capabilities[].stage_id`.

Position: runs after program-analyzer (needs at least some
`program-analysis.md` files); consumed by `legacy-sme-review-facilitator`
to drive the three-bucket review routing.

## Inputs

| Input | Source | Required |
| --- | --- | --- |
| All `program-analysis.md` for a module | `02_programs/<MODULE-SLUG>/*/program-analysis.md` | yes |
| Inventory with criticality | `01_inventory/inventory.yaml` (objects with `criticality` and `criticality_confirmed_by_sme: true`) | yes |
| `workflow-state.yaml` | `<project.root>/workflow-state.yaml` | yes |
| Existing digest (if regenerating) | `02_programs/<MODULE-SLUG>/programs-batch-digest.md` | optional |

Input readiness scoring:

- `0-5 blocked`: inventory missing, criticality not SME-confirmed, no
  `program-analysis.md` files, module scope ambiguous, or evidence
  authorization unresolved.
- `6 minimum_pass`: module slug, approved inventory with SME-confirmed
  criticality, workflow state, and at least two program analyses are present.
- `7-8 usable`: all inventory programs have corresponding analyses or clear
  `not yet analyzed` rows.
- `9-10 strong`: regenerated digest context, latest SME routing preferences,
  prior digest, and known review capacity/priority notes are also supplied.
- Missing existing digest does not block; missing analyses for some inventory
  programs lowers completeness but can be reported explicitly.

**Stop conditions:**

- Inventory has no `criticality` fields or
  `criticality_confirmed_by_sme: false` for any program → block; route
  user back to `legacy-ibmi-inventory` to finish criticality
  classification + SME confirmation
- No `program-analysis.md` files exist → block; route to
  `legacy-ibmi-program-analyzer` first
- Programs in inventory but not in `02_programs/<MODULE>/` → still
  produce the digest, but mark those rows as `not yet analyzed`

## Output Contract

Single output: `02_programs/<MODULE-SLUG>/programs-batch-digest.md`.

Format specified in
[`references/digest-format.md`](references/digest-format.md). Summary:

```markdown
# Programs Batch Digest — <MODULE-SLUG>

**Generated:** <YYYY-MM-DD by skill version>
**Source:** <count> program-analysis.md files in `02_programs/<MODULE-SLUG>/`
**Inventory:** `01_inventory/inventory.yaml` (criticality confirmed <date> by <SME>)

## At a glance

- Critical: <N> programs  (full SME review)
- Standard: <M> programs  (spot-check)
- Low-risk: <K> programs  (batch confirm)
- Not yet analyzed: <L> programs

## Critical (<N>) — full SME review per program

| OBJ | Role (1 line) | Key pending decisions | TBDs | Status | Detail |
| --- | --- | --- | --- | --- | --- |
| OBJ-<MOD>-<NAME> | one-sentence role from analysis Metadata | top-3 `needs_sme_review` rows, comma-separated | count | draft / approved | [`<path>`](<path>) |
| ...

## Standard (<M>) — spot-check sample

| OBJ | Role | Key decisions | TBDs | Status | Detail |
| ...

## Low-risk (<K>) — batch confirm

| ... |

## Not yet analyzed (<L>)

| OBJ | Source member | Why analysis is pending |
| ...

---

## SME signoff

- **Critical bucket** — reviewed per-program by: ________ on ________
- **Standard bucket** — spot-checked <count> of <N> by: ________ on ________
- **Low-risk bucket** — batch-confirmed by: ________ on ________

Rejections / corrections recorded in
`08_business-understanding/<CAP-*>/sme-review-<date>.md`.
```

Required sections:

- "At a glance" counts — pulled from criticality field
- One table per criticality bucket (omit a bucket only if its count is 0)
- "Not yet analyzed" table for programs in inventory without an analysis
- "SME signoff" stub at the bottom

Each row's "Role" comes from the program-analysis.md `Metadata.role` or
the inventory `role` field (whichever is more specific). Do NOT invent.

Each row's "Key pending decisions" comes from the program-analysis.md
rows with `review_status: needs_sme_review`. Take the top 3 by
significance (rows in money/posting paths first). If none, write `(none)`.

Each row's "TBDs" is the count of rows in the `Open Questions` table
with `Resolution` empty.

## Step Contract

### Input

- **Required**: a module slug + a project root containing approved
  inventory (with criticality SME-confirmed) and at least 2
  `program-analysis.md` files for that module
- **Optional**: existing digest to regenerate (re-render replaces, never
  edits in place)
- **Input readiness scoring**: apply
  `../../docs/input-readiness-rubric.md`; `minimum_pass` requires confirmed
  criticality plus analyzable program outputs, while review-capacity notes are
  quality boosters only.
- **Readiness checks**: inventory's `criticality_confirmed_by_sme` is
  `true` for every program; criticality_summary present in
  `sme_review`
- **Stop conditions**: inventory criticality not confirmed; no
  program-analysis files; programs span more than one module (this skill
  is per-module, not per-project — caller must scope correctly)

### Execution

- **Procedure**:
  1. Read inventory; partition programs by criticality
  2. For each analyzed program, extract Metadata.role +
     `needs_sme_review` rows + open TBDs
  3. For unanalyzed programs, mark "not yet analyzed" with reason
  4. Render the markdown in the format above; sort within bucket by
     `OBJ id` lexicographic
  5. Save to `02_programs/<MODULE-SLUG>/programs-batch-digest.md`
- **Allowed inference**: extracting roles from existing Metadata fields;
  picking the "top-3 significant" decisions using money-path > inventory
  > compliance > customer-status > everything else as priority
- **Forbidden assumptions**: inventing a `role` or `criticality` not in
  source artifacts; copying program-analysis prose verbatim (use the
  Metadata fields and table rows only); silently dropping programs from
  inventory that have no analysis — they appear in "Not yet analyzed"
- **TBD handling**: a digest row may say `(unclear)` when source data is
  ambiguous; never invent

### Output

- **Canonical artifact**: `programs-batch-digest.md` at the path above
- **Required sections**: At a glance, one table per non-empty
  criticality bucket, Not yet analyzed, SME signoff
- **Required IDs**: every row cites an `OBJ-*` from inventory and a
  link path to the detailed analysis (when present)
- **Handoff status**: consumed primarily by
  `legacy-sme-review-facilitator` for three-bucket routing and by the
  SME directly as a single-page scan target

### Validation

- **Mechanical**: every program in inventory appears in exactly one
  bucket table (analyzed) or in "Not yet analyzed"; every "Detail" link
  resolves; counts in "At a glance" match table row counts; criticality
  matches inventory verbatim
- **AI semantic**: roles match Metadata; pending decisions cite real
  rows from the source analysis (no fabricated decisions); TBD counts
  match the open count in the source
- **SME / human approval**: not required for the digest itself, but the
  digest contains the SME signoff stub that captures the SME's batch
  decisions
- **Blocking conditions**: inventory criticality not confirmed; programs
  span multiple modules; digest produced from incomplete inventory

## Workflow

1. **Resolve inputs**: orchestrator hands you `project.root +
   module-slug`. Read `inventory.yaml` and partition by criticality.
   Validate `criticality_confirmed_by_sme: true` for every entry —
   otherwise STOP and route to inventory.
2. **Discover analyses**: glob
   `02_programs/<MODULE>/*/program-analysis.md`. Build a map `OBJ-id →
   analysis path` for analyzed; `OBJ-id → null` for not-yet-analyzed.
3. **Extract per-row data**: for each analyzed program, read its
   Metadata block, its rows with `review_status: needs_sme_review`,
   and its Open Questions table. Build the row tuple `(obj_id,
   role_one_line, top_3_decisions, tbd_count, status, detail_path)`.
4. **Render markdown**: in the format specified in
   [`references/digest-format.md`](references/digest-format.md). Group
   by criticality; within group, sort by `OBJ id`.
5. **Write file**: replace any existing
   `programs-batch-digest.md` for this module. Never edit in place — full
   re-render every run.
6. **Append history**: one entry per
   `docs/workflow-state-contract.md`; do not advance `stage_id`.

## Anti-Hallucination Rules

- Never invent a `role`, `criticality`, or `OBJ-*` ID that is not in
  inventory or the source program-analysis.
- Never copy prose from program-analysis verbatim into the digest. Use
  Metadata fields and structured rows; if Metadata is missing, write
  `(role unstated — see detail)` rather than fabricating.
- Never collapse two programs into one row. Even if two RPGLE members
  have near-identical roles, they get separate rows.
- Never re-order programs by your own assessment of importance.
  Criticality from inventory is the only sort grouping; within a group,
  use `OBJ id` lexicographic order.
- Never modify `inventory.yaml`. This skill is read-only against
  inventory.

## SME Review Questions

Co-located with the digest's "SME signoff" stub:

- **Critical bucket**: per-program — "Is the role correct? Are the
  pending decisions complete? Any branch we missed that touches money /
  posting / compliance?"
- **Standard bucket**: spot-check — "Pick N of M; for each pick, the
  same questions as critical. If all picks pass, OK to batch the rest."
- **Low-risk bucket**: batch — "Scan the table. Anything that doesn't
  look truly low-risk? If not, batch-confirm."
- **Not-yet-analyzed**: "Should these be analyzed before flow analysis
  proceeds, or are they safe to defer?"

## Workflow State Write-Back (history only — supplemental)

This is a supplemental skill. It does NOT mutate `capabilities[].stage_id`
or `current_focus`. After a run, append one `history[]` entry to
`<project.root>/workflow-state.yaml` per
[`docs/workflow-state-contract.md`](../../docs/workflow-state-contract.md).

**Last artifact path pattern:**
`02_programs/<MODULE-SLUG>/programs-batch-digest.md`

**Per-run write:**

```yaml
history:
  - at: <ISO 8601>
    skill: legacy-ibmi-batch-digest
    capability_id: <CAP-* from current_focus, or null if module-scoped>
    stage_after: <UNCHANGED stage_id>
    artifact: 02_programs/<MODULE-SLUG>/programs-batch-digest.md
    note: "digest for <MODULE> — critical/<N>, standard/<M>, low_risk/<K>, not-analyzed/<L>"
```

Also overwrite `project.last_updated_at` / `project.last_updated_by`.

**Permitted side-effect:** none. This skill does NOT touch
`capabilities[].blocking.*` or `stage_id`. The owning Tier 1 skill
(`legacy-ibmi-program-analyzer` for stage advancement) keeps that
responsibility. After SME signoff is recorded in the digest's SME
signoff stub, `legacy-sme-review-facilitator` may update
`blocking.sme_pending` based on rejections, not this skill.

If `workflow-state.yaml` does not exist, this skill does NOT create it.

## Runtime Portability

The canonical skill source lives under:

```text
skills/legacy-ibmi-batch-digest/SKILL.md
```

Runtime copies may be synced to:

```text
.claude/skills/legacy-ibmi-batch-digest/SKILL.md
.opencode/skills/legacy-ibmi-batch-digest/SKILL.md
.agents/skills/legacy-ibmi-batch-digest/SKILL.md
.codex/skills/legacy-ibmi-batch-digest/SKILL.md
```

From the repository root, use `scripts/sync-skills.sh` to create or check
runtime copies.

## Version History

- v0.1.0 (2026-05-16): Initial batch digest skill. Per-module aggregation
  grouped by `criticality` (from inventory). Drives SME review friction
  down to one-page-per-module instead of N files. Co-exists with
  `legacy-ibmi-program-analyzer` (detail) and
  `legacy-sme-review-facilitator` (active decision queue). Strategy 2 of
  the SME-bandwidth reduction plan, complementing Strategy 1
  (criticality classification) and Strategy 3 (rule auto-validation).
