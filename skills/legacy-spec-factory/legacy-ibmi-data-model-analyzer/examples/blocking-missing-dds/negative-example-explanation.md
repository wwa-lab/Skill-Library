# Example: Blocking Case - Missing DDS and Invented Facts

## Overview

This example demonstrates a **negative case** where a data model analysis becomes blocked because of missing source evidence and attempted invention of facts. This serves as a teaching example for what NOT to do and what signals should trigger a stop condition.

## Scenario

- **Domain**: Order management with incomplete inventory
- **Files**:
  - ORDER (PF) - exists in system but DDS source is missing
  - ORDITEM (PF) - referenced by programs but not in inventory
- **Programs**: ORDENTRY (order entry), ORDSHIP (shipping), ORDCAN (order cancellation)
- **Problem**: Inventory lists OBJ-ORDER-001 but DDS cannot be located; program analysis references OBJ-ORDITEM-001 which is not in inventory at all

## What Went Wrong

### Missing DDS Source

**Stop Condition #1**: DDS source for ORDER file cannot be located.

- **Evidence Sought**: QRPGLESRC(ORDER) or equivalent source library member
- **Attempt**: Searched QSYS.QRPGLESRC, QGPL, and documented source libraries
- **Result**: File QRPGLESRC(ORDER) does not exist; likely deleted or renamed
- **Fallback Option**: DSPFFD output exists from 2023-01-15
- **Problem**: DSPFFD output is incomplete; column comments are missing, constraints are not shown

**Correct Action**: Create blocking TBD instead of proceeding

```
TBD-ORDER-SYSTEM-001: Locate original DDS source for ORDER file
- Status: pending_source (blocking)
- Evidence: DDS source QRPGLESRC(ORDER) not found
- Fallback: DSPFFD from 2023-01-15 available but incomplete
- Action Required: Locate source library or recreate DDS from DB2 catalog
- SME Input: Is DDS archived? Has file been migrated to SQL without DDS preservation?
```

### Attempted Invention: Key Field Guessing

**Problem**: With DDS unavailable, analyzer sees DSPFFD output and program analysis showing:
- Program ORDENTRY reads ORDER by "order number"
- Program field is named ORDERNO

**Incorrect Action**: Assume ORDERNO is the primary key and invent:

```
PRIMARY KEY: ORDERNO
Evidence: "Inferred from program usage in ORDENTRY"
```

**Why This Is Wrong**:
1. Field name alone is not sufficient evidence of key status
2. Program might read by ORDERNO but that doesn't mean it's the primary key
3. Could be a candidate key (unique alternate identifier), a foreign key to another file, or just a frequently-accessed field
4. Compound keys are invisible from program name guessing

**Correct Action**: Mark as TBD candidate, not fact

```
TBD-ORDER-SYSTEM-002: Confirm primary key for ORDER file
- Status: pending_source (blocking)
- Observed: Programs read ORDER by ORDERNO field
- Evidence: program-analysis-OBJ-ORDENTRY-001.md, CHAIN by ORDERNO (line 78)
- Assumption: ORDERNO might be primary key, but cannot confirm without DDS or DB2 constraints
- Candidate Structure (unconfirmed):
  - Option A: PRIMARY KEY (ORDERNO)
  - Option B: PRIMARY KEY (ORDERNO, ORDLINE) - compound key
  - Option C: PRIMARY KEY (ORDNO, ORDVER) - versioned orders
- SME Input: Which is correct? Provide DDS or constraint definition.
```

### Attempted Invention: Relationship Guessing

**Problem**: Analyzer sees:
- File ORDER has field CUSTNO
- File CUSTOMER exists in inventory (OBJ-CUSTOMER-001)
- CUSTOMER has field CUSTNO
- Program analysis shows no explicit joins

**Incorrect Action**: Invent a foreign key relationship

```
FOREIGN KEY: ORDER.CUSTNO -> CUSTOMER.CUSTNO
Evidence: "Inferred from naming convention"
Confidence: Medium (based on matching field names)
```

**Why This Is Wrong**:
1. Matching names are weak evidence (could be coincidence)
2. DDS join logic (JFLD) was not consulted because DDS is missing
3. No DB2 FOREIGN KEY constraint was found
4. No program analysis confirms the join

**Correct Action**: Mark as relationship candidate pending evidence

```
TBD-ORDER-SYSTEM-003: Confirm foreign key relationship between ORDER and CUSTOMER
- Status: pending_source (blocking)
- Observed: ORDER file has CUSTNO field; CUSTOMER file has CUSTNO field
- Weak Evidence: "Naming convention match" - insufficient
- Fallback Evidence: program-analysis-OBJ-ORDENTRY-001.md does not show explicit CUSTOMER lookup
- Candidate Relationship (unconfirmed): ORDER.CUSTNO -> CUSTOMER.CUSTNO
- Confirmation Required:
  - DDS source for ORDER showing explicit join or reference
  - DB2 FOREIGN KEY constraint (via approved QSYS2 catalog extract or SQL DDL)
  - Program analysis showing join logic (CHAIN to CUSTOMER by CUSTNO)
- SME Input: Is ORDER.CUSTNO actually a foreign key to CUSTOMER? How is referential integrity enforced?
```

