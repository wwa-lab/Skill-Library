---
skill: legacy-traceability-packager
scorecard_version: v0.1.1
static_score: 9.51
decision: field-pilot ready
status: current
last_verified: 2026-05-16
runtimes_tested:
  codex: { status: passed, model: gpt-5.4-mini, date: 2026-05-16 }
  claude_code: { status: passed, model: haiku, date: 2026-05-16 }
  opencode: { status: passed, model: minimax-m2.5-free, date: 2026-05-16 }
evidence_source: docs/runtime-matrix.md
---

# Skill Review Scorecard: legacy-traceability-packager v0.1.1

## Metadata

- skill_name: `legacy-traceability-packager`
- skill_path: `skills/legacy-traceability-packager/`
- reviewed_version: `v0.1.1`
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
  - [x] field-pilot ready

Static review score: **9.51 / 10**.

Current score after runtime cap: **9.51 / 10**. The three-runtime smoke
protocol passed in Codex, Claude Code, and OpenCode and is recorded in
`docs/runtime-matrix.md`.

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

No mandatory stop conditions apply.

## Weighted Score

| Category | Weight | Score | Weighted |
| --- | ---: | ---: | ---: |
| Purpose and trigger clarity | 10% | 9.7 | 0.97 |
| Workflow completeness | 12% | 9.5 | 1.14 |
| IBM i / domain correctness | 14% | 9.4 | 1.32 |
| Evidence and anti-hallucination | 12% | 9.7 | 1.16 |
| Output contract | 10% | 9.6 | 0.96 |
| Progressive disclosure | 8% | 9.4 | 0.75 |
| Runtime portability | 10% | 9.3 | 0.93 |
| Reviewability and testability | 10% | 9.5 | 0.95 |
| Engineering handoff value | 8% | 9.6 | 0.77 |
| Maintainability | 6% | 9.4 | 0.56 |

Final static score: **9.51 / 10**

Current score: **9.51 / 10** after runtime smoke execution evidence.

## Findings

### Blocking Findings

| ID | Severity | Finding | Required Change | Affects |
| --- | --- | --- | --- | --- |
| None |  |  |  |  |

### Fixed During Review

| ID | Finding | Change Made |
| --- | --- | --- |
| TRACE-FIX-001 | `PKG-*` package IDs were minted by the skill but were absent from `docs/id-conventions.md`, making the skill fail its own ID-format discipline. | Added `SPEC` and `PKG` prefixes to `docs/id-conventions.md`; changed blocked attempts to use valid `package_id` plus `attempt_number`. |
| TRACE-FIX-002 | The positive example claimed `pass` while also carrying a `NON-BLOCKING-TBD` info finding; this contradicted the status table. | Defined `pass` as zero blocking/warning/info findings and moved open TBDs to `pass_with_warnings`; removed the open TBD from the positive example. |
| TRACE-FIX-003 | `templates/traceability-package.yaml` classified `BR-CREDIT-CHECK-002` as `knowledge_type: observed_behavior`. | Corrected the business rule coverage row to `knowledge_type: inferred_business_rule`. |
| TRACE-FIX-004 | The review checklist required every `AC-*` to validate exactly one BR, which is stricter than the spec schema and valid multi-rule AC patterns. | Changed the rule to "at least one existing, approved `BR-*`" with waiver handling. |
| TRACE-FIX-005 | The workflow said blocking findings do not short-circuit, while blocked examples marked later gates `not_evaluated`. | Clarified that the packager continues only when later checks are safe and reliable; otherwise later gates are explicitly `not_evaluated`. |
| TRACE-FIX-006 | The deferral predicate used "future date", which becomes stale in fixed examples. | Defined the check relative to the package audit date. |
| TRACE-FIX-007 | Runtime adapter copies were incomplete/drifted from canonical source. | Ran `scripts/sync-skills.sh --skill legacy-traceability-packager` and verified all four adapter copies with `--check`. |
| TRACE-FIX-008 | Three-runtime smoke had not been executed or recorded. | Added positive and negative smoke prompts to `docs/runtime-smoke-tests.md`, executed them in Codex CLI, Claude Code, and OpenCode, and recorded the passing result in `docs/runtime-matrix.md`. |

### Remaining Improvement Findings

| ID | Finding | Suggested Change |
| --- | --- | --- |
| TRACE-IMPROVE-002 | Examples are lightweight and measurable but still not full end-to-end input packages. | Add a fuller fixture only if pilot reviewers need runnable sample input trees. |

## SME Review

- [x] SME governance is explicit
- [x] Observed behavior, inferred rule, and modernization decision are separate
- [x] Evidence tags are required
- [x] IBM i-specific failure modes are covered
- [x] Open questions / TBDs are carried forward instead of hidden

Notes: The skill is an audit and packaging gate. It routes findings to owning
skills and does not resolve rules, evidence, acceptance criteria, decisions, or
TBDs on behalf of SMEs.

## Runtime Portability Review

- [x] canonical source under `skills/<skill-name>/`
- [x] Claude Code adapter or copy defined if needed
- [x] OpenCode adapter or copy defined if needed
- [x] Codex adapter or copy defined if needed
- [x] runtime-specific metadata isolated from canonical skill

Notes: Canonical source was synced to `.claude/skills/`, `.opencode/skills/`,
`.agents/skills/`, and `.codex/skills/` using `scripts/sync-skills.sh`.
Positive and negative no-write smoke passed in Codex CLI, Claude Code, and
OpenCode on 2026-05-16.

## Verification

```text
ruby -e 'require "yaml"; ARGV.each { |f| YAML.load_file(f); puts "OK #{f}" }' \
  skills/legacy-traceability-packager/templates/traceability-package.yaml \
  skills/legacy-traceability-packager/templates/blocking-findings.yaml \
  skills/legacy-traceability-packager/examples/traceability-blocked-dangling-id/blocking-findings.yaml \
  skills/legacy-traceability-packager/examples/traceability-warning-deferred-tbd/gate-summary.yaml

scripts/sync-skills.sh --skill legacy-traceability-packager --check
git diff --check -- docs/id-conventions.md skills/legacy-traceability-packager \
  .claude/skills/legacy-traceability-packager \
  .opencode/skills/legacy-traceability-packager \
  .agents/skills/legacy-traceability-packager \
  .codex/skills/legacy-traceability-packager

Runtime smoke, 2026-05-16:
- Codex CLI (`gpt-5.4-mini`, read-only ephemeral): positive `pass`; negative
  `blocked` with route to `legacy-spec-writer`.
- Claude Code (`haiku`, `Read` tool only): positive `pass`; negative `blocked`
  with forbidden new `BR-*` creation.
- OpenCode (`minimax-m2.5-free`): positive `pass`; negative `blocked` with
  only `traceability-review.md` and `blocking-findings.yaml` writable.
```

## Requested Revision Prompt For Claude Code

```text
No blocking revision is required for repository acceptance.

For the next hardening pass, add a fuller positive fixture tree only if pilot
reviewers need executable fixture coverage. Do not add skill-local README.md or
CHANGELOG.md files.

Do not remove author/copyright notices.
Keep the canonical skill under skills/legacy-traceability-packager/.
Maintain compatibility with Codex, Claude Code, and OpenCode.
```
