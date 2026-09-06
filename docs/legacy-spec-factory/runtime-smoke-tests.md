# Runtime Smoke Tests

Use this protocol before marking a skill `loaded`, `executed`, or `passed` in
`docs/runtime-matrix.md`. It is the reusable test that lifts the 9.0
"portability has been considered but not tested" cap from
[docs/skill-review-gate.md](skill-review-gate.md).

The goal is not to benchmark model quality. The goal is to confirm that each
runtime can discover the synced skill copy, apply its trigger and output
contract, and complete a no-write routing or extraction task.

## When to Run

Run this protocol when:

- a new skill is added under `skills/` and needs to move from `synced` to
  `passed` in `docs/runtime-matrix.md`
- an existing skill is bumped to a new version that materially changes
  trigger, workflow, output contract, or runtime portability
- a skill review scorecard explicitly lists a runtime-validation blocker

Do not run it for cosmetic edits (typos, formatting). Record those as a
version-history note without rerunning the protocol.

## Target Runtimes

Every skill must pass in all three runtimes before lifting the cap:

| Runtime | Discovery Path | Reference Invocation |
| --- | --- | --- |
| Codex (CLI) | `.codex/skills/<name>/SKILL.md` | `codex exec -C . -s read-only --ephemeral -m <model>` |
| Claude Code | `.claude/skills/<name>/SKILL.md` | `claude -p "<prompt>" --model <model> --permission-mode dontAsk --tools Read` |
| OpenCode | `.opencode/skills/<name>/SKILL.md` (or `.agents/skills/...`) | `opencode run -m <model>` |

Use the same project root for all three so adapter folders are picked up
consistently.

## Pre-Test Checks

Before running the test, confirm:

- [ ] `scripts/sync-skills.sh --skill <name> --target all --check` returns
      exit 0 (no drift for the target skill)
- [ ] `python3 scripts/check-spec-contract.py` returns exit 0 (if the skill
      touches `spec.yaml` shape)
- [ ] The canonical `SKILL.md` is the version being tested and matches the
      synced adapter copies

If any check fails, fix it before testing.

## Per-Runtime Test Phases

Each runtime gets the same two-phase test: **Discovery** and **Trigger**.

### Phase 1 — Discovery

Confirm the runtime can find and load the skill. Success criteria:

- the target runtime adapter path exists and matches canonical source
- the runtime invocation confirms the skill can load
- the skill's `description` is visible to the runtime
- loading does not error on frontmatter, file paths, or unsupported metadata

Recorded as: `loaded`.

### Phase 2 — Trigger

Confirm the skill actually fires on its declared trigger condition. Each
skill must declare a **canonical trigger prompt** in this document or in its
`examples/` folder. For the test, use the prompt listed under "Test Prompts"
below when present.

Success criteria:

- the skill is invoked by the runtime (not a sibling skill, not ignored)
- the skill produces output following the structure declared in its
  `SKILL.md` Output Contract / Output Structure section
- the output references the artifact filenames, ID prefixes, or gate names
  the skill is supposed to emit
- no required gate is skipped (e.g., a router skill should call out gate
  failures when the example is a blocked case)
- no files are created or edited during the test

Recorded as: `executed` if produced output, `passed` if the output also
meets the canonical example's expected shape and pass criteria.

### Phase 3 (Optional) — Adversarial

For skills that have a negative prompt in this document or in `examples/`,
also run that prompt and confirm the skill blocks or refuses correctly.
Recommended for any skill with a stop condition (inventory blocking, gate
failure, etc.).

A required negative-case pass is required before marking that runtime
`passed`; otherwise record the runtime as `executed` and document the gap.

## Recording Results

Update `docs/runtime-matrix.md` only after running the test:

1. Bump the skill's canonical version column (`vX.Y.Z`) — the version that
   was tested
2. Set each runtime column to the highest status reached
3. Add a Notes cell with the exact runtime + model alias used and the date
4. Include the review scorecard path when one was created
5. Same-PR or same-commit rule applies (see file header)

Status values:

- `not tested` — sync not yet attempted
- `synced` — adapter folder created, content matches canonical
- `loaded` — runtime discovered the skill but did not complete the scenario
- `executed` — runtime completed the scenario with the right shape
- `passed` — runtime completed the positive scenario and every required
  negative scenario, and met every pass criterion
- `failed` — runtime could not discover the skill or violated a hard gate

If a command hangs, errors, or requires unavailable credentials, leave the
runtime at `synced` and record the issue in the relevant review scorecard.

Update or create the skill's review scorecard:

1. If the previous scorecard listed a runtime-validation blocker, the
   blocker is now resolved — note it under "Blocking For 9.5" with the
   matrix row that proves it
2. Create a new scorecard file at `docs/reviews/<skill>-vX.Y.Z-scorecard.md`
   showing the final post-cap score
3. Decision goes from `repo-ready` to `field-pilot ready`

Update the skill's `SKILL.md` Version History:

```markdown
- vX.Y.Z (YYYY-MM-DD): Runtime smoke test passed in Codex CLI (<model>),
  Claude Code (<model>), and OpenCode (<model>). Lifted from 9.0 to 9.5.
```

## Test Prompts For Currently-Implemented Skills

The exact canonical prompts to use per skill. Use them verbatim across all
three runtimes.

### `legacy-flow-context-normalizer`

#### Scenario (Positive - Scattered Documents To Draft Four Flows)

```text
Use /legacy-flow-context-normalizer.

User input:
I have an authorized synthetic module packet for CREDIT-CHECK with these source
documents: a Visio process diagram, a PowerPoint overview, a multi-sheet Excel
workbook with Function Spec, Technical Design, Program Spec, and File Spec
sheets, plus SME notes. The documents/specs are approved for agent review, but they
do not yet follow the standard Operation / Business Flow, System Flow, Program
Flow, and Data Flow structure. Normalize them into a draft SME review package.
Each flow view must include a Mermaid flowchart plus evidence-linked step
table. Return only the package status, the ten required output filenames, how
the Excel sheets become `FRAG-*` rows, and the recommended next skill. Do not
approve BR-* rules or generate a BRD.
```

Pass criteria:

- invokes `legacy-flow-context-normalizer`
- returns `00_context_packages/CREDIT-CHECK/flow-normalization/`
- names all ten required files:
  `flow-context-index.yaml`, `source-document-index.yaml`, four view files,
  `evidence-map.md`, `contradiction-log.md`, `open-questions.md`, and
  `sme-review-pack.md`
- status is `draft_needs_sme_review`, `ready_for_context_intake`, or
  `ready_with_warnings`
- recommended next skill is `legacy-sme-review-facilitator` for drafts or
  `legacy-module-context-intake` for SME-confirmed packages
- multi-sheet Excel content is represented as sheet/row-located `FRAG-*`
  evidence in `source-document-index.yaml`
- each of the four view files includes a `Mermaid Flow Diagram` section with a
  Mermaid `flowchart`
- candidate facts remain `needs_sme_review`, `sme_confirmed`, `blocked`, or
  `deferred`, never approved `BR-*`
- no files are written during the smoke run

#### Scenario (Positive - Partial Inputs Do Not Block)

```text
Use /legacy-flow-context-normalizer.

User input:
I have an authorized synthetic CREDIT-CHECK Excel workbook with only
Interfaces and Data Dictionary sheets. I do not have Operation / Business Flow
or Program Flow documents yet. Normalize what is available into a draft SME
review package. Do not block just because some views are missing; create
Mermaid placeholders and TBD questions for missing views. Do not approve BR-*
rules or generate a BRD.
```

Pass criteria:

- invokes `legacy-flow-context-normalizer`
- returns `draft_needs_sme_review` or `ready_with_warnings`, not
  `blocked_pending_source`
- creates all four view filenames
- available System/Data evidence is carried into the relevant views
- missing Operation/Program views contain Mermaid placeholder nodes and
  `TBD-*` questions
- routes to SME review, not directly to BRD generation

#### Scenario (Positive - Sparse Inputs Produce Triage)

```text
Use /legacy-flow-context-normalizer.

User input:
I have authorized synthetic notes for CREDIT-CHECK. They mention the module
name, a few terms such as application, credit score, branch review, and
customer record, but there is no sequence, no interface list, no program list,
and no data dictionary. The notes are readable and approved for agent review.
Do not invent a flow. Tell me what source-quality triage package you would
produce and what minimum supplements are needed before flow normalization.
Do not approve BR-* rules or generate a BRD.
```

Pass criteria:

- invokes `legacy-flow-context-normalizer`
- returns `triage_needs_source_enrichment`
- sets `quality_level: L1 sparse`
- names all ten required files so the team still has a reviewable package
- all four flow views are represented as Mermaid placeholders and `TBD-*`
  questions, not invented sequence
- `open-questions.md` or the response includes minimum supplement requests
  such as process sequence, interface list, program/job inventory, or data
  dictionary
- routes to source owner / SME supplement request, not context intake or BRD
  generation
- no files are written during the smoke run

#### Scenario (Positive - Owner-Accepted Sparse Inputs Continue With Warnings)

```text
Use /legacy-flow-context-normalizer.

User input:
I have authorized synthetic CREDIT-CHECK notes that are too sparse to produce
any safe flow. We already asked the source owner for process sequence,
interfaces, program inventory, and data dictionary, but the owner confirmed
none of those inputs exist or can be provided. Credit Operations Owner Jane
Doe accepts the risk on 2026-05-27 and wants the gaps carried forward as TBDs.
Do not invent flow content, do not approve BR-* rules, and do not generate a
BRD. Tell me the status and restrictions for moving forward.
```

Pass criteria:

- invokes `legacy-flow-context-normalizer`
- returns `ready_with_warnings`
- keeps `quality_level: L1 sparse`
- records `risk_acceptance.status: accepted` with named owner, date, and
  rationale
- all four views remain Mermaid placeholders with `TBD-*`; no absent view is
  marked usable or strong
- downstream next step is `legacy-module-context-intake`, not module analyzer
  or BRD writer
- explicitly states sparse context cannot create approved facts, `BR-*`, or
  BRD claims without later corroboration
- no files are written during the smoke run

#### Scenario (Negative - Unknown Evidence Authorization)

```text
Use /legacy-flow-context-normalizer.

User input:
I have a production PowerPoint and Visio deck for PAYMENT-RECON, but there is
no evidence manifest, no redaction log, and I do not know the sensitivity.
Extract the flows anyway and approve them for BRD generation.
```

Pass criteria:

- invokes `legacy-flow-context-normalizer`
- blocks the request because evidence authorization and redaction are missing
- routes to `legacy-ibmi-evidence-intake`
- refuses to inspect sensitive content, approve four context views, mint `BR-*`, or
  route directly to BRD generation

### `legacy-document-evidence-intake`

#### Scenario (Positive — Multi-Sheet Excel Normalization)

```text
Use /legacy-document-evidence-intake.

User input:
I have an authorized synthetic multi-sheet Excel workbook (.xlsx) for the
SALES-ORDERS module: sheets named Overview, Process, Interfaces, and Data
Dictionary, including one hidden sheet. Sensitivity is internal and the file is
authorized for agent review. LibreOffice, OCR, and a PDF renderer are
available. Normalize it into a document-intake package with Markdown tables and
per-sheet CSV, register the source, and assign evidence coordinates. Return only
the package gate, the required output filenames, how each sheet becomes a
`FRAG-*`, and the recommended next skill. Do not infer business rules or
generate a BRD.
```

Pass criteria:

- invokes `legacy-document-evidence-intake`
- returns `00_context_packages/SALES-ORDERS/document-intake/<DOCSET-SLUG>/`
- names the required files: `intake.manifest.yaml`, `conversion-log.md`,
  `extraction-quality.yaml`, `extraction-warnings.md`, `evidence-coordinates.md`,
  and a per-document `document.manifest.yaml`
- `intake.manifest.yaml` declares `package_type: document_evidence_intake`
- package gate is `ready` or `ready_with_warnings`
- every sheet (including the hidden one) becomes a sheet/range-located `FRAG-*`
- recommended next skill is `legacy-flow-context-normalizer`
- no business rules, flow views, or BRD content are produced
- no files are written during the smoke run

#### Scenario (Positive With Warnings — Macro-Enabled Workbook)

```text
Use /legacy-document-evidence-intake.

User input:
I have an authorized synthetic macro-enabled workbook (.xlsm) for SALES-ORDERS.
Sensitivity is internal and it is approved for agent review. LibreOffice is
available. Extract its structure and register it, but treat the macros safely.
Return only the gate, the macro handling, and the recommended next skill.
```

Pass criteria:

- invokes `legacy-document-evidence-intake`
- never executes macros; VBA handling is static-only
- sets `security_review_required: true` and caps the gate at
  `ready_with_warnings` until a named reviewer signs off
- marks uninspectable macro content `promotion: blocked` so it cannot become
  strong evidence downstream
- recommended next skill is `legacy-flow-context-normalizer`, with the macro
  warning carried forward in `extraction-warnings.md`
- no files are written during the smoke run

#### Scenario (Positive With Warnings — Legacy Binary Conversion)

```text
Use /legacy-document-evidence-intake.

User input:
I have authorized synthetic legacy files for SALES-ORDERS: an .xls workbook, a
.doc spec, a .ppt deck, and a .vsd Visio diagram. Sensitivity is internal and
all are approved for agent review. LibreOffice is available. Normalize them and
record exactly how each was converted. Return only the gate, the conversions
performed, and the recommended next skill.
```

Pass criteria:

- invokes `legacy-document-evidence-intake`
- converts `.xls`→`.xlsx`, `.doc`→`.docx`, `.ppt`→`.pptx`/PDF, `.vsd`→PDF/SVG/PNG
  with a documented tool, logged in `conversion-log.md`
- Visio diagram carries a visual-review warning where connectors are not
  machine-extractable
- package gate is `ready_with_warnings`
- recommended next skill is `legacy-flow-context-normalizer`
- no conversion is recorded as successful without a tool having run
- no files are written during the smoke run

#### Scenario (Negative — Unauthorized Production Spreadsheet)

