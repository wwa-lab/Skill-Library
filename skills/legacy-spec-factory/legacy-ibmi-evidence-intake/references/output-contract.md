# Evidence Intake Output Contract

This document specifies the structure, required fields, validation rules, and
downstream usage rules for artifacts produced by the evidence-intake workflow.

---

## Evidence Manifest (`evidence-manifest.yaml`)

### Purpose

Single source of truth for all evidence items: IDs, types, sources, sensitivity,
source-path authorization or redaction status, approvals, package state, and
downstream inventory gate status.

### Package States

The manifest may exist in three states:

| `package_state` | Meaning | Downstream inventory |
| --- | --- | --- |
| `draft` | Intake is being assembled and has not reached review. | Not allowed |
| `blocked` | Intake has a blocking redaction, sensitivity, approval, or evidence gap. | Not allowed |
| `approved_for_inventory` | Source-path authorization or required redaction is complete; only non-blocking TBDs may remain. | Allowed |

Use the Step Contract compact validation status for the gate decision:

```yaml
intake_decision:
  status: pass | pass_with_warnings | blocked
  downstream_inventory_allowed: true | false
  decision_notes: string
```

`pass_with_warnings` is allowed only when all open `TBD-*` items are explicitly
non-blocking for inventory and are carried forward in `unresolved_items`.

### Required Top-Level Fields

```yaml
package_state: draft | blocked | approved_for_inventory
intake_mode: internal_source_review | governed_redaction

capability:
  name: string                    # Human-readable capability name
  slug: string                    # CAPABILITY-SLUG (used in IDs)
  description: string             # Business context
  source_system: string           # IBM i system and/or library context
  collection_date: YYYY-MM-DD     # When collected
  collection_context: string      # Which system, job, or process

redaction:
  owner: string | null            # Required before approved_for_inventory only when redaction_required is true
  owner_title: string | null
  owner_email: string | null
  redaction_date: YYYY-MM-DD | null
  approval_date: YYYY-MM-DD | null

intake_review:
  owner: string                   # Developer/reviewer responsible for Step 0 decision
  owner_title: string | null
  owner_email: string | null
  review_date: YYYY-MM-DD
  approval_status: pending | approved | approved_with_non_blocking_tbd | blocked
  approval_notes: string

sme_review:
  required: boolean               # false is valid for internal source review
  owner: string | null            # Required only when required is true
  owner_title: string | null
  owner_email: string | null
  review_date: YYYY-MM-DD | null
  approval_status: not_required | pending | approved | approved_with_non_blocking_tbd | blocked
  approval_notes: string

intake_decision:
  status: pass | pass_with_warnings | blocked
  downstream_inventory_allowed: boolean
  decision_notes: string

evidence_items:
  - array of evidence item objects (see below)

unresolved_items:
  - array of TBD objects (empty when no gaps remain)

summary:
  total_items: number
  items_by_type: {object with counts}
  items_by_review_status: {object with counts}
  items_by_redaction_status: {object with counts}
  next_steps: [string ...]
```

### Base Evidence Item Fields

Every item in `evidence_items` must include:

```yaml
evidence_id: string               # EV-<SLUG>-NNN (required, unique)
type: string                      # See type-specific schemas below
subtype: string | null            # rpgle, clle, dds, csv, job_log, screenshot, etc.
source_location: object           # Shape depends on evidence type
original_filename: string
redacted_filename: string | null  # Approved analysis path; may equal original source path for internal_source_review
source_path_verified: boolean     # True when user-provided source path is authorized for internal analysis
redaction_required: boolean
size_bytes: number | null
description: string
sensitivity: public | internal | confidential | unknown
sensitive_content: [string ...]   # Category names only, never raw values
redaction_status: not_required | pending | reviewed | approved | failed
approval_basis: source_path_provided | developer_review | redaction_owner_review | sme_review
redaction_notes: string           # What was done and why; no raw values
sme_required: boolean
sme_approval: boolean
reviewed_by: string | null
review_date: YYYY-MM-DD | null
tags: [string ...]
review_status: draft | in_review | approved | rejected
```

