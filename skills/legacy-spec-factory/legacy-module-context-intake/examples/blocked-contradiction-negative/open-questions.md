# Open Questions - PAYMENT-MATCH

## Blocking Questions

| TBD ID | Source ID | Question | Owner | Route To | Needed Before |
| --- | --- | --- | --- | --- | --- |
| TBD-PAYMENT-MATCH-001 | RAG-CONFLICT-PAYMENT-MATCH-001 | Is payment matching triggered daily EOD or on a weekly batch schedule? The SME note and runtime job log contradict each other. | AR Operations SME | SME review session | approving any downstream module analysis, BRD, or modernization decision |

## Non-Blocking Questions

| TBD ID | Source ID | Question | Owner | Carry Forward To |
| --- | --- | --- | --- | --- |
| TBD-PAYMENT-MATCH-002 | RAG-GAP-PAYMENT-MATCH-001 | Are there other programs that post to the AR balance table outside the identified matching path? | IT SME | 03-program-flow.md |
| TBD-PAYMENT-MATCH-003 | RAG-GAP-PAYMENT-MATCH-002 | Which physical file or table is the AR balance write target? | Data owner | 04-data-flow.md |

## Non-Blocking Assumptions

| Assumption ID | Statement | Evidence | Review Status |
| --- | --- | --- | --- |
| RAG-ASM-PAYMENT-MATCH-001 | Full program analysis should confirm whether matching logic is inline or delegated elsewhere. | SNP-PAYMENT-001; `PMTMATCH` | needs_sme_review |

## Recommended Next Prompt

```text
This package is blocked pending resolution of RAG-CONFLICT-PAYMENT-MATCH-001.

Do NOT route to legacy-ibmi-module-analyzer until the contradiction is resolved.

Required action:
1. Present TBD-PAYMENT-MATCH-001 to AR Operations SME for a ruling on
   matching frequency (daily EOD vs weekly batch).
2. Update contradiction-log.md with SME ruling and evidence.
3. Clear TBD-PAYMENT-MATCH-001 from blocking_items in context-index.yaml.
4. Update intake.status to ready_for_module_analysis or ready_with_warnings.
5. Re-run the validator:
   python3 skills/legacy-module-context-intake/scripts/validate_context_package.py \
     00_context_packages/PAYMENT-MATCH/
6. Then route to legacy-ibmi-module-analyzer.
```
