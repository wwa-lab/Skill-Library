# Output Contract: runtime-evidence.jsonl

## Overview

`runtime-evidence.jsonl` is a line-delimited JSON file containing structured observations extracted from IBM i runtime artifacts (job logs, spool files). Each line is a valid JSON object representing one observation.

**Format**: Line-delimited JSON (JSONL)  
**Consumers**: Program analyzer, flow analyzer, module analyzer, SME review process  
**Status**: All observations initially marked `sme_review_status: draft`

---

## Schema: Observation Object

Each line in `runtime-evidence.jsonl` must conform to this schema:

```json
{
  "observation_id": "RTE-CREDIT-CHECK-001",
  "evidence_id": "EV-CREDIT-CHECK-015",
  "observation_type": "call_sequence",
  "knowledge_type": "observed_behavior",
  "evidence_strength": "observed_in_runtime",
  "statement": "MAIN program calls VALIDATE, then CALC, then UPDATE in sequence",
  "supporting_detail": {
    "source_artifact": "joblog_EV-CREDIT-CHECK-015.txt",
    "source_log_lines": "145-180",
    "extraction_method": "CALL statement parsing",
    "timestamps": ["2026-05-15 22:01:30", "2026-05-15 22:01:45"],
    "call_chain": ["CREDITCHK", "VALIDATECREDIT", "CALCFEE", "UPDATEACCOUNT"]
  },
  "confidence": "high",
  "confidence_justification": "Observed in 5 independent job runs with identical sequence",
  "related_object_ids": ["OBJ-CREDIT-CHECK-001", "OBJ-CREDIT-CHECK-003", "OBJ-CREDIT-CHECK-005"],
  "source_artifact_type": "job_log",
  "source_artifact_name": "EV-CREDIT-CHECK-015",
  "sme_review_status": "draft",
  "reviewed_by": null,
  "review_notes": null,
  "created_date": "2026-05-16T10:30:00Z",
  "created_by": "legacy-ibmi-runtime-evidence-miner",
  "version": "0.1.0"
}
```

---

## Field Definitions

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `observation_id` | string | Unique stable ID: `RTE-<CAPABILITY-SLUG>-NNN` (e.g., `RTE-CREDIT-CHECK-001`). Sequential, never renumbered. |
| `evidence_id` | string | Back-reference to evidence manifest: `EV-<CAPABILITY-SLUG>-NNN`. Links this observation to the source artifact in evidence intake. |
| `observation_type` | string | One of: `call_sequence`, `error_pattern`, `timing_observation`, `batch_window`, `interactive_frequency`, `report_structure`, `lock_contention`, `commit_boundary`. See observation-taxonomy.md. |
| `knowledge_type` | string | Always `"observed_behavior"` for runtime mining (not inferred rule or decision). |
| `evidence_strength` | string | Always `"observed_in_runtime"` (tier 2 evidence per evidence taxonomy). |
| `statement` | string | Human-readable summary (1–2 sentences) of the observation. Must be actionable and traceable. Example: "MAIN calls VALIDATE, then CALC, then UPDATE" |
| `supporting_detail` | object | Raw extraction details (log lines, field values, timestamps). See below. |
| `confidence` | string | One of: `"high"`, `"medium"`, `"low"`. See mining-confidence-rules.md. |
| `related_object_ids` | array | List of OBJ-* IDs (programs, files, tables) involved in this observation. Example: `["OBJ-CREDIT-CHECK-001", "OBJ-CREDIT-CHECK-003"]` |
| `source_artifact_type` | string | One of: `"job_log"`, `"spool_or_report"`, `"transaction_sample"` (phase 2). |
| `source_artifact_name` | string | Name/path of the source artifact. Usually the evidence_id. Example: `"EV-CREDIT-CHECK-015"` |
| `sme_review_status` | string | One of: `"draft"`, `"needs_sme_review"`, `"approved"`, `"rejected"`. Initially `"draft"`. |
| `created_date` | string | ISO 8601 timestamp (UTC) when observation was created. Example: `"2026-05-16T10:30:00Z"` |
| `created_by` | string | Skill name that created this observation. Example: `"legacy-ibmi-runtime-evidence-miner"` |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `confidence_justification` | string | Why this confidence score was assigned. Example: "Observed in 5 independent runs with identical sequence" |
| `reviewed_by` | string | SME name or identifier who reviewed this observation. Null if draft. |
| `review_notes` | string | SME notes on the observation. Null if draft. Example: "Confirmed; this is the standard batch flow." |
| `version` | string | Skill version that created this observation. Example: `"0.1.0"` |

