---
skill: legacy-modernization-orchestrator
scorecard_version: v0.2.2
static_score: 9.37
decision: repo-ready
status: superseded
last_verified: 2026-05-27
runtimes_tested:
  codex: { status: synced, model: gpt-5.4-mini, date: null }
  claude_code: { status: passed, model: haiku, date: 2026-05-14 }
  opencode: { status: synced, model: minimax-m2.5-free, date: null }
evidence_source: docs/runtime-matrix.md
---

# Skill Review Scorecard: legacy-modernization-orchestrator v0.2.2

## Review Focus

v0.2.2 teaches the main router the risk-accepted sparse-input route. A raw
`triage_needs_source_enrichment` package still routes to source-owner
supplement collection, but a named-owner `ready_with_warnings` package with
`quality_level: L1 sparse` and accepted risk may route to
`legacy-module-context-intake`. The router still blocks direct module analysis
or BRD generation from sparse context.

## Decision

Repo-ready, not field-pilot ready.

Static score before cap: **9.37 / 10**

Current score after cap: **9.0 / 10**

## Blocking For 9.5

| ID | Finding | Required Change |
| --- | --- | --- |
| ORCH-V022-REV-001 | Risk-accepted sparse routing has not passed runtime smoke in all three runtimes. | Run the expanded orchestrator smoke suite, including sparse triage and owner-accepted sparse routes. |
| ORCH-V022-REV-002 | Prior expanded routes remain incompletely executed in Codex/OpenCode. | Execute program -> flow, flow -> module, module -> spec, blocked handoff, and document-normalizer routes across all runtimes. |

## Verification

```bash
python3 scripts/verify-skill-claims.py
scripts/sync-skills.sh --skill legacy-modernization-orchestrator --check
```

Structural claim and adapter drift checks passed locally.
