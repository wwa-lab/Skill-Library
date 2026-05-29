---
skill: legacy-flow-context-normalizer
scorecard_version: v0.1.4
static_score: 9.46
decision: repo-ready
status: superseded
last_verified: 2026-05-27
runtimes_tested:
  codex: { status: synced, model: gpt-5.4-mini, date: 2026-05-27 }
  claude_code: { status: synced, model: haiku, date: 2026-05-27 }
  opencode: { status: synced, model: minimax-m2.5-free, date: 2026-05-27 }
evidence_source: docs/runtime-matrix.md
---

# Skill Review Scorecard: legacy-flow-context-normalizer v0.1.4

## Metadata

- skill_name: legacy-flow-context-normalizer
- skill_path: skills/legacy-flow-context-normalizer
- reviewed_version: v0.1.4
- generated_by: Codex
- reviewed_by: Codex
- review_date: 2026-05-27
- target_runtime:
  - [x] Codex
  - [x] Claude Code
  - [x] OpenCode
- decision:
  - [ ] reject
  - [ ] revise
  - [x] repo-ready
  - [ ] field-pilot ready

## Review Focus

v0.1.4 adds an input quality ladder so the skill has a useful response across
strong, partial, sparse, and blocked input sets. The important new behavior is
`L1 sparse`: authorized readable documents that are module-relevant but cannot
support even one safe flow now produce a source-quality triage package with
placeholder views and supplement requests, not invented flow content.

## Mandatory Stop Conditions

No mandatory 8.0 cap conditions found.

The runtime cap still applies because the skill has been synced but not yet run
through positive, partial-input, sparse-triage, and negative no-write execution
smoke in Codex, Claude Code, and OpenCode.

## Weighted Score

| Category | Weight | Score | Weighted |
| --- | ---: | ---: | ---: |
| Purpose and trigger clarity | 10% | 9.7 | 0.97 |
| Workflow completeness | 12% | 9.8 | 1.18 |
| IBM i / domain correctness | 14% | 9.1 | 1.27 |
| Evidence and anti-hallucination | 12% | 9.7 | 1.16 |
| Output contract | 10% | 9.7 | 0.97 |
| Progressive disclosure | 8% | 9.6 | 0.77 |
| Runtime portability | 10% | 9.1 | 0.91 |
| Reviewability and testability | 10% | 9.8 | 0.98 |
| Engineering handoff value | 8% | 9.8 | 0.78 |
| Maintainability | 6% | 9.3 | 0.56 |

Final score before cap: **9.46 / 10**

Final score after cap: **9.0 / 10**

## Decision

Repo-ready, not field-pilot ready.

## Blocking For 9.5

| ID | Finding | Required Change | Affects |
| --- | --- | --- | --- |
| LFCN-REV-001 | Runtime loading and no-write execution have not been verified in all three runtimes. | Run positive, partial-input, sparse-triage, and negative smoke prompts in Codex, Claude Code, and OpenCode; update runtime matrix and scorecard. | Runtime portability, reviewability |
| LFCN-REV-002 | Mermaid diagrams are structurally required, but not rendered in runtime smoke yet. | Add smoke evidence that each runtime emits valid Mermaid diagrams and does not draw unsupported edges. | SME reviewability, evidence integrity |
| LFCN-REV-003 | Excel extractor has unit tests against synthetic OpenXML fixtures, not real field workbooks. | Run one pilot workbook with multiple sheets and messy headers; harden classification and row summarization if needed. | SME correctness, handoff value |
| LFCN-REV-004 | Sparse-input triage is documented and covered by smoke prompts, but not yet runtime-executed. | Execute the sparse-input smoke and confirm the skill emits `triage_needs_source_enrichment` rather than inventing a flow. | User experience, anti-hallucination |

## Strengths

- The skill now has explicit behavior for high-quality, partial, sparse, and
  truly blocked input sets.
- Sparse authorized inputs still produce an actionable artifact: source
  assessment, placeholder views, and a focused supplement request.
- The new status prevents sparse packages from being mistaken for context
  intake or BRD-ready material.
- Existing Mermaid, Excel, and missing-view placeholder behavior remains
  intact.

## Verification

```bash
python3 -m unittest tests/test_flow_context_excel_extractor.py

python3 skills/legacy-flow-context-normalizer/scripts/validate_flow_context_package.py \
  skills/legacy-flow-context-normalizer/examples/minimal-positive

python3 skills/legacy-flow-context-normalizer/scripts/validate_flow_context_package.py \
  --allow-blocked \
  skills/legacy-flow-context-normalizer/examples/blocked-authorization-negative
```

All commands returned successfully during local structural verification.

## Runtime Smoke Status

| Runtime | Status | Evidence |
| --- | --- | --- |
| Codex | synced | Adapter copy synced from canonical source on 2026-05-27 |
| Claude Code | synced | Adapter copy synced from canonical source on 2026-05-27 |
| OpenCode | synced | Adapter copy synced from canonical source on 2026-05-27 |

## Requested Next Revision

Run runtime smoke with:

1. A positive mixed-document prompt that includes a multi-sheet Excel workbook
   and expects four view files, each with a Mermaid diagram and evidence table.
2. A partial-input prompt with only Interfaces and Data Dictionary sheets that
   must produce draft or `ready_with_warnings`, not a block.
3. A sparse-input prompt with authorized module notes but no safe sequence that
   must produce `triage_needs_source_enrichment`.
4. A negative prompt with unknown source authorization that must route to
   `legacy-ibmi-evidence-intake` without extracting sensitive content.

Keep the canonical skill under `skills/legacy-flow-context-normalizer/`.
