<!--
Legacy Spec Factory
Copyright 2026 Leo L Zhang
License: Apache License 2.0
-->

# Handoff Workflow — 9 Ordered Steps

This document is the executable procedure for `legacy-brd-to-sdd-handoff`. It
is referenced from `SKILL.md` and from `references/handoff-gate-checklist.md`.

The workflow is **block-by-default**. Each step ends either in `pass` or in a
blocking finding. A blocking finding stops the entire workflow; partial
packages are not written.

---

## Step 1 — Validate BRD Status and Sign-Off

1. Confirm `05_brds/<CAPABILITY-SLUG>/brd.md` exists and is readable.
2. Confirm BRD frontmatter / metadata has `status: approved`.
3. Confirm `05_brds/<CAPABILITY-SLUG>/brd-review.md` contains an SME sign-off
   block with **all** of:
   - `sme_owner` (non-empty)
   - `sme_role` (non-empty)
   - `approved_date` (ISO 8601, non-empty)

Findings:

| Condition | Finding | Severity | Action |
| --- | --- | --- | --- |
| any field missing or empty | `BRD-SIGN-OFF-INCOMPLETE` | blocking | route to `legacy-brd-writer` |
| BRD status below `approved` | `BRD-NOT-APPROVED` | blocking | route to `legacy-brd-writer` |
| BRD owner ≠ spec owner | `SME-OWNERSHIP-MISMATCH` | info | record only |

---

## Step 2 — Validate Spec Status and Sign-Off

1. Confirm `05_specs/<CAPABILITY-SLUG>/spec.yaml` exists and is readable.
2. Confirm `status: approved`.
3. Confirm `05_specs/<CAPABILITY-SLUG>/spec-review.md` contains an SME sign-off
   block with `sme_owner`, `sme_role`, `approved_date`.
4. Confirm spec approval flags are all `true`:
   - `business_rules_approved`
   - `acceptance_criteria_approved`
   - `modernization_decisions_approved`

Findings:

| Condition | Finding | Severity | Action |
| --- | --- | --- | --- |
| spec file missing | `SPEC-MISSING` | blocking | route to `legacy-spec-writer`; **never substitute the BRD** |
| spec status below `approved` | `SPEC-NOT-APPROVED` | blocking | route to `legacy-spec-writer` |
| any approval flag `false` or missing | `SPEC-PARTIAL-APPROVAL` | blocking | route to `legacy-spec-writer` |
| sign-off fields missing | `SPEC-SIGN-OFF-INCOMPLETE` | blocking | request SME sign-off |

**Bypass rule**: under no circumstances does this skill generate a spec or
infer spec content. `legacy-spec-writer` is the only authorised producer of
`spec.yaml`. If the spec is absent, the handoff is blocked.

---

## Step 3 — Check for Blocking TBDs

1. Parse `spec.yaml` and extract all `TBD-*` records.
2. For each TBD evaluate the **deferral predicate** below before deciding
   severity.

### The Deferral Predicate

A TBD with `blocking: true` is treated as a **warning** (not a blocker)
only when **every** condition below is satisfied. If any condition is
missing, the TBD falls through to `BLOCKING-TBD-UNRESOLVED` (blocking).

| Field on the TBD       | Requirement |
| ---                    | --- |
| `blocking`             | `true` (kept; SME chose not to demote) |
| `resolution`           | non-empty string that names the SME and the deferral target (phase, milestone, or date) |
| `resolver`             | non-empty; must name a real person from the spec's SME roster |
| `planned_resolution_date` | a future ISO 8601 date |
| `deferral_recorded_in` (optional but expected) | a pointer such as `spec-review.md#sme-decisions` proving the deferral was logged at review time |

This predicate exists to prevent the two opposite mistakes the gate must
avoid:

- **Over-blocking**: penalising teams that responsibly defer with a named
  SME and date.
- **Under-warning**: hiding a known-incomplete decision behind a cosmetic
  resolution string. Anything weaker than the four-field predicate above
  is cosmetic and the gate must reject it.

