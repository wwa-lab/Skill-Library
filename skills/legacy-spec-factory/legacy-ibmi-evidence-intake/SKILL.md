---
name: legacy-ibmi-evidence-intake
description: Register, classify, assign evidence IDs, and record source-path authorization or redaction governance for IBM i modernization evidence. Use when preparing source code, DB metadata, job logs, spool files, screen samples, reports, transactions, or runtime evidence before inventory analysis. This skill records intake metadata, source paths, internal review decisions, and redaction approvals when required. Precedes legacy-ibmi-inventory.
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

# IBM i Evidence Intake

## Purpose

Provide a structured, auditable workflow for registering evidence from IBM i
legacy systems, assigning stable evidence IDs, validating sensitivity status,
governing source-path authorization and, when required, redaction of personally
identifiable information (PII), financial data, credentials, and other regulated
content, and producing a reviewed evidence manifest that downstream skills
(`legacy-ibmi-inventory`, flow analyzer, program analyzer) can reference with
confidence.

Default mode is **internal source review**: evidence remains inside the
company-controlled, isolated environment and the user-provided source path is
the authorization signal for downstream analysis. In this mode, source code and
metadata may proceed without creating a separate redacted copy when the same
source path is recorded as the approved analysis artifact and a developer or
reviewer signs the intake decision.

Use **governed redaction** only when evidence leaves the controlled
environment, contains production data samples/logs/spool/screenshots with PII or
regulated values, or the data owner explicitly requires masking. When evidence
is raw and sensitivity is unknown, work only from file names, counts, checksums,
owner-provided metadata, and review notes until an authorized reviewer confirms
whether internal source review is sufficient or redaction is required.

This skill does NOT perform technical analysis. It establishes the evidence
foundation—traceability, confidentiality, and data governance—that all
downstream skills depend on.

## Inputs

Accept metadata or already-redacted artifacts for any combination of:

- RPGLE, CLLE, COBOL, DDS, SQL source members or exported source files
- DB2 for i table and field metadata (DFD exports, catalog views)
- Job descriptions, CL command flows, scheduler notes
- Job logs, spool files, printer files (PRTF), display files (DSPF)
- Screen flow documentation, screenshots, or video samples
- Sample transactions, expected outputs, and runtime behavior examples
- DB extracts, test data, and masked sample records
- SME notes linking programs, files, or capabilities

For raw or sensitivity-unknown evidence, accept only an inventory of the item
(file name, source system, object/member name, size, owner, collection date,
hash/checksum if available). Do not inspect the raw content.

**Preconditions before intake:**

- IBM i / AS400 system access is authorized and documented.
- Evidence export has been approved by the data owner and client.
- Retention period and storage location are agreed.
- Intake mode is declared:
  - `internal_source_review` for company-internal, isolated analysis where
    source paths are supplied by the user and are allowed as-is.
  - `governed_redaction` for evidence that must be masked before use.
- Reviewer authority is defined. This may be the developer doing the initial
  analysis for internal source review; it does not need to be an SME at Step 0.

**Stop conditions:**

- Raw production samples, logs, spool, screenshots, or database extracts with
  likely PII/regulatory values are present and neither source-path
  authorization nor redaction review is recorded.
- Evidence sensitivity is marked `unknown` and cannot be reviewed by authorized
  staff.
- Evidence bundle is overly broad (e.g., "the entire application" vs. a
  capability slice).
- No developer/reviewer owner is assigned for the intake decision.

## Output Contract

Produce:

- `evidence-manifest.yaml` — structured registry of all collected evidence items,
  assigned IDs, package state, sensitivity classifications, and redaction status
- `redaction-log.md` — human-readable audit trail of what was redacted, why, and
  by whom
- `evidence-intake-review-checklist.md` — SME-executable review steps and
  acceptance criteria
- redacted evidence files (source members, logs, samples) organized by type

Reference templates in:

- `templates/evidence-manifest.yaml`
- `templates/redaction-log.md`
- `templates/evidence-intake-review-checklist.md`

