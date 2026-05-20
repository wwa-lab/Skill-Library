---
name: legacy-runtime-matrix-tester
description: Execute and validate runtime smoke tests for legacy spec factory skills across Codex, Claude Code, and OpenCode. Use when a new skill is added or an existing skill materially changes, and you need to verify portability and move it from `synced` to `passed` in docs/runtime-matrix.md.
license: Apache-2.0
metadata:
  author: Leo L Zhang
  maintainer: platform-engineering
  source: https://github.com/wwa-lab/legacy-spec-factory
  source_commit: 8871a6b
  domain: legacy-spec-factory
---

<!--
Legacy Spec Factory
Copyright 2026 Leo L Zhang

Original author: Leo L Zhang
License: Apache License 2.0

This skill is part of the Legacy Spec Factory project.
Retain this notice in substantial copies or derived versions.
-->

# Legacy Runtime Matrix Tester

## Purpose

Validate that legacy spec factory skills are discoverable, loadable, and functionally correct across all three target runtimes: Codex (CLI), Claude Code, and OpenCode. This skill orchestrates the smoke-test protocol defined in `docs/runtime-smoke-tests.md`, records the evidence, and updates `docs/runtime-matrix.md` with test results.

## Inputs

Accept:

- Skill name (e.g., `legacy-ibmi-inventory`, `legacy-spec-writer`)
- Target runtime(s) to test (all, codex, claude-code, opencode, or a specific subset)
- Optional: custom test prompt (if not using the canonical prompt from
  `docs/runtime-smoke-tests.md` or the target skill's `examples/`)
- Optional: run mode (discovery-only, execute, or full including negative-case)

Input readiness scoring:

- `0-5 blocked`: skill name missing or not in canonical `skills/`, target
  runtimes unspecified, sync drift detected, canonical examples/prompts missing
  with no override, or required runtime cannot be invoked.
- `6 minimum_pass`: canonical skill exists, target runtimes/run mode are clear,
  adapters are synced, and a positive prompt is available.
- `7-8 usable`: negative/adversarial prompt and version target are supplied.
- `9-10 strong`: expected pass criteria, prior runtime-matrix row, review
  scorecard context, and known runtime limitations are also supplied.
- Missing a custom prompt does not block when canonical smoke prompts exist;
  missing negative case may cap field-pilot readiness.

## Output Contract

Produce:

- `docs/runtime-matrix.md` (updated with test results and timestamp)
- `docs/reviews/<skill>-v<X>.<Y>.<Z>-scorecard.md` (new or updated review scorecard)
- Console report with:
  - Test phase results (discovery, trigger, optional adversarial)
  - Per-runtime status changes
  - Pass/fail criteria checklist
  - Recommended next actions
  - Blocking conditions (if any)

Use the templates in:

- `templates/runtime-matrix-entry.md`
- `templates/runtime-test-report.md`
- `templates/review-scorecard-template.md`

### Required Decision Rules

Use these rules in every console report, matrix recommendation, and scorecard
decision:

- If every target runtime is `passed`, no required negative case is missing,
  and no blocker is present, the scorecard decision is `field-pilot ready`.
  This is true in no-write/report-only mode too; the physical scorecard file
  does not need to exist yet for the recommendation to be field-pilot ready.
- If every target runtime is at least `loaded` or `executed`, but one or more
  runtime is not `passed`, the scorecard decision is `repo-ready` unless a
  required runtime failed.
- If any target runtime is `failed`, or a required negative case failed, the
  scorecard decision is `blocked`.
- A runtime blocked by credentials, login, network, or unavailable tooling is
  `synced`, not `passed` and not `executed`.
- Do not invent runtime statuses such as `blocked`. The only runtime matrix
  statuses are `not tested`, `synced`, `loaded`, `executed`, `passed`, and
  `failed`.
- If a requested target runtime cannot be exercised because of environment
  availability (credentials, login, network, or missing local runtime), keep
  that runtime's matrix status at `synced` when the adapter is present, set the
  smoke-run scorecard decision to `blocked`, and state that field-pilot
  readiness is blocked until that runtime is tested.
- Do not downgrade an all-`passed` evidence set to `repo-ready` because the
  previous matrix row was stale; the matrix recommendation describes the new
  tested state.
- The scorecard decision must be exactly one of: `repo-ready`,
  `field-pilot ready`, or `blocked`. Do not use `pass` or `passed` as a
  scorecard decision.

### Required Matrix Row Format

When asked for a matrix update, return a full Markdown table row with exactly
six cells matching `docs/runtime-matrix.md`:

```markdown
| `legacy-SKILL-NAME` | vX.Y.Z | passed | passed | passed | Notes with test date, runtime models, outcome, and scorecard path. |
```

The skill cell must be backtick-quoted. Do not add an overall status column.
Do not wrap the version or runtime status values in backticks. Runtime status
values must be lowercase exact enum values (`not tested`, `synced`, `loaded`,
`executed`, `passed`, or `failed`). The notes cell must include the test date,
runtime models, outcome summary, and scorecard path.

The scorecard path is always:

```text
docs/reviews/legacy-SKILL-NAME-vX.Y.Z-scorecard.md
```

Do not return the template path as the scorecard location.

For an all-passed evidence set, the minimum valid answer is:

```markdown
- scorecard decision: `field-pilot ready`
- updated runtime matrix row: | `legacy-SKILL-NAME` | vX.Y.Z | passed | passed | passed | Positive and negative no-write smoke passed on YYYY-MM-DD. Codex CLI (...), Claude Code (...), and OpenCode (...) all invoked `/legacy-SKILL-NAME`. See docs/reviews/legacy-SKILL-NAME-vX.Y.Z-scorecard.md. |
```

Follow:

- `../../../docs/legacy-spec-factory/runtime-smoke-tests.md`
- `../../../docs/legacy-spec-factory/skill-review-gate.md`
- `references/test-execution-protocol.md`

Examples:

- `examples/happy-path-new-skill/`
- `examples/negative-case-portability-blocker/`

## Step Contract

This skill conforms to the canonical Step Contract shape - see
`../legacy-step-contract/SKILL.md` and
`../legacy-step-contract/references/step-contract.md` for the full
field-level rules.

### Input

- **Required**: skill name (must exist under `skills/<skill-name>/SKILL.md` in
  the canonical source), list of runtimes to test (codex, claude-code,
  opencode, or all), run mode (discovery, execute, or full), target skill
  version to test (defaults to latest in canonical source).
- **Optional**: custom test prompt (if no canonical prompt exists in
  `docs/runtime-smoke-tests.md` or the target skill's examples, or if the user
  wants to override); negative-case prompt (if testing adversarial blocking).
- **Input readiness scoring**: apply
  `../../../docs/legacy-spec-factory/input-readiness-rubric.md`; canonical prompts satisfy minimum
  pass, while negative cases and prior scorecard context raise confidence.
- **Readiness checks**: Skill exists under `skills/`; skill version is not
  yet marked as `passed` in all target runtimes in `runtime-matrix.md`;
  `scripts/sync-skills.sh --skill <skill-name> --target all --check` exits
  0; canonical `SKILL.md` matches the synced adapter copies.
- **Stop conditions**: Skill does not exist in canonical source; skill is
  already at `passed` for all target runtimes (run diagnostics instead);
  skill's `examples/` folder is missing canonical test prompts and no
  override is provided; a pre-test check fails (sync drift, contract
  validation, or canonical changes that have not been synced to adapters).

### Execution

- **Procedure**: see the Workflow section below (9 ordered steps).
- **Allowed inference**: interpreting test output against the pass criteria;
  updating matrix status based on runtime discovery/execution; assigning
  review scorecard scores based on outcomes.
- **Forbidden assumptions**: inventing test results; marking a skill as
  `passed` if a negative-case or blocking scenario was not tested; assuming
  a timeout or credential error is a `passed` (record as `synced` with issue
  notes instead); reporting success in one runtime as success in all.
- **Handling gaps**: If a runtime cannot be tested (e.g., Claude Code missing
  login), record status as `synced` with blockers documented in the review
  scorecard. Do not force-mark as `passed`.

### Output

- **Canonical artifacts**:
  - `docs/runtime-matrix.md` (updated row with status, version, date, notes)
  - `docs/reviews/<skill>-v<X>.<Y>.<Z>-scorecard.md` (updated or new)
- **Optional shared artifact**:
  - `docs/runtime-smoke-tests.md` (updated only when the target skill lacks
    canonical reusable smoke prompts)
- **Required fields/sections in scorecard**:
  - Skill name and version
  - Pre-test checks (sync, contract, source state)
  - Per-runtime test results (discovery, trigger, adversarial if applicable)
  - Final gateway score and decision (repo-ready, field-pilot ready, or
    blocked)
  - Action items for next revision
  - Date of test execution
- **Handoff status**: After a `passed` in all target runtimes, the skill is
  eligible to move from 9.0 ("portability not tested") to 9.5+
  ("field-pilot ready") in the skill review gate scoring.

### Validation

- **Mechanical**: runtime matrix row syntax is valid YAML/Markdown; scorecard
  has all required headers; pre-test checks recorded (not assumed); test
  prompts are documented in `examples/` or overridden in full.
- **Functional**: adapter copies exist and frontmatter/description load
  without error; trigger prompt fires the correct skill (not a sibling);
  output follows the declared output contract; no files are created or edited
  during the target skill's no-write smoke test; negative-case scenarios
  correctly block with gate/router explanations.
- **Process**: `docs/runtime-matrix.md` is updated in the same PR or commit
  as the skill; scorecard decision aligns with pre-test checks and test
  results; review timestamps are recorded.

Emit a Step Validation Report (see
`../legacy-step-contract/templates/step-validation-report.md`) with status
`pass`, `pass_with_warnings`, or `blocked` when reporting upward to the
orchestrator.

## Workflow

1. **Verify skill and input readiness**
   Confirm the skill exists under `skills/` and is not already at `passed` in
   all target runtimes. Validate that the user has provided or that the
   canonical source supplies test prompts. If the skill is already
   fully-tested, offer to re-run diagnostics instead.

2. **Run pre-test checks**
   - `scripts/sync-skills.sh --skill <skill-name> --target all --check` must
     exit 0 (no drift for the target skill)
   - `python3 scripts/check-spec-contract.py` (if the skill touches
     `spec.yaml` shape)
   - Confirm canonical `SKILL.md` has been synced to the adapter copies that
     will be tested
   - Record outcomes in the scorecard

3. **Create or update scorecard**
   Create a new `docs/reviews/<skill>-v<X>.<Y>.<Z>-scorecard.md` or update
   an existing one. Record:
   - Skill name, version, and test date
   - Pre-test check results
   - Stub entries for per-runtime tests (will fill in during Phase 2)
   - Target completion date and reviewer identity

4. **Execute Phase 1 - Discovery (per runtime)**
   For each target runtime (codex, claude-code, opencode):
   - Verify the synced adapter path exists for that runtime
   - Verify the skill's frontmatter and description are readable
   - If the runtime exposes an interactive skill list, verify the skill appears
     there; otherwise treat the Phase 2 trigger as the runtime-load proof
   - Check for frontmatter or path errors in the runtime output
   - Record: `loaded` if successful, `failed` if the skill does not appear or
     errors on load

5. **Execute Phase 2 - Trigger (per runtime)**
   For each runtime that achieved `loaded`:
   - Use the canonical test prompt from `docs/runtime-smoke-tests.md`, the
     target skill's `examples/`, or the override provided
   - Invoke the runtime with the prompt
   - Verify the skill fires (not a sibling skill)
   - Check that output follows the declared output contract
   - Verify no files are created or edited during the test
   - Record: `executed` if the skill ran and produced output, `passed` if
     output meets all declared pass criteria

6. **Execute Phase 3 - Adversarial (per runtime, optional)**
   For each runtime that achieved `executed`, if a negative-case example
   exists:
   - Use the negative-case prompt from `docs/runtime-smoke-tests.md`, the
     target skill's `examples/`, or the override provided
   - Verify the skill blocks or refuses correctly
   - Verify the router calls out gate failure with explanation
   - Record: `passed` if both positive and required negative cases pass, or
     `executed` if the positive case passes but a required negative case was
     skipped or incomplete

7. **Update runtime matrix**
   Edit `docs/runtime-matrix.md`:
   - Bump the canonical version column to match the tested version
   - Update each runtime's status column with the highest status reached
   - Add a Notes cell with the exact runtime + model used, test date, and any
     blocking issues
   - Ensure the entry follows the table's format (piped columns, no orphaned
     notes)

