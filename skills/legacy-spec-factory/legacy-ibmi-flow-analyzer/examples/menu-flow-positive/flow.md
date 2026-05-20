# Flow Analysis: Customer Inquiry from CSR Menu (FLOW-CUST-INQUIRY-001)

## Metadata

- **Flow ID:** FLOW-CUST-INQUIRY-001
- **Business Event Name:** Customer service rep customer lookup and transaction history view
- **Trigger Model:** Interactive Menu (`*MENU CSRMENU`, option 5)
- **Module:** CUST-INQUIRY
- **Entry Node:** NODE-CUST-INQUIRY-01 (CUSTINQ / OBJ-CUST-INQ-001)
- **Exit Node:** NODE-CUST-INQUIRY-01 (same — control returns to menu after exit)
- **Runtime Model:** Synchronous, interactive, sub-second per screen
- **Status:** draft

---

## Trigger Context

- **Trigger Artifact:** `*MENU CSRMENU`, option `5 = Customer Inquiry`
- **Source / Configuration:** Menu source `CSRMENU` (MENU source member) — option 5 dispatches `CALL PGM(CUSTINQ)`
- **Caller / Initiator:** Customer service representatives (CSR role)
- **Frequency:** ~40 invocations per CSR per shift (SME estimate)
- **SLA:** Sub-second screen response; no formal SLA
- **Authentication Context:** Inherits user's IBM i profile; CSR group permission required to see option 5
- **Evidence:** [EV-CUST-INQUIRY-001: CSRMENU source option 5]

---

## Transaction Call Map

Source: derived-from-code + SME confirmed

```mermaid
flowchart LR
  MENU["CSRMENU option 5"]
  CUSTINQ["NODE-01 CUSTINQ"]
  CUSTLKP["NODE-02 CUSTLKP"]
  TXNHIST["NODE-03 TXNHIST"]
  MENU --> CUSTINQ
  CUSTINQ --> CUSTLKP
  CUSTINQ --> TXNHIST
```

### Call Chain Summary

```text
[CSR on CSRMENU; selects option 5]
    │
    ▼
NODE-01 (CUSTINQ)   ── shows DSPF CUSTINQD (search panel)
    │
    │   CSR enters CustID, presses Enter
    ▼
NODE-01 (CUSTINQ)   ── CALLP CUSTLKP(CustID : CustData : RC)
    │
    ▼
NODE-02 (CUSTLKP)   ── CHAIN CUSTMSTR; returns CustData or RC=-1
    │
    ▼
NODE-01 (CUSTINQ)   ── if found, shows DSPF CUSTINQD2 (detail panel)
    │
    │   CSR presses F11 to view transaction history
    ▼
NODE-01 (CUSTINQ)   ── CALLP TXNHIST(CustID : SubfileBuffer : RC)
    │
    ▼
NODE-03 (TXNHIST)   ── reads TXNLOGPF for CustID (last 90 days), populates subfile buffer
    │
    ▼
NODE-01 (CUSTINQ)   ── shows DSPF TXNHISTD (subfile)
    │
    │   CSR enters option 5 next to a row, presses Enter
    ▼   (subfile dispatch — option 5=Display)
NODE-01 (CUSTINQ)   ── opens transaction detail subwindow (same DSPF, different format)
    │
    │   CSR presses F12 to exit
    ▼
[Return to CSRMENU]
```

**Evidence:**
- [EV-CUST-INQUIRY-002: CUSTINQ:120 CALLP CUSTLKP]
- [EV-CUST-INQUIRY-003: CUSTINQ:180 CALLP TXNHIST (after F11)]
- [EV-CUST-INQUIRY-004: CUSTINQ:230 subfile option 5 dispatch]

---

## Nodes

| Node ID | Program (OBJ-*) | Role | Program Analysis | Notes |
| --- | --- | --- | --- | --- |
| NODE-CUST-INQUIRY-01 | CUSTINQ (OBJ-CUST-INQ-001) | orchestrator + UI | program-analysis-OBJ-CUST-INQ-001.md | Drives 3 DSPFs; calls lookup and history workers |
| NODE-CUST-INQUIRY-02 | CUSTLKP (OBJ-CUST-INQ-002) | data-access | program-analysis-OBJ-CUST-INQ-002.md | CHAIN on CUSTMSTR; pure lookup |
| NODE-CUST-INQUIRY-03 | TXNHIST (OBJ-CUST-INQ-003) | data-access | program-analysis-OBJ-CUST-INQ-003.md | READE on TXNLOGPF; populates subfile buffer |

