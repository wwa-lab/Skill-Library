---
skill: legacy-ibmi-flow-analyzer
scorecard_version: v0.1.0
static_score: 9.44
decision: repo-ready
status: superseded
superseded_by: v0.1.1
---

# Skill Review Scorecard: legacy-ibmi-flow-analyzer v0.1.0

## Metadata

- skill_name: legacy-ibmi-flow-analyzer
- skill_path: skills/legacy-ibmi-flow-analyzer
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
- Checked canonical source under `skills/legacy-ibmi-flow-analyzer/`.
- Checked output template, trigger checklist, references, and positive /
  negative examples.
- Ran `scripts/sync-skills.sh --target all --check`; all runtime adapter copies
  reported `OK`.
- Checked `docs/runtime-matrix.md`; all target runtimes are still `synced`, not
  `loaded`, `executed`, or `passed`.
- Checked `docs/runtime-smoke-tests.md`; no flow-analyzer prompt has been added
  yet, so the reusable smoke protocol cannot be run verbatim for this skill.

## Mandatory Stop Conditions

No mandatory 8.0 cap conditions found.

A 9.0 cap applies under the review gate:

- portability has been considered and adapter drift has been checked, but the
  skill has not been loaded or executed in Codex CLI, Claude Code, and OpenCode
- the runtime-smoke-test prompt set does not yet include
  `legacy-ibmi-flow-analyzer`

## Weighted Score

| Category | Weight | Score | Weighted |
| --- | ---: | ---: | ---: |
| Purpose and trigger clarity | 10% | 9.6 | 0.96 |
| Workflow completeness | 12% | 9.5 | 1.14 |
| IBM i / domain correctness | 14% | 9.4 | 1.32 |
| Evidence and anti-hallucination | 12% | 9.6 | 1.15 |
| Output contract | 10% | 9.3 | 0.93 |
| Progressive disclosure | 8% | 9.6 | 0.77 |
| Runtime portability | 10% | 9.0 | 0.90 |
| Reviewability and testability | 10% | 9.4 | 0.94 |
| Engineering handoff value | 8% | 9.6 | 0.77 |
| Maintainability | 6% | 9.4 | 0.56 |

Final score before cap: **9.44 / 10**

Final score after cap: **9.0 / 10**

Decision: **repo-ready, not field-pilot ready**

## Findings

### Blocking For 9.5

| ID | Severity | Finding | Required Change | Affects |
| --- | --- | --- | --- | --- |
| FLOW-REV-001 | High | Runtime portability is structurally clean but not tested. `docs/runtime-matrix.md` records this skill as `synced` only, and `docs/runtime-smoke-tests.md` has no positive or negative prompt for it. | Add flow-analyzer smoke prompts and pass criteria, run the protocol in Codex CLI, Claude Code, and OpenCode, then update `docs/runtime-matrix.md` and the scorecard. | Runtime portability, reviewability |
| FLOW-REV-002 | Medium | Trigger-model guidance is internally inconsistent. `references/trigger-models.md` says every flow begins with exactly one trigger, while the batch positive example uses `Scheduler → Batch Job (combined)` and the review notes endorse that combined model. | Define a primary-trigger rule: either allow a scheduler trigger with batch submission as the first edge, or treat scheduler and batch as separate linked flows. Update `SKILL.md`, `trigger-models.md`, template wording, and examples consistently. | Trigger clarity, SME correctness |
| FLOW-REV-003 | Medium | Blocked-flow status is inconsistent. The negative example uses `blocked_pending_source`, while the output contract and template list only `draft`, `needs_sme_review`, and `approved` for status. | Add blocked statuses such as `blocked_pending_source` and `blocked_pending_sme` to the output contract and template, and state when the analyzer must produce a blocked stub instead of a draft. | Output contract, downstream automation |
| FLOW-REV-004 | Medium | Capability seed IDs are inconsistent. `SKILL.md` says to extract `BR-*` candidates, while the output contract, template, and examples use `SEED-*`. | Standardize on `SEED-*` for flow-level candidate questions, or explicitly define how `BR-*` candidates are converted downstream by spec-writer. | Output contract, downstream automation |
| FLOW-REV-005 | Medium | Evidence wording is too source-code-centric for non-code triggers. The anti-hallucination rule requires every edge to trace to source code, but scheduler entries, menu definitions, trigger registrations, MQ queue contracts, and API gateway configuration may be authoritative configuration evidence rather than program source. | Add a trigger evidence taxonomy: source statement, IBM i object/config export, integration contract, and SME confirmation. Make clear which trigger evidence is sufficient and when a TBD is required. | Evidence integrity, IBM i correctness |

