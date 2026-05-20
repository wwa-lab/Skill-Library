---
skill: legacy-ibmi-data-model-analyzer
scorecard_version: v0.1.0
static_score: 9.32
decision: repo-ready
status: current
last_verified: 2026-05-16
runtimes_tested:
  codex: { status: passed, model: gpt-5.4-mini, date: 2026-05-16 }
  claude_code: { status: synced, model: haiku, date: null }
  opencode: { status: passed, model: minimax-m2.5-free, date: 2026-05-16 }
evidence_source: docs/runtime-matrix.md
---

# Skill Review Scorecard: legacy-ibmi-data-model-analyzer v0.1.0

## Metadata

- skill_name: legacy-ibmi-data-model-analyzer
- skill_path: `skills/legacy-ibmi-data-model-analyzer/`
- reviewed_version: v0.1.0
- generated_by: Claude Code
- reviewed_by: Codex
- review_date: 2026-05-16
- target_runtime:
  - [x] Codex
  - [x] Claude Code
  - [x] OpenCode
- decision:
  - [ ] reject
  - [ ] revise
  - [x] repo-ready
  - [ ] field-pilot ready

## Mandatory Stop Conditions

Check any condition that applies:

- [ ] no valid `SKILL.md`
- [ ] missing or weak `name` / `description` frontmatter
- [ ] no copyright / author notice
- [ ] not portable across Codex, Claude Code, and OpenCode
- [ ] runtime-specific assumptions mixed into canonical skill
- [ ] no clear trigger conditions
- [ ] no clear output contract
- [ ] no SME review or evidence governance for IBM i reverse engineering
- [ ] hallucination-prone instructions

If any box above is checked, score cap:

- [ ] cap at 8.0

## Weighted Score

| Category | Weight | Score | Weighted |
| --- | ---: | ---: | ---: |
| Purpose and trigger clarity | 10% | 9.5 | 0.95 |
| Workflow completeness | 12% | 9.4 | 1.13 |
| IBM i / domain correctness | 14% | 9.2 | 1.29 |
| Evidence and anti-hallucination | 12% | 9.5 | 1.14 |
| Output contract | 10% | 9.4 | 0.94 |
| Progressive disclosure | 8% | 9.4 | 0.75 |
| Runtime portability | 10% | 9.0 | 0.90 |
| Reviewability and testability | 10% | 9.2 | 0.92 |
| Engineering handoff value | 8% | 9.3 | 0.74 |
| Maintainability | 6% | 9.4 | 0.56 |

Weighted score before cap: 9.32 / 10.0

Final effective score: 9.0 / 10.0

Reason for cap: positive and negative smoke now pass in Codex CLI and
OpenCode, but Claude Code smoke could not run because the local Claude CLI is
not logged in. Per `docs/skill-review-gate.md`, field-pilot readiness remains
blocked until all target runtimes have recorded smoke evidence.

## Decision Rule

- `>= 9.5`: field-pilot ready
- `9.0 - 9.4`: repo-ready, not field-pilot ready
- `8.0 - 8.9`: revise
- `< 8.0`: reject or rewrite

Disposition: repo-ready, not field-pilot ready.

## Findings

### Blocking Findings

| ID | Severity | Finding | Required Change | Affects |
| --- | --- | --- | --- | --- |
| None | n/a | No blocking findings remain after revision. | n/a | n/a |

### Resolved Findings

