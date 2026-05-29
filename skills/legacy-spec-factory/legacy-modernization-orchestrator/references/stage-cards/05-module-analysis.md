# Stage 05: Module Analysis (4-view synthesis)

**You are here if:** every flow in scope for this module has an approved
`flow-<slug>.md`, or a ready `00_context_packages/<MODULE-SLUG>/` package is
being used as module-first context, AND you need to synthesize the module's
complete behavior into the canonical 4 views before BRD writing and review.

This is the **last reverse-engineering step** before BRD writing. Business
rule seeds and capability seeds emerge here, then the BRD Package becomes the
business / SME review artifact before any spec is produced.

## Need before starting

- `03_flows/<MODULE-SLUG>/flow-*.md` for every flow (all approved)
- `02_programs/<MODULE-SLUG>/<OBJ>/program-analysis.md` for every program
- `01_inventory/inventory.yaml` (approved)
- SME-confirmed BAU notes for the module (any operational quirks,
  workarounds, undocumented rules)

## Run

- **Skill:** `legacy-ibmi-module-analyzer` (Implemented v0.1.4)
- **Manual fallback:** Build the 4 views by hand following
  `docs/module-analysis-model.md` and the templates in
  `skills/legacy-ibmi-module-analyzer/references/`

## Produce

- **Artifact:** 4 view files + a module overview
  - `module-overview.md` — module identity, in-scope flows, capability seeds (`CAP-*`)
  - `01-operation-flow.md` — user/operator perspective + business rule seeds (`BR-*`)
  - `02-system-flow.md` — system interaction perspective
  - `03-program-flow.md` — program-level sequencing
  - `04-data-flow.md` — data lifecycle perspective
- **Save under:** `04_modules/<MODULE-SLUG>/` *(relative to your
  `project.root`, e.g. `docs/XXX260004-demo/04_modules/CREDIT-CHECK/`)*
- **Consumed by:** `legacy-brd-writer` first; `legacy-spec-writer` only after
  the selected capability has an approved BRD Package or an explicit
  technical-spec-only bypass.

## Gate before advancing

- **Name:** Module synthesis completeness (informal)
- **Check:** all 4 views present AND `module-overview.md` lists at least one
  `CAP-*` capability seed AND View 1 lists `BR-*` rule seeds with
  `evidence_id` and `knowledge_type`
  (`confirmed_from_code` | `inferred_business_rule` | `observed_in_runtime` | `modernization_decision`)
- **Blocks if:** any view missing, no capability seeds, or any BR seed
  lacking evidence linkage

## SME action

- **Required:** yes — every `inferred_business_rule` must be SME-confirmed
  before the Evidence Approval Gate at spec-writing time
- **Ask:** "For each BR-* marked `inferred`: is this rule correct? What
  exceptions exist? Should it be modernized as-is or changed?"
- **Recorded in:** View 1 `review_status` column + `module-overview.md`
  `sme_review` block

## Next card

[`05a-brd-writing.md`](05a-brd-writing.md) — once the 4 views and overview
are approved, produce the BRD Package for the selected `CAP-*` before moving
to spec writing.
