---
skill: legacy-sme-review-facilitator
scorecard_version: v0.1.2
static_score: 9.40
decision: repo-ready
status: current
last_verified: 2026-05-26
runtimes_tested:
  codex: { status: synced, model: gpt-5.4-mini, date: 2026-05-26 }
  claude_code: { status: synced, model: haiku, date: 2026-05-26 }
  opencode: { status: synced, model: minimax-m2.5-free, date: 2026-05-26 }
evidence_source: local static review + scripts/sync-skills.sh
---

# Skill Review Scorecard: legacy-sme-review-facilitator v0.1.2

## Change Under Review

v0.1.2 hardens SME question wording: questions must be business-language first,
with program names, fields, files, and node IDs left in evidence context unless
the SME is being asked as a technical owner.

## Decision

**Repo-ready, runtime smoke pending.**

The update directly reduces the risk that chat-based SME review asks business
reviewers to reason from code objects instead of policy, outcome, exception, or
control language.

## Blocking For Field Pilot

Run chat-review smoke across the three runtimes and confirm generated question
packs preserve business-first phrasing while retaining evidence IDs.
