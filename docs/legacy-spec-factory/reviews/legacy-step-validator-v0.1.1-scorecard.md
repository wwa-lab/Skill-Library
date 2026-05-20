---
skill: legacy-step-validator
scorecard_version: v0.1.1
static_score: 9.53
decision: field-pilot ready
status: current
last_verified: 2026-05-14
runtimes_tested:
  codex: { status: passed, model: gpt-5.4-mini, date: 2026-05-14 }
  claude_code: { status: passed, model: haiku, date: 2026-05-14 }
  opencode: { status: passed, model: minimax-m2.5-free, date: 2026-05-14 }
evidence_source: docs/runtime-matrix.md
---

# Skill Review Scorecard: legacy-step-validator v0.1.1

## Metadata

- skill_name: legacy-step-validator
- skill_path: skills/legacy-step-validator
- reviewed_version: v0.1.1
- generated_by: Claude Code; revised by Codex
- reviewed_by: Codex
- review_date: 2026-05-15
- target_runtime:
  - [x] Codex
  - [x] Claude Code
  - [x] OpenCode
- decision:
  - [ ] reject
  - [ ] revise
  - [ ] repo-ready
  - [x] field-pilot ready

## Review Evidence

- Reviewed against `docs/skill-review-gate.md`.
- Checked canonical source under `skills/legacy-step-validator/`.
- Checked `SKILL.md`, `references/validation-checklists.md`,
  `references/finding-taxonomy.md`,
  `templates/step-validation-report.md`,
  `templates/blocking-findings.yaml`, and examples under
  `skills/legacy-step-validator/examples/`.
- Verified v0.1.1 splits downstream advancement from remediation via
  `downstream_next_step` and `remediation_step`.
- Verified the blocked example consistently lists four blocking findings
  (`FIND-CARD-AUTH-001` through `FIND-CARD-AUTH-004`).
- Verified SME waiver source requirements are documented.
- Verified spec-review-as-a-step is intentionally deferred until
  `legacy-spec-reviewer` exists.
- Ran `scripts/sync-skills.sh --check`; all runtime adapter copies reported
  `OK`.
- Checked `docs/runtime-matrix.md` and `docs/runtime-smoke-tests.md`; positive
  and negative smoke tests passed in Codex CLI (`gpt-5.4-mini`), Claude Code
  (`haiku`), and OpenCode (`opencode/minimax-m2.5-free`) on 2026-05-14.

## Mandatory Stop Conditions

No mandatory 8.0 cap conditions found.

No 9.0 cap conditions remain:

- examples exist and include both pass and blocked outcomes
- validation reports and blocking findings are structured
- runtime portability has been smoke-tested in all three target runtimes
- review checklist maps to measurable compact-result fields

## Weighted Score

| Category | Weight | Score | Weighted |
| --- | ---: | ---: | ---: |
| Purpose and trigger clarity | 10% | 9.6 | 0.96 |
| Workflow completeness | 12% | 9.5 | 1.14 |
| IBM i / domain correctness | 14% | 9.2 | 1.29 |
| Evidence and anti-hallucination | 12% | 9.7 | 1.16 |
| Output contract | 10% | 9.5 | 0.95 |
| Progressive disclosure | 8% | 9.4 | 0.75 |
| Runtime portability | 10% | 9.7 | 0.97 |
| Reviewability and testability | 10% | 9.7 | 0.97 |
| Engineering handoff value | 8% | 9.6 | 0.77 |
| Maintainability | 6% | 9.4 | 0.56 |

Final score: **9.53 / 10**

Decision: **field-pilot ready**

## Findings

### Blocking Findings

| ID | Severity | Finding | Required Change | Affects |
| --- | --- | --- | --- | --- |
| None | - | No blocking findings remain for field-pilot entry. | - | - |

### Improvement Findings

| ID | Finding | Suggested Change |
| --- | --- | --- |
| STEP-VALIDATOR-IMP-001 | Re-run ID policy for repeated validations is still implicit. | Add a stable-finding-ID rule based on `step_id + dimension + referenced_check`. |
| STEP-VALIDATOR-IMP-002 | Checklist rows are useful but heavy to cite from findings. | Add short check IDs such as `INV-MECH-01` and `SPEC-SEM-04`. |
| STEP-VALIDATOR-IMP-003 | Slug casing and hyphen normalization are not fully specified for renamed folders. | Document whether to normalize or block on folder-name mismatch. |

## SME Review

- [x] SME governance is explicit
- [x] Observed behavior, inferred rule, and modernization decision are separate
- [x] Evidence tags are required
- [x] IBM i-specific failure modes are covered through per-step checklists
- [x] Open questions / TBDs are carried forward instead of hidden

Notes:

The validator checks SME readiness and recorded SME decisions without
approving on the SME's behalf. This is the correct boundary for a validation
skill.

## Runtime Portability Review

- [x] canonical source under `skills/legacy-step-validator/`
- [x] Claude Code adapter or copy defined
- [x] OpenCode adapter or copy defined
- [x] Codex adapter or copy defined
- [x] runtime-specific metadata isolated from canonical skill

Notes:

Adapter drift check passes. Positive and negative runtime smoke tests passed in
Codex CLI, Claude Code, and OpenCode.

## Adversarial Pass

| Scenario | Expected Behavior | Result |
| --- | --- | --- |
| Inventory pass example | Emits `pass`, no blocking items, and downstream program analyzer | Passed in smoke |
| Module blocked example | Emits `blocked`, exactly four findings, and remediation to flow analyzer | Passed in smoke |
| User asks validator to write a spec | Refuse and route to spec writer | Covered |
| User asks validator to approve SME decision | Refuse | Covered |
| Artifact contains unredacted data | Redaction Gate blocks before semantic review | Covered |

## Sign-Off

- Review Status: field-pilot ready
- Runtime Status: passed in Codex CLI, Claude Code, and OpenCode
- Remaining Work: optional checklist-ID and re-validation-ID cleanup only
