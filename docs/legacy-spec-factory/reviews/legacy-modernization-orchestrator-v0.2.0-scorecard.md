---
skill: legacy-modernization-orchestrator
scorecard_version: v0.2.0
static_score: 9.34
decision: repo-ready
status: superseded
last_verified: 2026-05-14
runtimes_tested:
  codex: { status: synced, model: gpt-5.4-mini, date: null }
  claude_code: { status: passed, model: haiku, date: 2026-05-14 }
  opencode: { status: synced, model: minimax-m2.5-free, date: null }
evidence_source: docs/runtime-matrix.md
---

# Skill Review Scorecard: legacy-modernization-orchestrator v0.2.0

## Metadata

- skill_name: legacy-modernization-orchestrator
- skill_path: skills/legacy-modernization-orchestrator
- reviewed_version: v0.2.0
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
- Checked canonical source under `skills/legacy-modernization-orchestrator/`.
- Checked `SKILL.md`, `references/stage-identification.md`,
  `references/routing-decision-table.md`, `references/gates.md`,
  `references/manual-fallback.md`, and all orchestrator examples.
- Compared v0.2.0 against the prior v0.1.1 scorecard, which was field-pilot
  ready for the narrower routing scope.
- Ran `scripts/sync-skills.sh --check`; all runtime adapter copies reported
  `OK`.
- Checked `docs/runtime-matrix.md`; v0.2.0 is synced in Codex, Claude Code,
  and OpenCode, but no v0.2.0 smoke pass has been recorded.
- Checked `docs/runtime-smoke-tests.md`; the orchestrator smoke prompts still
  cover the v0.1.1 evidence-ready and inventory-blocked routes, but do not
  exercise the new flow-analysis, module-analysis, or spec-writer routing paths.

## Mandatory Stop Conditions

No mandatory 8.0 cap conditions found.

- valid `SKILL.md` exists
- `name` / `description` frontmatter is clear
- copyright / author notice is present
- canonical source and runtime adapters are portable and drift-free
- trigger conditions are clear
- routing output contract is explicit
- SME governance and hard gates are explicit
- anti-hallucination rules forbid invented maturity, skipped gates, and
  assumed skill availability

One 9.0 cap applies:

- **Runtime portability for v0.2.0 has not been smoke-tested.** The v0.1.1
  smoke pass covered the old scope; v0.2.0 added flow, module, and spec routes
  that have not been executed in Codex CLI, Claude Code, and OpenCode.

## Weighted Score

| Category | Weight | Score | Weighted |
| --- | ---: | ---: | ---: |
| Purpose and trigger clarity | 10% | 9.6 | 0.96 |
| Workflow completeness | 12% | 9.4 | 1.13 |
| IBM i / domain correctness | 14% | 9.2 | 1.29 |
| Evidence and anti-hallucination | 12% | 9.5 | 1.14 |
| Output contract | 10% | 9.4 | 0.94 |
| Progressive disclosure | 8% | 9.3 | 0.74 |
| Runtime portability | 10% | 9.0 | 0.90 |
| Reviewability and testability | 10% | 9.2 | 0.92 |
| Engineering handoff value | 8% | 9.3 | 0.74 |
| Maintainability | 6% | 9.3 | 0.56 |

Static score before cap: **9.34 / 10**

Current score after cap: **9.0 / 10**

Decision: **repo-ready, not field-pilot ready**

## Findings

### Blocking For 9.5

| ID | Severity | Finding | Required Change | Affects |
| --- | --- | --- | --- | --- |
| ORCH-V020-REV-001 | High | v0.2.0 has not passed runtime smoke for the expanded routing surface. | ✅ Partially resolved. Added expanded v0.2.0 smoke prompts for program -> flow, flow -> module, module -> spec, and blocked forward handoff. Evidence-ready and inventory-blocked routes smoke tested in Claude Code (haiku, 2026-05-14). Codex/OpenCode and expanded-route execution remain pending. | Runtime portability, reviewability |
| ORCH-V020-REV-002 | Resolved | Active inventory-done example treated `legacy-ibmi-program-analyzer` as planned. | Replaced with an implemented-skill route to `legacy-ibmi-program-analyzer`. | Workflow completeness, engineering handoff |
| ORCH-V020-REV-003 | Resolved | `references/manual-fallback.md` described implemented MVP skills as planned/manual. | Updated fallback guidance so implemented MVP skills route directly; fallback applies to genuinely planned/future/deferred or unavailable skills. | Maintainability, routing correctness |
| ORCH-V020-REV-004 | Resolved | The top-level Reverse Chain Map presented folded/subsumed analyzers as active route nodes. | Rewrote the map around the current MVP path and labeled folded capabilities clearly. | Trigger clarity, workflow completeness |
| ORCH-V020-REV-005 | Resolved | Stage directory table used legacy `02_static-analysis/` paths. | Aligned stage directories to `02_programs/`, `03_flows/`, `04_modules/`, and `05_specs/`. | Engineering handoff, maintainability |

