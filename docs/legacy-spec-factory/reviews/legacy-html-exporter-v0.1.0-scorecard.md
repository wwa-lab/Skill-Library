---
skill: legacy-html-exporter
scorecard_version: v0.1.0
static_score: 9.31
decision: repo-ready
status: current
last_verified: 2026-05-19
runtimes_tested:
  codex: { status: passed, model: gpt-5.4-mini, date: 2026-05-19 }
  claude_code: { status: failed, model: haiku, date: 2026-05-19 }
  opencode: { status: passed, model: minimax-m2.5-free, date: 2026-05-19 }
evidence_source: docs/runtime-matrix.md
---

# Skill Review Scorecard: legacy-html-exporter v0.1.0

## Metadata

- skill_name: legacy-html-exporter
- skill_path: skills/legacy-html-exporter
- reviewed_version: v0.1.0
- generated_by: Codex
- reviewed_by: Codex
- review_date: 2026-05-19
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

9.0 cap still applies because runtime smoke produced mixed results: Codex and
OpenCode passed, but Claude Code violated a hard guardrail in the negative
scenario.

## Weighted Score

| Category | Weight | Score | Weighted |
| --- | ---: | ---: | ---: |
| Purpose and trigger clarity | 10% | 9.5 | 0.95 |
| Workflow completeness | 12% | 9.2 | 1.10 |
| IBM i / domain correctness | 14% | 8.8 | 1.23 |
| Evidence and anti-hallucination | 12% | 9.4 | 1.13 |
| Output contract | 10% | 9.5 | 0.95 |
| Progressive disclosure | 8% | 9.4 | 0.75 |
| Runtime portability | 10% | 9.1 | 0.91 |
| Reviewability and testability | 10% | 9.3 | 0.93 |
| Engineering handoff value | 8% | 9.0 | 0.72 |
| Maintainability | 6% | 9.0 | 0.54 |

Final score before cap: **9.31 / 10**

Final score after cap: **9.0 / 10**

## Decision

Repo-ready, not field-pilot ready.

## Blocking For 9.5

| ID | Finding | Required Change | Affects |
| --- | --- | --- | --- |
| HTML-REV-001 | Claude Code negative smoke ignored the non-negotiable rule that Markdown remains canonical and proposed `.html` as the new source of truth. | Tighten the skill prompt / guardrail wording until Claude Code blocks this request and preserves the original `.md` path as canonical. | Runtime portability, governance |

## Strengths

- Clear scope: HTML companion export only, with Markdown explicitly preserved
  as the canonical source.
- Good supplemental-skill boundaries: it does not redefine BRD/spec/review
  contracts or invent business content.
- Deterministic implementation: the renderer uses a repository-owned script
  with no external runtime dependency.
- Portable structure: canonical skill under `skills/`, synced adapters, and a
  root convenience wrapper all align with repository rules.
- The script already covers the Markdown structures common in this repo:
  headings, tables, links, lists, checklists, blockquotes, and code blocks.
- Codex CLI passed both the positive and negative smoke scenarios after the
  frontmatter description was quoted to satisfy strict YAML parsing.

## Improvement Notes

- Claude Code still needs stronger behavioral adherence to the guardrail that
  HTML cannot replace Markdown as the source of truth.
- Consider a small worked example package under the skill folder if future
  reviewers need frozen HTML expectations in addition to unit tests.

## Runtime Smoke Tests

Executed on 2026-05-19 against the synced canonical adapters.

| Runtime | Model | Result | Notes |
| --- | --- | --- | --- |
| Codex CLI | `gpt-5.4-mini` | passed | Positive scenario returned `STATUS.md` → `STATUS.html` and kept Markdown canonical. Negative scenario blocked HTML-as-source-of-truth and kept the `.md` path canonical. |
| Claude Code | `haiku` | failed | Positive scenario returned the correct paths but added extra explanatory structure beyond the requested shape. Negative scenario failed the hard guardrail and proposed `.html` as canonical. |
| OpenCode | `minimax-m2.5-free` | passed | After adding the deterministic contract helper, OpenCode invoked `legacy-html-exporter`, read `export_contract_helper.py`, and returned the exact three-line positive contract answer for `STATUS.md` → `STATUS.html` while keeping Markdown canonical. |

## Requested Revision Prompt For Claude Code

```text
Revise legacy-html-exporter to move from 9.0 to 9.5.

Target score: 9.5/10.

Blocking issues:
1. Runtime loading has not been verified in Codex, Claude Code, and OpenCode.

Required changes:
- Run positive and negative runtime smoke tests in Codex, Claude Code, and OpenCode.
- Update docs/runtime-matrix.md with the tested status and notes.
- Refresh the scorecard once runtime evidence is recorded.

Do not remove author/copyright notices.
Keep the canonical skill under skills/legacy-html-exporter/.
Maintain compatibility with Codex, Claude Code, and OpenCode.
```
