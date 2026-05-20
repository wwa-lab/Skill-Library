---
skill: legacy-step-validator
scorecard_version: v0.1.0
static_score: 9.28
decision: repo-ready
status: superseded
superseded_by: v0.1.1
---

# Skill Review Scorecard: legacy-step-validator v0.1.0

## Metadata

- skill_name: legacy-step-validator
- skill_path: skills/legacy-step-validator
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
- Checked canonical source under `skills/legacy-step-validator/`.
- Checked `SKILL.md`, `references/validation-checklists.md`,
  `references/finding-taxonomy.md`,
  `templates/step-validation-report.md`,
  `templates/blocking-findings.yaml`,
  `examples/pass/step-validation-report.md`,
  `examples/blocked/step-validation-report.md`,
  `examples/blocked/blocking-findings.yaml`.
- Cross-referenced `skills/legacy-step-contract/SKILL.md`,
  `skills/legacy-step-contract/references/step-contract.md`,
  `docs/evidence-and-knowledge-taxonomy.md`,
  `docs/data-collection-and-redaction.md`, `docs/id-conventions.md`,
  `docs/skill-review-gate.md`, `docs/forward-sdlc-contract.md`.
- Ran `scripts/sync-skills.sh --target all --check`; all four runtime
  adapter copies reported `OK`. No adapter drift.
- Checked `docs/runtime-matrix.md`; post-Codex-review v0.1.1 now lists
  `legacy-step-validator` as `passed` in Codex CLI, Claude Code, and
  OpenCode.
- Checked `docs/runtime-smoke-tests.md`; post-Codex-review v0.1.1 now
  includes positive and negative smoke prompts plus pass evidence.
- Audited the `blocked` example for internal consistency (see
  STEP-VALIDATOR-REV-002).

## Mandatory Stop Conditions

No mandatory 8.0 cap conditions found:

- valid `SKILL.md` ✓
- `name` / `description` frontmatter is precise; description lists which
  artifacts the validator handles and what it returns ✓
- copyright / author notice present ✓
- portable across Codex, Claude Code, and OpenCode; no runtime-specific
  assumptions in canonical source ✓
- clear trigger conditions (When to Use / When NOT to Use) ✓
- clear output contract (`06_quality/step-validation-report.md` +
  optional `06_quality/blocking-findings.yaml`) ✓
- SME governance is explicit: SME readiness ≠ SME approval; the
  validator refuses to approve on the SME's behalf ✓
- not hallucination-prone: explicit refusal to mint IDs, approve
  business rules, transition `status` fields, override SME decisions, or
  promote `blocked` to `pass_with_warnings` ✓

At initial v0.1.0 review time, one 9.0 cap applied under the review gate:

- **Runtime portability not yet smoke-tested.** Adapter drift is clean
  but the skill has not been loaded or executed in Codex CLI, Claude
  Code, or OpenCode through the protocol in
  `docs/runtime-smoke-tests.md`.

Examples *do* exist (`pass/` and `blocked/`), which would otherwise be a
9.0 cap; that cap therefore does not apply. The 9.0 cap from runtime
smoke evidence does apply.

Post-Codex-review v0.1.1 update: the runtime smoke cap has been addressed by
three-runtime positive and negative smoke execution. This v0.1.0 scorecard has
not been fully re-scored; create a refreshed v0.1.1 scorecard before claiming
field-pilot readiness.

## Weighted Score

| Category | Weight | Score | Weighted |
| --- | ---: | ---: | ---: |
| Purpose and trigger clarity | 10% | 9.5 | 0.95 |
| Workflow completeness | 12% | 9.4 | 1.13 |
| IBM i / domain correctness | 14% | 9.0 | 1.26 |
| Evidence and anti-hallucination | 12% | 9.5 | 1.14 |
| Output contract | 10% | 9.2 | 0.92 |
| Progressive disclosure | 8% | 9.5 | 0.76 |
| Runtime portability | 10% | 9.0 | 0.90 |
| Reviewability and testability | 10% | 9.0 | 0.90 |
| Engineering handoff value | 8% | 9.4 | 0.75 |
| Maintainability | 6% | 9.5 | 0.57 |

Final score before cap: **9.28 / 10**

Final score after cap: **9.0 / 10**

Decision: **repo-ready, not field-pilot ready**

Post-Codex-review v0.1.1 note: runtime cap is resolved. Current field-pilot
readiness remains **not claimed** until a refreshed v0.1.1 weighted scorecard
is produced.

## Findings

### Blocking For 9.5