### Severity Table

| `blocking` | Deferral predicate satisfied? | Finding | Severity | Action |
| --- | --- | --- | --- | --- |
| `true` | n/a, `resolution` unset / `pending` | `BLOCKING-TBD-UNRESOLVED` | **blocking** | escalate to SME; route to `legacy-spec-writer` |
| `true` | predicate satisfied | `BLOCKING-TBD-DEFERRED` | warning | carry forward verbatim; status becomes `approved_with_non_blocking_tbd` |
| `true` | partially satisfied (e.g. resolver missing) | `BLOCKING-TBD-UNRESOLVED` | **blocking** | escalate to SME — do not silently upgrade a half-deferral to a warning |
| `false` | n/a | `NON-BLOCKING-TBD` | info | carry forward verbatim; status becomes `approved_with_non_blocking_tbd` |

### Carry-Forward Discipline

All TBDs that survive Step 3 (warnings and info alike) flow into
`sdd-handoff.yaml.open_questions[]` and into
`atlas-context-pack.json.open_questions[]`, **verbatim**. The handoff
never:

- edits the TBD wording
- paraphrases the resolution text
- compresses multiple TBDs into one
- demotes `BLOCKING-TBD-DEFERRED` to `NON-BLOCKING-TBD` in the package
  (the finding severity is preserved so downstream Atlas tools can tell
  the two apart)

See `examples/handoff-warning-deferred-tbd/` for a worked
`BLOCKING-TBD-DEFERRED` case and `examples/handoff-blocked-blocking-tbd/`
for a worked `BLOCKING-TBD-UNRESOLVED` case using the same TBD shape.

---

## Step 4 — Every Approved BR has at Least One AC

1. Extract `business_rules[]` from `spec.yaml`.
2. For each rule where `review_status: approved`:
   - if `acceptance_criteria_ids[]` is non-empty and all referenced `AC-*`
     records exist → `BR-HAS-AC` (pass)
   - if empty / missing → `BR-MISSING-AC` (blocking); route to
     `legacy-spec-writer`
   - if a referenced `AC-*` ID does not resolve in the spec →
     `BR-AC-DANGLING-REFERENCE` (blocking); route to `legacy-spec-writer`

The handoff is never advanced with an approved rule that lacks acceptance
criteria. The skill must not invent the missing AC.

---

## Step 5 — Acceptance Criteria are Approved

For each `AC-*` referenced from an approved `BR-*`:

| `review_status` | Finding | Severity |
| --- | --- | --- |
| `approved` | `AC-APPROVED` | pass |
| `needs_sme_review` or `draft` | `AC-NOT-APPROVED` | blocking unless `spec-review.md` records an explicit SME waiver for this AC |
| `rejected` | `AC-REJECTED-BUT-LINKED` | blocking — spec contradiction |

A waiver must be a named SME entry in `spec-review.md` quoting the AC ID and
reason. The handoff records the waiver in `findings.warnings` and continues.

---

## Step 6 — Evidence Sensitivity Check

1. Union of `evidence_ids[]` referenced by BRD and spec.
2. For each `EV-*`, look it up in the evidence manifest produced by
   `legacy-ibmi-evidence-intake` (typically `evidence/manifest.yaml`).
3. Use the canonical manifest fields:
   - `evidence_items[].evidence_id`
   - `evidence_items[].sensitivity`
   - `evidence_items[].redaction_status`
   - `evidence_items[].redacted_filename`
   - `evidence_items[].source_path_verified`
   - `evidence_items[].redaction_required`
   - `evidence_items[].sme_required`
   - `evidence_items[].sme_approval`

The handoff gate consumes the evidence manifest contract, not an ad-hoc
`sensitive: true/false` shorthand. `spec.yaml.evidence[].sensitive` may still
exist as source-spec metadata, but the manifest is the redaction source of
truth for handoff.

