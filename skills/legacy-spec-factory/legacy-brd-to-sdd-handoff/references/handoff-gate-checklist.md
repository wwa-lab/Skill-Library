# Handoff Gate Checklist

This document details the validation rules for each gate in the SDD handoff process.

## Gate 1: BRD Status and Sign-Off Validation

### Input Checks
- [ ] File `05_brds/<CAPABILITY-SLUG>/brd.md` exists and is readable
- [ ] File `05_brds/<CAPABILITY-SLUG>/brd-review.md` exists and is readable
- [ ] BRD YAML/Markdown frontmatter includes `status` field

### Status Validation
- [ ] BRD `status` is exactly `approved` (not draft, needs_review, etc.)
- [ ] If status is lower, **stop and route back to `legacy-brd-writer` or for SME review**

### Sign-Off Validation
- [ ] `brd-review.md` contains an SME sign-off block with:
  - [ ] `sme_owner` — name of the SME (required)
  - [ ] `sme_role` — job title or business role (required; e.g., "Credit Policy Manager")
  - [ ] `approved_date` — ISO 8601 date (required; e.g., "2026-05-15")
  - [ ] `approval_notes` or `signature` — optional but recommended
- [ ] Sign-off fields are present and non-empty
- [ ] Sign-off date is recent (within the last 30 days; warn if older)

### Finding Rules
- **Pass**: All fields present and non-empty, status is approved
- **Fail**: Any field missing → **Finding: BRD-SIGN-OFF-INCOMPLETE (blocking)**
- **Warn**: Sign-off date is > 30 days old → **Finding: BRD-STALE-APPROVAL (info)**

---

## Gate 2: Spec Status and Sign-Off Validation

### Input Checks
- [ ] File `05_specs/<CAPABILITY-SLUG>/spec.yaml` exists and is readable
- [ ] File `05_specs/<CAPABILITY-SLUG>/spec-review.md` exists and is readable
- [ ] Spec YAML includes `status` field

### Status Validation
- [ ] Spec `status` is exactly `approved` (not draft, in_review, etc.)
- [ ] If status is lower, **stop and route back to `legacy-spec-writer` or for review**

### Sign-Off Validation
- [ ] `spec-review.md` contains an SME sign-off block with:
  - [ ] `sme_owner` — name of the SME (required)
  - [ ] `sme_role` — job title (required)
  - [ ] `approved_date` — ISO 8601 date (required)
  - [ ] `approval_checklist` with:
    - [ ] `business_rules_approved: true`
    - [ ] `acceptance_criteria_approved: true`
    - [ ] `modernization_decisions_approved: true`
- [ ] All three approval items are set to `true`

### Finding Rules
- **Pass**: All fields present, status approved, all three approvals are true
- **Fail**: Status not approved OR any approval is false or missing → **Finding: SPEC-NOT-FULLY-APPROVED (blocking)**
- **Fail**: Sign-off incomplete → **Finding: SPEC-SIGN-OFF-INCOMPLETE (blocking)**
- **Warn**: Sign-off date is > 30 days old → **Finding: SPEC-STALE-APPROVAL (info)**

---

## Gate 3: Blocking TBD Validation

### Input Checks
- [ ] Spec `spec.yaml` contains `open_questions[]` or `tbd[]` array
- [ ] Each TBD record has `id`, `question`, `blocking`, and `resolution` fields

### TBD Analysis
For each TBD record:
- [ ] Check `blocking` field value (true or false)
- [ ] Check `resolution` field:
  - If resolution is a real action or deferral: note it
  - If resolution is "pending" or empty: check blocking status
- [ ] **If `blocking: true` AND `resolution: pending`**:
  - **Finding: BLOCKING-TBD-UNRESOLVED (blocking)**
  - List the TBD ID and question
  - **Stop handoff**
- [ ] **If `blocking: true` AND `resolution: <something>`** (deferred or resolved):
  - **Finding: BLOCKING-TBD-DEFERRED (warning)**
  - Note the deferral in handoff findings
  - **Continue handoff**
