# Job Log Parsing Patterns

This document provides guidance for parsing IBM i JOBLOG000 and exported job logs to extract observations.

---

## JOBLOG000 Structure

IBM i job logs are semi-structured text files containing system messages, program output, and diagnostic information.

**Typical structure**:
```
JOBLOG display for job: CREDITCHK User: BATCHPROC Number: 123456
Subsystem: BATCH Job queue: BATCHQ
Start date/time: 05/15/26 01:00:02.123456 Start request ID: QC2FA4AE1234
CPF9898 -- A job is being initiated.

Message ID . . . . . . :   CPF9898
Message type . . . . . :   Completion
Severity . . . . . . . :   00
Date sent . . . . . . :   05/15/2026
Time sent . . . . . . :   01:00:02
From program . . . . . :   QSYSMAIN
From library . . . . . :   QSYS
From module . . . . . :   MAIN

To program . . . . . . :   QSYSMAIN
To library . . . . . . :   QSYS

Message . . . . . :   A job is being initiated.

---

Command issued from QSYS of job BATCHPROC
CALLPRC PRC='CREDITCHK/VALIDATECREDIT' PARM((&CUSTID &AMOUNT))
...

CPF5003 -- Cannot open file.

Message ID . . . . . . :   CPF5003
Message type . . . . . :   Diagnostic
Severity . . . . . . . :   40
Date sent . . . . . . :   05/15/2026
Time sent . . . . . . :   01:02:35
From program . . . . . :   QDBSRV
From library . . . . . :   QSYS
From module . . . . . :   UPDATE

To program . . . . . . :   CREDITUPD
To library . . . . . . :   MYLIB
To module . . . . . . :   MAIN

Message . . . . . :   Cannot open file CUSTFILE.

---

End of job log.
```

---

## Key Sections to Extract

### 1. Job Header
**Pattern**: "JOBLOG display for job:" or "Job name:" at the start

**Regex**: `^JOBLOG.*for job:\s+(\S+).*User:\s+(\S+)`

**Extract**:
- Job name
- User
- Job number
- Start date/time
- Subsystem
- Job queue

**Use for**: Mapping logs to batch jobs; timing observations

---

### 2. Program Calls
**Pattern**: CALL, CALLP, CALLPRC, or CALLSRVPGM statements

**Regex patterns**:
```
CALL\s+([A-Z0-9_]+)
CALLP\s+([A-Z0-9_]+)
CALLPRC\s+PRC='([A-Z0-9_/]+)'
CALLSRVPGM\s+([A-Z0-9_]+)
```

**Extract**:
- Program/procedure name
- Parameters (if logged)
- Timestamp (if available)
- Calling context (which program made the call)

**Use for**: call_sequence observations; validation of Program Call Map edges

**Example parsing**:
```
Input line: "CALLPRC PRC='CREDITCHK/VALIDATECREDIT' PARM((&CUSTID &AMOUNT))"
Extract: program='VALIDATECREDIT', library='CREDITCHK'
Timestamp: (from surrounding lines) 01:02:30
```

---

### 3. Error Messages
**Pattern**: Message ID lines (CPF*, MCH*, SQL*, etc.) followed by message details

**Regex**: `^[A-Z]{3}\d{4}\s+--\s+(.+)$`

**Key error codes to watch**:
- **CPF5003**: Cannot open file (FILE LOCKED)
- **CPF5004**: Cannot open file (RECORD LOCKED)
- **CPF2110**: Record locked by another job
- **MCH3401**: Pointer value is not valid
- **SQL0911**: Lock timeout
- **CPI1234**: Commitment control conflict

**Extract**:
- Error code (CPF5003, etc.)
- Severity (00–99, higher is worse)
- Message text
- From program/module
- To program/module
- Recovery action (if logged)

**Use for**: error_pattern observations; exception handling documentation

**Example**:
```
CPF5003 -- Cannot open file.
Severity: 40
From program: QDBSRV (module UPDATE)
To program: CREDITUPD (module MAIN)
Message: Cannot open file CUSTFILE.

→ Extract: {
    error_code: "CPF5003",
    severity: 40,
    message: "Cannot open file CUSTFILE",
    locked_resource: "CUSTFILE"
  }
```