### Strengths

- Excellent trigger coverage: batch, menu, subfile, F-key, DB trigger,
  scheduler, and API/remote are all represented with concrete SME questions.
- The skill clearly sits between program analysis and module/spec synthesis:
  it refuses to re-analyze programs and requires approved program analyses for
  every node.
- Output contract is rich and downstream-friendly: flow metadata, trigger
  context, sequence diagram, nodes, edges, data exchanges, branch points, UI
  surfaces, error propagation, commit boundaries, capability seeds, TBDs, and
  SME sign-off.
- Data-flow guidance covers several IBM i coupling mechanisms that are often
  missed: DTAARA, DTAQ, shared files, spool, IFS, message queues, and
  activation-group globals.
- Error propagation and commit-boundary guidance is field-useful, especially
  the vulnerable-window analysis.
- The examples are specific and varied: one scheduler/batch flow, one
  interactive menu flow with DSPFs/F-keys/subfile branch, and one blocked
  incomplete-flow negative case.

## SME Review

- [x] SME governance is explicit
- [x] Observed behavior, inferred rule, and modernization decision are separate
- [x] Evidence tags are required
- [x] IBM i-specific failure modes are covered
- [x] Open questions / TBDs are carried forward instead of hidden

Notes:

The skill is strong on SME governance. It asks SMEs to validate the trigger
model, business event name, node scope, production edges, cross-program data
flow, UI surfaces, error propagation, commit boundaries, and capability seeds.
It also keeps seeds as questions instead of promoted business rules, which is
exactly the right boundary for this layer.

## Runtime Portability Review

- [x] canonical source under `skills/<skill-name>/`
- [x] Claude Code adapter or copy defined if needed
- [x] OpenCode adapter or copy defined if needed
- [x] Codex adapter or copy defined if needed
- [x] runtime-specific metadata isolated from canonical skill

Notes:

Adapter drift check passes. The field-pilot cap remains because no runtime has
yet loaded or executed this skill through the reusable smoke-test protocol.

## Adversarial Pass

| Scenario | Expected Behavior | Result |
| --- | --- | --- |
| Program in chain lacks approved program analysis | Stop, create pending-source TBD, route to program-analyzer | Covered |
| Inventory is blocked or relationships are incomplete | Stop and route to inventory | Covered |
| Trigger model is ambiguous | Stop, create SME TBD, do not guess | Covered |
| Flow spans multiple business modules | Narrow scope to one transaction | Covered |
| Scheduler submits a batch job | Needs one consistent representation | Needs hardening |
| Source/code edge conflicts with SME recollection | Record both and block until reconciled | Covered |
| Interactive flow with F-keys and subfile options | Capture branch points and UI surfaces | Covered |
| Missing DSPF/MENU/trigger registration evidence | Should create source/config TBD | Partially covered; needs trigger evidence taxonomy |
| Runtime adapter folder differs from canonical path depth | Should keep relative links portable after sync | Structurally covered; smoke not run |

## Requested Revision Prompt For Claude Code

```text
Revise legacy-ibmi-flow-analyzer to address the following review findings.

Current score: 9.0/10 after the runtime-testing cap.
Target score: 9.5/10.

Blocking issues:
1. Runtime smoke prompts and three-runtime execution evidence are missing.
2. Trigger-model guidance is inconsistent for Scheduler -> Batch combined flows.
3. Blocked-flow status values are not aligned across SKILL.md, output contract, template, and negative example.
4. Capability seed IDs use both BR-* and SEED-*.
5. Trigger evidence rules need to cover IBM i object/config exports and integration contracts, not only program source.

Required changes:
- Add `legacy-ibmi-flow-analyzer` positive and negative prompts to `docs/runtime-smoke-tests.md`, including pass criteria for a complete batch/menu flow and a missing-program-analysis stop case.
- Run the smoke protocol in Codex CLI, Claude Code, and OpenCode; update `docs/runtime-matrix.md` with exact runtime/model/date notes.
- Define how Scheduler -> Batch is represented: one primary scheduler trigger with SBMJOB as the first edge, or two linked flows. Update all affected docs and examples consistently.
- Add blocked statuses such as `blocked_pending_source` and `blocked_pending_sme` to the output contract and template.
- Standardize capability seed IDs on `SEED-*`, or document conversion from flow-level seeds to downstream `BR-*` candidates.
- Add trigger evidence categories for source statements, IBM i object/config exports, integration contracts, and SME confirmation.

Do not remove author/copyright notices.
Keep the canonical skill under skills/legacy-ibmi-flow-analyzer/.
Maintain compatibility with Codex, Claude Code, and OpenCode.
```
