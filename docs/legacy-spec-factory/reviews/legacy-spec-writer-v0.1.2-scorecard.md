---
skill: legacy-spec-writer
scorecard_version: v0.1.2
static_score: 9.33
decision: repo-ready
status: current
last_verified: 2026-05-29
runtimes_tested:
  codex: { status: synced, model: gpt-5.4, date: 2026-05-29 }
  claude_code: { status: synced, model: haiku, date: 2026-05-29 }
  opencode: { status: synced, model: minimax-m2.5-free, date: 2026-05-29 }
evidence_source: static review + adapter drift checks
---

# Skill Review Scorecard: legacy-spec-writer v0.1.2

## Review Focus

v0.1.2 makes the BRD-first gate normative. Standard spec writing now requires
an approved BRD Package for the selected capability, and the spec uses that BRD
as reviewed business context rather than treating it as optional collateral.

## Decision

**Repo-ready, runtime smoke pending.**

The change reduces premature technical-spec generation and makes
`spec.md/spec.yaml` clearly downstream of SME / business review. It preserves
the existing anti-hallucination rule that BRD context cannot replace upstream
evidence.

## Blocking For Field Pilot

Run three-runtime positive smoke with an approved BRD Package and negative
smoke where module analysis exists but BRD approval is missing.
