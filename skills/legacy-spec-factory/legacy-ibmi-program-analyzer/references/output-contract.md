# Output Contract: Program Analysis

This document defines the precise shape and required fields for each `program-analysis-<OBJ-ID>.md` artifact produced by the analyzer.

## File Structure

Each program analysis follows this markdown structure:

```markdown
# Program Analysis: [Program Name] (OBJ-*)

## Metadata
## Analysis Coverage & Scope
## Program Call Map
## Routine Cards
## Deep Read Windows
## Entry Points & Parameters
## Object Dependencies
## Data Touch Map
## Control Flow
## File I/O
## External Calls
## Error Handling
## TBDs & Blocking Status
## Review Checklist
```

---

## Metadata Section

```markdown
## Metadata

- **Program ID:** OBJ-CREDIT-CHECK-003
- **Program Name:** CREDITCHK
- **Program Type:** RPGLE | CLLE | COBOL
- **Library:** CREDITLIB
- **Source Location:** [file path or collection ID]
- **Collection Date:** YYYY-MM-DD
- **Entry Points:** MAIN, VALIDATECREDIT
- **Files Accessed:** CREDFILE (PF), CUSTFILE (LF)
- **External Calls:** GETRATE, CHECKEXPOSE
- **Status:** draft | needs_sme_review | blocked_pending_source | approved | approved_with_non_blocking_tbd | rejected
```

**Required fields:**
- Program ID (OBJ-*) — must exist in approved inventory
- Program Name and Type
- Library
- At least one entry point
- Status (default: draft)

---

## Analysis Coverage & Scope Section

This section is mandatory for every program. It records analysis mode,
coverage limits, and known gaps so partial analysis cannot masquerade as
complete understanding. Align terminology with
`references/large-program-analysis.md`.

```markdown
## Analysis Coverage & Scope

### Source Size & Strategy

- **Source Lines:** 12,840
- **Routine Count:** 42
- **External Call Count:** 27
- **Object Dependency Count:** 31
- **Analysis Mode:** standard | segmented | large_program
- **Strategy:** structure index first, then routine cards, call/data maps, deep-read windows, and synthesis

### Coverage Ledger

| Metric | Count / Percent | Notes |
| --- | --- | --- |
| Source Lines | 12,840 | full source indexed |
| Routines Found | 42 | mainline + subroutines/procedures |
| Routines Deep-Read | 18 / 43% | hot paths, state changers, external boundaries |
| Routines Indexed Only | 21 / 50% | technical utilities with no observed state impact |
| External Edges Resolved | 25 / 27 | 2 parameter contracts pending |
| Data Touches Resolved | 36 / 40 | 4 payload structures pending DDS/copybook |
| Blocking Gaps | 1 | missing called program source |
| Non-Blocking Gaps | 5 | SME review questions only |

### Routine Coverage Summary

| Routine | Coverage | Reason | Evidence / Review |
| --- | --- | --- | --- |
| MAIN | deep_read | entry path | EV-AUTH-001 |
| SR100 | deep_read | hot path and data state change | EV-AUTH-002 |
| SR900 | indexed_only | utility routine, no business state impact observed | EV-AUTH-003 |
| SR999 | blocked | referenced but source range incomplete | TBD-AUTH-004 |
```

**Requirements:**
- Count source lines, routine definitions, external calls, and object
  dependencies before synthesis.
- Select one mode: `standard`, `segmented`, or `large_program`.
- Use `segmented` or `large_program` when the source cannot safely fit
  with evidence windows, or when call/data density requires
  structure-first analysis.
- Keep the coverage ledger current as routine cards, Program Call Map,
  Data Touch Map, and deep-read windows are produced.
- Do not claim complete understanding until coverage supports it.
- Routine coverage values are only `indexed_only`, `deep_read`, and
  `blocked`. SME confirmation belongs in evidence or review fields, not
  in the coverage field.

---

## Entry Points & Parameters Section

```markdown
## Entry Points & Parameters

| Entry Point | Type | Parameters | Return | Evidence Strength |
| --- | --- | --- | --- | --- |
| MAIN | Main Program | (CustID: numeric, CreditAmt: decimal) | Result Code (0/1/-1) | confirmed_from_code |
| VALIDATECREDIT | Subroutine | (Amount: decimal, Limit: decimal) | Pass/Fail (1/0) | confirmed_from_code |

**Evidence links:**
- [EV-CREDIT-CHECK-001: Source header documentation]
- [EV-CREDIT-CHECK-002: RPGLE procedure specifications]

**Unresolved:**
- TBD-CREDIT-CHECK-001: Confirm MAIN parameter order matches call sites
```

