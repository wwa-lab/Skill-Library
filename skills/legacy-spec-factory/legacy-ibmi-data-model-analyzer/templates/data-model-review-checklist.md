# Data Model Review Checklist: [DATA-SLUG]

## Metadata

- **Data Slug**: [DATA-SLUG]
- **Analysis Version**: [v0.1.0 / v0.2.0 / etc.]
- **Generated**: [YYYY-MM-DD]
- **Files in Scope**: [n files: OBJ-ID-001, OBJ-ID-002, ...]
- **Approved Program Analyses Used**: [list program-analysis-OBJ-*.md files referenced]
- **Approved Flow Analyses Used**: [list flow-*.md files referenced]

## SME Reviewer Information

- **Name**: [SME name]
- **Title**: [IBM i architect / data architect / domain SME]
- **Organization**: [team or department]
- **Date of Review**: [YYYY-MM-DD]
- **Review Sign-Off Status**: [ ] Approved / [ ] Approved with non-blocking TBDs / [ ] Needs rework / [ ] Blocked

---

## Record Format and Field Completeness

- [ ] **All record formats from DDS are documented**: [Y / N]
  - If N, which records are missing? [list]
  - Evidence: [reference to DDS source; note discrepancy]

- [ ] **All fields in each record are documented**: [Y / N]
  - If N, which fields are missing? [list with file and record name]
  - Evidence: [reference to DDS source]

- [ ] **Field data types are correctly interpreted**: [Y / N]
  - If N, which fields have incorrect types? [list with current vs. correct]
  - Evidence: [DDS type code reference]

- [ ] **Field lengths and decimal scales are correct**: [Y / N]
  - If N, list corrections needed: [field: current -> correct]
  - Evidence: [DDS length specification]

- [ ] **ALWNULL (allow nulls) is correctly documented**: [Y / N]
  - If N, which fields are misclassified? [list]
  - Evidence: [DDS source reference]

**SME Notes**: [any corrections, clarifications, or confirmations]

---

## Key Structure and Constraints

- [ ] **Primary keys are correctly identified**: [Y / N]
  - If N, which files have incorrect keys? [list corrections]
  - Evidence: [DDS K lines plus UNIQUE keyword, DB2 PRIMARY KEY, or SME-confirmed current production metadata]

- [ ] **Unique constraints are complete**: [Y / N]
  - If N, which unique constraints are missing or misidentified? [list]
  - Evidence: [DDS source or DB2 CONSTRAINT]

- [ ] **Key field order is correct**: [Y / N]
  - If N, which keys are misordered? [list corrections]
  - Evidence: [DDS key line sequence or DB2 key metadata]

- [ ] **Key semantics are understood**: [Y / N]
  - If N, describe ambiguity: [e.g., "compound key scope is unclear"]
  - Evidence: [program usage, SME clarification]

**SME Notes**: [confirmations or corrections to key structure]

---

## Logical Files and Access Paths

- [ ] **All logical files (LF) are documented**: [Y / N]
  - If N, which LFs are missing? [list by SRCMBR]
  - Evidence: [SRCLIB/SRCPF source]

- [ ] **LF key fields are correctly extracted from DDS key lines**: [Y / N]
  - If N, which LFs have incorrect keys? [list corrections]
  - Evidence: [DDS key line reference]

- [ ] **Join logical files (JFILE) are correctly identified**: [Y / N]
  - If N, which joins are misidentified? [list corrections]
  - Evidence: [DDS JFILE / JFLD reference]

- [ ] **LF SELECT criteria are correctly documented**: [Y / N]
  - If N, which SELECT statements are incomplete or incorrect? [list]
  - Evidence: [DDS SELECT() reference]

- [ ] **SQL views and indexes are documented (if applicable)**: [Y / N]
  - If N, which views/indexes are missing? [list]
  - Evidence: [SQL DDL or DB2 catalog]

**SME Notes**: [confirmations on LF usage, deprecation status, or changes]

---

## Relationship Mapping

- [ ] **Candidate foreign keys are correctly identified**: [Y / N]
  - If N, which relationships are missing or incorrect? [list]
  - Evidence: [DDS JFLD, DB2 FOREIGN KEY, or program analysis reference]

- [ ] **Relationship candidates are marked as candidates (not facts) unless SME-confirmed**: [Y / N]
  - If N, which relationships are overstated? [list]
  - Evidence: [how they should be reclassified]

- [ ] **No invented keys or relationships are present**: [Y / N]
  - If N, list invented items and request removal: [list]
  - Evidence: [explain why each was unsupported by source]

**SME Notes**: [confirm or reject candidate relationships; note any missing relationships]

---

## CRUD / Lifecycle Matrix

- [ ] **Program-to-file mappings are accurate**: [Y / N]
  - If N, which programs or operations are misclassified? [list]
  - Evidence: [program-analysis reference; note discrepancy]

