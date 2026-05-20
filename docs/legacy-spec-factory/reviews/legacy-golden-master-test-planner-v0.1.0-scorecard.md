---
skill: legacy-golden-master-test-planner
scorecard_version: v0.1.0
static_score: 9.59
decision: field-pilot ready
status: current
last_verified: 2026-05-16
runtimes_tested:
  codex: { status: passed, model: gpt-5.4-mini, date: 2026-05-16 }
  claude_code: { status: passed, model: haiku, date: 2026-05-16 }
  opencode: { status: passed, model: minimax-m2.5-free, date: 2026-05-16 }
evidence_source: docs/runtime-matrix.md
---

# Skill Review Scorecard - legacy-golden-master-test-planner v0.1.0

## Metadata

- skill_name: `legacy-golden-master-test-planner`
- skill_path: `skills/legacy-golden-master-test-planner/`
- reviewed_version: v0.1.0
- generated_by: Claude Code / Codex draft iteration
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

No mandatory stop condition applies after the v0.1.0 fixes.

## Weighted Score

| Category | Weight | Score | Weighted |
| --- | ---: | ---: | ---: |
| Purpose and trigger clarity | 10% | 9.6 | 0.96 |
| Workflow completeness | 12% | 9.6 | 1.15 |
| IBM i / domain correctness | 14% | 9.5 | 1.33 |
| Evidence and anti-hallucination | 12% | 9.7 | 1.16 |
| Output contract | 10% | 9.6 | 0.96 |
| Progressive disclosure | 8% | 9.4 | 0.75 |
| Runtime portability | 10% | 9.8 | 0.98 |
| Reviewability and testability | 10% | 9.7 | 0.97 |
| Engineering handoff value | 8% | 9.6 | 0.77 |
| Maintainability | 6% | 9.4 | 0.56 |

Final score: **9.59 / 10**

The previous runtime cap is resolved. Runtime adapter copies were refreshed for
this skill and positive/negative no-write smoke tests passed in Codex CLI,
Claude Code, and OpenCode on 2026-05-16.

## Decision Rule

- `>= 9.5`: field-pilot ready
- `9.0 - 9.4`: repo-ready, not field-pilot ready
- `8.0 - 8.9`: revise
- `< 8.0`: reject or rewrite

Decision: **field-pilot ready**.

## Findings

### Blocking Findings

| ID | Severity | Finding | Required Change | Affects |
| --- | --- | --- | --- | --- |
| None | - | No blocking findings remain in the canonical skill. | - | - |

### Improvement Findings

| ID | Finding | Suggested Change |
| --- | --- | --- |
| GMTP-IMP-001 | Resolved: runtime adapter copies were refreshed for this skill. | Keep adapters synced with canonical source before future releases. |
| GMTP-IMP-002 | Resolved: positive and negative smoke tests passed in Codex CLI, Claude Code, and OpenCode. | Keep the prompts in `docs/runtime-smoke-tests.md` current when the contract changes. |
| GMTP-IMP-003 | No deterministic validator script exists for the YAML plan contract. | Consider adding a small schema/check script if golden master planning becomes a frequent workflow. |

## SME Review

- [x] SME governance is explicit
- [x] Observed behavior, inferred rule, and modernization decision are separate
- [x] Evidence tags are required
- [x] IBM i-specific failure modes are covered
- [x] Open questions / TBDs are carried forward instead of hidden

Notes:

The skill requires capability-owner SME approval, test data owner approval, and
forward SDLC/test owner review before a plan becomes `approved`. It blocks on
missing observed expected outputs instead of deriving them from the spec.

## Runtime Portability Review

- [x] canonical source under `skills/<skill-name>/`
- [x] Claude Code adapter or copy defined if needed
- [x] OpenCode adapter or copy defined if needed
- [x] Codex adapter or copy defined if needed
- [x] runtime-specific metadata isolated from canonical skill

Notes:

The skill uses only portable Agent Skill files: `SKILL.md`, `references/`,
`templates/`, and `examples/`. It has no IDE-private assumptions. Runtime
copies for this skill were refreshed directly from canonical source to avoid
touching unrelated adapter drift in the current worktree.

## Runtime Smoke Results

| Runtime | Model | Positive | Negative | Result |
| --- | --- | --- | --- | --- |
| Codex CLI | `gpt-5.4-mini` | Returned five `06_quality/CREDIT-LIMIT/` files, `TC-CREDIT-LIMIT-001` through `TC-CREDIT-LIMIT-003`, full coverage, and no writes. | Blocked missing expected-output evidence, minted no `TC-*`, returned only blocked-run outputs, and confirmed no writes. | passed |
| Claude Code | `haiku` with Read-only tools | Returned the required `06_quality/CREDIT-LIMIT/` file set, three `TC-*`, full coverage, and no writes after reading the project skill. | Blocked missing expected-output evidence, minted no `TC-*`, returned blocked-run outputs, and confirmed no writes. | passed |
| OpenCode | `opencode/minimax-m2.5-free` | Returned the required `06_quality/CREDIT-LIMIT/` file set, three `TC-*`, full coverage, and no writes. | Blocked missing expected-output evidence, minted no `TC-*`, routed to evidence intake, and confirmed no writes. | passed |

Codex initially exposed an invalid unquoted frontmatter description; the
description is now quoted and frontmatter parsing passes in canonical and all
four adapter copies.

## Revision Summary

Fixed in this review pass:

- Linked `SKILL.md` to the added reference files and examples.
- Added explicit guidance for when to load selection, comparison, and
  anti-hallucination references.
- Completed the positive example package with human-readable plan, coverage
  matrix, sample data manifest, and review file.
- Added a blocked negative example for missing runtime expected-output evidence.
- Corrected `CAP-*`, `STEP-*`, and `TC-*` IDs to follow
  `docs/id-conventions.md`.
- Removed non-ASCII characters from the skill package.

## Requested Revision Prompt For Claude Code

```text
No blocking revision is required for v0.1.0.

Optional future hardening:
- Add a deterministic contract checker for `golden-master-tests.yaml` if the
  workflow needs stronger mechanical validation.

Do not remove author/copyright notices.
Keep the canonical skill under skills/legacy-golden-master-test-planner/.
Maintain compatibility with Codex, Claude Code, and OpenCode.
```