### Strengths

- The core router discipline from v0.1.1 remains intact: it refuses unsafe
  skips, checks hard gates, and keeps the orchestrator in a router-only role.
- v0.2.0 correctly adds the missing MVP route spine: inventory -> program
  analysis -> flow analysis -> module analysis -> spec writer.
- The Step Contract section is now strong enough for automation to consume
  compact routing results (`status`, `downstream_next_step`,
  `remediation_step`, blocking IDs).
- Active examples and fallback references now match the implemented MVP skill
  set rather than the old planned-skill posture.
- SME control points are still explicit and appropriately non-bypassable.
- Adapter sync is clean across Codex, Claude Code, OpenCode, and `.agents`.

## SME Review

- [x] SME governance is explicit
- [x] Observed behavior, inferred rule, and modernization decision are separate
- [x] Evidence tags are required
- [x] IBM i-specific failure modes are covered at the routing/gate level
- [x] Open questions / TBDs are carried forward instead of hidden

Notes:

The orchestrator still treats SMEs as the approval authority for inventory
coverage, inferred business rules, spec approval, waivers, and forward handoff.
The remaining gaps are not SME-governance gaps; they are routing-reference and
test-evidence gaps introduced by the expanded v0.2.0 scope.

## Runtime Portability Review

- [x] canonical source under `skills/legacy-modernization-orchestrator/`
- [x] Claude Code adapter or copy defined
- [x] OpenCode adapter or copy defined
- [x] Codex adapter or copy defined
- [x] runtime-specific metadata isolated from canonical skill

Notes:

`scripts/sync-skills.sh --check` reports all runtime copies as `OK`. The
field-pilot cap remains because v0.2.0's new routes have not passed the
runtime smoke protocol in all three target runtimes.

## Adversarial Pass

| Scenario | Expected Behavior | Result |
| --- | --- | --- |
| Evidence has unknown sensitivity | Stop at Redaction Gate | Covered |
| Inventory has blocking coverage gaps | Stop at Inventory Completeness Gate and route to inventory resume / SME waiver | Covered |
| User has all program analyses and wants a call-chain view | Route to `legacy-ibmi-flow-analyzer` | Covered in routing table, not smoke-tested |
| User has all approved flows and wants module synthesis | Route to `legacy-ibmi-module-analyzer` | Covered in routing table, not smoke-tested |
| User has approved module analysis and wants a spec | Route to `legacy-spec-writer` | Covered in routing table, not smoke-tested |
| Draft spec is requested for forward SDLC | Refuse handoff; require review, SME approval, and Forward Handoff Gate | Covered |
| User follows active example after inventory approval | Should route to implemented program analyzer | Covered |
| User opens manual fallback for spec writer | Should avoid fallback because spec writer is implemented | Covered |
| COBOL evidence bundle arrives | Route to future/manual COBOL inventory fallback | Covered |
| Folded CRUD/DDS/call-graph request arrives | Route through program/flow/module analyzers rather than separate planned skills | Covered in table, partially obscured by top-level map |

## Requested Revision Prompt For Claude Code

```text
Revise legacy-modernization-orchestrator v0.2.0 to move from 9.0/10
(repo-ready) toward 9.5/10 (field-pilot ready).

Current score: 9.0/10 after the remaining runtime-testing cap.
Target score: 9.5/10.

Blocking issues:
1. v0.2.0's expanded routes have not passed runtime smoke in Codex CLI,
   Claude Code, and OpenCode.

Required changes:
- Run the new smoke prompts in Codex CLI, Claude Code, and OpenCode; update
  `docs/runtime-matrix.md` and this scorecard afterward.

Do not remove author/copyright notices.
Keep the canonical skill under skills/legacy-modernization-orchestrator/.
Maintain compatibility with Codex, Claude Code, and OpenCode.
Do not let the orchestrator produce downstream business artifacts; it remains
the router and gatekeeper.
```
