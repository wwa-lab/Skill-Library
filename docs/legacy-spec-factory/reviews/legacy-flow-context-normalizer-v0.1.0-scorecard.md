---
skill: legacy-flow-context-normalizer
scorecard_version: v0.1.0
static_score: 9.34
decision: repo-ready
status: superseded
last_verified: 2026-05-27
runtimes_tested:
  codex: { status: synced, model: gpt-5.4-mini, date: 2026-05-27 }
  claude_code: { status: synced, model: haiku, date: 2026-05-27 }
  opencode: { status: synced, model: minimax-m2.5-free, date: 2026-05-27 }
evidence_source: docs/runtime-matrix.md
---

# Skill Review Scorecard: legacy-flow-context-normalizer v0.1.0

## Metadata

- skill_name: legacy-flow-context-normalizer
- skill_path: skills/legacy-flow-context-normalizer
- reviewed_version: v0.1.0
- generated_by: Codex
- reviewed_by: Codex
- review_date: 2026-05-27
- target_runtime:
  - [x] Codex
  - [x] Claude Code
  - [x] OpenCode
- decision:
  - [ ] reject
  - [ ] revise
  - [x] repo-ready
  - [ ] field-pilot ready

## Review Focus

This is a new upstream skill for the enterprise pain point where module
knowledge exists only in scattered Visio, Word, Excel, PDF, PowerPoint, RAG
summaries, screenshots, or SME notes. The skill normalizes those sources into
draft Operation / Business, System, Program, and Data flows for SME review
before `legacy-module-context-intake` and BRD work.

## Mandatory Stop Conditions

No mandatory 8.0 cap conditions found.

The runtime cap still applies because the skill has been synced but not yet run
through positive and negative no-write execution smoke in Codex, Claude Code,
and OpenCode.

## Weighted Score

| Category | Weight | Score | Weighted |
| --- | ---: | ---: | ---: |
| Purpose and trigger clarity | 10% | 9.5 | 0.95 |
| Workflow completeness | 12% | 9.4 | 1.13 |
| IBM i / domain correctness | 14% | 9.0 | 1.26 |
| Evidence and anti-hallucination | 12% | 9.6 | 1.15 |
| Output contract | 10% | 9.5 | 0.95 |
| Progressive disclosure | 8% | 9.2 | 0.74 |
| Runtime portability | 10% | 9.0 | 0.90 |
| Reviewability and testability | 10% | 9.4 | 0.94 |
| Engineering handoff value | 8% | 9.4 | 0.75 |
| Maintainability | 6% | 9.3 | 0.56 |

Final score before cap: **9.34 / 10**

Final score after cap: **9.0 / 10**

## Decision

Repo-ready, not field-pilot ready.

## Blocking For 9.5

| ID | Finding | Required Change | Affects |
| --- | --- | --- | --- |
| LFCN-REV-001 | Runtime loading and no-write execution have not been verified in all three runtimes. | Run positive and negative smoke prompts in Codex, Claude Code, and OpenCode; update runtime matrix and scorecard. | Runtime portability, reviewability |
| LFCN-REV-002 | The normalizer has only synthetic examples, not a real mixed-format field package. | Run one pilot bundle with at least two document formats and confirm SME questions are actionable. | SME correctness, handoff value |
| LFCN-REV-003 | The validator is structural and cannot verify extraction quality from binary documents. | Add optional extraction smoke fixtures or documented tool recipes for `.vsdx`, `.pptx`, `.xlsx`, and PDF when a pilot bundle is available. | Testability, maintainability |

## Strengths

- The skill fills the gap before `legacy-module-context-intake`: scattered
  documents become draft four-view flows instead of being treated as confirmed
  module context.
- Stop conditions protect sensitive evidence, unreadable proprietary files,
  hidden contradictions, and premature BRD/rule generation.
- Output separates source-document inventory, evidence map, contradictions,
  open questions, and SME review pack.
- View contracts keep business statements, technical evidence, candidate
  seeds, and unresolved gaps separated.
- The bundled validator catches required-file gaps, status vocabulary, missing
  evidence-map IDs, forbidden candidate approval, and pending sign-off on ready
  packages.

## Verification

```bash
python3 skills/legacy-flow-context-normalizer/scripts/validate_flow_context_package.py \
  skills/legacy-flow-context-normalizer/examples/minimal-positive

python3 skills/legacy-flow-context-normalizer/scripts/validate_flow_context_package.py \
  --allow-blocked \
  skills/legacy-flow-context-normalizer/examples/blocked-authorization-negative
```

Both commands returned `OK: flow context package is structurally valid`.

## Runtime Smoke Status

| Runtime | Status | Evidence |
| --- | --- | --- |
| Codex | synced | Adapter copy synced from canonical source on 2026-05-27 |
| Claude Code | synced | Adapter copy synced from canonical source on 2026-05-27 |
| OpenCode | synced | Adapter copy synced from canonical source on 2026-05-27 |

## Requested Next Revision

Run runtime smoke with:

1. A positive mixed-document prompt that supplies an authorized process deck,
   application list, and data dictionary excerpt and expects a draft
   `flow-normalization/` package.
2. A negative prompt with unknown source authorization that must route to
   `legacy-ibmi-evidence-intake` without extracting sensitive content.

Keep the canonical skill under `skills/legacy-flow-context-normalizer/`.
