# Example Routing: Scan Mode (Inherited Repo, No Workflow State)

## Scenario

The user has been handed someone else's Legacy Spec Factory project. They
run the orchestrator without any specific question, just to "see where
things are." The project root contains existing artifacts but no
`workflow-state.yaml`.

## User Input

> "I just inherited this repo. Where am I? What should I work on?"

## Step 0 — Read Workflow State

`workflow-state.yaml` is **missing**. Per Step 0 rules, treat as a
first-time-on-project case and plan to create the file in Step 8.

## Step 0.5 — Determine Focus

`current_focus` is unset and no `CAP-*` / `MODULE-*` / file path appears in
the user message → outcome candidates are `scan` (artifacts exist) or `new`
(cold start).

Quick artifact probe (per
`references/focus-selection.md` → "Scan Mode → Sources to scan"):

```
01_inventory/inventory.yaml                       → exists, sme_review.decision: approved
04_modules/CREDIT-CHECK/module-overview.md        → exists, 4 views approved, lists CAP-ORDER-PRICING + CAP-CREDIT-CHECK
04_modules/AR/module-overview.md                  → exists, View 4 still draft, lists CAP-AR-POSTING
05_brds/CAP-ORDER-PRICING/brd.md                  → status: approved
05_brds/CAP-CREDIT-CHECK/brd.md                   → status: approved
05_brds/CAP-AR-POSTING/                           → missing
05_specs/CAP-ORDER-PRICING/spec.yaml              → status: approved
05_specs/CAP-CREDIT-CHECK/spec.yaml               → status: in_review
05_specs/CAP-AR-POSTING/                          → missing
06_quality/CAP-ORDER-PRICING/golden-master-tests.md → exists
09_forward-sdlc/                                  → empty
```

Artifacts exist → outcome is `scan`. Present the picker before routing.

## Orchestrator Output

```markdown
This repo has existing artifacts but no `workflow-state.yaml`. I scanned
the standard directories and found three in-flight capabilities. Which do
you want to work on this turn? (Pick one; nothing is changed on disk yet.)

  1. CAP-ORDER-PRICING       (module: CREDIT-CHECK)   stage: 9 Equivalence Pack Ready
     last artifact: 06_quality/CAP-ORDER-PRICING/golden-master-tests.md

  2. CAP-CREDIT-CHECK        (module: CREDIT-CHECK)   stage: 8b Spec In Review
     last artifact: 05_specs/CAP-CREDIT-CHECK/spec.yaml

  3. CAP-AR-POSTING          (module: AR)             stage: 3e Module Analysis In Progress
     last artifact: 04_modules/AR/module-overview.md   (View 4 still draft)

  4. Work on the AR module as a whole (not a single capability).
  5. Start a brand-new capability — tell me the CAP-*.
  6. Start a brand-new module — tell me the MODULE-*.

Once you pick, I will:
- Set `current_focus` accordingly
- Re-derive the current stage from that capability's artifacts
- Route to the next safe skill with a stage card and a Quick Card
- Create `workflow-state.yaml` so the next session can resume

----------------------------------------------------------------------
QUICK CARD — Stage scan : Awaiting Focus Selection
----------------------------------------------------------------------
FOCUS:         unset [scan]
YOU ARE HERE:  pending — three capabilities in flight, picker shown above
JUST SAVED:    nothing yet
RUN NEXT:      (await user pick)
WILL PRODUCE:  workflow-state.yaml (after pick)
GATE CHECK:    not applicable (focus not yet resolved)
SME ACTION:    not needed — focus selection is a user choice, not an SME decision
STAGE CARD:    references/stage-cards/INDEX.md
STATE FILE:    workflow-state.yaml [unchanged — will be created after pick]
MANUAL FALLBACK: not needed (scan + picker are part of the orchestrator)
----------------------------------------------------------------------
```

## Follow-Up (User Picks Option 3)

> "Let's do option 3 — CAP-AR-POSTING."

## Step 0.5 — Re-Entry With Named Target