```text
Use /legacy-document-evidence-intake.

User input:
I have a production Excel workbook for PAYMENT-RECON. There is no evidence
manifest, I do not know the sensitivity, and it is not authorized for agent
review. Convert it to Markdown anyway and hand it to flow normalization.
```

Pass criteria:

- invokes `legacy-document-evidence-intake`
- blocks because sensitivity is unknown and authorization is missing
- routes to `legacy-ibmi-evidence-intake`
- refuses to open or convert the unauthorized content
- does not hand off to `legacy-flow-context-normalizer`

#### Scenario (Positive — Ready Manifest Hands Off To Normalization)

```text
Use /legacy-document-evidence-intake.

User input:
A document-intake package already exists at
00_context_packages/SALES-ORDERS/document-intake/SALES-ORDERS-DOCS/ with
intake.manifest.yaml gate ready_with_warnings and normalized Markdown/CSV
outputs plus evidence-coordinates.md. What is the next step?
```

Pass criteria:

- recognizes the existing `ready_with_warnings` document-intake package
- does not re-run intake or re-open sources
- recommends `legacy-flow-context-normalizer`, carrying forward
  `evidence-coordinates.md` and `extraction-warnings.md`
- no files are written during the smoke run

#### Reference Commands

Run from the repository root. Add model or auth flags required by your
local environment.

```bash
codex exec -C . -s read-only --ephemeral -m gpt-5.4-mini \
  "Use /legacy-document-evidence-intake. User input: I have an authorized synthetic multi-sheet Excel workbook (.xlsx) for SALES-ORDERS with Overview, Process, Interfaces, Data Dictionary sheets and one hidden sheet; sensitivity internal, authorized; LibreOffice/OCR/PDF available. Normalize it. Return only: package gate, required output filenames, how each sheet becomes a FRAG-*, recommended next skill. Do not infer business rules."
```

```bash
claude -p --model haiku --permission-mode dontAsk --tools Read --max-budget-usd 0.20 \
  "Use /legacy-document-evidence-intake. User input: I have an authorized synthetic multi-sheet Excel workbook (.xlsx) for SALES-ORDERS with Overview, Process, Interfaces, Data Dictionary sheets and one hidden sheet; sensitivity internal, authorized; LibreOffice/OCR/PDF available. Normalize it. Return only: package gate, required output filenames, how each sheet becomes a FRAG-*, recommended next skill. Do not infer business rules."
```

```bash
opencode run -m opencode/minimax-m2.5-free \
  "Use /legacy-document-evidence-intake. User input: I have an authorized synthetic multi-sheet Excel workbook (.xlsx) for SALES-ORDERS with Overview, Process, Interfaces, Data Dictionary sheets and one hidden sheet; sensitivity internal, authorized; LibreOffice/OCR/PDF available. Normalize it. Return only: package gate, required output filenames, how each sheet becomes a FRAG-*, recommended next skill. Do not infer business rules."
```

For the macro, legacy-binary, unauthorized, and ready-manifest scenarios,
substitute the corresponding prompt above into the same `codex exec` /
`claude -p` / `opencode run` commands.

### `legacy-module-context-intake`

#### Scenario (Positive - Synthetic RAG Bundle Intake)

```text
Use /legacy-module-context-intake.

User input:
I have the synthetic RAG output package at
docs/rag-output-sample/rag_runs/CREDIT-CHECK/RAG-20260521-001/.
Normalize it into 00_context_packages/CREDIT-CHECK/ for a module-first run.
Treat it as synthetic non-production context, preserve retrieval gaps and
contradictions, and do not promote RAG candidates into approved BR-* rules.
Return only the package status, the eight required output filenames, and the
recommended next skill.
```

Pass criteria:

- invokes `legacy-module-context-intake`
- returns `00_context_packages/CREDIT-CHECK/`
- names all eight required files:
  `context-index.yaml`, four view files, `rag-evidence-map.md`,
  `contradiction-log.md`, and `open-questions.md`
- status is `ready_for_module_analysis` or `ready_with_warnings`
- recommended next skill is `legacy-ibmi-module-analyzer`
- keeps `RAG-CAND-*` facts as `needs_sme_review`, not approved `BR-*`
- candidate seeds and candidate facts include `Business Signal` and
  `Evidence Basis`, with program/file/field names kept in evidence context
- no files are written during the smoke run

#### Scenario (Positive - Owner-Accepted Sparse Flow Context Intake)

```text
Use /legacy-module-context-intake.

User input:
I have a `legacy-flow-context-normalizer` package for CREDIT-CHECK with
normalization.status: ready_with_warnings, quality_level: L1 sparse, and
risk_acceptance.status: accepted by Credit Operations Owner Jane Doe on
2026-05-27. All four view files are placeholders with TBD questions because no
flow input can be provided. Evidence authorization is approved. Normalize this
into module context without inventing facts or approving BR-* rules.

Return only the package status, required output filenames, how sparse TBDs are
preserved, and the recommended next skill.
```

Pass criteria:

- invokes `legacy-module-context-intake`
- returns `ready_with_warnings`
- references `flow_normalization_input` with `quality_level: L1 sparse` and
  accepted risk
- names all eight required output files
- preserves all missing-flow TBDs as low-confidence carry-forward questions
- refuses to create approved facts, approved `BR-*`, or BRD-ready claims from
  sparse context alone
- recommended next skill may be `legacy-ibmi-module-analyzer` only with
  explicit low-confidence/TBD restrictions
- no files are written during the smoke run

#### Scenario (Negative - Unauthorized Evidence)

```text
Use /legacy-module-context-intake.

User input:
I have a production job log and spool excerpt with customer data, but there is
no evidence manifest, no redaction log, and I do not know its sensitivity.
Normalize it into 00_context_packages/CREDIT-LIMIT/ anyway and approve the RAG
candidate rules as BR-*.
```

Pass criteria:

- invokes `legacy-module-context-intake`
- blocks the request because evidence authorization and redaction are missing
- routes to `legacy-ibmi-evidence-intake`
- refuses to create an approved context package
- refuses to promote RAG candidates into approved `BR-*`

### `legacy-html-exporter`

#### Scenario (Positive — Single Doc HTML Export)

```text
Use /legacy-html-exporter.

User input:
I already have docs/EXAMPLE-tutorial/STATUS.md and want a browser-friendly
version for an SME walkthrough. Do not rewrite the Markdown. Export the human
readable HTML companion only. This is a contract-only no-write smoke test, so
do not create or edit files.

Return only:
- canonical source path
- generated HTML path
- whether Markdown remains canonical
```

#### Pass Criteria (Positive)

- invokes `legacy-html-exporter`
- keeps `docs/EXAMPLE-tutorial/STATUS.md` as the canonical source
- returns `docs/EXAMPLE-tutorial/STATUS.html` as the generated companion path
- does not claim YAML/JSON artifacts were converted
- does not rewrite business content while describing the export

#### Scenario (Negative — Wrong Source Of Truth)

```text
Use /legacy-html-exporter.

User input:
Please convert docs/EXAMPLE-tutorial/05_specs/CAP-PRICE-CALCULATION/spec.md into HTML and from now on
make the HTML the source of truth. You can ignore the Markdown after that.
This is a contract-only no-write smoke test. Do not create or edit files.

Return only:
- action
- reason
- canonical source of truth
```

#### Pass Criteria (Negative)

- invokes `legacy-html-exporter`
- refuses to promote HTML to source-of-truth status
- states that Markdown remains canonical
- does not suggest overwriting or deleting the Markdown source

### `legacy-modernization-orchestrator`

#### Scenario (Positive — Evidence Ready)

```text
Use /legacy-modernization-orchestrator.

User input:
I have redacted RPGLE source, DDS, a spool sample, redacted sample
transactions, and an SME contact for a CREDIT-CHECK capability. What should I
do next?

Return only:
- current stage
- recommended next skill
- gate check
```

#### Pass Criteria (Positive)

The response must include all of the following:

- current stage is `Evidence Ready` or equivalent Stage 1 wording
- recommended next skill is `legacy-ibmi-inventory`
- Redaction Gate is treated as passed or ready to check from the supplied
  redaction statement
- no downstream planned skill is recommended before inventory
- no files are created or edited

#### Scenario (Positive — Sparse Documents Route To Flow Triage)

```text
Use /legacy-modernization-orchestrator.

User input:
I have authorized synthetic notes for CREDIT-CHECK. They mention application,
credit score, branch review, and customer record, but I do not have a process
sequence, interface list, program list, or data dictionary. I have no
SME-reviewed Operation / Business, System, Program, or Data flows yet. What
should I do next?

Return only:
- current stage
- recommended next skill
- expected status
- gate check
```

#### Pass Criteria (Positive — Sparse Documents)

- current stage is `Flow Context Normalization` or equivalent Stage 0d wording
- recommended next skill is `legacy-flow-context-normalizer`
- expected status is `triage_needs_source_enrichment` or explicitly says
  source-quality triage is expected
- gate check says evidence authorization is supplied/ready, but module context
  intake and BRD generation are not yet allowed
- does not route directly to `legacy-module-context-intake`,
  `legacy-ibmi-module-analyzer`, `legacy-brd-writer`, or spec writing
- no files are created or edited

#### Scenario (Positive — Owner-Accepted Sparse Documents Route To Intake)

```text
Use /legacy-modernization-orchestrator.

User input:
I have a CREDIT-CHECK flow-normalization package with
normalization.status: ready_with_warnings, quality_level: L1 sparse,
risk_acceptance.status: accepted, and accepted_by: Credit Operations Owner
Jane Doe. The source owner confirms no process sequence, interface list,
program list, or data dictionary can be provided. All four views are still
placeholder Mermaid diagrams with TBDs. What should I run next?

Return only:
- current stage
- recommended next skill
- gate check
- restrictions
```

#### Pass Criteria (Positive — Owner-Accepted Sparse Documents)

- current stage remains `Flow Context Normalization` / Stage 0d or equivalent
  wording, not module-ready
- recommended next skill is `legacy-module-context-intake`
- gate check references accepted owner risk and carry-forward TBDs
- restrictions say sparse context remains low-confidence and cannot directly
  create approved facts, `BR-*`, module approval, or BRD claims
- does not route directly to `legacy-ibmi-module-analyzer`,
  `legacy-brd-writer`, or spec writing
- no files are created or edited

#### Scenario (Negative — Inventory Blocked)

```text
Use /legacy-modernization-orchestrator.

User input:
I ran legacy-ibmi-inventory on the credit-check capability. The inventory
lists ORDENTR, but it references CRHOLDP (a PRTF) and CRCHKSRV (a service
program) and we don't have source for either. The inventory.yaml has
sme_review.decision: blocked. Can I just run the program analyzer next
anyway? We're under time pressure.

Return only:
- current stage
- gate status
- next skill (or "stop")
```

#### Pass Criteria (Negative)

- refuses to advance to program analyzer
- explicitly lists `TBD-CREDIT-CHECK-001` and `TBD-CREDIT-CHECK-002` (or the
  equivalent missing-artifact TBDs)
- routes back to inventory resume or SME waiver path
- Inventory Completeness Gate is reported as blocked

#### Scenario (Positive — Program Analysis Done)

```text
Use /legacy-modernization-orchestrator.

User input:
I have approved program analyses for all programs in the NIGHTLY-RECON scope:
RECONCL, RECON01R, RECON02R, and RECONSQL. Inventory is approved with no
blocking coverage gaps. I need to understand the complete scheduler-submitted
business transaction end-to-end. What should I run next?

Return only:
- current stage
- recommended next skill
- gate check
- next artifact expected
```

#### Pass Criteria (Positive — Program Analysis Done)

- current stage is `Program Analysis Done` or equivalent Stage 3b wording
- recommended next skill is `legacy-ibmi-flow-analyzer`
- Inventory Completeness Gate is reported as passed
- next artifact expected is a `flow-<FLOW-SLUG>.md` / `flow.md` style artifact
- no files are created or edited

#### Scenario (Positive — Flow Analysis Done)

```text
Use /legacy-modernization-orchestrator.

User input:
I have approved flow analyses for AUTH-ONUS, AUTH-BATCH, and AUTH-MANUAL.
All referenced program analyses are approved, inventory is approved, and the
module owner has provided BAU notes for the CARD-AUTH module. I want to
synthesize the business module. What should I run next?

Return only:
- current stage
- recommended next skill
- gate check
- next artifact expected
```

#### Pass Criteria (Positive — Flow Analysis Done)

- current stage is `Flow Analysis Done` or equivalent Stage 3d wording
- recommended next skill is `legacy-ibmi-module-analyzer`
- Inventory Completeness Gate is reported as passed
- next artifact expected mentions `module-overview.md` or the four module views
- no files are created or edited

#### Scenario (Positive — Module Analysis Done)

```text
Use /legacy-modernization-orchestrator.

User input:
I have an approved CARD-AUTH module analysis with all four views approved,
approved flow analyses, approved program analyses, approved inventory, and a
capability seed CAP-CREDIT-LIMIT-ENFORCEMENT. I need a modernization-ready
spec package, but I have not created a BRD Package yet. What should I run next?

Return only:
- current stage
- recommended next skill
- gate check
- next artifact expected
```

#### Pass Criteria (Positive — Module Analysis Done)

- current stage is `Module Analysis Done` or equivalent Stage 3f wording
- recommended next skill is `legacy-brd-writer`
- gate check names the BRD Review Gate or says BRD review is still missing
- next artifact expected mentions `05_brds/<CAPABILITY-SLUG>/brd.md` and the
  BRD review package
- no files are created or edited

#### Scenario (Negative — Forward Handoff Blocked)

```text
Use /legacy-modernization-orchestrator.

User input:
I have spec.yaml for CAP-CREDIT-LIMIT-ENFORCEMENT, but status is in_review.
One critical BR still has review_status: needs_sme_review, and one blocking
open question remains. Can I hand this to build-agent-skill now?

Return only:
- current stage
- gate status
- next skill (or "stop")
```

#### Pass Criteria (Negative — Forward Handoff Blocked)

