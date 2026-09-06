---
skill: legacy-module-context-intake
scorecard_version: v0.1.0
static_score: 9.33
decision: repo-ready
status: superseded_by_v0.1.1
last_verified: 2026-05-21
runtimes_tested:
  codex: { status: synced, model: gpt-5.4-mini, date: 2026-05-21 }
  claude_code: { status: synced, model: haiku, date: 2026-05-21 }
  opencode: { status: synced, model: minimax-m2.5-free, date: 2026-05-21 }
evidence_source: docs/runtime-matrix.md
---

# Skill Review Scorecard: legacy-module-context-intake v0.1.0

## Metadata

- skill_name: legacy-module-context-intake
- skill_path: skills/legacy-module-context-intake
- reviewed_version: v0.1.0
- generated_by: Codex
- reviewed_by: Codex
- review_date: 2026-05-21
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

The runtime cap applies because the skill has been created and synced but not
yet executed in Codex, Claude Code, and OpenCode smoke scenarios.

## Weighted Score

| Category | Weight | Score | Weighted |
| --- | ---: | ---: | ---: |
| Purpose and trigger clarity | 10% | 9.5 | 0.95 |
| Workflow completeness | 12% | 9.4 | 1.13 |
| IBM i / domain correctness | 14% | 9.1 | 1.27 |
| Evidence and anti-hallucination | 12% | 9.5 | 1.14 |
| Output contract | 10% | 9.4 | 0.94 |
| Progressive disclosure | 8% | 9.3 | 0.74 |
| Runtime portability | 10% | 9.1 | 0.91 |
| Reviewability and testability | 10% | 9.4 | 0.94 |
| Engineering handoff value | 8% | 9.3 | 0.74 |
| Maintainability | 6% | 9.3 | 0.56 |

Final score before cap: **9.33 / 10**

Final score after cap: **9.0 / 10**

## Decision

Repo-ready, not field-pilot ready.

## Blocking For 9.5

| ID | Finding | Required Change | Affects |
| --- | --- | --- | --- |
| MCI-REV-001 | Runtime loading and no-write execution have not been verified in Codex, Claude Code, and OpenCode. | Run positive and negative smoke prompts in all three runtimes, update `docs/runtime-matrix.md`, and refresh this scorecard. | Runtime portability, reviewability |

## Strengths

- Clear trigger: module-first RAG or code-knowledge-graph output that must be
  normalized before module analysis.
- Strong boundary: blocks raw or unauthorized source evidence, and explicitly
  refuses to promote RAG candidates into approved `BR-*`.
- Concrete output contract for `00_context_packages/<MODULE-SLUG>/`, including
  provenance, contradiction visibility, and open-question carry-forward.
- Frozen positive example package covers the synthetic CREDIT-CHECK RAG bundle
  and demonstrates all eight required files.
- Bundled stdlib validator checks required files, status vocabulary,
  view-to-evidence-map linkage, contradiction completeness, and candidate
  promotion status without external dependencies.
- Good progressive disclosure: the main skill stays procedural while
  field-level details live in `references/output-contract.md`.
- Portable canonical layout under `skills/` with no runtime-specific
  assumptions.

## Improvement Notes

- Runtime smoke remains the main blocker for 9.5+.
- Future hardening can add a negative fixture package if field pilots reveal
  repeated blocked-package review patterns.

## Runtime Smoke Tests

Runtime copies were synced on 2026-05-21. Positive and negative execution
smoke tests are pending.

| Runtime | Model | Result | Notes |
| --- | --- | --- | --- |
| Codex CLI | `gpt-5.4-mini` | synced | Adapter copy exists after `scripts/sync-skills.sh`; execution pending. |
| Claude Code | `haiku` | synced | Adapter copy exists after `scripts/sync-skills.sh`; execution pending. |
| OpenCode | `minimax-m2.5-free` | synced | Adapter copy exists after `scripts/sync-skills.sh`; execution pending. |

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
- Confirm the negative prompt blocks unauthorized/unredacted source evidence
  and routes to legacy-ibmi-evidence-intake.
- Update docs/runtime-matrix.md and this scorecard with runtime evidence.

Do not remove author/copyright notices.
Keep the canonical skill under skills/legacy-module-context-intake/.
```
