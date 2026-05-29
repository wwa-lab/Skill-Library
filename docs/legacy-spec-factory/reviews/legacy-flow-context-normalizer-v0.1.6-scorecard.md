---
skill: legacy-flow-context-normalizer
scorecard_version: v0.1.6
static_score: 9.48
decision: repo-ready
status: current
last_verified: 2026-05-28
runtimes_tested:
  codex: { status: synced, model: gpt-5.4-mini, date: 2026-05-28 }
  claude_code: { status: synced, model: haiku, date: 2026-05-28 }
  opencode: { status: synced, model: minimax-m2.5-free, date: 2026-05-28 }
evidence_source: docs/runtime-matrix.md
---

# Skill Review Scorecard: legacy-flow-context-normalizer v0.1.6

## Review Focus

v0.1.6 expands raw input coverage beyond existing flow artifacts. The skill now
explicitly accepts Function Specs, Technical Designs, Program Specs, File
Specs, interface specs, and data dictionaries as optional evidence sources,
including multi-sheet Excel workbooks where each sheet may represent a
different spec role. The four flows remain the review target, not a mandatory
input shape.

## Decision

Repo-ready, not field-pilot ready.

Static score before cap: **9.48 / 10**

Current score after cap: **9.0 / 10**

## Blocking For 9.5

| ID | Finding | Required Change |
| --- | --- | --- |
| LFCN-REV-001 | Runtime execution has not covered Function Spec / Technical Design / Program Spec / File Spec inputs across all three runtimes. | Run positive, partial, sparse-triage, risk-accepted sparse, spec-workbook, and negative authorization smoke prompts in Codex, Claude Code, and OpenCode. |
| LFCN-REV-002 | Real messy workbooks remain untested. | Pilot one representative multi-sheet workbook and harden extraction if needed. |

## Verification

```bash
python3 -m unittest tests/test_flow_context_excel_extractor.py
python3 skills/legacy-flow-context-normalizer/scripts/validate_flow_context_package.py skills/legacy-flow-context-normalizer/examples/minimal-positive
python3 skills/legacy-flow-context-normalizer/scripts/validate_flow_context_package.py --allow-blocked skills/legacy-flow-context-normalizer/examples/blocked-authorization-negative
```

Local structural verification passed.
