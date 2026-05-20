# Mining Notes: Batch Job Positive Example

## Overview

This example demonstrates successful mining from a typical IBM i batch job log and spool file. The mining extracts call sequences, error patterns, timing observations, and report structure.

## Input Artifacts

### Job Log: input-joblog.txt
- **Evidence ID**: EV-CREDIT-CHECK-015
- **Size**: ~2KB (typical for single batch run)
- **Source**: BATCHRECON job, 05/15/2026 01:00–02:30
- **Content**: CALL statements, CPF5003 error, recovery action, timing

### Spool File: input-spool.txt
- **Evidence ID**: EV-CREDIT-CHECK-020
- **Source**: CREDITRPT printer output, same batch run
- **Content**: Report header, 3 detail rows, footer with totals

---

## Extraction Process (9-Step Workflow)

### Step 1: Verify Evidence Manifest & Readiness
✅ **PASS**
- Both artifacts listed in manifest with proper sensitivity (public in this example)
- Evidence IDs assigned: EV-CREDIT-CHECK-015 (joblog), EV-CREDIT-CHECK-020 (spool)
- Manifest state: approved_for_inventory
- No unredacted sensitive data (customer IDs and amounts are generic)

### Step 2: Map Runtime Artifacts to Inventory
✅ **PASS**
- Job log references programs: CREDITCHK (main), VALIDATECREDIT, CALCFEE, UPDATEACCOUNT
- Mapped to inventory:
  - OBJ-CREDIT-CHECK-001: CREDITCHK (main)
  - OBJ-CREDIT-CHECK-003: VALIDATECREDIT
  - OBJ-CREDIT-CHECK-005: CALCFEE
  - OBJ-CREDIT-CHECK-007: UPDATEACCOUNT
- Spool file maps to:
  - OBJ-CREDIT-CHECK-015: CREDITRPT (printer file)

### Step 3: Extract Call Sequences from Job Logs
✅ **PASS**
- Regex pattern matched CALL statements:
  - Line 32: `CALL VALIDATECREDIT` (01:00:30)
  - Line 48: `CALL CALCFEE` (01:02:35)
  - Line 58: `CALL UPDATEACCOUNT` (01:02:40, with retry at 01:02:43)
- Extracted sequence: VALIDATECREDIT → CALCFEE → UPDATEACCOUNT
- Timestamps extracted: 01:00:30 → 01:02:35 → 01:02:40
- **Observation RTE-CREDIT-CHECK-001** created with medium confidence (complete and unambiguous, but one run)

### Step 4: Extract Error Patterns from Job Logs
✅ **PASS**
- CPF5003 pattern matched at line 67: "Cannot open file CUSTFILE"
- Error code: CPF5003
- Severity: 40 (diagnostic)
- Context: During UPDATEACCOUNT call
- Recovery: Line 87 "RETRY after 2 seconds"
- Outcome: Line 93 "UPDATEACCOUNT completed successfully"
- **Observation RTE-CREDIT-CHECK-002** created with medium confidence (clear recovery, but one occurrence)

### Step 5: Extract Timing & Rhythm Observations
✅ **PASS**
- Job start: 05/15/2026 01:00:02 (line 3)
- Job end: 05/15/2026 02:30:15 (line 105)
- Duration: 1h 30m 13s (stated in log at line 103)
- Call timings:
  - VALIDATECREDIT: 01:00:30 (start)
  - CALCFEE: 01:02:35 (start)
  - UPDATEACCOUNT: 01:02:40 (start), 01:02:43 (retry)
- **Observation RTE-CREDIT-CHECK-003** created with low confidence for the one observed batch window
- **Observation RTE-CREDIT-CHECK-005** created with low confidence for the observed interval between VALIDATECREDIT and the next logged call

