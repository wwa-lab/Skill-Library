# Runtime Evidence Mining Review Checklist

**Capability**: [CAPABILITY-SLUG]  
**Mining Date**: [DATE]  
**Miner**: [LEGACY-IBMI-RUNTIME-EVIDENCE-MINER V0.1.0]  
**SME Reviewer**: [NAME]  
**Review Date**: [DATE]  

---

## Pre-Mining Verification

- [ ] Evidence manifest is approved for inventory (status: approved_for_inventory or later)
- [ ] All job logs are listed in manifest with sensitivity status
- [ ] All spool/report files are listed in manifest with sensitivity status
- [ ] Confidential artifacts are marked redaction_status: approved (redacted)
- [ ] No unredacted sensitive data in logging artifacts
- [ ] Inventory complete and available (01_inventory/inventory.yaml)

---

## Call Sequence Observations

**Question**: Do the observed program call sequences match your understanding of how this capability works?

| Observation | From Programs | Matches Code? | Matches Your Knowledge? | Notes |
|---|---|---|---|---|
| RTE-CREDIT-CHECK-001 | CREDITCHK → VALIDATECREDIT → CALCFEE → UPDATEACCOUNT | ☐ Yes ☐ No ☐ Partial | ☐ Yes ☐ No ☐ Partial | |
| [ADD MORE ROWS AS NEEDED] | | ☐ Yes ☐ No ☐ Partial | ☐ Yes ☐ No ☐ Partial | |

**Follow-up**: Are there program calls you expected but did NOT see in the logs?
- [ ] No, all expected calls are present
- [ ] Yes, the following calls are missing:
  - [Program name]: ___________ (dead code? or logs incomplete?)

---

## Error Pattern Observations

**Question**: Are the error messages and recovery paths typical BAU or exceptional?

| Error Code | Context | Observed Recovery | Is This Expected? | Notes |
|---|---|---|---|---|
| CPF5003 | FILE LOCKED on CUSTFILE during UPDATE | Automatic retry, 2-second wait | ☐ Yes ☐ No ☐ Rare | |
| [ADD MORE] | | | ☐ Yes ☐ No ☐ Rare | |

**Follow-up**: Which of these errors should be treated as business-as-usual (expected handling) vs. exceptions to investigate?
- [ ] All are expected BAU
- [ ] Some are exceptions:
  - [Error code] _________: [Expected or not]

---

## Timing & Batch Window Observations

**Question**: Are the batch windows and execution timings correct?

| Observation | Expected? | Typical Range | Notes |
|---|---|---|---|
| BATCHRECON runs 01:00–02:30 UTC nightly | ☐ Yes ☐ No | 85–92 minutes | |
| VALIDATECREDIT: 150–200 milliseconds | ☐ Yes ☐ No | per-transaction | |
| [ADD MORE] | ☐ Yes ☐ No | | |

**Follow-up**: Has there been recent change in batch windows (e.g., moved to different time, duration changed)?
- [ ] No recent changes; observations reflect current BAU
- [ ] Yes, changed: [describe when and why]

---

## Report Structure Observations

**Question**: Do the extracted report structures match what you expect?

| Report | Field Count | Header Lines | Footer Lines | Matches Expectation? |
|---|---|---|---|---|
| CREDITRPT | 8 fields | 1–3 | 195–200 | ☐ Yes ☐ No ☐ Partial |
| [ADD MORE] | | | | ☐ Yes ☐ No ☐ Partial |

**Follow-up**: Do reports vary significantly in structure across runs (e.g., conditional sections)?
- [ ] Structure is consistent across all observed runs
- [ ] Structure varies:
  - [Describe what varies and under what conditions]

---

## Data Values & Field Ranges

**Question**: Do the observed field value ranges match what you expect?

| Field | Data Type | Observed Range | Expected Range | Match? |
|---|---|---|---|---|
| AMOUNT | Monetary | 100.00–500000.00 | 0.00–999999.99 | ☐ Yes ☐ No ☐ Wider |
| CUST_ID | Numeric | 1–99999 | 1–999999 | ☐ Yes ☐ No ☐ Wider |
| [ADD MORE] | | | | ☐ Yes ☐ No ☐ Wider |

**Follow-up**: Were there any unusual or boundary values observed?
- [ ] All values within expected range
- [ ] Unusual values:
  - [Field]: [Value observed] — [Is this valid or an error?]

---

## Confidence Scoring Review

