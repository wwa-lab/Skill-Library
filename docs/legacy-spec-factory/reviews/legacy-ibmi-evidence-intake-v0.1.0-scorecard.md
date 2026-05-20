---
skill: legacy-ibmi-evidence-intake
scorecard_version: v0.1.0
static_score: 9.16
decision: repo-ready
status: current
last_verified: 2026-05-15
runtimes_tested:
  codex: { status: passed, model: gpt-5.4-mini, date: 2026-05-15 }
  claude_code: { status: passed, model: haiku, date: 2026-05-15 }
  opencode: { status: passed, model: minimax-m2.5-free, date: 2026-05-15 }
evidence_source: docs/runtime-matrix.md
---

# Skill Review Scorecard: legacy-ibmi-evidence-intake v0.1.0

## Metadata

- skill_name: legacy-ibmi-evidence-intake
- skill_path: skills/legacy-ibmi-evidence-intake
- reviewed_version: v0.1.0
- generated_by: Claude Code; hardened by Codex
- reviewed_by: Codex
- review_date: 2026-05-15
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
- Checked canonical source under `skills/legacy-ibmi-evidence-intake/`.
- Checked `SKILL.md`, manifest/redaction/checklist templates, references, and
  examples.
- Hardened the skill so the agent must not read, transform, summarize, or
  quote unredacted sensitive evidence. Raw or unknown-sensitivity evidence is
  handled only as metadata until a redaction owner approves a safe redacted
  artifact.
- Moved detailed evidence typing and redaction procedure out of `SKILL.md`
  into references, keeping the runtime path shorter and more portable.
- Added positive and blocked example packages with manifest, redaction log, and
  review checklist artifacts.
- Repaired the manifest contract so it separates `draft`, `blocked`, and
  `approved_for_inventory` package states.
- Added type-specific `source_location` shapes so source members, DB metadata,
  job logs, screen samples, transaction samples, and reports no longer pretend
  to share one object-member schema.
- Standardized gate status on the Step Contract compact result vocabulary:
  `pass`, `pass_with_warnings`, and `blocked`.
- Hardened redaction guidance for rule-critical thresholds, coefficients, and
  amounts so synthetic replacements cannot be mistaken for exact legacy rules.
- Added Evidence intake to the Step Contract ID minting table.
- Ran `scripts/sync-skills.sh --target all`; runtime adapter copies were
  created for Codex, Claude Code, OpenCode, and `.agents`.
- Ran `scripts/sync-skills.sh --check`; adapter drift check passed.
- Ran YAML and manifest-state validation for canonical templates/examples and
  runtime manifest templates.
- Ran Skill Creator quick validation; skill is valid.
- Tightened the positive smoke prompt so it explicitly records redaction-owner
  and SME approval dates instead of only saying owners were assigned.
- Updated the OpenCode smoke instructions to run in a disposable copy because
  `opencode run --help` does not expose a read-only mode.
- Removed remaining old status language from `SKILL.md` and replaced it with
  `review_status`, `intake_decision.status`, and `unresolved_items` vocabulary.
- Removed an unsupported percentage inference from the sample-data redaction
  example.
- Reran complete positive and negative smoke on 2026-05-15:
  - Codex CLI (`gpt-5.4-mini`, read-only ephemeral) passed the positive case by
    returning the required output files, allowing downstream inventory, and
    reporting `approved_for_inventory` / `pass`; it passed the negative case by
    blocking unknown-sensitivity evidence with no redaction-owner review.
  - Claude Code (`haiku`) initially produced no output in the default Codex
    execution sandbox and was stopped with exit code 143. A debug run showed
    EPERM errors writing Claude config/telemetry files under `/Users/leo`.
    Rerunning with Claude auth/config/network access passed: the positive case
    returned `pass_with_warnings` with downstream inventory allowed, and the
    negative case returned `blocked` for unknown sensitivity with no
    redaction-owner review.
  - OpenCode (`minimax-m2.5-free`) passed the positive and negative cases in
    disposable copies. No `evidence/` directory was created in either disposable
    copy or the real repository.

