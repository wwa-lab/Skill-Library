---
skill: legacy-spec-writer
scorecard_version: v0.1.1
static_score: 9.25
decision: repo-ready
status: current
last_verified: 2026-05-26
runtimes_tested:
  codex: { status: synced, model: gpt-5.4-mini, date: 2026-05-26 }
  claude_code: { status: synced, model: haiku, date: 2026-05-26 }
  opencode: { status: synced, model: minimax-m2.5-free, date: 2026-05-26 }
evidence_source: local static review + scripts/sync-skills.sh
---

# Skill Review Scorecard: legacy-spec-writer v0.1.1

## Change Under Review

v0.1.1 clarifies that `process_flow.steps[]` are business-visible target
capability steps. The legacy Transaction Call Map is supporting evidence, not a
source to copy one-for-one into the spec process flow.

## Decision

**Repo-ready, runtime smoke pending.**

This keeps `spec.yaml` modernization-ready while preventing the human-readable
spec from becoming a replay of legacy program call order.

## Blocking For Field Pilot

Run positive and negative spec-writing smoke across Codex, Claude Code, and
OpenCode; confirm process flow steps are behavior/outcome-oriented and still
trace to `EV-*`.