**Question**: Are the confidence levels justified?

| Observation | Confidence | Evidence Count | Justified? | Adjust To? |
|---|---|---|---|---|
| RTE-CREDIT-CHECK-001 (call_sequence) | High | 5 runs | ☐ Yes ☐ No | ☐ High ☐ Medium ☐ Low |
| RTE-CREDIT-CHECK-002 (error_pattern) | High | 3 occurrences | ☐ Yes ☐ No | ☐ High ☐ Medium ☐ Low |
| RTE-CREDIT-CHECK-003 (batch_window) | High | 5 nights | ☐ Yes ☐ No | ☐ High ☐ Medium ☐ Low |
| RTE-CREDIT-CHECK-004 (report_structure) | High | 3 spool files | ☐ Yes ☐ No | ☐ High ☐ Medium ☐ Low |
| RTE-CREDIT-CHECK-005 (timing_observation) | High | 5 runs | ☐ Yes ☐ No | ☐ High ☐ Medium ☐ Low |
| [ADD MORE] | | | ☐ Yes ☐ No | ☐ High ☐ Medium ☐ Low |

---

## Contradictions & TBDs

**Question**: Are there any contradictions between runtime observations and code analysis?

| Potential Contradiction | Observation 1 | Observation 2 | Resolution |
|---|---|---|---|
| [Example: Call sequence] | RTE-CREDIT-CHECK-001: A→B→C observed | Program analysis says A→C→B | ☐ Confirm which is correct ☐ Both valid (conditional) ☐ TBD for investigation |
| [ADD MORE] | | | |

**Question**: Are there observations that need SME judgment (marked as TBD)?

- [ ] No TBDs; all observations are clear
- [ ] Yes, the following need review:
  - RTE-CREDIT-CHECK-NNN: [Description of what needs clarification]

---

## Sensitive Data & Redaction

**Question**: Have sensitive data been properly handled?

- [ ] No unredacted customer names, account numbers, or personal identifiers in observations
- [ ] Field value ranges recorded instead of actual values (e.g., "1000.00–9999.99" not "2345.67")
- [ ] All observations traceable to evidence manifest (EV-* IDs present)

---

## Completeness & Gaps

**Question**: Is the mining coverage sufficient?

- [ ] All programs in scope have call sequence observations
- [ ] All significant error conditions are documented
- [ ] Batch timing and windows are clear
- [ ] Report structures (if applicable) are documented
- [ ] Interactive flow (if applicable) is documented

**Question**: Are there gaps in the evidence?

- [ ] No gaps identified
- [ ] Gaps exist:
  - [Program/file name]: [What's missing and why?]
  - [Program/file name]: [What's missing and why?]

---

## Overall Assessment

### Mining Quality
- [ ] Excellent — observations are complete, accurate, and actionable
- [ ] Good — observations are mostly complete with minor gaps
- [ ] Acceptable — observations cover main flows; some details missing
- [ ] Poor — observations are incomplete or have accuracy issues

### Recommendation
- [ ] **APPROVE** — Ready to use in downstream analysis (program/flow/module analyzers)
- [ ] **APPROVE WITH NOTES** — Approve but flag specific TBDs for ongoing investigation
- [ ] **REQUEST REVISION** — Return to mining; need more evidence or clarification on [specific points]
- [ ] **REJECT** — Do not use; contradictions or gaps are too significant

### SME Notes

[Use this space for any comments, concerns, or additional context the SME wants to record]

---

## Sign-Off

**SME Reviewer Name**: ___________________________

**SME Signature/Approval**: ___________________________

**Date**: ___________________________

**Overall Status**: ☐ APPROVED ☐ APPROVED WITH NOTES ☐ REJECTED

---

## Next Steps (if Approved)

1. observations marked `sme_review_status: "draft"` will be updated to `"approved"` (or `"rejected"`)
2. Observations will be consumed by:
   - [ ] `legacy-ibmi-program-analyzer` (optional runtime_hints)
   - [ ] `legacy-ibmi-flow-analyzer` (optional bau_notes)
   - [ ] `legacy-ibmi-module-analyzer` (View 1 context)
3. Any TBDs flagged here will be tracked as `pending_sme_judgment`
4. Archive this completed checklist with the final observations JSON

---

## Revision History

| Date | Revision | Reviewer | Change Summary |
|---|---|---|---|
| [DATE] | 1.0 | [NAME] | Initial mining review |
| | | | |
