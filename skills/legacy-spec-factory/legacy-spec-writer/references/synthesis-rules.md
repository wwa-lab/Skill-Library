# Spec Synthesis Rules

How each `spec.yaml` field is derived from upstream analyses.

The authoritative format is `../../../schemas/spec.schema.yaml`. This file
tells you **where each value comes from**.

---

## Field Sources

| spec.yaml field | Source | Rule |
| --- | --- | --- |
| `schema_version` | constant | `"0.1"` |
| `spec_id` | new ID | `SPEC-<CAP-SLUG>-<NNN>` |
| `capability.id/name/slug/owner` | module overview Capability Seeds + SME | direct copy after SME confirmation |
| `status` | workflow state | starts `draft`; → `in_review` after self-check; → `approved` after SME sign-off |
| `source_system` | inventory.yaml | copy `name`, `libraries`, `collection_date` |
| `target_platform` | SME / platform hint | architecture string + service hint |
| `business_goal` | approved BRD section 1, cross-checked against module View 1 Business Scope | one-sentence summary |
| `scope.in_scope` / `scope.out_of_scope` | approved BRD section 1 + SME + module overview Scope Statement | per-capability narrowing of module scope |
| `evidence[]` | every EV-* referenced by any in-scope flow / program analysis and approved BRD traceability | one row per EV; never inline raw sensitive data |
| `observed_behaviors[]` | flow analyses' control flow + program analyses' behaviors | factual: what the legacy does |
| `business_rules[]` | module View 1 BR seeds + SME confirmation | one BR per confirmed candidate |
| `modernization_decisions[]` | derived from BRs + target_platform constraints + SME | each DEC has rationale |
| `data_model.entities[]` | module View 4 (Data Flow) | each major PF/LF/SQL table that the target system will own |
| `data_model.entities[].fields[]` | DDS / SQL definitions + cross-program references | type maps to target type per platform |
| `process_flow.steps[]` | approved BRD section 6 + business-visible phases and outcomes from the relevant flow analysis; Transaction Call Map is supporting evidence | one STEP per business step, not one STEP per program node |
| `inputs[]` | approved BRD sections 3-5 + flow analysis Trigger Context + UI surfaces input fields | source = api/screen/batch/file/integration/manual |
| `outputs[]` | approved BRD sections 4-5 + flow analysis exit nodes + Cross-Program Data Flow carriers with external handoff / creates / updates state impact | target = api_response/event/database/report/spool/file/integration |
| `exceptions[]` | approved BRD section 8 + flow analysis Error Propagation + program analyses Error Handling | each EX has severity |
| `acceptance_criteria[]` | each approved BR → ≥1 AC | Gherkin preferred for procedural; checklist for declarative |
| `tests[]` | optional sketch only; defers to future equivalence-test skill | TC-* IDs only |
| `open_questions[]` | every unresolved TBD-* from upstream analyses, approved BRD section coverage decisions, and new TBDs from synthesis | preserve `blocking` status |
| `traceability[]` | computed by walking BR → EV / AC / TC links | every approved BR must trace to ≥1 EV and ≥1 AC |

---

## Required Approved BRD Package

In the standard workflow, `05_brds/<CAPABILITY-SLUG>/` must exist and be
approved before spec writing. Treat it as reviewed business context, not as a
replacement for upstream evidence. The BRD's SME-required functional areas map
into the spec as follows:

- BRD section 3 Channels and section 4 User Interface / User Touchpoints feed
  `inputs[]`, `outputs[]`, and user-visible exception context.
- BRD section 5 System Interfaces feeds `inputs[]`, `outputs[]`, and
  integration-related `open_questions[]`; it does not create architecture
  decisions unless a `DEC-*` is separately approved.
- BRD section 6 Process Flow frames `process_flow.steps[]` in business language.
- BRD section 8 Error Handling feeds `exceptions[]`.
- BRD section 9 Dependencies feeds `open_questions[]`, data model context, or
  implementation constraints only when backed by `EV-*` / SME evidence.
- BRD optional section 10 Security / Authentication may inform `inputs[]`,
  `exceptions[]`, or `modernization_decisions[]` only when the requirement is
  evidence-backed and SME-approved.

