---
skill: legacy-flow-context-normalizer
scorecard_version: v0.1.2
static_score: 9.42
decision: repo-ready
status: superseded
last_verified: 2026-05-27
runtimes_tested:
  codex: { status: synced, model: gpt-5.4-mini, date: 2026-05-27 }
  claude_code: { status: synced, model: haiku, date: 2026-05-27 }
  opencode: { status: synced, model: minimax-m2.5-free, date: 2026-05-27 }
evidence_source: docs/runtime-matrix.md
---

# Skill Review Scorecard: legacy-flow-context-normalizer v0.1.2

## Metadata

- skill_name: legacy-flow-context-normalizer
- skill_path: skills/legacy-flow-context-normalizer
- reviewed_version: v0.1.2
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

v0.1.2 makes Mermaid flow diagrams mandatory in every normalized view. The
diagram is the SME-readable surface, while the evidence-linked table remains
the traceability source of truth. The validator now rejects view files that
lack a `Mermaid Flow Diagram` section with a Mermaid `flowchart`.

## Mandatory Stop Conditions

No mandatory 8.0 cap conditions found.

The runtime cap still applies because the skill has been synced but not yet run
through positive and negative no-write execution smoke in Codex, Claude Code,
and OpenCode.

## Weighted Score

| Category | Weight | Score | Weighted |
| --- | ---: | ---: | ---: |
| Purpose and trigger clarity | 10% | 9.6 | 0.96 |
| Workflow completeness | 12% | 9.6 | 1.15 |
| IBM i / domain correctness | 14% | 9.1 | 1.27 |
| Evidence and anti-hallucination | 12% | 9.6 | 1.15 |
| Output contract | 10% | 9.7 | 0.97 |
| Progressive disclosure | 8% | 9.3 | 0.74 |
| Runtime portability | 10% | 9.1 | 0.91 |
| Reviewability and testability | 10% | 9.7 | 0.97 |
| Engineering handoff value | 8% | 9.7 | 0.78 |
| Maintainability | 6% | 9.3 | 0.56 |

Final score before cap: **9.42 / 10**

Final score after cap: **9.0 / 10**

## Decision

Repo-ready, not field-pilot ready.

## Blocking For 9.5

| ID | Finding | Required Change | Affects |
| --- | --- | --- | --- |
| LFCN-REV-001 | Runtime loading and no-write execution have not been verified in all three runtimes. | Run positive and negative smoke prompts in Codex, Claude Code, and OpenCode; update runtime matrix and scorecard. | Runtime portability, reviewability |
| LFCN-REV-002 | Mermaid diagrams are structurally required, but not rendered in runtime smoke yet. | Add smoke evidence that each runtime emits valid Mermaid diagrams and does not draw unsupported edges. | SME reviewability, evidence integrity |
| LFCN-REV-003 | Excel extractor has unit tests against synthetic OpenXML fixtures, not real field workbooks. | Run one pilot workbook with multiple sheets and messy headers; harden classification and row summarization if needed. | SME correctness, handoff value |

## Strengths

- Each of the four output views now has a human-readable Mermaid diagram plus
  a traceable evidence table.
- The validator enforces the Mermaid section, making the review surface
  measurable instead of aspirational.
- Diagram rules keep unsupported sequence arrows out of the visual flow.
- Multi-sheet Excel extraction from v0.1.1 remains intact.

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
   and expects four view files, each with a Mermaid diagram and evidence table.
2. A negative prompt with unknown source authorization that must route to
   `legacy-ibmi-evidence-intake` without extracting sensitive content.

Keep the canonical skill under `skills/legacy-flow-context-normalizer/`.
