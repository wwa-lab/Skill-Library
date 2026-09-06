# Output Contract: Flow Analysis

This document defines the precise shape and required fields for every
`flow-<FLOW-SLUG>.md` artifact.

## File Structure

```markdown
# Flow Analysis: [Business Event Name] (FLOW-*)

## Metadata
## Trigger Context
## Transaction Call Map
## Nodes (Programs in the Chain)
## Edges (Calls Between Nodes)
## Common Dependencies
## Cross-Program Data Flow
## Branch Points
## UI Surfaces                       (N/A for non-interactive flows)
## Error Propagation & Commit Boundaries
## Business Capability Seeds
## TBDs & Blocking Status
## Review Checklist
```

---

## Metadata Section

```markdown
## Metadata

- **Flow ID:** FLOW-ONUS-AUTH-001
- **Business Event Name:** On-Us Card Authorization (online)
- **Trigger Model:** API / Remote (Visa inbound auth request)
- **Module:** [MODULE-SLUG] (e.g., CARD-AUTH)
- **Entry Node:** NODE-ONUS-AUTH-01 (program CU101A / OBJ-AUTH-ONUS-001)
- **Exit Node(s):** NODE-ONUS-AUTH-14 (program CU199Z / OBJ-AUTH-ONUS-014, returns response to Visa)
- **Runtime Model:** synchronous, real-time, sub-second SLA
- **Status:** draft | needs_sme_review | approved | approved_with_non_blocking_tbd | blocked_pending_source | blocked_pending_sme
```

**Status values:**
- `draft` — Initial analysis; workflow incomplete, awaiting SME review
- `needs_sme_review` — All sections populated; awaiting SME judgment on business accuracy
- `approved` — SME reviewed and confirmed; ready for downstream processing
- `approved_with_non_blocking_tbd` — SME reviewed and approved with explicitly non-blocking TBDs carried forward
- `blocked_pending_source` — Analysis blocked; missing program-analysis, missing DSPF, or other source artifacts required before continuing
- `blocked_pending_sme` — Analysis blocked; ambiguous trigger model, unclear error intent, or missing SME business context; clarification required before continuing

---

## Trigger Context Section

Describe **how the flow starts** in enough detail that an SME can confirm
or correct. The format depends on the trigger model — see
`trigger-models.md`. Common required fields:

- Trigger artifact (CL name, MENU + option, DSPF + option / F-key,
  trigger registration, scheduler entry, API contract)
- Source line / configuration reference for the trigger
- Caller (who invokes — user role, scheduler, external system, internal
  program)
- Frequency / cadence
- SLA expectation (if any)
- Authentication / authorization context (if external)
- Evidence link

---

## Transaction Call Map Section

RDi-style call/dependency map showing the transaction's cross-program and
cross-boundary structure. This is not a business-process diagram and not
a statement-level flowchart. Internal subroutines remain folded into a
`Via` field unless exposing them is necessary for SME understanding.

```markdown
### Transaction Call Map

Source: derived-from-code + SME confirmed | header (if present) | both (matched)

```mermaid
flowchart LR
  TRG["Visa inbound trigger"]
  CU101A["NODE-01 CU101A"]
  CU110A["NODE-02 CU110A"]
  CU111S["NODE-03 CU111S"]
  MSG["CCOPRMSG\nshared utility"]
  TRG --> CU101A
  CU101A --> CU110A
  CU110A --> CU111S
  CU101A --> MSG
  CU110A --> MSG
```

### Call Chain Summary

```text
[Visa Inbound]
    │
    ▼
NODE-01 (CU101A)  ── validates auth request, derives currency
    │
    ▼
NODE-02 (CU110A)  ── calls credit-check
    │   │
    │   └─→ NODE-03 (CU111S)  ── credit limit lookup (SQLRPG)
    │
    ▼
NODE-04 (CU120A)  ── extracts track data, classifies recurring
    │
    ▼
NODE-05 (CU130A)  ── CVV validation
    │
    ▼
NODE-06 (CU199Z)  ── builds response, returns to Visa
    │
    ▼
[Visa Outbound response]
```

**Evidence:**
- [EV-...-001: CU101A CALLP CU110A, line 245]
- [EV-...-002: CU110A CALLP CU111S, line 312]
- ...
```

For interactive flows include UI surfaces inline:

