---
skill: legacy-flow-context-normalizer
scorecard_version: v0.1.9
static_score: 9.51
decision: repo-ready
status: current
last_verified: 2026-05-29
runtimes_tested:
  codex: { status: synced, model: gpt-5.4, date: 2026-05-29 }
  claude_code: { status: synced, model: haiku, date: 2026-05-29 }
  opencode: { status: synced, model: minimax-m2.5-free, date: 2026-05-29 }
evidence_source: local structural validation + adapter drift checks
---

# Skill Review Scorecard: legacy-flow-context-normalizer v0.1.9

## Review Focus

v0.1.9 adds technical-anchor gates for View 3 Program Flow and View 4 Data
Flow. API IDs, journey IDs, menu IDs, screen IDs, service labels, and business
data labels can no longer stand in for AS400 / IBM i program names or file
names. When the supplied material lacks those anchors, the skill must produce a
Mermaid placeholder and a `source_supplement_required` TBD asking for program
mapping, call graph, inventory, File Specs, DDS/DDL, data dictionary, CRUD
matrix, File I/O map, or SME-confirmed mapping.

## Decision

Repo-ready, not field-pilot ready.

Static score before cap: **9.51 / 10**

Current score after cap: **9.0 / 10**

## Blocking For 9.5

| ID | Finding | Required Change |
| --- | --- | --- |
| LFCN-V019-REV-001 | Three-runtime execution has not yet confirmed the new technical-anchor behavior under sparse and API-only input. | Run sparse, API/menu-only, business-data-only, and strong AS400-anchor prompts in Codex, Claude Code, and OpenCode and confirm View 3 / View 4 use placeholders instead of invented program/file nodes. |

## Verification

```bash
scripts/sync-skills.sh --check --skill legacy-flow-context-normalizer
python3 -m unittest tests/test_flow_context_excel_extractor.py
python3 skills/legacy-flow-context-normalizer/scripts/validate_flow_context_package.py skills/legacy-flow-context-normalizer/examples/minimal-positive
python3 skills/legacy-flow-context-normalizer/scripts/validate_flow_context_package.py --allow-blocked skills/legacy-flow-context-normalizer/examples/blocked-authorization-negative
python3 scripts/verify-skill-claims.py
```

Local structural checks passed at review time.
