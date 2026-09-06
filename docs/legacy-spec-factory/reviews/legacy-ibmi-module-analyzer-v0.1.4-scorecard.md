---
skill: legacy-ibmi-module-analyzer
scorecard_version: v0.1.4
static_score: 9.36
decision: repo-ready
status: current
last_verified: 2026-05-29
runtimes_tested:
  codex: { status: synced, model: gpt-5.4, date: 2026-05-29 }
  claude_code: { status: synced, model: haiku, date: 2026-05-29 }
  opencode: { status: synced, model: minimax-m2.5-free, date: 2026-05-29 }
evidence_source: static review + adapter drift checks
---

# Skill Review Scorecard: legacy-ibmi-module-analyzer v0.1.4

## Review Focus

v0.1.4 keeps the canonical four-view module analysis in
`04_modules/<MODULE-SLUG>/`, but aligns downstream wording with the BRD-first
workflow. The standard consumer is now `legacy-brd-writer`; spec-writing is
downstream of approved BRD review. It also makes Mermaid diagrams mandatory in
all four view files so SME review sees a rendered flow first and uses tables
only for evidence and traceability.

## Decision

**Repo-ready, runtime smoke pending.**

The change reduces premature spec-writing while preserving the module
analyzer's responsibility for the Operation, System, Program, and Data views
that BRD writer needs as evidence-backed input. The Mermaid requirement aligns
module analysis with `legacy-flow-context-normalizer` and prevents table-only
"flow" outputs.

## Blocking For Field Pilot

Run three-runtime smoke to confirm that module analysis output routes to BRD
writing first, renders Mermaid diagrams in each view, and does not describe
itself as directly ready for spec-writing.
