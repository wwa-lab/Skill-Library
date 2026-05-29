# Routing Decision Table

The complete current-stage × desired-outcome → next-skill table for the
reverse chain.

Skill statuses:

- **Implemented**: SKILL.md exists, scored ≥ 9.0
- **Planned**: in the README target list, not yet built
- **Future**: aspirational (other-platform Layer 1)
- **Doc-only**: not a skill — a documented gate or process
- **External**: handoff to `wwa-lab/build-agent-skill`

## Full Decision Table

| Current Stage | Desired Outcome | Route To | Skill Status | Note |
| --- | --- | --- | --- | --- |
| 0 — Evidence Intake | Any | `legacy-ibmi-evidence-intake` | Implemented v0.1.0 | Register metadata, assign `EV-*` IDs, govern redaction, and produce the manifest. The agent must not inspect unredacted sensitive content. |
| 0p — Document Evidence Intake | Format-normalize raw Office/Visio/PDF/image documents before flow context normalization | `legacy-document-evidence-intake` | Implemented v0.1.0 | Use when business/technical documents are still in `.xlsx`/`.xlsm`/`.xls`, `.docx`/`.doc`, `.pptx`/`.ppt`, `.vsdx`/`.vsd`, `.pdf`, or image/scanned form and no `document-intake/<DOCSET-SLUG>/intake.manifest.yaml` exists yet. Converts to Markdown/CSV/PDF/PNG/SVG with manifests and `DOC-*`/`FRAG-*` evidence coordinates; gates `ready`/`ready_with_warnings`/`blocked`. Static-only macro policy; never executes VBA. Routes unauthorized or sensitivity-unknown material to `legacy-ibmi-evidence-intake`; `ready`/`ready_with_warnings` hands off to `legacy-flow-context-normalizer`. Does not infer business rules, generate BRD/spec content, or classify flow views. |
| 0d — Flow Context Normalization | Convert or triage scattered documents/specs before module context intake | `legacy-flow-context-normalizer` | Implemented v0.1.8 | Use when Visio, Word, Excel, PDF, PowerPoint, Function Specs, Technical Designs, Program Specs, File Specs, interface specs, data dictionaries, exported diagrams, RAG summaries, or SME notes exist but the standard context views are not yet normalized or SME-reviewed. Strong/partial inputs produce Mermaid-backed draft context views under `00_context_packages/`; sparse authorized inputs produce `triage_needs_source_enrichment`; owner-accepted sparse packages may become `ready_with_warnings` with carry-forward TBDs; only unauthorized, unreadable, out-of-scope, or boundaryless inputs block. Draft context steps are never promoted to approved rules or canonical module flows. |
| 0d — Risk-Accepted Sparse Context | Continue after source owner/SME confirms no additional document, spec, or flow input can be provided | `legacy-module-context-intake` | Implemented v0.1.2 | Use only when `flow-context-index.yaml` has `normalization.status: ready_with_warnings`, `quality_level: L1 sparse`, and `risk_acceptance.status: accepted`. Context intake must preserve all gaps as low-confidence TBDs and must not route directly to module analysis or BRD generation without its own gates. |
| 0m — Module Context Intake | Normalize RAG/context package | `legacy-module-context-intake` | Implemented v0.1.0 | Use when the user has external RAG output, source snippets, dictionary mappings, contradictions, retrieval gaps, or human-confirmed four-view module context. Blocks on unapproved evidence and does not promote RAG candidates to approved rules. |
| 0n — Module Context Ready | Synthesize or validate module | `legacy-ibmi-module-analyzer` | Implemented v0.1.1 | Use when `00_context_packages/<MODULE-SLUG>/context-index.yaml` is `ready_for_module_analysis` or `ready_with_warnings`; preserve open questions as TBDs. |
| 1 — Evidence Ready (IBM i) | Start reverse engineering | `legacy-ibmi-inventory` | Implemented | First call after redaction |
| 1 — Evidence Ready (COBOL) | Start reverse engineering | `legacy-cobol-inventory` | Future | Use manual fallback; produce `inventory.yaml` following the same schema as the IBM i family |
| 2a — Inventory In Progress | Continue inventory | `legacy-ibmi-inventory` | Implemented | Keep iterating; do not exit until SME decision is recorded |
| 2b — Inventory Blocked | Any downstream | `legacy-ibmi-inventory` (resume) | Implemented | **Inventory Completeness Gate fails.** Resolve `coverage_gaps[].blocking: yes` or get explicit SME waiver |
| 2c — Inventory Done | Understand program logic | `legacy-ibmi-program-analyzer` | **Implemented v0.1.0** | Run per program; produces `program-analysis-<OBJ-ID>.md` |
| 2c — Inventory Done | Map calls / CRUD / DSPF | (subsumed) | n/a | Call graph, file I/O, object dependencies are embedded in program-analyzer + flow-analyzer + module-analyzer outputs |
| 2c — Inventory Done | Mine runtime evidence | `legacy-ibmi-runtime-evidence-miner` | Future (deferred from MVP) | Only when runtime samples are available and redacted |
| 3a — Program Analysis In Progress | Continue | `legacy-ibmi-program-analyzer` | **Implemented v0.1.0** | Complete coverage before routing to flow-analyzer |
| 3b — Program Analysis Done | Analyze a call chain | `legacy-ibmi-flow-analyzer` | **Implemented v0.1.0** | Required when business event spans multiple programs; supports 7 trigger models (batch / menu / subfile / F-key / DB trigger / scheduler / API) |
| 3c — Flow Analysis In Progress | Continue | `legacy-ibmi-flow-analyzer` | **Implemented v0.1.0** | Complete all in-scope flows before module synthesis |
| 3d — Flow Analysis Done | Synthesize the module | `legacy-ibmi-module-analyzer` | **Implemented v0.1.3** | Produces the canonical 4-view module analysis (Operation/System/Program/Data) under `04_modules/` per `docs/module-analysis-model.md` |
| 3e — Module Analysis In Progress | Continue | `legacy-ibmi-module-analyzer` | **Implemented v0.1.0** | All four views must reach `approved` or `approved_with_non_blocking_tbd` |
| 3f — Module Analysis Done, no approved BRD Package | Produce business-facing BRD for SME / business review | `legacy-brd-writer` | **Implemented v0.1.5** | One BRD Package per selected `CAP-*`; sections 1-9 are required for review, 10-12 optional/evidence-backed |
| 3f — Module Analysis Done, approved BRD Package exists | Produce capability spec | `legacy-spec-writer` | **Implemented v0.1.2** | One spec per `CAP-*` seed from `module-overview.md`; consumes approved BRD Package as the business review layer |
| 4 — Static Analysis | (optional supplemental artifacts) | n/a | Optional | Subsumed by program/flow/module analyses; no separate skill needed for MVP |
| 5 — Runtime Evidence Mined | Augment BRD/spec package | `legacy-brd-writer` or `legacy-spec-writer` (rerun after the applicable review gate) | **Implemented** | Runtime evidence miner is future, but once evidence exists the BRD/spec package can consume it to improve traceability and `evidence_strength`; keep BRD review before spec approval |
| 6 — Business Rules Drafted | (subsumed) | (BR seeds live in module View 1; spec-writer formalizes) | n/a | Stage retained for backward compatibility |
| 7 — Capabilities Mapped | (subsumed) | (CAP seeds live in module-overview; spec-writer produces one spec per CAP) | n/a | Stage retained for backward compatibility |
| 8a — Spec Drafted | Expand modernization decisions (optional) | `legacy-modernization-decision-writer` | **Implemented v0.1.0** | Optional governance skill. Use when decisions are complex, cross-cutting, or need explicit architecture approval. Produces `05_decisions/` package; reconciles back to `spec.yaml`. |
| 8a — Spec Drafted | Prepare browser-friendly SME review view | `legacy-html-exporter` | **Implemented v0.1.0** | Optional companion route only when stable human-facing Markdown already exists (`spec.md`, `traceability.md`, review/question docs). Markdown remains canonical; HTML must not replace review source. |
| 8a — Spec Drafted | Validate | `legacy-spec-reviewer` | Future (deferred from MVP) | Until implemented, use spec-writer's `spec-review.md` + SME |
| 8b — Spec In Review | Promote to approved | (SME sign-off) | Doc-only | Update `spec.yaml.status: approved` once SME signs; not a skill |
| 8b — Spec In Review | Make review docs easier for SMEs to read | `legacy-html-exporter` | **Implemented v0.1.0** | Optional review ergonomics. Use for browser-readable companions during SME walkthroughs; fix Markdown first if content is wrong. |
| 8c — Spec Approved | Generate equivalence tests | `legacy-equivalence-test-generator` | Planned | Produces golden-master test pack |
| 8c — Spec Approved | Export approved human-facing package | `legacy-html-exporter` | **Implemented v0.1.0** | Optional after approval for stakeholder browsing. Does not advance the chain and does not alter `spec.yaml.status`. |
| 9 — Equivalence Pack Ready | Hand off to forward SDLC | `docs/forward-sdlc-contract.md` then `ibm-i-program-spec` / `ibm-i-code-generator` / etc. | External | **Forward Handoff Gate first.** Cross to `wwa-lab/build-agent-skill` only after gate passes |

