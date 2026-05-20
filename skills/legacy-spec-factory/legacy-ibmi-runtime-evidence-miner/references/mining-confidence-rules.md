# Mining Confidence Rules

This document defines the scoring rules for assigning `confidence` values (high/medium/low) to observations in `runtime-evidence.jsonl`.

---

## Core Principle

**Never claim high confidence from a single run.** Runtime behavior is inherently variable; multiple independent observations are required to establish a reliable pattern.

---

## Scoring Framework

### High Confidence

**Definition**: The observation is repeatable, consistent, and unambiguous across multiple independent runs.

**Criteria**:
1. **Frequency**: Observed in 3+ independent runs/logs. For repeatable event observations such as `error_pattern` or `lock_contention`, 3+ occurrences in one complete log can support high confidence for that event only; do not use same-log repetition to claim high confidence for `call_sequence`, `timing_observation`, `batch_window`, or `report_structure`.
2. **Consistency**:
   - For deterministic observations (call sequences, report structure): Pattern is 100% identical
   - For timing/frequency observations: Within ±10% variance (e.g., 90–110 seconds out of 100 second average)
3. **Unambiguous extraction**: No interpretation required; pattern is directly visible in log
4. **No contradictory evidence**: Across all observed runs, no contradictory pattern exists

**Justification format**:
```
"Observed in 5 independent job runs (2026-05-10 to 2026-05-15) 
with identical sequence and consistent timing"
```

**Examples**:
- ✅ Call sequence: "MAIN → VALIDATE → CALC" in all 5 runs → **high**
- ✅ Batch window: Start time 01:00–01:03 (±3 min), duration 85–92 min (±3.5%) across 5 runs → **high**
- ✅ Report structure: Identical field positions in 3 different spool files → **high**
- ✅ Single job run showing a complete, unambiguous call sequence → **medium** (not high)
- ❌ Batch window: 1st run 01:00–02:30, 2nd run 01:30–03:30 (high variance) → **medium** (not high)

---

### Medium Confidence

**Definition**: The observation is clear and unambiguous, but based on limited evidence (1–2 runs) or shows some variance.

**Criteria**:
1. **Frequency**: Observed in 1–2 independent runs/logs
2. **Clarity**: Extraction is unambiguous; no interpretation required
3. **Consistency**:
   - For deterministic observations: Identical across available runs
   - For timing observations: Within ±20% variance
4. **No contradictory evidence**: No contradicting pattern observed
5. **Expected behavior**: Aligns with known BAU or documented patterns (from code review or SME notes)

**Justification format**:
```
"Observed in 2 independent runs; pattern is clear and unambiguous. 
Expected BAU for credit processing flow."
```

**Examples**:
- ✅ Call sequence: "MAIN → VALIDATE → CALC" in 2 runs, no variance → **medium**
- ✅ Error pattern: "FILE LOCKED on CUSTFILE; retry succeeds" observed 2 times → **medium**
- ✅ Batch window: 01:00–02:30 (both runs within ±5 min) from 2 runs → **medium**
- ✅ Complete, unambiguous call sequence in a single run → **medium** (clear but limited evidence)
- ❌ Timing observation: Single run showing 150ms execution time → **low** (timing needs multiple runs)
- ❌ Call sequence with variance: "MAIN → VALIDATE → CALC" in run 1, "MAIN → CALC → VALIDATE" in run 2 → **low** (contradictory)

---

### Low Confidence

**Definition**: The observation is based on minimal evidence, requires interpretation, is contradictory, or shows significant variance.

**Criteria** (any one triggers **low**):
1. **Single occurrence**: Observed in only 1 run/log (applies especially to timing observations)
2. **Ambiguous extraction**: Requires interpretation or inference
3. **Variance**: For timing, variance exceeds ±20% (e.g., 100–200 seconds out of 100 second average)
4. **Contradictory evidence**: Other observations suggest different behavior
5. **Exceptional circumstance**: Marked as unusual or error condition in logs
6. **Unidentified elements**: Programs/files in observation not in inventory

**Justification format**:
```
"Single run; timing exhibits high variance due to system load. 
Pending additional evidence to establish baseline."
```

**Examples**:
- ✅ Timing observation: Single 150ms execution time → **low** (need 3+ runs)
- ✅ Batch window: Single run observed; scheduling not yet confirmed → **low** (need pattern across days)
- ✅ Error pattern: Single FILE LOCKED occurrence; unclear if expected or exceptional → **low**
- ✅ Lock contention: 1 lock observed; retry outcome unclear → **low** (need 3+ to claim success)
- ✅ Call sequence: "MAIN → VALIDATE → CALC" observed once, but SME notes suggest sometimes skips VALIDATE → **low** (contradictory)
- ✅ Program in logs not in inventory: Unidentified CALCFEE program → **low** (unverified)

