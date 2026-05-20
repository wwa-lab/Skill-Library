# Trigger Models: How a Flow Starts

A flow is a single business transaction. Every flow begins with **exactly
one trigger** — the event that starts the chain. This document defines the
seven trigger models the analyzer must recognize, the IBM i artifacts that
signal each, and the questions each model requires the SME to answer.

## Why Trigger Model Matters

The trigger model determines:

- Whether there is a user session (interactive) or not (batch)
- The expected SLA and error-recovery posture
- Where the analyst must look for the "starting point" of the flow
- What goes in the UI Surfaces section
- What commit-boundary expectations apply

Misclassifying the trigger model leads to misleading analysis. If the
analyzer cannot determine the trigger model with confidence, **stop** and
ask the SME — do not guess.

---

## 1. Batch Job

**Signal:** A CL program containing `SBMJOB`, or an `SBMJOB` reference in
a scheduler, or direct `CALL` from another batch chain.

**Characteristics:**
- Asynchronous; runs without a user session
- Often long-running (minutes to hours)
- Usually has a job description (`JOBD`), job queue (`JOBQ`), output queue (`OUTQ`)
- Commit boundary is usually the whole job (all-or-nothing) or
  checkpoint-based (per record / per batch of records)

**Capture in flow analysis:**
- CL program name and library
- `SBMJOB` command parameters (`CMD()`, `JOB()`, `JOBD()`, `JOBQ()`, `USER()`)
- Job description settings if non-default
- Expected runtime / cut-off window (from SME)

**SME questions:**
- Who or what schedules this job? (operator, scheduler, another program)
- What is the cut-off time / window?
- What happens if it fails mid-run? (restart from scratch, restart from
  checkpoint, manual recovery)
- Is there a re-run procedure?

**Example IDs:** `FLOW-DAILY-RECON-001`, `FLOW-MONTHEND-GL-001`

---

## 2. Interactive Menu (\*MENU)

**Signal:** A `*MENU` object on the user's job menu, or a CL command
`GO MENU(X/Y)` displayed in shop documentation.

**Characteristics:**
- Synchronous; user is in a 5250 session waiting for response
- Session-scoped (library list, output, job state persists for session)
- Driven by option selection (typically numeric option codes)
- Each option launches one flow (so a menu produces N flow analyses,
  one per option chosen for in-scope analysis)
- Tight SLA — user expects sub-second response

**Capture in flow analysis:**
- Menu object name (`*MENU`)
- Option number selected
- Command associated with that option (from menu definition: `MENU` /
  `MENUOPT` commands)
- Program invoked, parameters passed
- Return path (back to menu after program ends)

**SME questions:**
- Who uses this menu (role / department)?
- How often is this option selected (daily / weekly / rarely)?
- Are there role-based restrictions (only supervisors see option 9)?

**Example IDs:** `FLOW-CUST-LOOKUP-001`, `FLOW-MANUAL-AUTH-001`

---

## 3. Subfile Dispatch

**Signal:** A DSPF subfile (SFLCTL) where the user enters an option code
(typically `1=Select`, `2=Change`, `4=Delete`, `5=Display`, `9=Approve`)
next to a row.

**Characteristics:**
- The option-code field is read in a loop; each non-blank code triggers
  a different sub-program or sub-procedure
- Multiple records can be selected in one screen, with each triggering
  the dispatcher separately
- Common in maintenance / approval / inquiry screens

**Capture in flow analysis:**
- DSPF subfile name + control record
- Option-code field name and width
- Option-code dispatch table (typically a SELECT / WHEN block in source):

  | Option | Target | Description |
  |---|---|---|
  | 1 | PGM_SELECT | Select for further processing |
  | 4 | PGM_DELETE | Delete record (with confirmation) |
  | 5 | PGM_DISPLAY | View detail (read-only) |
  | 9 | PGM_APPROVE | Approve (requires supervisor) |

- For each option, the resulting flow continues from the target program

**SME questions:**
- Are all option codes documented, or are some "shop conventions" only?
- What happens if an unknown option is entered? (silent ignore, error
  message, drop)
- Are there permission checks per option (only supervisors can do 4=Delete)?

**Example IDs:** `FLOW-CUST-MAINT-OPT4-001` (or model the whole subfile
as one parent flow with branches; either is acceptable — pick the
granularity the SME thinks in)

---

## 4. F-Key Branch

**Signal:** A DSPF with function-key handlers (F-key DDS keywords like
`CAxx` / `CFxx`) and source code branching on the F-key indicator.

**Characteristics:**
- User-initiated divergence: pressing F6 might mean "new entry",
  F9 might mean "approve", F12 might mean "cancel"
- F-key conventions are usually shop-standard but not universal

**Capture in flow analysis:**
- DSPF object name
- F-key handlers (indicator + meaning from DDS):

  | F-Key | Indicator | Target | Description |
  |---|---|---|---|
  | F3 | *IN03 | (exit) | Exit to caller |
  | F6 | *IN06 | PGM_NEW | Add new record |
  | F9 | *IN09 | PGM_APPROVE | Approve transaction |
  | F12 | *IN12 | (cancel) | Cancel and return |

- For each F-key, the resulting flow branch

**SME questions:**
- Are F-key conventions shop-standard or screen-specific?
- Do any F-keys have side effects (auto-save, audit log)?

**Example IDs:** `FLOW-AUTH-MANUAL-001` (F-key flow for manual override),
`FLOW-CUST-EDIT-001`