---

### 4. Timestamps
**Pattern**: "Date sent" and "Time sent" fields, or ISO 8601 timestamps

**Regex patterns**:
```
Date sent.*:\s+(\d{2}/\d{2}/\d{4})
Time sent.*:\s+(\d{2}:\d{2}:\d{2})
(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)
```

**Extract**:
- Start time (job initiated)
- End time (job completed)
- Per-step timing (if available)

**Use for**: timing_observation and batch_window observations; execution duration calculation

**Example**:
```
Job start: 2026-05-15 01:00:02
First CALL: 2026-05-15 01:00:30
Second CALL: 2026-05-15 01:02:35
Job end: 2026-05-15 02:30:15

→ Calculate:
  Total duration: 1h 30m 13s
  Setup time: 28s
  VALIDATE step: 2m 5s
  ...
```

---

### 5. Retry/Recovery Actions
**Pattern**: Retry messages, ROLLBACK, COMMIT, or recovery-related output

**Regex patterns**:
```
RETRY\s+(\d+)
ROLLBACK
COMMIT
Recovery action:
Retry successful
```

**Extract**:
- Recovery action taken
- Number of retries (if available)
- Success/failure indicator

**Use for**: error_pattern observations; recovery path documentation

**Example**:
```
CPF5003 -- Cannot open file.
...
Recovery action: RETRY after 2 seconds
Retry successful.

→ Extract: {
    error_code: "CPF5003",
    recovery_action: "RETRY after 2 seconds",
    retry_successful: true
  }
```

---

## Parsing Strategy

### Line-by-Line Processing
Process the job log line-by-line, maintaining a state machine:

1. **State**: `header` | `message_detail` | `command` | `eof`
2. **Transition on key patterns**:
   - Match "JOBLOG display" → Enter `header` state
   - Match message ID (CPF*, MCH*) → Enter `message_detail` state
   - Match CALL/CALLP → Enter `command` state
   - Match "End of job log" → Enter `eof` state

### Handling Incomplete or Corrupted Logs

If a job log is truncated or corrupted:

1. **Continue parsing available data** — Don't fail; extract what's readable
2. **Mark confidence as low** — Note that data is incomplete
3. **Flag gaps** — Document which sections were skipped
4. **Create TBDs** — For observations that depend on missing data

**Example**:
```
Log ends at line 5000 (abruptly, during CALC execution)
Observations extracted: call_sequence (partial), timing_observation (incomplete)
Confidence: low
TBD: Confirm whether CALC completed or was interrupted
```

---

## Common Patterns

### Call Sequence Extraction

**Input log**:
```
CALLPRC PRC='CREDITCHK/VALIDATECREDIT'
...
Message completed successfully.

CALLPRC PRC='CREDITCHK/CALCFEE'
...
Message completed successfully.

CALLPRC PRC='CREDITCHK/UPDATEACCOUNT'
...
Message completed successfully.
```

**Output observation**:
```json
{
  "observation_type": "call_sequence",
  "call_chain": ["VALIDATECREDIT", "CALCFEE", "UPDATEACCOUNT"],
  "confidence": "high"
}
```

---

### Conditional Call Detection

If a call only appears in some runs:

**Log A**:
```
CALLPRC PRC='CREDITCHK/VALIDATECREDIT'
CALLPRC PRC='CREDITCHK/CALCFEE'
CALLPRC PRC='CREDITCHK/UPDATEACCOUNT'
```

**Log B**:
```
CALLPRC PRC='CREDITCHK/VALIDATECREDIT'
CPF2110 -- Record locked
(RETRY)
CALLPRC PRC='CREDITCHK/CALCFEE'
CALLPRC PRC='CREDITCHK/UPDATEACCOUNT'
```

