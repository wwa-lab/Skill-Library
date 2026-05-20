# Synthetic Corpus Pilot Execution Checklist

Use this checklist to run a **consistent internal pilot** against the synthetic
fixtures under [`docs/synthetic-corpus/`](README.md).

The goal is not to produce perfect downstream artifacts on day one. The goal is
to verify that the main Legacy Spec Factory skills:

- trigger reliably
- classify stage correctly
- respect blocking gates
- avoid hallucinating missing source or business meaning
- extract the right high-level structure from representative IBM i inputs

## Fixtures In Scope

| Fixture | Purpose | Primary Skills |
| --- | --- | --- |
| [`sqlrpgle-credit-check-happy`](sqlrpgle-credit-check-happy/README.md) | fixed-format `SQLRPGLE` happy path | orchestrator, intake, inventory, program, flow |
| [`sqlrpgle-credit-check-blocked`](sqlrpgle-credit-check-blocked/README.md) | blocked gate / anti-hallucination path | orchestrator, inventory, program |
| [`batch-ar-reconciliation`](batch-ar-reconciliation/README.md) | scheduler + batch + spool + joblog path | orchestrator, intake, inventory, runtime-evidence, program, flow |
| [`screen-subfile-inquiry`](screen-subfile-inquiry/README.md) | menu + DSPF + subfile inquiry path | orchestrator, inventory, screen, program, flow |

## Pilot Output

For each fixture, record:

- runtime used
- prompt used
- skill invoked
- output summary
- pass / executed / blocked / failed judgment
- notes on hallucination, missed coverage, or routing mistakes

Keep the first pilot lightweight. A Markdown table or one short review note per
fixture is enough.

## OpenCode-Only Note

If your company pilot can only run in **OpenCode**, treat this checklist as an
OpenCode-first workflow:

- use OpenCode as the only execution runtime
- ignore Codex / Claude Code portability comparisons for this pilot round
- focus on whether the skill triggers, blocks correctly, and produces the
  expected structure inside OpenCode

In that case, your real pilot outcome is:

- can OpenCode safely run the reverse-modernization path on representative IBM i
  inputs?

That is enough to validate product direction for an internal pilot.

## General Pass Rules

Mark a step as:

- `passed` when the right skill fires and the output matches the fixture's
  `expected/` assertions
- `executed` when the skill fires and output is structurally useful, but misses
  one or more important assertions
- `blocked` when the skill correctly stops due to a real gap in the blocked
  fixture
- `failed` when the wrong skill fires, the gate is skipped, or the output
  invents unsupported facts

## Phase 1: Orchestrator Routing

Run `legacy-modernization-orchestrator` first for every fixture.

Use [`docs/orchestrator-review-checklist.md`](../orchestrator-review-checklist.md)
to score whether the orchestrator is reliable enough as the single OpenCode
entry point.

### Expected Results

- `sqlrpgle-credit-check-happy`
  Should route to evidence intake or inventory, not directly to spec writing.
- `sqlrpgle-credit-check-blocked`
  Should refuse to move past the missing-source gap.
- `batch-ar-reconciliation`
  Should identify a batch or scheduler-driven path and route toward intake /
  inventory / flow-oriented analysis.
- `screen-subfile-inquiry`
  Should identify an inquiry-style interactive path and not misclassify it as a
  batch flow.

### Failure Signs

- recommends downstream spec generation too early
- ignores missing-source blockers
- misclassifies screen-driven inquiry as report-only or batch-only
- treats batch runtime evidence as optional noise

## Phase 2: Evidence Intake

Run `legacy-ibmi-evidence-intake` for:

- `sqlrpgle-credit-check-happy`
- `batch-ar-reconciliation`
- `screen-subfile-inquiry`

The blocked credit-check fixture can also be used here, but the key check is
whether missing source is surfaced clearly rather than silently tolerated.

### Expected Results

- identifies source, runtime, and SME assets
- keeps sensitivity / redaction framing explicit
- records enough evidence for inventory to proceed on happy paths
- surfaces missing-source gaps on blocked paths

### Compare Against

- fixture `README.md`
- fixture `sme/`
- fixture `runtime/`

## Phase 3: Inventory

Run `legacy-ibmi-inventory` for all four fixtures.

### Compare Against

- `sqlrpgle-credit-check-happy/expected/inventory-assertions.md`
- `sqlrpgle-credit-check-blocked/expected/inventory-assertions.md`
- `batch-ar-reconciliation/expected/inventory-assertions.md`

For `screen-subfile-inquiry`, use the fixture README and source set as the
reference until a dedicated inventory assertion file is added.

### Expected Results

- happy fixtures enumerate the core program, file, and surface objects
- blocked fixture remains blocked because `CREDITVW.LF` is missing
- screen fixture includes menu, DSPF, and program as distinct assets
- batch fixture preserves the operational importance of `ARCTRL` and `ARERRRPT`