```text
[User on MENU CMENU100, option 5]
    │
    ▼
NODE-01 (CU200A)  ── shows DSPF CU200D (customer lookup)
    │
    │  User enters CustID, presses Enter
    ▼
NODE-01 (CU200A)  ── validates input, calls lookup
    │
    ▼
NODE-02 (CU201A)  ── customer record lookup
    │
    ▼
NODE-01 (CU200A)  ── shows DSPF CU200D2 (customer detail subfile)
    │
    │  User selects option 5=Display next to row
    ▼
NODE-03 (CU205A)  ── customer history detail
```

---

## Nodes Section

```markdown
### Nodes

| Node ID | Program (OBJ-*) | Role | Program Analysis | Coverage Status | Blocking Coverage Gaps | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| NODE-ONUS-AUTH-01 | CU101A (OBJ-AUTH-ONUS-001) | Entry / validator | `program-analysis-OBJ-AUTH-ONUS-001.md` | mode=standard; readiness=approved; routines=deep_read | none | Validates inbound payload format |
| NODE-ONUS-AUTH-02 | CU110A (OBJ-AUTH-ONUS-002) | Credit orchestrator | `program-analysis-OBJ-AUTH-ONUS-002.md` | mode=segmented; readiness=warning; routines=indexed_only technical utility | TBD-ONUS-AUTH-021: non-blocking utility routine coverage gap | Calls credit-check sub-flow |
| NODE-ONUS-AUTH-03 | CU111S (OBJ-AUTH-ONUS-003) | Data access (SQLRPG) | `program-analysis-OBJ-AUTH-ONUS-003.md` | mode=large_program; readiness=blocked; routines=indexed_only state-impacting routine | TBD-ONUS-AUTH-022: credit update routine not deep-read; route to program analyzer unless named SME waiver recorded | DB2 cursor over credit-history |
| ... | ... | ... | ... | ... | ... | ... |
```

**Role taxonomy:**
- `entry` — first program in the chain after the trigger
- `validator` — input validation, preliminary checks
- `orchestrator` — calls other programs; mostly control flow
- `worker` — does the actual business logic
- `data-access` — primarily DB I/O (SQLRPG, native I/O wrappers)
- `reporter` — produces PRTF / spool / file output
- `exit` — last program; returns response or commits

**Requirements:**
- Every Node must have an approved `program-analysis-<OBJ-ID>.md`. If
  not → blocking TBD (route back to program-analyzer).
- `Coverage Status` must use the structured format
  `mode=<standard|segmented|large_program>; readiness=<approved|warning|blocked>; routines=<deep_read|indexed_only|blocked plus short qualifier>`.
  SME waivers are recorded in `Blocking Coverage Gaps` or review notes,
  never as a coverage value.
- Every Node must carry upstream program coverage state from the program
  analysis, including any routine-level `deep_read`, `indexed_only`, or
  `blocked` gaps that affect flow readiness.
- Node IDs are sequence-numbered (`NODE-<SLUG>-01`, `NODE-<SLUG>-02`, …).
- A program that is called multiple times in different roles may appear
  as multiple nodes (with different sequence numbers), or as one node
  with multiple inbound edges — pick what the SME finds clearer.

### Program Coverage Propagation

Every flow node must carry upstream program coverage state. A flow cannot
use an edge, data exchange, branch, error path, or commit boundary from
an `indexed_only` routine when that routine has business state impact.

| Upstream Coverage | Flow Outcome |
| --- | --- |
| `deep_read` | May use as flow evidence |
| `indexed_only` + technical utility | May use with non-blocking warning |
| `indexed_only` + state impact | Block and route back to program analyzer unless named SME waiver recorded |
| `blocked` | Block flow analysis |

SME confirmation or waiver is review metadata captured in evidence,
review notes, or sign-off. It is not a coverage value.

---

## Edges Section

```markdown
### Edges

| Edge ID | From -> To | Via | Call Type | Site (program:line) | Condition | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| EDGE-ONUS-AUTH-01 | (trigger) -> NODE-01 | N/A | API inbound | (Visa contract) | always | EV-ONUS-AUTH-001 |
| EDGE-ONUS-AUTH-02 | NODE-01 -> NODE-02 | SR100 | CALLP | CU101A:245 | if validation passed | EV-ONUS-AUTH-002 |
| EDGE-ONUS-AUTH-03 | NODE-02 -> NODE-03 | SR300 | CALLP | CU110A:312 | always | EV-ONUS-AUTH-003 |
| EDGE-ONUS-AUTH-04 | NODE-02 -> NODE-04 | SR350 | CALLP | CU110A:330 | if credit OK | EV-ONUS-AUTH-004 |
| EDGE-ONUS-AUTH-05 | NODE-04 -> NODE-05 | N/A | CALLP | CU120A:185 | always | EV-ONUS-AUTH-005 |
| EDGE-ONUS-AUTH-06 | NODE-05 -> NODE-06 | N/A | CALLP | CU130A:90 | always | EV-ONUS-AUTH-006 |
```

