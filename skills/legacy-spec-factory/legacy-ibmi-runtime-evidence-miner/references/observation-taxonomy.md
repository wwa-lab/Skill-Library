# Observation Taxonomy

This document defines the types of observations that can be extracted from IBM i runtime evidence.

---

## Observation Types

### 1. call_sequence

**Purpose**: Document the sequence of program calls extracted from job logs.

**When to use**: Any time CALL, CALLP, or CALLPRC statements are logged by the system.

**Key fields in supporting_detail**:
- `call_chain` (array): List of program names in call order
- `timestamps` (array): Execution timestamps if logged
- `conditional_calls` (array, optional): Calls that only occur in specific paths

**Confidence scoring**:
- **High**: Identical sequence in 3+ independent runs
- **Medium**: Sequence in 1–2 runs; unambiguous
- **Low**: Partial, truncated, contradictory, or ambiguous call sequences (e.g., CALL not logged clearly)

**Example statement**:
"CREDITCHK main program calls VALIDATECREDIT, then CALCFEE, then UPDATEACCOUNT in sequence"

**Downstream consumption**:
- Program analyzer validates extracted Program Call Map edges against runtime observations
- Marks call edges as `confirmed_from_code + observed_in_runtime` where validated
- Flags dead code (call in source but never observed in logs)

---

### 2. error_pattern

**Purpose**: Document error messages and recovery paths observed in job logs.

**When to use**: Any time error codes (MCH*, CPF*, SQL errors, etc.) appear in logs.

**Key fields in supporting_detail**:
- `error_code` (string): System error code (e.g., "CPF2110", "MCH3401")
- `error_message` (string): Human-readable error text
- `recovery_action` (string, optional): Action taken after error (RETRY, ROLLBACK, CLOSE, etc.)
- `occurrence_count` (integer): How many times this error was seen

**Confidence scoring**:
- **High**: Same error observed 3+ times with consistent recovery path
- **Medium**: Error observed 1–2 times with clear recovery
- **Low**: Single error instance; unclear recovery path

**Example statement**:
"FILE LOCKED on CUSTFILE (CPF5003) encountered during UPDATE; retry succeeds within 2 seconds"

**Downstream consumption**:
- Program analyzer documents error handling code paths
- Flow analyzer uses to substantiate exception handling
- Module analyzer feeds into error recovery documentation

---

### 3. timing_observation

**Purpose**: Document execution duration, frequency, and performance characteristics.

**When to use**: When job logs include timestamps or DSPLY messages.

**Key fields in supporting_detail**:
- `start_time` (string): ISO 8601 start timestamp
- `end_time` (string): ISO 8601 end timestamp
- `duration_seconds` (integer): Elapsed time
- `frequency` (string, optional): How often this occurs ("nightly", "per-transaction", etc.)

**Confidence scoring**:
- **High**: 3+ runs with consistent timing (+/- 10%)
- **Medium**: 2 runs with similar timing
- **Low**: Single run; timing is variable

**Important rule**: Never claim high confidence from a single run. Timing is inherently variable.

**Example statement**:
"VALIDATECREDIT subroutine executes in 150–200 milliseconds during typical batch runs"

**Downstream consumption**:
- Flow analyzer uses to estimate trigger frequency
- Module analyzer documents operational SLAs
- Used for performance baselines

---

### 4. batch_window

**Purpose**: Document when batch jobs run and how long they take.

**When to use**: When mining job logs for JOBQ execution.

**Key fields in supporting_detail**:
- `job_name` (string): Submitted job name
- `job_queue` (string): Job queue
- `runs_observed` (array): List of {date, start, end, duration_minutes}

**Confidence scoring**:
- **High**: 3+ runs with consistent start time (within 5 minutes) and duration (within 10%)
- **Medium**: 2 runs with similar pattern
- **Low**: Single run

**Example statement**:
"Batch job BATCHRECON runs nightly: start 01:00 UTC, end 02:30 UTC (90 minutes typical)"

**Downstream consumption**:
- Flow analyzer documents trigger frequency
- Module analyzer grounds BAU rhythm in observed data
- Used for operational scheduling

---

### 5. interactive_frequency

**Purpose**: Document when interactive transactions run and how often.

**When to use**: When mining job logs for DSPLY (display) or EXFMT (execute format) statements.

**Key fields in supporting_detail**:
- `peak_hours` (array): Hours when interactive activity is highest (e.g., [8, 9, 10, ...17])
- `typical_transaction_count` (integer): How many transactions per hour during peak
- `example_interaction` (string, optional): Type of interaction (e.g., "customer lookup", "order entry")

**Confidence scoring**:
- **High**: 5+ days of logs with consistent peak hours
- **Medium**: 2–3 days of logs with similar pattern
- **Low**: Single day; pattern unclear

**Example statement**:
"Interactive credit lookups peak during 08:00–17:00; average 150 lookups/hour"

**Downstream consumption**:
- Flow analyzer documents interactive trigger model
- Module analyzer for View 1 operational context
- Used for user load planning

---

### 6. report_structure

**Purpose**: Document the structure of spool files / printer output.

**When to use**: When mining PRTF output (spool files).

**Key fields in supporting_detail**:
- `report_header_lines` (string): Line range (e.g., "1-3")
- `report_footer_lines` (string): Line range (e.g., "195-200")
- `section_markers` (array): Text strings that mark section boundaries
- `field_positions` (array): [{field_name, column_start, column_end, data_type}, ...]
- `grand_total_line` (integer): Line number with grand total