| ID | Severity | Finding | Required Change | Affects |
| --- | --- | --- | --- | --- |
| STEP-VALIDATOR-REV-001 | Resolved | Three-runtime smoke evidence was missing. | ✅ Resolved in v0.1.1: positive and negative smoke tests passed in Codex CLI, Claude Code, and OpenCode; see `docs/runtime-matrix.md`. | Runtime portability, reviewability |
| STEP-VALIDATOR-REV-002 | Resolved | The `blocked` example originally listed three blocking findings in the report headline but four in the dimension breakdown and companion YAML. | ✅ Resolved after Codex review: the compact result now lists `FIND-CARD-AUTH-001` through `004` consistently. | Reviewability, output contract, downstream automation |
| STEP-VALIDATOR-REV-003 | Resolved | The validator's former `next_safe_step` field was overloaded between downstream advancement and prerequisite remediation. | ✅ Resolved after Codex review: compact results now use `downstream_next_step` and `remediation_step`. | Output contract, engineering handoff value |
| STEP-VALIDATOR-REV-004 | Resolved | `references/validation-checklists.md` did not explain why spec-review-as-a-step is absent while `legacy-spec-reviewer` is planned. | ✅ Resolved after Codex review: SKILL.md and the checklist now document the manual fallback through the spec-writing package. | Workflow completeness, downstream automation |
| STEP-VALIDATOR-REV-005 | Resolved | The `recommended_action` rule asked for one short sentence while the blocked example used folded multi-line actions. | ✅ Resolved after Codex review: example actions are now single short sentences. | Output contract, maintainability |
| STEP-VALIDATOR-REV-006 | Resolved | The validator had a `waivers:` block but did not state where SME-recorded waivers are read from. | ✅ Resolved after Codex review: Workflow step 3 now requires waivers to be recorded in the artifact or review file with role/name/date/reason/IDs. | SME governance, output contract |

### Improvement Findings (Non-Blocking)

| ID | Finding | Suggested Change |
| --- | --- | --- |
| STEP-VALIDATOR-IMP-001 | Step type detection relies on a directory/file fingerprint table in `references/validation-checklists.md`. The table is good but does not address packages partially renamed (e.g., a module folder named `cardauth/` rather than `CARD-AUTH/`). | Add a one-line rule that slug casing/hyphenation is normalised before fingerprint match, or reject and request rename. |
| STEP-VALIDATOR-IMP-002 | The "Default-to-Blocking Rule" in `references/finding-taxonomy.md` is well-stated but does not give an example of how a reviewer should distinguish a legitimately-non-blocking finding from a "looks low-risk but propagates downstream" finding. | Add one short example pair to `references/finding-taxonomy.md`. |
| STEP-VALIDATOR-IMP-003 | The validator does not specify whether a re-run on a previously-validated package should reuse `FIND-*` IDs or mint new ones. Stable IDs help traceability across revisions; fresh IDs prevent stale-finding rot. | Pick one rule (recommended: stable per `dimension + referenced_check + step_id` tuple) and document it under "Anti-Hallucination Rules" or a new "Idempotency" subsection. |
| STEP-VALIDATOR-IMP-004 | Per-step mechanical checklists have ~10–15 rows each; nice for thoroughness but heavy to scan during a one-off validation. | Consider tagging each row with a short ID (e.g., `INV-MECH-01`) so findings can cite `referenced_check: INV-MECH-01` rather than the row's prose. |
| STEP-VALIDATOR-IMP-005 | The skill cites `templates/skill-review-scorecard.md` but clarifies that scoring skills is *not* the validator's job. The mention may confuse new readers. | Either remove the citation from "Output Contract" → "Follow" (it is genuinely out of scope) or move it under a "What this skill does NOT consume" note. |
| STEP-VALIDATOR-IMP-006 | `SKILL.md` is 412 lines. The ten-dimension table, the finding taxonomy summary, and the validation-result enum are all duplicated in references. | Trim duplication; keep `SKILL.md` to the workflow and the dimension list, with the rest cited via `references/`. Optional. |

### Strengths

- The validator-vs-author separation is preserved cleanly. The validator
  reads what is in front of it and cites IDs; it never produces IBM i
  facts, never approves a `BR-*`, and never promotes a `status` field.
- The three-layer model (mechanical / semantic / SME readiness) is
  faithful to the upstream Step Contract and is applied consistently
  across all six per-step checklists.
- The ten review dimensions give findings a stable taxonomy that a
  reviewer or automation tool can sort by. The dimension is enforced as
  exactly one per finding, which prevents the "this finding is sort of
  about everything" trap.
- `examples/pass/` and `examples/blocked/` exist, and the blocked example
  carries a companion `blocking-findings.yaml`. This lifts the usual
  "examples missing" 9.0 cap.
