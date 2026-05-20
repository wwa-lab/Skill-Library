---
skill: legacy-spec-writer
scorecard_version: v0.1.0
static_score: 9.24
decision: repo-ready
status: current
last_verified: 2026-05-14
runtimes_tested:
  codex: { status: synced, model: gpt-5.4-mini, date: null }
  claude_code: { status: passed, model: haiku, date: 2026-05-14 }
  opencode: { status: synced, model: minimax-m2.5-free, date: null }
evidence_source: docs/runtime-matrix.md
---

# Skill Review Scorecard: legacy-spec-writer v0.1.0

## Metadata

- skill_name: legacy-spec-writer
- skill_path: skills/legacy-spec-writer
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
- Checked canonical source under `skills/legacy-spec-writer/`.
- Checked `SKILL.md`, `references/`, `templates/`, `examples/spec-positive/`,
  `schemas/spec.schema.yaml`, `docs/forward-sdlc-contract.md`,
  `docs/evidence-and-knowledge-taxonomy.md`, and
  `docs/runtime-smoke-tests.md`.
- Ran `scripts/sync-skills.sh --target all --check`; all runtime adapter copies
  reported `OK`.
- Ran `python3 scripts/check-spec-contract.py`; spec contract alignment passed
  for the root `templates/spec.yaml` and `schemas/spec.schema.yaml`.
- Parsed `skills/legacy-spec-writer/templates/spec.yaml`,
  `skills/legacy-spec-writer/examples/spec-positive/spec.yaml`,
  `templates/spec.yaml`, and `schemas/spec.schema.yaml` as YAML; all parsed.
- Checked `docs/runtime-matrix.md`; `legacy-spec-writer` is `passed` in Claude Code
  (haiku, 2026-05-14), `synced` in Codex and OpenCode pending execution.
- Checked `docs/runtime-smoke-tests.md`; positive and negative `legacy-spec-writer`
  smoke prompts exist and have been executed in Claude Code with passing results
  (2026-05-14). Execution results in Codex CLI and OpenCode are still pending.
- Ran `python3 scripts/check-spec-contract.py legacy-spec-writer`; the
  skill-local template now aligns with the schema.

## Mandatory Stop Conditions

No mandatory 8.0 cap conditions found.

A 9.0 cap applied pending runtime portability evidence. Status:

- ✅ Smoke test positive scenario (all upstream analyses approved, 8 programs)
  passed in Claude Code (haiku, 2026-05-14)
- ✅ Smoke test negative scenario (missing/draft flow analysis) passed in Claude Code
  (haiku, 2026-05-14)
- ⏳ Codex (gpt-5.4-mini) smoke execution pending
- ⏳ OpenCode (minimax-m2.5-free) smoke execution pending

Field-pilot readiness is conditional on all three runtimes passing. Score remains
capped at 9.0 until Codex and OpenCode execution results are recorded.

## Weighted Score

| Category | Weight | Score | Weighted |
| --- | ---: | ---: | ---: |
| Purpose and trigger clarity | 10% | 9.5 | 0.95 |
| Workflow completeness | 12% | 9.4 | 1.13 |
| IBM i / domain correctness | 14% | 9.2 | 1.29 |
| Evidence and anti-hallucination | 12% | 9.5 | 1.14 |
| Output contract | 10% | 9.1 | 0.91 |
| Progressive disclosure | 8% | 9.3 | 0.74 |
| Runtime portability | 10% | 9.0 | 0.90 |
| Reviewability and testability | 10% | 8.8 | 0.88 |
| Engineering handoff value | 8% | 9.3 | 0.74 |
| Maintainability | 6% | 9.3 | 0.56 |

Final score before cap: **9.24 / 10**

Final score after cap: **9.0 / 10**

Decision: **repo-ready, not field-pilot ready**

## Findings

### Blocking For 9.5

