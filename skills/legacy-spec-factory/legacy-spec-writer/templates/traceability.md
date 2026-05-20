# Traceability: SPEC-<CAP-SLUG>-001

Cross-reference report. Every approved Business Rule must trace to at
least one Evidence item and at least one Acceptance Criterion.

## BR → EV / BEH / AC / TC Walk

### BR-<CAP-SLUG>-001 — <Rule summary> (review_status)
- **Supporting Evidence:**
  - EV-<CAP-SLUG>-001 (<Source description>) — `<evidence_strength>`
  - EV-<CAP-SLUG>-NNN (<Source description>) — `<evidence_strength>`
- **Linked Behaviors:**
  - BEH-<CAP-SLUG>-001 (<What the legacy does>)
- **Validating Acceptance Criteria:**
  - AC-<CAP-SLUG>-001 (<Scenario>)
- **Tests (sketch):** TC pending; will be implemented per spec.tests
- **Verdict:** ✅ approvable — confirmed evidence + AC / ⏸ on hold — <reason> / ❌ blocked — <reason>

### BR-<CAP-SLUG>-NNN — <Rule summary> (review_status)
- **Supporting Evidence:**
  - EV-<CAP-SLUG>-NNN
- **Linked Behaviors:**
  - BEH-<CAP-SLUG>-NNN
- **Validating Acceptance Criteria:**
  - AC-<CAP-SLUG>-NNN or none yet (if draft/needs_sme_review)
- **Blocking TBDs:**
  - TBD-<CAP-SLUG>-NNN (<Unresolved issue>)
- **Verdict:** ✅ / ⏸ / ❌ <reason>

## DEC Walk

### DEC-<CAP-SLUG>-001 — <Decision summary> (review_status)
- **Rationale ties to:** BR-<CAP-SLUG>-NNN (<Business driver>)
- **Reviewer pending:** <Role> (<Expert name>)
- **Blocking TBD:** TBD-<CAP-SLUG>-NNN if any

## Evidence Coverage Audit

| EV ID | Used By | Strength |
| --- | --- | --- |
| EV-<CAP-SLUG>-001 | BR-001, BEH-001, STEP-001 | confirmed_from_code |
| EV-<CAP-SLUG>-NNN | BR-NNN, IN-NNN, data_model | <evidence_strength> |

✅ No orphan evidence; every EV referenced by ≥1 spec element.

## AC Coverage Audit

| AC ID | Validates | BR Status |
| --- | --- | --- |
| AC-<CAP-SLUG>-001 | BR-<CAP-SLUG>-001 | approved |

✅ No orphan ACs; every AC validates approved BRs only.

## BR → AC Coverage Audit

| BR ID | Has ≥1 AC? | Status OK? |
| --- | --- | --- |
| BR-<CAP-SLUG>-001 | ✅ AC-001 | approved + AC = OK |
| BR-<CAP-SLUG>-NNN | ❌ | draft / needs_sme_review → AC not required yet |

✅ Every approved BR has at least one AC.

## Forward-Handoff Gate Verdict

To reach `status: approved`:

- [X] Every approved BR has ≥1 confirmed-strength evidence
- [X] Every approved BR has ≥1 approved AC
- [X] Every approved AC validates an approved BR
- [X] No `blocking: yes` TBD without SME waiver
- [X] No `evidence_strength: missing` in data model fields
- [X] Capability owner SME signed off

**Verdict:** ✅ ready for `approved` / ⏸ blocked on <TBD-ID> / ❌ cannot proceed — <reason>

Next action: <Clarify unresolved TBD> / <Promote to approved> / <Route to [skill]>
