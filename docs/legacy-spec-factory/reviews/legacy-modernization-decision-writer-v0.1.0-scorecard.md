---
skill: legacy-modernization-decision-writer
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

# Skill Review Scorecard: legacy-modernization-decision-writer v0.1.0

## Metadata

- skill_name: `legacy-modernization-decision-writer`
- skill_path: `skills/legacy-modernization-decision-writer/`
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

- Reviewed against `docs/skill-review-gate.md`,
  `docs/id-conventions.md`, `docs/evidence-and-knowledge-taxonomy.md`,
  `skills/legacy-step-contract/references/step-contract.md`,
  `skills/legacy-spec-writer/SKILL.md`, and the existing orchestrator routing
  table.
- Checked canonical source under
  `skills/legacy-modernization-decision-writer/`.
- Fixed contract drift in `SKILL.md`, `references/`, `templates/`, examples,
  `README.md`, orchestrator routing, and the Step Contract ID-minting table.
- Added `skills/legacy-modernization-decision-writer/scripts/smoke-test.sh`.
- Ran:
  - `skills/legacy-modernization-decision-writer/scripts/smoke-test.sh`
  - `bash -n skills/legacy-modernization-decision-writer/scripts/smoke-test.sh`
  - `ruby -e "require 'yaml'; YAML.load_file('skills/legacy-modernization-decision-writer/templates/modernization-decisions.yaml')"`
  - `git diff --check -- <reviewed decision-writer, adapter, README, orchestrator, and step-contract paths>`
  - `scripts/sync-skills.sh --target all --skill legacy-modernization-decision-writer --check`
  - `scripts/sync-skills.sh --target all --skill legacy-step-contract --check`
  - `scripts/sync-skills.sh --target all --skill legacy-modernization-orchestrator --check`
- Ran positive and negative no-write runtime smoke tests in Codex CLI
  (`gpt-5.4-mini`, read-only ephemeral), Claude Code (`haiku`, Read-only
  tools), and OpenCode (`opencode/minimax-m2.5-free`) on 2026-05-16.

## Mandatory Stop Conditions

No mandatory 8.0 cap conditions found.

The previous 9.0 runtime-execution cap is lifted. The synced skill was loaded
and used successfully in Codex, Claude Code, and OpenCode with the same positive
and negative no-write prompts on 2026-05-16.

## Weighted Score

| Category | Weight | Score | Weighted | Notes |
| --- | ---: | ---: | ---: | --- |
| Purpose and trigger clarity | 10% | 9.5 | 0.95 | Trigger and non-trigger cases are consistent with draft/in-review/approved spec states and optional DEC expansion. |
| Workflow completeness | 12% | 9.6 | 1.15 | Formal Step Contract summary, blocking gates, four-file package, and reconciliation back to `spec.yaml` are explicit. |
| IBM i / domain correctness | 14% | 9.5 | 1.33 | IBM i SME approval and architecture/product target authority are separated cleanly. |
| Evidence and anti-hallucination | 12% | 9.7 | 1.16 | Runtime negative smoke confirmed missing BR/BEH/EV, unknown sensitivity, and invented PostgreSQL/Kafka choices are blocked. |
| Output contract | 10% | 9.6 | 0.96 | YAML template is YAML-only; package output, status enums, reconciliation fields, and non-outputs are explicit. |
| Progressive disclosure | 8% | 9.2 | 0.74 | SKILL.md stays compact enough for runtime loading; detailed category guidance remains in references. |
| Runtime portability | 10% | 9.7 | 0.97 | Canonical and adapter copies sync cleanly; positive and negative runtime smoke passed in Codex, Claude Code, and OpenCode. |
| Reviewability and testability | 10% | 9.7 | 0.97 | Focused script plus cross-runtime no-write positive/negative prompts cover the main contract regression risks. |
| Engineering handoff value | 8% | 9.6 | 0.77 | Decision package avoids AC/task/design ownership and reconciles cleanly to spec for downstream handoff. |
| Maintainability | 6% | 9.5 | 0.57 | README, runtime matrix, smoke protocol, orchestrator, and Step Contract now match the skill's implemented status. |

Final score before cap: **9.56 / 10**

Final score after runtime-execution cap: **9.56 / 10**

Decision: **field-pilot ready**

## Findings Resolved In This Review

