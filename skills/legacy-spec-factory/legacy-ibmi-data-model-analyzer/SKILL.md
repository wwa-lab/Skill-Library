---
name: legacy-ibmi-data-model-analyzer
description: Analyze IBM i data models from DDS physical/logical files, DB2 for i metadata, SQL DDL, approved inventory, and program/flow evidence to produce an evidence-backed data model package with dictionary, access paths, CRUD matrix, and SME review checklist. Use when reverse-engineering a business domain's data structure to support modernization. Layer 1.5 (platform-specific) skill of the Legacy Spec Factory reverse chain.
license: Apache-2.0
metadata:
  author: Leo L Zhang
  maintainer: platform-engineering
  source: https://github.com/wwa-lab/legacy-spec-factory
  source_commit: 8871a6b
  domain: legacy-spec-factory
---

<!--
Legacy Spec Factory
Copyright 2026 Leo L Zhang

Original author: Leo L Zhang
License: Apache License 2.0

This skill is part of the Legacy Spec Factory project.
Retain this notice in substantial copies or derived versions.
-->

# IBM i Legacy Data Model Analyzer

## Purpose

Create a comprehensive analysis of one or more IBM i data structures
(physical files, logical files, SQL tables, views) documenting record formats,
field definitions, keys, access paths, and evidence-backed relationships. This
skill does not infer business rules from field names, invent field meanings or
keys, or design target schemas. It produces evidence-backed data structure
analysis ready for SME validation and downstream spec generation.

## Pipeline Position — Conditionally Required

This skill is **mandatory** (not optional) when
`inventory.yaml.sme_review.downstream_required.data_model_analyzer.required: true`.
Inventory auto-detects the trigger when:

- the module touches ≥ 3 physical/logical files
- two files share a key field (foreign-key-like relation)
- any program writes to ≥ 2 master files (compound transactional update)

SME confirms during the same single batched signoff as criticality. Full
trigger rules:
[`skills/legacy-ibmi-inventory/references/downstream-triggers.md`](../legacy-ibmi-inventory/references/downstream-triggers.md).

When triggered, the orchestrator's `3b Program Analysis Done` gate
refuses to advance until
`04_modules/<MODULE-SLUG>/data-model/dictionary.md` exists at
`review_status: approved` or `approved_with_non_blocking_tbd`.

Downstream consumers when this output exists:

- `legacy-ibmi-module-analyzer` View 4 (Data Flow) — populates from the
  dictionary instead of re-deriving from program-analysis rows
- `legacy-spec-writer` populates `spec.yaml.data_model.entities` directly
  from `dictionary.md`, preserving cross-program invariants
- `legacy-golden-master-test-planner` consumes the dictionary for
  test data shapes

For tiny modules (≤ 2 files, no FK-like relations), the trigger is NOT
met (`required: false`); spec-writer derives entities from inventory
directly without this skill's overhead.

## Inputs

Accept:

- **DDS source files** (PF, LF definitions) for the domain being analyzed
- **DB2 for i metadata** (DSPFFD output, catalog views, or SQL DDL scripts)
- **SQL DDL scripts** (if available for migrated tables or hybrid systems)
- **Approved inventory** with file objects (OBJ-*) already cataloged in `01_inventory/inventory.yaml`
- **Approved program analyses** that reference these files when CRUD/lifecycle
  behavior is in scope; analyses are required for every program that writes,
  updates, or deletes in-scope data
- **Optional approved flow analyses** that connect file usage to business
  transaction context
- **Optional:** SME notes on retention policies, archival, data quality issues, or migration constraints

Stop and require clarification if:

- DDS source is missing or incomplete (create TBD instead of guessing)
- File object is not found in the approved inventory
- A program writes, updates, or deletes an in-scope file but lacks an approved
  `program-analysis-<OBJ-ID>.md`
