# Skill Review Scorecard

## Metadata

- skill_name:
- skill_path:
- reviewed_version:
- generated_by:
- reviewed_by:
- review_date:
- target_runtime:
  - [ ] Codex
  - [ ] Claude Code
  - [ ] OpenCode
- decision:
  - [ ] reject
  - [ ] revise
  - [ ] repo-ready
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
| Purpose and trigger clarity | 10% |  |  |
| Workflow completeness | 12% |  |  |
| IBM i / domain correctness | 14% |  |  |
| Evidence and anti-hallucination | 12% |  |  |
| Output contract | 10% |  |  |
| Progressive disclosure | 8% |  |  |
| Runtime portability | 10% |  |  |
| Reviewability and testability | 10% |  |  |
| Engineering handoff value | 8% |  |  |
| Maintainability | 6% |  |  |

Final score:

## Decision Rule

- `>= 9.5`: field-pilot ready
- `9.0 - 9.4`: repo-ready, not field-pilot ready
- `8.0 - 8.9`: revise
- `< 8.0`: reject or rewrite

## Findings

### Blocking Findings

| ID | Severity | Finding | Required Change | Affects |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

### Improvement Findings

| ID | Finding | Suggested Change |
| --- | --- | --- |
|  |  |  |

## SME Review

- [ ] SME governance is explicit
- [ ] Observed behavior, inferred rule, and modernization decision are separate
- [ ] Evidence tags are required
- [ ] IBM i-specific failure modes are covered
- [ ] Open questions / TBDs are carried forward instead of hidden

Notes:

## Runtime Portability Review

- [ ] canonical source under `skills/<skill-name>/`
- [ ] Claude Code adapter or copy defined if needed
- [ ] OpenCode adapter or copy defined if needed
- [ ] Codex adapter or copy defined if needed
- [ ] runtime-specific metadata isolated from canonical skill

Notes:

## Requested Revision Prompt For Claude Code

```text
Revise <skill_name> to address the following review findings.

Target score: 9.5/10.

Blocking issues:
1.
2.
3.

Required changes:
-
-
-

Do not remove author/copyright notices.
Keep the canonical skill under skills/<skill-name>/.
Maintain compatibility with Codex, Claude Code, and OpenCode.
```