Follow:

- `../../../docs/legacy-spec-factory/data-collection-and-redaction.md`
- `../../../docs/legacy-spec-factory/input-readiness-rubric.md`
- `../../../docs/legacy-spec-factory/id-conventions.md`
- `../../../docs/legacy-spec-factory/evidence-and-knowledge-taxonomy.md`
- `references/evidence-types.md`
- `references/redaction-checklist.md`

## Step Contract

This skill conforms to the Step Contract shape. See
`../legacy-step-contract/references/step-contract.md` for field-level rules.

### Input

- **Required**:
  - Evidence item list or approved analysis / governed-redaction bundle
  - Business capability name and slug (e.g., `CREDIT-CHECK`)
  - Evidence collection date and collection context (which IBM i library, job,
    or system)
  - Assigned intake reviewer. In `internal_source_review`, this is typically the
    developer/reviewer who will analyze the evidence first.

- **Optional**:
  - Prior shop documentation (spreadsheets, wiki, vendor docs) — treat as
    tier-3 hints only
  - Known sensitive data locations or patterns
  - Assigned redaction owner, when governed redaction is required
  - Assigned SME owner, when business judgment or redaction-quality validation
    is required
  - Custom redaction rules beyond standard PII/financial masking

- **Input readiness scoring**:
  - `0-5 blocked`: no evidence list/source path, no capability scope, no
    intake reviewer, unresolved export authorization, or raw production samples
    with neither source-path authorization nor required redaction review.
  - `6 minimum_pass`: evidence items, capability slug, collection context,
    intake mode, and reviewer are present; unknowns are captured as TBDs.
  - `7-8 usable`: sensitivity classes, owners, hashes/checksums, and approved
    analysis paths are mostly populated.
  - `9-10 strong`: collection rationale, known sensitive patterns, SME/data
    owner notes, retention location, and downstream inventory focus are also
    supplied.
  - Missing SME owner is optional in Step 0 unless the intake decision needs
    business judgment, redaction-quality validation, or compliance approval.

