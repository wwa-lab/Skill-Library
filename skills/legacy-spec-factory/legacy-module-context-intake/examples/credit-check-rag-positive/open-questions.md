# Open Questions - CREDIT-CHECK

## Blocking Questions

| TBD ID | Source ID | Question | Owner | Route To | Needed Before |
| --- | --- | --- | --- | --- | --- |
| TBD-CREDIT-CHECK-002 | RAG-GAP-CREDIT-CHECK-005 | Does the wrapper use or discard the returned credit decision? | IBM i developer | legacy-ibmi-program-analyzer | approving system/program flow |
| TBD-CREDIT-CHECK-004 | RAG-GAP-CREDIT-CHECK-001 | How is available credit derived from physical customer credit fields? | Data owner | legacy-ibmi-data-model-analyzer | approving data flow |

## Non-Blocking Questions

| TBD ID | Source ID | Question | Owner | Carry Forward To |
| --- | --- | --- | --- | --- |
| TBD-CREDIT-CHECK-001 | RAG-GAP-CREDIT-CHECK-004 | Are over-limit denials audited, queued, or simply rejected inline? | Credit Operations SME | 01-operation-flow.md |
| TBD-CREDIT-CHECK-003 | RAG-GAP-CREDIT-CHECK-003 | Are there other callers of the credit decision routine outside the synthetic fixture? | IT SME | 03-program-flow.md |

## Non-Blocking Assumptions

| Assumption ID | Statement | Evidence | Review Status |
| --- | --- | --- | --- |
| RAG-ASM-CREDIT-CHECK-001 | Business-rule ownership appears to sit in the credit decision routine rather than the operational wrapper. | SME-CREDIT-CHECK-001; `CRDTCMD` | needs_sme_review |
| RAG-ASM-CREDIT-CHECK-002 | Full program analysis should prioritize the credit decision routine. | SNP-CREDIT-CHECK-004; `CREDITCHK` | needs_sme_review |

## Recommended Next Prompt

```text
Use legacy-ibmi-module-analyzer with
00_context_packages/CREDIT-CHECK/ as module-first context.
Treat RAG snippets and runtime observations as evidence context only.
Preserve contradiction-log.md and open-questions.md as TBD inputs.
Do not promote candidate rules without SME review.
Preserve business-signal-first candidate seeds; keep program and file names in
evidence context unless the target view is explicitly technical.
```
