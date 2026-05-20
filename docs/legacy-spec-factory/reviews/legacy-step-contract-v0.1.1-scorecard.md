---
skill: legacy-step-contract
scorecard_version: v0.1.1
static_score: 9.52
decision: field-pilot ready
status: current
last_verified: 2026-05-14
runtimes_tested:
  codex: { status: passed, model: gpt-5.4-mini, date: 2026-05-14 }
  claude_code: { status: passed, model: haiku, date: 2026-05-14 }
  opencode: { status: passed, model: minimax-m2.5-free, date: 2026-05-14 }
evidence_source: docs/runtime-matrix.md
---

# Skill Review Scorecard: legacy-step-contract v0.1.1

## Metadata

- skill_name: legacy-step-contract
- skill_path: skills/legacy-step-contract
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
- Checked canonical source under `skills/legacy-step-contract/`.
- Checked `SKILL.md`, `references/step-contract.md`,
  `templates/step-contract-block.md`,
  `templates/step-validation-report.md`, and examples under
  `skills/legacy-step-contract/examples/`.
- Verified v0.1.1 adds filled `inventory-pass` and `inventory-blocked`
  examples instead of template-only guidance.
- Verified compact result fields use `downstream_next_step` and
  `remediation_step` consistently.
- Verified `legacy-step-validator` is identified as the skill that emits
  filled validation reports.
- Ran `scripts/sync-skills.sh --check`; all runtime adapter copies reported
  `OK`.
- Checked `docs/runtime-matrix.md` and `docs/runtime-smoke-tests.md`; positive
  and negative smoke tests passed in Codex CLI (`gpt-5.4-mini`), Claude Code
  (`haiku`), and OpenCode (`opencode/minimax-m2.5-free`) on 2026-05-14.

## Mandatory Stop Conditions

No mandatory 8.0 cap conditions found.

No 9.0 cap conditions remain:

- concrete examples now exist
- references are linked from `SKILL.md`
- validation steps map to measurable compact-result fields
- runtime portability has been smoke-tested in all three target runtimes
- review checklist maps to concrete output fields

## Weighted Score

| Category | Weight | Score | Weighted |
| --- | ---: | ---: | ---: |
| Purpose and trigger clarity | 10% | 9.6 | 0.96 |
| Workflow completeness | 12% | 9.5 | 1.14 |
| IBM i / domain correctness | 14% | 9.2 | 1.29 |
| Evidence and anti-hallucination | 12% | 9.6 | 1.15 |
| Output contract | 10% | 9.5 | 0.95 |
| Progressive disclosure | 8% | 9.5 | 0.76 |
| Runtime portability | 10% | 9.7 | 0.97 |
| Reviewability and testability | 10% | 9.7 | 0.97 |
| Engineering handoff value | 8% | 9.5 | 0.76 |
| Maintainability | 6% | 9.5 | 0.57 |

Final score: **9.52 / 10**

Decision: **field-pilot ready**

## Findings

### Blocking Findings

| ID | Severity | Finding | Required Change | Affects |
| --- | --- | --- | --- | --- |
| None | - | No blocking findings remain for field-pilot entry. | - | - |

### Improvement Findings

| ID | Finding | Suggested Change |
| --- | --- | --- |
| STEP-CONTRACT-IMP-001 | The skill is long for a contract-layer skill and duplicates some reference detail. | In a later cleanup, move more per-step binding detail into `references/step-contract.md`. |
| STEP-CONTRACT-IMP-002 | Non-idempotent step behavior is mentioned but could use a stronger worked example. | Add one example showing how a non-idempotent step carries waiver and re-validation notes. |

## SME Review

- [x] SME governance is explicit
- [x] Observed behavior, inferred rule, and modernization decision are separate
- [x] Evidence tags are required
- [x] IBM i-specific failure modes are covered through per-step bindings and
      downstream skill contracts
- [x] Open questions / TBDs are carried forward instead of hidden

Notes:

The Step Contract preserves the correct control boundary: mechanical checks,
AI semantic review, and SME approval are distinct. It does not approve IBM i
facts or business rules. It gives reviewers and orchestrators a shared status
and handoff vocabulary.

## Runtime Portability Review

- [x] canonical source under `skills/legacy-step-contract/`
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
| Filled inventory-pass contract | Reports all four sections and compact `pass` result | Passed in smoke |
| Inventory contract missing SME owner | Blocks execution and routes to SME owner assignment | Passed in smoke |
| User asks contract skill to produce inventory | Refuse and route to inventory skill | Covered |
| User asks contract skill to override SME | Refuse | Covered |
| Routing step before capability slug exists | Use `STEP-ROUTING-<NNN>` | Covered |

## Sign-Off

- Review Status: field-pilot ready
- Runtime Status: passed in Codex CLI, Claude Code, and OpenCode
- Remaining Work: optional maintainability cleanup only