---

## Supporting Detail Schema

The `supporting_detail` object contains raw extraction information. Structure varies by observation type; common fields:

| Field | Type | Description |
|-------|------|-------------|
| `source_artifact` | string | File name or path of the artifact this observation came from. Example: `"joblog_EV-CREDIT-CHECK-015.txt"` |
| `source_log_lines` | string | Line range in the source artifact. Example: `"145-180"` or `"line 145"` |
| `extraction_method` | string | How the observation was extracted. Example: `"CALL statement parsing"`, `"error message regex"` |
| `raw_excerpt` | string | (optional) Short quote from log (10–50 chars, no sensitive data). Example: `"CALL VALIDATECREDIT"` |

**Per observation type**:

- **`call_sequence`**: Include `call_chain` (array of program names), `timestamps` (if available)
- **`error_pattern`**: Include `error_code` (e.g., "CPF2110"), `error_message`, `recovery_action` (if logged)
- **`timing_observation`**: Include `start_time`, `end_time`, `duration_seconds`, `frequency` (if 3+ runs)
- **`batch_window`**: Include `job_name`, `start_time`, `end_time`, `run_count` (number of independent runs)
- **`report_structure`**: Include `report_header_line`, `section_markers`, `footer_line`, `field_positions` (array of {field_name, column_start, column_end})
- **`lock_contention`**: Include `locked_resource` (file/table name), `lock_count`, `retry_count` (if logged)

---

## Validation Rules

### Format Validation
1. Each line must be valid JSON (parseable line-by-line)
2. Required fields must be present in every observation
3. Field values must match their declared types (string, array, object)
4. No circular references or nested observations

### Business Logic Validation
1. `observation_id` must be unique within the file
2. `evidence_id` must exist in the evidence manifest (EV-CREDIT-CHECK-* pattern)
3. `related_object_ids` must exist in inventory (OBJ-* pattern)
4. `confidence` must be justified if "high" (3+ independent runs)
5. `statement` must reference facts, not inferences ("MAIN calls VALIDATE" ✓, "MAIN probably validates" ✗)
6. No unredacted sensitive data in `statement` or `supporting_detail`

### Evidence Minimum
Each observation must satisfy:
1. ✅ Traceable to a specific log line or spool section (via `source_log_lines`)
2. ✅ Confidence score with justification
3. ✅ Back-reference to evidence_id in manifest
4. ✅ No invented behavior (mined, not inferred)
5. ✅ No unredacted customer names, account numbers, personal data

---

## Examples

### Example 1: Call Sequence Observation

```json
{
  "observation_id": "RTE-CREDIT-CHECK-001",
  "evidence_id": "EV-CREDIT-CHECK-015",
  "observation_type": "call_sequence",
  "knowledge_type": "observed_behavior",
  "evidence_strength": "observed_in_runtime",
  "statement": "CREDITCHK main program calls VALIDATECREDIT, then CALCFEE, then UPDATEACCOUNT in sequence",
  "supporting_detail": {
    "source_artifact": "joblog_EV-CREDIT-CHECK-015.txt",
    "source_log_lines": "145-180",
    "extraction_method": "CALL statement parsing from JOBLOG000",
    "call_chain": ["CREDITCHK", "VALIDATECREDIT", "CALCFEE", "UPDATEACCOUNT"],
    "timestamps": ["2026-05-15 22:01:30", "2026-05-15 22:01:45", "2026-05-15 22:01:50", "2026-05-15 22:02:00"]
  },
  "confidence": "high",
  "confidence_justification": "Observed in 5 independent job runs (2026-05-10 through 2026-05-15) with identical sequence",
  "related_object_ids": ["OBJ-CREDIT-CHECK-001", "OBJ-CREDIT-CHECK-003", "OBJ-CREDIT-CHECK-005", "OBJ-CREDIT-CHECK-007"],
  "source_artifact_type": "job_log",
  "source_artifact_name": "EV-CREDIT-CHECK-015",
  "sme_review_status": "draft",
  "reviewed_by": null,
  "review_notes": null,
  "created_date": "2026-05-16T10:30:00Z",
  "created_by": "legacy-ibmi-runtime-evidence-miner",
  "version": "0.1.0"
}
```