**Requirements:**
- One table row per entry point (main program + callables)
- Columns: Entry Point name, Type (Main Program / Subroutine / Callable Procedure), Parameters (with types), Return value/status code, evidence strength
- Every parameter must be documented with direction (input/output/both) if visible in source
- Evidence links must reference EV-* IDs from inventory
- TBDs for undocumented or unclear contracts

**Evidence strength values:**
- `confirmed_from_code` — source header or procedure specification documents this
- `medium_confidence` — inferred from usage but not explicitly declared
- `needs_sme_review` — behavior visible but interpretation unclear

---

## Program Call Map Section

This section captures the RDi-style structural skeleton of the program:
which mainline, subroutine, procedure, external program, API, queue, and
service nodes call which. It is a call map, not a business-process
diagram and not a statement-level control-flow chart.

**Five required views:**

### View 1: Visual Overview

```markdown
### Visual Overview

Source: source-level flow header (lines 8-22) | derived-from-code | both (matched)

```mermaid
flowchart LR
  MAIN["CU101A mainline"]
  MAIN --> SR990["SR990 first-time initialization"]
  MAIN --> SR100["SR100 preliminary validation"]
  SR100 --> SR110["SR110 amount conversion"]
  SR100 --> CHECKEXPOSE["CHECKEXPOSE external program"]
```
```

**Rules:**
- Prefer a compact graph over a complete visual tangle. The full edge
  table remains the source of truth.
- Include internal nodes (`EXSR`, procedure calls) and external boundary
  nodes (`CALL`, `CALLP`, API, data queue, message queue, service
  program) when they help a reader understand the program quickly.
- Mark common or hub nodes in the label when useful, but do not invent
  roles from names alone.

### View 2: Node Inventory

```markdown
### Node Inventory

| Node | Node Type | Defined At | Role / Notes | Evidence |
| --- | --- | --- | --- | --- |
| CU101A | Mainline | lines 100-220 | entry orchestration | EV-AUTH-ONUS-001 |
| SR100 | Subroutine | line 300 | hot path; preliminary validation | EV-AUTH-ONUS-002 |
| SR110 | Subroutine | line 410 | amount conversion | EV-AUTH-ONUS-003 |
| CHECKEXPOSE | External Program | call site line 520 | parameter contract pending SME | EV-AUTH-ONUS-004 |
```

**Node types:** `Mainline`, `Subroutine`, `Procedure`, `External
Program`, `Service Program`, `API`, `DTAQ`, `MSGQ`, `File`, `Copybook`.

**Requirements:**
- Every declared subroutine/procedure found in source is listed.
- Every external call target is listed.
- Nodes with no inbound calls are listed as orphan candidates with TBDs
  unless they are confirmed alternate entry points or callbacks.
- Nodes with many inbound calls are listed as hub/common candidates; the
  analyzer records the count and evidence, not a business interpretation.

### View 3: Call Tree (matches IBM i flow-header convention)

```markdown
### Call Tree

Source: source-level flow header (lines 8–22) | derived-from-code | both (matched)

```text
Main line                    Main flow control
|-- SR990                    First time initialization
|-- SR995                    Re-initialization
|-- SR100                    Card, account and product preliminary validation
|    |-- SR110               Convert authorization amount to LCY/billing
|    |    |-- SR111          Convert transaction amount (LCY/billing)
|    |    |-- SR112          Convert auth amount (non-ATMP)
|    |    |-- SR113          Convert auth amount (ATMP)
|    |-- SR120               Extract track information
|    |-- SR121               Classify recurring transactions
|    |-- SR130               Validate CVV/CVC 1
```

Evidence: [EV-SLUG-NNN: source-level flow header lines 8–22] + [EV-SLUG-NNN: EXSR statements lines 145–890]
```

**Rules:**
- If the program has a source-level flow-header comment, reproduce it verbatim (with line numbers).
- If the code-derived graph matches the header, mark "both (matched)".
- If they differ, show both trees side-by-side and create a TBD.
- If no header exists, derive purely from code and mark "derived-from-code".

### View 4: Call Edge Table

