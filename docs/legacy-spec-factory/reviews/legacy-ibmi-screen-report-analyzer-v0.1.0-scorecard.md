---
skill: legacy-ibmi-screen-report-analyzer
scorecard_version: v0.1.0
static_score: 9.38
decision: repo-ready
status: current
last_verified: 2026-05-16
runtimes_tested:
  codex: { status: passed, model: gpt-5.4-mini, date: 2026-05-16 }
  claude_code: { status: passed, model: haiku, date: 2026-05-16 }
  opencode: { status: passed, model: minimax-m2.5-free, date: 2026-05-16 }
evidence_source: docs/runtime-matrix.md
---

# Skill Review Scorecard

## Metadata

- skill_name: legacy-ibmi-screen-report-analyzer
- skill_path: skills/legacy-ibmi-screen-report-analyzer
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
| Workflow completeness | 12% | 9.2 | 1.10 |
| IBM i / domain correctness | 14% | 9.0 | 1.26 |
| Evidence and anti-hallucination | 12% | 9.6 | 1.15 |
| Output contract | 10% | 9.4 | 0.94 |
| Progressive disclosure | 8% | 9.3 | 0.74 |
| Runtime portability | 10% | 10.0 | 1.00 |
| Reviewability and testability | 10% | 9.4 | 0.94 |
| Engineering handoff value | 8% | 9.3 | 0.74 |
| Maintainability | 6% | 9.4 | 0.56 |

Final score: 9.38 / 10

## Decision Rule

- `>= 9.5`: field-pilot ready
- `9.0 - 9.4`: repo-ready, not field-pilot ready
- `8.0 - 8.9`: revise
- `< 8.0`: reject or rewrite

Decision: repo-ready, not field-pilot ready.

Smoke-test update (2026-05-16): Positive no-write DSPF scenario passed in
Codex CLI (`gpt-5.4-mini`), Claude Code (`haiku`), and OpenCode
(`opencode/minimax-m2.5-free`). Runtime-matrix row records the exact result.
Field-pilot readiness remains blocked by SME/domain validation and real
redacted DSPF/PRTF examples.

## Findings

### Blocking Findings

| ID | Severity | Finding | Required Change | Affects |
| --- | --- | --- | --- | --- |
| None | - | No mandatory stop condition remains after revision. | - | - |

### Improvement Findings

| ID | Finding | Suggested Change |
| --- | --- | --- |
| IMP-001 | Examples are toy examples, not shop-validated IBM i extracts. | Before field pilot, validate against at least one real redacted DSPF and one real redacted PRTF/spool bundle. |
| IMP-002 | Runtime portability is sync-checked but not smoke-tested through all agents. | Resolved on 2026-05-16; see `docs/runtime-matrix.md`. |
| IMP-003 | Domain reference is conservative but still should be reviewed by an IBM i SME. | Have an IBM i DSPF/PRTF SME review `references/dspf-screen-patterns.md` and `references/prtf-report-patterns.md`. |

## SME Review

- [x] SME governance is explicit
- [x] Observed behavior, inferred rule, and modernization decision are separate
- [x] Evidence tags are required
- [x] IBM i-specific failure modes are covered
- [x] Open questions / TBDs are carried forward instead of hidden

Notes: The revised skill now treats function-key labels, subfile behavior, and
report totals as evidence-scoped claims instead of inferring business behavior
from layout artifacts.

## Runtime Portability Review

- [x] canonical source under `skills/<skill-name>/`
- [x] Claude Code adapter or copy defined if needed
- [x] OpenCode adapter or copy defined if needed
- [x] Codex adapter or copy defined if needed
- [x] runtime-specific metadata isolated from canonical skill

Notes: A scoped `--skill` option was added to `scripts/sync-skills.sh` so this
skill can be synced without overwriting unrelated dirty runtime adapter copies.
Positive no-write smoke passed in Codex CLI, Claude Code, and OpenCode on
2026-05-16.

## Requested Revision Prompt For Claude Code

```text
Revise legacy-ibmi-screen-report-analyzer to reach field-pilot readiness.

Target score: 9.5/10.

Required changes:
- Validate DSPF and PRTF references with an IBM i SME.
- Add one real redacted DSPF example and one real redacted PRTF/spool example.
- Run a negative stop-condition smoke test through Codex, Claude Code, and OpenCode.

Do not remove author/copyright notices.
Keep the canonical skill under skills/legacy-ibmi-screen-report-analyzer/.
Maintain compatibility with Codex, Claude Code, and OpenCode.
```