- Source contains raw, unredacted production data (require redaction review per `../../../docs/legacy-spec-factory/data-collection-and-redaction.md`)
- Business meaning of fields or relationships is ambiguous (mark as TBD, do not invent)
- Retention, archival, or purge policies are unknown (mark TBD for SME decision)

## Output Contract

Produce:

- `03_data_models/<DATA-SLUG>/` directory with unified data model analysis

`<DATA-SLUG>` must be uppercase and hyphen-separated (for example,
`CUSTOMER-MASTER`). Do not use lowercase directory names.

Use:

- `templates/data-model-overview.md` as the entry point
- `templates/data-dictionary.md` for field-level documentation
- `templates/relationship-map.md` for candidate keys and access patterns
- `templates/access-paths.md` for logical file definitions, views, and indexed access
- `templates/crud-lifecycle-matrix.md` for program-to-file interaction mapping
- `templates/data-model-review-checklist.md` for SME validation
- `references/output-contract.md` for stable ID minting and field definitions
- `references/dds-patterns.md` for physical/logical file recognition
- `references/db2-patterns.md` for DB2 for i metadata interpretation
- `../../../docs/legacy-spec-factory/id-conventions.md` for stable IDs (reuse OBJ-*, EV-*; mint DATA-*, TBD-*, STEP-*)
- `../../../docs/legacy-spec-factory/evidence-and-knowledge-taxonomy.md` for evidence strength labels
- `../../../docs/legacy-spec-factory/input-readiness-rubric.md` for input readiness scoring

Examples:

- `examples/positive-pf-lf-model/` - straightforward PF + LF pair with clean DDS and program usage
- `examples/blocking-missing-dds/` - negative case: referenced file without DDS source, TBD handling
- `examples/partial-program-analysis-gap/` - warning/blocking case: structural
  DDS exists, but CRUD/lifecycle is blocked by missing mutating program analysis

## Step Contract

This skill is one step in the Legacy Spec Factory reverse chain. It conforms
to the canonical Step Contract shape - see
`../legacy-step-contract/SKILL.md` and
`../legacy-step-contract/references/step-contract.md` for the full
field-level rules. The summary below is normative for this skill.

### Input

- **Required**: one or more physical files (PF), logical files (LF), or SQL tables referenced in an `approved` (or `approved_with_non_blocking_tbd`) `01_inventory/inventory.yaml`.
- **Required**: DDS source or DB2 metadata for each file; SQL DDL if applicable.
- **Required when CRUD/lifecycle is in scope**: approved program analyses for every program that writes, updates, deletes, archives, or purges in-scope data.
- **Optional**: approved flow analyses that use these files; SME notes on retention, archival, data quality.
- **Input readiness scoring**:
  - `0-5 blocked`: approved inventory missing, target file/table unresolved,
    core DDS/DB metadata missing, mutating program analysis missing when
    lifecycle is in scope, or evidence authorization unresolved.
  - `6 minimum_pass`: approved inventory plus authoritative file/table and
    field metadata are present; missing meanings become TBDs.
  - `7-8 usable`: access paths, mutating program analyses, flow references,
    and data dictionary hints are supplied.
  - `9-10 strong`: sample records, runtime observations, SME field meaning,
    boundary values, retention notes, and exception examples are also supplied.
  - Missing sample records does not block structural data analysis; it limits
    value-domain and edge-case confidence.
- **Readiness checks**: Inventory Completeness Gate passing; files are not marked `blocked` in inventory; source is current production (tier 1) rather than archival; evidence authorization is resolved.
- **Stop conditions**: file missing from inventory; DDS or metadata unavailable; mutating program analysis missing; unauthorized raw production data present.

### Execution