`sensitivity: unknown`, `redacted_filename: null`, missing reviewers, and
`redaction_status: pending` are valid only while `package_state` is `draft` or
`blocked`. They must be linked to an unresolved `TBD-*` before the manifest is
saved as blocked.

For `intake_mode: internal_source_review`, `redacted_filename` means "approved
analysis path" and may equal `original_filename` or the supplied source path
when all of the following are true:

- `source_path_verified: true`
- `redaction_required: false`
- `redaction_status: not_required` or `reviewed`
- `approval_basis: source_path_provided` or `developer_review`

This is the normal Step 0 path for source members and metadata inside an
isolated company environment. Do not block inventory merely because no separate
redacted copy exists.

### Type-Specific Source Location Fields

All items use the base fields above. The `source_location` object then varies by
type.

#### `source_member`

```yaml
type: source_member
subtype: rpgle | cobol | clle | dds | sql | other
source_location:
  library: string
  source_file: string | null       # e.g. QRPGLESRC, QCLLESRC, QDDSSRC
  member_name: string
  object_name: string | null
  object_type: PGM | FILE | DSPF | PRTF | LF | PF | SQL | other
  last_modified: YYYY-MM-DD | null
```

#### `db_metadata`

```yaml
type: db_metadata
subtype: db2_field_description | catalog_export | dspffd | dspfd | other
source_location:
  library: string
  object_name: string
  object_type: FILE | TABLE | VIEW | LF | PF | other
  collection_method: string        # DSPFFD, catalog view, vendor export, etc.
  collection_date: YYYY-MM-DD | null
```

#### `job_log`

```yaml
type: job_log
subtype: job_log | trace | other_log
source_location:
  job_name: string
  job_user: string | null
  job_number: string | null
  job_queue: string | null
  library: string | null
  collection_date: YYYY-MM-DD
  collection_time: HH:MM:SS | null
```

#### `screen_sample`

```yaml
type: screen_sample
subtype: screenshot | screen_note | video_sample | other
source_location:
  screen_name: string
  display_file: string | null
  library: string | null
  collection_date: YYYY-MM-DD
  collection_method: string
```

#### `transaction_sample`

```yaml
type: transaction_sample
subtype: csv | json | fixed_width | database_extract | other
source_location:
  transaction_type: string
  source_file: string | null
  library: string | null
  sample_date: YYYY-MM-DD
  sample_count: number
  sampling_notes: string | null
```

#### `spool_or_report`

```yaml
type: spool_or_report
subtype: spool_file | prtf_source | report_output | other
source_location:
  report_name: string | null
  printer_file: string | null
  output_queue: string | null
  job_name: string | null
  library: string | null
  collection_date: YYYY-MM-DD
```

### Unresolved Item Fields

Use one row per open question, evidence gap, contradiction, or redaction blocker.

```yaml
unresolved_items:
  - tbd_id: TBD-<SLUG>-NNN
    category: missing_inputs | evidence_gaps | contradictory_evidence | sme_questions | downstream_handoff_blockers
    points_to: [string ...]        # Evidence IDs, paths, or artifact names
    finding: string
    resolver: source_owner | redaction_owner | sme | data_owner | reviewer
    blocks_inventory: true | false
    blocks_later_analysis: true | false
    next_step: string
    status: open | resolved | waived
```

### Validation Rules

All manifest states:

- Every `evidence_id` must be unique within the capability.
- Every `evidence_id` must match `EV-<SLUG>-NNN` (NNN = 001-999).
- Every `TBD-*` must match `TBD-<SLUG>-NNN` and have a resolver and next step.
- No raw sensitive values may appear in any manifest field.
- Dates must use ISO 8601 calendar format (`YYYY-MM-DD`) when known.
- Summary counts must match the item list.

`package_state: blocked`:

