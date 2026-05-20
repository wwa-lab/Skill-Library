# Skill Families

Legacy Spec Factory has 20 skills. They are not equally connected — some are
called every run, some only at boundaries, some only when reviewing. This
document groups them into **families** so callers (humans and orchestrators)
know which skills travel together, which order they fire in, and which
shared vocabulary they use.

**Authoritative status / scores**: see
[`skill-status-truth-table.md`](skill-status-truth-table.md). This document
is about **how skills relate**, not whether they are field-pilot ready.

## Family Overview

| Family | Skills | When They Fire |
| --- | ---: | --- |
| Routing | 1 | At any decision point — picks the next skill |
| Layer 1 — IBM i extraction | 8 | Once per legacy capability slice |
| Layer 2 — synthesis | 3 | After Layer 1 produces evidence |
| Bridge / handoff | 2 | After synthesis is approved |
| Governance | 5 | Cross-cutting; called by other skills |
| Verification | 1 | Before cutover / parallel-run |
| **Total** | **20** | |

---

## 1. Routing

**Purpose**: Identify the current pipeline stage, the next safest skill, and
the gates that must pass first. Never produces business artifacts.

| Skill | Role |
| --- | --- |
| [`legacy-modernization-orchestrator`](../skills/legacy-modernization-orchestrator/SKILL.md) | Stateless router; reads the user's situation and emits `(stage, next_skill, gate_status)` |

**Typical call**: every time a user asks "what should I do next?" or "is this
ready for the next step?"

**Important**: the orchestrator does NOT execute downstream skills. It tells
the user (or wrapping agent) which skill to invoke next.

---

## 2. Layer 1 — IBM i Extraction

**Purpose**: Read raw IBM i artifacts (RPGLE, CLLE, COBOL, DDS, jobs, screens,
reports) and produce structured, evidence-tagged extraction output. Every
Layer 1 skill respects the same anti-hallucination rules: code is ground
truth (tier 1), SME knowledge is tier 2/3, prior wikis are tier 4.

| Skill | Reads | Writes | Position |
| --- | --- | --- | --- |
| [`legacy-ibmi-evidence-intake`](../skills/legacy-ibmi-evidence-intake/SKILL.md) | raw evidence bundles | `evidence/manifest.yaml`, `redaction-log.md` | **First** — gates everything else |
| [`legacy-ibmi-inventory`](../skills/legacy-ibmi-inventory/SKILL.md) | approved evidence + source listings | `01_inventory/inventory.yaml`, object map | After intake |
| [`legacy-ibmi-runtime-evidence-miner`](../skills/legacy-ibmi-runtime-evidence-miner/SKILL.md) | approved job logs / spool files + inventory mappings | `runtime-evidence.jsonl`, mining checklist | After intake + inventory; parallel evidence enrichment |
| [`legacy-ibmi-program-analyzer`](../skills/legacy-ibmi-program-analyzer/SKILL.md) | one program (RPGLE/CLLE/COBOL) | `program-analysis-<OBJ-ID>.md` | Once per program in inventory |
| [`legacy-ibmi-flow-analyzer`](../skills/legacy-ibmi-flow-analyzer/SKILL.md) | multiple program-analyses for one transaction | `flow-<FLOW-SLUG>.md` | After per-program analysis is done |
| [`legacy-ibmi-module-analyzer`](../skills/legacy-ibmi-module-analyzer/SKILL.md) | related flows | `04_modules/<MODULE-SLUG>/` (4-view) | After flows for a capability are done |
| [`legacy-ibmi-data-model-analyzer`](../skills/legacy-ibmi-data-model-analyzer/SKILL.md) | DDS PF/LF + related programs | `03_data_models/<DATA-SLUG>/` | Parallel to program/flow analysis |
| [`legacy-ibmi-screen-report-analyzer`](../skills/legacy-ibmi-screen-report-analyzer/SKILL.md) | DSPF/PRTF + driving programs | `screen-report-analysis-<OBJ-ID>.md` | Parallel to program/flow analysis |

**Sequence**:

```
evidence-intake (gate)
  ├─ inventory
  │    ├─ runtime-evidence-miner (optional but recommended where logs/spool exist)
  │    ├─ program-analyzer (per program)
  │    │    └─ flow-analyzer (per transaction flow)
  │    │         └─ module-analyzer (per capability module)
  │    ├─ data-model-analyzer (per data subject)
  │    └─ screen-report-analyzer (per UI/report surface)
```

**Shared vocabulary**: `OBJ-*`, `EV-*`, `TBD-*` IDs; `observed/inferred/unknown`
classification; sensitivity tagging; SME review gate.

**Anti-pattern**: skipping intake to "save time" — every downstream skill
will refuse to start without the evidence manifest.