| ID | Finding | Fix |
| --- | --- | --- |
| DATA-REV-001 | DDS key semantics overstated ordinary `K` lines as primary keys. | Updated `SKILL.md`, DDS reference, output contract, templates, and positive example to distinguish keyed access paths from uniqueness and primary-key claims. |
| DATA-REV-002 | Output contract introduced non-canonical `FK-*` / candidate IDs. | Relationship IDs now use `DATA-*`; no new nonstandard ID prefix is minted. |
| DATA-REV-003 | Templates encouraged field business-name invention. | Replaced "Field Name (Business)" with SME-approved meaning and TBD guidance. |
| DATA-REV-004 | DB2 examples used non-IBM-i `SYSCAT.*` assumptions. | Reframed metadata extraction around approved IBM i/QSYS2 or shop-provided extracts and warned against blind query use. |
| DATA-REV-005 | Missing mutating program analysis was not represented as its own example. | Added `examples/partial-program-analysis-gap/partial-example.md`. |
| DATA-REV-006 | Smoke found OpenCode using lowercase artifact directory and minting `DATA-*` IDs for PF/LF objects. | Tightened `SKILL.md` and `references/output-contract.md`: `03_data_models/<DATA-SLUG>/` must use uppercase slug, and individual data objects must reuse `OBJ-*`. |
| DATA-REV-007 | Smoke found OpenCode shortening `ORDER-DATA` TBD IDs to `TBD-ORDER-*`. | Added explicit slug rule: all newly minted `DATA-*` and `TBD-*` IDs must use the supplied data-domain slug exactly. |

### Improvement Findings

| ID | Finding | Suggested Change |
| --- | --- | --- |
| DATA-IMP-001 | Claude Code smoke is not recorded. | Run the positive and negative scenarios after `claude` login is restored; then re-score for field-pilot readiness. |
| DATA-IMP-002 | DB2/QSYS2 catalog details may vary by IBM i release. | During field pilot, capture the exact shop-approved metadata extraction commands in evidence intake, not in the portable skill. |

## Smoke Test Evidence

| Runtime | Model | Positive | Negative | Status |
| --- | --- | --- | --- | --- |
| Codex CLI | `gpt-5.4-mini` | Returned `03_data_models/CUSTOMER-MASTER/`, six artifacts, `DATA-CUSTOMER-MASTER-001`, PF/LF access-path findings, CRUD summary, and retention TBDs. | Blocked missing DDS and missing approved ORDPOST program analysis; refused ORDERNO primary-key and ORDER.CUSTNO relationship inference. | passed |
| Claude Code | `haiku` | Not run: CLI returned `Not logged in - Please run /login`. | Not run for same auth blocker. | synced |
| OpenCode | `opencode/minimax-m2.5-free` | Passed after tightening directory and ID rules; returned uppercase `03_data_models/CUSTOMER-MASTER/` and one package `DATA-*` ID. | Passed after tightening slug rule; returned `TBD-ORDER-DATA-*` blockers and refused forbidden inferences. | passed |

No `03_data_models/` artifacts were created in the repository during smoke.
Full `scripts/sync-skills.sh --check` still reports unrelated drift in other
new skills, but all four runtime copies of this skill match canonical source.

## SME Review

- [x] SME governance is explicit
- [x] Observed behavior, inferred rule, and modernization decision are separate
- [x] Evidence tags are required
- [x] IBM i-specific failure modes are covered
- [x] Open questions / TBDs are carried forward instead of hidden

Notes: the revised skill is strict about source-backed structure, SME-backed
meaning, and TBD-led uncertainty. It now avoids turning DDS field names,
ordinary `K` lines, matching names, or inventory relationships into business
facts.

## Runtime Portability Review

- [x] canonical source under `skills/<skill-name>/`
- [x] Claude Code adapter or copy defined if needed
- [x] OpenCode adapter or copy defined if needed
- [x] Codex adapter or copy defined if needed
- [x] runtime-specific metadata isolated from canonical skill

Notes: runtime copies must be synced from canonical source. This review does
not claim field-pilot readiness until Claude Code smoke evidence is captured.

## Requested Revision Prompt For Claude Code

```text
Revise legacy-ibmi-data-model-analyzer for field-pilot readiness.

Target score: 9.5/10.

Remaining issues:
1. Run Claude Code positive and negative smoke after `claude` login is restored.
2. Confirm DB2/QSYS2 catalog extract guidance against a live IBM i field environment.

Required changes:
- Follow docs/runtime-smoke-tests.md.
- Record Claude smoke output in docs/runtime-matrix.md and this scorecard.
- Do not add runtime-specific logic to canonical SKILL.md.
- Preserve author/copyright notices.
- Keep the canonical skill under skills/legacy-ibmi-data-model-analyzer/.
```
