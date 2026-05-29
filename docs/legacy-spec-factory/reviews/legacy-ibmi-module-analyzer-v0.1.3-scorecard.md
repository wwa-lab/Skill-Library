---
skill: legacy-ibmi-module-analyzer
scorecard_version: v0.1.3
static_score: 9.34
decision: repo-ready
status: current
last_verified: 2026-05-29
runtimes_tested:
  codex: { status: synced, model: gpt-5.4, date: 2026-05-29 }
  claude_code: { status: synced, model: haiku, date: 2026-05-29 }
  opencode: { status: synced, model: minimax-m2.5-free, date: 2026-05-29 }
evidence_source: adapter drift checks
---

# Skill Review Scorecard: legacy-ibmi-module-analyzer v0.1.3

## Review Focus

v0.1.3 makes module analyzer the explicit owner of canonical four-flow module
artifacts under `04_modules/<MODULE-SLUG>/`. Upstream context-package views
must be consumed as inputs and synthesized into fresh module outputs.

## Decision

Repo-ready, runtime smoke pending.

## Blocking For Field Pilot

Run module-first context package and normal flow-analysis synthesis prompts
across Codex, Claude Code, and OpenCode. Confirm outputs create
`module-overview.md`, `01-operation-flow.md`, `02-system-flow.md`,
`03-program-flow.md`, and `04-data-flow.md` only under `04_modules/`.

## Verification

```bash
scripts/sync-skills.sh --check --skill legacy-ibmi-module-analyzer
```

Scoped adapter drift checks passed locally.
