---
skill: legacy-flow-context-normalizer
scorecard_version: v0.1.8
static_score: 9.50
decision: repo-ready
status: superseded
last_verified: 2026-05-29
runtimes_tested:
  codex: { status: synced, model: gpt-5.4, date: 2026-05-29 }
  claude_code: { status: synced, model: haiku, date: 2026-05-29 }
  opencode: { status: synced, model: minimax-m2.5-free, date: 2026-05-29 }
evidence_source: local structural validation + adapter drift checks
---

# Skill Review Scorecard: legacy-flow-context-normalizer v0.1.8

## Review Focus

v0.1.8 clarifies that this skill creates draft context views under
`00_context_packages/`, not canonical module-flow artifacts under
`04_modules/`. The goal is to prevent sparse Function Spec / Technical Design
inputs from being reported as completed module analysis.

## Decision

Repo-ready, not field-pilot ready.

Static score before cap: **9.50 / 10**

Current score after cap: **9.0 / 10**

## Blocking For 9.5

| ID | Finding | Required Change |
| --- | --- | --- |
| LFCN-V018-REV-001 | Three-runtime execution has not yet confirmed the new reporting language. | Run sparse, partial, and strong document-normalization prompts in Codex, Claude Code, and OpenCode and confirm outputs say "context views" before module analysis. |

## Verification

```bash
scripts/sync-skills.sh --check --skill legacy-flow-context-normalizer
python3 -m unittest tests/test_flow_context_excel_extractor.py
python3 skills/legacy-flow-context-normalizer/scripts/validate_flow_context_package.py skills/legacy-flow-context-normalizer/examples/minimal-positive
python3 skills/legacy-flow-context-normalizer/scripts/validate_flow_context_package.py --allow-blocked skills/legacy-flow-context-normalizer/examples/blocked-authorization-negative
```

All local checks passed.
