# Stage 03: Program Analysis (one program at a time)

**You are here if:** inventory is approved AND you want to analyze one
program's behavior (control flow, file I/O, calls, error handling) before
tracing the full call chain.

You will produce **one program-analysis file per in-scope program**. Loop
through programs one at a time before moving to flow analysis.

## Need before starting

- `01_inventory/inventory.yaml` with `sme_review.decision: approved`
  (or `approved_with_non_blocking_tbd`)
- Redacted source member for the target program
- Any referenced copybook / service-program interfaces
- File list and called objects from `inventory.yaml`

## Run

- **Skill:** `legacy-ibmi-program-analyzer` (Implemented v0.1.0)
- **Manual fallback:** Use the program-analysis skeleton in
  `skills/legacy-ibmi-program-analyzer/references/` and fill it section by
  section against the source

Optional companions (run in parallel when applicable):

- `legacy-ibmi-runtime-evidence-miner` — strengthen evidence with job logs
- `legacy-ibmi-screen-report-analyzer` — for DSPF / PRTF / subfile programs
- `legacy-ibmi-data-model-analyzer` — for domain data model
- `legacy-ibmi-batch-digest` — **run after ≥ 5 programs are analyzed** to
  produce a single SME-facing scan page (`02_programs/<MODULE>/programs-batch-digest.md`)
  grouped by criticality. Cuts SME bandwidth dramatically for medium /
  large modules. Re-run any time new analyses land.

## Produce

- **Artifact:** `program-analysis.md` (one per program)
- **Save under:**
  `02_programs/<MODULE-SLUG>/<OBJ-PROGRAM>/program-analysis.md`
  *(relative to your `project.root`)*
  e.g. `docs/XXX260004-demo/02_programs/CREDIT-CHECK/ORDENTR/program-analysis.md`
- **Consumed by:** `legacy-ibmi-flow-analyzer`

Required sections: Metadata, Entry Points, Control Flow, File I/O, External
Calls, Error Handling, Open Questions (TBD-*). Every row cites an
`evidence_id`.

## Gate before advancing

- **Name:** Program analysis coverage + triggered companions
- **Check:**
  1. count of `program-analysis.md` files == count of in-scope programs
     in `inventory.yaml`
  2. IF `inventory.yaml.sme_review.downstream_required.screen_report_analyzer.required: true`
     → every triggered DSPF / PRTF / menu has an approved
     `screen-report-analysis.md` under
     `02_programs/<MODULE>/screens/`
  3. IF `inventory.yaml.sme_review.downstream_required.data_model_analyzer.required: true`
     → `04_modules/<MODULE>/data-model/dictionary.md` exists at
     `review_status: approved` or `approved_with_non_blocking_tbd`
- **Blocks if:** any of (1), (2), (3) fail; OR any analysis has
  `review_status: needs_sme_review` for a money / inventory / compliance
  / customer-status branch

The conditional gates (2) and (3) are MECHANICALLY enforced by the
orchestrator — once inventory declares the trigger, the optional skills
become required. Trigger rules:
[`skills/legacy-ibmi-inventory/references/downstream-triggers.md`](../../../legacy-ibmi-inventory/references/downstream-triggers.md).

## SME action

- **Required:** for any branch affecting money, inventory, compliance,
  customer status, or posting
- **Ask:** "Is this branch's observed behavior correct in production? Are
  any conditions or exceptions missing?"
- **Recorded in:** `program-analysis.md` → `review_status` per row +
  `Open Questions` table

## Next card

[`04-flow-analysis.md`](04-flow-analysis.md) — once every in-scope program
has an approved analysis.
