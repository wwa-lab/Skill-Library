---
skill: legacy-ibmi-flow-analyzer
scorecard_version: v0.1.2
static_score: 9.62
decision: repo-ready
status: current
last_verified: 2026-05-26
runtimes_tested:
  codex: { status: synced, model: gpt-5.4-mini, date: 2026-05-26 }
  claude_code: { status: synced, model: haiku, date: 2026-05-26 }
  opencode: { status: synced, model: minimax-m2.5-free, date: 2026-05-26 }
evidence_source: local static review + scripts/sync-skills.sh
---

# Skill Review Scorecard: legacy-ibmi-flow-analyzer v0.1.2

## Change Under Review

v0.1.2 hardens `Business Capability Seeds` so candidate rules and SME
questions are business-readable. Technical node, program, field, and object
references remain in `Evidence Basis`, but no longer carry the candidate
statement.

## Decision

**Repo-ready, runtime smoke pending.**

This is a narrow prompt/template hardening. It does not change the flow
analyzer's technical evidence contract, but it reduces downstream leakage of
call-map language into BRD and SME review artifacts.

## Blocking For Field Pilot

Run positive and negative smoke in Codex, Claude Code, and OpenCode against the
new five-column seed table and confirm no model collapses `Business Signal` back
into node/program-only wording.
