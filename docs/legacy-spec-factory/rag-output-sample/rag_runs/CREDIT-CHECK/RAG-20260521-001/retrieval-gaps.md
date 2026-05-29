# Retrieval Gaps

RAG must expose missing context explicitly. These gaps should become
`open-questions.md` entries in the Legacy Spec Factory context package.

| Gap ID | Severity | Summary | Evidence | Suggested owner |
| --- | --- | --- | --- | --- |
| `RAG-GAP-CREDIT-CHECK-001` | medium | `CREDITVW.AVAIL_CREDIT` derivation is not proven by the supplied DDS. | `DDS-CREDIT-CHECK-CUSTMAST-001`, `DDS-CREDIT-CHECK-CREDITVW-001` | IT SME / data owner |
| `RAG-GAP-CREDIT-CHECK-002` | medium | Only one runtime sample is present, so runtime evidence cannot establish normal operating frequency or all edge cases. | `RUN-CREDIT-CHECK-JOBLOG-001`, `RUN-CREDIT-CHECK-SPOOL-001` | QA / operations SME |
| `RAG-GAP-CREDIT-CHECK-003` | low | No real ARCAD REF export is included in the synthetic fixture, so caller/callee completeness is not independently cross-checked. | `SNP-CREDIT-CHECK-001` | IT SME |
| `RAG-GAP-CREDIT-CHECK-004` | medium | No evidence shows whether denied over-limit requests are queued, audited, or simply rejected inline. | `SME-CREDIT-CHECK-001` | Credit Operations SME |
| `RAG-GAP-CREDIT-CHECK-005` | medium | `CREDITCHK` returns a decision from the RPG interface, but the supplied CL wrapper does not visibly capture that return value. | `SNP-CREDIT-CHECK-001`, `SNP-CREDIT-CHECK-004` | IBM i developer / IT SME |

## Non-Blocking Assumptions

| Assumption ID | Statement | Why it is non-blocking for the sample |
| --- | --- | --- |
| `RAG-ASM-CREDIT-CHECK-001` | `CRDTCMD` is operational glue, not the business rule owner. | SME note directly says the wrapper is operational glue only. |
| `RAG-ASM-CREDIT-CHECK-002` | `CREDITCHK` is the first downstream target for program analysis. | It contains the field lookup, branch conditions, decision value, and amount output logic. |

## Recommended Next Prompt

```text
Use legacy-module-context-intake with the CREDIT-CHECK RAG output package.
Normalize it into 00_context_packages/CREDIT-CHECK/, preserve retrieval gaps
as open questions, and do not promote candidate business rules without SME
review.
```
