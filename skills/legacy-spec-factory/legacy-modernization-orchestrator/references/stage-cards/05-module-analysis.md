# Stage 05: Module Analysis (4-view synthesis)

**You are here if:** every flow in scope for this module has an approved
`flow-<slug>.md` AND you need to synthesize the module's complete behavior
into the canonical 4 views before writing a `spec.yaml`.

This is the **last reverse-engineering step** before spec writing. Business
rule seeds and capability seeds emerge here.

## Need before starting

- `03_flows/<MODULE-SLUG>/flow-*.md` for every flow (all approved)
- `02_programs/<MODULE-SLUG>/<OBJ>/program-analysis.md` for every program
- `01_inventory/inventory.yaml` (approved)
- SME-confirmed BAU notes for the module (any operational quirks,
  workarounds, undocumented rules)

## Run

- **Skill:** `legacy-ibmi-module-analyzer` (Implemented v0.1.0)
- **Manual fallback:** Build the 4 views by hand following
  `docs/module-analysis-model.md` and the templates in
  `skills/legacy-ibmi-module-analyzer/references/`

## Produce

- **Artifact:** 4 view files + a module overview
  - `module-overview.md` — module identity, in-scope flows, capability seeds (`CAP-*`)
  - `view-1-operation-flow.md` — user/operator perspective + business rule seeds (`BR-*`)
  - `view-2-system-flow.md` — system interaction perspective
  - `view-3-program-flow.md` — program-level sequencing
  - `view-4-data-flow.md` — data lifecycle perspective
- **Save under:** `04_modules/<MODULE-SLUG>/` *(relative to your
  `project.root`, e.g. `docs/XXX260004-demo/04_modules/CREDIT-CHECK/`)*
- **Consumed by:** `legacy-spec-writer`, `legacy-brd-writer` (optional)

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

[`06-spec-writing.md`](06-spec-writing.md) — once the 4 views and overview
are approved.

Optional sidetrack: if stakeholders want a business-facing BRD before the
technical spec, run `legacy-brd-writer` first; the BRD and spec share the
same module-analysis input.
