---
skill: legacy-flow-context-normalizer
scorecard_version: v0.1.5
static_score: 9.47
decision: repo-ready
status: superseded
last_verified: 2026-05-27
runtimes_tested:
  codex: { status: synced, model: gpt-5.4-mini, date: 2026-05-27 }
  claude_code: { status: synced, model: haiku, date: 2026-05-27 }
  opencode: { status: synced, model: minimax-m2.5-free, date: 2026-05-27 }
evidence_source: docs/runtime-matrix.md
---

# Skill Review Scorecard: legacy-flow-context-normalizer v0.1.5

## Review Focus

v0.1.5 adds the owner risk-acceptance exit for sparse inputs. When the team
cannot provide more flow material after being asked, the package may move from
`triage_needs_source_enrichment` to `ready_with_warnings` only with named
SME/source-owner acceptance, preserved `quality_level: L1 sparse`, visible
carry-forward `TBD-*`, and downstream restrictions against approved facts or
BRD claims from sparse context alone.

## Decision

Repo-ready, not field-pilot ready.

Static score before cap: **9.47 / 10**

Current score after cap: **9.0 / 10**

## Blocking For 9.5

| ID | Finding | Required Change |
| --- | --- | --- |
| LFCN-REV-001 | Runtime execution has not covered owner-accepted sparse inputs. | Run positive, partial, sparse-triage, risk-accepted sparse, and negative authorization smoke prompts in Codex, Claude Code, and OpenCode. |
| LFCN-REV-002 | Real messy workbooks remain untested. | Pilot one representative multi-sheet workbook and harden extraction if needed. |

## Verification

```bash
python3 -m unittest tests/test_flow_context_excel_extractor.py
python3 skills/legacy-flow-context-normalizer/scripts/validate_flow_context_package.py skills/legacy-flow-context-normalizer/examples/minimal-positive
python3 skills/legacy-flow-context-normalizer/scripts/validate_flow_context_package.py --allow-blocked skills/legacy-flow-context-normalizer/examples/blocked-authorization-negative
```

Local structural verification passed.