- [ ] **CREATE operations are complete**: [Y / N]
  - If N, which programs perform unrecorded CREATE? [list]
  - Evidence: [program-analysis reference with WRITE statement location]

- [ ] **READ operations are complete**: [Y / N]
  - If N, which programs perform unrecorded READ? [list]
  - Evidence: [program-analysis reference with SETLL/READE/CHAIN location]

- [ ] **UPDATE operations are complete**: [Y / N]
  - If N, which programs perform unrecorded UPDATE? [list]
  - Evidence: [program-analysis reference with UPDATE statement location]

- [ ] **DELETE operations are complete**: [Y / N]
  - If N, which programs perform unrecorded DELETE? [list]
  - Evidence: [program-analysis reference with DELETE statement location]

- [ ] **Operation conditions and triggers are clear**: [Y / N]
  - If N, which operations lack clarity? [list with required context]

**SME Notes**: [clarifications on program behavior, edge cases, or rarely-used operations]

---

## Field Meaning and Business Context

- [ ] **Field meanings are documented or explicitly marked TBD**: [Y / N]
  - If N, list fields with missing meaning: [list by file and field name]

- [ ] **No field meanings are inferred from names alone**: [Y / N]
  - If N, which fields have overinterpreted meanings? [list with note on what should be removed]
  - Evidence: [examples of overinterpretation]

- [ ] **Field edit codes, formats, and display hints are documented**: [Y / N]
  - If N, which fields lack format documentation? [list]
  - Evidence: [DDS EDTCDE / EDTWRD reference]

**SME Notes**: [clarify field meanings for critical fields; confirm or reject TBDs on meaning]

---

## Retention, Archival, and Purge Policies

- [ ] **Retention policies are documented for all files**: [Y / N]
  - If N, which files lack retention policy? [list as TBD]
  - Evidence: [inventory comment, DDS note, or SME source]

- [ ] **Archival strategy is documented (if applicable)**: [Y / N]
  - If N, which files have unknown archival strategy? [list as TBD]
  - Evidence: [program-analysis reference to archival jobs, or SME clarification]

- [ ] **Purge / delete rules are documented (if applicable)**: [Y / N]
  - If N, which files have unknown purge triggers? [list as TBD]
  - Evidence: [program-analysis reference to cleanup jobs, or SME decision required]

- [ ] **Archival and purge operations are traceable to programs**: [Y / N]
  - If N, which operations are missing program/job references? [list]
  - Evidence: [program-analysis or batch job documentation]

**SME Notes**: [confirm retention periods, archival frequency, purge safety checks; approve or reject archival TBDs]

---

## Data Quality and Migration Readiness

- [ ] **Known data quality issues are accurately documented**: [Y / N]
  - If N, which issues are missing or mischaracterized? [list]
  - Evidence: [program error handling, SME note, or runtime observation]

- [ ] **No data quality issues are invented**: [Y / N]
  - If N, which issues lack evidence? [list for removal]

- [ ] **Migration risks are clearly identified**: [Y / N]
  - If N, which risks are missing? [list examples: large file size, complex access patterns, unusual types]
  - Evidence: [program-analysis reference or data metric]

- [ ] **Mitigation strategies are proposed for high-risk files**: [Y / N]
  - If N, which files need mitigation strategy? [list]

**SME Notes**: [assess data quality issues; propose migration strategies; confirm or revise risk assessment]

---

## Overall Readiness Assessment

- [ ] **All blocking TBDs are resolved or marked as approved_with_non_blocking_tbd**: [Y / N]
  - If N, list unresolved blocking TBDs: [list TBD-SLUG-NNN]
  - Disposition: [what must be done to resolve each]

- [ ] **All non-blocking TBDs are clearly marked**: [Y / N]
  - If N, which TBDs lack classification? [list]

- [ ] **Data model is complete and accurate**: [Y / N]
  - If N, describe gaps: [summary of missing elements or corrections needed]

- [ ] **Data model is ready for downstream use** (module analysis, BRD writing,
  spec generation, and target data design): [Y / N]
  - If N, what rework is required before handoff? [list specific items]

---

## Sign-Off

**SME Name**: [name]
**Title**: [IBM i architect / data architect / domain SME]
**Date**: [YYYY-MM-DD]
**Approval Status**:
- [ ] Approved
- [ ] Approved with non-blocking TBDs (list TBDs: [TBD-IDs])
- [ ] Needs rework (describe blockers: [summary])
- [ ] Blocked (describe critical issues: [summary])

**Approval Notes**:

[Free-text notes on data model quality, key assumptions, recommendations for downstream work, or follow-up actions]

---

## Follow-Up Actions (if any)

- [ ] Action 1: [TBD resolution item or rework task] - Owner: [name] - Due: [date]
- [ ] Action 2: [...]

---

Generated by legacy-ibmi-data-model-analyzer v0.1.0
Legacy Spec Factory Copyright 2026 Leo L Zhang