## Mandatory Stop Conditions

No mandatory 8.0 cap conditions found after Codex hardening.

No 9.0 runtime-testing cap remains after the 2026-05-15 smoke rerun.

The weighted score remains below the 9.5 field-pilot threshold because the
positive compact response is passable but still not deterministic enough for a
pilot gate.

## Weighted Score

| Category | Weight | Score | Weighted |
| --- | ---: | ---: | ---: |
| Purpose and trigger clarity | 10% | 9.3 | 0.93 |
| Workflow completeness | 12% | 9.4 | 1.13 |
| IBM i / domain correctness | 14% | 9.3 | 1.30 |
| Evidence and anti-hallucination | 12% | 9.5 | 1.14 |
| Output contract | 10% | 9.4 | 0.94 |
| Progressive disclosure | 8% | 9.3 | 0.74 |
| Runtime portability | 10% | 9.5 | 0.95 |
| Reviewability and testability | 10% | 9.4 | 0.94 |
| Engineering handoff value | 8% | 9.4 | 0.75 |
| Maintainability | 6% | 9.3 | 0.56 |

Static score before cap: **9.38 / 10**

Current score after cap: **9.38 / 10**

Decision: **repo-ready, not field-pilot ready**

## Findings

### Remaining For 9.5

| ID | Severity | Finding | Required Change | Affects |
| --- | --- | --- | --- | --- |
| EVID-INTAKE-REV-013 | Medium | Positive compact smoke output is passable but not deterministic enough: Claude returned `pass_with_warnings` and allowed inventory, but also expanded into directory layout, inferred non-blocking optional gaps, and used mixed compact-status wording. | Tighten the compact-response instructions and/or examples so short smoke prompts return the three requested fields with a machine-readable `intake_decision.status`, `downstream_inventory_allowed`, and no extra directory tree unless explicitly requested. | Reviewability, downstream automation |

### Resolved In This Hardening Pass

| ID | Status | Finding | Resolution | Affects |
| --- | --- | --- | --- | --- |
| EVID-INTAKE-REV-002 | Resolved | `SKILL.md` was long and contained detailed procedural guidance that could move into references. | Condensed runtime workflow and relied on `references/evidence-types.md`, `references/redaction-checklist.md`, and `references/output-contract.md` for details. | Progressive disclosure, maintainability |
| EVID-INTAKE-REV-003 | Resolved | Examples were useful but lightweight compared with the risk of evidence intake. | Added positive and blocked example packages with manifest, redaction log, checklist, and expected review notes. | Reviewability, evidence governance |
| EVID-INTAKE-REV-004 | Resolved | The manifest contract used one rigid source-member shape while templates/examples used job-log, screen, and transaction-specific metadata. | Added base evidence fields plus type-specific schemas for source members, DB metadata, job logs, screen samples, transaction samples, and spool/report evidence; updated templates and examples to match. | Output contract, downstream automation |
| EVID-INTAKE-REV-005 | Resolved | Blocked draft manifests and approved handoff manifests were not explicitly separated. | Added `package_state`, `intake_decision`, and `unresolved_items`; allowed `unknown` sensitivity and null redacted paths only in draft/blocked packages tied to `TBD-*` items. | Evidence integrity, SME governance |
| EVID-INTAKE-REV-006 | Resolved | Status vocabulary drifted across manifests, redaction logs, review checklists, and Step Contract terminology. | Standardized package/gate decisions on `pass`, `pass_with_warnings`, and `blocked`; kept item review state separate from redaction status. | Output contract, maintainability |
| EVID-INTAKE-REV-007 | Resolved | Redaction examples could cause synthetic thresholds or amounts to be inferred as exact legacy rules. | Added synthetic-value guidance and required semantic preservation notes for changed rule-critical constants, thresholds, coefficients, and amounts. | IBM i correctness, evidence integrity |
| EVID-INTAKE-REV-008 | Resolved | Evidence intake minted `EV-*` IDs but the Step Contract ID minting table did not list the pre-inventory step. | Added Evidence intake to the Step Contract minting table with `EV-*`, `TBD-*`, and `STEP-*`. | Runtime contract, downstream automation |
| EVID-INTAKE-REV-009 | Resolved | Positive smoke prompt said owners were assigned while pass criteria required approvals recorded. | Updated prompt and reference commands to include redaction-owner approval date and SME approval date. | Reviewability, runtime smoke |
| EVID-INTAKE-REV-010 | Resolved | OpenCode smoke command could write into the real repository. | Removed the direct OpenCode command and documented disposable-copy execution with a post-run `git status --short` check. | Runtime portability, repository safety |
| EVID-INTAKE-REV-011 | Resolved | `SKILL.md` retained old status language (`approved with notes`, `status: blocking`). | Replaced with canonical `review_status`, `intake_decision.status`, and `unresolved_items[].blocks_inventory` wording. | Output contract, maintainability |
| EVID-INTAKE-REV-012 | Resolved | Sample-data redaction text inferred an unsupported approval rate from three synthetic rows. | Reworded the example to say only that decision-code structure and amount scale are preserved. | Evidence integrity, anti-hallucination |
| EVID-INTAKE-REV-001 | Resolved | Three-runtime smoke evidence was incomplete. | Reran positive and negative smoke in Codex CLI, Claude Code, and OpenCode on 2026-05-15. All three runtimes passed after rerunning Claude Code with access to its auth/config/network files. | Runtime portability, reviewability |

