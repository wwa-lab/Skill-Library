---
skill: legacy-step-contract
scorecard_version: v0.1.0
static_score: 9.09
decision: repo-ready
status: superseded
superseded_by: v0.1.1
---

# Skill Review Scorecard: legacy-step-contract v0.1.0

## Metadata

- skill_name: legacy-step-contract
- skill_path: skills/legacy-step-contract
- reviewed_version: v0.1.0
- generated_by: Claude Code (Opus 4.7)
- reviewed_by: Claude Code (Opus 4.7) — draft, awaiting Codex confirmation
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
- Checked canonical source under `skills/legacy-step-contract/`.
- Checked `SKILL.md`, `references/step-contract.md`,
  `templates/step-contract-block.md`,
  `templates/step-validation-report.md`.
- Cross-referenced `docs/evidence-and-knowledge-taxonomy.md`,
  `docs/id-conventions.md`, `docs/data-collection-and-redaction.md`,
  `docs/forward-sdlc-contract.md`, `templates/skill-review-scorecard.md`.
- Ran `scripts/sync-skills.sh --target all --check`; all four runtime
  adapter copies reported `OK`. No adapter drift.
- Checked `docs/runtime-matrix.md`; post-Codex-review v0.1.1 now lists
  `legacy-step-contract` as `passed` in Codex CLI, Claude Code, and
  OpenCode.
- Checked `docs/runtime-smoke-tests.md`; post-Codex-review v0.1.1 now
  includes positive and negative smoke prompts plus pass evidence.
- Confirmed that the Step Contract per-step bindings (inventory, program
  analysis, flow analysis, module analysis, spec writing, spec review,
  forward SDLC handoff) match the input/output contracts in the
  corresponding skills' canonical `SKILL.md` files.

## Mandatory Stop Conditions

No mandatory 8.0 cap conditions found:

- valid `SKILL.md` ✓
- `name` / `description` frontmatter is precise and includes both what the
  skill does and when to use it ✓
- copyright / author notice present ✓
- portable across Codex, Claude Code, and OpenCode; no runtime-specific
  assumptions in canonical source ✓
- clear trigger conditions (When to Use / When NOT to Use) ✓
- clear output contract (Step Contract block + Step Validation Report
  templates) ✓
- SME governance is explicit: SME approval is a third validation layer
  with named role, date, and IDs; not interchangeable with mechanical or
  semantic checks ✓
- not hallucination-prone: explicit anti-hallucination section forbids
  inventing IBM i facts, promoting status, collapsing layers, or
  rubber-stamping SME ✓

At initial v0.1.0 review time, two 9.0 caps applied under the review gate:

- **Examples are missing.** The skill ships two fill-in templates and a
  field-level reference but no concrete, filled-in example of either a
  Step Contract block or a Step Validation Report. Per the gate, "examples
  are missing or too generic" caps at 9.0.
- **Runtime portability not yet smoke-tested.** Adapter drift is clean
  but the skill has not been loaded or executed in Codex CLI, Claude
  Code, or OpenCode through the protocol in
  `docs/runtime-smoke-tests.md`.

Post-Codex-review v0.1.1 update: both caps above have been addressed by the
worked inventory-pass example and three-runtime smoke execution. This v0.1.0
scorecard has not been fully re-scored; create a refreshed v0.1.1 scorecard
before claiming field-pilot readiness.

## Weighted Score

| Category | Weight | Score | Weighted |
| --- | ---: | ---: | ---: |
| Purpose and trigger clarity | 10% | 9.5 | 0.95 |
| Workflow completeness | 12% | 9.0 | 1.08 |
| IBM i / domain correctness | 14% | 9.0 | 1.26 |
| Evidence and anti-hallucination | 12% | 9.5 | 1.14 |
| Output contract | 10% | 8.8 | 0.88 |
| Progressive disclosure | 8% | 9.5 | 0.76 |
| Runtime portability | 10% | 9.0 | 0.90 |
| Reviewability and testability | 10% | 8.3 | 0.83 |
| Engineering handoff value | 8% | 9.0 | 0.72 |
| Maintainability | 6% | 9.5 | 0.57 |

Final score before cap: **9.09 / 10**

Final score after cap: **9.0 / 10**

Decision: **repo-ready, not field-pilot ready**