```markdown
### Call Edge Table

| From | To | Type | Line | Call Condition / Context | Evidence |
| --- | --- | --- | --- | --- | --- |
| Main | SR990 | EXSR (internal) | 145 | first-time-only (LR off) | confirmed_from_code |
| Main | SR100 | EXSR (internal) | 152 | every call | confirmed_from_code |
| SR100 | SR110 | EXSR (internal) | 320 | always | confirmed_from_code |
| SR110 | SR111 | EXSR (internal) | 410 | currency = LCY | confirmed_from_code |
| SR110 | SR112 | EXSR (internal) | 422 | trans_type ≠ ATMP | confirmed_from_code |
| SR110 | SR113 | EXSR (internal) | 434 | trans_type = ATMP | confirmed_from_code |
| SR100 | UPDTRISK | CALL (external) | 520 | only if approved | confirmed_from_code |
```

**Required columns:**
- **From / To:** subroutine, procedure, program, API, queue, service, or
  other node names
- **Type:** `EXSR (internal)`, `CALLP (internal)`, `CALL (external)`, `PERFORM (internal)`, `CALLPRC (external)`, etc.
- **Line:** source line of the call site
- **Call Condition:** when this call happens (`always`, `in DOWHILE loop`, `only if X`, `first-time only`, etc.) — derived from surrounding control flow
- **Evidence:** evidence strength + EV-* link

### View 5: Reverse Caller Index

```markdown
### Reverse Caller Index

| Node | Called By | Notes |
| --- | --- | --- |
| SR990 | Main [line 145] | dead code after first call (LR-gated) |
| SR100 | Main [line 152] | hot path: called every invocation |
| SR110 | SR100 [line 320] | only callsite |
| SR111 | SR110 [line 410] | LCY branch only |
| SR112 | SR110 [line 422] | non-ATMP branch |
| SR113 | SR110 [line 434] | ATMP branch |
| (no callers) | — | dead subroutine (flag with TBD) |
```

**Why these views:**
- **Visual Overview** -> gives an RDi-like first read of the program.
- **Node Inventory** -> ensures every routine and external boundary is
  accounted for.
- **Call Tree** -> matches IBM i convention; SME can compare to source
  header at a glance.
- **Call Edge Table** -> captures *condition* of each call (the thing
  diagrams cannot show reliably).
- **Reverse Caller Index** -> exposes orphaned subroutines (declared but
  never called -> dead code TBD) and hotspots (one node called from many
  sites).

### Source-Level Flow Header Handling

If the source has a flow-header comment block (common in IBM i shops), the analyzer **must** reproduce it verbatim under "Call Tree" as documented intent and navigation evidence. The header is useful for orientation and SME comparison, but it is not authoritative when it disagrees with actual EXSR/CALL/PERFORM/CALLP/CALLPRC call sites.

**Then** independently derive a Program Call Map from code. Actual call
sites are authoritative for behavior facts and code-derived call edges.
Compare:

| Header vs. Code | Action |
| --- | --- |
| Match exactly | Cite both the header and code-derived call sites; behavior facts remain supported by the code-derived call sites. |
| Header has subroutine not in code | TBD: comment drift (likely subroutine renamed/removed) |
| Code has subroutine not in header | TBD: comment drift (likely subroutine added without updating header) |
| Header parent-child order differs from code | TBD: comment may reflect old structure |
| No header present | Derive from code only; note absence. |

When header and code conflict, use the code-derived Program Call Map for
call edges and create a TBD for the mismatch. Matching header and code
may cite both sources, but EXSR/CALL/PERFORM/CALLP/CALLPRC statements
support `confirmed_from_code` behavior facts.

---

## Routine Cards Section

Routine cards are required for `segmented` and `large_program` mode and
recommended for standard mode when routines have meaningful state
impact. Each card summarizes one semantic unit before whole-program
synthesis.

```markdown
## Routine Cards

### MAIN

| Field | Value |
| --- | --- |
| Routine | MAIN |
| Location | lines 100-240 |
| Called By | external program entry |
| Calls Out | SR100, SR200, CHECKEXPOSE |
| Data Touches | CUSTMSTR, AUTHLOG, CHECKEXPOSE parameter list |
| State Impact | external handoff |
| Error Handling | checks return code from CHECKEXPOSE |
| Evidence | EV-AUTH-001, EV-AUTH-002 |
| Coverage | deep_read |
| Open Questions | Confirm caller parameter order with SME |
```

**Required fields:**
- Routine: subroutine, procedure, paragraph, or mainline segment
- Location: source line range
- Called By: immediate inbound callers
- Calls Out: internal and external calls made by this routine
- Data Touches: files, queues, screens, reports, parameters, and
  critical fields
- State Impact: `read-only`, `creates`, `updates`, `deletes`,
  `external handoff`, or `unknown`
- Error Handling: local monitor, indicator checks, message writes, or
  propagated status
- Evidence: source evidence IDs and line ranges
- Coverage: `indexed_only`, `deep_read`, or `blocked`
- Open Questions: source gaps, SME questions, or contradiction
  references

