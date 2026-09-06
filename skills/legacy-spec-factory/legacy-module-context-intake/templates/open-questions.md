# Open Questions - [MODULE-SLUG]

## Blocking Questions

| TBD ID | Source ID | Question | Owner | Route To | Needed Before |
| --- | --- | --- | --- | --- | --- |

## Non-Blocking Questions

| TBD ID | Source ID | Question | Owner | Carry Forward To |
| --- | --- | --- | --- | --- |

## Non-Blocking Assumptions

| Assumption ID | Statement | Evidence | Review Status |
| --- | --- | --- | --- |

## Recommended Next Prompt

```text
Use legacy-ibmi-module-analyzer with
00_context_packages/[MODULE-SLUG]/ as module-first context.
Treat RAG snippets and runtime observations as evidence context only.
Preserve contradiction-log.md and open-questions.md as TBD inputs.
Do not promote candidate rules without SME review.
Generate the canonical four module views only under
04_modules/[MODULE-SLUG]/.
```