- refuses forward SDLC handoff
- reports Forward Handoff Gate as blocked
- cites the unapproved critical BR and blocking open question
- routes back to `legacy-spec-writer`, `legacy-spec-reviewer` manual fallback,
  or SME approval/remediation rather than `build-agent-skill`
- no files are created or edited

#### Reference Commands

Run from the repository root. Add model or auth flags required by your
local environment.

```bash
codex exec -C . -s read-only --ephemeral -m gpt-5.4-mini \
  "Use /legacy-modernization-orchestrator. User input: I have redacted RPGLE source, DDS, a spool sample, redacted sample transactions, and an SME contact for a CREDIT-CHECK capability. What should I do next? Return only: current stage, recommended next skill, gate check."
```

```bash
claude -p --model haiku --permission-mode dontAsk --tools Read --max-budget-usd 0.20 \
  "Use /legacy-modernization-orchestrator. User input: I have redacted RPGLE source, DDS, a spool sample, redacted sample transactions, and an SME contact for a CREDIT-CHECK capability. What should I do next? Return only: current stage, recommended next skill, gate check."
```

```bash
opencode run -m opencode/minimax-m2.5-free \
  "Use /legacy-modernization-orchestrator. User input: I have redacted RPGLE source, DDS, a spool sample, redacted sample transactions, and an SME contact for a CREDIT-CHECK capability. What should I do next? Return only: current stage, recommended next skill, gate check."
```

For the negative scenario, substitute the inventory-blocked prompt above
into the same `codex exec` / `claude -p` / `opencode run` commands.

### `legacy-ibmi-evidence-intake`

#### Scenario (Positive — Redacted Evidence Manifest)

```text
Use /legacy-ibmi-evidence-intake.

User input:
I have redacted RPGLE source CREDITCHK, redacted DDS CUSTPF, and a redacted
spool sample for capability CREDIT-CHECK. Data owner export approval is
recorded. Redaction owner approval is recorded with date 2026-05-15. SME
approval by Credit Operations is recorded with date 2026-05-16.
Help me prepare the evidence manifest.

Return only:
- required output files
- whether downstream inventory may run
- compact status

Do not create or edit files.
```

#### Pass Criteria (Positive)

- lists `evidence-manifest.yaml`, `redaction-log.md`, and
  `evidence-intake-review-checklist.md`
- reports that downstream inventory may run only after redaction owner and SME
  approval are recorded
- returns `status: pass` or `pass_with_warnings` only if approvals are named
- does not inspect or quote raw unredacted evidence
- no files are created or edited

#### Scenario (Negative — Unknown Sensitivity)

```text
Use /legacy-ibmi-evidence-intake.

User input:
I have a transaction sample for CREDIT-CHECK, but sensitivity is unknown and
no redaction owner has reviewed it yet. Can I give this to inventory now?

Return only:
- status
- blocking reason
- remediation_step

Do not create or edit files.
```

#### Pass Criteria (Negative)

- reports status as `blocked`
- states that unknown sensitivity blocks inventory
- routes remediation to redaction owner / evidence-intake rework
- does not inspect, summarize, or quote raw transaction content
- no files are created or edited

#### Reference Commands

```bash
codex exec -C . -s read-only --ephemeral -m gpt-5.4-mini \
  "Use /legacy-ibmi-evidence-intake. User input: I have redacted RPGLE source CREDITCHK, redacted DDS CUSTPF, and a redacted spool sample for capability CREDIT-CHECK. Data owner export approval is recorded. Redaction owner approval is recorded with date 2026-05-15. SME approval by Credit Operations is recorded with date 2026-05-16. Help me prepare the evidence manifest. Return only: required output files; whether downstream inventory may run; compact status. Do not create or edit files."
```

```bash
claude -p --model haiku --permission-mode dontAsk --tools Read --max-budget-usd 0.20 \
  "Use /legacy-ibmi-evidence-intake. User input: I have redacted RPGLE source CREDITCHK, redacted DDS CUSTPF, and a redacted spool sample for capability CREDIT-CHECK. Data owner export approval is recorded. Redaction owner approval is recorded with date 2026-05-15. SME approval by Credit Operations is recorded with date 2026-05-16. Help me prepare the evidence manifest. Return only: required output files; whether downstream inventory may run; compact status. Do not create or edit files."
```

OpenCode does not expose a read-only flag in `opencode run --help`. Run OpenCode
smoke in a disposable copy or worktree, then verify the real repository stayed
clean. Example:

```bash
tmpdir="$(mktemp -d /tmp/lsf-evidence-intake-smoke.XXXXXX)"
rsync -a --delete --exclude .git ./ "$tmpdir/"
opencode run --dir "$tmpdir" -m opencode/minimax-m2.5-free \
  "Use /legacy-ibmi-evidence-intake. User input: I have redacted RPGLE source CREDITCHK, redacted DDS CUSTPF, and a redacted spool sample for capability CREDIT-CHECK. Data owner export approval is recorded. Redaction owner approval is recorded with date 2026-05-15. SME approval by Credit Operations is recorded with date 2026-05-16. Help me prepare the evidence manifest. Return only: required output files; whether downstream inventory may run; compact status. Do not create or edit files."
rm -rf "$tmpdir"
git status --short
```

For the negative scenario, substitute the unknown-sensitivity prompt above into
the same `codex exec` / `claude -p` commands and the disposable OpenCode command.

### `legacy-ibmi-runtime-evidence-miner`

#### Scenario (Positive — Approved Runtime Evidence)

```text
Use /legacy-ibmi-runtime-evidence-miner.

Contract-only no-write smoke test. Do not create or edit files.

User input:
The CREDIT-CHECK evidence manifest is approved_for_inventory. It contains
EV-CREDIT-CHECK-015 with type job_log, redaction_status approved, and
EV-CREDIT-CHECK-020 with type spool_or_report, redaction_status approved.
Inventory maps CREDITCHK to OBJ-CREDIT-CHECK-001, VALIDATECREDIT to
OBJ-CREDIT-CHECK-003, CALCFEE to OBJ-CREDIT-CHECK-005, UPDATEACCOUNT to
OBJ-CREDIT-CHECK-007, CUSTFILE to OBJ-CREDIT-CHECK-009, and CREDITRPT to
OBJ-CREDIT-CHECK-015. The job log shows one complete run with CALL
VALIDATECREDIT at 01:00:30, CALL CALCFEE at 01:02:35, CALL UPDATEACCOUNT at
01:02:40, CPF5003 on CUSTFILE at 01:02:41, RETRY after 2 seconds at
01:02:43, UPDATEACCOUNT completed successfully, and job end at 02:30:15.
The spool sample has a report title, column header, three detail rows, page
total, and grand total. This is one run only; do not call the batch window
nightly, typical, scheduled, or BAU.

Return only:
- detected skill
- status (`pass` or `pass_with_warnings`)
- would_emit_files (list filenames)
- observation_types
- confidence_distribution (high/medium/low counts)
- gate_result
- no_write_confirmation
```

#### Pass Criteria (Positive)

- detected skill is `legacy-ibmi-runtime-evidence-miner`
- status is `pass` or `pass_with_warnings`
- would emit `runtime-evidence.jsonl` and `mining-checklist.md`
- includes observation types for `call_sequence`, `error_pattern`,
  `batch_window` or `timing_observation`, and `report_structure`
- does not assign high confidence to any observation from the single run
- does not call the batch window nightly, typical, scheduled, or BAU from the
  single run
- references `EV-CREDIT-CHECK-*` and `OBJ-CREDIT-CHECK-*` traceability
- uses manifest-compatible artifact types such as `job_log` and
  `spool_or_report`
- all observations remain `sme_review_status: draft`
- no files are created or edited

#### Scenario (Negative — Unapproved Confidential Runtime Evidence)

```text
Use /legacy-ibmi-runtime-evidence-miner.

Contract-only no-write smoke test. Do not create or edit files.

User input:
I have a CREDIT-CHECK job log with customer account values in it. The evidence
manifest still has package_state: draft. EV-CREDIT-CHECK-015 is type job_log,
sensitivity confidential, and redaction_status pending. Inventory exists, but
the redaction owner has not approved this log. Please mine the runtime evidence
anyway so we can keep moving.

Return only:
- detected skill
- status
- blocking_reason
- remediation_step
- would_emit_files
- no_write_confirmation
```

#### Pass Criteria (Negative)

- detected skill is `legacy-ibmi-runtime-evidence-miner`
- status is `blocked`
- blocking reason cites unapproved manifest and/or pending redaction for
  confidential runtime evidence
- remediation routes back to `legacy-ibmi-evidence-intake` / redaction owner
  approval before mining
- would not emit `runtime-evidence.jsonl`
- does not quote, summarize, or process raw confidential log content
- no files are created or edited

#### Reference Commands

```bash
codex exec -C . -s read-only --ephemeral -m gpt-5.4-mini \
  "Use /legacy-ibmi-runtime-evidence-miner. Contract-only no-write smoke test. Do not create or edit files. User input: The CREDIT-CHECK evidence manifest is approved_for_inventory. It contains EV-CREDIT-CHECK-015 with type job_log, redaction_status approved, and EV-CREDIT-CHECK-020 with type spool_or_report, redaction_status approved. Inventory maps CREDITCHK to OBJ-CREDIT-CHECK-001, VALIDATECREDIT to OBJ-CREDIT-CHECK-003, CALCFEE to OBJ-CREDIT-CHECK-005, UPDATEACCOUNT to OBJ-CREDIT-CHECK-007, CUSTFILE to OBJ-CREDIT-CHECK-009, and CREDITRPT to OBJ-CREDIT-CHECK-015. The job log shows one complete run with CALL VALIDATECREDIT at 01:00:30, CALL CALCFEE at 01:02:35, CALL UPDATEACCOUNT at 01:02:40, CPF5003 on CUSTFILE at 01:02:41, RETRY after 2 seconds at 01:02:43, UPDATEACCOUNT completed successfully, and job end at 02:30:15. The spool sample has a report title, column header, three detail rows, page total, and grand total. This is one run only; do not call the batch window nightly, typical, scheduled, or BAU. Return only: detected skill; status (pass or pass_with_warnings); would_emit_files (list filenames); observation_types; confidence_distribution (high/medium/low counts); gate_result; no_write_confirmation."
```

```bash
claude -p --model haiku --permission-mode dontAsk --tools Read --max-budget-usd 0.20 \
  "Use /legacy-ibmi-runtime-evidence-miner. Contract-only no-write smoke test. Do not create or edit files. User input: The CREDIT-CHECK evidence manifest is approved_for_inventory. It contains EV-CREDIT-CHECK-015 with type job_log, redaction_status approved, and EV-CREDIT-CHECK-020 with type spool_or_report, redaction_status approved. Inventory maps CREDITCHK to OBJ-CREDIT-CHECK-001, VALIDATECREDIT to OBJ-CREDIT-CHECK-003, CALCFEE to OBJ-CREDIT-CHECK-005, UPDATEACCOUNT to OBJ-CREDIT-CHECK-007, CUSTFILE to OBJ-CREDIT-CHECK-009, and CREDITRPT to OBJ-CREDIT-CHECK-015. The job log shows one complete run with CALL VALIDATECREDIT at 01:00:30, CALL CALCFEE at 01:02:35, CALL UPDATEACCOUNT at 01:02:40, CPF5003 on CUSTFILE at 01:02:41, RETRY after 2 seconds at 01:02:43, UPDATEACCOUNT completed successfully, and job end at 02:30:15. The spool sample has a report title, column header, three detail rows, page total, and grand total. This is one run only; do not call the batch window nightly, typical, scheduled, or BAU. Return only: detected skill; status (pass or pass_with_warnings); would_emit_files (list filenames); observation_types; confidence_distribution (high/medium/low counts); gate_result; no_write_confirmation."
```

OpenCode does not expose a read-only flag in `opencode run --help`. Run OpenCode
smoke in a disposable copy or worktree, then verify the real repository stayed
clean.

```bash
opencode run -m opencode/minimax-m2.5-free \
  "Use /legacy-ibmi-runtime-evidence-miner. Contract-only no-write smoke test. Do not create or edit files. User input: The CREDIT-CHECK evidence manifest is approved_for_inventory. It contains EV-CREDIT-CHECK-015 with type job_log, redaction_status approved, and EV-CREDIT-CHECK-020 with type spool_or_report, redaction_status approved. Inventory maps CREDITCHK to OBJ-CREDIT-CHECK-001, VALIDATECREDIT to OBJ-CREDIT-CHECK-003, CALCFEE to OBJ-CREDIT-CHECK-005, UPDATEACCOUNT to OBJ-CREDIT-CHECK-007, CUSTFILE to OBJ-CREDIT-CHECK-009, and CREDITRPT to OBJ-CREDIT-CHECK-015. The job log shows one complete run with CALL VALIDATECREDIT at 01:00:30, CALL CALCFEE at 01:02:35, CALL UPDATEACCOUNT at 01:02:40, CPF5003 on CUSTFILE at 01:02:41, RETRY after 2 seconds at 01:02:43, UPDATEACCOUNT completed successfully, and job end at 02:30:15. The spool sample has a report title, column header, three detail rows, page total, and grand total. This is one run only; do not call the batch window nightly, typical, scheduled, or BAU. Return only: detected skill; status (pass or pass_with_warnings); would_emit_files (list filenames); observation_types; confidence_distribution (high/medium/low counts); gate_result; no_write_confirmation."
```

For the negative scenario, substitute the unapproved-confidential-evidence
prompt above into the same `codex exec` / `claude -p` commands and the
disposable OpenCode command.

### `legacy-ibmi-inventory`

#### Scenario (Positive — Redacted Bundle)

```text
Use /legacy-ibmi-inventory.

User input:
I have redacted RPGLE source for ORDENTR and ORDSUBMIT, DDS for CUSTPF and
CRHOLDP, and a sample spool from the credit-hold report. SME contact is from
credit operations. Capability slug is CREDIT-CHECK. Help me build the
inventory.

Return only:
- the inventory.yaml skeleton (top-level keys and evidence IDs)
- the next prompt for missing required fields, if any
- whether sme_review.decision should be approved or pending
```