SME confirmation belongs in evidence or review fields, not the coverage
field.

---

## Deep Read Windows Section

Deep-read windows document the exact source windows used for semantic
analysis when the whole program cannot safely stay in context.

```markdown
## Deep Read Windows

| Window ID | Routine / Path | Source Lines | Why Selected | Coverage Outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| DRW-AUTH-001 | MAIN -> SR100 -> SR110 | 100-520 | hot path and approval decision | deep_read | EV-AUTH-001 |
| DRW-AUTH-002 | SR800 | 2100-2260 | writes AUTHLOG | deep_read | EV-AUTH-006 |
```

**Selection priorities:**
- Entry mainline and trigger handling
- Routines on hot call paths
- Routines with external calls
- Routines that write, update, delete, commit, roll back, send messages,
  or send queue payloads
- Routines touching money, account/customer IDs, inventory,
  approval/decline state, posting flags, audit IDs, or error/return
  codes
- Routines involved in contradictions or flow-header drift

Do not deep-read every technical utility routine if it is structurally
indexed and has no business state impact.

---

## Control Flow Section

```markdown
## Control Flow

### Main Entry Point
1. Accept input parameters [EV-CREDIT-CHECK-001]
2. Call VALIDATECREDIT subroutine with (Amount, Limit) → [evidence_strength]
3. Branch on validation result:
   - If validation PASS (result = 1): proceed to step 4
   - If validation FAIL (result = 0): jump to step 5
4. Call CHECKEXPOSE program (Amount, CustID) → [evidence_strength]
   - If CHECKEXPOSE returns APPROVED: set result code = 1, go to step 6
   - If CHECKEXPOSE returns DENIED: set result code = -1, go to step 5
5. Write error message to QSYSOPR message queue, return result code
6. Return result code to caller

**Control structures:**
- Conditional: SELECT statement on validation result (lines 120–150)
- Loop: READE on CUSTFILE for validation iterations (lines 160–180)
- External call: CALLP CHECKEXPOSE (line 175)

**Evidence links:**
- [EV-CREDIT-CHECK-001: Source lines 100–210]

### VALIDATECREDIT Subroutine
1. Compare input Amount parameter vs. CREDLIMIT value from CREDFILE
2. If Amount ≤ CREDLIMIT: return 1 (pass)
3. Else: return 0 (fail)

**No error handling observed.** [evidence_strength: confirmed_from_code]
```

**Requirements:**
- Document main entry point control flow first, then each callable subroutine
- Use numbered steps with brief descriptions
- Identify control structures: conditionals, loops, external calls, error handling
- Tag evidence for each non-trivial step
- Note line numbers if available
- Create TBD for unclear branching logic or missing subroutines

**Format guidelines:**
- Steps should be executable (SME can predict program behavior from steps alone)
- Subroutine flow should be self-contained (independent of caller context)
- Loops and branches should show all paths (happy path + error paths)
- External calls should name the called program and parameters

---

## Object Dependencies Section

This section is the **flat reference inventory** — every external object the program touches, in one table. It matches the shop's `F5-OBJREF TREE` tool output so SMEs can compare side-by-side.

**Why this section exists separately from File I/O / External Calls:**
- Object Dependencies = **what is referenced** (flat list, all types)
- File I/O = **how files are read/written** (deep dive on PF/LF/DSPF/PRTF only)
- External Calls = **how programs are invoked** (deep dive on \*PGM / \*SRVPGM only)

An object listed in Object Dependencies that is a file should also appear in File I/O with operation details; if it is a called program, in External Calls. Data areas, copybooks, data structures appear only here.

### Format

