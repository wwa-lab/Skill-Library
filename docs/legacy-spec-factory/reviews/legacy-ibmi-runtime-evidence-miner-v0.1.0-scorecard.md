---
skill: legacy-ibmi-runtime-evidence-miner
scorecard_version: v0.1.0
static_score: 9.57
decision: field-pilot ready
status: current
last_verified: 2026-05-16
runtimes_tested:
  codex: { status: passed, model: gpt-5.4-mini, date: 2026-05-16 }
  claude_code: { status: passed, model: haiku, date: 2026-05-16 }
  opencode: { status: passed, model: minimax-m2.5-free, date: 2026-05-16 }
evidence_source: docs/runtime-matrix.md
---

<!--
Legacy Spec Factory
Copyright 2026 Leo L Zhang

Original author: Leo L Zhang
License: Apache License 2.0

This skill scorecard is part of the Legacy Spec Factory project.
-->

# Skill Review Scorecard: legacy-ibmi-runtime-evidence-miner v0.1.0

## Metadata

- skill_name: `legacy-ibmi-runtime-evidence-miner`
- skill_path: `skills/legacy-ibmi-runtime-evidence-miner/`
- reviewed_version: v0.1.0
- reviewed_by: Codex
- review_date: 2026-05-16
- target_runtime:
  - [x] Codex
  - [x] Claude Code
  - [x] OpenCode
- decision:
  - [ ] reject
  - [ ] revise
  - [ ] repo-ready
  - [x] field-pilot ready

## Mandatory Stop Conditions

No mandatory stop condition applies after the v0.1.0 fixes.

- [ ] no valid `SKILL.md`
- [ ] missing or weak `name` / `description` frontmatter
- [ ] no copyright / author notice
- [ ] not portable across Codex, Claude Code, and OpenCode
- [ ] runtime-specific assumptions mixed into canonical skill
- [ ] no clear trigger conditions
- [ ] no clear output contract
- [ ] no SME review or evidence governance for IBM i reverse engineering
- [ ] hallucination-prone instructions
- [ ] cap at 8.0

## Weighted Score

| Category | Weight | Score | Weighted |
| --- | ---: | ---: | ---: |
| Purpose and trigger clarity | 10% | 9.6 | 0.96 |
| Workflow completeness | 12% | 9.5 | 1.14 |
| IBM i / domain correctness | 14% | 9.4 | 1.32 |
| Evidence and anti-hallucination | 12% | 9.7 | 1.16 |
| Output contract | 10% | 9.6 | 0.96 |
| Progressive disclosure | 8% | 9.4 | 0.75 |
| Runtime portability | 10% | 9.8 | 0.98 |
| Reviewability and testability | 10% | 9.7 | 0.97 |
| Engineering handoff value | 8% | 9.6 | 0.77 |
| Maintainability | 6% | 9.4 | 0.56 |

Final score: **9.57 / 10**

The prior runtime cap is resolved. Positive and negative no-write smoke tests
passed in Codex CLI, Claude Code, and OpenCode on 2026-05-16.

## Findings

### Resolved Findings

| ID | Finding | Fix |
| --- | --- | --- |
| RTE-REV-001 | Canonical `SKILL.md` had no portable YAML frontmatter, so the skill was not discoverable in the loaded Codex skill list. | Added conservative `name` and `description` frontmatter to canonical source and synced all runtime adapters. |
| RTE-REV-002 | Positive example claimed high confidence from a single run. | Updated positive and incomplete-log examples plus confidence rules so single-run observations stay medium/low and incomplete observations stay low. |
| RTE-REV-003 | Runtime smoke exposed schedule overstatement: a single run could be described as nightly/typical. | Added explicit single-run frequency rule to `SKILL.md` and smoke prompts; reruns avoided nightly/scheduled/BAU claims. |
| RTE-REV-004 | Output contract used `joblog`, which drifted from evidence-intake manifest type `job_log`. | Aligned output contract and templates to `source_artifact_type: job_log`. |
| RTE-REV-005 | `mining-checklist.md` was implied by Step 9 but not explicit in the OUTPUT section. | Marked `mining-checklist.md` as the required review artifact whenever mining proceeds. |
| RTE-REV-006 | Scorecard lacked frontmatter, so status verification ignored it. | Added current scorecard frontmatter matching runtime matrix and truth table claims. |

### Remaining Improvement Items

| ID | Finding | Suggested Change |
| --- | --- | --- |
| RTE-IMP-001 | Downstream consumption with program/flow/module analyzers was not integration-tested in this pass. | Add a separate integration smoke that feeds `runtime-evidence.jsonl` into `runtime_hints`, `bau_notes`, and module View 1 context. |
| RTE-IMP-002 | There is no deterministic JSONL schema validator script for generated runtime evidence. | Consider adding a small line-by-line JSONL validator if field pilots generate many runtime evidence files. |

## Runtime Smoke Results

| Runtime | Model | Positive | Negative | Result |
| --- | --- | --- | --- | --- |
| Codex CLI | `gpt-5.4-mini` | Returned `runtime-evidence.jsonl`, `mining-checklist.md`, five observation types, `high: 0`, `medium: 2`, `low: 3`, and no writes. | Blocked draft confidential job log with pending redaction; emitted no files and routed to evidence/redaction approval. | passed |
| Claude Code | `haiku` | Passed after tightening single-run frequency rules; returned required files, no schedule claim, `high: 0`, and no writes. | Blocked draft confidential job log with pending redaction; emitted no files and routed to evidence intake/redaction owner approval. | passed |
| OpenCode | `opencode/minimax-m2.5-free` | Passed in disposable temp copy; returned `runtime-evidence.jsonl`, `mining-checklist.md`, four observation types, `high: 0`, `medium: 0`, `low: 4`, and no writes. | Passed in disposable temp copy; blocked draft confidential job log and emitted no files. | passed |

## Decision

Decision: **field-pilot ready**.

The skill is discoverable, portable, and contract-safe across Codex, Claude
Code, and OpenCode. The positive smoke confirms runtime mining proceeds only
from approved/redacted evidence and does not overstate confidence from a single
run. The negative smoke confirms confidential unapproved logs block at Step 1.
