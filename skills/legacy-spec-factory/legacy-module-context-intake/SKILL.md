---
name: legacy-module-context-intake
description: Normalize external RAG or code-knowledge-graph output, human-confirmed four-view module context, or owner-accepted sparse flow-normalization output into a traceable `00_context_packages/<MODULE-SLUG>/` package. Use when a team already has module-first context, RAG hydration output, source snippets, field dictionary mappings, impact scope, contradictions, retrieval gaps, four reviewed context views, or `legacy-flow-context-normalizer` output accepted as `ready_with_warnings` and needs a safe handoff to `legacy-ibmi-module-analyzer` or BRD preparation. Blocks on unauthorized or unredacted evidence, missing module scope, hidden contradictions, or attempts to promote RAG candidates or sparse-context TBDs into approved business rules or canonical module flows.
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

# Legacy Module Context Intake

## Purpose

Turn external RAG / code knowledge graph output plus human-confirmed module
context into a portable, evidence-tagged context package:

```text
00_context_packages/<MODULE-SLUG>/
|-- context-index.yaml
|-- 01-operation-business-flow.md
|-- 02-system-flow.md
|-- 03-program-flow.md
|-- 04-data-flow.md
|-- rag-evidence-map.md
|-- contradiction-log.md
`-- open-questions.md
```

This skill is a **module-first intake bridge**. It makes RAG output usable by
Legacy Spec Factory, but it does not approve business rules, replace source
analysis, or bypass SME review.

The four Markdown files in this package are normalized context views. They
may seed module analysis, but they are not the final four module-flow artifacts
under `04_modules/`. When reporting this step to a user, say that context
views were normalized for module analysis; do not say that the canonical
module flows were created.

## Use This Skill When

- A team supplies a business module or subsystem context before running the
  usual program-by-program reverse chain.
- External RAG output includes `rag-run-index.yaml`, source snippets, field
  dictionary mappings, impact scope, contradictions, or retrieval gaps.
- `legacy-flow-context-normalizer` produced `ready_with_warnings` with
  `quality_level: L1 sparse` and a named `risk_acceptance.status: accepted`
  because no additional flow input can be provided.
- The user asks to ingest, normalize, package, or prepare a RAG output bundle
  under `00_context_packages/<MODULE-SLUG>/`.
- A BRD or module analysis should start from human-confirmed four-view context
  instead of from raw source only.

## Do Not Use This Skill When

- The user only has raw IBM i source, DDS, job logs, spool, or DB extracts with
  unknown authorization or sensitivity. Route to `legacy-ibmi-evidence-intake`.
- The user wants an approved module analysis. Route the finished context
  package to `legacy-ibmi-module-analyzer`.
- The user wants `spec.yaml` or final `BR-*` rules. Route through
  `legacy-ibmi-module-analyzer`, `legacy-brd-writer`, and
  `legacy-spec-writer`.
- The task is to build or query the external RAG system itself. This skill
  consumes file-based RAG output only.

## Required Inputs

- Module slug, business name, and scope statement.
- Human-confirmed or explicitly draft four-view module context views:
  Operation / Business Flow, System Flow, Program Flow, and Data Flow.
- RAG output bundle when available, preferably with:
  - `rag-run-index.yaml`
  - `flow-hydration-summary.md`
  - `source-snippets.md`
  - `field-dictionary-context.md`
  - `impact-scope.md`
  - `contradictions.md`
  - `retrieval-gaps.md`
- Evidence authorization signal for source/runtime content:
  - approved evidence manifest from `legacy-ibmi-evidence-intake`, or
  - explicit RAG metadata proving the bundle is synthetic, public,
    non-production, or otherwise approved for agent review.

## Stop Conditions

Stop and produce only blocking findings / requested remediation if any apply:

| Condition | Route |
| --- | --- |
| Source/runtime evidence sensitivity is unknown | `legacy-ibmi-evidence-intake` |
| Confidential evidence is present without approved redaction | `legacy-ibmi-evidence-intake` |
| Module slug, business name, or scope is missing | module owner / SME clarification |
| Four-view context is absent and there is no owner-accepted sparse flow-normalization package | requester must provide module context, accept sparse-input risk, or route to normal inventory/program/flow chain |
| RAG contradictions are missing, blank without evaluated checks, or hidden in prose | rerun / repair RAG bundle before intake |
| RAG candidate rules are requested as approved `BR-*` | block; candidates stay `needs_sme_review` seeds only |
| Source paths, snippet IDs, or dictionary IDs cannot be traced | record `TBD-*` in `open-questions.md`; do not smooth over |

## Output Contract

Use `references/output-contract.md` for required fields and examples. Use the
templates under `templates/` as scaffolding.

For deterministic local validation, run:

```bash
python3 skills/legacy-module-context-intake/scripts/validate_context_package.py \
  00_context_packages/<MODULE-SLUG>/
