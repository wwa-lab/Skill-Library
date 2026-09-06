---
skill: legacy-flow-context-normalizer
scorecard_version: v0.1.1
static_score: 9.38
decision: repo-ready
status: superseded
last_verified: 2026-05-27
runtimes_tested:
  codex: { status: synced, model: gpt-5.4-mini, date: 2026-05-27 }
  claude_code: { status: synced, model: haiku, date: 2026-05-27 }
  opencode: { status: synced, model: minimax-m2.5-free, date: 2026-05-27 }
evidence_source: docs/runtime-matrix.md
---

# Skill Review Scorecard: legacy-flow-context-normalizer v0.1.1

## Metadata

- skill_name: legacy-flow-context-normalizer
- skill_path: skills/legacy-flow-context-normalizer
- reviewed_version: v0.1.1
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

v0.1.1 adds deterministic multi-sheet `.xlsx` intake. The new helper reads an
Excel workbook with only Python standard library APIs, enumerates every sheet,
uses the first non-empty row as headers, emits one `FRAG-*` per non-empty data
row, and classifies each row into Operation / Business, System, Program, Data,
or `cross_view` based on sheet/header/content keywords.

## Mandatory Stop Conditions

No mandatory 8.0 cap conditions found.

The runtime cap still applies because the skill has been synced but not yet run
through positive and negative no-write execution smoke in Codex, Claude Code,
and OpenCode.

## Weighted Score

| Category | Weight | Score | Weighted |
| --- | ---: | ---: | ---: |
| Purpose and trigger clarity | 10% | 9.5 | 0.95 |
| Workflow completeness | 12% | 9.5 | 1.14 |
| IBM i / domain correctness | 14% | 9.0 | 1.26 |
| Evidence and anti-hallucination | 12% | 9.6 | 1.15 |
| Output contract | 10% | 9.6 | 0.96 |
| Progressive disclosure | 8% | 9.3 | 0.74 |
| Runtime portability | 10% | 9.1 | 0.91 |
| Reviewability and testability | 10% | 9.6 | 0.96 |
| Engineering handoff value | 8% | 9.5 | 0.76 |
| Maintainability | 6% | 9.3 | 0.56 |

Final score before cap: **9.38 / 10**

Final score after cap: **9.0 / 10**

## Decision

Repo-ready, not field-pilot ready.

## Blocking For 9.5

| ID | Finding | Required Change | Affects |
| --- | --- | --- | --- |
| LFCN-REV-001 | Runtime loading and no-write execution have not been verified in all three runtimes. | Run positive and negative smoke prompts in Codex, Claude Code, and OpenCode; update runtime matrix and scorecard. | Runtime portability, reviewability |
| LFCN-REV-002 | The Excel extractor has unit tests against synthetic OpenXML fixtures, not real field workbooks. | Run one pilot workbook with multiple sheets and messy headers; harden classification and row summarization if needed. | SME correctness, handoff value |
| LFCN-REV-003 | The extractor supports `.xlsx` only, not legacy `.xls` binary workbooks. | Require CSV/XLSX export for `.xls`, or add a separate conversion path when a field case needs it. | Testability, maintainability |

## Strengths

- Multi-sheet `.xlsx` files are now parsed deterministically without pandas or
  openpyxl.
- Each non-empty data row becomes a traceable `FRAG-*` with sheet/row locator.
- The helper makes Excel inventories, interface lists, data dictionaries, CRUD
  matrices, and process-step sheets usable as source-document evidence.
- Unit tests cover multi-sheet extraction and output-file writing.
- The original gates still prevent draft extracted rows from becoming approved
  flows or `BR-*` rules.

## Verification

```bash
python3 -m unittest tests/test_flow_context_excel_extractor.py

python3 skills/legacy-flow-context-normalizer/scripts/validate_flow_context_package.py \
  skills/legacy-flow-context-normalizer/examples/minimal-positive

python3 skills/legacy-flow-context-normalizer/scripts/validate_flow_context_package.py \
  --allow-blocked \
  skills/legacy-flow-context-normalizer/examples/blocked-authorization-negative
```

All commands returned successfully.

## Runtime Smoke Status

| Runtime | Status | Evidence |
| --- | --- | --- |
| Codex | synced | Adapter copy synced from canonical source on 2026-05-27 |
| Claude Code | synced | Adapter copy synced from canonical source on 2026-05-27 |
| OpenCode | synced | Adapter copy synced from canonical source on 2026-05-27 |

## Requested Next Revision

Run runtime smoke with:

1. A positive mixed-document prompt that includes a multi-sheet Excel workbook
   and expects a `source-document-index.yaml` draft with `FRAG-*` rows from all
   sheets.
2. A negative prompt with unknown source authorization that must route to
   `legacy-ibmi-evidence-intake` without extracting sensitive workbook content.

Keep the canonical skill under `skills/legacy-flow-context-normalizer/`.
