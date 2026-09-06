---
name: legacy-flow-context-normalizer
description: "Use when scattered Visio, Word, Excel, PDF, PowerPoint, exported diagrams, RAG summaries, SME notes, Function Specs, Technical Designs, Program Specs, File Specs, interface specs, and data dictionaries need draft Mermaid-backed four-view context files for SME review before context intake, module analysis, or BRD generation. Blocks on unauthorized evidence, missing module scope, unreadable opaque files, hidden contradictions, or attempts to treat draft context as approved rules or canonical module flows."
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

# Legacy Flow Context Normalizer

## Purpose

Turn scattered historical documentation and specs into a **draft,
evidence-linked four-view context review package**:

```text
00_context_packages/<MODULE-SLUG>/flow-normalization/
|-- flow-context-index.yaml
|-- source-document-index.yaml
|-- 01-operation-business-flow.md
|-- 02-system-flow.md
|-- 03-program-flow.md
|-- 04-data-flow.md
|-- evidence-map.md
|-- contradiction-log.md
|-- open-questions.md
`-- sme-review-pack.md
```

This skill is the upstream bridge for teams whose knowledge is trapped in
Visio, Word, Excel, PDF, PowerPoint, exported screenshots, Function Specs,
Technical Designs, Program Specs, File Specs, interface specs, data dictionary
extracts, old process decks, runbooks, or SME notes. The four context views
are the normalization target, not a raw-input requirement. This skill makes the
material reviewable, but it does **not** approve context, mint final `BR-*`
rules, or generate a BRD.

These files are context views under `00_context_packages/`, not the canonical
module-analysis artifacts under `04_modules/`. When reporting this step to a
user, call them **draft context views** or a **flow-normalization package**.
Do not say this step created the final four module flows. The canonical
`01-operation-flow.md` / `02-system-flow.md` / `03-program-flow.md` /
`04-data-flow.md` module artifacts are produced later by
`legacy-ibmi-module-analyzer`.

## Boundary

Use this skill before `legacy-module-context-intake` when the team does **not**
yet have SME-reviewed four-view module context.

Do not use it as a replacement for:

- `legacy-ibmi-evidence-intake` when raw source/runtime evidence authorization
  or redaction is unresolved.
- `legacy-module-context-intake` when the four context views are already
  SME-reviewed or explicitly supplied as human-confirmed context.
- `legacy-ibmi-flow-analyzer` when the task is source-backed call-chain
  analysis across IBM i programs.
- `legacy-brd-writer` when the user wants the BRD; BRD generation requires
  approved module context first.

## Required Inputs

- Module slug, business name, draft scope statement, and owner or SME role.
- One or more source documents, specs, or exported readable forms:
  - Visio / diagram exports (`.vsdx`, PDF, SVG, PNG, or image export)
  - Word / runbook / procedure docs
  - Excel / CSV process, application, interface, data dictionary, or CRUD lists
  - PDF / PPT / PPTX decks
  - Function Specs / Functional Specs / requirement catalogues
  - Technical Designs / architecture or integration designs
  - Program Specs / job specs / screen-report specs
  - File Specs / record layouts / table specs / field dictionaries
  - Interface Specs / batch layout specs / API message specs
  - RAG or code-knowledge summaries
  - SME notes, meeting notes, or annotated screenshots
- Evidence authorization signal for every source:
  - approved evidence manifest,
  - synthetic / non-production / public classification, or
  - explicit owner approval for agent review.

## Stop Conditions

Stop and produce only blocking findings if any apply:

| Condition | Route |
| --- | --- |
| Any source/runtime evidence has unknown sensitivity or missing authorization | `legacy-ibmi-evidence-intake` |
| Confidential or production evidence needs redaction and no approved redaction exists | `legacy-ibmi-evidence-intake` |
| Module slug, business name, or scope is missing | module owner / SME clarification |
| No supplied document can be read or extracted into text/table/diagram fragments | request PDF/SVG/PNG/CSV/text export |
| Documents appear to cover multiple modules and no draft boundary can be proposed | SME boundary decision |
| Contradictions are found but the user asks to hide or smooth them over | block; keep `contradiction-log.md` visible |
| Draft flows are requested as approved rules, approved module context, or BRD input without SME review | block; route through SME review first |

Missing one or more of the four standard context views is **not** a stop
condition. Create the missing view file with a placeholder Mermaid node, a `TBD-*`
question, and `coverage.<view>: absent` or `partial`. If no flow can be safely
generated but the authorized documents contain module-relevant clues, produce a
source-quality triage package instead of failing silently. The goal is to
improve user experience by making incomplete inputs reviewable instead of
blocking unless a downstream step would need to invent facts.

## Input Quality Ladder

Classify the input set before drafting flows:

| Level | Signal | Required response |
| --- | --- | --- |
| `L3 strong` | The documents support all four views with visible evidence. | Produce four substantive view files, each with Mermaid flowchart, evidence-linked steps, candidate seeds, and SME questions. |
| `L2 partial` | The documents support one to three views. | Produce substantive views where evidence exists; create Mermaid placeholders and `TBD-*` questions for missing views; route to SME review. |
| `L1 sparse` | Documents are authorized and readable, but no coherent flow sequence can be generated. | Produce the same ten-file package as a source-quality triage artifact: all four view files use placeholders, `open-questions.md` lists the minimum supplement request, and `normalization.status` is `triage_needs_source_enrichment`. |
| `L0 blocked` | Evidence is unauthorized, unreadable, out of scope, or lacks a usable module boundary. | Stop with blocking findings and route to evidence intake, readable export, or SME boundary clarification. |

`L1 sparse` is still useful output. It should identify what was found, why no
flow should be inferred, which source types would unlock the next pass, and
which SME questions can resolve the gap fastest.

If the team has already attempted supplement collection and the source owner
or SME confirms that no additional document, spec, or flow input can be
provided, do not loop forever asking for more. Record an explicit
risk-acceptance decision. Only a named accountable owner may convert
`triage_needs_source_enrichment` to `ready_with_warnings`; the package must
remain `quality_level: L1 sparse`, carry every missing view as `TBD-*`, and
tell downstream skills to treat all context as low-confidence review material,
not confirmed facts.

## Output Contract

Use `references/output-contract.md` for required fields and examples. Start
from the templates under `templates/`.

For deterministic local validation, run:

```bash
python3 skills/legacy-flow-context-normalizer/scripts/validate_flow_context_package.py \
  00_context_packages/<MODULE-SLUG>/flow-normalization
