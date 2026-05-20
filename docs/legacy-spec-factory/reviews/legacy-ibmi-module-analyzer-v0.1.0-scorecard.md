---
skill: legacy-ibmi-module-analyzer
scorecard_version: v0.1.0
static_score: 9.15
decision: repo-ready
status: superseded
superseded_by: v0.1.1
---

# Skill Review Scorecard: legacy-ibmi-module-analyzer v0.1.0

## Metadata

- skill_name: legacy-ibmi-module-analyzer
- skill_path: skills/legacy-ibmi-module-analyzer
- reviewed_version: v0.1.0
- generated_by: Codex
- reviewed_by: Codex
- review_date: 2026-05-14
- target_runtime:
  - [x] Codex
  - [x] Claude Code
  - [x] OpenCode
- decision:
  - [ ] reject
  - [ ] revise
  - [x] repo-ready
  - [ ] field-pilot ready

## Review Evidence

- Reviewed against `docs/skill-review-gate.md`.
- Checked canonical source under `skills/legacy-ibmi-module-analyzer/`.
- Checked `SKILL.md`, templates, references, positive example, and negative
  incomplete-module example.
- Checked `docs/module-analysis-model.md`, `docs/code-as-ground-truth.md`,
  `docs/evidence-and-knowledge-taxonomy.md`, and `docs/id-conventions.md` for
  model and evidence alignment.
- Ran `scripts/sync-skills.sh --target all --check`; all runtime adapter copies
  reported `OK`.
- Checked `docs/runtime-matrix.md`; all target runtimes are still `synced`, not
  `loaded`, `executed`, or `passed`.
- Checked `docs/runtime-smoke-tests.md`; positive and negative
  `legacy-ibmi-module-analyzer` smoke prompts now exist. Execution results in
  Codex CLI, Claude Code, and OpenCode are still pending.

## Mandatory Stop Conditions

No mandatory 8.0 cap conditions found.

A 9.0 cap applies under the review gate:

- portability has been considered and adapter drift has been checked, but the
  skill has not been loaded or executed in Codex CLI, Claude Code, and OpenCode
- the runtime-smoke-test prompt set exists, but no three-runtime pass evidence
  has been recorded yet

## Weighted Score

| Category | Weight | Score | Weighted |
| --- | ---: | ---: | ---: |
| Purpose and trigger clarity | 10% | 9.6 | 0.96 |
| Workflow completeness | 12% | 9.2 | 1.10 |
| IBM i / domain correctness | 14% | 9.3 | 1.30 |
| Evidence and anti-hallucination | 12% | 9.4 | 1.13 |
| Output contract | 10% | 8.9 | 0.89 |
| Progressive disclosure | 8% | 8.7 | 0.70 |
| Runtime portability | 10% | 9.0 | 0.90 |
| Reviewability and testability | 10% | 9.1 | 0.91 |
| Engineering handoff value | 8% | 9.2 | 0.74 |
| Maintainability | 6% | 8.8 | 0.53 |

Final score before cap: **9.15 / 10**

Final score after cap: **9.0 / 10**

Decision: **repo-ready, not field-pilot ready**

## Findings

### Blocking For 9.5

| ID | Severity | Finding | Required Change | Affects |
| --- | --- | --- | --- | --- |
| MOD-REV-001 | High | Runtime portability is structurally clean but not tested. | Smoke prompts and pass criteria now exist in `docs/runtime-smoke-tests.md`; run the protocol in Codex CLI, Claude Code, and OpenCode, then update `docs/runtime-matrix.md` and this scorecard. | Runtime portability, reviewability |
| MOD-REV-002 | High | `SKILL.md` pointed to nonexistent per-view methodology files and a wildcard template. | ✅ Resolved. Workflow now points to existing `references/output-contract.md`, `references/synthesis-rules.md`, and `templates/view-template.md`; adapter drift check should remain clean after sync. | Progressive disclosure, maintainability, runtime portability |
| MOD-REV-003 | Medium | Blocked-module status was inconsistent across contract and templates. | ✅ Resolved. Blocked statuses are now listed in the output contract, module overview template, and view template. | Output contract, downstream automation |
| MOD-REV-004 | Medium | Evidence traceability was asserted but not enforceable enough in the artifact contract. | Partially resolved. The output contract now requires evidence references in per-view tables; a final field-pilot rescore should verify whether this is strict enough for every claim type. | Evidence integrity, SME correctness, downstream automation |
| MOD-REV-005 | Medium | Per-view review checklists were not fully materialized. | ✅ Resolved. `references/output-contract.md` now contains measurable per-view checklist sections and the view template points to them. | Reviewability, SME governance |