User named `CAP-AR-POSTING`. It is not yet in `state.capabilities[]` (file
doesn't exist), but it **was discovered** in scan results, so this is
`continued` rather than `new`: the capability already has on-disk artifacts;
the orchestrator just hadn't seen them before.

Resolved focus: `(capability_id: CAP-AR-POSTING, module_slug: AR,
focus_intent: continued)`.

## Steps 1–6 — Stage and Routing

Stage derivation for `CAP-AR-POSTING`:

- `04_modules/AR/module-overview.md` exists; View 4 is still draft → stage
  `3e Module Analysis In Progress` (NOT `3f`).
- Next safe skill: `legacy-ibmi-module-analyzer` to complete View 4.

## Orchestrator Output (Round 2)

```markdown
## Workflow Decision

- **Current Stage:** 3e Module Analysis In Progress (for CAP-AR-POSTING / AR)
- **Desired Outcome:** Complete the 4-view module synthesis
- **Recommended Next Skill:** `legacy-ibmi-module-analyzer` (status: Implemented v0.1.0)
- **Why:** View 4 (Data Flow) is still draft. Finishing it advances the
  module to `3f`, which is the prerequisite for BRD writing / review.

## Routing Notes

- **Stage skip safe?** No. Skipping to spec-writer would orphan the
  unfinished data view and starve the spec of evidence linkage.
- **Gate check:** Module synthesis completeness — blocked on View 4.
- **Minimum input needed next:** the partial `04-data-flow.md`, the
  approved Views 1–3, and SME contact for the data-lifecycle review.
- **Route confidence:** High.
- **Next artifact expected:** approved
  `04_modules/AR/04-data-flow.md` plus an updated
  `04_modules/AR/module-overview.md`.

## Next Step

- **Invoke:** `legacy-ibmi-module-analyzer`
- **Produce:** completed View 4 + updated `module-overview.md`
- **Save reminder:** save under `04_modules/AR/`; consumed by
  `legacy-brd-writer` once all four views are approved.
- **SME reminder:** confirm any `inferred_business_rule` in View 1 or any
  new ones surfaced by completing View 4.
- **Review/export reminder:** Not applicable for this blocked module step. Once
  stable `spec.md`, `traceability.md`, or review-pack Markdown exists, use
  `legacy-html-exporter` only as a browser-friendly companion view.
- **Manual fallback:** Not needed — `legacy-ibmi-module-analyzer` is
  implemented.

----------------------------------------------------------------------
QUICK CARD — Stage 3e Module Analysis In Progress : AR module
----------------------------------------------------------------------
FOCUS:         CAP-AR-POSTING [continued]
YOU ARE HERE:  3e Module Analysis In Progress
JUST SAVED:    nothing yet (this is the resume turn)
RUN NEXT:      legacy-ibmi-module-analyzer   [implemented]
WILL PRODUCE:  04_modules/AR/04-data-flow.md
GATE CHECK:    BLOCKED: module-completeness — View 4 still draft
SME ACTION:    required — confirm any new inferred_business_rule surfaced in View 4
STAGE CARD:    references/stage-cards/05-module-analysis.md
STATE FILE:    workflow-state.yaml [created]
MANUAL FALLBACK: not needed (skill is implemented)
----------------------------------------------------------------------
```

## Step 8 — State File Created

Because no `workflow-state.yaml` existed, the orchestrator creates it now
from the template, populated by scan results plus the user's pick:

```yaml
version: 1

project:
  name: inherited-AR-project
  started_at: 2026-05-16
  last_updated_at: 2026-05-16
  last_updated_by: legacy-modernization-orchestrator

current_focus:
  capability_id: CAP-AR-POSTING
  module_slug: AR
  stage_id: "3e Module Analysis In Progress"
  next_skill: legacy-ibmi-module-analyzer
  next_artifact: 04_modules/AR/04-data-flow.md
  stage_card: references/stage-cards/05-module-analysis.md
  open_gates: ["module_completeness"]

capabilities:
  - id: CAP-ORDER-PRICING
    module_slug: CREDIT-CHECK
    stage_id: "9 Equivalence Pack Ready"
    last_artifact: 06_quality/CAP-ORDER-PRICING/golden-master-tests.md
    last_skill: unknown   # discovered by scan; will be overwritten on next run
    last_updated: 2026-05-16
    blocking:
      tbds: []
      sme_pending: []
      gates: []
    archived: false
  - id: CAP-CREDIT-CHECK
    module_slug: CREDIT-CHECK
    stage_id: "8b Spec In Review"
    last_artifact: 05_specs/CAP-CREDIT-CHECK/spec.yaml
    last_skill: unknown
    last_updated: 2026-05-16
    blocking:
      tbds: []
      sme_pending: []
      gates: []
    archived: false
  - id: CAP-AR-POSTING
    module_slug: AR
    stage_id: "3e Module Analysis In Progress"
    last_artifact: 04_modules/AR/module-overview.md
    last_skill: unknown
    last_updated: 2026-05-16
    blocking:
      tbds: []
      sme_pending: []
      gates: ["module_completeness"]
    archived: false

history:
  - at: 2026-05-16T09:00:00Z
    skill: legacy-modernization-orchestrator
    capability_id: null
    stage_after: "scan"
    artifact: null
    note: "scan-mode picker presented (3 in-flight capabilities discovered)"
  - at: 2026-05-16T09:01:00Z
    skill: legacy-modernization-orchestrator
    capability_id: CAP-AR-POSTING
    stage_after: "3e Module Analysis In Progress"
    artifact: null
    note: "focus set to CAP-AR-POSTING after user pick; state file created from scan"
```

The orchestrator tells the user: "I've created `workflow-state.yaml`.
Please commit it so the next session can resume from the same point."

## Why This Works

- The user did not need to know the directory layout, the stage taxonomy,
  or the contract.
- The orchestrator did not invent any capability — every `CAP-*` in the
  picker came from a real on-disk `spec.yaml` or `module-overview.md`.
- The orchestrator did not pre-pick. Even with one obvious "most
  downstream" capability (`CAP-ORDER-PRICING` at stage 9), the user might
  legitimately want to work on the unfinished `CAP-AR-POSTING` instead.
- Stage `3e` was correctly identified — not "rounded up" to `3f` despite
  three of four views being approved.
- The state file is now the resume point. Next turn, Step 0 reads it; the
  user does not need to re-explain anything.