### Example 2: Error Pattern Observation

```json
{
  "observation_id": "RTE-CREDIT-CHECK-002",
  "evidence_id": "EV-CREDIT-CHECK-015",
  "observation_type": "error_pattern",
  "knowledge_type": "observed_behavior",
  "evidence_strength": "observed_in_runtime",
  "statement": "FILE LOCKED on CUSTFILE (CPF5003) encountered during UPDATE; retry succeeds within 2 seconds",
  "supporting_detail": {
    "source_artifact": "joblog_EV-CREDIT-CHECK-015.txt",
    "source_log_lines": "185, 197, 209",
    "extraction_method": "Error message regex (CPF5003)",
    "error_code": "CPF5003",
    "error_message": "FILE LOCKED - CUSTFILE",
    "recovery_action": "Automatic retry, waited 2 seconds",
    "occurrence_count": 3
  },
  "confidence": "high",
  "confidence_justification": "Observed in 3 independent runs; consistent pattern: LOCK → 2-second wait → retry succeeds",
  "related_object_ids": ["OBJ-CREDIT-CHECK-007"],
  "source_artifact_type": "job_log",
  "source_artifact_name": "EV-CREDIT-CHECK-015",
  "sme_review_status": "draft",
  "reviewed_by": null,
  "review_notes": null,
  "created_date": "2026-05-16T10:35:00Z",
  "created_by": "legacy-ibmi-runtime-evidence-miner",
  "version": "0.1.0"
}
```

### Example 3: Batch Window Observation

```json
{
  "observation_id": "RTE-CREDIT-CHECK-003",
  "evidence_id": "EV-CREDIT-CHECK-015",
  "observation_type": "batch_window",
  "knowledge_type": "observed_behavior",
  "evidence_strength": "observed_in_runtime",
  "statement": "Batch job BATCHRECON runs nightly: start 01:00 UTC, end 02:30 UTC (90 minutes typical)",
  "supporting_detail": {
    "source_artifact": "joblog_EV-CREDIT-CHECK-015.txt",
    "source_log_lines": "1-50",
    "extraction_method": "JOBLOG000 timestamp parsing (start/end entries)",
    "job_name": "BATCHRECON",
    "runs_observed": [
      {"date": "2026-05-10", "start": "01:02", "end": "02:31", "duration_minutes": 89},
      {"date": "2026-05-11", "start": "01:01", "end": "02:29", "duration_minutes": 88},
      {"date": "2026-05-12", "start": "01:00", "end": "02:32", "duration_minutes": 92},
      {"date": "2026-05-13", "start": "01:03", "end": "02:28", "duration_minutes": 85},
      {"date": "2026-05-15", "start": "01:00", "end": "02:30", "duration_minutes": 90}
    ]
  },
  "confidence": "high",
  "confidence_justification": "Observed in 5 consecutive nightly runs; consistent start window (01:00–01:03) and duration (85–92 minutes)",
  "related_object_ids": ["OBJ-CREDIT-CHECK-001"],
  "source_artifact_type": "job_log",
  "source_artifact_name": "EV-CREDIT-CHECK-015",
  "sme_review_status": "draft",
  "reviewed_by": null,
  "review_notes": null,
  "created_date": "2026-05-16T10:40:00Z",
  "created_by": "legacy-ibmi-runtime-evidence-miner",
  "version": "0.1.0"
}
```

### Example 4: Report Structure Observation