```markdown
## Object Dependencies

Source: shop F5-OBJREF TREE tool output | derived-from-code | both (matched)

### Uses (forward dependencies)

| Object        | Type      | Version  | Description                                  | Inventory ID         | Evidence            |
| ---           | ---       | ---      | ---                                          | ---                  | ---                 |
| HSSDTAR002    | *DTAARA   | 01.00.00 | Batch Run Date-Related Parameters Data Area  | OBJ-AUTH-ONUS-014    | confirmed_from_code |
| HSSDTAR100    | *DTAARA   | —        | (description not in tool output)             | OBJ-AUTH-ONUS-015    | confirmed_from_code |
| @CU176D       | PF (DS)   | 01.00.00 | @CU176 Program Parameter Data Structure      | OBJ-AUTH-ONUS-016    | confirmed_from_code |
| ADEALTP       | PF        | 01.00.00 | ATM Deal Number Table                        | OBJ-AUTH-ONUS-017    | confirmed_from_code |
| AUTHTPDS      | PF        | 25.K.23A | DS for Segment ID AUTHTP IN CCAUSGP/HP       | OBJ-AUTH-ONUS-018    | confirmed_from_code |
| CC030D        | PF (DS)   | 01.00.00 | CC030 Program Parameter Data Structure       | OBJ-AUTH-ONUS-019    | confirmed_from_code |
| CC040D        | PF (DS)   | 01.00.00 | CC040 Program Parameter Data Structure       | OBJ-AUTH-ONUS-020    | confirmed_from_code |
| HCCDTAR001    | Copybook  | —        | (D-spec include)                             | TBD-AUTH-ONUS-NNN    | confirmed_from_code |
| HCCDTAR115    | Copybook  | —        | (D-spec include)                             | TBD-AUTH-ONUS-NNN    | confirmed_from_code |
| CHECKEXPOSE   | *PGM      | —        | Credit exposure check (external program)     | OBJ-AUTH-ONUS-030    | confirmed_from_code |

### Used By (reverse dependencies)

Drawn from `01_inventory/inventory.yaml` `relationships` section.

| Caller      | Type   | Notes                              | Evidence                          |
| ---         | ---    | ---                                | ---                               |
| ORDENTR     | *PGM   | Calls CU101A on online auth flow   | from inventory relationships      |
| CU101B      | *PGM   | Calls CU101A after batch staging   | from inventory relationships      |
```

### Required Columns

| Column | Source / Meaning |
| --- | --- |
| Object | Object name as it appears in source code (uppercase, IBM i naming) |
| Type | `PF`, `LF`, `DSPF`, `PRTF`, `*DTAARA`, `*DTAQ`, `*MSGF`, `*PGM`, `*SRVPGM`, `Copybook`, `PF (DS)` |
| Version | Shop-tracked version if available (e.g., `01.00.00`, `25.K.23A`); `—` if not tracked |
| Description | Business description from the shop tool, source comment, or inventory |
| Inventory ID | Matching `OBJ-*` from `01_inventory/inventory.yaml`; or `TBD-*` if inventory has no entry |
| Evidence | `confirmed_from_code` (F-spec, D-spec, /COPY, CALL statement) or `needs_sme_review` |

### Object-Type Recognition Hints

- **`H`-prefix** in shop conventions often = **header / D-spec include** (copybook); confirm against `/COPY` directives in source
- **`@`-prefix** often = **data-structure copybook** (parameter DS); confirm against `D` specs
- **`HSS`-prefix** in this shop = data areas (`HSSDTAR…` = SSDTAR data area family)
- **`HCC`-prefix** in this shop = copybooks (`HCCDTAR…` = CCDTAR family copybooks)
- These conventions are **shop-specific** — verify with the SME and add to a shop-conventions reference rather than hard-coding into the analysis.

### Inventory Cross-Check Rule

For every object in this table:
- If `01_inventory/inventory.yaml` has a matching `OBJ-*` → use that ID
- If not → create `TBD-<SLUG>-NNN: inventory gap, object [NAME] used by [PROGRAM] not in inventory`
  - Blocking: `pending_source` (inventory is incomplete)
  - This is a signal back to the inventory skill that its scope needs widening.

### Source Comparison Rule

If the shop's `F5-OBJREF TREE` output is provided as input:
- Reproduce its rows verbatim in the "Uses" table
- Independently re-derive the list from source code (F-specs, D-specs, /COPY directives, CALL statements)
- Mark "Source: both (matched)" if identical
- If shop tool has objects not in code or vice versa → create TBD (tool drift / dead reference / missing source)

---

## Data Touch Map Section

The Data Touch Map is the program-local data movement and state-change
view. It answers: "Which routine touches which data carrier, with what
operation, and what state impact?"

It is not a full field lineage report. Track object-level, record-level,
and critical-field-level movement only.

### Format