---

## 5. DB Trigger

**Signal:** A trigger program registered against a file via `ADDPFTRG` or
SQL `CREATE TRIGGER`. The trigger program runs whenever an
INSERT / UPDATE / DELETE / READ event occurs.

**Characteristics:**
- Implicit invocation — caller does not directly CALL the trigger
- Runs in the caller's job and commit scope (usually)
- Limited error-handling options — failing a trigger may abort the
  triggering operation
- Often used for audit, replication, business-rule enforcement,
  cross-file integrity

**Capture in flow analysis:**
- Triggered file (PF/LF) + event type (BEFORE / AFTER, INSERT / UPDATE /
  DELETE / READ)
- Trigger program name + library
- What the trigger reads (`OldRecord`, `NewRecord` from trigger buffer)
- What the trigger does (writes audit, validates, propagates)
- Whether the trigger can veto the operation (signals an error to caller)

**Evidence requirements** (see `output-contract.md` Evidence Taxonomy):
- **Type 1 (Source statement):** ADDPFTRG command in CL, or SQL CREATE TRIGGER statement
- **Type 2 (Config export):** WRKPFTRG listing or trigger configuration export showing file + event + program
- **Type 4 (SME confirmation):** Business purpose (audit / validation / replication), failure behavior, implicit vs. explicit trigger knowledge

**SME questions:**
- Why does this trigger exist? (audit / business rule / replication)
- Who knows it exists? (often invisible to application developers)
- What is the upstream caller's expected behavior when the trigger fails?

**Example IDs:** `FLOW-CUST-AUDIT-TRG-001`, `FLOW-TXN-REPL-TRG-001`

---

## 6. Scheduler (WRKJOBSCDE)

**Signal:** An entry in the job-scheduler table (`WRKJOBSCDE`,
`WRKJOBSCDEE`) that fires a job at a defined time / frequency.

**Characteristics:**
- Time-driven (cron-like): daily 18:00, weekday 09:00, last working day
  of month, etc.
- Usually submits a batch job via `SBMJOB`, or directly `CALL`s a program
- When a scheduler entry submits a CL via `SBMJOB`, the flow is still
  **one flow** with **one primary trigger (the scheduler entry)**, not two
  separate flows. The `SBMJOB` is the submission mechanism; the CL program(s)
  are nodes in the same flow.

**Capture in flow analysis:**
- Scheduler entry ID
- Frequency (`SCDDATE`, `SCDDAY`, `SCDTIME`, `FRQ`)
- Submitted command (`CMD()` — usually `SBMJOB` or `CALL`)
- If `SBMJOB`: the CL program name and parameters; continue analysis into the batch program chain
- If direct `CALL`: the program name and parameters

**Evidence requirements** (see `output-contract.md` Evidence Taxonomy):
- **Type 2 (Config export):** WRKJOBSCDE entry listing with frequency, command, and parameters
- **Type 4 (SME confirmation):** Business purpose, SLA (cut-off time), downstream dependencies, failure recovery procedure

**SME questions:**
- What does this job do for the business?
- What happens if the schedule is missed (job queue held, system down)?
- Is there a downstream system that expects this job's output by a
  cut-off time?

**Example IDs:** `FLOW-NIGHTLY-INTEREST-001`, `FLOW-HOURLY-SYNC-001`

---

## 7. API / Remote

**Signal:** Inbound program call from outside the IBM i — remote PGM call
(DDM / DRDA), message arriving on an MQ queue, HTTP request handled by
an IBM i web service, file dropped via FTP / IFS, message arriving on a
data queue from another partition.

**Characteristics:**
- Driven by an external system, not by a user or schedule
- Often time-sensitive (SLA) and frequently retried
- Authentication / authorization is usually external

**Capture in flow analysis:**
- Inbound mechanism (remote PGM, MQ queue, HTTP endpoint, FTP / IFS, DTAQ)
- Authentication (if visible — TLS cert, signed payload, profile name)
- Parameter / payload contract (from copybook, JSON schema, fixed-width
  template)
- Source system (Visa, Mastercard, channel system, partner bank)

**Evidence requirements** (see `output-contract.md` Evidence Taxonomy):
- **Type 3 (Integration contract):** MQ queue configuration, API gateway route definition, DDM registration, FTP drop location documented in system-integration agreement
- **Type 4 (SME confirmation):** Upstream system name + organization, SLA and throughput expectations, retry semantics, idempotency and exactly-once delivery guarantees

**SME questions:**
- Who is the upstream system? (name + integration agreement)
- What is the SLA (response time, throughput)?
- What is the retry behavior on the caller side?
- Is the call idempotent (safe to retry)?

**Example IDs:** `FLOW-VISA-AUTH-IN-001`, `FLOW-MQ-CLEARING-001`

---

## When the Trigger Model Is Ambiguous

It is common for the entry point to look like one model but actually be
another. Examples:

- A CL that *both* schedules itself with `SBMJOB` *and* is invoked from
  a menu → two trigger models, two flows
- A program that is called by an F-key handler *and* by a subfile option
  dispatcher → two flows sharing the same target program
- A trigger that calls a normally interactive program → unusual; document
  carefully and flag for SME

**Rule:** Each *invocation path* is a separate flow. Two different
trigger models invoking the same target program → two flow analyses
referencing that program as a common node.

When in doubt, list the candidate trigger models in a TBD and let the
SME pick.