### Failure Signs

- silently invents missing LF or access-path details
- collapses menu / DSPF / program into one asset
- ignores PRTF or spool-facing artifacts in batch flow

## Phase 4: Program Analysis

Run `legacy-ibmi-program-analyzer` for:

- `sqlrpgle-credit-check-happy/source/CREDITCHK.SQLRPGLE`
- `sqlrpgle-credit-check-blocked/source/CREDITCHK.SQLRPGLE`
- `batch-ar-reconciliation/source/ARRECON.SQLRPGLE`
- `screen-subfile-inquiry/source/CUSTINQ.SQLRPGLE`

### Compare Against

- `sqlrpgle-credit-check-happy/expected/program-analysis-assertions.md`
- `sqlrpgle-credit-check-blocked/expected/program-analysis-assertions.md`
- `batch-ar-reconciliation/expected/program-analysis-assertions.md`

For `screen-subfile-inquiry`, the inquiry behavior should align with the README
and screen-analysis expectations even though there is no separate program
assertion file yet.

### Expected Results

- happy credit-check analysis recognizes embedded SQL decision branches
- blocked credit-check analysis describes visible structure but refuses to
  approve unsupported meaning
- batch analysis recognizes scheduler/batch loop, restart semantics, and
  exception reporting
- inquiry analysis does not invent update-heavy behavior

### Failure Signs

- invents derived-field semantics without source
- upgrades blocked branch meaning into approved business rules
- treats inquiry code as if it were a maintenance transaction

## Phase 5: Runtime Evidence Mining

Run `legacy-ibmi-runtime-evidence-miner` for:

- `batch-ar-reconciliation/runtime/sample-joblog.txt`
- `batch-ar-reconciliation/runtime/sample-spool.txt`

Optionally use the credit-check happy runtime set as a lighter secondary check.

### Compare Against

- `batch-ar-reconciliation/expected/runtime-evidence-assertions.md`

### Expected Results

- identifies submission, restart, exception, and completion observations
- extracts report-structure signals from spool output
- keeps confidence below `high` for one-run evidence

### Failure Signs

- invents schedule stability from one run
- ignores the spool structure
- misses restart or completion observations

## Phase 6: Screen Analysis

Run `legacy-ibmi-screen-report-analyzer` for:

- `screen-subfile-inquiry/source/CUSTINQDSP.DSPF`

### Compare Against

- `screen-subfile-inquiry/expected/screen-analysis-assertions.md`

### Expected Results

- classifies the surface as DSPF + subfile inquiry
- recognizes header format, subfile, and subfile control
- recognizes `F5` refresh and `F12` return
- does not invent maintenance or delete behavior

### Failure Signs

- classifies the screen as update-first without evidence
- invents row-level update or delete semantics
- misses subfile control behavior

## Phase 7: Flow Analysis

Run `legacy-ibmi-flow-analyzer` for:

- `sqlrpgle-credit-check-happy`
- `batch-ar-reconciliation`
- `screen-subfile-inquiry`

The blocked credit-check fixture should only be used to confirm that flow work
does not advance improperly when prerequisites are unresolved.

### Compare Against

- `sqlrpgle-credit-check-happy/expected/flow-assertions.md`
- `batch-ar-reconciliation/expected/flow-assertions.md`
- `screen-subfile-inquiry/expected/flow-assertions.md`

### Expected Results

- credit-check is modeled as a direct or wrapper-triggered synchronous decision
  path
- batch is modeled as a scheduler-submitted reconciliation path
- inquiry is modeled as a menu-driven customer-service review path

### Failure Signs

- batch flow described as interactive
- inquiry flow described as update workflow
- blocked fixture advances to approved flow despite unresolved missing source

## Recommended Pilot Order

Run the fixtures in this order:

1. `sqlrpgle-credit-check-happy`
2. `sqlrpgle-credit-check-blocked`
3. `batch-ar-reconciliation`
4. `screen-subfile-inquiry`

Why this order:

- start with the cleanest fixed-format `SQLRPGLE` happy path
- immediately test blocked-gate discipline on the paired negative case
- then test batch/runtime complexity
- finish with screen/subfile inquiry interpretation

## Minimal Pilot Exit Criteria

Consider the synthetic pilot useful when all of these are true:

- orchestrator routes all four fixtures plausibly
- blocked credit-check remains blocked without hallucinated completion
- happy credit-check reaches useful inventory, program, and flow outputs
- batch fixture yields useful runtime and flow observations
- screen fixture yields useful screen interpretation without invented update
  semantics

## What To Tighten Next

After one full pilot pass, use the findings to decide which to add next:

- missing `expected/inventory-assertions.md` for `screen-subfile-inquiry`
- blocked sibling for `batch-ar-reconciliation`
- blocked sibling for `screen-subfile-inquiry`
- fixture test protocol templates for recording per-runtime observations
