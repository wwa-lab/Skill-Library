---
skill: legacy-step-contract
scorecard_version: v0.1.2
static_score: 9.52
decision: field-pilot ready
status: current
last_verified: 2026-05-29
runtimes_tested:
  codex: { status: passed, model: gpt-5.4, date: 2026-05-29 }
  claude_code: { status: passed, model: haiku, date: 2026-05-29 }
  opencode: { status: passed, model: minimax-m2.5-free, date: 2026-05-29 }
evidence_source: adapter drift checks
---

# Skill Review Scorecard: legacy-step-contract v0.1.2

## Review Focus

v0.1.2 is a terminology-only contract alignment. It renames the
flow-context-normalizer execution output from "draft four-flow package" to
"draft four-view context package" so the generic Step Contract matches the
module-first context boundary.

## Decision

Field-pilot-ready for this narrow wording change.

## Verification

```bash
scripts/sync-skills.sh --check --skill legacy-step-contract
```

Scoped adapter drift checks passed locally.