**Confidence scoring**:
- **High**: Same structure in 3+ independent spool files
- **Medium**: Same structure in 2 independent spool files
- **Low**: Single spool file, missing sections, or structure varies across runs

**Example statement**:
"CREDITRPT report has header (lines 1–3), detail sections (lines 4–N), and footer with grand totals (lines 195–200)"

**Downstream consumption**:
- Program analyzer documents report generation logic
- Screen-report analyzer for output structure validation
- Used for migration planning (old report vs. new UI)

---

### 7. lock_contention

**Purpose**: Document FILE LOCKED or RECORD LOCKED patterns.

**When to use**: When mining job logs for lock-related error codes (CPF5003, CPF5004, etc.).

**Key fields in supporting_detail**:
- `locked_resource` (string): File or record name that was locked
- `lock_count` (integer): How many times locked in the observed period
- `retry_count` (integer, optional): How many retries succeeded
- `typical_wait_time` (string, optional): E.g., "2 seconds"

**Confidence scoring**:
- **High**: 3+ runs show consistent lock pattern; reliable retry success
- **Medium**: Locks observed 1–2 times with known recovery
- **Low**: Single lock instance; unclear if expected or exceptional

**Example statement**:
"CUSTFILE lock contention observed 3 times during BATCHRECON; retry succeeds within 2 seconds (100% success)"

**Downstream consumption**:
- Program analyzer documents locking and retry logic
- Flow analyzer for error recovery documentation
- Module analyzer for concurrency understanding

---

### 8. commit_boundary

**Purpose**: Document explicit or inferred commit boundaries (transaction control points).

**When to use**: When job logs show COMMIT or ROLLBACK statements, or when inferred from error recovery patterns.

**Key fields in supporting_detail**:
- `commit_type` (string): "explicit" (COMMIT statement logged) or "inferred" (from recovery pattern)
- `commit_frequency` (string): E.g., "after each record", "after batch completes"
- `rollback_observed` (boolean): Was ROLLBACK ever invoked?
- `recovery_example` (string, optional): Quote from log showing recovery

**Confidence scoring**:
- **High**: Explicit COMMIT statements logged
- **Medium**: Consistent inferred commit pattern (e.g., batch always completes or rolls back)
- **Low**: Inferred from single error recovery

**Example statement**:
"UPDATEACCOUNT program commits after each record update; observed in 5 runs with consistent pattern"

**Downstream consumption**:
- Program analyzer documents transaction control logic
- Flow analyzer for data consistency understanding
- Module analyzer for operational SLAs

---

## Observation Type Reference Matrix

| Type | Source | Confidence Threshold | Rarity (High=Rare) | Actionability |
|------|--------|----------------------|-------------------|---------------|
| `call_sequence` | JOBLOG | 3+ runs | Low | High — feeds Program Call Map validation |
| `error_pattern` | JOBLOG | 3+ occurrences | Medium | High — documents exception handling |
| `timing_observation` | JOBLOG timestamps | 3+ runs | Low | High — for SLA & performance baseline |
| `batch_window` | JOBLOG | 3+ runs | Low | High — operational scheduling |
| `interactive_frequency` | JOBLOG DSPLY | 5+ days | Medium | Medium — for user load planning |
| `report_structure` | SPOOL | 3+ files | Low | High — for output validation |
| `lock_contention` | JOBLOG CPF53* | 3+ runs | High | Medium — for concurrency issues |
| `commit_boundary` | JOBLOG COMMIT/ROLLBACK | Explicit or 3+ inferred | High | Medium — for transaction understanding |

---

## When Observation Type Is Unclear

If an observation doesn't fit neatly into one type:

1. **Use the primary type** — Choose the most dominant observation type
2. **Document cross-type dependencies** in `supporting_detail` — E.g., if a call_sequence is conditional on an error, note both
3. **Create separate observations** — Break complex observations into simpler ones (e.g., "CALC called after VALIDATE" + "VALIDATE only called if error from LOOKUP")
4. **If still uncertain** — Mark `sme_review_status: needs_sme_review` and let SME clarify intent

---

## Confidence Scoring Rules (Detailed)

### High Confidence
- Observation repeated in 3+ independent runs/logs
- Pattern consistent within ±10% (for timing) or identical (for structure/calls)
- No contradictory evidence
- Unambiguous extraction (not dependent on interpretation)

### Medium Confidence
- Observation in 1–2 runs/logs
- Clear extraction; unambiguous
- No contradictory evidence
- Expected BAU or known issue

### Low Confidence
- Single run/occurrence
- Requires interpretation (e.g., "probably locked" vs. "locked")
- Contradictory evidence exists
- Rare/exceptional circumstance
- Timing varies significantly (±20% or more)

---

## Contradictory Evidence Handling

When multiple observations contradict:

1. **Document separately** — Create two RTE observations, one per contradiction
2. **Mark both as TBD** — Add note for SME review: "RTE-CREDIT-CHECK-007 observes call sequence A→B→C, but RTE-CREDIT-CHECK-012 observes A→C→B. Confirm which is correct or if both occur in different circumstances."
3. **Never suppress** — Do not delete the minority observation; SME must decide

---

## Reserved Observation Types (Future)

The following are reserved for Phase 2 mining extensions:

- `transaction_sample` — Mined from CSV or fixed-width transaction samples
- `field_value_range` — Mined from DB extracts or sample data
- `special_code_inventory` — Status codes, indicator values from transaction samples

Do not create observations of these types in v0.1.0.