- The "default-to-blocking" rule is explicit and defended, including the
  asymmetric-cost rationale. This is the right bias for a pre-handoff
  validator.
- The Redaction Gate is run as a pre-flight before any other layer, with
  a hard stop on `sensitive: unknown` or unredacted production data.

## SME Review

- [x] SME governance is explicit
- [x] Observed behavior, inferred rule, and modernization decision are separate
- [x] Evidence tags are required
- [x] IBM i-specific failure modes are covered (per-step checklists cite
      DSPF, PRTF, `*MENU`, MONMSG, EXSR/CALL, OBJREF TREE, commit
      boundaries, scheduler/trigger configuration exports)
- [x] Open questions / TBDs are carried forward instead of hidden

Notes:

SME governance is clearly separated from SME approval. The skill's
`sme_readiness` layer checks that an artifact is in a shape an SME can
review (named owner, scoped questions, traceable IDs); it never approves
on the SME's behalf. SME-recorded waivers are accepted only when the
artifact carries them verbatim; the validator does not invent waivers.
The remaining SME-related gap is finding STEP-VALIDATOR-REV-006: the
exact location in the underlying artifact where waivers are read is not
specified.

## Runtime Portability Review

- [x] canonical source under `skills/legacy-step-validator/`
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
| Package contains unredacted production data | Status is `blocked` immediately; Redaction Gate cited; no further layer run | Covered (pre-flight step) |
| Package contains two step types | Refuse; request scope clarification | Covered |
| Package matches no fingerprint | Mark unrecognised and stop | Covered |
| User asks the validator to produce a `spec.yaml` | Refuse; route to `legacy-spec-writer` | Covered ("When NOT to Use") |
| User asks the validator to override SME approval | Refuse; cite anti-hallucination | Covered |
| Mechanical check fails as blocking; user asks for a waiver | Accept only if the artifact carries a named SME waiver; otherwise record SME absence as a finding | Partially covered — see STEP-VALIDATOR-REV-006 |
| Two evidence items disagree without a `DEC-*` | Surface as `contradictory_evidence` under dimension 9; status is `blocked` | Covered in the blocked example |
| Module step claims `approved` view without SME role/date/IDs | Status is `blocked`; finding under dimension 6 | Covered in the blocked example |
| Re-run on a previously-validated, revised package | (Behaviour unspecified — see STEP-VALIDATOR-IMP-003) | Partially covered |
| Validator is asked to score a *skill* (rather than a step artifact) | Refuse; defer to `docs/skill-review-gate.md` | Covered ("When NOT to Use") |
| Spec-review step (planned) | Currently no checklist row; behaviour ambiguous | Not covered — see STEP-VALIDATOR-REV-004 |
| Slug casing mismatch in module folder name | (Behaviour unspecified — see STEP-VALIDATOR-IMP-001) | Partially covered |
| `pass_with_warnings` with carry-forward warnings | Emit warnings in compact result and in handoff note | Covered in both examples (the pass example has zero warnings; the contract is stated) |

## Requested Revision Prompt For Claude Code

```text
Revise legacy-step-validator to move from 9.0/10 (repo-ready) toward
9.5/10 (field-pilot ready).

Current score: 9.0/10 after the runtime-testing cap.
Target score: 9.5/10.

Blocking issues:
1. Three-runtime smoke execution evidence is missing.
2. Resolved after Codex review: the blocked example now lists four
   blocking findings consistently in the report and YAML.
3. Resolved after Codex review: the former overloaded next-step field was
   split into `downstream_next_step` and `remediation_step`.
4. Resolved after Codex review: waiver source requirements are now
   documented in Workflow step 3.
5. Resolved after Codex review: spec-review-as-a-step is documented as
   intentionally out of scope until `legacy-spec-reviewer` exists.
6. Resolved after Codex review: blocked example `recommended_action`
   values are single short sentences.

Required changes:
- Add positive and negative smoke prompts to docs/runtime-smoke-tests.md
  for this skill (positive: validate the pass example; negative:
  validate the blocked example and expect 4 blocking findings).
- Run smoke prompts in Codex CLI, Claude Code, and OpenCode; update
  docs/runtime-matrix.md with runtime/model/date notes.
- Resolved after Codex review: compact results now carry
  `downstream_next_step` and `remediation_step`.
- Resolved after Codex review: blocked findings, waiver handling,
  spec-review fallback, and one-sentence recommended actions were aligned.
- Re-score this skill after the runtime evidence is recorded.

Do not remove author/copyright notices.
Keep the canonical skill under skills/legacy-step-validator/.
Maintain compatibility with Codex, Claude Code, and OpenCode.
Do not approve any IBM i fact, business rule, or SME decision from
within this skill — it is a validator, not a business analyzer.
```
