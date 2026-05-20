# Input: Flow Definition (Batch Job Example)

This is the input handed to the flow analyzer to produce
`examples/batch-job-positive/flow.md`.

## Flow Scope

**Capability / Module:** Card Authorization (CARD-AUTH module)

**Business Event:** Nightly reconciliation of on-us card transactions
against the GL.

**Trigger:** Scheduler entry `NIGHTLY-RECON` fires at 22:00 every
weekday, submitting CL `RECONCL` via SBMJOB.

**Programs in chain (provided by inventory):**

| Order | Program | OBJ-* | Approved program-analysis |
|---|---|---|---|
| 1 | RECONCL  | OBJ-CARD-AUTH-101 | program-analysis-OBJ-CARD-AUTH-101.md ✅ |
| 2 | RECON01R | OBJ-CARD-AUTH-102 | program-analysis-OBJ-CARD-AUTH-102.md ✅ |
| 3 | RECON02R | OBJ-CARD-AUTH-103 | program-analysis-OBJ-CARD-AUTH-103.md ✅ |
| 4 | RECONSQL | OBJ-CARD-AUTH-104 | program-analysis-OBJ-CARD-AUTH-104.md ✅ |

**Data objects involved (from inventory):**

- `TXNLOGPF` (PF) — daily transaction log
- `GLPOSTPF` (PF) — GL posting staging
- `HSSDTAR002` (\*DTAARA) — Batch Run Date
- `RECONDTAQ` (\*DTAQ) — async confirmation to monitoring
- `RECONPRT` (PRTF) — exception report spool

**SME contact:** Anna Chen (Finance Ops); confirmed trigger model and
business event name; can answer recovery-procedure questions.

**Known production reality (from SME):**
- The job has a cut-off of 06:00 next morning before downstream GL
  consolidation reads `GLPOSTPF`
- If the job fails after midnight, ops uses a partial-restart procedure
  (re-runs RECON02R + RECONSQL only, using a checkpoint flag in
  HSSDTAR002)
- Exception report is hand-reviewed by Finance the following morning
