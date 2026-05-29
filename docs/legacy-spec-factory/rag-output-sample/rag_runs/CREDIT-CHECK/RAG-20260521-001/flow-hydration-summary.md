# Flow Hydration Summary

## Run Metadata

| Field | Value |
| --- | --- |
| Module | `CREDIT-CHECK` |
| RAG run | `RAG-20260521-001` |
| Source snapshot | `synthetic-sqlrpgle-credit-check-happy-2026-05-21` |
| Dictionary version | `synthetic-dict-v1` |
| Fixture | `docs/synthetic-corpus/sqlrpgle-credit-check-happy/` |
| Evidence status | Draft RAG context; not SME-approved Legacy Spec Factory output |

## Module-First Hydration Result

### 01 Operation / Business Flow

Customer service submits a customer number and requested order amount for credit
evaluation. The observed legacy path returns an approve/deny decision and an
approved amount. If the request exceeds available credit, the observed runtime
sample denies the request while returning the available credit amount for
reference.

Evidence:

| Evidence ID | Type | Summary | Strength |
| --- | --- | --- | --- |
| `SNP-CREDIT-CHECK-004` | source snippet | Amount comparison and approve/deny assignment | confirmed_from_code |
| `RUN-CREDIT-CHECK-SPOOL-001` | spool sample | One denied over-limit scenario with capped approved amount | observed_in_runtime |
| `SME-CREDIT-CHECK-001` | SME note | SME confirms inactive denial and over-limit cap behavior | sme_confirmed |

### 02 System Flow

The operational entry wrapper `CRDTCMD` calls `CREDITCHK`. `CREDITCHK` reads
credit status and available credit from logical file `CREDITVW`, emits messages
to `QSYSPRT` for denial/error cases, sets the approved amount output parameter,
and returns a decision from the RPG interface. Whether the CL wrapper captures
that returned decision is not visible in the supplied wrapper source.

Evidence:

| Evidence ID | Type | Summary | Strength |
| --- | --- | --- | --- |
| `SNP-CREDIT-CHECK-001` | source snippet | `CRDTCMD` calls `CREDITCHK` | confirmed_from_code |
| `SNP-CREDIT-CHECK-002` | source snippet | `CREDITCHK` declares parameters and printer output | confirmed_from_code |
| `SNP-CREDIT-CHECK-003` | source snippet | `CREDITCHK` selects status and available credit from `CREDITVW` | confirmed_from_code |
| `RUN-CREDIT-CHECK-JOBLOG-001` | job log | Runtime messages show wrapper completion and over-limit diagnostic | observed_in_runtime |

### 03 Program Flow

```text
CRDTCMD
  -> CALL CREDITCHK
      -> SELECT STATUS, AVAIL_CREDIT FROM CREDITVW WHERE CUSTNO = :CustNo
      -> default Decision = 'D'
      -> deny if customer missing, SQL error, or inactive
      -> approve when ReqAmt <= AvailCredit
      -> deny and cap ApprAmt when ReqAmt > AvailCredit
      -> WRITE QSYSPRT denial/error message when applicable
```

Candidate downstream program-analysis focus:

| Program | Role | Suggested action |
| --- | --- | --- |
| `CRDTCMD` | Operational wrapper | Confirm wrapper responsibility only; do not promote business rules from wrapper text |
| `CREDITCHK` | Business decision owner | Perform full program analysis and rule extraction |

### 04 Data Flow

`CREDITVW` exposes `CUSTNO`, `STATUS`, and `AVAIL_CREDIT`. The logical file is
based on `CUSTMAST`, whose physical fields include `CUSTNO`, `STATUS`,
`CRDLMT`, and `USEDAMT`. The sample does not include enough DDS or SQL view
definition detail to prove how `AVAIL_CREDIT` is derived from credit limit and
used amount, so that derivation remains an open retrieval gap.

Evidence:

| Evidence ID | Type | Summary | Strength |
| --- | --- | --- | --- |
| `DDS-CREDIT-CHECK-CUSTMAST-001` | DDS PF | Physical customer credit fields | confirmed_from_code |
| `DDS-CREDIT-CHECK-CREDITVW-001` | DDS LF | Logical view fields used by `CREDITCHK` | confirmed_from_code |
| `DD-CREDIT-AVAILABLE-AMOUNT` | dictionary field | Business meaning for available credit | approved_dictionary |

## Candidate BRD Facts

These are retrieval candidates only. Legacy Spec Factory must re-check them
against source analysis, runtime evidence, and SME review before promotion.

| Candidate ID | Statement | Business Signal | Evidence Basis | Promotion status |
| --- | --- | --- | --- | --- |
| `RAG-CAND-CREDIT-CHECK-001` | Missing customers are denied by default. | Customer service cannot continue order release when the account cannot be resolved. | `SNP-CREDIT-CHECK-003`, `SNP-CREDIT-CHECK-004` | needs_sme_review |
| `RAG-CAND-CREDIT-CHECK-002` | Inactive customers are denied even if credit exists. | Customer eligibility status can override available credit. | `SNP-CREDIT-CHECK-004`, `SME-CREDIT-CHECK-001` | needs_sme_review |
| `RAG-CAND-CREDIT-CHECK-003` | Requests at or below available credit are approved for the requested amount. | In-limit orders may proceed without a credit exception. | `SNP-CREDIT-CHECK-004` | needs_sme_review |
| `RAG-CAND-CREDIT-CHECK-004` | Requests over available credit are denied and return the available amount as the maximum approvable amount. | Over-limit orders are blocked, but the response exposes the amount that may be approvable. | `SNP-CREDIT-CHECK-004`, `RUN-CREDIT-CHECK-SPOOL-001`, `SME-CREDIT-CHECK-001` | needs_sme_review |

## Handoff Notes

- Use `source-snippets.md` as the initial `rag-evidence-map.md` seed.
- Use `retrieval-gaps.md` to populate `open-questions.md`.
- Use `contradictions.md` to populate `contradiction-log.md`.
- Do not treat this summary as the final BRD or spec.