```markdown
## Data Touch Map

### Data Touches

| Data Object / Carrier | Mechanism | Operation | Routine / Procedure | Key / Payload | Critical Fields Touched | State Impact | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CUSTMSTR | PF | CHAIN | SR100 | key=CustID | CustID, Status, RiskCode | read-only lookup | EV-AUTH-001 |
| AUTHLOG | PF | WRITE | SR800 | AuthNo | Amount, Decision, RC | creates audit/transaction row | EV-AUTH-002 |
| HSSDTAR002 | *DTAARA | IN / OUT | SR990 | BatchRunDate + completion flag | BatchRunDate, CompleteFlag | reads and updates shared state | EV-AUTH-003 |
| QRCVDTAQ | *DTAQ | QRCVDTAQ | SR980 | inbound fixed-format message | AccountNo, Amount, TranType | async receive | EV-AUTH-004 |
| PA196 | CALL parameters | inout | SR300 | AccountNo, Amount, Decision, RC | Decision, RC | external program boundary | EV-AUTH-005 |

### Critical Field Watchlist

| Field / Data Structure | Object / Carrier | Why It Matters | Observed Operations | Evidence |
| --- | --- | --- | --- | --- |
| Decision | PA196 parameter list | approval / decline outcome | passed out, tested by caller | EV-AUTH-005 |
| Amount | AUTHLOG / PA196 | money movement | compared, written, passed to external program | EV-AUTH-002 |
```

### Required Columns

| Column | Source / Meaning |
| --- | --- |
| Data Object / Carrier | File, data area, data queue, message queue, call parameter list, copybook/data structure, DSPF/PRTF, or IFS file |
| Mechanism | `PF`, `LF`, `DSPF`, `PRTF`, `*DTAARA`, `*DTAQ`, `*MSGQ`, `CALL parameters`, `Copybook/DS`, `IFS` |
| Operation | `READ`, `CHAIN`, `READE`, `WRITE`, `UPDATE`, `DELETE`, `EXFMT`, `IN`, `OUT`, `SNDDTAQ`, `RCVDTAQ`, `CALL in/out/inout`, etc. |
| Routine / Procedure | Internal node from the Program Call Map that performs the operation |
| Key / Payload | Key fields, message format, parameter list, or record format used |
| Critical Fields Touched | Important fields only: money, status, customer/account, inventory, posting, approval, return/error codes, audit IDs |
| State Impact | `read-only`, `creates`, `updates`, `deletes`, `async send`, `async receive`, `external handoff`, `unknown` |
| Evidence | EV-* link to source statements / DDS / copybook / interface docs |

### Granularity Rule

Default to object / record / critical-field granularity. Do not document
every RPG work variable. Escalate to field-level detail only when the
field affects money, inventory, customer/account status, posting,
approval/decline, compliance, auditability, external payloads, or error
outcomes.

### Relationship to File I/O and External Calls

- Data Touch Map = where data enters, changes, persists, or leaves this
  program.
- File I/O = detailed file access mechanics for PF/LF/DSPF/PRTF.
- External Calls = detailed program/interface invocation contracts.

The same evidence may appear in all three sections from different
angles. For example, `CALL PA196` appears as a Program Call Map edge, a
Data Touch row for parameter movement, and an External Calls row for
interface contract.

---

## File I/O Section

```markdown
## File I/O

| File | Type | Operations | Key Fields | Purpose | Evidence |
| --- | --- | --- | --- | --- | --- |
| CREDFILE | PF | CHAIN | CUSTID | Fetch credit profile | [EV-CREDIT-CHECK-002] |
| CUSTFILE | LF | READE | CUSTID | Iterate customer records for validation | [EV-CREDIT-CHECK-003] |
| LIMITTBL | PF | SETLL, READE | COUNTRY, CATEGORY | Lookup credit limit by country/category | [EV-CREDIT-CHECK-004] |

**Operation details:**

- **CREDFILE / CHAIN on CUSTID:** Fetch entire customer credit record. Key field: CUSTID (numeric). Result: populated *IN99 (not found indicator).
- **CUSTFILE / READE on CUSTID:** Loop through all customer records matching CUSTID. Continue until EOF or error.
- **LIMITTBL / SETLL + READE:** Locate and read limit table by (COUNTRY, CATEGORY). If SETLL finds no match, skip READE.

**Evidence links:**
- [EV-CREDIT-CHECK-002: DB2 for i table definitions]
- [EV-CREDIT-CHECK-003: RPGLE F-specs and I/O statements]

**Unresolved:**
- TBD-CREDIT-CHECK-002: Confirm whether CUSTFILE includes historical records or active only
```

**Requirements:**
- One table row per file accessed
- Columns: File name, Type (PF / LF / DSPF / PRTF), Operations, Key fields, Purpose, Evidence link
- Supported operations:
  - Sequential: READ (next record), READP / READPE (read previous)
  - Random: SETLL (set lower limit), READE (read equal), CHAIN (random access)
  - Write: WRITE (add new record), UPDATE (modify record), DELETE (remove record)
  - Display: EXFMT (formatted I/O on DSPF, used for menus and interactive input screens)
  - SQL: EXEC SQL blocks, cursor operations, SQLCODE / SQLSTATE error handling