| Manifest condition | Finding | Severity | Action |
| --- | --- | --- | --- |
| `package_state` is not `approved_for_inventory` or `intake_decision.downstream_inventory_allowed` is not `true` | `EVIDENCE-PACKAGE-NOT-APPROVED` | blocking | route to `legacy-ibmi-evidence-intake` |
| referenced `EV-*` not found in `evidence_items[].evidence_id` | `EVIDENCE-MANIFEST-MISS` | blocking | repair upstream manifest |
| `sensitivity: unknown` | `EVIDENCE-SENSITIVITY-UNKNOWN` | blocking | route to `legacy-ibmi-evidence-intake` |
| `redaction_required: true` and `redaction_status: approved` | `EVIDENCE-REDACTED` | pass | continue |
| `redaction_required: true` and `redaction_status` is anything else | `EVIDENCE-AWAITING-REDACTION` | blocking | route to `legacy-ibmi-evidence-intake` |
| `redaction_required: false` and `source_path_verified: true` and `redaction_status: not_required` or `reviewed` or `approved` | `EVIDENCE-SOURCE-AUTHORIZED` | pass | continue |
| `redaction_required: false` and `source_path_verified` is not `true` | `EVIDENCE-SOURCE-NOT-AUTHORIZED` | blocking | route to `legacy-ibmi-evidence-intake` |
| `redacted_filename` missing or null | `EVIDENCE-APPROVED-PATH-MISSING` | blocking | route to `legacy-ibmi-evidence-intake` |
| `sme_required: true` and `sme_approval` is not `true` | `EVIDENCE-SME-APPROVAL-MISSING` | blocking | request evidence SME approval |

`sensitivity: unknown` is **always** blocking. The handoff never assumes a
default sensitivity. SME approval is required only when the evidence manifest
marks `sme_required: true`; internal source-review evidence with
`sme_required: false` must not be blocked for missing SME approval.

---

## Step 7 — Traceability Completeness

Build the matrix from spec records (do not re-derive from raw source):

- every `EV-*` references at least one `BEH-*` or `BR-*`
- every approved `BR-*` references at least one `EV-*` and at least one
  `AC-*`
- every `AC-*` references exactly one `BR-*`
- every `TC-*` (if test cases exist in the spec) references at least one
  `AC-*` or `BR-*`
- every `DEC-*` carries a rationale that names a `BR-*`, `BEH-*`, or
  explicit platform / regulatory constraint

Findings:

| Condition | Finding | Severity |
| --- | --- | --- |
| any `EV-*` not linked to a `BEH-*` or `BR-*` | `ORPHANED-EVIDENCE` | warning; final status blocks unless explicitly SME-waived |
| any approved `BR-*` not linked to any `EV-*` | `BR-NO-EVIDENCE` | blocking |
| any `AC-*` whose `rule_id` is not in `business_rules[]` | `AC-DANGLING-RULE-REF` | blocking |
| any `DEC-*` with no rationale | `DEC-NO-RATIONALE` | warning |

---

## Step 8 — Assemble the Handoff Package

Only entered if every previous step ended in `pass`, `warning`, or
explicit SME-waived condition. Any blocking finding short-circuits to
Step 9b.

For each output file:

1. **`sdd-handoff.yaml`** — start from `templates/sdd-handoff.yaml`. Populate
   only with values pulled directly from spec / BRD / evidence manifest /
   this run's findings. Do **not** add `forward_sdlc_hints`,
   `recommended_pattern`, `target_platform`, or any field that the spec
   did not already approve as a `DEC-*`. Status:
   - `approved` if no blocking and no warning findings
   - `approved_with_non_blocking_tbd` if only `NON-BLOCKING-TBD` and/or
     `BLOCKING-TBD-DEFERRED` findings exist alongside passes
   - `blocked` if any blocking finding remains

2. **`sdd-handoff.md`** — render the executive summary from
   `templates/sdd-handoff.md`. Carry-forward sections must cite IDs;
   prose summaries must not state any architecture / framework / platform
   choice unless that choice is an approved `DEC-*`.