| ID | Severity | Finding | Required Change | Affects |
| --- | --- | --- | --- | --- |
| SPEC-REV-001 | High | Runtime portability is structurally clean but not tested. | ✅ Partially resolved. Smoke test passed in Claude Code (haiku, 2026-05-14). Codex and OpenCode execution pending to lift cap to 9.5. See `docs/runtime-matrix.md` entry. | Runtime portability, reviewability |
| SPEC-REV-002 | High | The skill-local template generated an AC for a BR marked `needs_sme_review`. | ✅ Resolved. `skills/legacy-spec-writer/templates/spec.yaml` now defaults to `acceptance_criteria: []` with comments allowing ACs only for approved BRs. | Evidence integrity, anti-hallucination |
| SPEC-REV-003 | High | The forward-handoff data-model evidence gate was not represented in schema/template fields. | ✅ Resolved. `schemas/spec.schema.yaml`, the skill-local template, and the positive example now include field-level `evidence_strength` and `review_status`. | Output contract, downstream automation |
| SPEC-REV-004 | Medium | Required outputs `spec-review.md` and `traceability.md` lacked templates. | ✅ Resolved. Canonical templates now exist and are linked from `SKILL.md`. | Reviewability, SME governance |
| SPEC-REV-005 | Medium | Contract checking validated the root template but not the skill-local template. | ✅ Resolved. `scripts/check-spec-contract.py legacy-spec-writer` validates the skill-local template. | Maintainability, output contract |
| SPEC-REV-006 | Medium | The positive traceability example checked a failed forward-handoff row. | ✅ Resolved. The unresolved blocking TBD row is now unchecked while the spec remains `in_review`. | Reviewability, downstream automation |

### Strengths

- The skill has excellent layer discipline: it consumes approved inventory,
  module, flow, and program analyses instead of re-reading IBM i source or
  jumping directly to Java/cloud code.
- The rule-extraction protocol is strong and appropriately conservative:
  Class A/B/C/D handling keeps observed behavior, inferred business rules, SME
  approval, and speculation separate.
- Anti-hallucination guidance is concrete and operational, especially around
  not inventing BRs, data field semantics, target architecture, ACs, or hidden
  TBD resolution.
- The output package is the right handoff shape for forward SDLC:
  `spec.yaml`, `spec.md`, `spec-review.md`, and `traceability.md`.
- The positive example is realistic and demonstrates the correct `in_review`
  posture when a BR and modernization decision remain unresolved.

## SME Review

- [x] SME governance is explicit
- [x] Observed behavior, inferred rule, and modernization decision are separate
- [x] Evidence tags are required
- [x] IBM i-specific failure modes are covered
- [x] Open questions / TBDs are carried forward instead of hidden

Notes:

SME control is one of this skill's strongest areas. The skill requires a named
capability owner, blocks rule approval without SME confirmation, separates
observed behaviors from BRs and DECs, and keeps unresolved ambiguity in
`TBD-*` records. The template/schema/checker hardening now mirrors that
discipline more directly; the remaining field-pilot blocker is runtime smoke
execution evidence and post-smoke re-scoring.

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
| Module analysis is not approved | Stop and route back to module analyzer | Covered |
| Capability seed has blocking TBDs | Stop and require clarification | Covered |
| No capability owner SME exists | Stop; BRs cannot move beyond draft | Covered |
| Evidence has `sensitive: unknown` | Stop for redaction review | Covered |
| BR candidate has no SME confirmation | Keep as `needs_sme_review`; do not generate AC | Covered in prose and template |
| AC validates a draft or unapproved BR | Flag as orphan/invalid; remove or block | Covered in prose and template |
| Data model field lacks evidence | Create field-level TBD / block handoff | Covered in schema/template |
| Blocking TBD remains at handoff | Spec remains `in_review`; no forward SDLC handoff | Covered; example checkbox corrected |
| Runtime adapter folder differs from canonical path depth | Should keep relative links portable after sync | Structurally covered; smoke not run |

## Requested Revision Prompt For Claude Code

```text
Revise legacy-spec-writer to finish the remaining review finding.

Current score: 9.0/10 after the runtime-testing and enforceability cap.
Target score: 9.5/10.

Blocking issue:
1. Three-runtime smoke execution evidence is missing.

Required changes:
- Run the smoke protocol in Codex CLI, Claude Code, and OpenCode; update
  docs/runtime-matrix.md with exact runtime/model/date notes.
- If all three pass, re-score this skill and update the scorecard toward
  field-pilot readiness.

Do not remove author/copyright notices.
Keep the canonical skill under skills/legacy-spec-writer/.
Maintain compatibility with Codex, Claude Code, and OpenCode.
```
