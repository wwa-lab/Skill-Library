# Expected Output: Incomplete Module (Negative Case)

## Input

A module definition for `MODULE-ORDER-MGMT-001` with three flows
in scope:

- FLOW-ORDER-INTAKE-001 — ✅ approved flow analysis
- FLOW-ORDER-VALIDATE-001 — ❌ no flow analysis yet (only program analyses exist)
- FLOW-ORDER-FULFILL-001 — ✅ approved

Plus: SME contact for the module is **not yet assigned**.

## Expected Module-Analyzer Behavior

The skill must **refuse to produce all four views** and instead produce a
`module-overview.md` marked `blocked_pending_source` with explicit
routing back to upstream skills.

### Correct module-overview.md

```markdown
# Module: Order Management (MODULE-ORDER-MGMT-001) — BLOCKED

## Metadata
- **Module ID:** MODULE-ORDER-MGMT-001
- **Business Name:** Order Management
- **Scope Statement:** (pending — no SME contact)
- **Module Owner:** **NOT YET ASSIGNED**
- **In-scope Flows:**
  - FLOW-ORDER-INTAKE-001 ✅
  - FLOW-ORDER-VALIDATE-001 ❌ NO FLOW ANALYSIS
  - FLOW-ORDER-FULFILL-001 ✅
- **Status:** **blocked_pending_source**

## View Index
| View | File | Status |
| --- | --- | --- |
| 1. Operation Flow | (not produced) | blocked — no SME |
| 2. System Flow | (not produced) | blocked — incomplete inputs |
| 3. Program Flow | (not produced) | blocked — flow missing |
| 4. Data Flow | (not produced) | blocked — flow missing |

## Blocking TBDs

### Pending Source (routes back to upstream skills)

- **TBD-ORDER-MGMT-001:** FLOW-ORDER-VALIDATE-001 lacks an approved flow analysis
  - Blocking: pending_source
  - Routes to: `legacy-ibmi-flow-analyzer`
  - Action: produce `flow-ORDER-VALIDATE-001.md` first

### Pending SME Judgment

- **TBD-ORDER-MGMT-002:** No SME contact assigned for this module
  - Blocking: pending_sme_judgment
  - Routes to: SME assignment process
  - Action: identify module owner; View 1 cannot be produced without SME
    input on business scope, actors, BAU rhythm

## Why The Module Cannot Be Synthesized Yet

- View 1 (Operation Flow) requires SME input on business scope, actors,
  and BAU — none of which is in code. Without an assigned SME, View 1
  would be pure invention.
- View 3 (Program Flow) requires all in-scope flow analyses to aggregate.
  Missing FLOW-ORDER-VALIDATE-001 means View 3 would have a gap of
  unknown size.
- View 4 (Data Flow) depends on every flow's data-flow section. Missing
  flow → missing data exchanges → incomplete picture.
- View 2 (System Flow) could partially be derived from the two completed
  flows, but would still miss whatever upstream/downstream systems
  appear only in the missing flow.

## Routing Decision

The orchestrator should:

1. Route to `legacy-ibmi-flow-analyzer` for FLOW-ORDER-VALIDATE-001
2. In parallel, escalate SME assignment
3. After both unblock, re-run module-analyzer with the same input

## Sign-Off
- **Module Owner:** NOT YET ASSIGNED
- **Decision:** blocked_pending_source
```

## Why This Output Is Correct

- ✅ Refuses to produce View 1/3/4 with missing inputs
- ✅ Does not invent business scope, actors, or BAU
- ✅ Does not produce a partial View 3 omitting the missing flow silently
- ✅ Explicit routing to flow-analyzer for the missing flow
- ✅ Escalates SME assignment as a separate blocker

## What the Analyzer Must NOT Do

- ❌ Produce a "best-effort" module overview by ignoring FLOW-ORDER-VALIDATE
- ❌ Invent business actors or BAU from program names
- ❌ Write View 4 with only the data objects visible in the 2 available flows
- ❌ Approve the module despite blocking TBDs

## The Anti-Hallucination Test

Delete one in-scope flow analysis and re-run. If the module-analyzer
produces any output other than a `blocked_pending_source` overview with
explicit routing, something is wrong.

This example exists to make blocked output the obvious, documented
expected behavior — preventing module syntheses from quietly papering
over upstream gaps.
