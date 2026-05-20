---
skill: legacy-runtime-matrix-tester
scorecard_version: v0.1.0
static_score: 9.56
decision: field-pilot ready
status: current
last_verified: 2026-05-16
runtimes_tested:
  codex: { status: passed, model: gpt-5.4-mini, date: 2026-05-16 }
  claude_code: { status: passed, model: haiku, date: 2026-05-16 }
  opencode: { status: passed, model: minimax-m2.5-free, date: 2026-05-16 }
evidence_source: docs/runtime-matrix.md
---

# Skill Review Scorecard: legacy-runtime-matrix-tester v0.1.0

## Metadata

- skill_name: `legacy-runtime-matrix-tester`
- skill_path: `skills/legacy-runtime-matrix-tester/`
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
  - [ ] repo-ready
  - [x] field-pilot ready

## Review Evidence

- Reviewed against `docs/skill-review-gate.md`, `docs/runtime-matrix.md`,
  `docs/runtime-smoke-tests.md`, repository `AGENTS.md`, and
  `scripts/sync-skills.sh` behavior.
- Checked canonical source under `skills/legacy-runtime-matrix-tester/`.
- Fixed contract drift around runtime discovery, per-skill sync checks,
  unavailable runtime handling, scorecard decisions, and matrix-row formatting.
- Synced canonical source to `.claude/skills/`, `.opencode/skills/`,
  `.agents/skills/`, and `.codex/skills/`.
- Ran:
  - `scripts/sync-skills.sh --skill legacy-runtime-matrix-tester --target all --check`
  - `python3 scripts/check-spec-contract.py`
  - YAML frontmatter parse for canonical and adapter `SKILL.md` files
  - `git diff --check`
- Ran positive and negative no-write runtime smoke tests in Codex CLI
  (`gpt-5.4-mini`, read-only ephemeral), Claude Code (`haiku`, Read-only
  tools), and OpenCode (`opencode/minimax-m2.5-free`) on 2026-05-16.

## Mandatory Stop Conditions

No mandatory 8.0 cap conditions found.

The runtime-execution cap is lifted. The synced skill was loaded and used
successfully in Codex, Claude Code, and OpenCode with the same positive and
negative no-write scenarios on 2026-05-16.

## Weighted Score

| Category | Weight | Score | Weighted | Notes |
| --- | ---: | ---: | ---: | --- |
| Purpose and trigger clarity | 10% | 9.7 | 0.97 | Trigger cases are explicit for matrix updates, scorecard creation, and runtime blockers. |
| Workflow completeness | 12% | 9.6 | 1.15 | Covers pre-test checks, discovery, trigger, adversarial cases, matrix updates, and scorecard decisions. |
| IBM i / domain correctness | 14% | 9.4 | 1.32 | Governance fits the Legacy Spec Factory chain and keeps SME/evidence gates visible without owning domain conclusions. |
| Evidence and anti-hallucination | 12% | 9.7 | 1.16 | Negative smoke proves unavailable runtimes are not upgraded to `passed` and field-pilot readiness stays blocked. |
| Output contract | 10% | 9.7 | 0.97 | Matrix row, report, and scorecard outputs are concrete, bounded, and enum-driven. |
| Progressive disclosure | 8% | 9.3 | 0.74 | `SKILL.md` stays readable while detailed rules live in references and templates. |
| Runtime portability | 10% | 9.8 | 0.98 | Canonical and adapter copies sync cleanly and execute in all target runtimes. |
| Reviewability and testability | 10% | 9.7 | 0.97 | Positive and negative examples expose the main false-pass risks. |
| Engineering handoff value | 8% | 9.5 | 0.76 | Produces exactly the evidence downstream maintainers need to trust runtime matrix status. |
| Maintainability | 6% | 9.0 | 0.54 | Good current structure; future versions could add a small command wrapper for repeatable local smoke runs. |

Final score before cap: **9.56 / 10**

Final score after runtime-execution cap: **9.56 / 10**

Decision: **field-pilot ready**

## Findings Resolved In This Review

| ID | Severity | Finding | Fix |
| --- | --- | --- | --- |
| RTM-REV-001 | High | Pre-test guidance used whole-repo sync drift, which is brittle in dirty worktrees. | Required `scripts/sync-skills.sh --skill <name> --target all --check`. |
| RTM-REV-002 | High | Discovery depended on runtime-specific list commands that are not portable or available in every runtime. | Reframed discovery as adapter presence plus runtime invocation confirmation. |
| RTM-REV-003 | High | Unavailable runtimes could be confused with `passed` or invented blocked matrix statuses. | Required synced adapters to remain `synced` when auth/network/tooling blocks execution; scorecard becomes `blocked`. |
| RTM-REV-004 | Medium | Matrix-row formatting was underspecified. | Required exactly six cells, backticked skill name, unbackticked version/status cells, lowercase enum statuses, and dated model/path notes. |
| RTM-REV-005 | Medium | Positive-only smoke could mark a runtime `passed` while negative gates were untested. | Required negative-case success before using runtime status `passed` when a negative prompt exists. |

## Runtime Execution Evidence

| Runtime | Model | Positive No-Write Smoke | Negative No-Write Smoke | Result |
| --- | --- | --- | --- | --- |
| Codex CLI | `gpt-5.4-mini` | Returned a six-cell matrix row with lowercase statuses, `field-pilot ready` scorecard decision, scorecard path, and no-write confirmation. | Kept unavailable Claude Code at `synced`, refused false `passed`, marked the smoke run `blocked`, and confirmed no writes. | Passed |
| Claude Code | `haiku` with Read-only tools | Returned a six-cell matrix row with lowercase statuses, `field-pilot ready` scorecard decision, scorecard path, and no-write confirmation. | Kept unavailable Claude Code at `synced`, returned `blocked`, and blocked field pilot until auth is fixed. | Passed |
| OpenCode | `opencode/minimax-m2.5-free` | Returned a six-cell matrix row with lowercase statuses, `field-pilot ready` scorecard decision, scorecard path, and no-write confirmation. | Kept unavailable Claude Code at `synced`, returned `blocked`, and blocked field pilot until auth is fixed. | Passed |

Codex emitted unrelated warnings for a user-home skill with invalid
frontmatter and a plugin-cache 403, but `/legacy-runtime-matrix-tester` loaded
and executed correctly.

## Runtime Portability Review

- [x] canonical source under `skills/<skill-name>/`
- [x] Claude Code adapter copy synced
- [x] OpenCode adapter copy synced
- [x] Codex adapter copy synced
- [x] runtime-specific metadata absent from canonical skill

Notes:

`scripts/sync-skills.sh --skill legacy-runtime-matrix-tester --target all --check`
passes after sync. Runtime smoke proves the synced copies can be loaded and
used by Codex, Claude Code, and OpenCode.

## Remaining Post-Pilot Improvements

| ID | Severity | Finding | Suggested Change |
| --- | --- | --- | --- |
| RTM-IMPROVE-001 | Low | The smoke commands are documented but not wrapped in a helper script. | Add a thin optional script only if repeated manual runs become error-prone. |

## Recommendation

The skill is ready for field pilot. It is deliberately conservative around
runtime evidence and blocks readiness when one target runtime cannot be
executed, which is the right failure mode for this governance step.