**Call types:** `CALL`, `CALLP`, `CALLPRC` (service program), `SBMJOB`,
`trigger-fire`, `API-inbound`, `MENU-option`, `subfile-option`, `F-key`,
`scheduler-fire`, `DTAQ-receive`

**Condition examples:** `always`, `if validation passed`, `in loop per
record`, `error path`, `option = 4`, `F6 pressed`

**Via:** the internal routine/procedure from the caller's Program Call Map
that crosses the program/system boundary. Use `N/A` only when the call is
the trigger itself or no meaningful internal site applies.

---

## Common Dependencies Section

Multiple programs often call the same common program, API, data queue, or
message utility. Preserve every inbound edge in the edge table; this
section summarizes shared dependencies so the visual map stays readable.

```markdown
### Common Dependencies

| Common Node | Inbound Callers | Role Classification | Main Graph Treatment | Risk Notes | Evidence |
| --- | --- | --- | --- | --- | --- |
| CCOPRMSG | NODE-01, NODE-02, NODE-05 | shared utility | folded as hub | shared message behavior; regression-sensitive | EV-... |
| AUTHPOST | NODE-03, NODE-04 | business state changer | expanded as formal node | writes authorization state | EV-... |
```

**Role classifications:** `shared utility`, `business state changer`,
`integration boundary`, `data-access hub`, `unknown`.

**Expansion rules:**
- If a common node writes business files, changes customer/account/
  inventory/money state, controls commit/rollback, makes approval/
  decline decisions, or calls an external business system, keep it
  expanded as a formal flow node.
- If a common node is logging, message formatting, date/time,
  delay/wait, or a technical wrapper, it may be folded in the visual
  graph but must remain in Common Dependencies and Edges.
- Never infer a Java service boundary from shared usage alone; service
  boundaries are modernization decisions that require module/spec
  evidence and SME review.

---

## Cross-Program Data Flow Section

Document **what** travels along each edge. See `data-flow-patterns.md`.
This section tracks data carriers, producers, consumers, timing, and
state impact. It is not a full field-lineage report; use field-level
detail only for critical fields.

```markdown
### Cross-Program Data Flow

| Data ID | Carrier | Producer | Consumer | Mechanism | Payload / Key Fields | Direction & Timing | State Impact | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DATA-ONUS-AUTH-01 | EDGE-02 | NODE-01 | NODE-02 | CALL parameters | CustID, CardNo, Amount, Currency | sync in | read-only handoff | EV-... |
| DATA-ONUS-AUTH-02 | EDGE-02 | NODE-02 | NODE-01 | CALL parameter (out) | Decision, AuthCode, ErrorMsg | sync out | decision returned | EV-... |
| DATA-ONUS-AUTH-03 | HSSDTAR002 | NODE-02 | NODE-04 | Shared data area | BatchRunDate | out-of-band shared state | read/update shared state | EV-... |
| DATA-ONUS-AUTH-04 | ONUSDTAQ | NODE-04 | NODE-06 | DTAQ | TxnLogMessage | async | external handoff | EV-... |
| DATA-ONUS-AUTH-05 | TXNLOGPF | NODE-04 | NODE-06 | Shared file | full transaction record keyed by AuthNo | batch-later / file handoff | creates then reads persistent row | EV-... |
```

**Mechanism taxonomy:**
- `CALL parameters` — passed in call (in / out / inout per parameter)
- `Shared data area` — `*DTAARA` written by one node, read by another
- `Data queue` — `*DTAQ` SNDDTAQ / RCVDTAQ between nodes
- `Shared file` — PF or LF written by one, read by another (with key)
- `Shared work file` — temp file with explicit lifecycle
- `Spool / PRTF` — output for downstream consumption
- `DSPF / screen fields` — user-entered or displayed fields that drive the flow
- `IFS file` — stream file produced or consumed outside DB2 for i
- `Message queue` — `*MSGQ` visible to operator or monitor process
- `Activation-group globals` — variables shared via ACTGRP
- `Out-of-band / manual` — SME-confirmed manual handoff

**Required:** every entry traces to source (parameter declaration, data
area access, queue send / receive, file write / read, screen field,
message send, or SME note).

**Critical field rule:** identify fields that affect money, inventory,
customer/account status, posting, approval/decline, compliance, audit,
external payloads, return codes, or error outcomes. Non-critical work
fields stay out of this table unless needed to explain a handoff.

