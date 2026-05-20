# Calibration Scorecard: 9.5 Field-Pilot Ready

> **Hypothetical snapshot.** This document calibrates what a 9.5 score would
> look like for `legacy-ibmi-inventory` **after** all three target runtimes
> have been load- and execution-validated. It is not the current score.
>
> The current actual score for this skill is **9.0**, capped on runtime
> validation. See
> [docs/reviews/legacy-ibmi-inventory-v0.1.0-scorecard.md](../reviews/legacy-ibmi-inventory-v0.1.0-scorecard.md)
> for the authoritative review record.
>
> Do not cite this file as evidence that the skill has reached field-pilot
> status.

## Metadata

- skill_name: legacy-ibmi-inventory
- skill_path: skills/legacy-ibmi-inventory
- reviewed_version: example validated revision
- generated_by: Claude Code
- reviewed_by: Codex
- review_date: 2026-05-13
- target_runtime:
  - [x] Codex
  - [x] Claude Code
  - [x] OpenCode
- decision:
  - [ ] reject
  - [ ] revise
  - [ ] repo-ready
  - [x] field-pilot ready

## Weighted Score

| Category | Weight | Score | Weighted |
| --- | ---: | ---: | ---: |
| Purpose and trigger clarity | 10% | 9.5 | 0.95 |
| Workflow completeness | 12% | 9.5 | 1.14 |
| IBM i / domain correctness | 14% | 9.5 | 1.33 |
| Evidence and anti-hallucination | 12% | 9.5 | 1.14 |
| Output contract | 10% | 9.5 | 0.95 |
| Progressive disclosure | 8% | 9.5 | 0.76 |
| Runtime portability | 10% | 9.5 | 0.95 |
| Reviewability and testability | 10% | 9.5 | 0.95 |
| Engineering handoff value | 8% | 9.5 | 0.76 |
| Maintainability | 6% | 9.5 | 0.57 |

Final score: **9.5 / 10**

## Why This Is 9.5

- Clear trigger and non-goals.
- Explicit output contract and templates.
- SME review is built into the workflow.
- Evidence, sensitivity, and TBD handling are mandatory.
- Runtime portability is addressed with canonical source plus sync script.
- The skill stays focused on inventory and does not collapse into rule mining
  or spec writing.

## Remaining Risk

This score assumes the skill is tested in all three runtimes after sync. If no
runtime validation has happened, cap at 9.0.

## Category Calibration

| Category | What Makes This 9.5 |
| --- | --- |
| Purpose and trigger clarity | The skill says exactly when to use it and explicitly excludes rule mining and Java generation. |
| Workflow completeness | The workflow moves from scope to evidence classification, object inventory, relationships, gaps, SME review, and gate decision. |
| IBM i / domain correctness | It covers programs, CL flow, PF/LF, DSPF, PRTF, spool, data areas, data queues, message queues, copybooks, and jobs. |
| Evidence and anti-hallucination | Missing artifacts become TBDs; object names and calls cannot be invented. |
| Output contract | `inventory.yaml`, `object-map.md`, and review checklist are defined with templates and examples. |
| Progressive disclosure | Core procedure stays in `SKILL.md`; detailed structure lives in references/templates/examples. |
| Runtime portability | Canonical source syncs cleanly to Codex, Claude Code, and OpenCode adapters and has a recorded runtime matrix. |
| Reviewability and testability | Positive and negative examples show expected gate behavior. |
| Engineering handoff value | Output is specific enough for the next analyzer to consume without re-discovering scope. |
| Maintainability | Authorship, version history, ID conventions, and sync rules are explicit. |
