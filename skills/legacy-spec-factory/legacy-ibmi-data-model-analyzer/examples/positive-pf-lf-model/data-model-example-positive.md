# Example: Positive Case - Simple Customer Master Data Model

## Overview

This example demonstrates a straightforward data model analysis for a CUSTOMER master file with one logical file and simple program usage. This is a **positive case** showing complete, evidence-backed analysis without invented facts.

## Scenario

- **Domain**: Customer master file and active customer access
- **Files**:
  - CUSTOMER (PF) - physical file containing customer records
  - CUSTACT (LF) - logical file keyed by CUSTNO and selecting active records
- **Programs**: CUSTINQ (customer inquiry), CUSTMAINT (customer maintenance)
- **Approved Inventory**: Files OBJ-CUSTOMER-001 and OBJ-CUSTOMER-ACTIVE-001 listed in inventory.yaml

## DDS Source

### Physical File (CUSTOMER)

Source: QRPGLESRC(CUSTOMER)

```dds
     A                                      UNIQUE
     A          R CUSTREC
     A            CUSTNO        10A       COLHDG('Customer Number')
     A            CUSTNAME      30A       COLHDG('Customer Name')
     A            ACTIVE_FLAG    1A       COLHDG('Active Flag')
     A            CREATED_DATE   8  0     COLHDG('Created Date - YYYYMMDD')
     A          K CUSTNO
```

**Evidence**: EV-CUSTOMER-001 = extraction of QRPGLESRC(CUSTOMER) source lines 1-7

### Logical File (CUSTACT)

Source: QRPGLESRC(CUSTACT)

```dds
     A          R CUSTACT                  PFILE(CUSTOMER)
     A            CUSTNO
     A            CUSTNAME
     A            ACTIVE_FLAG
     A          K CUSTNO
     A          S ACTIVE_FLAG   *EQ 'Y'
```

**Evidence**: EV-CUSTOMER-002 = extraction of QRPGLESRC(CUSTACT) source lines 1-7

## Data Dictionary Extract

### CUSTOMER (OBJ-CUSTOMER-001)

| Seq | SME-Approved Meaning | DDS Name | Type | Length | Dec | Allow Null | Evidence | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Customer Number | CUSTNO | A | 10 | N/A | N | EV-CUSTOMER-001 | COLHDG says "Customer Number"; uniqueness supported by DDS UNIQUE + K CUSTNO. Numeric-only validation, if required, must come from program evidence or SME. |
| 2 | Customer Name | CUSTNAME | A | 30 | N/A | N | EV-CUSTOMER-001 | COLHDG says "Customer Name"; no further business meaning inferred. |
| 3 | Active Flag | ACTIVE_FLAG | A | 1 | N/A | N | EV-CUSTOMER-001 | Program analysis confirms values `Y` and `N`; other values remain TBD if not checked. |
| 4 | Created Date | CREATED_DATE | S | 8 | 0 | N | EV-CUSTOMER-001 | Date when customer record was created in YYYYMMDD format. |

**Key Fields**:
- Unique keyed access path: CUSTNO (DDS `UNIQUE` + `K CUSTNO`)

**Status**: approved (all fields documented, no ambiguity)

### CUSTACT (OBJ-CUSTOMER-ACTIVE-001)

Logical file; references CUSTOMER file above. Adds selection criterion: ACTIVE_FLAG = 'Y'.

**Status**: approved (derived from documented CUSTOMER file)

## Relationship Map

### CUSTOMER File Keys

| Key Type | Fields | Status | Evidence |
| --- | --- | --- | --- |
| Unique keyed access path | CUSTNO | confirmed_from_code | DDS UNIQUE + K CUSTNO at EV-CUSTOMER-001 |

### No Foreign Keys Identified

The CUSTOMER file is a master file and does not reference other files as foreign keys in DDS. Program analysis may reveal lookups (e.g., validation against a REGION file), but those would be application-level, not schema-level relationships.

**Status**: Complete; no relationship candidates to other files in this domain.

## Access Paths

### CUSTACT (OBJ-CUSTOMER-ACTIVE-001)

| Property | Value | Evidence |
| --- | --- | --- |
| Logical File Name | CUSTACT | EV-CUSTOMER-002 |
| Base File | CUSTOMER | DDS PFILE(CUSTOMER) at EV-CUSTOMER-002 |
| Key Fields | CUSTNO | DDS K CUSTNO at EV-CUSTOMER-002 |
| Selection Criteria | ACTIVE_FLAG = 'Y' | DDS SELECT at EV-CUSTOMER-002 |
| Uniqueness | Unique (inherited from base primary key) | CUSTNO is unique in CUSTOMER |
| Programs Using | OBJ-CUSTINQ-001, OBJ-CUSTMAINT-001 | From approved program analyses |
| Status | Active | Confirmed in current system |

## CRUD / Lifecycle Matrix