---

## Per-Observation-Type Scoring Guide

### call_sequence

| Evidence | High | Medium | Low |
|----------|------|--------|-----|
| **3+ runs, identical** | ✅ | | |
| **2 runs, identical, expected** | | ✅ | |
| **1 run, clear extraction** | | | ✅ |
| **Multiple runs, some variance** | | | ✅ |
| **Conditional calls (unclear when)** | | | ✅ |

**Justification template**:
- High: "Observed in 5 independent runs with identical sequence: [list programs]"
- Medium: "Observed in 2 runs with identical sequence and expected pattern"
- Low: "Single run observation; pattern requires SME confirmation"

---

### error_pattern

| Evidence | High | Medium | Low |
|----------|------|--------|-----|
| **3+ error occurrences with consistent recovery** | ✅ | | |
| **1–2 error occurrences, clear recovery** | | ✅ | |
| **Single error, unclear recovery** | | | ✅ |
| **Error observed but contradicts code** | | | ✅ |
| **Orphan error (program not in inventory)** | | | ✅ |

**Justification template**:
- High: "Observed in 3 independent runs; FILE LOCKED → 2-second retry → success (100%)"
- Medium: "Observed 2 times; clear recovery path; expected behavior"
- Low: "Single occurrence; recovery path unclear"

---

### timing_observation

| Evidence | High | Medium | Low |
|----------|------|--------|-----|
| **3+ runs, ±10% variance** | ✅ | | |
| **2 runs, ±10% variance** | | ✅ | |
| **2 runs, ±20% variance** | | ✅ | |
| **Single run, any variance** | | | ✅ |
| **3+ runs, >20% variance** | | | ✅ |

**Variance examples**:
- Average 100 seconds, range 90–110 seconds: ±10% ✅ high
- Average 100 seconds, range 80–120 seconds: ±20% ✅ medium
- Average 100 seconds, range 50–150 seconds: ±50% ❌ low

**Justification template**:
- High: "5 runs observed: 150ms, 152ms, 149ms, 151ms, 150ms (±1.3% variance)"
- Medium: "2 runs: 150ms, 165ms (±10% variance); typical batch load"
- Low: "Single run: 150ms; timing highly variable; need more data"

---

### batch_window

| Evidence | High | Medium | Low |
|----------|------|--------|-----|
| **5+ nights with consistent start time (±5min) and duration (±10%)** | ✅ | | |
| **3–4 nights with consistent pattern** | ✅ | | |
| **2 nights with similar pattern, expected** | | ✅ | |
| **Single night observation** | | | ✅ |
| **Dates show high variance in timing** | | | ✅ |

**Justification template**:
- High: "5 consecutive nights: start 01:00–01:03, duration 85–92 minutes; consistent pattern"
- Medium: "2 nights observed: 01:00–02:30 and 01:02–02:28; expected nightly schedule"
- Low: "Single night: 01:00–02:30; confirm if nightly or one-time event"

---

### interactive_frequency

| Evidence | High | Medium | Low |
|----------|------|--------|-----|
| **5+ days of logs with consistent peak hours** | ✅ | | |
| **3 days with consistent peak, expected pattern** | ✅ | | |
| **2 days with similar peak hours** | | ✅ | |
| **Single day of logs** | | | ✅ |
| **Peak hours vary significantly across days** | | | ✅ |

**Justification template**:
- High: "7 days of logs: peak hours consistently 08:00–17:00; 150–200 transactions/hour"
- Medium: "3 days: peak observed 08:30–17:00 with 150 transactions/hour average"
- Low: "Single day snapshot; need more data to establish peak pattern"

---

### report_structure

| Evidence | High | Medium | Low |
|----------|------|--------|-----|
| **3+ spool files with identical structure** | ✅ | | |
| **2 spool files with identical structure, expected** | | ✅ | |
| **1 spool file; structure clear** | | | ✅ |
| **Multiple spool files, structure varies** | | | ✅ |

**Justification template**:
- High: "3 independent CREDITRPT spools show identical structure: header (lines 1–3), detail (4–N), footer (N+1–N+5)"
- Medium: "2 spool files; field positions identical; expected report layout"
- Low: "Single spool file; structure clear but may vary on different input"

---

### lock_contention

