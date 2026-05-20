---
skill: legacy-ibmi-program-analyzer
scorecard_version: v0.1.0
static_score: 9.39
decision: repo-ready
status: current
last_verified: not-yet-tested
runtimes_tested:
  codex: { status: synced, model: gpt-5.4-mini, date: null }
  claude_code: { status: synced, model: haiku, date: null }
  opencode: { status: synced, model: minimax-m2.5-free, date: null }
evidence_source: docs/runtime-matrix.md
---

# Skill Review Scorecard: legacy-ibmi-program-analyzer v0.1.0

## Metadata

- skill_name: legacy-ibmi-program-analyzer
- skill_path: skills/legacy-ibmi-program-analyzer
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
- Checked canonical source under `skills/legacy-ibmi-program-analyzer/`.
- Checked output template, references, and positive / negative examples.
- Ran `scripts/sync-skills.sh --target all --check`; all runtime adapter copies
  reported `OK`.
- Checked `docs/runtime-matrix.md`; all target runtimes are still `synced`, not
  `loaded`, `executed`, or `passed`.
- Checked `docs/runtime-smoke-tests.md`; positive and negative
  `legacy-ibmi-program-analyzer` smoke prompts now exist. Execution results in
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
| Purpose and trigger clarity | 10% | 9.7 | 0.97 |
| Workflow completeness | 12% | 9.5 | 1.14 |
| IBM i / domain correctness | 14% | 9.2 | 1.29 |
| Evidence and anti-hallucination | 12% | 9.7 | 1.16 |
| Output contract | 10% | 9.4 | 0.94 |
| Progressive disclosure | 8% | 9.3 | 0.74 |
| Runtime portability | 10% | 9.0 | 0.90 |
| Reviewability and testability | 10% | 9.2 | 0.92 |
| Engineering handoff value | 8% | 9.5 | 0.76 |
| Maintainability | 6% | 9.4 | 0.56 |

Final score before cap: **9.39 / 10**

Final score after cap: **9.0 / 10**

Decision: **repo-ready, not field-pilot ready**

## Findings

### Blocking For 9.5

✅ **All 5 findings resolved (2026-05-14)**

| ID | Severity | Finding | Resolution | Commit |
| --- | --- | --- | --- | --- |
| PROG-REV-001 | High | Runtime portability not tested | ✅ Added positive and negative smoke test prompts + pass criteria to `docs/runtime-smoke-tests.md` (lines 293–380). Ready for execution in Codex CLI, Claude Code, OpenCode. | 99e27f4 |
| PROG-REV-002 | Medium | RPGLE/CLLE terminology imprecise | ✅ Fixed SKILL.md step 2: added fixed-form `P...B/E`, free-form `dcl-proc/end-proc`, `BEGSR/ENDSR`, CLLE `SUBR/CALLSUBR` (lines 71–76). | 99e27f4 |
| PROG-REV-003 | Medium | File I/O coverage incomplete | ✅ Expanded SKILL.md step 6: added `READ`, `READP`, `READPE`, `EXFMT`, embedded SQL/SQLRPGLE (lines 127–137). Updated output-contract.md requirements (lines 334–349). | 99e27f4 |
| PROG-REV-004 | Medium | Blocked-source status inconsistent | ✅ Added `blocked_pending_source` to output-contract.md status values (line 512). Updated template to show all status options (line 14). | 99e27f4 |
| PROG-REV-005 | Low | References not linked | ✅ Linked `references/evidence-tagging.md` and `templates/evidence-tags.md` from SKILL.md Use section (lines 50–51). | 99e27f4 |

### Strengths

- Clear trigger and non-goals: one IBM i program, no business-rule invention, no
  modernization code generation.
- Strong stop conditions for missing source, blocked inventory, unknown program
  ID, and raw production data.
- Output contract is specific and downstream-friendly: metadata, entry points,
  call graph, object dependencies, file I/O, external calls, error handling,
  TBDs, and SME sign-off.
- Call graph handling is stronger than the baseline: it separates source-level
  flow headers from code-derived call sites and requires drift TBDs.
- Anti-hallucination instructions are direct and operational, with concrete
  examples of what to do instead of guessing.
- Positive and negative examples exercise both a simple RPGLE path and an
  incomplete-source stop condition.

## SME Review

- [x] SME governance is explicit
- [x] Observed behavior, inferred rule, and modernization decision are separate
- [x] Evidence tags are required
- [x] IBM i-specific failure modes are covered
- [x] Open questions / TBDs are carried forward instead of hidden

Notes:

The skill keeps SMEs in the approval loop and uses TBDs correctly for missing
DDS, missing subroutines, unclear external parameters, and comment/code drift.
The IBM i terminology and I/O hardening requested in the original review was
completed in commit `99e27f4`; the remaining field-pilot blocker is runtime
smoke execution evidence.

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
| Program ID missing from approved inventory | Stop and require inventory correction | Covered |
| Inventory marks program `blocked` | Stop instead of analyzing | Covered |
| Program source incomplete | Create pending-source TBDs and avoid guessing | Covered, but status contract needs alignment |
| DDS missing for referenced file | Create pending-source TBD and avoid field meaning inference | Covered |
| Source-level flow header disagrees with actual calls | Prefer code for behavior and create drift TBD | Covered |
| External call parameters undocumented | Tag `needs_sme_review` and create TBD | Covered |
| Embedded SQL / SQLRPGLE program | Should capture DB2 for i access and SQL status handling | Needs hardening |
| Runtime adapter folder differs from canonical path depth | Should keep relative links portable after sync | Structurally covered; smoke not run |

## Requested Revision Prompt For Claude Code

```text
Revise legacy-ibmi-program-analyzer to finish the remaining review finding.

Current score: 9.0/10 after the runtime-testing cap.
Target score: 9.5/10.

Blocking issue:
1. Three-runtime smoke execution evidence is missing.

Required changes:
- Run the smoke protocol in Codex CLI, Claude Code, and OpenCode; update `docs/runtime-matrix.md` with exact runtime/model/date notes.
- If all three pass, update this scorecard from repo-ready to field-pilot ready
  and lift the runtime cap.

Do not remove author/copyright notices.
Keep the canonical skill under skills/legacy-ibmi-program-analyzer/.
Maintain compatibility with Codex, Claude Code, and OpenCode.
```