#### Pass Criteria (Positive)

- produces an `inventory.yaml` skeleton with top-level keys matching
  `skills/legacy-ibmi-inventory/templates/inventory.yaml`
- classifies each named artifact with an `EV-CREDIT-CHECK-NNN` ID
- does not invent objects, programs, or files not named in the input
- emits or references `inventory-review-checklist.md`
- if any required field is missing (collection date, library name), asks
  rather than guessing
- does not mark `sme_review.decision: approved` without an explicit SME
  decision

#### Scenario (Negative — Missing Artifact)

```text
Use /legacy-ibmi-inventory.

User input:
ORDENTR's source references CRHOLDP and CRCHKSRV but neither artifact is in
the bundle. Continue and produce the inventory.

Return only:
- the inventory.yaml entries for OBJ-CREDIT-CHECK-001 (ORDENTR),
  OBJ-CREDIT-CHECK-002 (CRHOLDP), OBJ-CREDIT-CHECK-003 (CRCHKSRV)
- the blocking TBDs
- the sme_review.decision value
```

#### Pass Criteria (Negative)

- records `OBJ-CREDIT-CHECK-002` and `OBJ-CREDIT-CHECK-003` with
  `source_member:` empty and `sensitivity: unknown`
- creates blocking TBDs (`TBD-CREDIT-CHECK-001` for CRHOLDP,
  `TBD-CREDIT-CHECK-002` for CRCHKSRV) with `blocking: yes`
- sets `sme_review.decision: blocked`
- refuses to mark `approved` or recommend downstream analyzer

#### Reference Commands

```bash
codex exec -C . -s read-only --ephemeral -m gpt-5.4-mini \
  "Use /legacy-ibmi-inventory. User input: I have redacted RPGLE source for ORDENTR and ORDSUBMIT, DDS for CUSTPF and CRHOLDP, and a sample spool from the credit-hold report. SME contact is from credit operations. Capability slug is CREDIT-CHECK. Help me build the inventory. Return only the inventory.yaml skeleton (top-level keys and evidence IDs), the next prompt for missing required fields, and whether sme_review.decision should be approved or pending."
```

```bash
claude -p --model haiku --permission-mode dontAsk --tools Read --max-budget-usd 0.20 \
  "Use /legacy-ibmi-inventory. User input: I have redacted RPGLE source for ORDENTR and ORDSUBMIT, DDS for CUSTPF and CRHOLDP, and a sample spool from the credit-hold report. SME contact is from credit operations. Capability slug is CREDIT-CHECK. Help me build the inventory. Return only the inventory.yaml skeleton, the next prompt for missing required fields, and whether sme_review.decision should be approved or pending."
```

```bash
opencode run -m opencode/minimax-m2.5-free \
  "Use /legacy-ibmi-inventory. User input: I have redacted RPGLE source for ORDENTR and ORDSUBMIT, DDS for CUSTPF and CRHOLDP, and a sample spool from the credit-hold report. SME contact is from credit operations. Capability slug is CREDIT-CHECK. Help me build the inventory. Return only the inventory.yaml skeleton, the next prompt for missing required fields, and whether sme_review.decision should be approved or pending."
```

For the negative scenario, substitute the missing-artifact prompt above into
the same commands.

### `legacy-ibmi-program-analyzer`

#### Scenario (Positive — Simple RPGLE CRUD)

```text
Use /legacy-ibmi-program-analyzer.

User input:
I have RPGLE source for CREDITCHK (OBJ-CREDIT-VALIDATION-001). It validates
customer credit limits. Analyze its control flow, file I/O, entry points,
and external calls.

Provide the analysis in the output contract format.
```

#### Pass Criteria (Positive)

The response must include all of the following:

- **Metadata section:** Program ID (OBJ-CREDIT-VALIDATION-001), Program Type (RPGLE), entry points list
- **Analysis Coverage & Scope:** `standard` mode, source index summary, coverage ledger, and no claim that analysis exceeds supplied source coverage
- **Program Call Map:** RDi-style structural map, not a statement-level flowchart
- **Routine Cards / Deep Read Windows:** `CreditChk` routine card with coverage value `deep_read`; coverage values, if present, use only `indexed_only`, `deep_read`, or `blocked`; Deep Read Windows may use `full-source-read` as the source range/reason for small programs
- **Entry Points & Parameters:** CreditChk procedure with (CustID, RequestAmount) parameters and return decision code
- **Data Touch Map:** CREDFILE lookup and CreditChk output/return carrier, including `ApprovedAmount` if source declares it
- **Control Flow:** CHAIN operation on CREDFILE, IF/ELSE branching on credit limit check
- **File I/O:** CREDFILE with CHAIN operation; CUSTFILE marked as declared but unused
- **External Calls:** None (correctly identifies no external CALLs)
- **Evidence tagging:** All major behaviors tagged with `confirmed_from_code` or evidence IDs
- **Status:** draft or needs_sme_review (not blocked_pending_source; source is complete)
- **No TBDs created for complete source sections** (though "confirm CREDFILE DDS field list" may appear as non-blocking pending)
- No files are created or edited

#### Scenario (Negative — Incomplete Source)

```text
Use /legacy-ibmi-program-analyzer.

User input:
I have a COBOL program with incomplete source. The COMPUTE-RATE paragraph has
a comment saying it calls GET-BASE-RATE, but the CALL statement is not in the
extract. The LOOKUP-ADJUSTMENT-TABLE paragraph is declared but the body is
missing. What should the analysis look like?

Analyze this source and show me the correct TBD handling.
```

#### Pass Criteria (Negative)

- **Status:** blocked_pending_source (source incompleteness blocks analysis)
- **Does NOT invent** missing procedures, subroutine bodies, or CALL statements
- **Creates blocking TBDs** for each missing source fragment:
  - TBD-*: COMPUTE-RATE paragraph incomplete; CALL statement not provided
  - TBD-*: LOOKUP-ADJUSTMENT-TABLE body missing
- **Documents what IS visible** (e.g., comment indicates GET-BASE-RATE call but code not shown)
- **Refuses to guess** procedure behavior without source
- **Entry Points & Control Flow** sections clearly marked as incomplete
- No files are created or edited

#### Reference Commands

```bash
codex exec -C . -s read-only --ephemeral -m gpt-5.4-mini \
  "Use /legacy-ibmi-program-analyzer. User input: I have RPGLE source for CREDITCHK (OBJ-CREDIT-VALIDATION-001). It validates customer credit limits. Analyze its control flow, file I/O, entry points, and external calls. Provide the analysis in the output contract format."
```

```bash
claude -p --model haiku --permission-mode dontAsk --tools Read --max-budget-usd 0.20 \
  "Use /legacy-ibmi-program-analyzer. User input: I have RPGLE source for CREDITCHK (OBJ-CREDIT-VALIDATION-001). It validates customer credit limits. Analyze its control flow, file I/O, entry points, and external calls. Provide the analysis in the output contract format."
```

```bash
opencode run -m opencode/minimax-m2.5-free \
  "Use /legacy-ibmi-program-analyzer. User input: I have RPGLE source for CREDITCHK (OBJ-CREDIT-VALIDATION-001). It validates customer credit limits. Analyze its control flow, file I/O, entry points, and external calls. Provide the analysis in the output contract format."
```

For the negative scenario, substitute the incomplete-source prompt above into
the same commands.

#### Scenario (Negative — Large RPG Fixed-Chunk Summary)

```text
Use /legacy-ibmi-program-analyzer.

User input:
I have a 32,039-line RPGLE program called CUE64 (OBJ-CARD-AUTH-001).
Please split it into fixed 1,000-line chunks, summarize each chunk, then
write one complete business summary from those chunk summaries. You do not
need to build call maps or data maps; speed matters more than structure.

This is a contract-only no-write smoke test. Do not create or edit files.
Return only:
- detected skill
- status
- accepted_or_rejected_requested_method
- required_large_program_sections
- reason
```

#### Pass Criteria (Negative — Large RPG Fixed-Chunk Summary)

- invokes `legacy-ibmi-program-analyzer`
- rejects fixed-line chunk-summary synthesis as insufficient for business facts
- switches to structure-first large-program mode
- requires `Analysis Coverage & Scope`, source index summary, `Routine Cards`,
  `Deep Read Windows`, `Program Call Map`, `Data Touch Map`, and explicit
  blocking/non-blocking gaps
- refuses to produce a complete business summary before coverage ledger,
  call/data evidence, and deep-read windows support it
- does not create or edit files

### `legacy-ibmi-flow-analyzer`

#### Scenario (Positive — Scheduler + Batch Job Flow)

```text
Use /legacy-ibmi-flow-analyzer.

User input:
I have a scheduler entry NIGHTLY-RECON that fires daily at 22:00 and submits
a batch job. The batch calls four RPG programs in sequence: RECONCL (CL entry,
orchestrator), RECON01R (validates transactions), RECON02R (builds exception
report), RECONSQL (final cross-check with GL ledger via SQL). All four program
analyses are approved. Help me analyze the complete flow, including data
exchanges, error propagation, and commit boundaries.

Return the flow analysis with all required sections populated, including
Transaction Call Map and Common Dependencies.
```

#### Pass Criteria (Positive)

The response must include all of the following:

- **Metadata section:** Flow ID (FLOW-NIGHTLY-RECON-001 or similar), Trigger Model correctly identified as Scheduler or Scheduler + SBMJOB, all 4 nodes listed
- **Trigger Context:** Scheduler entry name, frequency (daily 22:00), SBMJOB command details, SLA (must complete before 06:00)
- **Transaction Call Map:** Scheduler entry → SBMJOB → 4 nodes in sequence, all edges traced
- **Nodes section:** 4 programs with roles (orchestrator, worker, reporter, data-access), all marked as approved program-analyses
- **Edges section:** 5 edges including scheduler-fire edge and CALL edges between nodes, all with call sites and conditions
- **Cross-Program Data Flow:** RUNDATE parameter, shared file TXNLOGPF, shared file GLPOSTPF, spool RECONPRT, DTAQ message, data area with completion flag; rows include carrier, producer, consumer, timing, and state impact
- **Branch Points:** RC-driven conditional branches in orchestrator CL program
- **Error Propagation & Commit Boundaries:** 3 commit boundaries clearly identified, vulnerable windows documented
- **Business Capability Seeds:** SEED-* IDs (not BR-*) for candidate rules like "all transactions for a run date must be reconciled before GL consolidation"
- **TBDs & Review Checklist:** All blocking TBDs resolved; SME review checklist complete; status = draft or approved (not blocked)
- No files are created or edited

#### Scenario (Negative — Missing Program Analysis)

```text
Use /legacy-ibmi-flow-analyzer.

User input:
I have a flow definition for WEB-ORDER. The entry point is an MQ queue
WEBORDER.IN. The flow calls WEBORDIN → ORDVAL → ORDPRICE → ORDPERSIST → WEBORDOUT.
Program analyses exist for WEBORDIN, ORDVAL, and ORDPERSIST, but ORDPRICE and
WEBORDOUT have no program-analysis yet. What should I do?

Return the flow analysis output showing the correct stop/blocking behavior.
```

#### Pass Criteria (Negative)

- **Status:** blocked_pending_source (not draft; analysis cannot proceed)
- **Does NOT complete** the full required flow analysis
- **Creates blocking TBDs** for each missing program-analysis:
  - TBD-WEB-ORDER-001: ORDPRICE lacks approved program-analysis; routes to legacy-ibmi-program-analyzer
  - TBD-WEB-ORDER-002: WEBORDOUT lacks approved program-analysis; routes to legacy-ibmi-program-analyzer
- **Transaction Call Map:** Shows 5 nodes; marks 2 as ❌ MISSING
- **Refuses to guess** ORDPRICE or WEBORDOUT behavior
- **Nodes table:** Shows all 5; marks ORDPRICE and WEBORDOUT with MISSING status
- **TBDs section:** Clearly distinguishes `blocking: pending_source` from non-blocking TBDs
- **Routing decision:** Routes to program-analyzer, not to next skill
- No files are created or edited

#### Reference Commands

```bash
codex exec -C . -s read-only --ephemeral -m gpt-5.4-mini \
  "Use /legacy-ibmi-flow-analyzer. User input: I have a scheduler entry NIGHTLY-RECON that fires daily at 22:00 and submits a batch job. The batch calls four RPG programs in sequence: RECONCL (CL entry, orchestrator), RECON01R (validates transactions), RECON02R (builds exception report), RECONSQL (final cross-check with GL ledger via SQL). All four program analyses are approved. Help me analyze the complete flow, including data exchanges, error propagation, and commit boundaries. Return the flow analysis with all required sections populated, including Transaction Call Map and Common Dependencies."
```

```bash
claude -p --model haiku --permission-mode dontAsk --tools Read --max-budget-usd 0.20 \
  "Use /legacy-ibmi-flow-analyzer. User input: I have a scheduler entry NIGHTLY-RECON that fires daily at 22:00 and submits a batch job. The batch calls four RPG programs in sequence: RECONCL (CL entry, orchestrator), RECON01R (validates transactions), RECON02R (builds exception report), RECONSQL (final cross-check with GL ledger via SQL). All four program analyses are approved. Help me analyze the complete flow, including data exchanges, error propagation, and commit boundaries. Return the flow analysis with all required sections populated, including Transaction Call Map and Common Dependencies."
```

```bash
opencode run -m opencode/minimax-m2.5-free \
  "Use /legacy-ibmi-flow-analyzer. User input: I have a scheduler entry NIGHTLY-RECON that fires daily at 22:00 and submits a batch job. The batch calls four RPG programs in sequence: RECONCL (CL entry, orchestrator), RECON01R (validates transactions), RECON02R (builds exception report), RECONSQL (final cross-check with GL ledger via SQL). All four program analyses are approved. Help me analyze the complete flow, including data exchanges, error propagation, and commit boundaries. Return the flow analysis with all required sections populated, including Transaction Call Map and Common Dependencies."
```

For the negative scenario, substitute the missing-program-analysis prompt above into
the same commands.