| Evidence | High | Medium | Low |
|----------|------|--------|-----|
| **3+ lock occurrences with consistent retry success** | ✅ | | |
| **1–2 lock occurrences with clear recovery** | | ✅ | |
| **Single lock, unclear recovery** | | | ✅ |
| **Lock observed but contradicts program code** | | | ✅ |

**Justification template**:
- High: "CUSTFILE lock observed 3 times in 5 runs; all retries succeeded within 2 seconds"
- Medium: "FILE LOCKED observed 2 times; retry successful both times"
- Low: "Single RECORD LOCKED on ACCTFILE; recovery unclear from logs"

---

### commit_boundary

| Evidence | High | Medium | Low |
|----------|------|--------|-----|
| **Explicit COMMIT statements logged consistently** | ✅ | | |
| **Consistent inferred commit pattern across 3+ runs** | ✅ | | |
| **Inferred commit pattern across 2 runs** | | ✅ | |
| **Single observation of commit/rollback** | | | ✅ |
| **Commit behavior unclear or contradictory** | | | ✅ |

**Justification template**:
- High: "COMMIT logged after every record in 5 runs; consistent pattern"
- Medium: "2 runs show commit after batch completes; expected transaction model"
- Low: "Inferred 1 ROLLBACK from single error recovery; confirm transaction boundaries"

---

## Special Cases

### Case 1: High Variance with Identifiable Cause

**Scenario**: Batch job runtime varies from 60–180 minutes over 5 runs. Later, you discover Run 3 was during month-end close (heavy load).

**Decision**: Score as **medium** (data is variable) rather than high, and note the cause in `confidence_justification`:

```
"5 runs observed: 60–180 min variance. 
4 runs (normal): 85–92 min (±3.5% — high confidence). 
1 run (month-end close): 180 min (exceptional load, low confidence). 
Recommend high confidence for normal BAU, TBD for peak load behavior."
```

### Case 2: Single Run with Very Clear Pattern

**Scenario**: A single job log is comprehensive, 10MB+, with 100+ program calls all consistently sequenced.

**Decision**: Still score as **medium** (single run), not **high**, because a single run could be:
- Atypical due to specific input data
- Affected by one-time system load
- Not representative of normal variation

```
"Very comprehensive single run (10MB log, 100+ calls logged). 
Pattern is unambiguous, but recommend 2–3 additional run samples to upgrade to high confidence."
```

### Case 3: Contradictory Evidence Across Runs

**Scenario**: Run 1 shows call sequence A→B→C, Run 2 shows A→C→B.

**Decision**: Score both as **low** due to contradiction. Create separate RTE observations and flag for SME review:

```
RTE-CREDIT-CHECK-010 (call_sequence):
  statement: "MAIN calls VALIDATE before CALC"
  confidence: "low"
  confidence_justification: "Observed in Run 1; Run 2 shows different sequence. 
     Confirm whether both sequences occur or if one is error condition."
```

---

## When to Mark "Needs SME Review"

Set `sme_review_status: "needs_sme_review"` when:

1. **Contradictory evidence**: Multiple observations conflict (see Case 3 above)
2. **Exceptional circumstance**: Observation seems unusual or error-related
3. **Unresolved ambiguity**: Extraction is clear but business intent is unclear
4. **Pending inventory**: Program/file identified in logs but not yet in inventory (pending_source TBD)
5. **Confidence gap**: Evidence points to low confidence but seems important

Example:
```json
{
  "observation_id": "RTE-CREDIT-CHECK-010",
  "confidence": "low",
  "sme_review_status": "needs_sme_review",
  "review_notes": "Call sequence contradicts between runs. Confirm whether both paths are valid."
}
```

---

## Confidence Score Audit Checklist

Before submitting observations for SME review, audit confidence scores:

- [ ] All high-confidence observations: 3+ evidence sources or runs
- [ ] All medium-confidence observations: 1–2 sources, clear extraction
- [ ] All low-confidence observations: justified (single run, ambiguity, contradictions)
- [ ] Timing observations: Never high-confidence from single run
- [ ] No observations claim high confidence without evidence
- [ ] Contradictions documented, not suppressed
- [ ] Justifications are specific, not generic ("observed multiple times" → "observed in 5 runs on 2026-05-10 through 2026-05-15")

---

## Updating Confidence Scores Post-Review

After SME review:

1. **If SME approves**: No change needed; move to `sme_review_status: "approved"`
2. **If SME requests evidence upgrade**: Add more runs/logs and recalculate confidence
3. **If SME marks invalid**: Mark `sme_review_status: "rejected"` with reason in `review_notes`
4. **If SME challenges confidence**: Adjust score down if necessary and update justification

Do not adjust confidence scores downward on a whim; only when new contradictory evidence emerges.
