---
skill: legacy-ibmi-inventory
scorecard_version: v0.1.0
static_score: 9.35
decision: repo-ready
status: current
last_verified: not-yet-tested
runtimes_tested:
  codex: { status: synced, model: gpt-5.4-mini, date: null }
  claude_code: { status: synced, model: haiku, date: null }
  opencode: { status: synced, model: minimax-m2.5-free, date: null }
evidence_source: docs/runtime-matrix.md
---

# Skill Review Scorecard: legacy-ibmi-inventory v0.1.0

## Metadata

- skill_name: legacy-ibmi-inventory
- skill_path: skills/legacy-ibmi-inventory
- reviewed_version: v0.1.0
- generated_by: Codex
- reviewed_by: Codex
- review_date: 2026-05-13
- target_runtime:
  - [x] Codex
  - [x] Claude Code
  - [x] OpenCode
- decision:
  - [ ] reject
  - [ ] revise
  - [x] repo-ready
  - [ ] field-pilot ready

## Mandatory Stop Conditions

No mandatory 8.0 cap conditions found.

9.0 cap still applies because runtime copies are synced, but loading/execution
has not yet been verified in all target runtimes.

## Weighted Score

| Category | Weight | Score | Weighted |
| --- | ---: | ---: | ---: |
| Purpose and trigger clarity | 10% | 9.4 | 0.94 |
| Workflow completeness | 12% | 9.4 | 1.13 |
| IBM i / domain correctness | 14% | 9.3 | 1.30 |
| Evidence and anti-hallucination | 12% | 9.5 | 1.14 |
| Output contract | 10% | 9.4 | 0.94 |
| Progressive disclosure | 8% | 9.4 | 0.75 |
| Runtime portability | 10% | 9.1 | 0.91 |
| Reviewability and testability | 10% | 9.4 | 0.94 |
| Engineering handoff value | 8% | 9.4 | 0.75 |
| Maintainability | 6% | 9.2 | 0.55 |

Final score before cap: **9.35 / 10**

Final score after cap: **9.0 / 10**

## Decision

Repo-ready, not field-pilot ready.

## Blocking For 9.5

| ID | Finding | Required Change | Affects |
| --- | --- | --- | --- |
| INV-REV-001 | Runtime copies have been synced but not loaded or executed in Codex, Claude Code, and OpenCode | Verify loading/execution in target runtimes and update `docs/runtime-matrix.md` | Runtime portability |

## Strengths

- Clear non-goal: inventory only, no rule mining or Java generation.
- Evidence and redaction gates are explicit.
- SME review is part of the workflow, not a final afterthought.
- Output contract is structured and linked to ID/taxonomy docs.
- Runtime portability has a canonical/adapters strategy and sync script.
- Positive and negative examples cover normal inventory and missing-artifact
  gate behavior.

## Requested Revision Prompt For Claude Code

```text
Revise legacy-ibmi-inventory to move from 9.0 to 9.5.

Target score: 9.5/10.

Blocking issues:
1. Runtime loading has not been verified in Codex, Claude Code, and OpenCode.

Required changes:
- Load or execute the synced skill in Codex, Claude Code, and OpenCode.
- Update docs/runtime-matrix.md with the tested status and notes.

Do not remove author/copyright notices.
Keep the canonical skill under skills/legacy-ibmi-inventory/.
Maintain compatibility with Codex, Claude Code, and OpenCode.
```
