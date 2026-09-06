---
skill: legacy-modernization-orchestrator
scorecard_version: v0.2.1
static_score: 9.36
decision: repo-ready
status: superseded
last_verified: 2026-05-27
runtimes_tested:
  codex: { status: synced, model: gpt-5.4-mini, date: null }
  claude_code: { status: passed, model: haiku, date: 2026-05-14 }
  opencode: { status: synced, model: minimax-m2.5-free, date: null }
evidence_source: docs/runtime-matrix.md
---

# Skill Review Scorecard: legacy-modernization-orchestrator v0.2.1

## Metadata

- skill_name: legacy-modernization-orchestrator
- skill_path: skills/legacy-modernization-orchestrator
- reviewed_version: v0.2.1
- generated_by: Codex
- reviewed_by: Codex
- review_date: 2026-05-27
- target_runtime:
  - [x] Codex
  - [x] Claude Code
  - [x] OpenCode
- decision:
  - [ ] reject
  - [ ] revise
  - [x] repo-ready
  - [ ] field-pilot ready

## Review Focus

v0.2.1 aligns the main router with `legacy-flow-context-normalizer` v0.1.4.
The orchestrator now routes scattered document inputs by quality: strong and
partial inputs go to draft flow normalization, sparse authorized inputs go to
`triage_needs_source_enrichment`, and only unauthorized, unreadable,
out-of-scope, or boundaryless inputs are treated as blocked remediation.

## Mandatory Stop Conditions

No mandatory 8.0 cap conditions found.

The existing runtime cap still applies. The prior Claude Code smoke evidence
covers older routes, but v0.2.1's sparse-document routing has not been run in
Codex CLI, Claude Code, and OpenCode.

## Weighted Score

| Category | Weight | Score | Weighted |
| --- | ---: | ---: | ---: |
| Purpose and trigger clarity | 10% | 9.6 | 0.96 |
| Workflow completeness | 12% | 9.5 | 1.14 |
| IBM i / domain correctness | 14% | 9.2 | 1.29 |
| Evidence and anti-hallucination | 12% | 9.6 | 1.15 |
| Output contract | 10% | 9.4 | 0.94 |
| Progressive disclosure | 8% | 9.4 | 0.75 |
| Runtime portability | 10% | 9.0 | 0.90 |
| Reviewability and testability | 10% | 9.3 | 0.93 |
| Engineering handoff value | 8% | 9.4 | 0.75 |
| Maintainability | 6% | 9.3 | 0.56 |

Static score before cap: **9.36 / 10**

Current score after cap: **9.0 / 10**

Decision: **repo-ready, not field-pilot ready**

## Blocking For 9.5

| ID | Finding | Required Change | Affects |
| --- | --- | --- | --- |
| ORCH-V021-REV-001 | v0.2.1 sparse-document routing has not passed runtime smoke in all three runtimes. | Run the expanded orchestrator smoke suite, including the sparse-document route to `legacy-flow-context-normalizer`, in Codex, Claude Code, and OpenCode. | Runtime portability, reviewability |
| ORCH-V021-REV-002 | The prior v0.2.0 expanded routes are still not fully executed in Codex/OpenCode. | Execute program -> flow, flow -> module, module -> spec, blocked forward handoff, and document-normalizer routes across all runtimes. | Routing correctness |

## Strengths

- The main router no longer implies users need perfect four-flow inputs before
  starting the module-first path.
- `triage_needs_source_enrichment` is held at stage 0d, preventing premature
  routing to context intake, module analysis, or BRD generation.
- Stage identification, decision table, stage card index, skill family docs,
  README, and smoke prompts now share the same sparse-input route.

## Verification

```bash
python3 scripts/verify-skill-claims.py
scripts/sync-skills.sh --skill legacy-modernization-orchestrator --check
```

Structural claim and adapter drift checks passed locally after the update.