## Optional Detours

### Modernization Decision Expansion (After Spec Draft)

When routing from "Spec Drafted" to approval, consider whether the spec's
`modernization_decisions[]` should be expanded into a separate decision package.

**Trigger the optional `legacy-modernization-decision-writer` if**:

- Spec has 3+ `DEC-*` records
- Decisions are cross-cutting (affect multiple capabilities)
- Decisions are high-risk or require explicit architecture/product approval
- Spec review identifies unresolved platform, data, API, compatibility, or
  error-handling questions
- Decision authority (architecture owner) is separate from SME authority

**Skip `legacy-modernization-decision-writer` if**:

- Simple decisions that fit inline in `spec.yaml`
- All required SME and architecture/product approvals are already captured in
  the spec review package
- Forward SDLC handoff is not blocked by unresolved decisions

When using the decision-writer:

1. Feed it the draft `spec.yaml` + module/flow/program analyses
2. Decision-writer produces `05_decisions/<CAP-SLUG>/` package
3. Once approved, decision-writer reconciles approved `DEC-*` back to
   `spec.yaml`
4. Resume normal spec approval workflow

---

## Special Routes

### "Where am I?" requests

When the user just asks what they have without a clear outcome, run Step 1
(stage identification), report the stage, and list the 2-3 most useful next
moves with their gate requirements.

