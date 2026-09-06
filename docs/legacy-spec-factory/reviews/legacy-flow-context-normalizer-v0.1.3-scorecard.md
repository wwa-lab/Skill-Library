---
skill: legacy-flow-context-normalizer
scorecard_version: v0.1.3
static_score: 9.44
decision: repo-ready
status: superseded
last_verified: 2026-05-27
runtimes_tested:
  codex: { status: synced, model: gpt-5.4-mini, date: 2026-05-27 }
  claude_code: { status: synced, model: haiku, date: 2026-05-27 }
  opencode: { status: synced, model: minimax-m2.5-free, date: 2026-05-27 }
evidence_source: docs/runtime-matrix.md
---

# Skill Review Scorecard: legacy-flow-context-normalizer v0.1.3

## Metadata

- skill_name: legacy-flow-context-normalizer
- skill_path: skills/legacy-flow-context-normalizer
- reviewed_version: v0.1.3
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

v0.1.3 makes missing flow coverage a soft UX gate instead of a hard block.
If teams have only partial documents, the skill still produces all four view
files, carries absent views as Mermaid placeholders plus `TBD-*` questions,
and routes the package to SME review or SME-accepted `ready_with_warnings`
instead of forcing users to stop.

## Mandatory Stop Conditions

No mandatory 8.0 cap conditions found.

The runtime cap still applies because the skill has been synced but not yet run
through positive, partial-input, and negative no-write execution smoke in
Codex, Claude Code, and OpenCode.

## Weighted Score

| Category | Weight | Score | Weighted |
| --- | ---: | ---: | ---: |
| Purpose and trigger clarity | 10% | 9.7 | 0.97 |
| Workflow completeness | 12% | 9.7 | 1.16 |
| IBM i / domain correctness | 14% | 9.1 | 1.27 |
| Evidence and anti-hallucination | 12% | 9.6 | 1.15 |
| Output contract | 10% | 9.7 | 0.97 |
| Progressive disclosure | 8% | 9.5 | 0.76 |
| Runtime portability | 10% | 9.1 | 0.91 |
| Reviewability and testability | 10% | 9.7 | 0.97 |
| Engineering handoff value | 8% | 9.8 | 0.78 |
| Maintainability | 6% | 9.4 | 0.56 |

Final score before cap: **9.44 / 10**

Final score after cap: **9.0 / 10**

## Decision

Repo-ready, not field-pilot ready.

## Blocking For 9.5

| ID | Finding | Required Change | Affects |
| --- | --- | --- | --- |
| LFCN-REV-001 | Runtime loading and no-write execution have not been verified in all three runtimes. | Run positive, partial-input, and negative smoke prompts in Codex, Claude Code, and OpenCode; update runtime matrix and scorecard. | Runtime portability, reviewability |
| LFCN-REV-002 | Mermaid diagrams are structurally required, but not rendered in runtime smoke yet. | Add smoke evidence that each runtime emits valid Mermaid diagrams and does not draw unsupported edges. | SME reviewability, evidence integrity |
| LFCN-REV-003 | Excel extractor has unit tests against synthetic OpenXML fixtures, not real field workbooks. | Run one pilot workbook with multiple sheets and messy headers; harden classification and row summarization if needed. | SME correctness, handoff value |
| LFCN-REV-004 | Partial-input behavior is documented and covered by smoke prompts, but not yet runtime-executed. | Execute the partial Excel-only smoke and confirm missing views become Mermaid placeholders with non-blocking `TBD-*` questions. | User experience, adoption |

## Strengths

- Missing Operation / Business, System, Program, or Data flow coverage no
  longer blocks by itself.
- The output contract preserves all four review surfaces even when evidence is
  partial, making gaps visible to SMEs instead of hiding them in prose.
- `ready_with_warnings` gives SMEs a controlled path to carry known gaps
  forward without forcing premature approval.
- Mermaid requirements and multi-sheet Excel extraction remain intact.

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
3. A negative prompt with unknown source authorization that must route to
   `legacy-ibmi-evidence-intake` without extracting sensitive content.

Keep the canonical skill under `skills/legacy-flow-context-normalizer/`.
