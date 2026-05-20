# CRUD / Lifecycle Matrix: [DATA-SLUG]

## Overview

This document maps programs and flows to the files they interact with, showing which operations (CREATE, READ, UPDATE, DELETE) are performed, in what sequence, and under what conditions. This matrix is derived from approved program analyses and flow analyses.

## File x Program Cross-Reference

| File (OBJ-ID) | Program | Operation(s) | Conditions | Evidence |
| --- | --- | --- | --- | --- |
| [OBJ-FILE-001] | [OBJ-PGM-001] | C / R / U / D | [e.g., "READ on CHAIN by CUSTNO", "UPDATE after validation"] | [program-analysis-OBJ-PGM-001.md line nn] |
| | [OBJ-PGM-002] | R | "READ via SETLL + READ" | program-analysis-OBJ-PGM-002.md |
| [OBJ-FILE-002] | [OBJ-PGM-001] | C / D | "CREATE new record, DELETE by date range" | program-analysis-OBJ-PGM-001.md |

**Legend**:
- **C** = CREATE (WRITE operation)
- **R** = READ (SETLL, READE, CHAIN, READ operations)
- **U** = UPDATE (UPDATE operation)
- **D** = DELETE (DELETE operation)
- **A** = ARCHIVE (archive/copy-out operation)
- **P** = PURGE (cleanup/removal operation)
- **X** = EXPORT (interface/report/output file operation)

---

## Detailed File Lifecycle: [FILE-NAME] (OBJ-ID)

### Overview

- **Primary Key**: [key fields]
- **Record Count**: [estimated; from inventory or SME]
- **Growth Rate**: [annual growth, if known]
- **Archival Strategy**: [if known; else TBD]

### CREATE Operations

| Program | Sequence | Conditions | Output | Evidence |
| --- | --- | --- | --- | --- |
| [OBJ-PGM] | [order in flow] | [e.g., "when customer is approved"] | [new record with fields ...] | EV-ID / program-analysis line nn |

**TBD**: [TBD-ID if creation logic is unclear or conditional on external input]

### READ Operations

| Program | Access Method | Search Criteria | Expected Result | Evidence |
| --- | --- | --- | --- | --- |
| [OBJ-PGM] | [CHAIN / SETLL+READP / sequential READ] | [e.g., "by CUSTNO", "by REGION"] | [single record / record set] | program-analysis |

### UPDATE Operations

| Program | Trigger | Fields Updated | Validation | Evidence |
| --- | --- | --- | --- | --- |
| [OBJ-PGM] | [e.g., "balance change", "status flag"] | [field names] | [e.g., "amount must be positive"] | program-analysis |

### DELETE Operations

| Program | Trigger | Scope | Safety Checks | Evidence |
| --- | --- | --- | --- | --- |
| [OBJ-PGM] | [e.g., "archival batch job"] | [e.g., "records > 5 years old"] | [e.g., "cascade delete to orders", "audit log"] | program-analysis |

---

## Flow-Level Sequencing

[For each major business flow that uses [FILE-NAME], document the sequence of operations on this file]

### Flow: [FLOW-SLUG]

**Source**: [flow-FLOW-SLUG.md]

```
Step 1: [Program] -> READ [FILE-NAME] by [key]
Step 2: [Program] -> UPDATE [FILE-NAME]
Step 3: [Program] -> CREATE record in [related file]
```

**Expected Outcome**: [summary of data state after flow completion]

---

## Data Lifecycle Diagram (Conceptual)

[Optional: ASCII art or description of data lifecycle]

```
CREATE -> (new record created)
  |
READ -> (record accessed by programs)
  |
UPDATE -> (record modified; may occur multiple times)
  |
DELETE or ARCHIVE -> (record removed or archived based on retention policy)
```

---

## Retention and Archival Policy

**Current Policy** (from inventory or SME notes):

- **Retention Period**: [TBD if unknown]
- **Archival Frequency**: [TBD if unknown]
- **Purge Trigger**: [TBD if unknown]
- **Backup/Recovery**: [e.g., "daily incremental, monthly full"]

**Archival Job(s)**: [if any programs perform archival, list them]

**TBDs**:

- [ ] TBD-SLUG-NNN: Confirm retention policy for [FILE-NAME]
- [ ] TBD-SLUG-NNN: Confirm archival schedule and scope
- [ ] TBD-SLUG-NNN: Confirm purge/delete safety checks and audit requirements

---

## Data Quality and Risk Observations

[From program error handling and SME notes]

### Known Data Quality Issues

- [ ] [Issue]: [Description from program error handling or SME note]. Mitigation: [if known]. Evidence: [program-analysis or SME note]

### Migration Risks

- [ ] **Large file size**: [FILE-NAME] contains [n] million records. Migration strategy: [TBD / plan for batched migration / plan for read-only initial sync]
- [ ] **Complex access patterns**: [FILE-NAME] is accessed via [n] distinct logical files. Risk: [data consistency during migration]. Mitigation: [TBD]
- [ ] **Unusual field formats**: [FILE-NAME] uses [packed decimals, zoned, etc.]. Risk: [type mismatch in target SQL]. Mitigation: [conversion logic required]
- [ ] **Commitment control**: [if applicable] [FILE-NAME] participates in commitment control. Risk: [transaction semantics may differ in target]. Mitigation: [TBD]

---

## Summary Statistics

| Metric | Value | Notes |
| --- | --- | --- |
| Total Files in Data Model | [n] | |
| Files with CREATE Operations | [n] | |
| Files with READ Operations | [n] | |
| Files with UPDATE Operations | [n] | |
| Files with DELETE Operations | [n] | |
| Files with Unknown Lifecycle | [n] | TBD-SLUG-NNN |
| Programs Accessing This File | [n] | |
| Flows Referencing This File | [n] | |

---

Generated by legacy-ibmi-data-model-analyzer v0.1.0
Legacy Spec Factory Copyright 2026 Leo L Zhang
