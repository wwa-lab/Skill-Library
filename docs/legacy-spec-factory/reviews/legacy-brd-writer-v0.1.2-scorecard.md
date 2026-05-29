---
skill: legacy-brd-writer
scorecard_version: v0.1.2
static_score: 9.36
decision: repo-ready
status: superseded_by_v0.1.3
last_verified: 2026-05-22
runtimes_tested:
  codex: { status: synced, model: gpt-5.4-mini, date: 2026-05-22 }
  claude_code: { status: synced, model: haiku, date: 2026-05-22 }
  opencode: { status: synced, model: minimax-m2.5-free, date: 2026-05-22 }
evidence_source: docs/runtime-matrix.md
---

# Skill Review Scorecard: legacy-brd-writer v0.1.2

## Metadata

- **skill_name:** legacy-brd-writer
- **skill_path:** skills/legacy-brd-writer/
- **reviewed_version:** v0.1.2
- **reviewed_by:** Codex
- **review_date:** 2026-05-22
- **decision:** repo-ready

## Change Under Review

v0.1.2 extends the BRD Package from three artifacts to four by adding
`validation-scenarios.md`. It introduces BRD-stage `VAL-*` validation scenario
seeds so SMEs, BAs, QA, and SOW owners can review expected coverage before
formal `AC-*` acceptance criteria or `TC-*` golden-master cases are minted by
downstream skills.

The update keeps the original BRD boundary: the skill may draft scenario seeds
from existing `BEH-*`, `BR-*`, and `EV-*` references, but it must not invent
formal test cases, exact expected outputs, target-platform decisions, or
approved business rules.

## Runtime Smoke Tests

No v0.1.2 runtime smoke has been executed yet. Runtime adapter copies are
synced, so the skill is repo-ready but capped below field-pilot status until
positive and negative no-write scenarios pass in Codex, Claude Code, and
OpenCode.

| Runtime | Model | Result | Notes |
| --- | --- | --- | --- |
| Codex CLI | `gpt-5.4-mini` | synced | Adapter copy matches canonical skill; execution smoke pending. |
| Claude Code | `haiku` | synced | Adapter copy matches canonical skill; execution smoke pending. |
| OpenCode | `minimax-m2.5-free` | synced | Adapter copy matches canonical skill; execution smoke pending. |

## Weighted Score

| Category | Weight | Score | Weighted | Notes |
| --- | ---: | ---: | ---: | --- |
| Purpose and trigger clarity | 10% | 9.6 | 0.96 | BRD-stage scenario review is clearly positioned before spec-writing. |
| Workflow completeness | 12% | 9.4 | 1.13 | The four-artifact package and validation scenario step are executable. |
| IBM i / domain correctness | 14% | 9.3 | 1.30 | Preserves SME control and avoids raw source assumptions. |
| Evidence and anti-hallucination | 12% | 9.5 | 1.14 | `VAL-*` items must map to existing behavior/rule/evidence IDs. |
| Output contract | 10% | 9.5 | 0.95 | Adds `validation-scenarios.md` and updates traceability expectations. |
| Progressive disclosure | 8% | 9.2 | 0.74 | Main skill stays readable; detailed scenario rules live in templates. |
| Runtime portability | 10% | 9.0 | 0.90 | Synced across runtimes; execution smoke still pending. |
| Reviewability and testability | 10% | 9.2 | 0.92 | The new artifact gives SMEs a better review surface, but needs frozen examples. |
| Engineering handoff value | 8% | 9.5 | 0.76 | Cleanly feeds SME review, spec-writing, and golden-master planning. |
| Maintainability | 6% | 9.4 | 0.56 | Version history and artifact boundary are clear. |

**Final static score: 9.36 / 10**.

**Current score after runtime cap: 9.0 / 10**.

## Decision

**Repo-ready, not field-pilot ready.**

## Blocking For 9.5

| ID | Finding | Required Change | Affects |
| --- | --- | --- | --- |
| BRD-REV-001 | v0.1.2 has not passed three-runtime no-write smoke. | Run positive and negative smoke prompts in Codex, Claude Code, and OpenCode. | Runtime portability, reviewability |
| BRD-REV-002 | No frozen positive example yet demonstrates `validation-scenarios.md` with `VAL-*` mappings. | Add or update a fixture showing `VAL-* -> BEH/BR/EV` traceability. | Reviewability, output contract |

## Strengths

- Keeps BRD scenario seeds separate from formal acceptance criteria and test
  cases.
- Gives SMEs a concrete coverage surface before spec-writing.
- Preserves the rule that inferred business rules remain SME-reviewable until
  explicitly approved downstream.

## Risks

- Without runtime smoke, adapter behavior is not yet proven.
- `VAL-*` can be mistaken for formal `TC-*` if callers skip the boundary rules;
  smoke tests should include this negative case.
