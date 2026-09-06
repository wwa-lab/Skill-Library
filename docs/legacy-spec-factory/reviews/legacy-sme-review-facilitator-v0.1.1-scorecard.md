---
skill: legacy-sme-review-facilitator
scorecard_version: v0.1.1
static_score: 9.39
decision: repo-ready
status: superseded_by_v0.1.2
last_verified: 2026-05-22
runtimes_tested:
  codex: { status: synced, model: gpt-5.4-mini, date: 2026-05-22 }
  claude_code: { status: synced, model: haiku, date: 2026-05-22 }
  opencode: { status: synced, model: minimax-m2.5-free, date: 2026-05-22 }
evidence_source: docs/runtime-matrix.md
---

# Skill Review Scorecard: legacy-sme-review-facilitator v0.1.1

## Metadata

- **skill_name:** legacy-sme-review-facilitator
- **skill_path:** skills/legacy-sme-review-facilitator/
- **reviewed_version:** v0.1.1
- **reviewed_by:** Codex
- **review_date:** 2026-05-22
- **decision:** repo-ready

## Change Under Review

v0.1.1 makes Conversation Review Mode the default SME interaction model. The
SME can answer guided batches directly in chat, while the facilitator records
the audit trail in `07_sme_reviews/<CAPABILITY-SLUG>/` and writes BRD Package
review decisions back to `05_brds/<CAPABILITY-SLUG>/review-decision.yaml`.

The update also adds explicit `VAL-*` review handling, `raw_chat_answer`
capture, `ai_suggested_decision` prefill boundaries, and optional email /
checklist exports for non-chat workflows.

## Runtime Smoke Tests

No v0.1.1 runtime smoke has been executed yet. Runtime adapter copies are
synced, so the skill is repo-ready but capped below field-pilot status until
positive and negative chat-review scenarios pass in Codex, Claude Code, and
OpenCode.

| Runtime | Model | Result | Notes |
| --- | --- | --- | --- |
| Codex CLI | `gpt-5.4-mini` | synced | Adapter copy matches canonical skill; execution smoke pending. |
| Claude Code | `haiku` | synced | Adapter copy matches canonical skill; execution smoke pending. |
| OpenCode | `minimax-m2.5-free` | synced | Adapter copy matches canonical skill; execution smoke pending. |

## Weighted Score

| Category | Weight | Score | Weighted | Notes |
| --- | ---: | ---: | ---: | --- |
| Purpose and trigger clarity | 10% | 9.6 | 0.96 | Chat-first review trigger is clear and aligned with module-first BRD work. |
| Workflow completeness | 12% | 9.5 | 1.14 | Batch questions, SME answer parsing, and write-back are specified. |
| IBM i / domain correctness | 14% | 9.4 | 1.32 | Preserves SME authority over inferred legacy behavior and contradictions. |
| Evidence and anti-hallucination | 12% | 9.6 | 1.15 | AI suggestions cannot become SME decisions without explicit answers. |
| Output contract | 10% | 9.5 | 0.95 | Adds BRD review write-back while retaining decision logs and sign-off. |
| Progressive disclosure | 8% | 9.2 | 0.74 | Email/checklist exports are optional instead of cluttering the default path. |
| Runtime portability | 10% | 9.0 | 0.90 | Synced across runtimes; execution smoke still pending. |
| Reviewability and testability | 10% | 9.3 | 0.93 | Strong review surface; needs frozen chat transcript examples. |
| Engineering handoff value | 8% | 9.4 | 0.75 | Produces machine-readable review decisions for BRD/spec/handoff consumers. |
| Maintainability | 6% | 9.2 | 0.55 | Templates and references are aligned, but new mode needs smoke fixtures. |

**Final static score: 9.39 / 10**.

**Current score after runtime cap: 9.0 / 10**.

## Decision

**Repo-ready, not field-pilot ready.**

## Blocking For 9.5

| ID | Finding | Required Change | Affects |
| --- | --- | --- | --- |
| SME-REV-001 | Conversation Review Mode has not passed three-runtime no-write smoke. | Run positive and negative chat-review scenarios in Codex, Claude Code, and OpenCode. | Runtime portability, reviewability |
| SME-REV-002 | No frozen chat transcript example yet proves terse answer parsing and BRD Package write-back. | Add a positive example with `BR-*`, `TBD-*`, and `VAL-*` chat answers plus `review-decision.yaml`. | Output contract, testability |
| SME-REV-003 | Negative smoke must verify AI suggestions cannot be promoted to SME decisions without explicit SME answers. | Add a blocked / refusal scenario for missing SME decision. | Anti-hallucination, governance |

## Strengths

- Matches the desired user experience: one chat can carry the SME review loop.
- Keeps chat as the interaction surface while files remain the audit record.
- Preserves the boundary between `ai_suggested_decision` and `sme_decision`.

## Risks

- Without smoke fixtures, terse chat parsing may drift across runtimes.
- Review write-back must stay conservative so `VAL-*` seeds do not become
  formal `TC-*` test cases prematurely.