### Strengths

- The skill has a clear layer boundary: it synthesizes approved inventory,
  program analyses, flow analyses, and BAU notes instead of re-analyzing code.
- The four-view model is well aligned with `docs/module-analysis-model.md` and
  separates business, system, program, and data concerns cleanly.
- Stop conditions are strong: missing flow analyses, ambiguous module boundary,
  missing SME scope confirmation, and missing BAU notes all block synthesis.
- Anti-hallucination language is specific and operational, especially for
  business actors, BAU rhythm, system interfaces, regulatory claims, and
  business-rule seeds.
- The negative example is valuable: it shows the analyzer refusing partial
  synthesis when a flow and SME owner are missing.
- Cross-view consistency checks create useful handoff pressure before
  `legacy-spec-writer` consumes capability seeds.

## SME Review

- [x] SME governance is explicit
- [x] Observed behavior, inferred rule, and modernization decision are separate
- [x] Evidence tags are required
- [x] IBM i-specific failure modes are covered
- [x] Open questions / TBDs are carried forward instead of hidden

Notes:

The skill treats SMEs as the authority for module boundaries, BAU rhythm,
manual procedures, operational exception handling, integration intent, and
approval. It also correctly keeps business rules as seeds for `legacy-spec-writer`
rather than promoting them inside the module layer.

Before field-pilot use, the output artifacts should force evidence IDs and
per-view checklist items more explicitly so SME review can reject individual
claims without relying on prose memory.

## Runtime Portability Review

- [x] canonical source under `skills/<skill-name>/`
- [x] Claude Code adapter or copy defined if needed
- [x] OpenCode adapter or copy defined if needed
- [x] Codex adapter or copy defined if needed
- [x] runtime-specific metadata isolated from canonical skill

Notes:

Adapter drift check passes. The broken canonical links have been corrected.
The field-pilot cap remains because no runtime has yet loaded or executed this
skill through the reusable smoke-test protocol.

## Adversarial Pass

| Scenario | Expected Behavior | Result |
| --- | --- | --- |
| One in-scope flow lacks approved analysis | Stop, produce blocked overview, route to flow-analyzer | Covered by negative example |
| SME owner / BAU notes missing | Stop, do not invent Operation Flow | Covered |
| Flow belongs to multiple modules | Create SME-boundary TBD | Covered |
| Program or object inventory gap appears during aggregation | Create pending-source TBD and block as needed | Covered |
| SME says a path is dead but flow analysis found code/config evidence | Record conflict and create TBD; code wins on behavior | Covered |
| Cross-flow dependency inferred from shared file | Must trace to flow data sections / object dependencies | Covered |
| System/interface detail is absent from flow or integration docs | Create pending-source or SME TBD | Covered |
| Per-view methodology file is followed from `SKILL.md` | Follow existing output-contract and synthesis-rules references | Covered after post-review hardening |
| Runtime adapter folder differs from canonical path depth | Sync strategy works structurally; smoke not run | Structurally covered |

## Requested Revision Prompt For Claude Code

```text
Revise legacy-ibmi-module-analyzer to finish the remaining review findings.

Current score: 9.0/10 after the runtime-testing and broken-reference caps.
Target score: 9.5/10.

Remaining issues:
1. Three-runtime smoke execution evidence is missing.
2. Evidence traceability has been strengthened, but should be re-scored after
   smoke output is available.

Required changes:
- Run the smoke protocol in Codex CLI, Claude Code, and OpenCode; update `docs/runtime-matrix.md` with exact runtime/model/date notes.
- Re-score the output contract after smoke output is available; if all
  remaining criteria pass, update this scorecard toward field-pilot readiness.

Do not remove author/copyright notices.
Keep the canonical skill under skills/legacy-ibmi-module-analyzer/.
Maintain compatibility with Codex, Claude Code, and OpenCode.
```
