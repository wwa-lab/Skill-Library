# Review Notes: Why This Menu-Flow Analysis Is Good

## What This Example Demonstrates

- ✅ Interactive trigger (\*MENU + option) correctly handled
- ✅ 3 DSPFs (search / detail / subfile) cleanly documented in UI Surfaces
- ✅ F-key handling (F3 / F11 / F12) captured as branch points
- ✅ Subfile option dispatch captured as a branch point
- ✅ Re-entrant program (CUSTINQ appears multiple times in sequence) modeled correctly — same NODE-01 cycled through different DSPF screens
- ✅ Read-only flow explicitly stated for commit boundaries (no fabrication)
- ✅ "Silent option drop" captured as a SEED, not asserted as correct UX

## Key Patterns Demonstrated

### 1. Re-entrant Orchestrator Node
CUSTINQ is shown multiple times in the Transaction Call Map, but it's still
one Node (NODE-01). This is correct: the same program cycles between
showing DSPFs and calling workers. We do not create separate nodes for
each visit.

### 2. F-Key Branch Inside an Interactive Flow
The flow is not just menu-triggered — it has further F-key driven branches
inside (F11 to show history). Captured through EDGE-CUST-INQUIRY-03 plus
NODE-CUST-INQUIRY-01 exit paths.

### 3. Subfile Option Dispatch as a Branch
Subfile option codes are a separate branch type under
NODE-CUST-INQUIRY-01 subfile dispatch. Documents both the handled option
(5=Display) and the unhandled-option behavior (silent drop) — the latter as
a SEED for SME.

### 4. Read-Only Flow with No Commit Boundaries
Explicit "no commit boundaries — read-only" rather than leaving the
section empty. Tells the SME this is intentional, not an oversight.

## What Would Disqualify This Analysis

- ❌ Inventing CSR permissions ("only managers can see option 9") without SME
- ❌ Asserting "90 days is regulatory" without SME (it's just code)
- ❌ Drawing a separate NODE for each DSPF screen (DSPFs aren't programs)
- ❌ Calling it "FLOW-CUSTINQ-001" (program name) instead of business event name
- ❌ Treating subfile options 1, 2, 4, 9 as branches when source only handles 5

## When To Pick MENU vs Subfile-Dispatch vs F-Key Trigger Model

This flow chose **MENU** as the primary trigger because the *entry into
the flow* is option 5 on CSRMENU. The subsequent F-keys and subfile
options are **branches within** the flow, not separate flows.

Alternative valid framings:
- Treat F11→TXNHIST as its own sub-flow → finer granularity, more flows
- Treat subfile option 5 as its own sub-flow → very fine granularity

Pick the granularity the SME thinks in: if Liu Wei describes "customer
inquiry" as one workflow, model it as one flow.