```

For multi-sheet Excel intake, generate an initial `source-document-index.yaml`
fragment draft with:

```bash
python3 skills/legacy-flow-context-normalizer/scripts/extract_excel_fragments.py \
  source-docs/<workbook>.xlsx \
  --module-slug <MODULE-SLUG> \
  --title "<Workbook title>" \
  --owner "<Document owner>" \
  --output 00_context_packages/<MODULE-SLUG>/flow-normalization/source-document-index.yaml
```

The package status in `flow-context-index.yaml` must be one of:

- `draft_needs_sme_review`
- `triage_needs_source_enrichment`
- `ready_for_context_intake`
- `ready_with_warnings`
- `blocked_pending_evidence`
- `blocked_pending_scope`
- `blocked_pending_readable_source`
- `blocked_pending_contradiction_review`

Allowed handoff:

- `draft_needs_sme_review` -> SME review or `legacy-sme-review-facilitator`
- `triage_needs_source_enrichment` -> source owner / SME supplement request
- `ready_for_context_intake` / `ready_with_warnings` -> `legacy-module-context-intake`
- any `blocked_*` -> do not route downstream; record exact remediation in
  `open-questions.md` and `flow-context-index.yaml`

## Step Contract

This skill conforms to the Legacy Spec Factory Step Contract.

### Input

- **Required**: module identity, source document list, evidence authorization,
  and enough readable content to identify either candidate flow evidence or
  module-relevant triage clues.
- **Optional**: existing RAG output, Function Specs, Technical Designs,
  Program Specs, File Specs, interface specs, ARCAD / application inventory
  extracts, data dictionary exports, screen/report samples, meeting notes,
  known SME owner, and reviewed module glossary.
- **Technical-anchor supplements for View 3 / View 4**: API IDs, journey IDs,
  menu IDs, screen IDs, and business data labels are not enough to draw IBM i
  program or data views. For a substantive View 3, request at least one
  AS400 / IBM i program, job, service program, CL/RPG object, or explicit
  API/menu-to-program mapping. For a substantive View 4, request at least one
  AS400 / IBM i PF/LF, SQL table, data area, data queue, printer/display file,
  file spec, DDS/DDL extract, CRUD matrix, or explicit business-data-to-file
  mapping.
- **Input readiness scoring**:
  - `0-5 blocked`: evidence authorization unresolved, module scope missing,
    source files unreadable with no export, or all documents out of scope.
  - `6 minimum_pass`: module identity, authorized readable documents, and at
    least one module-relevant clue are present; if no flow can be produced,
    emit `triage_needs_source_enrichment`.
  - `7-8 usable`: documents cover one or more views with visible source
    provenance, gaps, and contradictions; missing views are represented as
    explicit `TBD-*` questions rather than blockers.
  - `9-10 strong`: each view has multiple corroborating sources, View 3 has
    IBM i program/job anchors, View 4 has IBM i file/table/data-object anchors,
    data dictionary or interface context is present, and SME owner is assigned.

### Execution

- **Procedure**: follow the Workflow below.
- **Allowed inference**: classify document fragments into the four views;
  normalize labels; create candidate flow steps from supplied document content;
  connect repeated system, program, file, and actor names across sources when
  evidence is visible.
- **Forbidden assumptions**: inventing actors, systems, programs, file names,
  field meanings, sequence order, trigger timing, exception handling, manual
  workarounds, business rules, SLAs, or modernization decisions. Do not
  promote API IDs, journey IDs, menu IDs, screen IDs, or business labels into
  AS400 program names or file names.
- **ID policy**: may mint `DOC-*`, `FRAG-*`, `STEP-*`, `SYS-*`, `PGM-*`,
  `DATA-*`, `CAND-*`, `CONFLICT-*`, and `TBD-*` within the draft
  package. Do not mint final `BR-*`, `CAP-*`, `DEC-*`, `AC-*`, or `TC-*`.

### Output

- **Canonical directory**:
  `00_context_packages/<MODULE-SLUG>/flow-normalization/`.
- **Required files**: the ten files listed in Purpose.
- **Required gates**: evidence authorization, readable source, module scope,
  four-view coverage, contradiction visibility, SME review, and no rule
  promotion.
- **Handoff status**: only `ready_for_context_intake` and
  `ready_with_warnings` may feed `legacy-module-context-intake`. A partial
  package may use `ready_with_warnings` only when SME explicitly accepts the
  missing views or gaps as carry-forward TBDs. `triage_needs_source_enrichment`
  must not feed context intake unless it is converted to
  `ready_with_warnings` by a named owner risk-acceptance decision after
  supplement collection has been attempted or declared impossible.

### Validation

- **Mechanical**: all required files exist; the index lists every input and
  output; every view file has status, summary, evidence-linked flow steps,
  candidate seeds, and gaps; every evidence ID referenced by a view appears in
  `evidence-map.md`.
- **Semantic**: no draft flow is presented as approved; contradictions are not
  hidden; View 1 uses business language first; View 2 captures system and
  integration behavior; View 3 captures application/program/job behavior;
  View 4 captures data movement and ownership questions; View 3 uses IBM i
  program/job anchors when available and otherwise carries a supplement TBD;
  View 4 uses IBM i file/table/data-object anchors when available and
  otherwise carries a supplement TBD; BRD functional analysis hints record
  which extracted fragments can feed SME-required BRD areas without treating
  missing hints as invented facts.
- **SME / human approval**: SME or accountable owner confirms module boundary,
  flow sequence, missing or obsolete documents, exception behavior, manual
  steps, and which contradictions block context intake.
- **Blocking conditions**: authorization gap, no readable source, no usable
  module boundary, hidden contradiction, missing evidence links for major flow
  steps that are stated as facts, or absent SME decision when package claims
  readiness. Missing flow coverage by itself is not blocking when it is
  captured as `TBD-*` and the package remains draft or SME-accepted
  `ready_with_warnings`. If all flow coverage is absent but authorized
  module-relevant clues exist, use `triage_needs_source_enrichment` rather than
  a blocked status. If the owner explicitly accepts sparse-input risk, convert
  to `ready_with_warnings` with `quality_level: L1 sparse`, all flow gaps still
  visible, and downstream restrictions recorded.

Emit a Step Validation Report (see
`../legacy-step-contract/templates/step-validation-report.md`) with status
`pass`, `pass_with_warnings`, or `blocked` when reporting upward to the
orchestrator.

## Workflow

1. **Resolve module identity**
   - Confirm `MODULE-SLUG`, business name, scope statement, owner, and SME role.
   - If one document bundle covers multiple modules, split or block until SME
     assigns boundaries.

2. **Gate evidence authorization**
   - Check source sensitivity, redaction, and owner approval before reading
     content.
   - If **any** source has unknown authorization, route the entire package to
     `legacy-ibmi-evidence-intake`. Do not proceed with only the authorized
     subset; authorization must be resolved for every document before
     normalization begins.
   - Exception: if an unauthorized document is clearly out of scope and the
     owner explicitly confirms it can be excluded, set its `readable_status` to
     `not_needed`, record the exclusion in `open-questions.md`, and proceed
     with the remaining authorized documents.

3. **Inventory source documents**
   - Create `source-document-index.yaml`.
   - Assign stable `DOC-*` IDs and record path, format, source document role,
     readable extraction method, sensitivity, owner, date, and confidence.
   - Keep `format` (file type such as `.xlsx` or `.docx`) separate from
     `source_type` (document role such as `function_spec`, `technical_design`,
     `program_spec`, `file_spec`, `interface_spec`, or `flow_diagram`).
   - Follow `references/source-classification.md` for format-specific notes.

4. **Extract candidate fragments**
   - Extract only enough content needed for flow normalization.
   - Mint `FRAG-*` IDs for relevant diagram nodes, table rows, paragraphs,
     slide elements, or SME notes.
   - Preserve page, sheet, slide, row, shape, or section references.
   - For `.xlsx` workbooks, prefer the bundled
     `scripts/extract_excel_fragments.py` helper. It enumerates every sheet,
     treats the first non-empty row as headers, emits one `FRAG-*` per
     non-empty data row, and classifies fragments by sheet/header keywords into
     Operation / Business, System, Program, Data, or `cross_view`. Sheet names
     such as `Function Spec`, `Technical Design`, `Program Spec`, and
     `File Spec` are classification signals, not mandatory sheets.

5. **Classify input quality**
   - Set `quality_level` to `L3 strong`, `L2 partial`, `L1 sparse`, or
     `L0 blocked`.
   - Record the reason in `flow-context-index.yaml.normalization.
     decision_reason`.
   - For `L1 sparse`, do not invent sequence or edges. Continue to create the
     ten-file package as a triage artifact with all four views marked
     `absent`, placeholder Mermaid nodes, and prioritized supplement requests.

6. **Classify fragments into four views**
   - Operation / Business Flow: actors, BAU sequence, approvals, manual steps,
     exceptions, customer or operational outcome.
   - System Flow: upstream/downstream systems, interfaces, batches, queues,
     files, schedules, security/SLA hints.
   - Program Flow: IBM i programs, jobs, service programs, CL/RPG objects,
     call hints, trigger points, and technical branching. API IDs, journey
     IDs, menu IDs, and screen IDs may appear only as trigger or boundary
     context unless the source explicitly maps them to IBM i programs.
   - Data Flow: IBM i files/tables, PF/LF objects, SQL tables, data areas,
     data queues, display/printer files, fields, CRUD direction, derivation,
     retention, and ownership. Business data labels may appear only as
     descriptions unless mapped to concrete IBM i objects.

7. **Draft each view**
   - Use `templates/view-template.md`.
   - Include a `Mermaid Flow Diagram` in every view. The diagram is the
     SME-readable flow surface; the evidence table remains the traceability
     surface.
   - Run the View 3 / View 4 technical-anchor gate before drawing diagrams:
     - If View 3 evidence has API/menu/journey/screen labels but no IBM i
       program/job/object names, do **not** draw those labels as program nodes.
       Create a placeholder node and `TBD-*` asking for API/menu-to-program
       mapping, inventory, ARCAD export, DSPPGMREF/call graph, program spec,
       or SME confirmation.
     - If View 4 evidence has business data labels but no IBM i file/table/
       data-object names, do **not** draw those labels as data nodes. Create a
       placeholder node and `TBD-*` asking for file specs, DDS/DDL, data
       dictionary, CRUD matrix, File I/O map, or SME mapping.
   - Draw Mermaid edges only when the source evidence or SME note supports the
     sequence. Mark uncertain nodes as `(needs SME review)` instead of making
     the diagram look approved.
   - Keep every major step evidence-linked and marked `needs_sme_review`.
   - Put technical names in `Evidence Basis` when the view is business-facing.
   - If a view has no usable source fragments, still create the view file with
     one Mermaid placeholder node, one evidence-linked placeholder row pointing
     to the available source set or `TBD-*`, and a blocking or non-blocking SME
     question. Mark coverage as `absent`, not `blocked`, unless the package
     would otherwise invent facts.

8. **Build evidence map**
   - Use `templates/evidence-map.md`.
   - Map every `DOC-*` / `FRAG-*` / source row to the views that use it.

9. **Carry contradictions and gaps**
   - Use `templates/contradiction-log.md` and `templates/open-questions.md`.
   - Keep obsolete-document signals visible rather than deleting them.
   - Ask SME to decide whether a contradiction is blocking, obsolete, or a real
     alternate path.

10. **Prepare SME review package**
   - Use `templates/sme-review-pack.md`.
   - Group questions by view and prioritize blockers first.
   - Include explicit approval choices; do not ask SME to review raw dumps.

11. **Set handoff status**
    - `draft_needs_sme_review` when flow content is usable but SME decision is
      not recorded.
    - `triage_needs_source_enrichment` when authorized documents are readable
      and module-relevant, but no flow sequence should be generated. Route to
      source owner / SME supplement request, not BRD or context intake.
    - Convert `triage_needs_source_enrichment` to `ready_with_warnings` only
      when a named SME/source owner records that no additional document, spec,
      or flow input can be provided and accepts carrying the gaps forward.
      Preserve
      `quality_level: L1 sparse`; do not upgrade coverage or confidence.
    - `ready_for_context_intake` only when SME review confirms all four
      context views for intake.
    - `ready_with_warnings` only when unresolved items are explicitly
      non-blocking and carried into `open-questions.md`; this is the preferred
      status for SME-accepted partial packages.
    - `blocked_*` when a downstream skill would need to invent facts.

12. **Validate**
    - Run the bundled validator:
      ```bash
      python3 skills/legacy-flow-context-normalizer/scripts/validate_flow_context_package.py \
        --allow-draft 00_context_packages/<MODULE-SLUG>/flow-normalization
      ```
    - Fix every reported finding, then re-run until the validator outputs
      `OK: flow context package is structurally valid`.
    - Do not route to SME review or context intake until the validator passes.

## Handoff

After SME approval, run `legacy-module-context-intake` with:

- the four context-view files from this package,
- `evidence-map.md`,
- `contradiction-log.md`,
- `open-questions.md`,
- `sme-review-pack.md` or the recorded SME decision log,
- evidence authorization metadata.

Do not hand this package directly to `legacy-brd-writer`.

For sparse packages that were owner-accepted as `ready_with_warnings`, tell
`legacy-module-context-intake`:

- this is `quality_level: L1 sparse`,
- missing flows are accepted carry-forward TBDs, not confirmed absence,
- no candidate may become an approved fact, `BR-*`, or BRD claim from this
  package alone,
- downstream module analysis must keep confidence low until corroborated by
  source, runtime evidence, or SME decision.

## Version

- v0.1.0 (2026-05-27): Initial document-to-four-view-context normalization skill.
- v0.1.1 (2026-05-27): Added deterministic multi-sheet `.xlsx` extraction
  helper that emits `DOC-*` and `FRAG-*` rows for `source-document-index.yaml`.
- v0.1.2 (2026-05-27): Required Mermaid flow diagrams in every normalized
  view while keeping evidence tables as the traceability source of truth.
- v0.1.3 (2026-05-27): Softened missing-flow handling so partial four-view
  packages can proceed as drafts or SME-accepted warnings instead of blocking.
- v0.1.4 (2026-05-27): Added an input quality ladder and
  `triage_needs_source_enrichment` status for authorized sparse inputs where no
  flow can be safely generated.
- v0.1.5 (2026-05-27): Added the owner risk-acceptance path for cases where
  additional flow input cannot be provided; sparse triage may proceed as
  `ready_with_warnings` only with explicit sign-off and low-confidence
  downstream restrictions.
- v0.1.6 (2026-05-28): Expanded raw input coverage beyond existing flow
  artifacts to Function Specs, Technical Designs, Program Specs, File Specs,
  interface specs, and data dictionaries while keeping all such sources
  optional and evidence-linked.
- v0.1.7 (2026-05-28): Added advisory BRD functional-analysis hints so raw
  flow/context fragments can surface likely inputs for BRD sections 1-9 and
  optional sections 10-12 without making absent facts look confirmed.
- v0.1.8 (2026-05-29): Clarified canonical timing: this skill creates draft
  context views under `00_context_packages/`, while final module four-flow
  artifacts are produced only by `legacy-ibmi-module-analyzer`.
- v0.1.9 (2026-05-29): Added View 3 / View 4 technical-anchor gates so API,
  journey, menu, screen, and business data labels are not substituted for IBM i
  program names or file names. Sparse technical evidence now produces explicit
  supplement TBDs instead of misleading diagrams.