```

The package status in `context-index.yaml` must be one of:

- `ready_for_module_analysis`
- `ready_with_warnings`
- `blocked_pending_evidence`
- `blocked_pending_scope`
- `blocked_pending_contradiction_review`

Allowed handoff:

- `ready_for_module_analysis` or `ready_with_warnings` -> route to
  `legacy-ibmi-module-analyzer`.
- Any `blocked_*` status -> do not route downstream; list exact remediation in
  `open-questions.md` and `context-index.yaml`.

## Step Contract

This skill conforms to the Legacy Spec Factory Step Contract.

### Input

- **Required**: module slug, module business name, scope statement, four-view
  context, a RAG hydration summary that contains all four views, or an
  owner-accepted sparse `legacy-flow-context-normalizer` package; evidence
  authorization for every source/runtime artifact referenced.
- **Optional**: approved evidence manifest, inventory, program analyses, flow
  analyses, SME notes, architecture diagrams, dictionary export, ARCAD REF
  export, runtime sample index.
- **Input readiness scoring**:
  - `0-5 blocked`: evidence authorization unresolved, module scope missing,
    contradictions missing, no usable four-view context, and no accepted sparse
    package.
  - `6 minimum_pass`: module identity, four views, RAG provenance, and explicit
    open questions are present; or sparse flow-normalization output has named
    owner risk acceptance and all missing views carried as TBDs.
  - `7-8 usable`: source snippets, dictionary mappings, impact scope, and
    contradiction checks are traceable.
  - `9-10 strong`: approved evidence manifest, SME-reviewed four-view context,
    source/runtime snippets, dictionary ownership, and resolved high-severity
    contradictions are supplied.

### Execution

- **Procedure**: follow the Workflow below.
- **Allowed inference**: normalize and cross-link supplied context; derive
  evidence mappings from snippet tables; classify gaps and contradictions
  already present in the bundle.
- **Forbidden assumptions**: inventing module boundaries, systems, actors,
  flows, data owners, dictionary meanings, normal operating frequency,
  business rules, or modernization decisions.
- **ID policy**: may mint `TBD-*` and reuse upstream `RAG-*`, `SNP-*`, `RUN-*`,
  `DD-*`, `EV-*`, `FLOW-*`, `OBJ-*`, `MODULE-*`, and `VIEW-*`. Do not mint
  final `BR-*`, `CAP-*`, `DEC-*`, `AC-*`, or `TC-*`.

### Output

- **Canonical directory**: `00_context_packages/<MODULE-SLUG>/`.
- **Required files**: the eight files listed in Purpose.
- **Required gates**: evidence authorization, provenance completeness,
  contradiction visibility, four-view coverage, and open-question carry-forward.
- **Handoff status**: only `ready_for_module_analysis` and
  `ready_with_warnings` may feed `legacy-ibmi-module-analyzer`. For
  owner-accepted sparse input, `ready_with_warnings` means low-confidence
  context only, not approval of any missing flow.

### Validation

- **Mechanical**: all required files exist; `context-index.yaml` names every
  input bundle and output file; every RAG evidence ID referenced in a view is
  listed in `rag-evidence-map.md`; every contradiction/gap has an owner or
  routing destination.
- **Semantic**: no RAG candidate is promoted to an approved business rule; all
  claims preserve knowledge type and evidence strength; contradictory evidence
  remains visible; candidate seeds explain the business signal first and keep
  program names, file names, field names, snippet IDs, and runtime object names
  in evidence context unless the view is explicitly technical; BRD functional
  analysis hints preserve which context can feed SME-required BRD areas without
  inventing channels, touchpoints, interfaces, dependencies, security, or
  source-document mappings.
- **Sparse-input restriction**: if the upstream package is
  `quality_level: L1 sparse`, preserve every missing view as a `TBD-*`, mark
  evidence strength low, and do not create approved facts, `BR-*`, or BRD-ready
  claims from the sparse context alone.
- **SME / human approval**: module owner confirms business name and scope;
  data owner or dictionary owner confirms approved dictionary mappings where
  they are used as business terminology.

## Workflow

1. **Resolve module identity**
   - Confirm `MODULE-SLUG`, business name, scope statement, and module owner.
   - Normalize slug to uppercase hyphenated form without renumbering existing
     IDs.

2. **Check evidence authorization**
   - Read RAG sensitivity/provenance metadata and any evidence manifest.
   - Block if source/runtime artifacts are not approved for agent review.

3. **Inventory RAG bundle files**
   - Record each supplied input in `context-index.yaml`.
   - Capture run ID, source snapshot, dictionary version, ARCAD REF snapshot,
     corpus root, and generation timestamp when present.
   - If input comes from `legacy-flow-context-normalizer`, record
     `flow-normalization/flow-context-index.yaml`, `quality_level`, and
     `risk_acceptance` status. If `quality_level: L1 sparse` lacks accepted
     risk, route back to source-owner supplement request.

4. **Normalize four views**
   - Create one Markdown file per view using the supplied module context.
   - Every factual claim must include a source row, evidence ID, or SME note.
   - Keep candidate rules as candidates or seeds, never approved rules.
   - Phrase candidate seeds with business meaning first. In View 1 this means a
     business rule / capability / exception candidate; in Views 2-4 this may be
     a system, program, or data analysis focus, but it must still say what
     business behavior or decision depends on the technical check.
   - Keep program names, file names, field names, node IDs, source paths, and
     raw RAG IDs in `Evidence Basis`, not as the main candidate statement.
   - For owner-accepted sparse input, copy placeholder views forward as
     low-confidence context and preserve missing sequence, actor, system,
     program, and data questions as carry-forward `TBD-*`.

5. **Build evidence map**
   - Convert source snippets, runtime observations, dictionary mappings, and
     impact-scope rows into `rag-evidence-map.md`.
   - Preserve original IDs such as `SNP-*`, `RUN-*`, `DD-*`, `RAG-CAND-*`, and
     `RAG-CONFLICT-*`.

6. **Carry contradictions forward**
   - Copy every contradiction into `contradiction-log.md`.
   - If the RAG bundle says no contradictions exist, include the evaluated
     checks that justify that result.

7. **Carry gaps and assumptions forward**
   - Convert retrieval gaps, missing mappings, and non-blocking assumptions
     into `open-questions.md`.
   - Mint `TBD-*` only for questions that need Legacy Spec Factory tracking.

8. **Set handoff decision**
   - If any hard gate failed, set a `blocked_*` status and name the upstream
     owner.
   - Otherwise set `ready_for_module_analysis` or `ready_with_warnings` and
     route to `legacy-ibmi-module-analyzer`.

## Handoff To Module Analyzer

When the package is ready, tell the next agent:

```text
Use legacy-ibmi-module-analyzer with
00_context_packages/<MODULE-SLUG>/ as module-first context.
Treat RAG snippets and runtime observations as evidence context only.
Preserve contradiction-log.md and open-questions.md as TBD inputs.
Do not promote candidate rules without SME review.
Preserve business-signal-first candidate seeds; do not turn evidence object
names into capability boundaries.
Generate the canonical four module views only under
04_modules/<MODULE-SLUG>/.
```

## References

- `references/output-contract.md` - required file shape and field-level rules.
- `templates/` - scaffolding for the eight required output files.
- `examples/credit-check-rag-positive/` - frozen positive context package.
- `examples/unauthorized-evidence-negative/` - expected blocked response.
- `scripts/validate_context_package.py` - local structural validator.
- `../../docs/rag-setup-detail.md` - external RAG bundle boundary.
- `../../docs/rag-output-sample/` - compact synthetic RAG output example.
- `../../docs/module-analysis-model.md` - downstream four-view module model.
- `../../docs/evidence-and-knowledge-taxonomy.md` - knowledge type and evidence
  strength vocabulary.

## Version History

- v0.1.3 (2026-05-28): Added advisory BRD functional-analysis coverage hints
  to `context-index.yaml` so downstream module analysis can preserve channel,
  UI, interface, validation, error, and dependency gaps without inventing them.
- v0.1.4 (2026-05-29): Clarified that intake view files are context-only
  inputs and that canonical four-flow module artifacts are generated only by
  `legacy-ibmi-module-analyzer`.
- v0.1.1 (2026-05-26): Added business-signal-first candidate seed guidance so
  RAG/program/file evidence does not become the business-facing statement.
- v0.1.2 (2026-05-27): Accepted owner-risk-approved sparse
  `legacy-flow-context-normalizer` packages as low-confidence
  `ready_with_warnings` input while preserving TBDs and forbidding approved
  facts from sparse context alone.
- v0.1.0 (2026-05-21): Initial module context intake skill.
