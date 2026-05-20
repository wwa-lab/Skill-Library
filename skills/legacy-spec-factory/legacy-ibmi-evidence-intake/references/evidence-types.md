# Evidence Types and Collection Guide

This document defines the types of evidence collected for IBM i modernization
and provides guidance on collection, validation, and sensitivity assessment for
each type.

---

## Source Code Evidence

### RPGLE / ILE RPG Source Members

**What it is:** High-level language procedure source code (RPGLE, ILE RPG).

**Sensitivity:** **Confidential** (contains business rules, thresholds)

**Redaction checklist:**
- [ ] Customer identifiers (account numbers, SSNs)
- [ ] Customer-specific financial values and examples
- [ ] Rule-critical thresholds, parameters, and coefficients only when the data
      owner requires masking; if changed, mark replacements as synthetic
- [ ] API keys or credentials

**Preservation requirements:**
- Keep variable names and field types
- Preserve control flow (IF/THEN/ELSE)
- Preserve loop structures
- Preserve subroutine names
- Preserve exact rule-critical constants when approved; otherwise preserve type,
  scale, branch relationships, and explicitly mark the value as synthetic

### COBOL / CL / DDS Source

**What it is:** COBOL, CLLE, or Data Description Specifications source.

**Sensitivity:** **Internal** to **Confidential** depending on content

**Preservation requirements:**
- Keep variable/field names
- Keep control flow and logic structure
- Keep file and record definitions

---

## Database Evidence

### DB2 for i Table Definitions (DSPFFD)

**What it is:** Field descriptions and schema metadata.

**Sensitivity:** **Internal** (metadata only, no data)

**Redaction:** None required

**Preservation:** All field names, types, lengths, constraints

### Catalog Exports (WRKOBJ, DSPOBJD)

**What it is:** Library/object listings and metadata.

**Sensitivity:** **Internal** (object names are operational)

**Redaction:** None required

---

## Runtime Evidence

### Job Logs

**What it is:** Program execution log from a job.

**Sensitivity:** **Confidential** (may contain transaction IDs, account numbers)

**Redaction checklist:**
- [ ] Customer transaction IDs
- [ ] Account numbers
- [ ] Credentials or API keys

**Preservation requirements:**
- Keep timestamps and timing
- Keep error codes and message types
- **Keep error messages** (FILE LOCKED, RECORD LOCKED, etc.) — operational, not personal

### Spool Files and Report Output

**What it is:** Printer output or report listing.

**Sensitivity:** **Confidential** (contains customer data, amounts)

**Redaction checklist:**
- [ ] Customer identifiers and names
- [ ] Amounts and balances
- [ ] Decisions tied to individuals

**Preservation:** Keep layout, formulas, thresholds, summary counts

### Display File Samples

**What it is:** Screenshot or description of a screen (DSPF).

**Sensitivity:** **Internal** (if test) or **Confidential** (if production)

**Redaction:** Customer IDs and amounts from production data only

**Preservation:** Field labels, positions, validation messages, navigation

---

## Sample Data and Documentation

### Sample Transactions

**What it is:** Representative records or test data.

**Sensitivity:** **Confidential** (if production) or **Internal** (if test)

**Redaction checklist:**
- [ ] Customer identifiers
- [ ] Account numbers
- [ ] Amounts (unless needed for business logic)

**Strategic decision:** Amounts may be preserved to understand approval thresholds
while redacting IDs.

### SME Notes

**What it is:** Documentation from IBM i experts.

**Sensitivity:** **Internal** to **Confidential**

**Redaction:** Remove customer-specific examples and operational secrets

**Preservation:** Business rules, flow, limitations, integrations

---

## Evidence Strength Assessment

| Strength | Definition | Example |
|----------|-----------|---------|
| **Tier 1** | Direct from system; verified | RPGLE, DDS, DB metadata, DSPOBJD |
| **Tier 2** | Observed in execution | Job logs, spool, transaction samples |
| **Tier 3** | Useful but not authoritative | SME notes, documentation |

**Rule:** Ground business rules in Tier 1 or Tier 2 evidence only.

---

## Sensitivity Classification

| Sensitivity | Definition | Redaction |
|---|---|---|
| **Public** | Can be shared openly | ❌ No |
| **Internal** | Operational; no PII/financial data | ❌ No |
| **Confidential** | Contains PII/financial/secrets | ✅ Yes |
| **Unknown** | Cannot determine | 🚫 Block |

---

## Collection Checklist

For each capability, collect:

- [ ] Main programs (RPGLE, COBOL)
- [ ] Menu/routing procedures (CLLE)
- [ ] Primary and secondary screens (DSPF)
- [ ] Report definitions (PRTF)
- [ ] Data descriptions for all files (DDS)
- [ ] Database metadata (DSPFFD)
- [ ] Job description/scheduler notes
- [ ] Job log from recent execution
- [ ] Screen samples (test screenshots)
- [ ] Transaction samples (10–20 records)
- [ ] SME notes (business context)

---

## Validation After Redaction

Spot-check each item:

1. **File integrity:** Opens and parses without errors
2. **Logic preservation:** Business logic remains clear
3. **No missed PII:** Re-scan for patterns
4. **Data types:** Field types/lengths unchanged
5. **Calculations:** Expressions still compute correctly