3. **`atlas-context-pack.json`** — agent-consumable JSON. It reshapes
   `sdd-handoff.yaml` content; it does not add fields absent from the YAML
   contract. If a summary field is useful for agents, first include that
   deterministic summary in `sdd-handoff.yaml`, then mirror it in the JSON.
   In particular, the pack must not contain `recommended_patterns`,
   `deployment_context`, examples, or integration topology unless those are
   encoded as approved `DEC-*` in the spec and present in the YAML.

4. **`handoff-review.md`** — gate checklist (one row per step above), then
   findings grouped by severity, then sign-off block.

5. **`traceability.md`** — render the matrix from Step 7. No new IDs are
   minted here.

---

## Step 9 — Sign-Off and Deliver

### 9a. Approved path

1. Populate the top-level validator fields and `sme_sign_offs[]` in
   `sdd-handoff.yaml` and `sdd-handoff.md`:
   - `handoff_validator` (e.g. `Claude Code / legacy-brd-to-sdd-handoff v0.1.0`)
   - `handoff_date` (ISO 8601, UTC)
   - `sme_sign_offs[]`: BRD approver, spec approver, and handoff approver,
     each with `name`, `role`, ISO `date`, and `approval_scope`
   - `status`: `approved` or `approved_with_non_blocking_tbd`
2. Write all five files atomically into
   `06_sdd_handoffs/<CAPABILITY-SLUG>/`.
3. Do not write a sixth runtime output file such as `gate-summary.yaml`; any
   compact summary must be derived by the orchestrator from `sdd-handoff.yaml`
   or `handoff-review.md`.
4. Notify `legacy-modernization-orchestrator` that the capability is
   ready for the Atlas SDD chain.

### 9b. Blocked path

1. Do **not** write `sdd-handoff.yaml`, `sdd-handoff.md`,
   `atlas-context-pack.json`, or `traceability.md`.
2. Write only:
   - `handoff-review.md` (gate checklist + blocking findings + required
     remediation)
   - `blocking-finding.yaml` (machine-readable findings record for the
     orchestrator)
3. Return control to the named upstream skill (`legacy-spec-writer`,
   `legacy-brd-writer`, `legacy-ibmi-evidence-intake`, or the capability
   SME) with the exact remediation quoted from the finding.

A blocked handoff is a normal outcome, not an error. The gate's job is to
fail loudly and early.

---

## Output Status Decision Table

| Findings present | Final `status` (YAML) | Display label |
| --- | --- | --- |
| only `pass` findings | `approved` | `pass` |
| `pass` + `NON-BLOCKING-TBD` and/or `BLOCKING-TBD-DEFERRED` | `approved_with_non_blocking_tbd` | `pass_with_warnings` |
| `pass` + explicitly SME-waived `AC-NOT-APPROVED` or SME-waived `ORPHANED-EVIDENCE` | `approved_with_non_blocking_tbd` | `pass_with_warnings` |
| any other warning (no explicit SME waiver) | `blocked` | `blocked` |
| any blocking finding | `blocked` | `blocked` |

The skill must not invent a fourth status. Ambiguous cases default to
`blocked`. The display labels are documented in `SKILL.md` and are
exact synonyms of the YAML values; tooling may use either.

### Worked Examples

| Example | Step that fires | Finding | Final status | Display |
| --- | --- | --- | --- | --- |
| `examples/handoff-positive/` | none beyond pass | — | `approved` | `pass` |
| `examples/handoff-warning-deferred-tbd/` | Step 3 | `BLOCKING-TBD-DEFERRED` | `approved_with_non_blocking_tbd` | `pass_with_warnings` |
| `examples/handoff-missing-spec/` | Step 2 | `SPEC-MISSING` | `blocked` | `blocked` |
| `examples/handoff-blocked-blocking-tbd/` | Step 3 | `BLOCKING-TBD-UNRESOLVED` | `blocked` | `blocked` |
| `examples/handoff-blocked-missing-ac/` | Step 4 | `BR-MISSING-AC` | `blocked` | `blocked` |