---

## 3. Layer 2 — Synthesis

**Purpose**: Take Layer 1 extracted output (no raw source code) and synthesize
business-facing artifacts. Layer 2 is platform-agnostic — adding a new
legacy platform (e.g., COBOL/JCL) means adding a new Layer 1 family but
reusing Layer 2.

| Skill | Reads | Writes | When |
| --- | --- | --- | --- |
| [`legacy-brd-writer`](../skills/legacy-brd-writer/SKILL.md) | approved module-analysis | `05_brds/<CAPABILITY-SLUG>/brd.md`, `brd-review.md`, `traceability.md` | After module-analyzer is approved |
| [`legacy-spec-writer`](../skills/legacy-spec-writer/SKILL.md) | approved BRD + module-analysis | `spec.yaml`, `spec.md` | After BRD is SME-approved |
| [`legacy-modernization-decision-writer`](../skills/legacy-modernization-decision-writer/SKILL.md) | spec.yaml entries needing expansion | `05_decisions/<CAPABILITY-SLUG>/` | Optional — when a `DEC-*` becomes large or architecture-governed |

**Sequence**:

```
module-analyzer (approved)
  └─ brd-writer
       └─ SME review (use sme-review-facilitator)
            └─ spec-writer
                 └─ decision-writer (optional, per cross-cutting DEC)
```

**Shared vocabulary**: `BR-*`, `BEH-*`, `DEC-*`, `AC-*`; `needs_sme_review`
status; `observed_behavior` vs `inferred_business_rule` vs
`modernization_decision` separation.

**Anti-pattern**: writing `BR-*` rules in inventory/program-analysis output —
those are extraction artifacts, not synthesis. `BR-*` IDs are minted by
`brd-writer`.

---

## 4. Bridge / Handoff

**Purpose**: Move from this repo's reverse pipeline to the forward Atlas
delivery chain. Validates approval gates and packages structured handoff
inputs.

| Skill | Reads | Writes | Sends To |
| --- | --- | --- | --- |
| [`legacy-traceability-packager`](../skills/legacy-traceability-packager/SKILL.md) | spec.yaml + BRD + module + tests | `06_traceability_packages/` | Audit / review |
| [`legacy-brd-to-sdd-handoff`](../skills/legacy-brd-to-sdd-handoff/SKILL.md) | approved spec + traceability package | `06_sdd_handoffs/<CAPABILITY-SLUG>/` (5-file bundle) | Atlas SDD chain |

**Sequence**:

```
spec-writer (approved)
  └─ traceability-packager
       └─ brd-to-sdd-handoff
            → Atlas Engineering Delivery Hub (external)
```

**Anti-pattern**: handing off a spec without traceability or without a named
SME sign-off — Atlas downstream skills will not consume it.

---

## 5. Governance

**Purpose**: Cross-cutting quality and process skills. Called by other skills
or by reviewers, not by end users directly.

| Skill | Role | Used By |
| --- | --- | --- |
| [`legacy-step-contract`](../skills/legacy-step-contract/SKILL.md) | Defines the INPUT → EXECUTION → OUTPUT → VALIDATION shape every step must follow | Skill authors; reviewers |
| [`legacy-step-validator`](../skills/legacy-step-validator/SKILL.md) | Applies the contract to a completed step package; emits `pass` / `pass_with_warnings` / `blocked` report | Orchestrator before advancing |
| [`legacy-sme-review-facilitator`](../skills/legacy-sme-review-facilitator/SKILL.md) | Prepares SME review packages, records decision logs, captures sign-off, routes follow-up findings | Between BRD/spec writing and approval |
| [`legacy-runtime-matrix-tester`](../skills/legacy-runtime-matrix-tester/SKILL.md) | Orchestrates runtime smoke evidence + matrix + scorecard decisions across Codex / Claude Code / OpenCode | When new skill is added or version-bumped |
| [`legacy-html-exporter`](../skills/legacy-html-exporter/SKILL.md) | Exports stakeholder-facing Markdown artifacts into standalone HTML companions for easier SME / user review | After BRD/spec/review/status docs already exist and need browser-friendly packaging |

**Pairings (use together, but kept separate intentionally)**:

- `step-contract` ↔ `step-validator`: contract-time vs validation-time. The
  validator imports the contract definition. They share `06_quality/`
  output paths and `BLOCKING / WARNING / OK` finding taxonomy.
- `sme-review-facilitator` is upstream of any Layer 2 / Bridge skill that
  requires `sme_sign_offs[]`. It is not part of the synthesis itself; it
  prepares humans for it.
- `runtime-matrix-tester` is independent of the BRD/spec pipeline but
  required for skill release readiness.