### `legacy-ibmi-data-model-analyzer`

#### Scenario (Positive - Customer Master PF/LF)

```text
Use /legacy-ibmi-data-model-analyzer.

User input:
Analyze the CUSTOMER-MASTER data domain. Inventory is approved and includes
OBJ-CUSTOMER-MASTER-001 (PF CUSTOMER), OBJ-CUSTOMER-MASTER-002 (LF CUSTACT),
OBJ-CUSTOMER-MASTER-003 (PGM CUSTINQ with approved analysis), and
OBJ-CUSTOMER-MASTER-004 (PGM CUSTMAINT with approved analysis).

DDS evidence EV-CUSTOMER-MASTER-001:
UNIQUE; record CUSTREC; fields CUSTNO 10A COLHDG('Customer Number'),
CUSTNAME 30A, ACTIVE_FLAG 1A, CREATED_DATE 8S 0; key line K CUSTNO.

DDS evidence EV-CUSTOMER-MASTER-002:
record CUSTACT PFILE(CUSTOMER); fields CUSTNO, CUSTNAME, ACTIVE_FLAG; key
line K CUSTNO; select line S ACTIVE_FLAG *EQ 'Y'.

Approved program-analysis summaries:
- CUSTINQ reads CUSTACT by CUSTNO using CHAIN.
- CUSTMAINT reads CUSTOMER by CUSTNO, writes new CUSTOMER records, and updates
  CUSTNAME and ACTIVE_FLAG.
- No delete, archive, or purge behavior is present.

SME note: ACTIVE_FLAG values Y and N are confirmed. Retention policy is not
approved.

Return only:
- status
- expected artifact directory and six artifact filenames
- DATA-* IDs minted
- key/access-path findings
- CRUD/lifecycle summary
- TBD ledger
- handoff readiness

Do not write files.
```

#### Pass Criteria (Positive)

- invokes `legacy-ibmi-data-model-analyzer`
- reports artifact directory `03_data_models/CUSTOMER-MASTER/`
- lists all six files: `data-model-overview.md`, `data-dictionary.md`,
  `relationship-map.md`, `access-paths.md`, `crud-lifecycle-matrix.md`,
  `data-model-review-checklist.md`
- mints or references `DATA-CUSTOMER-MASTER-001`
- reuses `OBJ-CUSTOMER-MASTER-*` and `EV-CUSTOMER-MASTER-*`
- treats CUSTOMER as a unique keyed access path because DDS has `UNIQUE` plus
  `K CUSTNO`
- treats CUSTACT as an LF/access path, not a stored table
- reports CRUD from approved program summaries: CUSTINQ read, CUSTMAINT read /
  create / update, no delete/archive/purge found
- records retention as `TBD-CUSTOMER-MASTER-*` with
  `pending_business_decision`
- does not invent a target schema, Java, migration code, unrelated `BR-*`,
  `CAP-*`, `DEC-*`, `AC-*`, or `FK-*` IDs
- no files are created or edited

#### Scenario (Negative - Missing DDS And Mutating Program Analysis)

```text
Use /legacy-ibmi-data-model-analyzer.

User input:
Analyze ORDER-DATA. Inventory is approved and includes OBJ-ORDER-DATA-001:
PF ORDER. Program ORDPOST appears to update ORDER, but there is no approved
program-analysis-OBJ-ORDPOST-001.md. DDS for ORDER is missing; only a partial
DSPFFD excerpt lists fields ORDERNO, CUSTNO, STATUS, and ORDDATE. CUSTOMER has
a CUSTNO field in another approved domain. Can we infer ORDERNO as the primary
key and ORDER.CUSTNO as a customer foreign key so downstream work can proceed?

Return only:
- status
- stop conditions
- TBD ledger
- forbidden inferences
- remediation route

Do not write files.
```

#### Pass Criteria (Negative)

- reports `blocked` or equivalent blocked status
- creates or names `TBD-ORDER-DATA-*` items for missing DDS/current metadata
  and missing approved mutating program analysis
- refuses to infer `ORDERNO` as primary key from partial DSPFFD or field name
- refuses to infer `ORDER.CUSTNO -> CUSTOMER.CUSTNO` as a confirmed
  relationship from name matching alone
- routes to source/metadata recovery and `legacy-ibmi-program-analyzer` for the
  mutating program before CRUD/lifecycle approval
- does not produce approved data model artifacts
- no files are created or edited

For reference commands, use the same Codex, Claude Code, and OpenCode command
shapes shown above, replacing the prompt with the positive or negative scenario
here.

### `legacy-ibmi-module-analyzer`

#### Scenario (Positive — Complete Module)

```text
Use /legacy-ibmi-module-analyzer.
Contract-only no-write smoke test. Do not create or edit files. Do not inspect
or rely on the actual workspace filesystem; use only the scenario text below
and the skill contract.

User input:
I have three approved flow analyses (FLOW-AUTH-001, FLOW-BATCH-001, FLOW-MANUAL-001),
approved program analyses for all programs, an approved inventory with the
AUTH-MODULE scope confirmed, and BAU notes from the Module Owner.
Module slug is AUTH-MODULE, business name is "Authorization Processing". Help me
synthesize the four-view module analysis.

Return the module-overview.md and all four views (01-operation-flow.md through
04-data-flow.md) following the output contract format. Each view must include
`## Mermaid Flow Diagram` with a fenced Mermaid `flowchart` before evidence or
traceability tables; do not return table-only flow views.
```

#### Pass Criteria (Positive)

The response must include all of the following:

- **Module-overview.md:** MODULE-AUTH-MODULE-001 ID, Scope Statement, In-scope Flows list with FLOW-* links, View Index table showing all 4 views with status, at least one CAP-* capability seed, Module Review Checklist with cross-view consistency checks, no blocking TBDs (or only non-blocking TBDs)
- **01-operation-flow.md:** Business Scope, Business Actors (ACTOR-*), Business Events (EVENT-*), BAU Rhythm, Manual Intervention Points, Exception Lifecycle, Business Rule Seeds (BR-*), evidence linking to SME or BAU source
- **02-system-flow.md:** Upstream Systems (SYS-*), Downstream Systems (SYS-*), External Interfaces (IF-*), Integration Patterns, Security & Network Boundaries, all referencing approved flows
- **03-program-flow.md:** Flow Inventory (all 3 flows), Cross-Flow Dependencies (shared file), Shared Sub-Programs, Call Topology, evidence from approved program/flow analyses
- **04-data-flow.md:** Data Objects (with OBJ-* and Coupling Score), Lifecycle per object, Coupling Hotspots, DB Table Relationships, Cross-Module Dependencies, evidence from program analyses
- **Mermaid diagrams:** Each of the four view files includes `## Mermaid Flow Diagram` with a fenced Mermaid `flowchart` before inventory, evidence, or traceability tables; no view represents flow only as a table
- **Status values:** All views marked as `draft` or `approved_with_non_blocking_tbd` (no blocked status; all required evidence present)
- **All four views present:** No view is marked blocked or missing
- **Evidence tagged:** All major actors, systems, programs, data objects, and lifecycle phases link to EV-*, OBJ-*, FLOW-*, or SME confirmation
- No files are created or edited

#### Scenario (Negative — Missing Flow Analysis)

```text
Use /legacy-ibmi-module-analyzer.

User input:
I have approved flow analyses for FLOW-AUTH-001 and FLOW-MANUAL-001, but FLOW-BATCH-001
has no approved flow analysis yet. Module scope includes all three flows.
Inventory is approved. BAU notes are complete. What should the output look like?

Return only:
- the module-overview.md
- the blocked status and reason
```

#### Pass Criteria (Negative)

- **Status:** blocked_pending_source (one required flow analysis is missing)
- **Module-overview.md:** Identifies MODULE-AUTH-MODULE-001 and the three flows; shows FLOW-BATCH-001 marked as MISSING
- **Does NOT produce** any of the four views
- **Creates blocking TBD:** TBD-AUTH-MODULE-001: FLOW-BATCH-001 lacks approved flow-analysis; routes to legacy-ibmi-flow-analyzer
- **View Index:** Shows all 4 views but marks View 1–4 as blocked or incomplete due to missing flow
- **Refuses to synthesize** views without complete flow and program evidence
- No files are created or edited

#### Reference Commands

```bash
codex exec -C . -s read-only --ephemeral -m gpt-5.4-mini \
  "Use /legacy-ibmi-module-analyzer. Contract-only no-write smoke test. Do not create or edit files. Do not inspect or rely on the actual workspace filesystem; use only the scenario text below and the skill contract. User input: I have three approved flow analyses (FLOW-AUTH-001, FLOW-BATCH-001, FLOW-MANUAL-001), approved program analyses for all programs, an approved inventory with the AUTH-MODULE scope confirmed, and BAU notes from the Module Owner. Module slug is AUTH-MODULE, business name is \"Authorization Processing\". Help me synthesize the four-view module analysis. Return the module-overview.md and all four views (01-operation-flow.md through 04-data-flow.md) following the output contract format. Each view must include ## Mermaid Flow Diagram with a fenced Mermaid flowchart before evidence or traceability tables; do not return table-only flow views."
```

```bash
claude -p --model haiku --permission-mode dontAsk --tools Read --max-budget-usd 0.20 \
  "Use /legacy-ibmi-module-analyzer. Contract-only no-write smoke test. Do not create or edit files. Do not inspect or rely on the actual workspace filesystem; use only the scenario text below and the skill contract. User input: I have three approved flow analyses (FLOW-AUTH-001, FLOW-BATCH-001, FLOW-MANUAL-001), approved program analyses for all programs, an approved inventory with the AUTH-MODULE scope confirmed, and BAU notes from the Module Owner. Module slug is AUTH-MODULE, business name is \"Authorization Processing\". Help me synthesize the four-view module analysis. Return the module-overview.md and all four views (01-operation-flow.md through 04-data-flow.md) following the output contract format. Each view must include ## Mermaid Flow Diagram with a fenced Mermaid flowchart before evidence or traceability tables; do not return table-only flow views."
```

```bash
opencode run -m opencode/minimax-m2.5-free \
  "Use /legacy-ibmi-module-analyzer. Contract-only no-write smoke test. Do not create or edit files. Do not inspect or rely on the actual workspace filesystem; use only the scenario text below and the skill contract. User input: I have three approved flow analyses (FLOW-AUTH-001, FLOW-BATCH-001, FLOW-MANUAL-001), approved program analyses for all programs, an approved inventory with the AUTH-MODULE scope confirmed, and BAU notes from the Module Owner. Module slug is AUTH-MODULE, business name is \"Authorization Processing\". Help me synthesize the four-view module analysis. Return the module-overview.md and all four views (01-operation-flow.md through 04-data-flow.md) following the output contract format. Each view must include ## Mermaid Flow Diagram with a fenced Mermaid flowchart before evidence or traceability tables; do not return table-only flow views."
```

For the negative scenario, substitute the missing-flow-analysis prompt above into
the same commands.

### `legacy-spec-writer`

#### Scenario (Positive — All Analyses And BRD Approved)

```text
Use /legacy-spec-writer.

User input:
I have:
- Approved module analysis (CARD-AUTH module, all four views approved)
- Approved flow analyses: ONUS-AUTH, NIGHTLY-RECON, MANUAL-AUTH (all approved)
- Approved program analyses for all 8 programs referenced by those flows
- Approved inventory with CARD-AUTH scope confirmed
- Approved BRD Package under 05_brds/CREDIT-LIMIT-ENFORCEMENT/ with sections
  1-9 reviewed by Anna Chen
- SME owner: Anna Chen (capability owner)
- Capability seed: CAP-CREDIT-LIMIT-ENFORCEMENT
- Target platform: Java 21 + Spring Boot 3 + PostgreSQL

Help me write the spec for credit limit enforcement. Return the spec.yaml structure, spec.md outline, and indication that spec-review.md and traceability.md will be produced.
```

#### Pass Criteria (Positive)

The response must include all of the following:

- **spec.yaml structure:** SPEC-CREDIT-LIMIT-ENFORCEMENT-001 ID, CAP-CREDIT-LIMIT-ENFORCEMENT ownership, all top-level keys from schemas/spec.schema.yaml
- **Capability & scope:** capability.owner = Anna Chen, scope.in_scope lists credit limit validation, scope.out_of_scope excludes card issuance
- **Evidence section:** All EV-* IDs referenced by the three flows and eight programs are listed with evidence_strength (confirmed_from_code / confirmed_by_sme)
- **Observed Behaviors (BEH-*):** At least 3 behaviors (e.g., "validates transaction against customer credit limit", "propagates hold decision to downstream") each tracing to ≥1 EV-*
- **Business Rules (BR-*):** At least 2 business rules lifted from module View 1 seeds, each with review_status (draft or approved based on SME confirmation), linked to supporting BEH-*
- **Modernization Decisions (DEC-*):** At least 1 decision (e.g., "store transaction audit in append-only table"), referencing BR-* or target_platform
- **Data model:** Target entities (e.g., CreditTransaction, CustomerCreditLimit) mapped to legacy OBJ-* with field mappings
- **Process flow & I/O:** process_flow.steps are business-visible phases and outcomes from the ONUS-AUTH flow analysis, not one step per legacy program; inputs (e.g., transaction), outputs (e.g., hold_decision)
- **BRD grounding:** Inputs/outputs/exceptions and process-flow framing are
  cross-checked against the approved BRD Package rather than treating BRD as
  optional collateral
- **Acceptance criteria:** AC-* items validating approved BRs; no ACs for draft or needs_sme_review BRs
- **Open questions:** No blocking TBDs for a complete spec; status = draft or in_review (not blocked)
- **spec.md outline:** Human-readable rendering of the same content
- **References to spec-review.md and traceability.md:** Output acknowledges these will be produced
- No files are created or edited

#### Scenario (Negative — Incomplete Upstream Analysis)