**Missing program analyses:** none.

---

## Edges

| Edge ID | From -> To | Via | Call Type | Site | Condition | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| EDGE-CUST-INQUIRY-01 | (MENU option 5) -> NODE-01 | N/A | MENU-option | CSRMENU opt 5 | user selects | EV-001 |
| EDGE-CUST-INQUIRY-02 | NODE-01 -> NODE-02 | search-handler routine | CALLP | CUSTINQ:120 | always after CustID input | EV-002 |
| EDGE-CUST-INQUIRY-03 | NODE-01 -> NODE-03 | F11-handler routine | CALLP | CUSTINQ:180 | user presses F11 on detail panel | EV-003 |

---

## Common Dependencies

| Common Node | Inbound Callers | Role Classification | Main Graph Treatment | Risk Notes | Evidence |
| --- | --- | --- | --- | --- | --- |
| (none) | N/A | N/A | N/A | no shared common program/API is called by multiple nodes in this flow | EV-002 to EV-003 |

---

## Cross-Program Data Flow

| Data ID | Carrier | Producer | Consumer | Mechanism | Payload / Key Fields | Direction & Timing | State Impact | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DATA-CUST-INQUIRY-01 | EDGE-02 | NODE-01 | NODE-02 / NODE-01 | CALL parameters | CustID (in), CustData DS (out), RC (out) | sync in/out | lookup result returned | EV-... |
| DATA-CUST-INQUIRY-02 | EDGE-03 | NODE-01 | NODE-03 / NODE-01 | CALL parameters | CustID (in), SubfileBuffer (out array), RC (out) | sync in/out | history buffer returned | EV-... |
| DATA-CUST-INQUIRY-03 | CUSTMSTR | NODE-02 | NODE-01 via EDGE-02 | Shared file | full customer master record keyed by CustID | sync lookup | read-only | EV-... |
| DATA-CUST-INQUIRY-04 | TXNLOGPF | NODE-03 | NODE-01 via EDGE-03 | Shared file | last 90 days of CustID transactions | sync lookup | read-only | EV-... |

**Critical trails:**
- Customer identity: DSPF input CustID -> CUSTINQ -> CUSTLKP -> CUSTMSTR -> CustData DS -> CUSTINQ detail panel.
- Transaction history: CUSTINQ F11 branch -> TXNHIST -> TXNLOGPF -> SubfileBuffer -> TXNHISTD subfile.

---

## Branch Points

| Branch Ref | Location | Decider | Alternatives | Evidence |
| --- | --- | --- | --- | --- |
| EDGE-CUST-INQUIRY-02 / NODE-CUST-INQUIRY-01 not-found path | CUSTINQ:135 | RC from CUSTLKP | RC=0 → show detail panel; RC=-1 → show "not found" message on search panel | EV-... |
| EDGE-CUST-INQUIRY-03 / NODE-CUST-INQUIRY-01 exit paths | CUSTINQ:175 | F-key pressed on detail panel | F3 → exit to menu; F11 → EDGE-CUST-INQUIRY-03; F12 → back to search | EV-... |
| NODE-CUST-INQUIRY-01 subfile dispatch | CUSTINQ:225 | Subfile option code | 5 → show detail subwindow; other → ignore (no error) | EV-... |

**Unhandled subfile options:** silent ignore (per NODE-CUST-INQUIRY-01 subfile dispatch) → SEED-CUST-INQUIRY-02 (is this correct UX?)

---

## UI Surfaces