- **Procedure**: see the Workflow section below (9 ordered steps).
- **Allowed inference**: record format and field extraction from DDS syntax; key field recognition from DDS KEY/UNIQUE keywords and DB2 constraints; access path identification from LF definitions and SQL indexes; CRUD patterns from cross-referenced program/flow analyses (not invented).
- **Forbidden assumptions**: field business meaning from names alone; invented keys, relationships, or access patterns; retention policies not stated in DDS comments or SME notes; data quality issues not observed in evidence; target schema design; Java or migration code generation.
- **TBD handling**: missing DDS -> `TBD: pending_source`; ambiguous field meaning -> `TBD: pending_sme_judgment`; unknown retention policy -> `TBD: pending_business_decision`; non-blocking gaps tagged `non_blocking`.

### Output

- **Canonical artifact directory**: `03_data_models/<DATA-SLUG>/` with subdocuments:
  - `data-model-overview.md` (summary, blocking TBDs, sign-off state)
  - `data-dictionary.md` (file-by-file field catalogue with DDS/SQL evidence)
  - `relationship-map.md` (candidate keys, foreign key candidates, access path hints)
  - `access-paths.md` (logical files, SQL views, indexed access methods)
  - `crud-lifecycle-matrix.md` (program-to-file I/O mapping from program/flow analysis)
  - `data-model-review-checklist.md` (SME validation items)
- **Required IDs**: reuses `OBJ-*` (file references) and `EV-*` (evidence)
  from inventory; mints `DATA-<DATA-SLUG>-001` for the data model package and
  additional `DATA-*` only for confirmed/candidate relationships, lifecycle
  trails, or cross-object exchanges. Do not mint `DATA-*` for individual PF,
  LF, SQL table, program, or job objects; those must reuse `OBJ-*`. Mints
  `TBD-*` and `STEP-*` only as appropriate. Does not mint `BR-*`, `CAP-*`,
  `DEC-*`, `AC-*`, or `FK-*`.
- **Slug rule**: all newly minted IDs must use the supplied data-domain slug
  exactly. For example, `ORDER-DATA` produces `DATA-ORDER-DATA-001` and
  `TBD-ORDER-DATA-001`, not `DATA-ORDER-001` or `TBD-ORDER-001`.
- **Handoff status**: `status: draft` until SME review; `approved` or `approved_with_non_blocking_tbd` is required before downstream module analysis, BRD writing, spec generation, or target data design.

### Validation

- **Mechanical**: every in-scope file referenced from inventory is analyzed; every record format has at least one `EV-*` link to DDS or SQL source; every field has a DDS/SQL line number and evidence tag; every unknown constraint or retention policy is explicitly marked TBD with blocking status; required sections all present.
- **AI semantic**: field definitions do not infer business meaning from names; key candidates are traced to DDS KEY/UNIQUE or DB2 constraints, not invented; relationships are marked as candidates (not facts) unless SME-confirmed; CRUD matrix cross-references to program/flow analyses; evidence strength not overstated.
- **SME / human approval**: SME confirms record format completeness, validates key field identification, reviews data quality observations, and makes final determination on retention/archival policy TBDs. Required for all files in regulated or customer-facing domains.
- **Blocking conditions**: any field or key without evidence; any invented key or relationship; any unresolved `pending_source` TBD on a critical file; SME absence when SME is required by the domain's risk class.

Emit a Step Validation Report (see
`../legacy-step-contract/templates/step-validation-report.md`) with
status `pass`, `pass_with_warnings`, or `blocked` when reporting upward
to the orchestrator.

## Workflow

1. **Identify and Verify Files**
   - Accept list of file IDs (OBJ-*) or file names from inventory
   - Confirm each file is in approved `01_inventory/inventory.yaml`
   - Document file type: PF (physical), LF (logical), SQL table, or view
   - Stop if any file is marked `blocked` or missing from inventory
   - Note collection date and source location (source library, DB2 catalog query, DDL script)

2. **Locate and Parse DDS / SQL Source**
   - Retrieve DDS source for each PF/LF from the source library
   - Retrieve DB2 metadata (DSPFFD output or catalog queries) or SQL DDL for each table/view
   - Confirm source is complete: no truncated lines, all RECORD statements present
   - Stop if source is incomplete; create TBD: pending_source
   - Create TBD for any unredacted production data; do not proceed until redacted

