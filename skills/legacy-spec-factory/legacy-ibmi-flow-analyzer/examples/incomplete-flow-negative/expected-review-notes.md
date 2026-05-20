# Expected Review Notes: Incomplete Flow (Negative Case)

## What This Example Demonstrates

This is a **negative case** — the input is *not* yet ready for full flow
analysis. The analyzer must:

1. ❌ **NOT** proceed with full analysis
2. ❌ **NOT** invent program behavior to fill the gaps
3. ✅ Produce a **blocked** flow stub
4. ✅ Route back to `legacy-ibmi-program-analyzer` for each missing program
5. ✅ Optionally route to inventory if `relationships` are uncertain

---

## Correct Output for This Input

```markdown
# Flow Analysis: Web Order Submission (FLOW-WEB-ORDER-001) — BLOCKED

## Metadata

- **Flow ID:** FLOW-WEB-ORDER-001
- **Business Event Name:** (pending SME confirmation)
- **Trigger Model:** API / Remote (MQ queue WEBORDER.IN)
- **Module:** ORDER-SUBMIT
- **Status:** **blocked_pending_source**

## Trigger Context
(partial — captured what's known about the MQ trigger)

## Transaction Call Map

```text
[MQ WEBORDER.IN]
    │
    ▼
NODE-01 (WEBORDIN)  ── ✅ approved
    │
    ▼
NODE-02 (ORDVAL)    ── ✅ approved
    │
    ▼
NODE-03 (ORDPRICE)  ── ❌ NO program-analysis
    │
    ▼
NODE-04 (ORDPERSIST) ── ✅ approved
    │
    ▼
NODE-05 (WEBORDOUT) ── ❌ NO program-analysis
    │
    ▼
[MQ WEBORDER.OUT — assumed; not confirmed]
```

## Nodes

| Node | Program | Program Analysis | Status |
| --- | --- | --- | --- |
| NODE-01 | WEBORDIN | ✅ | OK |
| NODE-02 | ORDVAL | ✅ | OK |
| NODE-03 | ORDPRICE | ❌ | **MISSING** |
| NODE-04 | ORDPERSIST | ✅ | OK |
| NODE-05 | WEBORDOUT | ❌ | **MISSING** |

## TBDs & Blocking Status

### Pending Source (BLOCKING — analysis cannot proceed)

- **TBD-WEB-ORDER-001:** ORDPRICE lacks approved program-analysis
  - Routes to: `legacy-ibmi-program-analyzer` with input OBJ-ORDER-SUBMIT-003
  - Blocking: pending_source
  - Question: Run program-analyzer on ORDPRICE before continuing.

- **TBD-WEB-ORDER-002:** WEBORDOUT lacks approved program-analysis
  - Routes to: `legacy-ibmi-program-analyzer` with input OBJ-ORDER-SUBMIT-005
  - Blocking: pending_source
  - Question: Run program-analyzer on WEBORDOUT before continuing.

- **TBD-WEB-ORDER-003:** No SME contact identified for this flow
  - Routes to: SME assignment process
  - Blocking: pending_sme_judgment
  - Question: Business event name, expected SLA, retry contract not confirmable without SME.

## Why This Output Is Correct

- ✅ Does not invent ORDPRICE or WEBORDOUT behavior
- ✅ Does not guess what MQ payload looks like (would need SME / contract doc)
- ✅ Explicitly marks status as blocked
- ✅ Names the exact next step (run program-analyzer)
- ✅ Distinguishes pending_source (analyses missing) from pending_sme (business context missing)
```

---

## What the Analyzer Must NOT Do

### ❌ Invent ORDPRICE Behavior
"ORDPRICE looks up tier pricing and applies discounts based on customer
loyalty level."

→ Wrong. There is no program-analysis for ORDPRICE. The analyzer doesn't
know what it does. Saying anything specific is hallucination.

### ❌ Skip the Missing Programs
Pretending the chain is `WEBORDIN → ORDVAL → ORDPERSIST` and ignoring
ORDPRICE and WEBORDOUT.

→ Wrong. The inventory `relationships` indicate ORDPRICE and WEBORDOUT
are in the chain. Skipping them produces a flow that doesn't match
production behavior.

### ❌ Guess the MQ Payload Format
"The inbound message is JSON with fields: orderId, customerId, items[]."

→ Wrong. The MQ contract is not in source code; it's in an integration
agreement (system flow, not program flow). Without that document or SME
confirmation, the analyzer doesn't know.

### ❌ Produce a "Best-Effort" Approved Flow
Marking the flow as `approved_with_non_blocking_tbd` and saying "missing
program analyses are not blocking because we have most of the chain."

→ Wrong. Missing program analyses are **blocking** — the flow is
fundamentally incomplete. A spec built on a partial flow will encode the
wrong behavior.

---

## Routing Decision

The orchestrator should:

1. Mark this flow as `blocked_pending_source`
2. Spawn (or recommend the user run) `legacy-ibmi-program-analyzer` for
   OBJ-ORDER-SUBMIT-003 and OBJ-ORDER-SUBMIT-005
3. After both program-analyses are approved, re-run flow-analyzer with
   the same input
4. In parallel, request SME assignment to confirm business event name
   and SLA

---

## The Anti-Hallucination Test

A good test for any flow analysis: **delete one node's program-analysis
file. Re-run the flow analyzer. If it produces anything other than a
blocked output, something is wrong.**

This example exists specifically to make the blocked output the obvious,
documented expected behavior.