- `intake_decision.status` must be `blocked`.
- `downstream_inventory_allowed` must be `false`.
- At least one unresolved item must have `blocks_inventory: true`.
- Any item with `sensitivity: unknown`, missing approved analysis path, missing
  required redaction owner, or missing reviewer must point to a blocking
  `TBD-*`.

`package_state: approved_for_inventory`:

- `intake_decision.status` must be `pass` or `pass_with_warnings`.
- `downstream_inventory_allowed` must be `true`.
- No evidence item may have `sensitivity: unknown`.
- Every item must have a `redacted_filename` or approved analysis path. In
  `internal_source_review`, this may be the original source path with
  `source_path_verified: true`.
- Every item with `redaction_required: true` must have `redaction_status:
  approved`.
- Internal/public source-path-authorized items may have `redaction_status:
  not_required`, `reviewed`, or `approved`.
- Confidential source code or metadata may proceed without masking only when
  `intake_mode: internal_source_review`, `source_path_verified: true`, and
  `redaction_required: false`; mark `redaction_status: reviewed`.
- `sme_approval` must be `true` only for items with `sme_required: true`.
- `intake_review.approval_status` must be `approved` or
  `approved_with_non_blocking_tbd`.
- `sme_review.approval_status` may be `not_required` for Step 0 internal source
  review; otherwise it must be `approved` or
  `approved_with_non_blocking_tbd` when `sme_review.required: true`.
- Any open unresolved item must have `blocks_inventory: false`.

---

## Redaction Log (`redaction-log.md`)

### Purpose

Audit trail of what was authorized as source-path input or redacted, why, by
whom, and when. Enables compliance review and traceability without exposing raw
sensitive data.

### Required Sections

1. **Metadata**
   - Capability name and slug
   - Intake reviewer (name, title, email)
   - Redaction owner (name, title, email), when redaction was required
   - Redaction date
   - Review status (`draft | in_review | approved | blocked`)

2. **Redaction Summary Table**
   - Evidence ID, item name, sensitivity level, strategy, status, issues, owner

3. **Detailed Redaction Records (one per evidence item)**
   - What category was redacted
   - Why (PII, financial data, operational secret)
   - Replacement strategy (stable fake IDs, amount masking, removal)
   - Shape preservation (field type, length, scale)
   - Semantic preservation for rule-critical constants and thresholds
   - Spot-check results

4. **Spot-Check Procedure**
   - File opens without errors
   - Logic is understandable after redaction
   - No missed PII patterns
   - Calculations still valid or explicitly marked synthetic
   - Timestamps/error codes preserved

5. **Redaction Challenges and Decisions**
   - Any strategic decisions (preserve amounts, synthesize thresholds, remove
     secrets, etc.)
   - Risk assessment
   - Approval

6. **Post-Redaction Verification**
   - All files validate (syntax, structure, integrity)
   - No corruption
   - SME approved quality

7. **Approval Records**
   - Intake reviewer sign-off
   - Redaction owner sign-off, when required
   - SME reviewer sign-off, when required
   - Final decision (`pass | pass_with_warnings | blocked`)

### Validation Rules

- No raw sensitive values anywhere in the log.
- Document what was redacted (for example, "customer account numbers"), not which
  raw values were removed.
- If a rule-critical threshold, coefficient, amount, or code value is changed,
  mark the replacement as synthetic and state whether the exact legacy value may
  be inferred downstream.
- All decisions must be justified and approved by the intake reviewer.
- All spot-checks must pass before `approved_for_inventory`.

---

## Evidence Intake Review Checklist (`evidence-intake-review-checklist.md`)

### Purpose

Developer- or SME-executable assessment of evidence completeness, source-path
authorization, redaction quality when required, and readiness for downstream
analysis.

### Required Sections

1. **Scope**
   - Capability slug
   - Paths to manifest and redaction log
   - Reviewer name and date

2. **Evidence Completeness Matrix**
   - For each expected evidence type: present or pending?
   - For each item: sensitivity classification correct?
   - Any blocking gaps?

