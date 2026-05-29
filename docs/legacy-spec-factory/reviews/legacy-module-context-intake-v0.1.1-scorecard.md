---
skill: legacy-module-context-intake
scorecard_version: v0.1.1
static_score: 9.42
decision: repo-ready
status: superseded
last_verified: 2026-05-26
runtimes_tested:
  codex: { status: synced, model: gpt-5.4-mini, date: 2026-05-26 }
  claude_code: { status: synced, model: haiku, date: 2026-05-26 }
  opencode: { status: synced, model: minimax-m2.5-free, date: 2026-05-26 }
evidence_source: docs/runtime-matrix.md
---

# Skill Review Scorecard: legacy-module-context-intake v0.1.1

## Metadata

- skill_name: legacy-module-context-intake
- skill_path: skills/legacy-module-context-intake
- reviewed_version: v0.1.1
- generated_by: Codex
- reviewed_by: Codex
- review_date: 2026-05-26
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

v0.1.1 hardens module-first RAG intake against the same pattern found in BRD
generation: candidate statements could be anchored on program names, file
names, or RAG snippet IDs before the downstream module / BRD writers ever saw
them. The revision adds `Business Signal` and `Evidence Basis` columns to
candidate seed and candidate fact tables, updates examples, and repairs the
local validator's `approved` candidate detection.

## Mandatory Stop Conditions

No mandatory 8.0 cap conditions found.

The runtime cap still applies because the skill has been synced but not yet run
through positive and negative no-write execution smoke in Codex, Claude Code,
and OpenCode.

## Weighted Score

| Category | Weight | Score | Weighted |
| --- | ---: | ---: | ---: |
| Purpose and trigger clarity | 10% | 9.5 | 0.95 |
| Workflow completeness | 12% | 9.5 | 1.14 |
| IBM i / domain correctness | 14% | 9.2 | 1.29 |
| Evidence and anti-hallucination | 12% | 9.7 | 1.16 |
| Output contract | 10% | 9.6 | 0.96 |
| Progressive disclosure | 8% | 9.4 | 0.75 |
| Runtime portability | 10% | 9.1 | 0.91 |
| Reviewability and testability | 10% | 9.6 | 0.96 |
| Engineering handoff value | 8% | 9.5 | 0.76 |
| Maintainability | 6% | 9.4 | 0.56 |

Final score before cap: **9.42 / 10**

Final score after cap: **9.0 / 10**

## Decision

Repo-ready, not field-pilot ready.

## Blocking For 9.5

| ID | Finding | Required Change | Affects |
| --- | --- | --- | --- |
| MCI-REV-001 | Runtime loading and no-write execution have not been verified in Codex, Claude Code, and OpenCode for v0.1.1. | Run positive and negative smoke prompts in all three runtimes, update `docs/runtime-matrix.md`, and refresh this scorecard. | Runtime portability, reviewability |
| MCI-REV-002 | The hardening has been validated against frozen synthetic examples, not a field RAG/context package. | Run one real or pilot module-first package and confirm candidate statements stay business-signal first. | Field readiness |

## Strengths

- Candidate seed and candidate fact contracts now separate the business-facing
  signal from technical evidence.
- View 3 remains allowed to carry program-analysis focus, but must describe the
  business decision that depends on the technical check.
- Positive and blocked examples were updated to avoid program-name-first
  candidate statements while preserving traceable evidence.
- The stdlib validator now detects forbidden `approved` RAG candidate facts
  even after table shape changes.
- Existing authorization, contradiction visibility, and no-`BR-*` promotion
  boundaries remain intact.

## Verification

```bash
python3 skills/legacy-module-context-intake/scripts/validate_context_package.py \
  skills/legacy-module-context-intake/examples/credit-check-rag-positive

python3 skills/legacy-module-context-intake/scripts/validate_context_package.py \
  --allow-blocked \
  skills/legacy-module-context-intake/examples/blocked-contradiction-negative
```

Both commands returned `OK: module context package is structurally valid`.

Runtime adapter sync and cross-document claim verification are recorded in the
top-level runtime matrix and truth table.

## Requested Revision Prompt

```text
Revise legacy-module-context-intake to move from repo-ready to field-pilot
ready.

Target score: 9.5/10.

Required changes:
- Run positive and negative no-write runtime smoke tests in Codex, Claude Code,
  and OpenCode.
- Confirm the positive prompt returns the eight required
  00_context_packages/<MODULE-SLUG>/ files and routes to
  legacy-ibmi-module-analyzer.
- Confirm candidate seeds and candidate facts include Business Signal and
  Evidence Basis, with program/file/field names kept in evidence context.
- Confirm the negative prompt blocks unauthorized/unredacted source evidence
  and routes to legacy-ibmi-evidence-intake.
- Update docs/runtime-matrix.md and this scorecard with runtime evidence.

Do not remove author/copyright notices.
Keep the canonical skill under skills/legacy-module-context-intake/.
```
