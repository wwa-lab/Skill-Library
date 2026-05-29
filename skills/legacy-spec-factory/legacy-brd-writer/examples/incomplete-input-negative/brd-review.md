# BRD Review Checklist: Order Routing (BLOCKED)

**BRD ID:** `BRD-ORDER-ROUTING-001`  
**Capability Owner (SME):** Sarah Lee (Order Fulfillment Manager)  
**Review Date:** `Not yet reviewed (blocked pre-review)`  
**Status:** `blocked`

---

## PRE-REVIEW ASSESSMENT: BLOCKER FOUND

**This BRD has been blocked BEFORE SME review due to missing upstream inputs
and evidence gaps.**

Do not proceed to SME review. The BRD cannot be validated without resolving
these blockers.

---

## Blocking Issues (Must Resolve Before SME Review)

### 1. BLOCKER: Missing Flow Analysis

**Issue:** Module analysis references `FLOW-ORDER-ROUTING-001` but the
approved flow analysis is not available.

**Evidence Gap:** `TBD-ORDER-ROUTING-003`

**Action Required:**
- [ ] Flow analyzer must complete `02_flows/flow-ORDER-ROUTING.md`
- [ ] Flow analysis must reach `approved` or `approved_with_non_blocking_tbd`
  status
- [ ] After flow is available, re-attempt BRD synthesis

**Resolver:** Flow Analyzer  
**Timeline:** Blocking — cannot proceed without this

---

### 2. BLOCKER: Program Flow Logic Not Detailed

**Issue:** Program analysis for `SELECT-FULFILLMENT-CENTER` routine only shows
the routine name and a comment. The actual control flow (which attributes are
checked? what is the algorithm?) is not extracted.

**Evidence Gap:** `TBD-ORDER-ROUTING-001`

**Action Required:**
- [ ] Program analyzer must re-examine the `SELECT-FULFILLMENT-CENTER` routine
- [ ] Detailed control flow must be documented: IF conditions, field checks,
  assignments
- [ ] After detailed analysis is available, re-attempt BRD synthesis

**Resolver:** Program Analyzer  
**Timeline:** Blocking — cannot write BRD without understanding logic

---

### 3. BLOCKER: Geographic Logic Not Evidenced

**Issue:** The draft must not claim "orders are assigned based on geographic
location" because only a code comment supports this. No actual geographic
lookup logic (ZIP code comparison, regional table, etc.) is shown in the program
analysis.

**Evidence Gap:** `TBD-ORDER-ROUTING-002`

**Action Required:**
- [ ] Program analyzer must show the actual geographic lookup logic
- [ ] Or: SME must clarify whether geographic routing is real or comment error
- [ ] After clarification, either add the behavior with evidence or keep it as
      a TBD

**Resolver:** Program Analyzer or SME  
**Timeline:** Blocking — cannot claim behavior without code evidence

---

### 4. BLOCKER: Scope Ambiguity

**Issue:** BRD scope states "shipping method selection" is in-scope, but all
behaviors describe "fulfillment center selection". Are these the same algorithm
or different?

**Evidence Gap:** `TBD-ORDER-ROUTING-004`

**Action Required:**
- [ ] SME must clarify: is shipping method selection part of this capability or
  a separate one?
- [ ] Update scope statement to match behaviors
- [ ] Or split into two capabilities if needed

**Resolver:** SME  
**Timeline:** Blocking — scope must be clear before SME review

---

### 5. BLOCKER: Business Rule Unclear

**Issue:** `BR-ORDER-ROUTING-001` cannot safely state whether routing should
minimize cost, minimize delivery time, balance both, or use another business
objective.

**Evidence Gap:** `TBD-ORDER-ROUTING-005`

**Action Required:**
- [ ] SME must specify business objective: minimize cost, minimize delivery
  time, or balance both?
- [ ] After SME decision, update BR-001 statement with clear objective
- [ ] Obtain SME confirmation

**Resolver:** SME  
**Timeline:** Blocking — business rule cannot be approved without clarity

---

## Recommendation

**Status:** `blocked` — Do not forward to SME review until all blocking TBDs
are resolved.

**Remediation Path:**

1. **First:** Flow analyzer provides `flow-ORDER-ROUTING.md` (blocking for BRD
   synthesis)
2. **Second:** Program analyzer re-runs with detailed control flow extraction
   (blocking for evidence)
3. **Third:** SME clarifies scope and optimization objective (blocking for
   business rule)
4. **Then:** Return BRD to author for synthesis with complete inputs
5. **Finally:** SME conducts full review with blocking issues resolved

**Estimated Timeline:** Depends on flow and program analyzer availability.
Cannot estimate without upstream work.

---

## Why This Example Matters

This example shows the **gate function** of the BRD step:

- **Good:** Upstream skills (flow analyzer, program analyzer) surface incomplete
  work EARLY
- **Good:** SME questions are surfaced EARLY so they can be investigated before
  expensive spec-writing
- **Bad:** If we ignored these blockers and submitted an incomplete BRD to SME
  anyway, the SME would reject it anyway (wasting their time)

**The BRD writer's job includes saying "No, this input is not ready" and
surfacing exactly what is missing.**

---

## Next Steps After Blockers Are Resolved

Once all blockers are addressed:

1. Author revises BRD with complete information
2. SME reviews revised BRD
3. SME completes `brd-review.md` with final decision (approved /
   needs_revision / rejected)
4. If approved, forward to spec-writer

---

**Assessment completed by:** Claude Code (2026-05-15)  
**Status:** `blocked` — awaiting upstream inputs and SME clarification