3. **Extract Record Formats and Fields**
   - For each file, list all RECORD definitions (LYREC, OUTREC, INZREC in DDS; columns in DB2/SQL)
   - For each field, extract:
     - Field name (exact DDS/SQL name)
     - Data type (A/B/P/S/F in DDS, CHAR/DECIMAL/INT/TIMESTAMP in SQL)
     - Length and decimal scale (for NUMERIC, PACKED, ZONED)
     - Allow nullability (ALWNULL / NULL constraint)
     - COLHDG (column heading) if present
     - EDTCDE / EDTWRD (edit codes) for display format hints
     - Line number in DDS or SQL source
     - SME-approved meaning only when evidenced; otherwise record TBD
   - Tag evidence: `confirmed_from_code` (DDS or SQL syntax)
   - Create TBD if field meaning is ambiguous or undocumented
   - Do NOT infer business meaning from field names; note the name in description only

4. **Identify Keys and Access Constraints**
   - For physical files, extract:
     - Keyed access path from DDS `K` lines
     - Uniqueness only when a DDS `UNIQUE` keyword, DB2 unique constraint,
       or SME-confirmed shop convention supports it
     - Any SIGNED or DESCENDING modifiers
   - For logical files, extract:
     - Key fields from DDS `K` lines
     - ACCSSPTH (access path) name
     - maintenance, select/omit, and join keywords when present
     - Compound keys and key order
   - For SQL tables/views, extract:
     - PRIMARY KEY constraint
     - UNIQUE constraints
     - FOREIGN KEY constraints (candidates for relationship mapping)
     - Index definitions
   - Document key source precisely: DDS `K` lines confirm access-path order,
     but do not by themselves prove uniqueness or business primary-key meaning
   - Tag unique/primary-key claims `confirmed_from_code` only for explicit DDS
     `UNIQUE`, DB2 constraints, or equivalent current production metadata
   - Create TBD if key semantics are unclear or depend on external context
   - Do NOT invent keys; only document what DDS/SQL explicitly defines

5. **Map Access Paths and Logical Files**
   - For each logical file (LF) in scope:
     - List the underlying physical file(s) it accesses
     - Extract DDS key lines and select/omit logic
     - Document any JDFTVAL (join default values) or JFLD (join field) relationships
     - Note if the LF is a join logical (JFILE) - list member files
   - For SQL views:
     - Extract SELECT definition
     - List underlying table(s)
     - Document JOIN conditions if present
   - For SQL indexes:
     - Extract UNIQUE / non-unique status
     - List indexed columns and order (ASC/DESC)
   - Tag: `confirmed_from_code` (from DDS key lines, JFILE/JFLD, or SQL DDL)
   - Create TBD if join logic is complex or undocumented

6. **Cross-Reference Program and Flow Analyses**
   - For each file, retrieve the approved program analyses that reference this file
   - Extract CRUD operations from the program analyses:
     - READ (SETLL, READE, CHAIN, READ operations) -> READ access
     - WRITE operations -> CREATE access
     - UPDATE / DELETE operations -> UPDATE / DELETE access
   - For each flow analysis that includes those programs, note the business context of the file usage
   - Build a CRUD matrix: file x program x operations (READ, CREATE, UPDATE, DELETE)
   - Document call path: which step calls which program; in what sequence
   - Tag: `confirmed_from_code` (from program I/O statements)
   - Create TBD if a program is listed in inventory but no analysis exists

7. **Document Data Quality and Migration Risk Observations**
   - From program analyses, note any error handling patterns related to file access (MONITOR, MONMSG blocks)
   - From flow analyses or SME notes, list known data quality issues (invalid fields, orphaned records, duplicate keys)
   - List any migration constraints observed:
     - Unusual field formats (e.g., ZONED decimals, packed booleans)
     - Character set or language considerations
     - Commitment control or locking dependencies
     - Large table sizes that may affect migration performance
   - Tag observations with the repository taxonomy (`confirmed_from_code`,
     `observed_in_runtime`, `confirmed_by_sme`, or `needs_sme_review`) and
     cite the program analysis, flow analysis, runtime evidence, or SME note
   - Do NOT invent data quality issues; only document what is explicitly noted in analyses or SME input