**Critical trails:** for major business records, add a short trail below
the table, e.g. `Auth request -> DTAQ -> CUE64 -> AUTHLOG -> nightly
recon -> GLPOSTPF`.

---

## Branch Points Section

```markdown
### Branch Points

| Branch Ref | Location (node + line) | Decider | Alternatives | Evidence |
| --- | --- | --- | --- | --- |
| EDGE-ONUS-AUTH-04 / EDGE-ONUS-AUTH-05 | NODE-02 CU110A:300 | Decision field from credit check | A → continue to NODE-04; D → return decline to NODE-01 | EV-... |
| EDGE-ONUS-AUTH-08 / EDGE-ONUS-AUTH-09 | NODE-05 CU130A:140 | CVV match result | matched → continue; mismatched → reject path | EV-... |
```

**Unhandled branch destinations** (e.g., an option code the dispatcher
doesn't recognize) must be listed explicitly. If unhandled → TBD.

---

## UI Surfaces Section

For interactive flows only. Otherwise: `N/A — non-interactive flow`.

```markdown
### UI Surfaces

| Surface ID | Object | Type | Displayed By | Key Fields | F-Keys Handled | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| UI-CUST-LOOKUP-01 | CU200D | DSPF | NODE-01 (CU200A) | CustID | F3=Exit, F6=New, F12=Cancel | EV-... |
| UI-CUST-LOOKUP-02 | CU200D2 | DSPF (subfile) | NODE-01 (CU200A) | CustID, CustName, Status | F3, F6, F12; subfile options 5=Display, 9=Approve | EV-... |
```

---

## Error Propagation & Commit Boundaries Section

See `error-propagation.md` for full guidance.

```markdown
### Error Propagation

| Error Source | Detected At | Propagation Path | Final Outcome | Commit Behavior | Evidence |
| --- | --- | --- | --- | --- | --- |
| Credit-check failure | NODE-03 (CU111S) | RC=-1 returned to NODE-02, which sets Decision='D', returns to NODE-01 | Decline response to Visa | nothing committed (read-only) | EV-... |
| CVV mismatch | NODE-05 | logged to QSYSOPR, returned to NODE-04, response built by NODE-06 | Decline response + log audit row in TXNLOGPF | TXNLOGPF write committed | EV-... |
| DB read I/O error in CU111S | NODE-03 | unhandled (no MONITOR) | flow aborts; Visa times out | nothing committed | needs_sme_review per TBD |

### Commit Boundaries

The flow has the following commit boundaries:

- **Boundary 1:** NODE-04 writes TXNLOGPF (committed implicitly at WRITE)
- **Boundary 2:** NODE-06 sends response to Visa (final, irrevocable)

Between Boundary 1 and Boundary 2 there is a window: if NODE-06 fails,
TXNLOGPF has a row but Visa got no response. Visa will retry. → TBD:
confirm idempotency strategy.
```

---

## Business Capability Seeds Section

Each seed is a **business-language question for SME**, with technical pointers
kept in evidence — *never* an asserted rule.

```markdown
### Business Capability Seeds

These seeds are candidate business rules and capabilities suggested by
the flow structure. SME and `legacy-spec-writer` resolve them; the
flow analyzer does not declare rules.

| Seed ID | Candidate Rule / Capability | Business Signal | Evidence Basis | SME Question |
| --- | --- | --- | --- | --- |
| SEED-ONUS-AUTH-01 | Credit limit must be respected on every authorization | Authorization decision is made before approval is returned | NODE-02 CU110A always calls credit check before approval | Is "no authorization above credit limit" a required business rule for this flow, or only one implementation path? |
| SEED-ONUS-AUTH-02 | CVV/CVC verification may be required for ATM/POS transactions | Transaction type changes the validation path | NODE-05 conditional on transaction-type field | Which transaction types require CVV/CVC verification? |
| SEED-ONUS-AUTH-03 | Authorization decisions may require durable audit before response | The flow records the decision before responding | NODE-04 writes TXNLOGPF before NODE-06 builds response | Is decision logging a hard audit requirement, or best-effort operational logging? |
```

---

## TBDs & Blocking Status Section

Same conventions as program-analyzer. Group by:

- **Pending Source** — missing program-analysis, missing DSPF, missing
  copybook
- **Pending SME Judgment** — trigger model unclear, error intent unclear,
  capability seed unanswered
- **Non-Blocking** — known gaps that don't affect downstream

---

## Review Checklist Section

```markdown
### Review Checklist

Before approval, SME must validate:

- [ ] Trigger model correctly identified
- [ ] Business event name accurately reflects the business transaction
- [ ] All nodes in scope (no missing, no extras)
- [ ] All edges reflect actual production calls
- [ ] Cross-program data flow captures carriers, producers, consumers, timing, and state impacts
- [ ] Branch points capture user-visible decisions
- [ ] UI surfaces match production screens (interactive flows only)
- [ ] Error propagation matches operational reality
- [ ] Commit boundaries correctly identified
- [ ] Capability seeds are reasonable questions, not invented rules
- [ ] All node program-analyses are approved

### SME Sign-Off

- **Reviewer:** ____________________
- **Review Date:** __________________
- **Decision:** approved | approved_with_non_blocking_tbd | rejected
- **Notes:** ____________________
```

---

## Evidence Taxonomy

Flow analysis requires **evidence** for every edge, data exchange, branch point, and trigger. This section defines what counts as authoritative evidence.

### Evidence Types

**1. Source Statement** (highest confidence for call flow)
- CALL / CALLP / CALLPRC in RPGLE
- CALL / SBMJOB in CL
- Trigger registration in CL (ADDPFTRG result, trigger program declaration)
- Example: EV-*: RECONCL line 38 CALL PGM(RECON01R)

**2. IBM i Object / Config Export** (authoritative for configuration)
- WRKJOBSCDE entry details (scheduler frequency, submitted command)
- DDS export for DSPF / PRTF / MENU (option codes, F-key handlers)
- ADDPFTRG output or trigger configuration listing
- File relationship details from DSPF (subfile control records, SFLCTL keywords)
- Example: EV-*: WRKJOBSCDE export, entry NIGHTLY-RECON (daily Mon-Fri 22:00)

**3. Integration Contract** (authoritative for external triggers)
- MQ queue configuration (queue name, message contract, publishing system)
- API gateway route definition and payload schema
- DDM registration for remote program calls
- FTP / IFS drop location and file format contract
- HTTP endpoint and request/response schema
- Example: EV-*: MQ queue WEBORDER.IN documented contract (JSON schema version 2.1)

**4. SME Confirmation** (authoritative for business context and intent)
- Documented BAU (business-as-usual) procedure or runbook
- Production execution procedures or disaster recovery playbook
- System-integration agreement with another department or external party
- Business event name and SLA confirmation
- Example: EV-*: Anna Chen (Finance Ops) confirmed: "Reconciliation must complete before 06:00 next-day GL consolidation"

### Using Multiple Evidence Types

A single edge or feature may require evidence from multiple types:

- **Scheduler entry submitting a batch job:** Evidence type 2 (WRKJOBSCDE export) + type 4 (SME confirmation of frequency and business meaning)
- **Trigger program defined by code + evidence of execution:** Evidence type 1 (ADDPFTRG statement in CL) + type 4 (SME confirmation of when trigger fires)
- **Remote program call:** Evidence type 3 (DDM or MQ contract) + type 4 (SME confirmation of partner system and SLA)
- **F-key dispatcher:** Evidence type 2 (DSPF DDS export showing CAxx keywords) + type 1 (IF/WHEN statements in source showing which programs are called)

### When TBD Is Required

If an edge or feature lacks evidence:
- `TBD-*: pending_source` — Missing type 1 or type 2 evidence (source code / config export)
- `TBD-*: pending_sme_judgment` — Missing type 4 evidence (SME confirmation of intent / business meaning)
- `TBD-*: non_blocking` — Evidence is weak but analysis can continue; noted for downstream review

---

## ID Conventions for Flow Analysis

| Prefix | Artifact | Example |
|---|---|---|
| `FLOW-` | the flow itself | `FLOW-ONUS-AUTH-001` |
| `NODE-` | one program participating in the flow | `NODE-ONUS-AUTH-03` |
| `EDGE-` | one call between two nodes | `EDGE-ONUS-AUTH-04` |
| `DATA-` | one data exchange / carrier touch (parameter set, DTAARA, DTAQ, shared file, screen field, message, IFS, manual handoff) | `DATA-ONUS-AUTH-02` |
| `UI-` | a UI surface (DSPF / PRTF / MENU) | `UI-ONUS-AUTH-01` |
| `SEED-` | a business-capability seed (question for SME) | `SEED-ONUS-AUTH-02` |
| `TBD-` | an open question | `TBD-ONUS-AUTH-005` |
| `EV-` | a piece of evidence | `EV-ONUS-AUTH-012` |

All IDs scope-prefixed by FLOW-SLUG so they remain unique across modules.
