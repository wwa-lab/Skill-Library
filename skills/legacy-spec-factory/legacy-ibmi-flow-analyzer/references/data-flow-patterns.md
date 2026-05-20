# Cross-Program Data Flow Patterns

This guide enumerates the mechanisms by which data passes between programs
in an IBM i call chain. The flow analyzer must classify every data
exchange into exactly one of these mechanisms and trace it to source.

---

## 1. CALL Parameters (Most Common)

The caller passes a parameter list; the callee receives it; the callee
may mutate output parameters in place.

**RPGLE:**
```rpgle
CALLP CU111S(CustID : Amount : Decision);
CALL  'UPDTRISK' (CustID : Amount : RC);
```

**CLLE:**
```clle
CALL PGM(VALIDATE) PARM(&CUSTID &AMOUNT &RC)
```

**COBOL:**
```cobol
CALL 'GET-RATE' USING BY VALUE RATE-CODE
                      BY REFERENCE RATE
                      BY REFERENCE STATUS.
```

**Capture:**
- Parameter list (name, type, direction: in / out / inout)
- Validation expectations (range, allowed values)
- Evidence: caller's CALL statement + callee's PI / PROCEDURE DIVISION

**Direction inference:**
- `BY VALUE` or `CONST` → in only
- `BY REFERENCE` → likely inout; confirm by checking whether callee
  modifies the parameter
- Numeric / character with no explicit direction → check usage in callee

**Pitfall:** A parameter modified by the callee but never read by the
caller is effectively wasted — flag for SME (might be dead code or
historical artifact).

---

## 2. Shared Data Area (\*DTAARA)

A small persistent key-value store shared by jobs and programs in the
same library / scope. Read with `IN`, written with `OUT`, locked with
`*LOCK`.

**RPGLE:**
```rpgle
D RUNDATE        S              8A
   ...
IN  RUNDATE;                 // read
OUT RUNDATE;                 // write
```

**CLLE:**
```clle
RTVDTAARA DTAARA(HSSDTAR002) RTNVAR(&RUNDATE)
CHGDTAARA DTAARA(HSSDTAR002) VALUE('2025-12-15')
```

**Capture:**
- DTAARA object name + library
- Read or write (or both)
- Lock posture (`*SHRRD` shared read, `*EXCL` exclusive, `*LOCK`)
- Producer node(s), consumer node(s)
- Update frequency

**Why DTAARA is a coupling hotspot:** It's the IBM i equivalent of a
global variable. Two programs that share a DTAARA are tightly coupled
even if they never call each other.

---

## 3. Data Queue (\*DTAQ)

Asynchronous message passing. Producer sends with `SNDDTAQ` / `QSNDDTAQ`,
consumer receives with `RCVDTAQ` / `QRCVDTAQ`.

**Modes:**
- FIFO / LIFO / Keyed
- Wait (blocking) or no-wait
- Persistent or transient

**Capture:**
- DTAQ object name + library
- Producer node(s) and what they send (message format)
- Consumer node(s) and how they consume (blocking, polling, keyed lookup)
- Wait timeout
- Message structure (often a fixed-format buffer; document fields)

**Why DTAQ matters:** It's the only truly asynchronous mechanism in
classic IBM i. If the flow uses a DTAQ, it has an async boundary, which
means commit / rollback story differs on each side.

---

## 4. Shared Files (PF / LF)

Program A writes a record; program B reads it later. The file is the
medium.

**Capture:**
- File name + library
- Writer node(s) + write operation (WRITE / UPDATE / DELETE)
- Reader node(s) + read operation (CHAIN / READE / SETLL)
- Key fields used for handoff
- Whether the write happens before / after the read in flow sequence
- Commit scope (journaled vs. not; commitment-control level)

**Subtypes:**
- **Transactional handoff:** writer writes one record, reader reads
  that specific record (e.g., transaction log)
- **State handoff:** writer updates a status field, reader checks status
  (e.g., job queue / order status)
- **Batch handoff:** writer produces many records overnight; reader
  consumes next morning (batch interface file)
- **Shared master:** both writer and reader use the master file; the
  "handoff" is conceptual rather than scheduled

