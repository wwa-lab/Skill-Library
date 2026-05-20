# Error Propagation & Commit Boundary Analysis

A flow's *happy path* is usually obvious. The *unhappy paths* — what
happens when a node fails — are where flows actually break in production.
This document defines how to trace errors across the chain and identify
commit / rollback boundaries.

---

## Error Propagation Patterns

### Pattern A: Return Code Propagation

The callee returns an error code; the caller checks and decides.

```rpgle
CALLP CU111S(CustID : Amount : Decision : RC);
if RC <> 0;
    EVAL flow_decision = 'D';
    return;
endif;
```

**Capture:**
- Source node + line where the error is detected
- Return code semantics (0 = OK, -1 = X, -2 = Y …)
- Caller's response (abort flow, branch to error path, log-and-continue)

### Pattern B: Exception Propagation (MONITOR not caught)

The callee throws an exception; the caller doesn't `MONITOR` it; it
propagates up the call stack until something catches it (or the job
abnormally terminates).

**Capture:**
- Source node + line where exception is raised
- Which node (if any) catches it (MONITOR + ON-ERROR block)
- If nothing catches it → flow aborts; document this
- Commit-control implications (uncommitted writes roll back at job
  termination if journaled)

### Pattern C: Logged-and-Continued Errors

The error is logged (QSYSOPR, audit file, error queue) but the flow
continues with degraded behavior.

**Capture:**
- Where logged
- What degraded behavior follows
- Whether the user / operator is notified

### Pattern D: Compensating Action

A downstream node detects an upstream error and tries to compensate
(reverse a write, decrement a counter, notify a downstream system).

**Capture:**
- Detection point + compensation logic
- Whether compensation can itself fail (often missed; flag for SME)

### Pattern E: Abandoned Mid-Flow State

The flow aborts after some writes have committed but before others.
Result: inconsistent state.

**Capture:**
- The writes that did commit (writer node + file)
- The writes that did not happen
- Whether anything cleans up the inconsistency (cleanup job, manual
  process, accepted-as-loss)

**This is often the most important pattern to surface for SME** — many
shops have known-bad mid-flow abort scenarios they have learned to
recover from manually but have never formalized.

---

## Commit Boundary Identification

A **commit boundary** is a point in the flow after which work is
durable / visible to other actors.

### Implicit Commit (non-journaled file writes)

A simple `WRITE` to a non-journaled PF is committed immediately. Every
write is its own commit boundary.

### Explicit Commit (commitment control)

If the file is journaled and the program uses commitment control:

```rpgle
COMMIT;        // commit pending writes
ROLBK;         // roll back pending writes
```

The boundary is where `COMMIT` is called, not where individual `WRITE`s
happen.

### Cross-Program Commitment Scope

Commitment scope is **per job** (default) or **per activation group**
(if specified). All programs in the same scope share pending commits.

**Capture:**
- For each program in the flow: does it use commitment control?
- For the flow as a whole: is there a single commit boundary at the end,
  or are there intermediate commits?
- Where are the rollback points?

### External Commit Boundaries

Some commits are external to the IBM i:

- Sending a response to an external API (irrevocable — the caller now
  has the response)
- Writing to an IFS file consumed by another system
- Sending to a remote MQ queue
- Updating a DB2 table via SQL with `COMMIT`

**These external boundaries are often the most critical** because they
make work visible outside the IBM i and cannot be rolled back by IBM i
mechanisms.

---

## Output Format

```markdown
## Error Propagation

### Error Conditions Per Node

| Node | Error Condition | Detection | Local Handling | Propagated To Caller | Evidence |
| --- | --- | --- | --- | --- | --- |
| NODE-02 | Credit-check returns -1 | RC check | sets Decision='D' | abort happy path; return to NODE-01 | EV-... |
| NODE-03 | DB CHAIN finds no record | %FOUND check | RC=-2 returned | NODE-02 treats as decline | EV-... |
| NODE-04 | DTAQ send timeout | MONITOR | logged to QSYSOPR | flow aborts | EV-... |
| NODE-05 | Unhandled exception | (none — no MONITOR) | none | propagates; job ends abnormally | needs_sme_review per TBD-... |

### Flow-Level Error Outcomes

| Trigger Error | What Happens | Operator Visibility | Recovery |
| --- | --- | --- | --- |
| Validation failure at NODE-01 | Decline response sent to caller | none (normal path) | n/a — decline is a valid outcome |
| Credit-check failure at NODE-03 | Decline response sent; nothing logged | none | n/a |
| DB I/O error at NODE-03 | Flow aborts; caller times out | QSYSOPR msg | manual retry by ops |
| Unhandled exception at NODE-05 | Job ends; caller times out; no audit row | QSYSOPR + job log | manual retry by ops |

### Commit Boundaries

```text
[Trigger]
   │
   ▼
NODE-01 (read-only)
   │
   ▼
NODE-02 (read-only)
   │
   ▼
NODE-03 (read-only — SQLRPG SELECT)
   │
   ▼
NODE-04 (WRITE TXNLOGPF, non-journaled)  ← Commit Boundary 1 (audit row durable)
   │
   ▼
NODE-05 (read-only)
   │
   ▼
NODE-06 (sends response to caller)        ← Commit Boundary 2 (response visible)
   │
   ▼
[End of flow]
```

### Vulnerable Windows

- **Between Boundary 1 and Boundary 2:** TXNLOGPF has an audit row but
  the caller may not have received the response. If NODE-06 fails, the
  caller will retry. The retry will produce a *duplicate* audit row.
  → TBD: confirm idempotency strategy (dedupe on transaction ID).

- **Before Boundary 1:** any failure leaves no trace. The caller times
  out but no audit row exists. → TBD: is this acceptable?
```

---

## SME Questions Specific to Error Propagation

For every flow, ask:

1. **What is the worst real-world failure you've seen with this flow?**
   What happened, and how did you recover?
2. **Is there a known mid-flow abort scenario?** What state does it
   leave the system in?
3. **What does the user / external caller see when this flow fails?**
4. **Is there a cleanup job for partial state?**
5. **Does the flow assume the caller will retry?** Is it idempotent?

These questions surface the *de-facto* error model, which is almost
always richer than what's documented in code.
