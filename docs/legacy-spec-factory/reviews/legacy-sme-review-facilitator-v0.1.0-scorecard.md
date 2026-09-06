---
skill: legacy-sme-review-facilitator
scorecard_version: v0.1.0
static_score: 9.55
decision: field-pilot ready
status: superseded
superseded_by: docs/reviews/legacy-sme-review-facilitator-v0.1.1-scorecard.md
last_verified: 2026-05-16
runtimes_tested:
  codex: { status: passed, model: gpt-5.4-mini, date: 2026-05-16 }
  claude_code: { status: passed, model: haiku, date: 2026-05-16 }
  opencode: { status: passed, model: minimax-m2.5-free, date: 2026-05-16 }
evidence_source: docs/runtime-matrix.md
---

# Skill Review Scorecard

## Metadata

- skill_name: `legacy-sme-review-facilitator`
- skill_path: `skills/legacy-sme-review-facilitator/`
- reviewed_version: `v0.1.0`
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

Static review score: **9.55 / 10**.

Current score after runtime smoke: **9.55 / 10**. The runtime cap is lifted
after positive and negative no-write smoke passed in Codex CLI, Claude Code,
and OpenCode on 2026-05-16.

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
| Purpose and trigger clarity | 10% | 9.6 | 0.96 |
| Workflow completeness | 12% | 9.6 | 1.15 |
| IBM i / domain correctness | 14% | 9.5 | 1.33 |
| Evidence and anti-hallucination | 12% | 9.8 | 1.18 |
| Output contract | 10% | 9.7 | 0.97 |
| Progressive disclosure | 8% | 9.3 | 0.74 |
| Runtime portability | 10% | 9.4 | 0.94 |
| Reviewability and testability | 10% | 9.7 | 0.97 |
| Engineering handoff value | 8% | 9.7 | 0.78 |
| Maintainability | 6% | 9.4 | 0.56 |

Final static score: **9.55 / 10**

Current score after runtime smoke: **9.55 / 10**

## Findings

### Blocking Findings

| ID | Severity | Finding | Required Change | Affects |
| --- | --- | --- | --- | --- |
| None |  |  |  |  |

### Fixed During Review

| ID | Finding | Change Made |
| --- | --- | --- |
| SME-FIX-001 | Decision outcome enum drifted across templates and references (`needs_revision`, `clarified`, `conditional`). | Normalized all decision outcomes to the contract enum and represented nuance through `suggested_revision`, notes, sign-off conditions, or `needs_more_evidence`. |
| SME-FIX-002 | Blocked review output referenced `blocked-findings.yaml`, but no template existed. | Added `templates/blocked-findings.yaml` and linked it from `SKILL.md`. |
| SME-FIX-003 | `REVIEW-*` and `FOLLOWUP-*` IDs were used without repo ID conventions. | Added `REVIEW` and `FOLLOWUP` prefixes to `docs/id-conventions.md`. |
| SME-FIX-004 | Contradiction examples used non-canonical `CONTRADICTION-*` IDs. | Changed contradiction review items to `FIND-*` with `item_type: contradiction`. |
| SME-FIX-005 | Example coverage was mostly narrative. | Added concrete positive, negative, and partial async example artifacts. |
| SME-FIX-006 | Follow-up priority was underspecified. | Added severity levels (`critical`, `high`, `medium`, `low`) to templates, examples, and workflow guidance. |
| SME-FIX-007 | Prior scorecard recommended `CHANGELOG.md`, which conflicts with this repo's skill minimalism rules. | Removed that recommendation; version history should live in review records and runtime matrix evidence. |
| SME-FIX-008 | Runtime smoke exposed portability edge cases: some runtimes lowercased capability slugs or inferred evidence redaction state too loosely. | Added explicit contract language requiring exact capability-slug preservation and explicit evidence `sensitivity` / `redaction_status`; synced adapters and reran smoke. |

### Remaining Improvement Findings

| ID | Finding | Suggested Change |
| --- | --- | --- |
| SME-IMPROVE-002 | Screen/report-specific SME review is represented by taxonomy, but not by a full example. | Add a later example involving DSPF screen behavior or PRTF/spool report review if pilot use cases require it. |

## SME Review

- [x] SME governance is explicit
- [x] Observed behavior, inferred rule, and modernization decision are separate
- [x] Evidence tags are required
- [x] IBM i-specific failure modes are covered
- [x] Open questions / TBDs are carried forward instead of hidden

Notes: The skill correctly treats SME judgment as the control point. It records
SME decisions without promoting rules or resolving TBDs on behalf of the owning
artifact skill.

## Runtime Portability Review

- [x] canonical source under `skills/<skill-name>/`
- [x] Claude Code adapter or copy defined if needed
- [x] OpenCode adapter or copy defined if needed
- [x] Codex adapter or copy defined if needed
- [x] runtime-specific metadata isolated from canonical skill

Notes: The skill uses only Markdown/YAML templates and references. No runtime
private folder convention is required in canonical instructions. Positive and
negative no-write smoke passed in Codex CLI (`gpt-5.4-mini`), Claude Code
(`haiku` with Read-only tools), and OpenCode (`opencode/minimax-m2.5-free`) on
2026-05-16.

## Requested Revision Prompt For Claude Code

```text
No blocking revision is required for repository acceptance or internal field
pilot.

If pilot feedback shows a need for more IBM i surface coverage, add one DSPF or
PRTF/spool SME review example.

Do not add top-level skill `README.md`, `CHANGELOG.md`, or other auxiliary
root documentation.
Keep the canonical skill under skills/legacy-sme-review-facilitator/.
Maintain compatibility with Codex, Claude Code, and OpenCode.
```
