---
skill: legacy-brd-writer
scorecard_version: v0.1.1
static_score: 9.56
decision: field-pilot ready
status: superseded
superseded_by: docs/reviews/legacy-brd-writer-v0.1.2-scorecard.md
last_verified: 2026-05-16
runtimes_tested:
  codex: { status: passed, model: gpt-5.4-mini, date: 2026-05-16 }
  claude_code: { status: passed, model: haiku, date: 2026-05-16 }
  opencode: { status: passed, model: minimax-m2.5-free, date: 2026-05-16 }
evidence_source: docs/runtime-matrix.md
---

# Skill Review Scorecard: legacy-brd-writer v0.1.1

## Metadata

- **skill_name:** legacy-brd-writer
- **skill_path:** skills/legacy-brd-writer/
- **reviewed_version:** v0.1.1
- **reviewed_by:** Codex
- **review_date:** 2026-05-16
- **decision:** field-pilot ready

## Runtime Smoke Tests

Executed in disposable synced workspace:

`/private/tmp/legacy-brd-smoke.3Q1ThB`

This avoided overwriting dirty adapter directories in the main worktree while
still validating generated `.codex`, `.claude`, `.opencode`, and `.agents`
copies from canonical `skills/`.

Pre-test sync check:

- `scripts/sync-skills.sh --target all --check`: pass

Runtime results:

| Runtime | Model | Result | Notes |
| --- | --- | --- | --- |
| Codex CLI | `gpt-5.4-mini` | passed | Read-only ephemeral run invoked `/legacy-brd-writer`, returned `05_brds/CREDIT-LIMIT/`, listed the three BRD files, preserved `BR-*` as `needs_sme_review`, refused new `BR-*` minting, used repository evidence-strength names, and confirmed no writes. |
| Claude Code | `haiku` | passed | Invoked `/legacy-brd-writer`, returned uppercase slug output directory, three-file contract, correct no-new-`BR-*` policy, repository evidence-strength names, and no-write confirmation. |
| OpenCode | `minimax-m2.5-free` | passed | After v0.1.1 enum hardening, invoked `legacy-brd-writer`, returned exact output directory/files, correct ID policy, repository evidence-strength names, and no-write confirmation. |

## Weighted Score

| Category | Weight | Score | Weighted | Notes |
| --- | ---: | ---: | ---: | --- |
| Purpose and trigger clarity | 10% | 9.5 | 0.95 | Clear BRD-specific trigger and optional position before spec-writing |
| Workflow completeness | 12% | 9.5 | 1.14 | Ordered workflow, stop conditions, and Step Contract shape are executable |
| IBM i / domain correctness | 14% | 9.5 | 1.33 | Consumes approved IBM i analyses, preserves SME control, and avoids raw-source assumptions |
| Evidence and anti-hallucination | 12% | 10 | 1.20 | Evidence strength stays in EV records; enum is pinned; no invented rules |
| Output contract | 10% | 10 | 1.00 | Three BRD artifacts, stable IDs, and traceability are clear |
| Progressive disclosure | 8% | 9.5 | 0.76 | Main skill remains lean; references/templates carry detail |
| Runtime portability | 10% | 10 | 1.00 | Codex, Claude Code, and OpenCode smoke tests passed from synced adapters |
| Reviewability and testability | 10% | 9.0 | 0.90 | Positive/blocked examples exist; future contradictory-evidence example would help |
| Engineering handoff value | 8% | 9.5 | 0.76 | Handoff to spec-writer is explicit without generating AC/DEC artifacts |
| Maintainability | 6% | 9.5 | 0.57 | Clean layout, version history, and matrix record |

**Final score: 9.56 / 10**.

## Decision

**FIELD-PILOT READY**.

Remaining improvement:

- Add a second negative example showing contradictory evidence across programs.