- For each operation, document:
  - Key fields used in access (e.g., CHAIN on CUSTID)
  - Indicators set (e.g., *IN99 for not found) or status variables (SQLCODE)
  - Expected record count or iteration scope
- Reference file definitions from inventory (EV-*) and DDS / SQL schema where available
- Tag evidence as `confirmed_from_code` or `needs_sme_review`
- Create TBD for missing DDS, unclear key fields, SQL schema not documented, or undocumented access patterns

---

## External Calls Section

```markdown
## External Calls

| Called Program | Type | Parameters (In / Out) | Purpose | Evidence |
| --- | --- | --- | --- | --- |
| GETRATE | RPGLE Service Program | (RateCode: char) → (Rate: decimal) | Fetch interest rate by code | [EV-CREDIT-CHECK-005] |
| CHECKEXPOSE | RPGLE Program | (Amount: decimal, CustID: numeric) → (Decision: char) | Check credit exposure limits | [EV-CREDIT-CHECK-006] |
| UPDATEJNL | COBOL Program | (JournalCode: char, Timestamp: timestamp) → (RC: numeric) | Write to audit journal | [EV-CREDIT-CHECK-007] |

**Call details:**

- **GETRATE:** CALLP GETRATE(RateCode), returns RATE field. Error handling: if call fails, MONITOR catches and logs error.
- **CHECKEXPOSE:** CALL CHECKEXPOSE (Amount, CustID, Decision). Synchronous, blocks until return.
- **UPDATEJNL:** CALL 'UPDATEJNL' (JournalCode, Timestamp, RC). Called only if audit flag is set.

**Parameter contracts:**
- GETRATE expects RateCode to match RATE_TABLE key (uppercase, 3 chars). Undocumented → TBD-CREDIT-CHECK-003
- CHECKEXPOSE returns Decision: 'A' (approved), 'D' (denied), 'U' (unknown). Confirmed from source comments.
- UPDATEJNL RC values: 0 (success), 1 (journal full), -1 (system error). Confirmed from called program documentation.

**Unresolved:**
- TBD-CREDIT-CHECK-003: Confirm GETRATE parameter validation and error codes
- TBD-CREDIT-CHECK-004: Confirm CHECKEXPOSE network timeout behavior (call fails or returns default?)
```

**Requirements:**
- One table row per external call (program call, service program call, remote interface)
- Columns: Called program/interface name, Type (RPGLE Program / CLLE Program / Service Program / HTTP API / Message Queue / etc.), Parameters with types (In/Out), Purpose, Evidence
- For each call, document:
  - Parameter types and expected ranges
  - Return value or status code
  - Synchronous vs. asynchronous
  - Error handling (if monitored)
  - When the call is made (conditional or always)
- Reference evidence links (EV-*)
- Tag evidence as `confirmed_from_code` or `needs_sme_review`
- Create TBD for undocumented parameters, missing documentation, or unclear network behavior

---

## Error Handling Section

```markdown
## Error Handling

| Error Condition | Detected By | Handling | Recovery | Evidence |
| --- | --- | --- | --- | --- |
| File not found (CREDFILE) | MONITOR block (lines 200–210) | Write error message to QSYSOPR | Return -1 (error code) | [EV-CREDIT-CHECK-008] |
| Program not found (GETRATE) | CALL exception (CPDA error) | Log to error queue, skip rate lookup | Use default rate = 0, continue | [EV-CREDIT-CHECK-009] |
| Unexpected amount (< 0) | IF statement (line 115) | Write validation error | Return 0 (denied) | [EV-CREDIT-CHECK-010] |
| No records found (READE EOF) | SETOF indicator (lines 160–180) | Exit loop, proceed to next step | No error, expected path | [EV-CREDIT-CHECK-011] |

**Unhandled exceptions:**
- CUSTFILE READE fails with I/O error: no MONITOR block → Program will abnormally terminate → TBD-CREDIT-CHECK-005: Confirm error handling intent

**Logged errors:**
- Error messages written to QSYSOPR (message queue)
- Error codes logged if UPDATEJNL succeeds
- No persistent error table observed

**Evidence links:**
- [EV-CREDIT-CHECK-008: RPGLE MONITOR blocks]
- [EV-CREDIT-CHECK-009: CALL error handling]
```

**Requirements:**
- One table row per monitored error condition
- Columns: Error condition (what goes wrong), Detected by (MONITOR block / IF statement / indicator check / etc.), Handling (what code does), Recovery (result for caller), Evidence
- Separate section for unhandled exceptions (errors NOT caught)
- Note which errors log messages and where
- Reference evidence links
- Tag evidence strength
- Create TBD for unclear error codes, missing error handling, or context-dependent behavior