### "HTML / browser view / SME-readable export" requests

When the user asks for HTML, a browser view, a web-readable package, or easier
SME/user review:

1. Confirm the source is human-facing Markdown (`*.md`) or a directory
   containing Markdown review docs.
2. If the Markdown exists and is stable enough for review, route to
   `legacy-html-exporter`.
3. If the Markdown is missing, blocked, draft content that still needs upstream
   correction, or the request targets `spec.yaml` / JSON / YAML machine
   artifacts, route back to the producing skill or gate first.
4. If the user asks to make HTML the canonical artifact, block the request:
   Markdown remains canonical for human-facing docs, and `spec.yaml` remains
   canonical for automation.

Do not treat HTML export as a stage advancement. It is a supplemental read
view for review ergonomics.

### "Skip ahead" requests

When the user wants to jump several stages forward:

1. Identify what substance the skipped stages would have contributed
2. Check whether the current artifact already contains that substance
3. If yes, allow the jump and document the substitution
4. If no, refuse and route to the earliest unmet prerequisite

### "Multi-program slice" requests

When the slice contains multiple programs:

- Inventory must cover all of them before any program-analyzer runs
- Program-analyzer can run per-program in parallel
- Rule-miner aggregates across programs — do not invoke until at least the
  business-critical programs are analyzed

### "Already approved spec, want to regenerate" requests

When the user has an approved `spec.yaml` and wants to redo something:

- Do not retire approved rule IDs; mark them `status: retired` and create new
  IDs per `docs/id-conventions.md`
- Re-run `legacy-spec-reviewer` after any material change
- Re-run Forward Handoff Gate before re-crossing to the forward chain

## Cross-Chain Notes

- This orchestrator never invokes a forward-chain skill. It tells the user to
  cross over once the Forward Handoff Gate passes.
- The forward chain's `ibm-i-workflow-orchestrator` does not know about the
  reverse chain. Forward chain users with only existing source (no CR) should
  use this orchestrator, not theirs.