8. **Capture Retention, Archival, and Purge Questions**
   - From SME notes or inventory comments, extract any stated retention policy
   - Create TBD for each file where retention policy is not documented:
     - `TBD: confirm_retention_policy for [FILE-NAME]`
     - `TBD: confirm_archival_strategy for [FILE-NAME]`
     - `TBD: confirm_purge_rules for [FILE-NAME]`
   - Mark TBD blocking status: all retention TBDs are `pending_business_decision` until SME or compliance confirms
   - Do NOT invent archival or purge rules
   - Document any purge-related programs found in program analyses (batch jobs that clean up old records)

9. **Prepare for SME Review**
   - Consolidate all TBDs created in steps 2-8 with clear blocking status:
     - `pending_source` - missing DDS, incomplete metadata, missing mutating program analysis
     - `pending_sme_judgment` - field meaning, relationship interpretation, data quality confirmation
     - `pending_business_decision` - retention, archival, purge policies
     - `non_blocking` - known gaps that do not affect downstream analysis
   - Generate review checklist for SME validation (see SME Review Questions section below)
   - Mark analysis as `draft` (ready for review)
   - Gate: Analysis artifact is ready when every field, key, and access path has an `EV-*` link; every relationship candidate is marked candidate (not fact) unless SME-approved; all TBDs are explicitly tagged with blocking status

## Workflow State Write-Back (history only — supplemental)

This is a supplemental Layer 1 skill. It produces a data dictionary,
access paths, CRUD matrix, and SME checklist that strengthen module and
spec analysis, but does NOT advance the main linear stage. It does NOT
mutate `capabilities[].stage_id` or `current_focus`.

After a run, append one `history[]` entry to
`<project-root>/workflow-state.yaml` per
[`docs/workflow-state-contract.md`](../../../docs/legacy-spec-factory/workflow-state-contract.md):

```yaml
history:
  - at: <ISO 8601>
    skill: legacy-ibmi-data-model-analyzer
    capability_id: <CAP-* from current_focus, or null if module-scoped>
    stage_after: <UNCHANGED stage_id>
    artifact: <path to the data-model package, e.g. 04_modules/<MODULE>/data-model/dictionary.md>
    note: "data model analyzed for <MODULE-SLUG> — <N> entities, <M> access paths"
```

Also overwrite `project.last_updated_at` / `project.last_updated_by`.

**Permitted side-effect:** if the analysis uncovers new TBDs or evidence
gaps, you MAY append to `capabilities[<CAP-*>].blocking.tbds`. You MUST
NOT change `stage_id`, `last_artifact`, or `last_skill`.

If `workflow-state.yaml` does not exist, this skill does NOT create it.

## Anti-Hallucination Rules

**DDS and DB2 are ground truth for structure.** When approved program analyses
or SME recollection conflict with DDS/SQL metadata, the DDS/SQL syntax wins for
structural claims. The disagreement itself becomes a TBD asking the SME to
confirm whether the DDS is stale, the program logic drifted from the schema, or
the analysis is incomplete. Until then, the data model describes what current
DDS/SQL metadata actually defines.

**Do NOT invent:**