### Step 6: Extract Structure from Spool Files
✅ **PASS**
- Report header: Lines 1–3 (title, date)
- Column header: Lines 6–7
- Data rows: Lines 8–10 (3 rows)
- Field positions calculated from separator line (line 7):
  - Cust ID: columns 1–8
  - Name: columns 10–14
  - Type: columns 16–19
  - Status: columns 21–25
  - Amount: columns 27–35
- Footer: Line 12 (Page Total), Line 14 (Grand Total), Line 15 (Date/Time)
- **Observation RTE-CREDIT-CHECK-004** created with low confidence (clear structure from one spool file)

### Step 7: Correlate Multiple Runs
✅ **PASS**
- Single run available; confidence stays below high for all observations
- Call sequence is clear, but repeatability is not yet proven
- Error pattern is documented (CPF5003 with recovery in this run)
- All observations align with expected BAU behavior

### Step 8: Generate runtime-evidence.jsonl
✅ **PASS**
- 5 JSON objects created (one per observation)
- Each line is valid JSON
- All required fields present
- observation_id format: RTE-CREDIT-CHECK-NNN
- evidence_id back-references: EV-CREDIT-CHECK-015 and EV-CREDIT-CHECK-020
- confidence values assigned per evidence volume (no high-confidence claims from one run)
- supporting_detail includes source line numbers, extracted values, timestamps

### Step 9: Prepare for SME Review
✅ **PASS**
- All observations marked `sme_review_status: "draft"`
- High-value observations highlighted:
  - Call sequence validates expected flow
  - Error handling (CPF5003 retry) is documented
  - Timing shows batch completes in 90+ minutes
  - Report structure extractable from the supplied spool sample
- No contradictions identified
- No unidentified programs/files in logs
- Ready for SME review and sign-off

---

## Output Artifacts

### runtime-evidence.jsonl
Located: [This directory]
Contains: 5 observations
- RTE-CREDIT-CHECK-001: call_sequence (medium confidence - complete single run)
- RTE-CREDIT-CHECK-002: error_pattern (medium confidence - one occurrence with recovery)
- RTE-CREDIT-CHECK-003: batch_window (low confidence - single run)
- RTE-CREDIT-CHECK-004: report_structure (low confidence - one spool file)
- RTE-CREDIT-CHECK-005: timing_observation (low confidence - single run)

### mining-checklist.md (filled)
Located: review-notes.md (example SME response)
Status: Ready for SME review

---

## Key Insights from This Mining Run

1. **Call sequence is clear** — The supplied log shows MAIN → VALIDATE → CALC → UPDATE
2. **Error handling is visible** — FILE LOCKED triggers a logged 2-second retry, which succeeds in this run
3. **Batch window is observed once** — The supplied log runs from 01:00 to 02:30; SME or more logs must confirm the normal schedule
4. **Report structure is extractable** — Field positions and totals are visible in the supplied spool sample
5. **Performance remains a draft observation** — One run is not enough to establish variance

---

## Confidence Assessment

| Observation | Confidence | Runs/Occurrences | Justification |
|---|---|---|---|
| call_sequence | medium | 1 complete run | Pattern is explicit in logs; repeatability still needs more runs |
| error_pattern | medium | 1 occurrence with recovery | Error code, recovery, and success are all logged once |
| batch_window | low | 1 run | Single night observed; cannot claim normal schedule without more runs or SME confirmation |
| report_structure | low | 1 report | Field positions and layout are clear, but only one spool file is supplied |
| timing_observation | low | 1 run | Timing data present but variance is unknown |

---

## Recommendations for SME Review

1. **Confirm call sequence** — Does VALIDATE → CALC → UPDATE match your understanding?
2. **Confirm error handling** — Is CPF5003 + 2-second retry the expected BAU?
3. **Confirm batch timing** — Does nightly 01:00–02:30 window match your operational schedule?
4. **Confirm report structure** — Do field positions match documentation?

If SME confirms all, observations are ready for downstream consumption (program/flow/module analyzers).