### Strengths

- Establishes evidence IDs before inventory, giving downstream artifacts a
  stronger traceability root.
- Separates evidence registration, redaction approval, SME review, and
  downstream analysis.
- Explicitly blocks agent inspection of unredacted sensitive content.
- Provides manifest, redaction log, review checklist, references, and examples.
- Syncs cleanly into all runtime adapter folders.

## SME Review

- [x] SME governance is explicit
- [x] Observed evidence, redaction decisions, and downstream analysis are separate
- [x] Evidence IDs are required
- [x] IBM i evidence sources are covered
- [x] Open questions / TBDs are carried forward instead of hidden

Notes:

The skill is repo-ready because it was hardened to avoid exposing raw sensitive
evidence to the agent and now includes a realistic blocked intake example.
Field-pilot use should wait for one more compact-output hardening pass.

## Runtime Portability Review

- [x] canonical source under `skills/legacy-ibmi-evidence-intake/`
- [x] Claude Code adapter or copy defined
- [x] OpenCode adapter or copy defined
- [x] Codex adapter or copy defined
- [x] runtime-specific metadata isolated from canonical skill

Notes:

Adapter drift check passes. Codex, Claude Code, and OpenCode positive and
negative smoke pass. Claude Code requires execution with access to its
auth/config/network files; the default Codex sandbox caused the earlier timeout.

## Requested Revision Prompt For Claude Code

```text
Revise legacy-ibmi-evidence-intake to move from 9.0/10 (repo-ready)
toward 9.5/10 (field-pilot ready).

Current score: 9.38/10 after the runtime-testing cap was removed.
Target score: 9.5/10.

Blocking issues:
1. Positive compact smoke output is passable but not deterministic enough for a
   field-pilot gate.

Required changes:
- Tighten compact-response instructions and examples so runtime smoke returns
  the three requested fields with machine-readable status values.
- Do not emit an evidence directory tree unless the user explicitly asks for
  file organization.
- Rerun positive and negative smoke in Codex CLI, Claude Code, and OpenCode.
- Keep OpenCode smoke in a disposable copy/worktree unless a read-only mode becomes available.
- Update docs/runtime-matrix.md with exact runtime, model, date, and pass/fail result.
- Refresh this scorecard after smoke evidence is recorded.

Do not remove author/copyright notices.
Keep the canonical skill under skills/legacy-ibmi-evidence-intake/.
Maintain compatibility with Codex, Claude Code, and OpenCode.
```