If `review-decision.yaml.functional_analysis_coverage[]` marks a required BRD
section as `accepted_with_tbd`, carry the named `TBD-*` into
`open_questions[]`. If a section is `blocked` or `needs_more_evidence`, the
spec must not move to `approved`.

## Aggregation Rules (Across Multiple Flows)

A single capability often spans multiple flows. E.g., "Credit Limit
Enforcement" appears in `FLOW-ONUS-AUTH` (online) and `FLOW-MANUAL-AUTH`
(manual). Synthesis rules:

1. **Union, deduplicated by stable ID** — same BR-* in two flow seeds →
   one BR in the spec, both flows' EV-* listed.
2. **BEH consolidation** — if two flows show the same behavior (e.g.,
   "credit limit checked against CREDFILE.CREDLIMIT"), one BEH covers
   both; `evidence_ids` includes both occurrences.
3. **Conflicting behaviors** — if two flows do the same thing differently
   (e.g., online checks before lookup, manual checks after lookup),
   capture both as separate BEHs and create a TBD asking SME whether
   the divergence is intentional.

## Deriving Decisions (DEC-*)

A modernization decision must answer one of:

- **Architecture:** what target component owns this capability?
- **Data:** is the target data model a copy, a transformation, or a new design?
- **API surface:** how does the modernized capability expose itself?
- **Error handling:** does target use exceptions, return codes, or events?
- **Async boundaries:** preserved from legacy, or restructured?
- **Compatibility:** does the target maintain legacy data formats?

Each DEC's `rationale` must reference:
- The BR(s) it serves, OR
- The BEH(s) it preserves or replaces, OR
- A `target_platform` constraint (e.g., "Java/Spring requires JPA entity")

DECs with rationale "because that's how the legacy did it" need stronger
justification or should be marked `needs_sme_review`.

## Acceptance Criteria Patterns

For each approved BR, produce ≥1 AC. Patterns:

### Gherkin (procedural rule)

```yaml
acceptance_criteria:
  - id: AC-CARD-AUTH-CREDLIM-001
    format: gherkin
    text: |
      Given an active customer with credit limit 50000
      And a pending authorization request for amount 60000
      When the system processes the authorization request
      Then the authorization is declined
      And the response code is "INSUFFICIENT_CREDIT"
      And an audit row is written with decision="DECLINED"
    validates:
      - BR-CARD-AUTH-CREDLIM-001
```

### Checklist (declarative rule)

```yaml
acceptance_criteria:
  - id: AC-CARD-AUTH-CREDLIM-002
    format: checklist
    text: |
      - [ ] Credit limit is read from authoritative source (CUSTOMER-MASTER module)
      - [ ] Stale credit-limit cache is acceptable up to 5 minutes
      - [ ] Limit changes propagate within one transaction cycle
    validates:
      - BR-CARD-AUTH-CREDLIM-001
```

## Traceability Generation

`traceability.md` is generated by walking the spec:

```
For each approved BR:
  list supporting EVs (evidence_ids)
  list validating ACs (where AC.validates contains this BR)
  list test cases (TC.validates contains this BR) if any
For each approved AC:
  list the BR it validates
For each EV:
  list the BR(s) / BEH(s) that reference it
```

A BR with no AC → spec is incomplete (cannot be `approved`).
An AC with no approved BR → orphan; remove or flag.
An EV with no BR / BEH reference → unused evidence; remove or move to TBD.

## Forward-Handoff Gate

Before `status` can become `approved`, all of the following must be true:

1. Every BR with `review_status: approved` has at least one EV with
   evidence_strength `confirmed_from_code`, `observed_in_runtime`,
   `confirmed_by_sme`, or `strongly_inferred` (+ explicit SME approval).
2. Every approved BR has ≥1 approved AC.
3. Every approved AC `validates` exactly approved BRs (no orphans, no
   pointing to draft BRs).
4. Every `blocking: yes` TBD is resolved or explicitly waived by SME.
5. The data model has no field with `evidence_strength: missing` unless
   that field is also flagged as a TBD with SME ownership.
6. The capability owner SME has signed off.

The `docs/forward-sdlc-contract.md` document describes the contract to
`build-agent-skill`; this skill must satisfy it before handing off.