```json
{
  "observation_id": "RTE-CREDIT-CHECK-004",
  "evidence_id": "EV-CREDIT-CHECK-020",
  "observation_type": "report_structure",
  "knowledge_type": "observed_behavior",
  "evidence_strength": "observed_in_runtime",
  "statement": "CREDITRPT report has header (line 1-3), detail sections (lines 4-N), and footer with grand totals (final 5 lines)",
  "supporting_detail": {
    "source_artifact": "spool_EV-CREDIT-CHECK-020.txt",
    "source_log_lines": "1-200",
    "extraction_method": "Spool file structure analysis (headers, sections, footers)",
    "report_header_lines": "1-3",
    "report_footer_lines": "195-200",
    "section_markers": ["Detail Section Start", "Section Total", "Page Break"],
    "field_positions": [
      {"field_name": "CUST_ID", "column_start": 1, "column_end": 8, "data_type": "numeric"},
      {"field_name": "CUST_NAME", "column_start": 10, "column_end": 39, "data_type": "alpha"},
      {"field_name": "AMOUNT", "column_start": 41, "column_end": 50, "data_type": "numeric"},
      {"field_name": "STATUS", "column_start": 52, "column_end": 59, "data_type": "alpha"}
    ],
    "grand_total_line": 198,
    "grand_total_amount_range": "100000.00–500000.00"
  },
  "confidence": "high",
  "confidence_justification": "Same structure observed in 3 independent spool files from different report runs",
  "related_object_ids": ["OBJ-CREDIT-CHECK-015"],
  "source_artifact_type": "spool_or_report",
  "source_artifact_name": "EV-CREDIT-CHECK-020",
  "sme_review_status": "draft",
  "reviewed_by": null,
  "review_notes": null,
  "created_date": "2026-05-16T10:45:00Z",
  "created_by": "legacy-ibmi-runtime-evidence-miner",
  "version": "0.1.0"
}
```

---

## Consuming runtime-evidence.jsonl

### In Program Analyzer

Program analyzer accepts optional `runtime_hints` parameter:

```bash
/legacy-ibmi-program-analyzer \
  --program OBJ-CREDIT-CHECK-001 \
  --inventory 01_inventory/inventory.yaml \
  --runtime_hints runtime-evidence.jsonl
```

Program analyzer reads observations with `related_object_ids` containing this program and uses them to:
- Validate extracted Program Call Map edges against runtime observations
- Upgrade evidence strength to `confirmed_from_code + observed_in_runtime` where confirmed
- Flag dead code (program in source but never seen in logs)
- Document error paths with runtime examples

### In Flow Analyzer

Flow analyzer accepts optional `bau_notes` parameter (derived from runtime observations):

```bash
/legacy-ibmi-flow-analyzer \
  --flow BATCH-RECON \
  --program_analyses 02_programs/*/program-analysis-*.md \
  --bau_notes runtime-evidence.jsonl
```

### In Module Analyzer

Module analyzer uses runtime observations to ground View 1 (Operation Flow):

```yaml
## View 1: Operation Flow / Business Context

### BAU Rhythm (informed by runtime mining)
- Observation ID: RTE-CREDIT-CHECK-003
- Batch window: Every night 01:00–02:30 UTC (observed in 5 runs, high confidence)
- Peak interactive usage: 08:00–17:00 (inferred from DSPLY frequency in logs)
- Error recovery: Manual retry on file lock; 95% success rate
```

---

## JSONL File Format Rules

1. **Line-based**: Each observation is exactly one line; no line breaks within a JSON object
2. **Valid per line**: Each line must be independently valid JSON (parseable separately)
3. **No leading/trailing**: No blank lines, no trailing commas, no array wrapper
4. **UTF-8 encoding**: UTF-8 text, no special line endings

**Valid**:
```jsonl
{"observation_id":"RTE-CREDIT-CHECK-001", ...}
{"observation_id":"RTE-CREDIT-CHECK-002", ...}
```

**Invalid**:
```jsonl
[
  {"observation_id":"RTE-CREDIT-CHECK-001", ...},
  {"observation_id":"RTE-CREDIT-CHECK-002", ...}
]
```

---

## Status Transition Rules

1. Initial status: `sme_review_status: "draft"`
2. After SME review: `"approved"` or `"rejected"`
3. If rejected: SME provides `review_notes` explaining why (e.g., "This observation contradicts the actual flow; see RTE-CREDIT-CHECK-012")
4. Once approved: Observation can be consumed by downstream skills (program/flow/module analyzers)

---

## Versioning

When the skill is updated, increment the version in the `version` field:
- v0.1.0: Initial release
- v0.1.1: Bug fixes, schema unchanged
- v0.2.0: Schema changes (break downstream consumers)

Always update observations' `version` field to match the skill version that created them.