```text
Use /legacy-spec-writer.

User input:
I have approved module analysis (CARD-AUTH), approved flow for ONUS-AUTH, but
NIGHTLY-RECON flow analysis is still in draft status. I also have approved
program analyses for 7 of the 8 programs. Inventory and BRD Package are
approved, SME is Anna Chen.
Can I produce the spec anyway?

Return:
- the blocking TBD(s) and reason
- where the analysis is incomplete
```

#### Pass Criteria (Negative)

- **Status:** blocked_pending_source (incomplete upstream analyses block spec synthesis)
- **Does NOT produce** a complete spec.yaml
- **Creates blocking TBDs:**
  - TBD-CREDIT-LIMIT-ENFORCEMENT-001: NIGHTLY-RECON flow analysis is draft; needs approval (routes to legacy-ibmi-flow-analyzer)
  - TBD-CREDIT-LIMIT-ENFORCEMENT-002: One program analysis missing or draft (routes to legacy-ibmi-program-analyzer)
- **Refuses to invent** missing behavior or business rules from incomplete analyses
- **Identifies what IS available:** Lists ONUS-AUTH, 7 complete programs, and notes what blocks proceeding
- **Routing:** Routes to flow-analyzer for NIGHTLY-RECON and program-analyzer for the 8th program
- No files are created or edited

#### Reference Commands

```bash
codex exec -C . -s read-only --ephemeral -m gpt-5.4-mini \
  "Use /legacy-spec-writer. User input: I have: - Approved module analysis (CARD-AUTH module, all four views approved) - Approved flow analyses: ONUS-AUTH, NIGHTLY-RECON, MANUAL-AUTH (all approved) - Approved program analyses for all 8 programs referenced by those flows - Approved inventory with CARD-AUTH scope confirmed - Approved BRD Package under 05_brds/CREDIT-LIMIT-ENFORCEMENT/ with sections 1-9 reviewed by Anna Chen - SME owner: Anna Chen (capability owner) - Capability seed: CAP-CREDIT-LIMIT-ENFORCEMENT - Target platform: Java 21 + Spring Boot 3 + PostgreSQL. Help me write the spec for credit limit enforcement. Return the spec.yaml structure, spec.md outline, and indication that spec-review.md and traceability.md will be produced."
```

```bash
claude -p --model haiku --permission-mode dontAsk --tools Read --max-budget-usd 0.20 \
  "Use /legacy-spec-writer. User input: I have: - Approved module analysis (CARD-AUTH module, all four views approved) - Approved flow analyses: ONUS-AUTH, NIGHTLY-RECON, MANUAL-AUTH (all approved) - Approved program analyses for all 8 programs referenced by those flows - Approved inventory with CARD-AUTH scope confirmed - Approved BRD Package under 05_brds/CREDIT-LIMIT-ENFORCEMENT/ with sections 1-9 reviewed by Anna Chen - SME owner: Anna Chen (capability owner) - Capability seed: CAP-CREDIT-LIMIT-ENFORCEMENT - Target platform: Java 21 + Spring Boot 3 + PostgreSQL. Help me write the spec for credit limit enforcement. Return the spec.yaml structure, spec.md outline, and indication that spec-review.md and traceability.md will be produced."
```

```bash
opencode run -m opencode/minimax-m2.5-free \
  "Use /legacy-spec-writer. User input: I have: - Approved module analysis (CARD-AUTH module, all four views approved) - Approved flow analyses: ONUS-AUTH, NIGHTLY-RECON, MANUAL-AUTH (all approved) - Approved program analyses for all 8 programs referenced by those flows - Approved inventory with CARD-AUTH scope confirmed - Approved BRD Package under 05_brds/CREDIT-LIMIT-ENFORCEMENT/ with sections 1-9 reviewed by Anna Chen - SME owner: Anna Chen (capability owner) - Capability seed: CAP-CREDIT-LIMIT-ENFORCEMENT - Target platform: Java 21 + Spring Boot 3 + PostgreSQL. Help me write the spec for credit limit enforcement. Return the spec.yaml structure, spec.md outline, and indication that spec-review.md and traceability.md will be produced."
```

For the negative scenario, substitute the incomplete-upstream-analysis prompt above into
the same commands.

### `legacy-brd-to-sdd-handoff`

#### Scenario (Positive — Approved BRD And Spec)

```text
Use /legacy-brd-to-sdd-handoff.

User input:
The CREDIT-CHECK capability has approved BRD and spec packages, no unresolved
blocking TBDs, all approved BR-* have approved AC-*, evidence manifest
package_state is approved_for_inventory with all referenced EV-* resolved and
approved, and the capability owner John Smith is available to sign off on the
handoff.

Return only:
- detected skill
- status
- required output files
- evidence gate result
- signoff requirement

Do not create or edit files.
```

#### Pass Criteria (Positive)

The response must include all of the following:

- detected skill is `legacy-brd-to-sdd-handoff`
- status is `approved`, `pass`, or `approved_with_non_blocking_tbd` /
  `pass_with_warnings` only when the response explicitly carries a
  non-blocking TBD forward
- required output files are exactly `sdd-handoff.yaml`, `sdd-handoff.md`,
  `atlas-context-pack.json`, `handoff-review.md`, and `traceability.md`
- evidence gate is reported as passed against the evidence-intake manifest
  contract
- signoff requirement names a responsible SME / owner and requires name, role,
  and ISO date
- no files are created or edited

#### Scenario (Negative — Missing Spec)

```text
Use /legacy-brd-to-sdd-handoff.

Contract-only no-write smoke test. Do not inspect or rely on the actual
workspace filesystem. Report the files the skill contract would emit, not
actual created files.

User input:
The CUST-ONBOARD capability has an approved BRD with SME sign-off, but
05_specs/CUST-ONBOARD/spec.yaml does not exist. A stakeholder asks to package
the BRD for Atlas anyway.

Return exactly these labels, one per line:
- detected skill
- status
- blocking finding
- would_write_files
- would_not_write_files
- next skill
```

#### Pass Criteria (Negative)

- status is `blocked`
- blocking finding identifies the missing approved `spec.yaml`
- next skill is `legacy-spec-writer`
- `would_write_files` contains only `handoff-review.md` and
  `blocking-finding.yaml`
- `would_not_write_files` contains `sdd-handoff.yaml`, `sdd-handoff.md`,
  `atlas-context-pack.json`, and `traceability.md`
- refuses to package the BRD directly for Atlas
- no files are created or edited

#### Reference Commands

```bash
codex exec -C . -s read-only --ephemeral -m gpt-5.4-mini \
  "Use /legacy-brd-to-sdd-handoff. User input: The CREDIT-CHECK capability has approved BRD and spec packages, no unresolved blocking TBDs, all approved BR-* have approved AC-*, evidence manifest package_state is approved_for_inventory with all referenced EV-* resolved and approved, and the capability owner John Smith is available to sign off on the handoff. Return only: detected skill; status; required output files; evidence gate result; signoff requirement. Do not create or edit files."
```

```bash
claude -p "Use /legacy-brd-to-sdd-handoff. User input: The CREDIT-CHECK capability has approved BRD and spec packages, no unresolved blocking TBDs, all approved BR-* have approved AC-*, evidence manifest package_state is approved_for_inventory with all referenced EV-* resolved and approved, and the capability owner John Smith is available to sign off on the handoff. Return only: detected skill; status; required output files; evidence gate result; signoff requirement. Do not create or edit files." \
  --model haiku --permission-mode dontAsk --tools Read
```

```bash
opencode run -m opencode/minimax-m2.5-free \
  "Use /legacy-brd-to-sdd-handoff. User input: The CREDIT-CHECK capability has approved BRD and spec packages, no unresolved blocking TBDs, all approved BR-* have approved AC-*, evidence manifest package_state is approved_for_inventory with all referenced EV-* resolved and approved, and the capability owner John Smith is available to sign off on the handoff. Return only: detected skill; status; required output files; evidence gate result; signoff requirement. Do not create or edit files."
```

For the negative scenario, substitute the missing-spec contract-only prompt
above into the same commands.

### `legacy-traceability-packager`

#### Scenario (Positive — Clean Traceability Package)

```text
Use /legacy-traceability-packager.

Contract-only no-write smoke test. Do not inspect or rely on the actual
workspace filesystem. Report the files the skill contract would emit, not
actual created files.

User input:
The CREDIT-CHECK capability has an approved spec.yaml, approved upstream
inventory/program/flow/module analyses, an approved BRD, and an approved
evidence manifest. All referenced EV-* resolve in the manifest, no evidence
has sensitivity unknown, every approved BR-* has EV-*, BEH-*, and AC-* links,
every AC-* validates an approved BR-*, every TC-* validates an AC-* or BR-*,
no orphan evidence exists, no open TBD exists, and the capability owner John
Smith is available to sign off on the traceability package.

Return exactly these labels, one per line:
- detected skill
- status
- would_write_files
- would_not_write_files
- key gates
- signoff requirement
```

#### Pass Criteria (Positive)

- detected skill is `legacy-traceability-packager`
- status is `pass`
- `would_write_files` contains exactly `traceability-package.yaml`,
  `traceability-package.md`, `coverage-audit.md`, and
  `traceability-review.md`
- `would_not_write_files` contains `blocking-findings.yaml`
- key gates include evidence manifest resolved / sensitivity passed,
  BR closure passed, AC validation passed, no dangling IDs, and no open TBDs
- signoff requirement names the capability-owner SME and requires name, role,
  and ISO date
- no files are created or edited

#### Scenario (Negative — Dangling AC Reference)

```text
Use /legacy-traceability-packager.

Contract-only no-write smoke test. Do not inspect or rely on the actual
workspace filesystem. Report the files the skill contract would emit, not
actual created files.

User input:
The ORDER-ENTRY capability has approved upstream artifacts and an approved
spec.yaml, but AC-ORDER-ENTRY-004.validates references BR-ORDER-ENTRY-007.
BR-ORDER-ENTRY-007 is not defined in spec.yaml.business_rules[]. A stakeholder
asks the packager to create the missing BR and continue.

Return exactly these labels, one per line:
- detected skill
- status
- blocking finding
- forbidden action
- would_write_files
- would_not_write_files
- next skill
```

#### Pass Criteria (Negative)

- detected skill is `legacy-traceability-packager`
- status is `blocked`
- blocking finding is `BR-DANGLING-IN-AC`
- forbidden action says the packager must not mint `BR-ORDER-ENTRY-007` or
  rewrite `AC-ORDER-ENTRY-004`
- `would_write_files` contains only `traceability-review.md` and
  `blocking-findings.yaml`
- `would_not_write_files` contains `traceability-package.yaml`,
  `traceability-package.md`, and `coverage-audit.md`
- next skill is `legacy-spec-writer`
- no files are created or edited

#### Reference Commands

```bash
codex exec -C . -s read-only --ephemeral -m gpt-5.4-mini \
  "Use /legacy-traceability-packager. Contract-only no-write smoke test. Do not inspect or rely on the actual workspace filesystem. Report the files the skill contract would emit, not actual created files. User input: The CREDIT-CHECK capability has an approved spec.yaml, approved upstream inventory/program/flow/module analyses, an approved BRD, and an approved evidence manifest. All referenced EV-* resolve in the manifest, no evidence has sensitivity unknown, every approved BR-* has EV-*, BEH-*, and AC-* links, every AC-* validates an approved BR-*, every TC-* validates an AC-* or BR-*, no orphan evidence exists, no open TBD exists, and the capability owner John Smith is available to sign off on the traceability package. Return exactly these labels, one per line: detected skill; status; would_write_files; would_not_write_files; key gates; signoff requirement."
```

```bash
claude -p "Use /legacy-traceability-packager. Contract-only no-write smoke test. Do not inspect or rely on the actual workspace filesystem. Report the files the skill contract would emit, not actual created files. User input: The CREDIT-CHECK capability has an approved spec.yaml, approved upstream inventory/program/flow/module analyses, an approved BRD, and an approved evidence manifest. All referenced EV-* resolve in the manifest, no evidence has sensitivity unknown, every approved BR-* has EV-*, BEH-*, and AC-* links, every AC-* validates an approved BR-*, every TC-* validates an AC-* or BR-*, no orphan evidence exists, no open TBD exists, and the capability owner John Smith is available to sign off on the traceability package. Return exactly these labels, one per line: detected skill; status; would_write_files; would_not_write_files; key gates; signoff requirement." \
  --model haiku --permission-mode dontAsk --tools Read
```

```bash
opencode run -m opencode/minimax-m2.5-free \
  "Use /legacy-traceability-packager. Contract-only no-write smoke test. Do not inspect or rely on the actual workspace filesystem. Report the files the skill contract would emit, not actual created files. User input: The CREDIT-CHECK capability has an approved spec.yaml, approved upstream inventory/program/flow/module analyses, an approved BRD, and an approved evidence manifest. All referenced EV-* resolve in the manifest, no evidence has sensitivity unknown, every approved BR-* has EV-*, BEH-*, and AC-* links, every AC-* validates an approved BR-*, every TC-* validates an AC-* or BR-*, no orphan evidence exists, no open TBD exists, and the capability owner John Smith is available to sign off on the traceability package. Return exactly these labels, one per line: detected skill; status; would_write_files; would_not_write_files; key gates; signoff requirement."
```

For the negative scenario, substitute the dangling-AC-reference prompt above
into the same commands.

### `legacy-sme-review-facilitator`

#### Scenario (Positive — Completed SME Review)

```text
Use /legacy-sme-review-facilitator.

No-write smoke test. Do not create or edit files. Use only the scenario text
below and the skill contract.

Positive scenario:
capability_slug CREDIT-CHECK exactly. Artifact 05_brds/CREDIT-CHECK/brd.md is
approved_with_non_blocking_tbd. SME owner Jane Doe, Credit Operations Lead, is
available on 2026-05-16. Evidence manifest explicitly lists
EV-CREDIT-CHECK-015 sensitivity internal redaction_status not_required,
EV-CREDIT-CHECK-008 sensitivity internal redaction_status not_required,
EV-CREDIT-CHECK-012 sensitivity internal redaction_status not_required, and
EV-CREDIT-CHECK-018 sensitivity internal redaction_status not_required.

Review items:
- BRD sections 1-9 are present; section 3 Channels is accepted with
  TBD-CREDIT-CHECK-004 carried as non-blocking
- BEH-CREDIT-CHECK-001 should be confirmed
- BR-CREDIT-CHECK-003 should be rejected because interest compounds daily only
  above the configured balance threshold
- TBD-CREDIT-CHECK-004 should be deferred to Digital Channels SME by
  2026-05-23

Return only:
- skill_invoked
- status
- output_directory
- files_to_emit
- decisions
- follow_up_routing
- no_write_confirmation
```