---

## TBDs & Blocking Status Section

```markdown
## TBDs & Blocking Status

### Pending Source
- **TBD-CREDIT-CHECK-002:** Confirm CUSTFILE includes historical records or active only
  - Blocking: pending_source — missing CUSTFILE DDS field documentation
  - Related: [OBJ-CREDIT-CHECK-001], [EV-CREDIT-CHECK-003]

### Pending SME Judgment
- **TBD-CREDIT-CHECK-001:** Confirm MAIN parameter order matches call sites
  - Blocking: pending_sme_judgment — source header ambiguous
  - Related: [EV-CREDIT-CHECK-001]

- **TBD-CREDIT-CHECK-003:** Confirm GETRATE parameter validation and error codes
  - Blocking: pending_sme_judgment — external program undocumented
  - Related: [OBJ-CREDIT-CHECK-005]

- **TBD-CREDIT-CHECK-005:** Confirm error handling intent for CUSTFILE I/O failures
  - Blocking: pending_sme_judgment — unhandled exception possible
  - Related: [OBJ-CREDIT-CHECK-001]

### Non-Blocking
- **TBD-CREDIT-CHECK-004:** Confirm CHECKEXPOSE network timeout behavior
  - Blocking: non_blocking — call has error handling, timeout path defined
  - Related: [OBJ-CREDIT-CHECK-006]
```

**Requirements:**
- Group TBDs by blocking status:
  - `pending_source` — missing DDS, incomplete source
  - `pending_sme_judgment` — behavior unclear from source alone
  - `non_blocking` — known gaps that don't affect downstream analysis
- For each TBD, include:
  - Question statement
  - Blocking status
  - Related object/evidence IDs
- No TBD should be vague ("something is unclear")
- Every TBD must map to a concrete gap or ambiguity

---

## Review Checklist Section

```markdown
## Review Checklist

Before approval, SME must validate:

- [ ] Entry points are correct and complete (no missing callable subroutines)
- [ ] Parameter contracts match actual usage (no invented parameters)
- [ ] Data Touch Map captures critical carriers, keys, payloads, and state impacts
- [ ] File I/O matches job design (no hallucinated key fields or unobserved operations)
- [ ] External calls match system interfaces (especially for undocumented calls)
- [ ] Error handling aligns with production reliability requirements
- [ ] TBDs are non-blocking or properly flagged for follow-up
- [ ] No invented subroutines or undocumented file access
- [ ] All evidence links reference existing inventory items (OBJ-*, EV-*)
- [ ] Status field is set correctly (`draft` → `needs_sme_review` /
  `blocked_pending_source` → `approved` / `approved_with_non_blocking_tbd` /
  `rejected`)

**SME sign-off:**

- Reviewer: ________________
- Review Date: ________________
- Decision: approved | approved_with_non_blocking_tbd | rejected
- Notes: [free-form]
```

---

## Evidence Strength Taxonomy

Every claim (entry point, control flow step, file I/O, external call, error handling) must carry one evidence strength:

| Strength | Meaning | Example |
| --- | --- | --- |
| `confirmed_from_code` | Source code directly shows this (visible in procedure spec, F-spec, I/O statement, MONITOR block) | RPGLE procedure header declares parameter types |
| `medium_confidence` | Inferred from usage pattern but not explicitly declared (e.g., indicator logic implies condition) | A field is assigned only in one IF branch → likely purpose of the field |
| `strongly_inferred` | Multiple evidence points support this (call site + default behavior) | External call always preceded by data validation → likely required validation |
| `needs_sme_review` | Evidence present but interpretation ambiguous (multiple possible meanings) | Error code returned but undocumented; could mean multiple things |
| `missing` | Evidence required but not available (DDS missing, source incomplete) | File accessed but DDS not in inventory → TBD |

---

## Review Status Values

- **draft** — initial analysis, ready for SME review
- **needs_sme_review** — waiting for SME validation (has blocking TBDs or ambiguities)
- **blocked_pending_source** — source incomplete or unavailable; analysis paused pending artifact delivery (DDS, CALL definitions, file descriptions) or SME unblock. Analyzer stops instead of guessing.
- **approved** — SME confirmed all behaviors and resolved TBDs
- **approved_with_non_blocking_tbd** — SME approved despite non-blocking TBDs (e.g., undocumented call without impact on this program's behavior)
- **rejected** — SME found serious errors or inconsistencies