- [ ] **If `blocking: false`**:
  - **Finding: NON-BLOCKING-TBD (info)**
  - Carry forward into handoff package
  - **Continue handoff**

### Finding Rules
- **Pass**: No blocking TBDs with pending resolution
- **Warn**: Blocking TBDs deferred with clear resolver and date
- **Fail**: Any blocking TBD with resolution=pending → **stop handoff**

---

## Gate 4: Business Rules Have Acceptance Criteria

### Input Checks
- [ ] Spec `spec.yaml` contains `business_rules[]` array
- [ ] Each business rule has `id`, `statement`, and `acceptance_criteria_ids[]` fields

### Rule Analysis
For each business rule where `review_status: approved`:
- [ ] Check `acceptance_criteria_ids[]` array
- [ ] **If array exists and is non-empty**:
  - **Finding: BR-HAS-AC (pass)**
  - Verify each AC-* ID exists in the spec
  - **Continue**
- [ ] **If array is empty, null, or missing**:
  - **Finding: BR-MISSING-AC (blocking)**
  - List the rule ID and title
  - **Stop handoff**

### Finding Rules
- **Pass**: All approved BR-* have non-empty `acceptance_criteria_ids[]`
- **Fail**: Any approved BR-* lacks AC-* records → **stop handoff; return to spec writer**

---

## Gate 5: Acceptance Criteria Are Approved

### Input Checks
- [ ] Spec `spec.yaml` contains `acceptance_criteria[]` array
- [ ] Each AC record has `id`, `criterion`, and `review_status` fields

### AC Analysis
For each acceptance criterion linked from Gate 4:
- [ ] Check `review_status` field
- [ ] **If `review_status: approved`**:
  - **Finding: AC-APPROVED (pass)**
  - **Continue**
- [ ] **If `review_status: draft` or `needs_sme_review`**:
  - **Finding: AC-NOT-APPROVED (blocking)**
  - **Stop handoff** unless `spec-review.md` contains an explicit named SME
    waiver for this exact `AC-*` with reason and date
  - If waived, record the waiver in `findings.warnings` and continue with
    `approved_with_non_blocking_tbd`
- [ ] **If `review_status: rejected`**:
  - **Finding: AC-REJECTED-BUT-LINKED (blocking)**
  - **Stop handoff**; route to `legacy-spec-writer`

### Finding Rules
- **Pass**: All linked AC-* have `review_status: approved`
- **Warn**: A linked AC-* is not approved only when an explicit named SME
  waiver is present in `spec-review.md`
- **Fail**: Any linked AC-* is draft, needs SME review, rejected, or missing
  without an explicit waiver → **stop handoff; escalate to SME or
  `legacy-spec-writer`**

---

## Gate 6: Evidence Sensitivity Check

### Input Checks
- [ ] Spec `spec.yaml` contains `evidence_ids[]` or `evidence[]` array
- [ ] An evidence manifest from `legacy-ibmi-evidence-intake` exists
      (typically `evidence/manifest.yaml`)
- [ ] Manifest has `package_state: approved_for_inventory`
- [ ] Manifest `intake_decision.downstream_inventory_allowed` is `true`
- [ ] Each referenced evidence record is found by
      `evidence_items[].evidence_id`
- [ ] Each referenced evidence record has `sensitivity`,
      `redaction_status`, `redacted_filename` / approved analysis path,
      `source_path_verified`, `redaction_required`, `sme_required`, and
      `sme_approval`

