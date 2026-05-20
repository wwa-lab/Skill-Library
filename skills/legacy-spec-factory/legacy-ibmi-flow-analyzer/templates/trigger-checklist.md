# Trigger Identification Checklist

Use this checklist at step 1 of the workflow to confirm the trigger model
before proceeding with the rest of the analysis. Misclassifying the
trigger model invalidates everything downstream.

---

## Decision Tree

```
Does the entry program have a *MENU object pointing to it
or a 'GO MENU(X)' invocation in shop docs?
    └─ YES → MENU FLOW
       Capture: menu name, option number, command associated with option
       Continue to UI surface analysis.

Does a user press an F-key on a DSPF to invoke the entry program?
    └─ YES → F-KEY BRANCH FLOW
       Capture: DSPF object, function-key indicator, branch destination
       Continue to UI surface analysis.

Does a user enter an option code (1/2/4/5/9/...) on a subfile row?
    └─ YES → SUBFILE DISPATCH FLOW
       Capture: subfile name, option-code field, dispatch table
       Continue to UI surface analysis.

Is the entry program registered as a trigger on a PF/LF
(ADDPFTRG or SQL CREATE TRIGGER)?
    └─ YES → DB TRIGGER FLOW
       Capture: file, event (insert/update/delete), before/after, trigger buffer
       UI surfaces = N/A.

Is the entry invocation in WRKJOBSCDE / scheduler config?
    └─ YES → SCHEDULER FLOW
       Capture: schedule entry, frequency, command submitted
       Likely chains into a Batch Job flow downstream.

Is the entry invocation an inbound API call (remote PGM call,
MQ message, HTTP, IFS file drop, DTAQ receive from another system)?
    └─ YES → API / REMOTE FLOW
       Capture: inbound mechanism, source system, parameter contract,
       authentication
       UI surfaces = N/A.

Is the entry invocation a SBMJOB or direct CALL from a CL?
    └─ YES → BATCH JOB FLOW
       Capture: CL name, SBMJOB parameters, runtime expectations
       UI surfaces = N/A.

Otherwise → STOP. Trigger model unclear. Create TBD: pending_sme_judgment
and ask SME to clarify. Do not guess.
```

---

## Per-Model Checklist

### Batch Job
- [ ] CL program name + library captured
- [ ] SBMJOB parameters (CMD, JOBD, JOBQ, USER) captured
- [ ] Initiator identified (operator / scheduler / upstream program)
- [ ] Expected runtime window / cut-off documented
- [ ] Failure / restart procedure noted from SME

### Interactive Menu
- [ ] *MENU object name captured
- [ ] Option number selected captured
- [ ] Command associated with that option captured
- [ ] User role / department who uses this menu captured (SME)
- [ ] Frequency of selection captured (SME)
- [ ] Role-based restrictions noted (SME)

### Subfile Dispatch
- [ ] DSPF subfile + control record captured
- [ ] Option-code field name + width captured
- [ ] Dispatch table documented (option → target)
- [ ] Permission rules per option captured (SME)
- [ ] Handling of unknown option codes documented

### F-Key Branch
- [ ] DSPF object captured
- [ ] F-key handler table documented (F-key → indicator → meaning → target)
- [ ] Shop-standard vs screen-specific noted (SME)
- [ ] Side effects per F-key documented (audit / auto-save)

### DB Trigger
- [ ] Triggered file + event type (BEFORE/AFTER INSERT/UPDATE/DELETE) captured
- [ ] Trigger program + library captured
- [ ] Why the trigger exists captured (SME — audit / business rule / replication)
- [ ] Can trigger veto caller's operation documented
- [ ] Upstream caller's expectation when trigger fails documented (SME)

### Scheduler
- [ ] Scheduler entry ID captured
- [ ] Frequency captured (SCDDATE / SCDDAY / SCDTIME / FRQ)
- [ ] Submitted command captured
- [ ] Business meaning of schedule documented (SME)
- [ ] Downstream cut-off dependency documented

### API / Remote
- [ ] Inbound mechanism captured (remote PGM / MQ / HTTP / FTP / IFS / DTAQ)
- [ ] Source system identified (Visa / Mastercard / channel / partner bank)
- [ ] Authentication method captured (TLS / signed payload / profile)
- [ ] Parameter or payload contract documented
- [ ] SLA captured (response time, throughput)
- [ ] Retry behavior documented (caller-side, idempotency)

---

## Common Mistakes

- **A program is both menu-invoked and batch-invoked** → two separate flows
- **A "trigger" turns out to be just a CALL inside another program** →
  not a DB trigger; reclassify as a node within an existing flow
- **A subfile dispatcher option that "always falls through" to the next
  program** → still a subfile flow, but with one option; document why
  the dispatcher exists
- **A scheduler entry that submits a CL that submits another CL** →
  scheduler is the trigger; the chain of CLs is the body of the flow