3. **Sensitivity Assessment and Redaction Quality**
   - For each evidence item:
     - Is sensitivity classification correct?
     - Is redaction complete (no missed PII)?
     - Is business logic preserved or explicitly marked synthetic?
     - SME approval status, when SME review is required

4. **Evidence Completeness for Downstream Analysis**
   - What does inventory need? Is it present?
   - What does flow analysis need? Is it present?
   - What does data modeling need? Is it present?
   - Any blocking gaps?

5. **Unresolved Item Impact Assessment**
   - For each TBD or gap:
     - Is it blocking for inventory?
     - Is it blocking for later analysis?
     - Who resolves it?
     - When can it be collected?

6. **Contradictions and Conflicts**
   - Are any evidence items contradictory?
   - Which require SME resolution?

7. **Intake Reviewer Sign-Off**
   - Approval status
   - Date and signature

8. **Redaction Owner Sign-Off, if Required**
   - Approval status
   - Date and signature

9. **SME Review Sign-Off, if Required**
   - Evidence suitability for modernization
   - Confidence in redaction quality
   - Approval status
   - Date and signature

### Validation Rules

- Every evidence item must have reviewer assessment.
- SME assessment is required only when `sme_required: true` or a business
  judgment is needed to unblock inventory.
- All required sign-offs must be dated for `approved_for_inventory`.
- No item can be marked approved with `sensitivity: unknown`.
- All blocking items must be listed in `unresolved_items`.
- All TBDs must have next steps.

---

## Organized Redacted Evidence Directory

### Directory Structure

```text
evidence/
├── manifest.yaml              # Registry (EV IDs, statuses, approvals)
├── redaction-log.md           # Audit trail
├── intake-review-checklist.md # SME assessment
│
├── 01_sources/                # RPGLE, COBOL, CLLE, DDS, SQL
│   ├── EV-SLUG-001-PROGRAM.RPGLE
│   ├── EV-SLUG-002-MENU.CLLE
│   └── ...
│
├── 02_metadata/               # DB2 FD, job descriptions, CL flows
│   ├── EV-SLUG-010-TABLE.FD
│   └── ...
│
├── 03_logs/                   # Job logs, spool, traces
│   ├── EV-SLUG-020-JOBLOG.txt
│   └── ...
│
├── 04_samples/                # Screen samples, transaction records
│   ├── EV-SLUG-030-SCREEN.png
│   ├── EV-SLUG-040-CREDRQ-SAMPLE.csv
│   └── ...
│
└── 05_reports/                # Report definitions, sample output
    ├── EV-SLUG-050-REPORT.PRTF
    └── ...
```

### Naming Rules

- File names must include evidence ID: `EV-SLUG-NNN-description`.
- Use hyphens, not spaces or underscores.
- Keep file extensions (`.RPGLE`, `.CLLE`, `.txt`, `.csv`, `.png`).
- Lowercase is preferred unless the shop uses uppercase IBM i source-member
  naming consistently.

---

## Downstream Usage Rules

### For `legacy-ibmi-inventory`

- Accept only manifests with `package_state: approved_for_inventory`.
- Reference evidence by `evidence_id`, not file name.
- Example: "See EV-CREDIT-CHECK-001 for RPGLE source."
- Cross-check all references against the manifest.
- If evidence is contradictory, flag for SME resolution.

### For `legacy-ibmi-flow-analyzer`

- Use evidence IDs in flow diagram annotations.
- Link each step to supporting evidence.
- If evidence is missing, mark as TBD (pending collection).
- Preserve all error messages from logs (`EV-*-020` type items).

### For `legacy-ibmi-program-analyzer`

- Reference source code (`EV-*-001`, etc.) by ID.
- Link each behavior and exception to evidence.
- Preserve field types and lengths from metadata (`EV-*-010` type items).
- If data flow is unclear, escalate to SME.

### For `legacy-spec-writer`

