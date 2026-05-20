# Expected TBD Findings: Incomplete Log Example

## Overview

This example demonstrates graceful handling of a truncated job log. The log ends abruptly during error recovery, leaving several observations incomplete.

## Expected Observations (with TBDs)

### RTE-NNN-001: call_sequence
**Status**: PARTIAL
- **Statement**: "CREDITCHK calls VALIDATECREDIT, then CALCFEE, then UPDATEACCOUNT (partial flow observed)"
- **Confidence**: low (calls observed but recovery/completion unknown)
- **Supporting Detail**:
  - Call chain: VALIDATECREDIT → CALCFEE → UPDATEACCOUNT (start only)
  - Timestamps: 01:00:30 → 01:02:35 → 01:02:40
  - Note: "Log ends abruptly at line 50; UPDATEACCOUNT call sequence incomplete"
- **TBD**: "pending_source: Did UPDATEACCOUNT complete successfully, or was it interrupted?"

### RTE-NNN-002: error_pattern
**Status**: PARTIAL
- **Statement**: "CPF5003 encountered on CUSTFILE during UPDATEACCOUNT; recovery action incomplete"
- **Confidence**: low (error observed; recovery unknown)
- **Supporting Detail**:
  - Error code: CPF5003
  - Severity: 40
  - Locked resource: CUSTFILE
  - Recovery action: **[LOG ENDS HERE]** (unknown if retry succeeded)
  - Note: "Log truncated; recovery outcome not observed"
- **TBD**: "pending_source: Confirm whether UPDATEACCOUNT retry succeeded or failed"
- **TBD**: "pending_sme_judgment: Is this error expected BAU?"

### RTE-NNN-003: batch_window
**Status**: NOT AVAILABLE
- **Statement**: N/A
- **Confidence**: N/A
- **Supporting Detail**: Log starts at 01:00:02 but ends prematurely; job completion time unknown
- **TBD**: "pending_source: No job end timestamp; log truncated before completion"

### RTE-NNN-004: timing_observation
**Status**: PARTIAL
- **Statement**: "VALIDATECREDIT: ~2 minutes (estimated from log start to CALCFEE call)"
- **Confidence**: low (incomplete; based on inferred timing)
- **Supporting Detail**:
  - Start: 01:00:30 (VALIDATECREDIT called)
  - Next call: 01:02:35 (CALCFEE called)
  - Duration: ~2 minutes (includes processing + communication)
  - Note: "Single run; timing may include I/O latency"
- **TBD**: "pending_source: Log ends before job completion; execution duration unknown"

---

## Mining Strategy for Incomplete Evidence

### Graceful Degradation Rules
1. **Continue mining available sections** — Don't fail on truncation
2. **Mark confidence as low** — Incomplete data cannot be high-confidence
3. **Document what's missing** — Create TBDs for unresolved sections
4. **Preserve partial observations** — Don't suppress; let SME decide on usefulness

### What to Extract
✅ **DO extract**:
- VALIDATECREDIT → CALCFEE → UPDATEACCOUNT sequence (complete through UPDATEACCOUNT start)
- CPF5003 error code and context (logged, though recovery unknown)
- Timing for VALIDATECREDIT (partial estimate)
- Program names and call order

❌ **DO NOT extract**:
- Batch window (no job completion timestamp)
- Error recovery outcome (log ends before recovery logged)
- Total job duration
- Whether error was handled or caused job failure

---

## Expected TBD Items

| TBD ID | Category | Description | Resolution |
|---|---|---|---|
| pending_source | UPDATEACCOUNT completion | Did UPDATEACCOUNT call complete, or was job interrupted by error? | Provide complete job log or confirm job completion status |
| pending_source | batch_window | Job end time unknown; cannot determine batch window or duration | Provide complete job log |
| pending_sme_judgment | error handling | CPF5003 on CUSTFILE—is this expected or exceptional? | SME to confirm if FILE LOCKED is BAU or requires investigation |
| pending_source | recovery outcome | Did retry of UPDATEACCOUNT succeed? | Confirm from separate job logs or JOBLOG with complete recovery section |

---

## Confidence Downgrades

All observations from incomplete logs should be downgraded:

| Observation Type | Normal High Confidence | Incomplete Log Confidence |
|---|---|---|
| call_sequence | 3+ runs, identical | ↓ low: sequence partial, completion unknown |
| error_pattern | 3+ occurrences with consistent recovery | ↓ low: error observed, recovery unknown |
| timing_observation | 3+ runs, ±10% variance | ↓ low: single run, inference-based |
| batch_window | 3+ nights, consistent timing | ❌ not available: no completion timestamp |

---

## Recommendations for SME Review

1. **Verify job completion** — Was job CREDITCHK interrupted or completed? Check JOBQ history or submit a fresh run.
2. **Interpret CPF5003** — Is file lock expected? Does system automatically retry?
3. **Confirm call sequence** — Even partial, does VALIDATE → CALC → UPDATE match your understanding?
4. **Obtain complete evidence** — If possible, provide complete job log or multiple runs of the same job to upgrade confidence.

---

## How This Example Shows Anti-Hallucination

This example demonstrates what NOT to do:

❌ **Incorrect (hallucination)**:
```json
{
  "observation": "UPDATEACCOUNT completed successfully after retry",
  "confidence": "high",
  "note": "This contradicts the log truncation; the log never shows completion"
}
```

✅ **Correct (anti-hallucination)**:
```json
{
  "observation": "CPF5003 error encountered; recovery action and outcome unknown",
  "confidence": "low",
  "note": "Log ends abruptly; cannot determine if retry succeeded or job failed",
  "tbd": "pending_source: Confirm UPDATEACCOUNT completion status"
}
```

---

## Testing Acceptance Criteria

- [ ] All partial observations marked with low confidence
- [ ] No observations claim high confidence
- [ ] All unresolved sections have TBD entries
- [ ] No invented behavior beyond what logs show
- [ ] Extraction continues despite truncation (graceful degradation)
- [ ] Notes explain why each observation is incomplete