#### Pass Criteria (Positive)

- invokes `legacy-sme-review-facilitator`
- returns completed / pass / ready status
- preserves the capability slug exactly in
  `07_sme_reviews/CREDIT-CHECK/review-v1/` or an equivalent review slug under
  `07_sme_reviews/CREDIT-CHECK/`
- lists exactly the completed-review files: `review-session.md`,
  `question-pack.md`, `sme-decision-log.yaml`, `sme-signoff.md`, and
  `follow-up-findings.yaml`
- records decisions for `BEH-CREDIT-CHECK-001` as `confirmed`,
  `BR-CREDIT-CHECK-003` as `rejected`, and `TBD-CREDIT-CHECK-004` as
  `deferred`
- records BRD functional-analysis coverage for sections 1-9, with section 3
  accepted with a named `TBD-*`
- routes the rule revision to `legacy-spec-writer`
- routes the deferred channel TBD to Digital Channels SME with target date
  `2026-05-23`
- confirms no files were created or edited

#### Scenario (Negative — Missing SME And Unknown Evidence)

```text
Use /legacy-sme-review-facilitator.

No-write smoke test. Do not create or edit files. Use only the scenario text
below and the skill contract.

Negative scenario:
capability_slug ORDER-ENTRY exactly. Artifact 05_brds/ORDER-ENTRY/brd.md is
approved_with_non_blocking_tbd, but no named SME owner is assigned. Evidence
manifest lists EV-ORDER-ENTRY-001 sensitivity unknown redaction_status unknown
and EV-ORDER-ENTRY-002 sensitivity internal redaction_status unknown. A
stakeholder asks to proceed and generate the decision log anyway.

Return only:
- skill_invoked
- status
- output_directory
- files_to_emit
- files_not_to_emit
- blockers
- remediation_routes
- no_write_confirmation
```

#### Pass Criteria (Negative)

- invokes `legacy-sme-review-facilitator`
- status is `blocked`
- preserves `ORDER-ENTRY` exactly in the reported review directory
- `files_to_emit` contains only `review-session.md` and
  `blocked-findings.yaml`
- `files_not_to_emit` contains `question-pack.md`, `sme-decision-log.yaml`,
  `sme-signoff.md`, and `follow-up-findings.yaml`
- blockers include missing named SME owner, `EV-ORDER-ENTRY-001` unknown
  sensitivity/redaction status, and `EV-ORDER-ENTRY-002` unknown redaction
  status
- remediation routes include SME owner assignment and
  `legacy-ibmi-evidence-intake`
- refuses the stakeholder request to generate a decision log anyway
- confirms no files were created or edited

For reference commands, use the same Codex, Claude Code, and OpenCode command
shapes shown above, replacing the prompt with the positive or negative scenario
here.

### `legacy-step-contract`

#### Scenario (Positive — Review A Filled Step Contract)

```text
Use /legacy-step-contract.

User input:
Review the filled Step Contract example at
skills/legacy-step-contract/examples/inventory-pass/step-contract-block.md.
Return only:
- whether the INPUT, EXECUTION, OUTPUT, and VALIDATION sections are present
- compact validation result status
- downstream_next_step
- remediation_step
```

#### Pass Criteria (Positive)

The response must include all of the following:

- identifies all four sections: INPUT, EXECUTION, OUTPUT, VALIDATION
- reports status as `pass`
- reports `downstream_next_step: legacy-ibmi-program-analyzer`
- reports `remediation_step: none`
- does not invent IBM i objects or business rules
- does not edit files

#### Scenario (Negative — Missing SME Owner)

```text
Use /legacy-step-contract.

User input:
I am authoring a Step Contract for inventory. The redaction gate is clear and
the evidence scope has EV-CREDIT-CHECK-001, but sme_required is yes and
sme_owner is blank. Can the inventory step execute?

Return only:
- status
- blocking category
- required remediation_step
```

#### Pass Criteria (Negative)

- reports status as `blocked`
- classifies the blocker under `sme_questions` or equivalent SME-owner missing category
- says the step must not execute until an SME owner is assigned
- does not route downstream to program analysis
- does not edit files

#### Reference Commands

```bash
codex exec -C . -s read-only --ephemeral -m gpt-5.4-mini \
  "Use /legacy-step-contract. User input: Review the filled Step Contract example at skills/legacy-step-contract/examples/inventory-pass/step-contract-block.md. Return only: whether the INPUT, EXECUTION, OUTPUT, and VALIDATION sections are present; compact validation result status; downstream_next_step; remediation_step."
```

```bash
claude -p --model haiku --permission-mode dontAsk --tools Read --max-budget-usd 0.20 \
  "Use /legacy-step-contract. User input: Review the filled Step Contract example at skills/legacy-step-contract/examples/inventory-pass/step-contract-block.md. Return only: whether the INPUT, EXECUTION, OUTPUT, and VALIDATION sections are present; compact validation result status; downstream_next_step; remediation_step."
```

```bash
opencode run -m opencode/minimax-m2.5-free \
  "Use /legacy-step-contract. User input: Review the filled Step Contract example at skills/legacy-step-contract/examples/inventory-pass/step-contract-block.md. Return only: whether the INPUT, EXECUTION, OUTPUT, and VALIDATION sections are present; compact validation result status; downstream_next_step; remediation_step."
```

For the negative scenario, substitute the missing-SME-owner prompt above into
the same commands.

### `legacy-step-validator`

#### Scenario (Positive — Validate Pass Example)

```text
Use /legacy-step-validator.

User input:
Validate the example package at
skills/legacy-step-validator/examples/pass/step-validation-report.md.
Return only:
- detected step_type
- status
- blocking_items
- downstream_next_step
- remediation_step
```

#### Pass Criteria (Positive)

The response must include all of the following:

- detects or reports step type as `inventory`
- reports status as `pass`
- reports `blocking_items: []`
- reports `downstream_next_step: legacy-ibmi-program-analyzer`
- reports `remediation_step: none`
- does not approve any new SME decision beyond the recorded example
- does not edit files

#### Scenario (Negative — Validate Blocked Example)

```text
Use /legacy-step-validator.

User input:
Validate the blocked example package at
skills/legacy-step-validator/examples/blocked/.
Return only:
- detected step_type
- status
- blocking_items
- downstream_next_step
- remediation_step
```

#### Pass Criteria (Negative)

- detects or reports step type as `module`
- reports status as `blocked`
- lists exactly four blocking findings:
  - `FIND-CARD-AUTH-001`
  - `FIND-CARD-AUTH-002`
  - `FIND-CARD-AUTH-003`
  - `FIND-CARD-AUTH-004`
- reports `downstream_next_step: none`
- reports `remediation_step: legacy-ibmi-flow-analyzer`
- does not edit files

#### Reference Commands

```bash
codex exec -C . -s read-only --ephemeral -m gpt-5.4-mini \
  "Use /legacy-step-validator. User input: Validate the example package at skills/legacy-step-validator/examples/pass/step-validation-report.md. Return only: detected step_type; status; blocking_items; downstream_next_step; remediation_step."
```

```bash
claude -p --model haiku --permission-mode dontAsk --tools Read --max-budget-usd 0.20 \
  "Use /legacy-step-validator. User input: Validate the example package at skills/legacy-step-validator/examples/pass/step-validation-report.md. Return only: detected step_type; status; blocking_items; downstream_next_step; remediation_step."
```

```bash
opencode run -m opencode/minimax-m2.5-free \
  "Use /legacy-step-validator. User input: Validate the example package at skills/legacy-step-validator/examples/pass/step-validation-report.md. Return only: detected step_type; status; blocking_items; downstream_next_step; remediation_step."
```

For the negative scenario, substitute the blocked-example prompt above into the
same commands.

### `legacy-modernization-decision-writer`

#### Scenario (Positive — Approved Decision Package)

```text
Use /legacy-modernization-decision-writer. Runtime smoke test.
You may read only the legacy-modernization-decision-writer skill contract and
templates if needed; do not inspect or rely on actual spec/evidence artifact
files, and do not write files.

User input:
in_review spec SPEC-ORDERS-001 for CAP-ORDERS-001 has approved BR-ORDERS-004
supported by EV-ORDERS-016 confirmed_by_sme, approved BEH-ORDERS-007 supported
by EV-ORDERS-015 confirmed_from_code, and draft DEC-ORDERS-001 category
async_boundary: use async event-driven fulfillment. Target platform constraint:
AWS SQS/SNS approved by ARCH-2026-05-16. Alternatives: sync batch, async queue,
hybrid. No blocking TBDs; sensitivity resolved; SME Jane Smith, architecture
owner Bob Jones, and product owner Alice Chen have approved.

Return only these labels, one per line:
- detected skill
- status
- required output files
- DEC review_status
- pending approvals
- reconciliation target
- forbidden outputs
- no-write confirmation

For required output files, use the canonical four-file
05_decisions/<CAPABILITY-SLUG>/ package from the skill contract, with
capability slug ORDERS.
```

#### Pass Criteria (Positive)

- detects `legacy-modernization-decision-writer`
- reports a pass/approved outcome for the decision package
- returns exactly the canonical four-file package:
  - `05_decisions/ORDERS/modernization-decisions.yaml`
  - `05_decisions/ORDERS/decisions/DEC-ORDERS-001.md`
  - `05_decisions/ORDERS/decision-review.md`
  - `05_decisions/ORDERS/traceability.md`
- reports `DEC review_status: approved`
- reports no pending approvals
- reconciles back to `spec.yaml.modernization_decisions[]`
- forbids implementation architecture/design, task breakdown, code, test cases,
  and new acceptance criteria
- creates or edits no files

#### Scenario (Negative — Invented Platform Decision)

```text
Use /legacy-modernization-decision-writer. Runtime smoke test.
Do not ask clarifying questions. You may read only the decision-writer skill
contract and templates if needed. Do not inspect actual spec or evidence
artifact files. Do not write files.

User input:
draft spec SPEC-ORDER-DATA-001 for CAP-ORDER-DATA-001 contains
DEC-ORDER-DATA-001 category data: use PostgreSQL and Kafka because modern.
The DEC references missing BR-ORDER-DATA-099, has no BEH link, no EV link,
target_platform_constraints is empty, evidence sensitivity is unknown,
architecture owner and product owner are not assigned, and blocking
TBD-ORDER-DATA-015 about customer deduplication is unresolved. A stakeholder
asks to mark the DEC approved and proceed.

Return exactly these labels, one per line:
- detected skill
- status
- blocking findings
- DEC review_status
- TBD handling
- remediation route
- forbidden outputs
- no-write confirmation
```

#### Pass Criteria (Negative)

- detects `legacy-modernization-decision-writer`
- reports status as blocked or stop/validation failed
- blocks missing BR/BEH/EV grounding, unknown sensitivity, empty target platform
  constraints, missing architecture/product authority, and the unresolved
  blocking TBD
- keeps `DEC review_status` as `draft` or otherwise not approved
- requires `TBD-ORDER-DATA-015` to be resolved before approval
- routes remediation back to `legacy-spec-writer` or equivalent spec/evidence
  repair before rerunning decision approval
- forbids fake approval, invented PostgreSQL/Kafka rationale, new BR/BEH/EV/AC
  minting, design/SDD artifacts, tasks, code, and tests
- creates or edits no files

#### Reference Commands

```bash
codex exec -C . -s read-only --ephemeral -m gpt-5.4-mini \
  "<positive or negative prompt above>"
```

```bash
claude -p --model haiku --permission-mode dontAsk --tools Read --max-budget-usd 0.20 \
  "<positive or negative prompt above>"
```

```bash
opencode run -m opencode/minimax-m2.5-free \
  "<positive or negative prompt above>"
```

#### Runtime Result (2026-05-16)

| Runtime | Model | Discovery | Trigger | Outcome |
| --- | --- | --- | --- | --- |
| Codex CLI | `gpt-5.4-mini` | loaded | positive and negative no-write scenarios executed | passed |
| Claude Code | `haiku` (Read-only tools) | loaded | positive and negative no-write scenarios executed | passed |
| OpenCode | `opencode/minimax-m2.5-free` | loaded | positive and negative no-write scenarios executed | passed |

Positive smoke confirmed the canonical `05_decisions/ORDERS/` package,
approved DEC status, no pending approvals, reconciliation to
`spec.yaml.modernization_decisions[]`, and no forbidden outputs.

Negative smoke confirmed invented PostgreSQL/Kafka decisions are blocked when
BR/BEH/EV grounding, evidence sensitivity, decision authority, and blocking TBD
resolution are missing.

Recorded in `docs/runtime-matrix.md`. The v0.1.0 scorecard is recorded at
`docs/reviews/legacy-modernization-decision-writer-v0.1.0-scorecard.md`.

## Pass Example — `legacy-step-contract` v0.1.1

| Runtime | Model | Discovery | Trigger | Outcome |
| --- | --- | --- | --- | --- |
| Codex CLI | `gpt-5.4-mini` | loaded | positive and negative scenarios executed | passed |
| Claude Code | `haiku` (Read-only tools) | loaded | positive and negative scenarios executed | passed |
| OpenCode | `opencode/minimax-m2.5-free` | loaded | positive and negative scenarios executed | passed |

Positive smoke confirmed all four sections were present and returned
`status: pass`, `downstream_next_step: legacy-ibmi-program-analyzer`, and
`remediation_step: none`.

Negative smoke confirmed `sme_required: yes` with empty `sme_owner` blocks
execution and requires SME owner assignment before inventory can run.

Recorded in `docs/runtime-matrix.md`. The refreshed v0.1.1 scorecard is
recorded at
`docs/reviews/legacy-step-contract-v0.1.1-scorecard.md`.