- `html-exporter` is independent of the evidence/spec gate chain. It improves
  review ergonomics only and must not be treated as a source-of-truth writer.

**Why these aren't merged**: see "Why we kept them as separate skills"
section below.

---

## 6. Verification

**Purpose**: Generate old-vs-new comparison evidence so cutover risk is
explicit before parallel-run.

| Skill | Reads | Writes |
| --- | --- | --- |
| [`legacy-golden-master-test-planner`](../skills/legacy-golden-master-test-planner/SKILL.md) | approved spec + BRD + observed behavior evidence | `06_quality/<CAPABILITY-SLUG>/` (5-file plan with `TC-*`) |

**When**: after `spec-writer` is approved, before Atlas builds the new
implementation. The test plan becomes the equivalence-test contract.

**Planned future skills** (not yet implemented, see README skill roadmap):

- `legacy-equivalence-test-generator` — generate executable tests from the
  test plan

---

## End-to-End Sequence

A canonical "first slice" run, in order:

```
1.  orchestrator                   → "stage: scope; next: evidence-intake"
2.  evidence-intake (gate)         → evidence/manifest.yaml approved
3.  inventory                      → 01_inventory/ approved by SME
4.  runtime-evidence-miner         → 07_runtime-evidence/runtime-evidence.jsonl (optional where logs/spool exist)
5.  program-analyzer × N           → program-analysis-*.md per OBJ-*
6.  flow-analyzer × M              → flow-*.md per FLOW-*
7.  data-model-analyzer × K        → 03_data_models/ per DATA-*
8.  screen-report-analyzer × J     → screen-report-analysis-*.md per OBJ-*
9.  module-analyzer × P            → 04_modules/<MODULE-SLUG>/ per MODULE-*
10. brd-writer                     → 05_brds/<CAPABILITY-SLUG>/
11. sme-review-facilitator         → 07_sme_reviews/<CAPABILITY-SLUG>/
12. spec-writer                    → 05_specs/<CAPABILITY-SLUG>/
13. decision-writer (optional)     → 05_decisions/<CAPABILITY-SLUG>/ (per DEC)
14. golden-master-test-planner     → 06_quality/<CAPABILITY-SLUG>/
15. traceability-packager          → 06_traceability_packages/
16. brd-to-sdd-handoff             → 06_sdd_handoffs/<CAPABILITY-SLUG>/
                                     → Atlas (external)
```

Governance skills (`step-contract`, `step-validator`, `runtime-matrix-tester`,
and `legacy-html-exporter`) are called as needed by the orchestrator, skill
authors, or human reviewers, not in this linear sequence.

---

## Why We Kept Some Skills Separate (Not Merged)

These four pairs looked like merge candidates but were intentionally kept
separate. Recording the reasons here so future "let's reduce skill count"
proposals can revisit with full context.

### `step-contract` + `step-validator` — kept separate

- Different triggers: contract = author-time (designing a new step).
  Validator = run-time (reviewing a completed step).
- Different outputs: contract block vs validation report.
- Different callers: skill author vs orchestrator.
- Merging produces an 800+ line SKILL.md that violates progressive disclosure
  and forces the LLM to choose a mode every call.
- Both are already field-pilot ready; merging would force re-running smoke
  tests and rewriting scorecards for net-zero functional gain.

### `data-model-analyzer` + `screen-report-analyzer` — kept separate

- Different surfaces: data structure (PF/LF) vs UI/report (DSPF/PRTF).
- Different IBM i sub-skills: SQL/access-path reasoning vs subfile/F-key
  reasoning.
- Mixing both contexts in one prompt makes the LLM choose a surface every
  call and reduces output specificity.

### `brd-writer` + `brd-to-sdd-handoff` — kept separate

- An SME approval gate sits between them. Merging implies a continuous
  flow and risks the LLM skipping SME review.
- BRD is the business artifact; handoff is the contract bundle. Different
  consumers (SME vs Atlas).

### `spec-writer` + `decision-writer` + `traceability-packager` — kept separate

- Decision-writer is **optional** (only for cross-cutting `DEC-*`).
  Merging into spec-writer makes every spec call think it must produce a
  decision package.
- Traceability-packager's real client is audit/review, not spec writing.
  Bundling them gives wrong dependency.
- spec-writer is currently `repo-ready` (9.24); the other two are
  `field-pilot ready` (9.56 / 9.51). Merging would drag the bundle to
  spec-writer's maturity.

---

## Verification

`scripts/verify-skill-claims.py` checks that every skill listed in
[`skill-status-truth-table.md`](skill-status-truth-table.md) appears in this
document under exactly one family.

Run:

```bash
python3 scripts/verify-skill-claims.py
```