Post-Codex-review v0.1.1 note: runtime cap and missing-example cap are
resolved. Current field-pilot readiness remains **not claimed** until a
refreshed v0.1.1 weighted scorecard is produced.

## Findings

### Blocking For 9.5

| ID | Severity | Finding | Required Change | Affects |
| --- | --- | --- | --- | --- |
| STEP-CONTRACT-REV-001 | Resolved | No concrete example of either a populated Step Contract block or a populated Step Validation Report. | ✅ Resolved in v0.1.1: added `skills/legacy-step-contract/examples/inventory-pass/` with a filled contract block and validation report. | Reviewability, output contract, engineering handoff value |
| STEP-CONTRACT-REV-002 | Resolved | Three-runtime smoke evidence was missing. | ✅ Resolved in v0.1.1: positive and negative smoke tests passed in Codex CLI, Claude Code, and OpenCode; see `docs/runtime-matrix.md`. | Runtime portability, reviewability |
| STEP-CONTRACT-REV-003 | Resolved | The skill is intentionally separate from `legacy-step-validator`, but `SKILL.md` did not enumerate which artifact actually carries a Step Validation Report at runtime. | ✅ Resolved after Codex review: the relationship section now states that `legacy-step-validator` emits the report. | Reviewability, engineering handoff value |
| STEP-CONTRACT-REV-004 | Resolved | The orchestrator emits `step_id: STEP-ROUTING-<NNN>`, while the Step Contract reference previously allowed only `STEP-<CAPABILITY-SLUG>-<NNN>`. | ✅ Resolved after Codex review: `STEP-ROUTING-<NNN>` is now an explicit reserved routing-step slug before a capability exists. | ID conventions, output contract |
| STEP-CONTRACT-REV-005 | Resolved | The compact validation result format used slightly different field semantics across SKILL.md and templates. | ✅ Resolved after Codex review: compact results now consistently split downstream advancement from remediation via `downstream_next_step` and `remediation_step`. | Output contract, maintainability |

### Improvement Findings (Non-Blocking)

| ID | Finding | Suggested Change |
| --- | --- | --- |
| STEP-CONTRACT-IMP-001 | The "Per-Step ID Minting Policy" table lives only in `references/step-contract.md` and is not summarized in `SKILL.md`. A reader who never opens the reference may not realise the table is the authoritative source. | Add one sentence in `SKILL.md` Output / Validation sections pointing to the per-step ID minting policy by name. |
| STEP-CONTRACT-IMP-002 | `Idempotency` is listed as a recommended EXECUTION field but the consequences of `non_idempotent` are not described. A non-idempotent step has implications for re-validation. | Add one paragraph in `references/step-contract.md` clarifying how non-idempotent steps interact with re-validation and waiver carry-forward. |
| STEP-CONTRACT-IMP-003 | The "Worked Step Bindings" thumbnails are useful but mix two formats (some have bullet lists, some have inline `mechanical: …` lines). | Standardise the thumbnail format across all seven step bindings. |
| STEP-CONTRACT-IMP-004 | The `assumptions_recorded` field is described as "assumptions the runner is allowed to make explicitly, never silently" — but the SKILL.md does not give an example of an acceptable vs unacceptable assumption. | Add one short example pair so the reviewer can calibrate. |
| STEP-CONTRACT-IMP-005 | `SKILL.md` is 398 lines, just inside the typical lean-skill envelope. Most of the volume is the per-step bindings table and the validation-layer detail. | Consider moving the per-step bindings summary table to `references/step-contract.md` and citing only the layer detail in `SKILL.md`. Optional. |

### Strengths

- The three-layer model (mechanical / AI semantic / SME approval) is
  rigorously applied. Each layer has explicit promotion rules, and the
  skill refuses to substitute one for another.
- The five-category unresolved-items ledger (`missing_inputs`,
  `evidence_gaps`, `contradictory_evidence`, `sme_questions`,
  `downstream_handoff_blockers`) gives reviewers a vocabulary that ties
  every TBD to a resolver role. This is meaningfully better than
  free-text TBDs.
- Status promotion discipline is strict: the contract skill does not
  promote any artifact's `status` field and does not approve any
  `BR-*`. Promotion is the owning skill's job; approval is the SME's.
- The Compact Validation Result (`pass` / `pass_with_warnings` /
  `blocked`) plus the five-key handoff block gives the orchestrator and
  any downstream automation a stable interface to consume.