### CUSTOMER (OBJ-CUSTOMER-001)

| Program | Operations | Context | Evidence |
| --- | --- | --- | --- |
| OBJ-CUSTINQ-001 | R | Inquiry program reads active customers by CUSTNO via CUSTACT LF. CHAIN operation to retrieve full record. | program-analysis-OBJ-CUSTINQ-001.md, lines 45-52 |
| OBJ-CUSTMAINT-001 | R, U | Maintenance program reads customer by CUSTNO (CHAIN), updates CUSTNAME, ACTIVE_FLAG fields when changes are submitted. | program-analysis-OBJ-CUSTMAINT-001.md, lines 72-91 (READ), 120-145 (UPDATE) |

### Lifecycle

```
CUSTOMER record lifecycle:

1. CREATE: New customer record created in OBJ-CUSTMAINT-001 when new customer is added
   - ACTIVE_FLAG defaults to 'Y'
   - CREATED_DATE set to current system date

2. READ: OBJ-CUSTINQ-001 and OBJ-CUSTMAINT-001 read customer via CUSTACT (active only)
   - Access method: CHAIN by CUSTNO
   - OBJ-CUSTMAINT-001 may also read via CUSTNO directly (PF, not LF) for maintenance

3. UPDATE: OBJ-CUSTMAINT-001 updates CUSTNAME, ACTIVE_FLAG, other fields as needed
   - Occurs after user submits changes on inquiry screen

4. DELETE: Not explicitly programmed; customers are deactivated (ACTIVE_FLAG = 'N') instead
   - No delete operation found in program analysis
   - Inactive customers remain in file for audit trail

5. ARCHIVE/PURGE: Unknown; no retention policy documented in inventory
   - TBD: Confirm whether inactive customers are retained indefinitely or archived after N years
```

### Retention Policy

**Current**: Unknown (TBD-CUSTOMER-001)
- **Evidence**: Inventory does not document retention period
- **Impact**: Cannot plan migration archival strategy without this decision
- **SME Input Required**: Compliance / business owner must confirm retention policy

## Data Quality and Migration Risk

### Observations from Program Analysis

1. **CREATED_DATE Format**: YYYYMMDD (numeric field, length 8, scale 0)
   - Risk: Non-standard date format; most SQL databases use DATE type
   - Mitigation: Conversion logic required during migration
   - Evidence: program-analysis-OBJ-CUSTMAINT-001.md, field format notes

2. **ACTIVE_FLAG Usage**: Consistently 'Y' or 'N' (no other values found in program validation)
   - Confidence: high (based on program validation logic)
   - Evidence: program-analysis-OBJ-CUSTMAINT-001.md, validation block lines 110-115

3. **Customer Name Display Truncation**: Field is 30A but programs display only 20 characters
   - Observation: display truncation belongs in screen/report analysis, not field definition
   - Evidence: SME note; DSPF evidence still pending
   - TBD: provide DSPF evidence before using this in downstream requirements

### Migration Risks

- [ ] CREATED_DATE type mismatch: ZONED vs. SQL DATE
- [ ] ACTIVE_FLAG: downstream target-design decision must preserve or explicitly transform `Y`/`N` behavior
- [ ] Record count: unknown; collect current production count before migration sizing

## Handoff Status

### Completeness Checklist

- [x] All record formats documented (CUSTREC in CUSTOMER)
- [x] All fields documented with DDS references
- [x] Primary key identified and confirmed
- [x] Logical files identified and explained
- [x] Access paths documented
- [x] CRUD operations mapped to programs
- [x] No invented keys or relationships
- [x] Data type mappings clear

### TBDs

- [ ] TBD-CUSTOMER-001: Confirm retention policy for CUSTOMER file
  - **Status**: pending_business_decision (non_blocking by SME waiver for BRD/spec drafting)
  - **Impact**: Archival strategy depends on this decision; target data design must not finalize retention without it
  - **SME Input Required**: Compliance or business owner

### Approval

**Status**: approved_with_non_blocking_tbd

**SME Reviewer**: [Name, Title]
**Review Date**: [YYYY-MM-DD]
**Notes**: All structural elements are documented and accurate. Retention policy TBD is explicitly waived as non-blocking for BRD/spec drafting and remains blocking for final target retention design.

---

**Key Takeaways from This Example**:

1. **Evidence-Backed**: Every field, key, and access path has an EV-* reference to source
2. **No Invention**: Relationship candidates are explicitly absent because DDS contains no foreign keys
3. **Program Traceability**: CRUD operations link directly to approved program analyses with line numbers
4. **TBD Discipline**: Unknown retention policy is explicitly marked TBD with blocking status and SME escalation path
5. **Complete Without Being Perfect**: Data model is approved despite a single open TBD because the TBD is non-blocking

---

Generated by legacy-ibmi-data-model-analyzer v0.1.0
Legacy Spec Factory Copyright 2026 Leo L Zhang