### Evidence Analysis
For each evidence ID referenced in the spec:
- [ ] Look up the evidence record in `evidence_items[].evidence_id`
- [ ] Check the manifest's authorization and redaction fields:
  - [ ] **If `redaction_required: false`, `source_path_verified: true`, and
        `redaction_status` is `not_required`, `reviewed`, or `approved`**:
    - **Finding: EVIDENCE-SOURCE-AUTHORIZED (pass)**
    - **Continue**
  - [ ] **If `redaction_required: true` AND `redaction_status: approved`**:
    - **Finding: EVIDENCE-REDACTED (pass)**
    - Note in handoff that evidence is sanitized
    - **Continue**
  - [ ] **If `redaction_required: true` AND `redaction_status` is not
        `approved`**:
    - **Finding: EVIDENCE-AWAITING-REDACTION (blocking)**
    - List the evidence ID
    - **Stop handoff; escalate to evidence intake**
  - [ ] **If `redaction_required: false` AND `source_path_verified` is not
        `true`**:
    - **Finding: EVIDENCE-SOURCE-NOT-AUTHORIZED (blocking)**
    - **Stop handoff; escalate to evidence intake**
  - [ ] **If `sensitivity: unknown`**:
    - **Finding: EVIDENCE-SENSITIVITY-UNKNOWN (blocking)**
    - List the evidence ID
    - **Stop handoff; escalate to evidence intake for review**
  - [ ] **If `redacted_filename` / approved analysis path is missing/null**:
    - **Finding: EVIDENCE-APPROVED-PATH-MISSING** (blocking)
    - **Stop handoff; escalate to evidence intake**
  - [ ] **If `sme_required: true` and `sme_approval` is not true**:
    - **Finding: EVIDENCE-SME-APPROVAL-MISSING** (blocking)
    - **Stop handoff; escalate to evidence intake**

### Finding Rules
- **Pass**: All referenced evidence satisfies the
  `legacy-ibmi-evidence-intake` approved-manifest contract
- **Fail**: Manifest not approved, evidence ID missing, `sensitivity:
  unknown`, source path not authorized, required redaction not approved,
  approved analysis path missing, or required SME approval missing → **stop
  handoff; escalate**

---

## Gate 7: Traceability Matrix Completeness

### Input Checks
- [ ] Spec contains or references a traceability matrix (or can be generated)
- [ ] Matrix includes evidence, rules, acceptance criteria, and test case mappings

### Traceability Analysis
- [ ] For each evidence ID (`EV-*`):
  - [ ] Is it linked to at least one business rule or behavior (`BR-*` or `BEH-*`)?
  - [ ] If not: **Finding: ORPHANED-EVIDENCE (warning)**; blocks final
        status unless an explicit SME waiver is recorded
- [ ] For each business rule (`BR-*`):
  - [ ] Is it linked to at least one evidence item?
  - [ ] Is it linked to at least one acceptance criterion?
  - [ ] If no evidence: **Finding: BR-NO-EVIDENCE (blocking)**
  - [ ] If no acceptance criterion: **Finding: BR-MISSING-AC (blocking)**
- [ ] For each acceptance criterion (`AC-*`):
  - [ ] Is it linked back to a business rule?
  - [ ] If not: **Finding: AC-DANGLING-RULE-REF (blocking)**
- [ ] For each test case (`TC-*`):
  - [ ] Is it linked to at least one acceptance criterion?
  - [ ] If not: **Finding: ORPHANED-TEST (info)**

### Finding Rules
- **Pass**: No orphaned IDs; all cross-references are valid
- **Warn**: Orphaned evidence → **note in findings; requires SME waiver to
  pass with warnings**
- **Info**: Orphaned test cases → **note but not blocking**
- **Fail**: Any approved BR lacks evidence or AC, or any AC points to a
  missing BR → **stop handoff; route to `legacy-spec-writer`**

---

## Summary

### Blocking Gates (Stop if failed)
1. BRD not approved or missing sign-off
2. Spec not approved or missing sign-off
3. Blocking TBD unresolved
4. Approved BR missing AC-*
5. Evidence sensitivity unknown or awaiting redaction

### Warning Gates (Continue but note)
- BRD or Spec approval > 30 days old
- Some AC-* not approved (may need SME escalation)
- Blocking TBDs deferred (non-blocking deferral is OK)
- Orphaned evidence or rules (traceability incomplete)

### Info Gates (Log but non-blocking)
- Orphaned test cases or ACs
- Non-blocking TBDs
- Tech-debt or implementation notes

---

## Testing the Gate Checklist

Before declaring a handoff ready, verify:

- [ ] All blocking gates have green status
- [ ] All warning gates have been reviewed and noted
- [ ] All findings have been categorized and reported
- [ ] SME sign-off is present on the handoff itself
- [ ] Handoff package is complete and valid
