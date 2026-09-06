---
skill: legacy-modernization-orchestrator
scorecard_version: v0.2.5
static_score: 9.44
decision: repo-ready
status: current
last_verified: 2026-05-29
runtimes_tested:
  codex: { status: synced, model: gpt-5.4, date: 2026-05-29 }
  claude_code: { status: synced, model: haiku, date: 2026-05-29 }
  opencode: { status: synced, model: minimax-m2.5-free, date: 2026-05-29 }
evidence_source: static review + adapter drift checks
---

# Skill Review Scorecard: legacy-modernization-orchestrator v0.2.5

## Review Focus

v0.2.5 makes BRD-first routing explicit. After module analysis, the standard
route is `legacy-brd-writer`; `legacy-spec-writer` requires an approved BRD
Package or an explicit technical-spec-only bypass with risk acceptance.

## Decision

**Repo-ready, expanded-route smoke pending.**

This closes the observed routing gap where a complete FS / Diagram Flow / TD
input could cause the workflow to jump to spec-writing before producing the
BRD review package.

## Blocking For Field Pilot

Run expanded-route smoke across Codex, Claude Code, and OpenCode covering:
module-analysis-done without BRD, approved BRD to spec, and explicit bypass.