| ID | Severity | Finding | Fix |
| --- | --- | --- | --- |
| DEC-REV-001 | High | Skill introduced `needs_arch_review`, which is not a repository review-status enum. | Replaced with `needs_sme_review` plus `pending_approvals` for missing architecture/product authority. |
| DEC-REV-002 | High | Template minted `DECPKG-*`, an unregistered ID prefix. | Removed package ID prefix; package identity is path plus `STEP-*`. Smoke test blocks `DECPKG-*` in templates/examples/references. |
| DEC-REV-003 | High | Input contract blocked draft specs even though the skill is meant to resolve draft/in-review decisions. | Allowed draft, in-review, and approved specs; stop conditions now focus on missing grounding records and authorities. |
| DEC-REV-004 | Medium | Decision record template drifted into implementation task lists. | Replaced with a decision-level template that explicitly forbids task, code, API-contract, AC, and TC generation. |
| DEC-REV-005 | Medium | `modernization-decisions.yaml` mixed YAML with Markdown sections. | Rewrote as YAML-only with schema version, `STEP-*`, decisions, summary, and traceability index. |
| DEC-REV-006 | Medium | Orchestrator and README still treated the skill as proposed or skipped architecture authority. | Updated README status and orchestrator skip criteria. |
| DEC-REV-007 | Medium | Step Contract had no optional decision-writing ID policy. | Added optional modernization decision writing row and package status enum. |

## Runtime Execution Evidence

| Runtime | Model | Positive No-Write Smoke | Negative No-Write Smoke | Result |
| --- | --- | --- | --- | --- |
| Codex CLI | `gpt-5.4-mini` | Returned canonical `05_decisions/ORDERS/` four-file package, approved DEC, no pending approvals, reconciliation target, and forbidden outputs. | Blocked invented PostgreSQL/Kafka DEC with missing BR/BEH/EV, unknown sensitivity, missing authority, and unresolved blocking TBD. | Passed |
| Claude Code | `haiku` with Read-only tools | Returned canonical four-file package, approved DEC, no pending approvals, reconciliation target, and no writes. | Blocked approval and routed to `legacy-spec-writer` for BR/BEH/EV repair, sensitivity resolution, authority assignment, and TBD resolution. | Passed |
| OpenCode | `opencode/minimax-m2.5-free` | Returned canonical four-file package, approved DEC, no pending approvals, reconciliation target, and no writes. | Blocked approval, kept DEC `draft`, required TBD resolution, and confirmed no writes. | Passed |

Codex emitted unrelated skill-load warnings for broken non-target skills and a
plugin-cache 403 warning, but `/legacy-modernization-decision-writer` loaded and
executed correctly.

## Remaining Post-Pilot Improvements

| ID | Severity | Finding | Required Change |
| --- | --- | --- | --- |
| DEC-REV-009 | Medium | Examples are illustrative, not derived from a real field BRD/spec package. | Add one real or realistic end-to-end decision package after a field-style capability is available. |

## SME Review

- [x] SME governance is explicit.
- [x] Observed behavior, inferred rule, and modernization decision are separate.
- [x] Evidence tags are required.
- [x] IBM i SME does not approve target architecture alone.
- [x] Open questions / TBDs are carried forward instead of hidden.

Notes:

The skill is conservative in the right places. It allows the decision writer to
expand and govern `DEC-*` records without becoming the spec writer, architecture
designer, or implementation planner.

## Runtime Portability Review

- [x] canonical source under `skills/<skill-name>/`
- [x] Claude Code adapter copy synced
- [x] OpenCode adapter copy synced
- [x] Codex adapter copy synced
- [x] runtime-specific metadata absent from canonical skill

Notes:

`scripts/sync-skills.sh --target all --skill legacy-modernization-decision-writer --check`
passes after sync. Runtime smoke also proves the synced copies can be loaded and
used by Codex, Claude Code, and OpenCode. Step Contract and orchestrator
adapters were also synced because this review changed their canonical sources.

## Adversarial Pass

| Scenario | Expected Behavior | Result |
| --- | --- | --- |
| Draft spec contains unresolved DEC records | Accept and expand the decisions if BR/BEH/EV grounding exists | Covered |
| DEC references missing BR/BEH/EV | Stop and route to spec repair | Covered |
| Architecture owner missing | DEC remains `draft` or `needs_sme_review` with `pending_approvals` | Covered |
| Target platform says only "cloud" | File `TBD-*`; do not invent technology | Covered |
| Existing ACs missing | Route back to spec-writer; do not mint ACs | Covered |
| Blocking TBD remains | Decision package cannot be approved | Covered |
| Decision package not reconciled to spec | Forward Handoff Gate remains blocked | Covered |

## Approval Summary

| Criterion | Status |
| --- | --- |
| No mandatory stop conditions | Pass |
| Score >= 9.5 | Pass |
| Portable canonical layout | Pass |
| Adapter drift check | Pass |
| Three-runtime positive/negative smoke | Pass |
| SME governance clear | Pass |
| Anti-hallucination rules present | Pass |
| Output contract enforceable | Pass |
| Smoke test present | Pass |

**APPROVAL DECISION**: **FIELD-PILOT READY**