- **Readiness checks**:
  - Data owner has approved evidence export.
  - No missing evidence expected (if so, document as a `TBD-<SLUG>-NNN`).
  - Capability slice is narrow enough for one SME to validate (avoid "whole
    application").

### Execution

- **Procedure**: 8 ordered steps below (Workflow section).
- **Allowed inference**: Identifying evidence types from file headers, extensions,
  and metadata; flagging likely sensitive content based on field names and
  patterns; assigning evidence IDs; treating a repeated user-provided source
  path as explicit authorization to use that path internally when
  `intake_mode: internal_source_review`.
- **Forbidden assumptions**: Inventing evidence that was not provided; reading
  unredacted regulated samples without authorization; assuming external
  redaction is required for ordinary source files in an isolated internal
  environment; committing raw production evidence to version control.
- **TBD handling**: Use `TBD-<SLUG>-<NNN>` for gaps (missing evidence files,
  unknown redaction rules, or unclear sensitivity status). Mark `status:
  open` until resolved.

### Output

- **Evidence manifest** (YAML) with every item tagged with:
  - `evidence_id` (EV-<SLUG>-NNN)
  - `type` (source, log, sample, metadata, etc.)
  - `source` (system, library, member name, export date)
  - `sensitivity` (public, internal, confidential, unknown)
  - `redaction_status` (not_required, pending, reviewed, approved, failed)
  - `source_path_verified` (true when the user-provided source path is the
    approved analysis artifact)
  - `approval_basis` (source_path_provided, developer_review,
    redaction_owner_review, sme_review)
  - `redaction_notes` (what was redacted and why)
  - `sme_required` and `sme_approval` (SME approval is required only when
    `sme_required: true`)

- **Package state and gate decision**:
  - `package_state` must be `draft`, `blocked`, or `approved_for_inventory`.
  - `intake_decision.status` must be `pass`, `pass_with_warnings`, or `blocked`.
  - Only `package_state: approved_for_inventory` may be handed to
    `legacy-ibmi-inventory`.
  - `sensitivity: unknown`, missing `redacted_filename`, missing redaction owner,
    or missing required SME approval is allowed only in `draft` or `blocked`
    manifests and must be tied to a `TBD-<SLUG>-NNN` unresolved item. For
    `internal_source_review`, `redacted_filename` may equal the user-provided
    source path when `source_path_verified: true` and `redaction_status:
    not_required` or `reviewed`.

- **Redaction log** (Markdown) documenting:
  - PII replaced and masking strategy
  - Financial data handling
  - Credentials and secrets removed
  - Field shapes and lengths preserved
  - Redaction owner and date
  - Issues encountered (contradictory data, missing items)

- **Review checklist** (Markdown) with:
  - Evidence completeness assessment
  - Sensitivity status confirmation per item
  - Redaction quality spot-check (samples re-reviewed for leaks)
  - Missing evidence impact assessment
  - SME sign-off and review date

- **Organized redacted evidence**:

  ```text
  evidence/
  ├── 01_sources/         # RPGLE, CLLE, COBOL, DDS, SQL
  ├── 02_metadata/        # DB2 FD, job descriptions, CL flows
  ├── 03_logs/            # Job logs, spool, traces
  ├── 04_samples/         # Screen samples, transaction records
  ├── 05_reports/         # Report definitions, sample output
  └── manifest.yaml       # Registry and ID assignments
  ```

## Workflow

### Step 1: Intake and Validation

**Input:**

- Evidence item list or approved analysis / governed-redaction bundle
- Capability scope (name, slug, libraries)
- Data owner approval memo or email

**Actions:**

1. Confirm data owner has approved export.
2. List all evidence items received (count by type: source, log, sample, etc.).
3. Verify capability slice is narrow (one business function, not entire
   application).
4. Assign an intake reviewer. Assign a redaction owner only when governed
   redaction is required. Assign an SME owner only when business judgment is
   needed for the Step 0 decision.
5. Note any obvious gaps (e.g., "DSPF expected but not provided").

**Output:**

- Evidence item list (file names, sizes, dates)
- Intake log with approval reference
- Identified gaps as `TBD-<SLUG>-NNN`

**Stop if:**

- Data owner approval cannot be found.
- Capability scope is too broad.
- Intake reviewer cannot be assigned.

### Step 2: Evidence Typing and Source Mapping

**Input:**

- Evidence item list
- Capability slug
- IBM i library/system context

**Actions:**

1. Classify each item using `references/evidence-types.md`.
2. Record source metadata needed by `references/output-contract.md`.
3. Cross-reference provided inventory lists or SME notes.
4. Flag any missing source, metadata, runtime, or sample evidence as `TBD`.

**Output:**

- Typed evidence list with metadata
- Library/object mapping
- Evidence gaps flagged as `TBD`

### Step 3: Sensitivity Assessment

**Input:**

- Typed evidence list
- Known sensitive patterns (customer IDs, account numbers, etc.)
- Redaction rules from `references/redaction-checklist.md`

**Actions:**

1. Assess each item as `public`, `internal`, `confidential`, or `unknown`
   using `references/evidence-types.md`.
2. Document rationale for each assessment without quoting sensitive values.
3. Flag every `unknown` item for reviewer assessment before downstream use. Use
   a redaction owner for governed redaction; use an SME only when the item's
   business meaning or safe masking strategy cannot be judged by the developer.

**Output:**

- Sensitivity matrix (item vs. classification)
- Redaction priority list (confidential items first)
- Reviewer list (unknown items)

**Stop if:**

- More than a few items are marked `unknown` and no authorized reviewer can
  classify them.

### Step 4: Evidence ID Assignment

**Input:**

- Typed and sensitivity-assessed evidence list
- Capability slug (e.g., `CREDIT-CHECK`)

**Actions:**

1. Assign a sequential `evidence_id` to every item:
   - Format: `EV-<CAPABILITY-SLUG>-NNN`
   - Example: `EV-CREDIT-CHECK-001`, `EV-CREDIT-CHECK-002`
   - Start at 001 for each new capability.
   - Do not renumber after assignment.

2. Create a mapping file listing:
   - EV ID
   - Original file/item name
   - Type
   - Sensitivity
   - Redaction owner, or intake reviewer when redaction is not required

3. Store mapping in source control (no raw data yet).

**Output:**

- Evidence ID assignment log
- Capability slug ↔ evidence ID index

### Step 5: Source Authorization or Redaction Planning

**Input:**

- Sensitivity matrix
- Evidence ID assignments
- Redaction checklist template from `references/redaction-checklist.md`

**Actions:**

1. For each item, choose one path:
   - `internal_source_review`: record the user-provided source path as the
     approved analysis path, set `source_path_verified: true`, and set
     `redaction_status: not_required` or `reviewed`.
   - `governed_redaction`: use `references/redaction-checklist.md` to identify
     categories that must be redacted.
2. Plan replacements that preserve type, field length, decimal scale, and
   downstream-relevant relationships when redaction is required.
3. Create an intake plan with one section per evidence item, including strategy,
   rationale, source path, and unresolved questions.

**Output:**

- Intake/redaction plan (markdown)
- Redaction rules document (custom rules beyond template)
- Estimated effort and timeline

**Stop if:**

- Redaction effort is too high for a governed-redaction package (suggest
  splitting the evidence bundle).
- Custom redaction rules cannot be agreed upon (escalate to SME or data owner).

### Step 6: Redaction Execution Governance

**Input:**

- Redaction plan
- Evidence file inventory (confidential items)
- Authorized redaction owner, when governed redaction is required

**Actions:**

1. If governed redaction is required, the redaction owner performs the actual
   redaction in the approved controlled environment. The agent records the
   redaction plan and the owner's reported results; it does not inspect raw
   confidential content.

2. If internal source review is used, record that the approved analysis artifact
   is the same user-provided source path; do not create a fake redacted copy just
   to satisfy the gate.
3. Require the redaction owner or intake reviewer to confirm that raw originals
   stayed in an approved restricted location and that the plan was followed.
4. Spot-check only approved analysis artifacts for missed sensitive patterns,
   corrupted structure, and lost business logic.
5. Record redaction actions at category and strategy level only; never record
   raw sensitive values.

**Output:**

- Approved analysis artifacts or redacted evidence files
- Detailed source-authorization/redaction log (what was approved or replaced,
  when, by whom)
- Spot-check report

### Step 7: Review

**Input:**

- Approved analysis artifacts or redacted evidence files
- Redaction log
- Review checklist template from `templates/evidence-intake-review-checklist.md`

**Actions:**

1. Assigned reviewer checks source-path authorization, evidence completeness,
   and downstream suitability using the review checklist. The reviewer may be a
   developer for Step 0 internal source review.
2. SME review is optional at Step 0 unless business meaning, data masking, or
   regulatory release needs SME judgment. Record deferred SME routing as a
   non-blocking TBD when inventory can proceed from source evidence.
3. Reviewer marks each item with `review_status: approved` or
   `review_status: rejected`. If the evidence set can advance with known
   non-blocking gaps, record those gaps in `unresolved_items` and set the
   package-level `intake_decision.status: pass_with_warnings`.
4. Reviewer documents missed redactions, data integrity issues, missing
   evidence, and confidence level.
5. If rejections exist, route back to Step 6 (redaction rework) or Step 2
   (evidence collection).

**Output:**

- Review checklist (filled and signed)
- Approval memo with intake reviewer and, when required, redaction owner/SME
  signatures
- List of approved items
- List of TBDs and blocking issues

### Step 8: Manifest and Registration

**Input:**

- All approved evidence items
- Redaction log
- Review approval memo
- Evidence ID assignments

**Actions:**

1. Create the evidence manifest (`evidence-manifest.yaml`):
   - One entry per evidence item
   - Include package-level `package_state`, `intake_decision`, redaction owner,
     intake reviewer, optional redaction owner, optional SME owner, and
     unresolved item ledger
   - Include per-item `evidence_id`, `type`, `subtype`, source metadata,
     `description`, `size_bytes`, `sensitivity`, `redaction_status`,
     `redaction_notes`, `sme_approval`, `reviewed_by`, and `review_date`
   - Use the type-specific field rules in `references/output-contract.md`

2. Organize redacted evidence files:

   ```text
   evidence/
   ├── manifest.yaml
   ├── redaction-log.md
   ├── intake-review-checklist.md
   ├── 01_sources/
   │   ├── EV-CREDIT-CHECK-001-CUSTPGM.RPGLE
   │   ├── EV-CREDIT-CHECK-002-CUSTMENU.CLLE
   │   └── ...
   ├── 02_metadata/
   │   ├── EV-CREDIT-CHECK-010-CUSTDB.FD
   │   └── ...
   ├── 03_logs/
   │   ├── EV-CREDIT-CHECK-020-JOBLOG.txt
   │   └── ...
   └── ...
   ```

3. Verify manifest completeness:
   - All evidence items listed.
   - All IDs assigned.
   - All redaction statuses or source-path authorizations recorded.
   - All required approvals signed.
   - `package_state: approved_for_inventory` has no `sensitivity: unknown`.
   - Any unresolved `TBD-*` is marked non-blocking before inventory is allowed.

4. Document any open issues as `TBD-<SLUG>-<NNN>`:
   - Missing evidence that may be collected later.
   - Contradictory evidence (note the conflict).
   - Unresolved redaction questions.

5. Create a final intake summary:
   - Total evidence items: count by type
   - Items approved, rejected, pending
   - Critical gaps or risks
   - Readiness for downstream analysis

**Output:**

- `evidence-manifest.yaml` (structured registry)
- `redaction-log.md` (audit trail)
- `evidence-intake-review-checklist.md` (signed review)
- Organized redacted evidence files
- Intake summary (markdown)

## Workflow State Write-Back

At the end of an intake run, update `<project-root>/workflow-state.yaml` per
[`docs/workflow-state-contract.md`](../../../docs/legacy-spec-factory/workflow-state-contract.md).
Template: [`skills/legacy-modernization-orchestrator/references/state-writeback-snippet.md`](../legacy-modernization-orchestrator/references/state-writeback-snippet.md).

**Stage this skill produces:**

- `1 Evidence Ready` when every item has `sensitivity` other than `unknown`,
  has either source-path authorization or completed redaction, and all required
  approvals are recorded
- `0 Evidence Intake` (no advancement) if any item still has
  `sensitivity: unknown`, lacks source-path authorization, or lacks required
  redaction records

**Last artifact path pattern:** `evidence/redacted/evidence-manifest.yaml`

**Capability scoping:** Evidence intake typically runs **before** a `CAP-*`
is scoped (capability seeds only emerge during module analysis). Two cases:

- If `current_focus.capability_id` is set, write the `capabilities[]` entry
  for that CAP-* with `stage_id: "1 Evidence Ready"` and your manifest path.
- If `current_focus.capability_id` is `null`, **append `history[]` only**
  with `capability_id: null` — do not invent a CAP-*. The orchestrator will
  scope a capability later.

**Writes per run:**

1. (When CAP-* is scoped) Overwrite `capabilities[<CAP-*>]` with stage id,
   artifact path, `last_skill: legacy-ibmi-evidence-intake`, and blocking
   IDs (any unauthorized unredacted production evidence remains a
   `gates: ["redaction"]` blocker).
2. Append one `history[]` entry — always.
3. Overwrite `project.last_updated_at` / `project.last_updated_by` — always.

Never touch `current_focus`, other capabilities' entries, or past
`history[]` rows. Evidence Authorization Gate failure is recorded in
`blocking.gates`, not silently — the orchestrator refuses to advance until that
list is empty.

## Adversarial Cases

### Incomplete Evidence

If evidence is incomplete (e.g., "DSPF expected but not provided"):

- Document the gap as `TBD-<SLUG>-NNN`.
- Assess impact: blocking vs. informational.
- Mark the related `unresolved_items` row with `blocks_inventory: true` if
  inventory cannot proceed.
- Plan collection as a follow-up.
- Do NOT invent missing evidence.

### Contradictory Evidence

If two sources disagree (e.g., job log shows one transaction but source shows
different logic):

- Document both versions in the manifest.
- Add a note: "Conflict: source logic vs. runtime evidence".
- Create a `TBD-<SLUG>-NNN` requiring SME resolution.
- Do NOT choose one over the other without SME approval.

### Unclear Sensitivity

If an evidence item's sensitivity status cannot be determined:

- Mark as `sensitivity: unknown`.
- Flag for SME review before redaction.
- Do NOT assume it is safe to redact.
- Do NOT assume it is safe to commit unredacted.

### Over-Redaction

If redaction removes business-critical information (e.g., all amounts redacted,
making business logic unanalyzable):

- SME rejects the redaction.
- Work with redaction owner to find a middle ground (e.g., redact some amounts,
  preserve others for calculation integrity).
- Re-execute redaction.
- SME re-reviews.

### Missing Reviewer, Redaction Owner, or SME

If no one is available to approve the Step 0 intake decision:

- Do not proceed.
- Escalate to project sponsor or data owner.
- Evidence must not be used without accountability.

If no SME is known yet but the item is source code or metadata provided by path
inside the isolated company environment, do not block inventory solely for
missing SME. Record `sme_required: false` or a non-blocking `TBD-*` for later
business validation.

## Success Criteria

- ✅ All evidence items have been typed and assessed for sensitivity.
- ✅ Each item has a unique `EV-<SLUG>-NNN` ID.
- ✅ Source-path authorization or redaction plan has been created and approved
  by the responsible reviewer.
- ✅ Required redaction has been executed, logged, and spot-checked.
- ✅ Reviewer has checked data integrity and completeness.
- ✅ SME has approved only items where `sme_required: true`; otherwise SME
  review may be deferred to later analysis stages.
- ✅ Evidence manifest lists all items with status and approvals.
- ✅ Approved handoff manifest has `package_state: approved_for_inventory` and
  `intake_decision.status` of `pass` or `pass_with_warnings`.
- ✅ Redaction log documents every change.
- ✅ Any gaps or contradictions are documented as `TBD-<SLUG>-NNN`.
- ✅ Redacted evidence is organized and ready for downstream skills.

## Next Steps

Once evidence intake is complete and SME-approved:

1. Use `legacy-ibmi-inventory` to analyze and catalog the evidence.
2. Reference evidence IDs (`EV-CREDIT-CHECK-001`, etc.) in all downstream
   analyses.
3. Link business rules, behaviors, and decisions to evidence IDs in
   `spec.yaml`.
4. If new evidence is discovered later, follow the same intake workflow and
   append to the manifest.

## References

- `references/evidence-types.md` — Detailed evidence type definitions
- `references/redaction-checklist.md` — Master redaction checklist and patterns
- `references/output-contract.md` — Evidence ID and manifest field definitions
- `../../../docs/legacy-spec-factory/data-collection-and-redaction.md` — Organization-level policy
- `../../../docs/legacy-spec-factory/id-conventions.md` — ID format rules
- `../../../docs/legacy-spec-factory/evidence-and-knowledge-taxonomy.md` — Evidence strength and
  knowledge type framework

## Examples

- `examples/customer-credit-intake/` — Worked example: collecting RPGLE,
  DSPF, job log, and transaction samples for a credit-check capability
- `examples/inventory-system-partial-intake/` — Negative case: incomplete
  evidence with documented gaps and redaction challenges
