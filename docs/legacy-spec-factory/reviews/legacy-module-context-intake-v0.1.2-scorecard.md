---
skill: legacy-module-context-intake
scorecard_version: v0.1.2
static_score: 9.43
decision: repo-ready
status: current
last_verified: 2026-05-27
runtimes_tested:
  codex: { status: synced, model: gpt-5.4-mini, date: 2026-05-27 }
  claude_code: { status: synced, model: haiku, date: 2026-05-27 }
  opencode: { status: synced, model: minimax-m2.5-free, date: 2026-05-27 }
evidence_source: docs/runtime-matrix.md
---

# Skill Review Scorecard: legacy-module-context-intake v0.1.2

## Review Focus

v0.1.2 accepts owner-risk-approved sparse `legacy-flow-context-normalizer`
packages as low-confidence `ready_with_warnings` input. The skill must preserve
all missing-view TBDs, keep sparse facts out of approved business rules, and
avoid treating risk acceptance as context approval.

## Decision

Repo-ready, not field-pilot ready.

Static score before cap: **9.43 / 10**

Current score after cap: **9.0 / 10**

## Blocking For 9.5

| ID | Finding | Required Change |
| --- | --- | --- |
| LMCI-REV-001 | Runtime smoke has not covered accepted sparse flow-normalization input. | Run positive RAG intake, accepted sparse intake, and negative unauthorized evidence prompts across Codex, Claude Code, and OpenCode. |
| LMCI-REV-002 | Downstream module-analyzer behavior with sparse context is not yet smoke-tested. | Add a module-analyzer negative/low-confidence route test before field-pilot label. |

## Verification

```bash
python3 skills/legacy-module-context-intake/scripts/validate_context_package.py skills/legacy-module-context-intake/examples/credit-check-rag-positive
python3 skills/legacy-module-context-intake/scripts/validate_context_package.py --allow-blocked skills/legacy-module-context-intake/examples/blocked-contradiction-negative
```

Existing structural examples remain valid.