8. **Finalize scorecard**
   Complete the scorecard:
   - Record all per-runtime results
   - Calculate gateway score based on skill-review-gate.md rubric (if this is
     the tester's role or if scorecard-generation help is available)
   - Update decision: `repo-ready` (all runtimes at `synced` or `loaded`),
     `field-pilot ready` (all runtimes at `passed`), or
     `blocked` (any runtime at `failed` or missing required scenario)
   - Sign off with tester identity and date

9. **Produce test report**
   Generate a human-readable summary:
   - Skill name and version
   - Per-runtime results (discovery, trigger, adversarial)
   - Pass/fail checklist
   - Recommended next actions
   - Blockers (if any) that must be resolved before field pilot
   - Link to updated scorecard and matrix entry

## Workflow State Write-Back (history only, not capability-scoped)

This is a meta / runtime-compatibility skill. It tests skill portability
across Codex / Claude Code / OpenCode and does NOT operate on a project's
business capabilities. It does NOT mutate `capabilities[]` or
`current_focus`.

If the project happens to have a `<project-root>/workflow-state.yaml`,
append one `history[]` entry per
[`docs/workflow-state-contract.md`](../../../docs/legacy-spec-factory/workflow-state-contract.md):

```yaml
history:
  - at: <ISO 8601>
    skill: legacy-runtime-matrix-tester
    capability_id: null
    stage_after: null
    artifact: docs/runtime-matrix.md
    note: "runtime smoke test — <skill-name> on <runtime>: pass | fail"
```

Also overwrite `project.last_updated_at` / `project.last_updated_by`.

If `workflow-state.yaml` does not exist, this skill does NOT create it —
runtime testing is a developer activity, not part of project-level
modernization state.

## Anti-Hallucination Rules

**Test results are ground truth.** Do not:

- Report a skill as `passed` unless the skill was actually invoked and
  produced output in the target runtime
- Assume one runtime's success carries over to another
- Mark a skill as `passed` if a required negative-case test was not run
- Invent test output or pretend a timeout is success
- Modify a target skill during the smoke execution phase to chase a passing
  result. If the user explicitly asked for review/fix, complete the revision
  first, sync adapters, then start or restart the smoke test and record the
  revised source state.

If a runtime cannot be tested due to missing credentials, environment setup,
or runtime unavailability, record the runtime as `synced` and document the
blocker in the scorecard. Do not force-mark as `passed`.

## Test Prompts and Pass Criteria

See `docs/runtime-smoke-tests.md` for the canonical test prompts for each
skill. A target skill may also provide prompts under its own `examples/`
folder. Prefer the shared smoke document when both exist.

- `examples/<scenario>/prompt.txt` - canonical positive or negative prompt
- `examples/<scenario>/expected-output.md` - measurable expected shape

If a skill does not yet have test prompts in `examples/`, this skill's user
must provide them, and the user is responsible for documenting them so the
test can be repeated consistently.

## Runtime Portability

The canonical skill source lives under:

```text
skills/legacy-runtime-matrix-tester/SKILL.md
```

Runtime copies may be synced to:

```text
.claude/skills/legacy-runtime-matrix-tester/SKILL.md
.opencode/skills/legacy-runtime-matrix-tester/SKILL.md
.agents/skills/legacy-runtime-matrix-tester/SKILL.md
.codex/skills/legacy-runtime-matrix-tester/SKILL.md
```

Use `../../../scripts/legacy-spec-factory/sync-skills.sh` to create or check runtime copies.

## Version History

- v0.1.0 (2026-05-16): Initial runtime matrix tester with per-skill sync
  checks, discovery/trigger/adversarial workflow, examples, templates, and
  output contract for matrix and scorecard updates. Passed positive and
  negative no-write smoke in Codex CLI (`gpt-5.4-mini`), Claude Code
  (`haiku`), and OpenCode (`opencode/minimax-m2.5-free`).