- **Field meanings** from field names alone (e.g., a field named CREDLIMIT does not explain *why* the limit exists, what values are valid, or how it's used)
- **Keys or unique constraints** not supported by DDS `K` lines plus
  `UNIQUE`, DB2 constraints, or SME-confirmed current production metadata
- **Foreign key relationships** not visible in DDS JFILE/JFLD or DB2 FOREIGN KEY; candidates must be marked as such
- **Retention or archival policies** if not stated in DDS comments, SME notes, or job descriptions
- **Data quality issues** if not explicitly observed in program error handling or SME notes
- **Access patterns** beyond what LF definitions or SQL indexes directly show

**Instead:**

- If field meaning is unclear, create `TBD-<SLUG>-NNN: Clarify business meaning of field [name] in [file]`
- If a key is suspected but not declared, tag it `needs_sme_review` with
  explicit reasoning and a `TBD-*`
- If retention policy is unknown, create `TBD-<SLUG>-NNN: Confirm retention and archival policy for [file]`
- If data quality issue is suspected but not confirmed, tag `needs_sme_review` instead of asserting the issue
- If access pattern is complex, document what DDS/SQL explicitly defines and mark ambiguities as TBD

**Evidence minimum:**

- Every field must have at least one evidence link (at minimum, the DDS/SQL line number)
- Every key/access-path claim must have evidence from DDS `K` lines, DDS
  `UNIQUE`, DB2 constraints, or equivalent current production metadata
- Every non-trivial access path must have evidence from LF key lines, select/omit
  lines, join lines, or SQL view/index definitions
- Do not document "likely" structure without explicit evidence tag
- TBD questions count as evidence of a gap, not coverage

## SME Review Questions

The generated data model package must include a checklist. Before approval, SME must validate:

- [ ] All record formats are complete (no missing fields or indicators)
- [ ] Field data types match actual storage (no misinterpretation of DDS type codes)
- [ ] Primary and unique keys are correct (no invented keys, no missed constraints)
- [ ] Logical file definitions and access paths are accurate
- [ ] SQL table/view definitions match DDS equivalents if applicable
- [ ] CRUD matrix correctly reflects program usage patterns
- [ ] Field meanings and purposes are understood (captured TBDs or notes, not invented)
- [ ] Retention, archival, and purge policies are documented or explicitly TBD
- [ ] Data quality observations match known issues in the system
- [ ] Relationship candidates are marked as candidates (not facts) until confirmed
- [ ] No invented keys, fields, or business rules
- [ ] All TBDs are properly classified (blocking vs. non-blocking)
- [ ] Data model is ready for downstream BRD/spec handoff without unresolved
  structural blockers

## Runtime Portability

Canonical source: `skills/legacy-ibmi-data-model-analyzer/SKILL.md`

Runtime adapters are synced via `scripts/sync-skills.sh`:

- Codex: `.codex/skills/legacy-ibmi-data-model-analyzer/SKILL.md`
- Claude Code: `.claude/skills/legacy-ibmi-data-model-analyzer/SKILL.md`
- OpenCode: `.opencode/skills/legacy-ibmi-data-model-analyzer/SKILL.md`
- Open Agent Skills compatible adapter: `.agents/skills/legacy-ibmi-data-model-analyzer/SKILL.md`

No runtime-specific assumptions are embedded in the canonical version.

## Version History

- v0.2.0 (2026-05-16): Promoted from "optional supplemental" to
  "conditionally required". When `inventory.yaml.sme_review.downstream_required.data_model_analyzer.required: true`
  (auto-detected when module touches ≥ 3 files OR shared key fields OR
  compound master-file writes), this skill becomes a mechanically
  enforced prerequisite for `3b Program Analysis Done`. `legacy-spec-writer`
  now populates `spec.yaml.data_model.entities` verbatim from this
  skill's `dictionary.md` instead of re-deriving across program-analysis
  rows, preserving cross-program transactional invariants.
- v0.1.0 (2026-05-16): Initial release
  - 9-step workflow for DDS physical/logical files, DB2 for i, and SQL DDL
  - Record format and field extraction with evidence tagging
  - Key and access path identification without invention
  - CRUD matrix cross-reference to program/flow analyses
  - Data quality and migration risk capture
  - Retention/archival/purge policy TBD handling
  - SME review checklist
  - Positive and negative examples