### Unrecorded Object in Inventory

**Problem**: Program analysis references OBJ-ORDITEM-001 (order line items), but this object is not in the approved inventory.

**Incorrect Action**: Proceed with analysis and hope for the best

**Correct Action**: Stop and escalate

```
TBD-ORDER-SYSTEM-004: ORDITEM file not found in approved inventory
- Status: pending_source (blocking)
- Evidence: program-analysis-OBJ-ORDENTRY-001.md references file ORDITEM (line 95, WRITE ORDITEM)
- OBJ-ID: Should be OBJ-ORDITEM-001, but not in 01_inventory/inventory.yaml
- Inventory Gap: Inventory is missing file object
- Action Required:
  - Verify that ORDITEM exists in production
  - Locate DDS and/or DB2 metadata
  - Add OBJ-ORDITEM-001 to inventory
  - Re-run inventory completeness gate
- SME Input: Is ORDITEM a real file? If so, why is it missing from inventory?
```

## What the Blocked Analysis Looks Like

### Header

```
Status: BLOCKED
Analysis Date: 2026-05-16
Reason: Critical source evidence missing; cannot proceed without DDS or equivalent metadata

Blocking TBDs:
- TBD-ORDER-SYSTEM-001: Locate DDS source for ORDER file [pending_source]
- TBD-ORDER-SYSTEM-002: Confirm primary key structure [pending_source]
- TBD-ORDER-SYSTEM-003: Confirm foreign key relationships [pending_source]
- TBD-ORDER-SYSTEM-004: ORDITEM file missing from inventory [pending_source]
```

### Incomplete Data Dictionary (What NOT to show)

**DO NOT** produce half-finished field lists like:

```
INCORRECT - Filled with guesses
| ORDNO | 10A | Inferred from program as order number |
| CUSTNO | 10A | Inferred as customer FK |
| ORDDATE | 8,0 | Guessed from field name (probably YYYYMMDD) |
| STATUS | 2A | Appears to be status code; unknown values |
```

**DO** produce blocked report instead:

```
CORRECT - Clearly blocked, awaiting evidence
Fields cannot be documented without DDS source.
See blocking TBDs above.
```

## Recovery Path

To unblock this analysis:

1. **Locate DDS Source** (TBD-ORDER-SYSTEM-001)
   - Search archive libraries or version control
   - Contact IBM i SME: "Has ORDER file DDS been archived?"
   - Alternative: Reconstruct minimal DDS from DSPFFD + DB2 catalog

2. **Verify Inventory Completeness** (TBD-ORDER-SYSTEM-004)
   - Confirm ORDITEM exists and is accessible
   - Add missing objects to inventory
   - Re-run inventory completeness gate

3. **Re-Run Analysis** with evidence
   - Provide DDS for ORDER and ORDITEM
   - Provide DB2 constraint info (PK, FK, UNIQUE)
   - Re-run data model analyzer in fresh session

4. **Validate Recovered Facts**
   - SME reviews recovered DDS
   - SME confirms key structure, relationships
   - SME approves re-run results

## Key Lessons

### What This Example Teaches

1. **Stop on Missing Source**: If DDS/metadata cannot be found, block immediately. Do not guess.

2. **Don't Invent Keys**: Inferred keys (from names or program usage) are candidates, not facts. Mark as TBD.

3. **Don't Invent Relationships**: Matching field names are weak evidence. Require explicit DDS/DB2 confirmation.

4. **Inventory is Ground Truth**: If an object is not in inventory, treat it as unverified. Do not proceed with downstream use.

5. **TBDs Communicate Gaps**: Explicit, actionable TBDs are better than guesses. They tell the SME exactly what's needed to proceed.

### How to Recognize This Situation

Signs that analysis is becoming blocked:

- [ ] DDS source cannot be found for a physical file
- [ ] Only DSPFFD or DB2 metadata available (incomplete evidence)
- [ ] Program analysis shows file usage but no explicit joins or constraints
- [ ] Inventory does not list an object that programs reference
- [ ] Field meanings depend on guessing from names
- [ ] Key structure seems uncertain from available evidence
- [ ] Foreign key relationships are inferred from naming conventions, not DDS/DB2

**Recommendation**: When 2+ of these conditions apply, stop and create blocking TBDs instead of proceeding.

---

Generated by legacy-ibmi-data-model-analyzer v0.1.0
Legacy Spec Factory Copyright 2026 Leo L Zhang
