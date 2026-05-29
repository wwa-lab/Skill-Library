---
skill: legacy-brd-writer
scorecard_version: v0.1.3
static_score: 9.42
decision: repo-ready
status: current
last_verified: 2026-05-26
runtimes_tested:
  codex: { status: synced, model: not_run, date: 2026-05-26 }
  claude_code: { status: synced, model: not_run, date: 2026-05-26 }
  opencode: { status: synced, model: not_run, date: 2026-05-26 }
evidence_source: local static review + scripts/sync-skills.sh
---

# Skill Review Scorecard: legacy-brd-writer v0.1.3

## Metadata

- **skill_name:** legacy-brd-writer
- **skill_path:** skills/legacy-brd-writer/
- **reviewed_version:** v0.1.3
- **reviewed_by:** Codex
- **review_date:** 2026-05-26
- **decision:** repo-ready

## Change Under Review

v0.1.3 hardens BRD generation so the main artifact is business-readable rather
than a technical runtime walkthrough. It adds an explicit business-first
translation gate, an `As-Is Business Process Summary` section, anti-pattern
guidance against direct program chains, SME review checks for business
readability, and updated positive/negative examples.

The change preserves the existing evidence discipline: program, file, library,
and object names remain available as traceability anchors, but they no longer
drive the main BRD narrative.

## Runtime Smoke Tests

No runtime generation smoke has been executed yet for v0.1.3. Runtime adapter
copies were regenerated from the canonical source with `scripts/sync-skills.sh`.

| Runtime | Model | Result | Notes |
| --- | --- | --- | --- |
| Codex CLI | not_run | synced | Adapter copy matches canonical source; generation smoke pending. |
| Claude Code | not_run | synced | Adapter copy matches canonical source; generation smoke pending. |
| OpenCode | not_run | synced | Adapter copy matches canonical source; generation smoke pending. |

## Weighted Score

| Category | Weight | Score | Weighted | Notes |
| --- | ---: | ---: | ---: | --- |
| Purpose and trigger clarity | 10% | 9.7 | 0.97 | Stronger distinction between business BRD and technical analysis. |
| Workflow completeness | 12% | 9.5 | 1.14 | Adds a concrete translation step before BEH / BR drafting. |
| IBM i / domain correctness | 14% | 9.4 | 1.32 | Preserves technical evidence while moving implementation detail out of the main narrative. |
| Evidence and anti-hallucination | 12% | 9.5 | 1.14 | New anti-pattern blocks runtime-chain overuse without inviting invented business meaning. |
| Output contract | 10% | 9.6 | 0.96 | Template now exposes a business process summary and evidence boundary. |
| Progressive disclosure | 8% | 9.3 | 0.74 | Detailed guidance lives in references; template remains usable. |
| Runtime portability | 10% | 9.0 | 0.90 | Synced across adapters; generation smoke remains pending. |
| Reviewability and testability | 10% | 9.4 | 0.94 | SME checklist now tests business readability directly. |
| Engineering handoff value | 8% | 9.5 | 0.76 | Cleaner BRD should improve downstream spec-writing context. |
| Maintainability | 6% | 9.3 | 0.56 | Examples, template, references, and version history were updated together. |

**Final static score: 9.42 / 10**.

**Current score after runtime cap: 9.0 / 10**.

## Decision

**Repo-ready, not field-pilot ready.**

## Blocking For 9.5

| ID | Finding | Required Change | Affects |
| --- | --- | --- | --- |
| BRD-REV-003 | v0.1.3 has not passed runtime generation smoke in Codex, Claude Code, and OpenCode. | Run one positive prompt and one negative prompt that includes a raw program chain; confirm generated BRD uses business process language and demotes unresolved business meaning to `TBD-*`. | Runtime portability, reviewability |
| BRD-REV-004 | No field BRD sample has been regenerated with the new `As-Is Business Process Summary` gate. | Regenerate or manually review one real/pilot BRD, such as Card Replacement, against the new business-readability checklist. | Field readiness |

## Strengths

- Directly addresses the failure mode where a BRD becomes a program-call-chain
  summary.
- Gives SMEs an explicit review question for business readability.
- Keeps technical evidence traceable without letting it dominate the business
  artifact.

## Risks

- Models may still overuse program names in `BEH-*` statements if upstream
  evidence is too technical; runtime smoke should check this.
- If business meaning is genuinely absent from evidence, the output will contain
  more `TBD-*` items. That is expected and preferable to false business prose.