- Every business rule must have an `evidence_ids` list.
- Example: `br_id: BR-CREDIT-CHECK-001, evidence_ids: [EV-CREDIT-CHECK-001, EV-CREDIT-CHECK-020]`.
- Link decisions to evidence in `spec.yaml`.

---

## Quality Gates

### Evidence Manifest Gate

Before manifest is approved for inventory:

- [ ] Package state is `approved_for_inventory`.
- [ ] Intake decision is `pass` or `pass_with_warnings`.
- [ ] All items have EV IDs.
- [ ] All IDs are unique.
- [ ] All items have type, subtype, source metadata, and description.
- [ ] No item has `sensitivity: unknown`.
- [ ] All items requiring redaction have `redaction_status: approved`.
- [ ] All items not requiring redaction have `source_path_verified: true` or an
      approved analysis artifact path.
- [ ] All items with `sme_required: true` have `sme_approval: true`.
- [ ] All dates are ISO format when known.
- [ ] No raw sensitive values appear in any field.
- [ ] Summary counts match item count.

### Redaction Log Gate

Before log is approved:

- [ ] All redaction actions are documented by category.
- [ ] No raw sensitive values appear.
- [ ] Synthetic replacements for rule-critical values are labeled.
- [ ] All decisions are justified.
- [ ] All spot-checks passed.
- [ ] Redaction owner signed off.
- [ ] SME reviewed and approved when required.

### Review Checklist Gate

Before checklist is approved:

- [ ] All evidence items assessed.
- [ ] All sensitivities verified.
- [ ] All redactions spot-checked.
- [ ] All gaps documented as TBDs.
- [ ] All contradictions identified.
- [ ] No blocking issues remain for inventory.
- [ ] Redaction owner signed off.
- [ ] Intake reviewer signed off.
- [ ] SME signed off when required.

---

## Downstream Handoff Criteria

Evidence intake is complete and ready to pass to `legacy-ibmi-inventory` when:

- Package state is `approved_for_inventory`.
- Intake decision is `pass` or `pass_with_warnings`.
- All evidence items have EV IDs and are organized.
- Manifest is complete and signed.
- Redaction log is complete and signed.
- Review checklist is complete and signed by the intake reviewer.
- SME review is complete when `sme_review.required: true`; otherwise it may be
  deferred to inventory/program/module analysis.
- No item has `sensitivity: unknown`.
- All items have source-path authorization or completed redaction.
- No unresolved item has `blocks_inventory: true`.
- All contradictions that affect business meaning are escalated to SME.

---

## Common Issues and Resolutions

| Issue | Solution |
| --- | --- |
| Evidence item has `sensitivity: unknown` | Block intake; escalate to intake reviewer for assessment |
| Redaction removed business-critical information | Rework redaction; preserve values or label synthetic replacements |
| Evidence item references missing file | Document as TBD; plan follow-up collection |
| Contradictory evidence (two sources disagree) | Document in manifest; escalate to SME for decision |
| Manifest has duplicate EV IDs | Assign new IDs for duplicates; do not renumber reviewed IDs |
| Spot-check found missed PII | Rework redaction; re-spot-check; re-approve |
| SME not known at Step 0 | Do not block internal source review; record `sme_review.required: false` or a non-blocking later-analysis TBD |
| SME rejects redaction quality | Return to redaction owner; rework; re-submit to SME |

---

## Versioning

Evidence manifest and logs should include:

- Capability slug (stable, used in IDs)
- Collection date (when evidence was gathered from IBM i)
- Redaction date (when PII was removed)
- Review date (when SME approved)
- Document version or creation date in file header

Example:

```yaml
# Evidence Manifest: Customer Credit Check
# Capability: CREDIT-CHECK
# Collected: 2026-05-14
# Redacted: 2026-05-15
# Reviewed: 2026-05-16
# Version: 1.0
```

---

## Reference

- `../../docs/data-collection-and-redaction.md` — Organization policy
- `../../docs/id-conventions.md` — ID format rules
- `evidence-types.md` — Evidence type definitions
- `redaction-checklist.md` — Redaction patterns