**Output**:
```json
{
  "observation_type": "call_sequence",
  "call_chain": ["VALIDATECREDIT", "CALCFEE", "UPDATEACCOUNT"],
  "conditional_calls": [
    {
      "call": "RETRY",
      "when": "Record locked (CPF2110) during VALIDATECREDIT"
    }
  ]
}
```

---

### Error Recovery Patterns

**Input log**:
```
01:02:35 CALLPRC PRC='CREDITCHK/UPDATEACCOUNT'
01:02:36 CPF5003 -- Cannot open file CUSTFILE
01:02:36 Recovery action: RETRY after 2 seconds
01:02:38 CALLPRC PRC='CREDITCHK/UPDATEACCOUNT' (RETRY)
01:02:39 Message completed successfully.
```

**Output**:
```json
{
  "observation_type": "error_pattern",
  "error_code": "CPF5003",
  "locked_resource": "CUSTFILE",
  "recovery_action": "RETRY after 2 seconds",
  "retry_successful": true,
  "supporting_detail": {
    "timestamps": ["01:02:36", "01:02:38", "01:02:39"],
    "duration_seconds": 3
  }
}
```

---

### Batch Window Extraction

**Multiple logs** (5 nights):
```
Log 1: Start 01:00:02, End 02:31:45 → 91m 43s
Log 2: Start 01:01:15, End 02:30:22 → 89m 7s
Log 3: Start 01:00:45, End 02:32:10 → 91m 25s
Log 4: Start 01:02:30, End 02:29:55 → 87m 25s
Log 5: Start 01:00:15, End 02:30:40 → 90m 25s
```

**Aggregate observation**:
```json
{
  "observation_type": "batch_window",
  "job_name": "BATCHRECON",
  "start_time_range": "01:00–01:03",
  "duration_minutes": 89,
  "duration_variance": "±3%",
  "runs_observed": 5,
  "confidence": "high"
}
```

---

## Anti-Hallucination Rules for Job Logs

1. **Never invent call sequences** — Extract only CALL/CALLP statements logged
2. **Never infer error recovery** — Document only logged recovery actions
3. **Never extrapolate timing** — Use only explicit timestamps; don't guess
4. **Do not quote unredacted data** — If log contains customer names or amounts, redact or record ranges only
5. **Do not create dead code findings** — If a call is missing from logs, mark as TBD, don't assume dead code

---

## Integration with Inventory

After extracting observations, map programs/files to OBJ-* IDs:

**Example**:
```
Extracted: CALLPRC PRC='CREDITCHK/VALIDATECREDIT'
Inventory lookup: OBJ-CREDIT-CHECK-003 (VALIDATECREDIT)

Output: related_object_ids: ["OBJ-CREDIT-CHECK-001", "OBJ-CREDIT-CHECK-003"]
```

**If not found in inventory**:
```
Extracted: CALLPRC PRC='CREDITCHK/UNKNOWN_MODULE'
Inventory lookup: NOT FOUND

Output: TBD = "pending_source: UNKNOWN_MODULE appears in logs but not in inventory; expand scope or investigate"
```

---

## Tools and Utilities

### Recommended Log Analysis Approach
1. **Text editor with regex search** (VS Code, grep) for quick pattern matching
2. **Python script** (provided in examples/) for systematic extraction
3. **jq or similar JSON tools** for assembling JSONL output

### Sample Python Snippet
```python
import re
from datetime import datetime

def extract_calls(joblog_text):
    calls = []
    for match in re.finditer(r"CALLP?RC\s+PRC='([A-Z0-9_/]+)'", joblog_text):
        calls.append(match.group(1))
    return calls

def extract_errors(joblog_text):
    errors = []
    for match in re.finditer(r"^([A-Z]{3}\d{4})\s+--\s+(.+)$", joblog_text, re.MULTILINE):
        errors.append({"code": match.group(1), "message": match.group(2)})
    return errors
```

---

## Examples in This Skill

See the `examples/` directory for complete worked examples:
- `examples/batch-job-positive/input-joblog.txt` — Real (anonymized) job log excerpt
- `examples/incomplete-logs-negative/input-joblog.txt` — Truncated log for graceful degradation testing
