---
skill: legacy-module-context-intake
scorecard_version: v0.1.4
static_score: 9.46
decision: repo-ready
status: current
last_verified: 2026-05-29
runtimes_tested:
  codex: { status: synced, model: gpt-5.4, date: 2026-05-29 }
  claude_code: { status: synced, model: haiku, date: 2026-05-29 }
  opencode: { status: synced, model: minimax-m2.5-free, date: 2026-05-29 }
evidence_source: local structural validation + adapter drift checks
---

# Skill Review Scorecard: legacy-module-context-intake v0.1.4

## Review Focus

v0.1.4 clarifies that intake view files are context-only inputs. They may feed
module analysis, but they must not be reported as canonical four-flow module
artifacts.

## Decision

Repo-ready, not field-pilot ready.

Static score before cap: **9.46 / 10**

Current score after cap: **9.0 / 10**

## Blocking For 9.5

| ID | Finding | Required Change |
| --- | --- | --- |
| LMCI-V014-REV-001 | Runtime smoke has not yet confirmed module-first context handoff wording across all three runtimes. | Run positive RAG intake, accepted sparse intake, and blocked contradiction prompts in Codex, Claude Code, and OpenCode. |

## Verification

```bash
scripts/sync-skills.sh --check --skill legacy-module-context-intake
python3 skills/legacy-module-context-intake/scripts/validate_context_package.py skills/legacy-module-context-intake/examples/credit-check-rag-positive
python3 skills/legacy-module-context-intake/scripts/validate_context_package.py --allow-blocked skills/legacy-module-context-intake/examples/blocked-contradiction-negative
```

All local checks passed.