- Per-step bindings are accurate against the existing analyzer and
  spec-writer skills; the IBM i specifics (DSPF / PRTF / `*MENU` /
  WRKJOBSCDE / commit boundaries) are deferred to the executing skills
  rather than restated, which is the right separation.

## SME Review

- [x] SME governance is explicit
- [x] Observed behavior, inferred rule, and modernization decision are separate
- [x] Evidence tags are required
- [x] IBM i-specific failure modes are covered (by deferral to the
      executing skills, not by restating)
- [x] Open questions / TBDs are carried forward instead of hidden

Notes:

SME governance is one of this skill's strongest areas. SME approval is
treated as a control point with named role, date, and IDs approved; the
skill explicitly forbids treating SME review as a rubber stamp and
forbids the validator role from approving on the SME's behalf. The
five-category TBD ledger is well aligned with the
`docs/evidence-and-knowledge-taxonomy.md` knowledge-type model.

## Runtime Portability Review

- [x] canonical source under `skills/legacy-step-contract/`
- [x] Claude Code adapter or copy defined
- [x] OpenCode adapter or copy defined
- [x] Codex adapter or copy defined
- [x] runtime-specific metadata isolated from canonical skill

Notes:

Adapter drift check passes for all four runtime targets. The field-pilot
cap remains because no runtime has loaded or executed this skill, and
`docs/runtime-smoke-tests.md` does not yet contain prompts for this
skill.

## Adversarial Pass

| Scenario | Expected Behavior | Result |
| --- | --- | --- |
| Step has `sensitive: unknown` evidence | Status is `blocked` immediately; Redaction Gate cited | Covered in 4a + STEP-CONTRACT pre-flight discipline |
| Prerequisite artifact below required status | Status is `blocked`; surface under `missing_inputs` | Covered |
| SME required but no `sme_owner` named | Status is `blocked`; surface under `sme_questions` | Covered |
| Two evidence items disagree | Surface under `contradictory_evidence`; SME records a `DEC-*` | Covered |
| Caller asks the contract skill to produce inventory | Refuse; route to the dedicated skill | Covered in "When NOT to Use" |
| Caller asks the contract skill to override an SME decision | Refuse; this skill does not approve | Covered in anti-hallucination |
| Step is non-idempotent and re-run | (Undocumented — see STEP-CONTRACT-IMP-002) | Partially covered |
| Routing-step `step_id` is required | Use `STEP-ROUTING-<NNN>` per orchestrator before a capability slug exists | Covered |
| Compact result has 0 blocking items but 1 TBD with `blocks_next_step: yes` | Status is `pass_with_warnings`; surface the carry-forward warning | Covered |

## Requested Revision Prompt For Claude Code

```text
Revise legacy-step-contract to move from 9.0/10 (repo-ready) toward
9.5/10 (field-pilot ready).

Current score: 9.0/10 after the examples and runtime-testing caps.
Target score: 9.5/10.

Blocking issues:
1. No concrete worked example of a populated Step Contract block or a
   populated Step Validation Report.
2. Three-runtime smoke execution evidence is missing.
3. Resolved after Codex review: the skill now delegates report production
   to `legacy-step-validator`.
4. Resolved after Codex review: `STEP-ROUTING-<NNN>` is now an explicit
   reserved slug for routing decisions before a capability exists.
5. Resolved after Codex review: compact result fields now distinguish
   `downstream_next_step` from `remediation_step`.

Required changes:
- Add skills/legacy-step-contract/examples/ with at least one filled
  Step Contract block + filled Step Validation Report for one real step
  (suggested: inventory for redacted-customer-credit-check).
- Resolved after Codex review: relationship, routing `step_id`, and
  compact-result field semantics were updated in canonical sources.
- Add positive and negative smoke prompts to docs/runtime-smoke-tests.md
  for this skill; run them in Codex CLI, Claude Code, and OpenCode;
  update docs/runtime-matrix.md.
- Re-score this skill after the runtime evidence is recorded.

Do not remove author/copyright notices.
Keep the canonical skill under skills/legacy-step-contract/.
Maintain compatibility with Codex, Claude Code, and OpenCode.
Do not approve any IBM i fact, business rule, or SME decision from
within this skill — it is a contract layer, not a business analyzer.
```
