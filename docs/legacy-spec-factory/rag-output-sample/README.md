# RAG Output Sample

This directory shows a compact file-based RAG evidence bundle for Legacy Spec
Factory. It is intentionally synthetic and uses the fixture at
`docs/synthetic-corpus/sqlrpgle-credit-check-happy/`.

The sample demonstrates the handoff contract described in
`docs/rag-setup-detail.md`: RAG provides source, runtime, relationship, and
dictionary context, but it does not approve business rules or replace SME
review.

## Package

```text
rag_runs/CREDIT-CHECK/RAG-20260521-001/
  rag-run-index.yaml
  flow-hydration-summary.md
  source-snippets.md
  field-dictionary-context.md
  impact-scope.md
  contradictions.md
  retrieval-gaps.md
```

## Intended Consumer

`legacy-module-context-intake` should ingest this package as context for a
module-first run and normalize it into:

```text
00_context_packages/CREDIT-CHECK/
  context-index.yaml
  01-operation-business-flow.md
  02-system-flow.md
  03-program-flow.md
  04-data-flow.md
  rag-evidence-map.md
  contradiction-log.md
  open-questions.md
```

## Sample Boundary

- This is an example output shape, not an accepted analysis package.
- The source system, dictionary, and ARCAD snapshots are synthetic.
- Runtime evidence contains one sample run only, so it can corroborate an
  observed scenario but cannot prove normal operating frequency.
- Any candidate business rule still requires downstream Legacy Spec Factory
  review and SME approval before promotion.