**Pitfall:** Some shared-file handoffs go through *intermediate* files
(work files, staging tables). Document the full path.

---

## 5. Spool / PRTF

A program produces spool (`OVRPRTF` + `WRITE`) that another program (or
human, or downstream system) reads.

**Capture:**
- PRTF object name
- Producer node + when (which step of flow)
- Consumer (downstream program, operator, RPA process, archive)
- Format (printer file DDS)

**Why this matters:** Spool is often the integration with downstream
systems in mid-aged IBM i shops (reports become input files for the
next process).

---

## 6. IFS Files

Files on the Integrated File System (root, QOpenSys, etc.) — UNIX-style
files. Often used for integration with non-IBM-i systems.

**Capture:**
- IFS path
- Producer + format (CSV, XML, JSON, fixed-width)
- Consumer (often a remote system over FTP / SFTP / share)
- Encoding (CCSID concerns)

---

## 7. Message Queues (\*MSGQ)

System message queues (QSYSOPR, QSYSLG, user message queues). Producer
sends with `SNDPGMMSG` / `SNDMSG`, consumer monitors.

**Capture:**
- MSGQ object name (system or user-defined)
- Sender + message text / ID
- Receiver (operator, monitor program, log aggregator)

**Note:** Often used for error reporting, not data flow per se. But for
flows that depend on operator action, this is the formal channel.

---

## 8. Activation Group Globals

Variables shared across programs in the same activation group via
imports / exports.

**Capture:**
- Variable name
- Defining (exporting) program
- Using (importing) program(s)
- Activation group name

**Pitfall:** Activation-group coupling is invisible at the call level —
two programs share state without any visible parameter, file, or queue.

---

## 9. Out-of-Band / SME-Only Knowledge

Sometimes the data exchange isn't in the code at all — it's a manual step
(operator copies data, support team reads a screen and types into
another, a daily file is dropped by SFTP and a human starts the next
job).

**Capture:**
- Out-of-band step description (from SME)
- Owner / responsible role
- Frequency / SLA
- Mark `evidence_strength: confirmed_by_sme` and link to SME note

---

## Documentation Template

For each data exchange in the flow:

```markdown
| Data ID | Carrier | Producer | Consumer | Mechanism | Payload / Key Fields | Direction & Timing | State Impact | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DATA-FLOW-01 | EDGE-02 | NODE-02 | NODE-01 | CALL parameter (out) | Decision: char 1 | sync out | decision returned | EV-FLOW-005 |
```

For each, capture:
- **Data ID** — `DATA-<SLUG>-<NN>` stable across the flow document
- **Carrier** — edge ID or data object carrying the exchange
- **Producer** — node, external system, user, scheduler, or manual actor
  that creates/sends/writes the data
- **Consumer** — node, external system, user, monitor, report consumer, or
  manual actor that receives/reads the data
- **Mechanism** — one of the 9 categories above
- **Payload / Key Fields** — what's actually communicated (record,
  message, parameter list, key fields, critical fields)
- **Direction & Timing** — sync in/out/inout, async, batch-later,
  polling, manual, external handoff
- **State Impact** — read-only, creates, updates, deletes, sends,
  receives, commits, or unknown
- **Evidence** — pointer to source code (parameter declaration, DTAARA
  access, queue send / receive, file I/O, IFS read / write) or to SME note

## Granularity Rule

Data flow is object / record / critical-field level by default. Do not
trace every RPG work variable.

Escalate to field-level detail only for:
- money / amount fields
- account / customer / card / inventory identifiers
- approval, decline, status, posting, reconciliation, and lifecycle flags
- return codes, reason codes, and error codes
- audit IDs, journal IDs, external message IDs
- fields crossing an external system boundary

---

## Aggregation Rule for Module Analysis

When the module-analyzer aggregates flows into the **Data Flow View**, it
collects every `DATA-*` entry across every flow. Each data object (file,
DTAARA, DTAQ) is tagged with:

- **Producer flows** — every flow that creates / updates it
- **Consumer flows** — every flow that reads it
- **Coupling score** — number of flows touching it

Objects with high coupling scores are module hotspots; consider them
modernization risks (changing one ripples through many flows).