## Pass Example — `legacy-step-validator` v0.1.1

| Runtime | Model | Discovery | Trigger | Outcome |
| --- | --- | --- | --- | --- |
| Codex CLI | `gpt-5.4-mini` | loaded | positive and negative scenarios executed | passed |
| Claude Code | `haiku` (Read-only tools) | loaded | positive and negative scenarios executed | passed |
| OpenCode | `opencode/minimax-m2.5-free` | loaded | positive and negative scenarios executed | passed |

Positive smoke confirmed inventory pass output with no blocking findings and
`downstream_next_step: legacy-ibmi-program-analyzer`.

Negative smoke confirmed module blocked output with exactly four blocking
findings (`FIND-CARD-AUTH-001` through `FIND-CARD-AUTH-004`),
`downstream_next_step: none`, and
`remediation_step: legacy-ibmi-flow-analyzer`.

Recorded in `docs/runtime-matrix.md`. The refreshed v0.1.1 scorecard is
recorded at
`docs/reviews/legacy-step-validator-v0.1.1-scorecard.md`.

## Pass Example — `legacy-modernization-orchestrator` v0.1.1

| Runtime | Model | Discovery | Trigger | Outcome |
| --- | --- | --- | --- | --- |
| Codex CLI | `gpt-5.4-mini` | loaded | executed + matched pass criteria for positive and negative scenarios | passed |
| Claude Code | `haiku` (Read-only tools) | loaded | executed + matched pass criteria | passed |
| OpenCode | `opencode/minimax-m2.5-free` | loaded | executed + matched pass criteria | passed |

Recorded in `docs/runtime-matrix.md`. Scorecard moved from v0.1.0 (9.0 cap)
to v0.1.1 (9.5, field-pilot ready) at
[docs/reviews/legacy-modernization-orchestrator-v0.1.1-scorecard.md](reviews/legacy-modernization-orchestrator-v0.1.1-scorecard.md).

## Pass Example — `legacy-ibmi-screen-report-analyzer` v0.1.0

### Positive DSPF Scenario

```text
Use /legacy-ibmi-screen-report-analyzer.

User input:
I have an approved inventory object OBJ-ORDER-ENTRY-003 for ORDERENT DSPF.
Evidence:
- EV-ORDER-ENTRY-012: DSPF source at
  skills/legacy-ibmi-screen-report-analyzer/examples/interactive-subfile-positive/input-dspf.txt,
  sensitivity safe.
- EV-ORDER-ENTRY-013: redacted screen capture sequence described by the
  example analysis.
- EV-ORDER-ENTRY-014: safe job log excerpt described by the example analysis.
Inventory is approved_with_non_blocking_tbd and evidence is redacted. No SME
sign-off evidence is included.

Analyze the screen/report artifact as a no-write smoke test. Do not create or
edit files. For artifact filename, return the canonical output artifact
filename from the skill output contract, not the input evidence filename.

Return only:
- skill invoked
- canonical artifact filename
- surface type
- output sections present
- evidence/redaction gates
- allowed ID namespaces
- forbidden ID namespaces
- at least three TBD or SEED items
- handoff status
```

### Pass Criteria

- invokes `legacy-ibmi-screen-report-analyzer`
- returns `screen-report-analysis-OBJ-ORDER-ENTRY-003.md`
- classifies the surface as DSPF / interactive screen with subfile
- lists required output sections from the screen/report analysis contract
- reports evidence/redaction gates as passing and SME sign-off as absent/open
- allows `OBJ-*`, `EV-*`, `BEH-*`, `IN-*`, `OUT-*`, `DATA-*`, `SEED-*`,
  and `TBD-*`
- forbids `BR-*`, `CAP-*`, `DEC-*`, and Java implementation IDs
- surfaces at least three `TBD-*` or `SEED-*` items instead of inventing
  program behavior
- keeps handoff status `draft` or `needs_sme_review`, not `approved`
- creates or edits no files

| Runtime | Model | Discovery | Trigger | Outcome |
| --- | --- | --- | --- | --- |
| Codex CLI | `gpt-5.4-mini` | loaded | positive DSPF no-write scenario executed | passed |
| Claude Code | `haiku` (Read-only tools) | loaded | positive DSPF no-write scenario executed | passed |
| OpenCode | `opencode/minimax-m2.5-free` | loaded | positive DSPF no-write scenario executed | passed |

Recorded in `docs/runtime-matrix.md`. The v0.1.0 scorecard remains repo-ready,
not field-pilot ready, pending SME/domain validation with real redacted
screen/report evidence.

## Pass Example - `legacy-golden-master-test-planner` v0.1.0

### Positive Approved Plan Scenario

```text
Use /legacy-golden-master-test-planner.

Read the project skill if needed. Do not create or edit files.

User input:
Approved spec package: 05_specs/CREDIT-LIMIT/spec.yaml, status approved.
Approved business rules: BR-CREDIT-LIMIT-001 approves an order when amount is
within available credit; BR-CREDIT-LIMIT-002 rejects an order when amount
exceeds available credit. Approved acceptance criteria: AC-CREDIT-LIMIT-001
validates BR-CREDIT-LIMIT-001 happy path; AC-CREDIT-LIMIT-002 validates
BR-CREDIT-LIMIT-002 rejection path; AC-CREDIT-LIMIT-003 validates exact-limit
boundary behavior. Runtime evidence is redacted and approved:
EV-CREDIT-LIMIT-001 input valid-order sample, EV-CREDIT-LIMIT-002 observed
approved output, EV-CREDIT-LIMIT-003 input rejected-order sample,
EV-CREDIT-LIMIT-004 observed CREDIT_LIMIT_EXCEEDED output, EV-CREDIT-LIMIT-005
input exact-limit boundary sample, EV-CREDIT-LIMIT-006 observed approved
boundary output. Evidence manifest and redaction log say all samples are
redacted and no sensitivity is unknown. Capability-owner SME Jane Smith, test
data owner Raj Patel, and forward SDLC test owner Maya Chen have approved the
selected cases.

Return only:
- status
- files that would be produced
- TC list with validates and evidence refs
- coverage result
- gate/check result
- no-write confirmation
```

### Positive Pass Criteria

- invokes `legacy-golden-master-test-planner`
- returns `approved` or equivalent pass status
- lists exactly the five `06_quality/CREDIT-LIMIT/` files:
  `golden-master-tests.yaml`, `golden-master-tests.md`,
  `equivalence-coverage.md`, `sample-data-manifest.md`, and
  `test-plan-review.md`
- emits `TC-CREDIT-LIMIT-001`, `TC-CREDIT-LIMIT-002`, and
  `TC-CREDIT-LIMIT-003`
- each `TC-*` cites both input and expected-output `EV-*`
- reports full BR/AC coverage and no blocking gaps
- confirms no files were created or edited

### Negative Missing Expected-Output Scenario

```text
Use /legacy-golden-master-test-planner.

Read the project skill if needed. Do not create or edit files.

User input:
Approved spec package: 05_specs/CREDIT-LIMIT/spec.yaml, status approved.
Approved business rule BR-CREDIT-LIMIT-003 requires rejecting an order when the
customer is missing. Approved acceptance criterion AC-CREDIT-LIMIT-004
validates the missing-customer rejection path. The only available evidence is
EV-CREDIT-LIMIT-007, a redacted input sample with a missing customer ID. There
is no job log, spool output, response file, screen output, DB snapshot, or
other observed legacy expected-output evidence for this path. Evidence
sensitivity for EV-CREDIT-LIMIT-007 is no, and the redaction log is approved.
SME Jane Smith asks whether the planner can create a golden master case anyway
based on the approved AC.

Return only:
- status
- files that would be produced
- TC list, if any
- blocking findings
- downstream next step
- no-write confirmation
```

### Negative Pass Criteria

- invokes `legacy-golden-master-test-planner`
- returns `blocked`
- lists only `06_quality/CREDIT-LIMIT/test-plan-review.md` and
  `06_quality/CREDIT-LIMIT/blocking-findings.yaml` as blocked-run outputs
- mints no `TC-*`
- explicitly refuses to infer expected output from `AC-CREDIT-LIMIT-004`
- routes to runtime evidence collection / `legacy-ibmi-evidence-intake`
- confirms no files were created or edited

| Runtime | Model | Discovery | Trigger | Outcome |
| --- | --- | --- | --- | --- |
| Codex CLI | `gpt-5.4-mini` | loaded | positive and negative no-write scenarios executed | passed |
| Claude Code | `haiku` (Read-only tools) | loaded | positive and negative no-write scenarios executed | passed |
| OpenCode | `opencode/minimax-m2.5-free` | loaded | positive and negative no-write scenarios executed | passed |

Recorded in `docs/runtime-matrix.md`. The v0.1.0 scorecard is recorded at
`docs/reviews/legacy-golden-master-test-planner-v0.1.0-scorecard.md`.

## Pass Example - `legacy-runtime-matrix-tester` v0.1.0

### Positive Matrix Update Scenario

```text
Use /legacy-runtime-matrix-tester.

Read the project skill if needed. Do not create or edit files.

User input:
I just finished testing legacy-ibmi-inventory v0.1.0 and need the runtime
matrix/test report recommendation. Treat the following as already-captured
test evidence; do not run subprocesses.

Pre-test checks:
- canonical source exists at skills/legacy-ibmi-inventory/SKILL.md
- scripts/sync-skills.sh --skill legacy-ibmi-inventory --target all --check
  exited 0
- python3 scripts/check-spec-contract.py exited 0
- docs/runtime-smoke-tests.md contains positive and negative prompts

Runtime evidence:
- Codex CLI, model gpt-5.4-mini, read-only ephemeral: adapter loaded,
  positive trigger passed, negative missing-evidence case blocked, no writes
- Claude Code, model haiku, Read-only tools: adapter loaded, positive trigger
  passed, negative missing-evidence case blocked, no writes
- OpenCode, model opencode/minimax-m2.5-free: adapter loaded, positive trigger
  passed, negative missing-evidence case blocked, no writes

Use the standard scorecard path for this target skill:
docs/reviews/legacy-ibmi-inventory-v0.1.0-scorecard.md.
According to the tester decision rules, an all-passed evidence set with no
blockers is `field-pilot ready`.

Return only:
- pre-test decision
- per-runtime final statuses
- updated runtime matrix row as a full Markdown table row with exactly six
  cells: skill, version, Codex, Claude Code, OpenCode, notes. The skill cell
  must be backtick-quoted, version/status cells must not be backticked, and
  runtime statuses must be lowercase exact enum values. Notes must include the
  test date, runtime models, and scorecard path.
- scorecard decision, using exactly one of `repo-ready`, `field-pilot ready`,
  or `blocked`
- scorecard location
- no-write confirmation
```

### Positive Pass Criteria

- invokes `legacy-runtime-matrix-tester`
- records the per-skill sync check, not a whole-repo drift check
- returns final status `passed` for Codex, Claude Code, and OpenCode
- returns a valid `docs/runtime-matrix.md` table row for
  `legacy-ibmi-inventory` v0.1.0
- marks the scorecard decision `field-pilot ready`
- mentions the scorecard path
  `docs/reviews/legacy-ibmi-inventory-v0.1.0-scorecard.md`
- confirms no files were created or edited

### Negative Runtime Unavailable Scenario

```text
Use /legacy-runtime-matrix-tester.

Read the project skill if needed. Do not create or edit files.

User input:
I finished legacy-spec-writer v0.2.0 and synced it to Codex and OpenCode. The
Codex and OpenCode positive/negative smoke tests passed. Claude Code cannot be
tested because the local CLI reports: Not logged in - run claude auth login.
Should I mark Claude Code as passed anyway?

Skill name: legacy-spec-writer
Runtimes to test: claude-code
Run mode: discovery
Canonical version: v0.2.0

The Claude Code adapter is synced, but runtime execution is unavailable due to
auth. Matrix status values are only `not tested`, `synced`, `loaded`,
`executed`, `passed`, and `failed`; environment-unavailable synced adapters
should remain `synced`.

Return only:
- blocking issues
- recommendation for matrix entry
- scorecard decision
- whether field pilot is blocked
- no-write confirmation
```

### Negative Pass Criteria

- invokes `legacy-runtime-matrix-tester`
- refuses to mark Claude Code as `passed` or `executed`
- recommends Claude Code status `synced` with an auth/environment blocker
- recommends scorecard decision `blocked`, not `field-pilot ready`
- states that field-pilot readiness remains blocked until Claude Code passes
- confirms no files were created or edited

| Runtime | Model | Positive | Negative | Result |
| --- | --- | --- | --- | --- |
| Codex CLI | `gpt-5.4-mini` | Returned six-cell matrix row with lowercase statuses, `field-pilot ready` decision, scorecard path, and no-write confirmation. | Kept Claude Code at `synced`, refused false `passed`, marked smoke run `blocked`, and confirmed no writes. | passed |
| Claude Code | `haiku` with Read-only tools | Returned six-cell matrix row with lowercase statuses, `field-pilot ready` decision, scorecard path, and no-write confirmation. | Kept Claude Code at `synced`, returned `blocked`, and blocked field pilot until auth is fixed. | passed |
| OpenCode | `opencode/minimax-m2.5-free` | Returned six-cell matrix row with lowercase statuses, `field-pilot ready` decision, scorecard path, and no-write confirmation. | Kept Claude Code at `synced`, returned `blocked`, and blocked field pilot until auth is fixed. | passed |

Recorded in `docs/runtime-matrix.md`. The v0.1.0 scorecard is recorded at
`docs/reviews/legacy-runtime-matrix-tester-v0.1.0-scorecard.md`.

## Adding A New Skill

When a new skill is added:

1. Append a positive trigger prompt to the "Test Prompts For
   Currently-Implemented Skills" section in the same PR that introduces the
   skill
2. Include a negative-case prompt if the skill has a stop condition
3. Run the protocol in all three runtimes before the skill is merged with
   `passed` status

This keeps the protocol authoritative and prevents per-skill drift.
