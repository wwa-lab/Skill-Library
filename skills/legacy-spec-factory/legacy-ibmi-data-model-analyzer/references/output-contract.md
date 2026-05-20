# Output Contract: legacy-ibmi-data-model-analyzer

This document defines the structure, required fields, ID minting rules, and evidence requirements for data model analysis artifacts produced by the `legacy-ibmi-data-model-analyzer` skill.

## Artifact Directory Structure

```
03_data_models/<DATA-SLUG>/
|-- data-model-overview.md       # Summary, file listing, TBD index, SME sign-off
|-- data-dictionary.md           # Complete field catalogue per file
|-- relationship-map.md          # Keys, relationship candidates, access hints
|-- access-paths.md              # Logical files, SQL views, indexes
|-- crud-lifecycle-matrix.md     # Program-to-file CRUD mapping and lifecycle
`-- data-model-review-checklist.md # SME validation and approval
```

`<DATA-SLUG>` must be uppercase and hyphen-separated. Use
`03_data_models/CUSTOMER-MASTER/`, not `03_data_models/customer-master/`.

## Required Fields in Each Artifact

### data-model-overview.md

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| Domain Slug | string (DATA-SLUG) | Y | Stable, uppercase, hyphen-separated (e.g., CUSTOMER-MASTER); minted DATA ID is `DATA-<DATA-SLUG>-001` |
| Business Context | prose | Y | 1-2 sentence description of business domain covered |
| Inventory Reference | list of OBJ-* | Y | List all files in scope by OBJ-ID from inventory |
| Approved Program/Flow References | list of IDs | Y | List program-analysis and flow-analysis files used |
| Analysis Status | enum | Y | [draft / needs_sme_review / approved / approved_with_non_blocking_tbd / blocked] |
| Last Updated | ISO date | Y | YYYY-MM-DD |
| Reviewed By | string | N | SME name and review date if approved |
| File Table | table | Y | Columns: File Name (OBJ-*), Type, Record Count, Key Fields, Primary Use, Status |
| Blocking TBDs | list | Y | Unresolved blocking issues; empty if none |
| Non-Blocking TBDs | list | Y | Known gaps that do not block approval |
| Handoff Status | checklist | Y | Completion and approval gates |
| Sign-Off | prose | N | SME approval notes (required if approved) |

### data-dictionary.md

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| File Name (OBJ-*) | string | Y | From inventory |
| File Type | enum | Y | [PF / LF / SQL Table / SQL View] |
| Source | string | Y | Source library/member or DDL file path |
| Record Format | string | Y | RECORD name from DDS or table name |
| Evidence ID | string | Y | EV-* pointing to source extraction |
| Collection Date | ISO date | Y | YYYY-MM-DD |
| Field Sequence | integer | Y | 1, 2, 3, ... (order in DDS or SQL) |
| SME-Approved Meaning | string | N | Use only when supported by DDS text, runtime evidence, or SME confirmation; otherwise reference a TBD |
| Field Name (DDS/SQL) | string | Y | Exact name from DDS or SQL definition |
| Data Type | string | Y | A/B/P/S/F (DDS) or CHAR/DECIMAL/INT/TIMESTAMP (SQL) |
| Length | integer | Y | Field length in bytes or digits |
| Decimal Scale | integer | N | For numeric fields; omit if not applicable |
| Allow Null | enum | Y | [Y / N]; defaults to N for DDS fields unless ALWNULL |
| COLHDG | string | N | Column heading from DDS; omit if not present |
| Edit Code | string | N | EDTCDE / EDTWRD from DDS; omit if not present |
| Notes | prose | Y | DDS source line reference; constraint explanation; any TBD reference |
| Evidence | string | Y | EV-* link to field definition source |
| TBD Reference | string | N | TBD-* if field meaning or constraint is pending |

### relationship-map.md

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| Relationship ID | string | Y | `DATA-*` for confirmed or candidate data relationship; do not mint `FK-*` |
| Parent File (OBJ-*) | string | Y | OBJ-ID of parent in relationship candidate |
| Parent Key | string | Y | Comma-separated field names from parent file |
| Child File (OBJ-*) | string | Y | OBJ-ID of child in relationship candidate |
| Child Field(s) | string | Y | Comma-separated field names from child file |
| Relationship Status | enum | Y | [confirmed_from_code / confirmed_by_sme / strongly_inferred / needs_sme_review / contradictory] |
| Evidence | string | Y | EV-* link to DDS JFLD, DB2 CONSTRAINT, or program-analysis reference |
| Notes | prose | N | Explanation of relationship, naming convention, archival implications |

### access-paths.md

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| Logical File Name (or Index Name) | string | Y | Exact name from DDS LF or SQL INDEX definition |
| OBJ-ID | string | Y | From inventory if cataloged; else TBD |
| Base File(s) | string | Y | Comma-separated OBJ-IDs of underlying physical files |
| Key Fields | string | Y | Comma-separated field names from DDS `K` lines or SQL index/view definition |
| Uniqueness | enum | Y | [UNIQUE / non-unique] |
| Sort Order | string | Y | [ASC / DESC / mixed]; field-by-field if mixed |
| Selection Criteria | prose | N | DDS select/omit lines or SQL WHERE clause; omit if not applicable |
| Join Details | prose | N | JFILE / JFLD for join LFs; omit for simple LFs |
| Source Line | integer | Y | Line number in DDS or SQL source |
| Evidence | string | Y | EV-* link to DDS LF or SQL INDEX definition |
| Programs Using | list | Y | List of OBJ-PGM IDs that reference this access path |
| Status | enum | Y | [active / deprecated / candidate] |
| TBD Reference | string | N | TBD-* if selection criteria or usage is pending clarification |

### crud-lifecycle-matrix.md

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| File (OBJ-*) | string | Y | From inventory |
| Program (OBJ-*) | string | Y | From inventory; program-analysis must be approved |
| Operations | string | Y | Comma-separated: [C / R / U / D / A / P / X] for CREATE, READ, UPDATE, DELETE, ARCHIVE, PURGE, EXPORT |
| Conditions | prose | Y | When and why each operation is performed; e.g., "READ on CHAIN by CUSTNO" |
| Evidence | string | Y | Reference to program-analysis-OBJ-PGM-* and specific line number(s) |
| Retention Policy | prose | N | Days/years retained; archival frequency; purge trigger; mark TBD if unknown |
| Archival Job | string | N | OBJ-PGM if known; else TBD |
| Purge Job | string | N | OBJ-PGM if known; else TBD |
| Lifecycle Note | prose | N | Conceptual flow (CREATE -> READ -> UPDATE -> DELETE/ARCHIVE) with expected durations |

### data-model-review-checklist.md

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| Data Slug | string | Y | DATA-SLUG from data-model-overview.md |
| SME Name | string | Y | Name of reviewer |
| SME Title | string | Y | IBM i architect / data architect / domain SME / etc. |
| Review Date | ISO date | Y | YYYY-MM-DD |
| Approval Status | enum | Y | [Approved / Approved with non-blocking TBDs / Needs rework / Blocked] |
| Blocking TBDs Resolved | boolean | Y | All blocking TBDs marked approved_with_non_blocking_tbd or resolved? |
| Record Formats Complete | boolean | Y | All DDS records documented? |
| Fields Complete | boolean | Y | All fields in each record documented? |
| Keys Correct | boolean | Y | Primary and unique keys correctly identified? |
| No Invented Facts | boolean | Y | No invented keys, relationships, or field meanings? |
| Retention Policy Approved | boolean | Y | Retention, archival, purge policies confirmed or marked TBD? |
| Approval Sign-Off | prose | Y | SME notes on approval, caveats, or follow-up actions |

## ID Minting Rules

### Reuse Existing IDs

- **OBJ-*** - Reuse from inventory for all files, programs, jobs
- **EV-*** - Reuse from program/flow analyses for all evidence references

### Mint New IDs

- **DATA-*** - One per data model package, confirmed/candidate data
  relationship, lifecycle trail, or cross-object data exchange, e.g.,
  `DATA-CUSTOMER-MASTER-001`
  - Format: `DATA-<BUSINESS-DOMAIN>-NNN`
  - Capability slug should reflect the business domain, not the skill name
  - Example: `DATA-ORDER-ENTRY-001`, `DATA-GL-ACCOUNT-001`
  - Do not mint `DATA-*` for individual PF, LF, SQL table, program, or job
    objects. Reuse their `OBJ-*` IDs from inventory.
  - Use the supplied `DATA-SLUG` exactly. If the user provides `ORDER-DATA`,
    mint `DATA-ORDER-DATA-001`, not `DATA-ORDER-001`.

- **TBD-*** - One per unresolved question
  - Format: `TBD-<BUSINESS-DOMAIN>-NNN`
  - Use the supplied `DATA-SLUG` exactly. If the user provides `ORDER-DATA`,
    mint `TBD-ORDER-DATA-001`, not `TBD-ORDER-001`.
  - Examples:
    - `TBD-CUSTOMER-MASTER-001: Pending DDS for logical file CUSTBYCTY`
    - `TBD-CUSTOMER-MASTER-002: Confirm retention policy for CUSTOMER file`
    - `TBD-CUSTOMER-MASTER-003: Clarify business meaning of CREDITCODE field`
- **STEP-*** - Only when reporting this analyzer run as a Step Contract instance

### Do NOT Mint

- **BR-*** - Business rules (not produced by data model analyzer)
- **CAP-*** - Capabilities (defined upstream, not by this analyzer)
- **DEC-*** - Modernization decisions (deferred to spec generation)
- **AC-*** - Acceptance criteria (defined in spec generation)

## Evidence Field Requirements

Every significant statement must be backed by evidence:

| Statement Type | Required Evidence | Example |
| --- | --- | --- |
| Field definition | DDS source line or SQL column definition | "Source line 42 in SRCLIB/SRCPF(SRCMBR): FLDNAME 10A" |
| Key identification | DDS `K` lines for access-path order; DDS `UNIQUE` or DB2 constraint for uniqueness/primary key | "DDS line 15: K CUSTNO; line 3: UNIQUE" |
| Access path | LF key/select/omit lines or SQL view/index definition | "DDS line 30: K REGION; DDS line 31: K SALESMAN" |
| Relationship candidate | DDS JFLD, DB2 FOREIGN KEY, or program-analysis reference | "DDS JFLD(CUSTNO CUSTNO); confirmed in program-analysis-OBJ-PGM-042.md line 87" |
| CRUD operation | Program-analysis reference with I/O statement | "program-analysis-OBJ-PGM-035.md: CHAIN by CUSTNO (line 156); UPDATE (line 201)" |
| Retention policy | Inventory comment, job description, or SME note | "Inventory: CUSTOMER file marked 'keep 7 years'; archival via OBJ-PGM-789" |

## Blocking Status Markers

Every TBD must carry explicit blocking status:

| Marker | Meaning | Handoff Impact |
| --- | --- | --- |
| `blocking` | Must resolve before approval | Prevents data model from reaching "approved" status |
| `non_blocking` | SME is aware; does not prevent approval | May be resolved in next iteration |
| `pending_source` | Evidence (DDS, metadata, or program analysis) is missing | Blocks unless marked non_blocking by SME |
| `pending_sme_judgment` | Requires SME interpretation; no clear answer from code | Blocks unless SME provides guidance |
| `pending_business_decision` | Requires business decision (e.g., retention policy) | Blocks unless business owner approves |

Example TBD entry:

```
TBD-CUSTOMER-MASTER-002: Confirm retention policy for CUSTOMER file
- Status: pending_business_decision (blocking)
- Source: Inventory does not document retention period
- Evidence Required: Compliance documentation or business policy statement
- SME Note: [to be filled during review]
- Resolution: [to be filled during review]
```

## Handoff Readiness Criteria

Data model analysis is "approved" when:

1. All blocking TBDs are either resolved or explicitly marked approved_with_non_blocking_tbd by SME
2. Every field, key, and access path has an EV-* evidence link
3. No invented keys, relationships, or field meanings (all marked TBD if unconfirmed)
4. SME has reviewed and signed off on the checklist
5. All required artifacts are present and complete

Handoff status: `approved` or `approved_with_non_blocking_tbd` only; never `draft` or `needs_sme_review` for downstream use.

---

Generated by legacy-ibmi-data-model-analyzer v0.1.0
Legacy Spec Factory Copyright 2026 Leo L Zhang