| Surface ID | Object | Type | Displayed By | Key Fields | F-Keys Handled | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| UI-CUST-INQUIRY-01 | CUSTINQD | DSPF | NODE-01 | CustID (input) | F3=Exit, F12=Back | EV-... |
| UI-CUST-INQUIRY-02 | CUSTINQD2 | DSPF | NODE-01 | CustName, Status, OpenDate | F3=Exit, F11=History, F12=Back | EV-... |
| UI-CUST-INQUIRY-03 | TXNHISTD | DSPF (subfile) | NODE-01 | TxnDate, TxnAmount, TxnType, Status; subfile option field | F3=Exit, F12=Back; subfile option 5=Display | EV-... |

---

## Error Propagation & Commit Boundaries

### Error Conditions Per Node

| Node | Error Condition | Detection | Local Handling | Propagated To Caller | Evidence |
| --- | --- | --- | --- | --- | --- |
| NODE-02 | Customer not found | %FOUND check on CHAIN | RC=-1, empty CustData | NODE-01 shows "Customer ID not found" on CUSTINQD | EV-... |
| NODE-02 | CUSTMSTR I/O error | MONITOR | RC=-2 + logs QSYSOPR | NODE-01 shows generic error; CSR retries | EV-... |
| NODE-03 | No transactions found | %EOF check first iteration | RC=0 with empty subfile | NODE-01 shows "No transactions" on TXNHISTD | EV-... |
| NODE-03 | TXNLOGPF I/O error | MONITOR | RC=-1 + logs QSYSOPR | NODE-01 shows generic error | EV-... |

### Flow-Level Error Outcomes

| Trigger Error | What Happens | Operator Visibility | Recovery |
| --- | --- | --- | --- |
| Customer not found | "Not found" message on search panel | none | CSR re-enters CustID |
| CUSTMSTR unavailable | Generic error; flow returns to menu | QSYSOPR | DBA / ops investigates |
| TXNLOGPF unavailable | Generic error; CSR can still see customer detail (NODE-02 already succeeded) | QSYSOPR | DBA / ops investigates |

### Commit Boundaries

This flow is **read-only** — no writes to any file. There are no commit
boundaries. Every error is fully recoverable by the user.

---

## Business Capability Seeds

| Seed ID | Candidate Rule / Capability | Suggested By | SME Question |
| --- | --- | --- | --- |
| SEED-CUST-INQUIRY-01 | CSR role must be authorised to view customer transaction history | Menu option 5 visibility depends on CSR group; data shown is sensitive | What governs CSR access — group profile only, or finer-grained authorities? |
| SEED-CUST-INQUIRY-02 | Unknown subfile options are silently dropped | NODE-CUST-INQUIRY-01 subfile dispatch ignores unrecognised option codes | Is silent drop intentional or should an error be shown? |
| SEED-CUST-INQUIRY-03 | Transaction history limited to 90 days | NODE-03 hard-coded 90-day window | Is 90 days a regulatory limit, performance choice, or arbitrary? |

---

## TBDs & Blocking Status

### Pending Source
- (none — all program-analyses approved)

### Pending SME Judgment
- **TBD-CUST-INQUIRY-001:** Confirm CSR authorisation model
  - Blocking: pending_sme_judgment
  - Related: SEED-01

- **TBD-CUST-INQUIRY-002:** Confirm 90-day window rationale
  - Blocking: pending_sme_judgment
  - Related: SEED-03

### Non-Blocking
- **TBD-CUST-INQUIRY-003:** Silent-drop UX choice
  - Blocking: non_blocking
  - Related: SEED-02

---

## Review Checklist

- [X] Trigger model correctly identified — Interactive Menu
- [X] Business event name confirmed by SME (Liu Wei)
- [X] All nodes in scope
- [X] All edges reflect actual production calls
- [X] Cross-program data flow captures carriers, producers, consumers, timing, and state impact
- [X] Branch points capture user-visible decisions (incl. F-keys and subfile options)
- [X] UI surfaces match production screens — 3 DSPFs documented
- [X] Error propagation matches operational reality
- [X] Commit boundaries: N/A — read-only flow (explicitly documented)
- [X] Capability seeds are reasonable questions
- [X] All node program-analyses approved

### SME Sign-Off

- **Reviewer:** [Liu Wei / CS Ops — pending]
- **Review Date:** [Pending]
- **Decision:** draft → needs_sme_review
- **Notes:** Read-only inquiry flow with clear UI structure; key open items are authorisation model and 90-day window rationale.
