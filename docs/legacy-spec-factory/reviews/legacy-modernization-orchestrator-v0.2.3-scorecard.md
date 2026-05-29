---
skill: legacy-modernization-orchestrator
scorecard_version: v0.2.3
static_score: 9.38
decision: repo-ready
status: current
last_verified: 2026-05-28
runtimes_tested:
  codex: { status: synced, model: gpt-5.4-mini, date: 2026-05-28 }
  claude_code: { status: synced, model: haiku, date: 2026-05-28 }
  opencode: { status: synced, model: minimax-m2.5-free, date: 2026-05-28 }
evidence_source: docs/runtime-matrix.md
---

# Skill Review Scorecard: legacy-modernization-orchestrator v0.2.3

## Review Focus

v0.2.3 updates the main router so users with Function Specs, Technical
Designs, Program Specs, File Specs, interface specs, data dictionaries, or
mixed historical spec workbooks are routed into
`legacy-flow-context-normalizer` instead of being treated as a forward-only
workflow. These sources remain optional starting material; the router still
does not require perfect four-flow input and still blocks direct BRD generation
from unreviewed draft context.

## Decision

Repo-ready, not field-pilot ready.

Static score before cap: **9.38 / 10**

Current score after cap: **9.0 / 10**

## Blocking For 9.5

| ID | Finding | Required Change |
| --- | --- | --- |
| ORCH-V023-REV-001 | Spec-document routing has not passed runtime smoke in all three runtimes. | Run the expanded orchestrator smoke suite with Function Spec, Technical Design, Program Spec, File Spec, sparse triage, and owner-accepted sparse routes. |
| ORCH-V023-REV-002 | Prior expanded routes remain incompletely executed in all runtimes for the new version. | Execute program -> flow, flow -> module, module -> spec, blocked handoff, document-normalizer, and risk-accepted sparse scenarios across all runtimes. |

## Verification

```bash
scripts/sync-skills.sh --skill legacy-modernization-orchestrator --check
```

Scoped adapter drift checks passed locally. The repository-wide
`scripts/verify-skill-claims.py` check is currently blocked by an unrelated
`legacy-brd-writer` version string drift in pre-existing dirty files.
