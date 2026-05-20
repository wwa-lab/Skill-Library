# Dictionary Center Integration Contract

This document defines how Legacy Spec Factory should integrate with the
company-wide dictionary center. The dictionary center owns global field
standardization; this repository consumes those standards while recovering
evidence-backed legacy behavior and producing specs, traceability, and handoff
packages.

## Boundary

The company dictionary center is the source of truth for:

- standard business field IDs
- canonical field names and aliases
- business domains and field ownership
- customer/internal/backend visibility classification
- display, masking, precision, currency, and permission attributes
- approved field definitions and calculation-basis versions

Legacy Spec Factory is the source of truth for:

- legacy evidence intake and redaction status
- object inventory, program flow, system flow, screen/report, and runtime
  observations
- code/runtime/SME-backed behavior recovery
- observed behavior, inferred rules, modernization decisions, TBDs, and
  traceability into `spec.yaml`
- downstream handoff to the forward SDLC chain

The repository should not duplicate the dictionary center as a full-field
master-data platform.

## Input From Dictionary Center

When available, each project should import or reference a dictionary-center
field package with at least:

| Field | Required | Description |
| --- | --- | --- |
| `standard_field_id` | yes | Stable dictionary-center ID for the business field. |
| `canonical_name` | yes | Approved business field name. |
| `legacy_aliases` | no | Known DDS/DB2/API/screen/report aliases. |
| `business_domain` | yes | Business module or domain owner. |
| `field_definition` | yes | Approved business meaning or calculation-basis summary. |
| `visibility_class` | yes | `customer`, `internal_user`, `backend_only`, or `restricted`. |
| `display_policy` | no | Masking, rounding, currency, precision, locale, and formatting rules. |
| `owner` | no | Business/data owner or steward. |
| `dictionary_version` | yes | Version or effective date of the field package. |
| `status` | yes | `draft`, `approved`, `deprecated`, or `retired`. |

The package may be materialized as YAML, CSV, JSONL, or a database export. The
exact transport format is not prescribed here; the important contract is the
stable `standard_field_id`.

## Propagation Rules

When a `standard_field_id` is provided, downstream artifacts should carry it
instead of relying only on raw legacy field names.

| Artifact | Expected Behavior |
| --- | --- |
| `inventory.yaml` | May reference dictionary package metadata at project scope. |
| `data-dictionary.md` | Map DDS/DB2 fields to `standard_field_id` when evidenced or dictionary-provided. |
| `screen-report-analysis-*.md` | Attach `standard_field_id` to visible input/output fields when known. |
| `program-analysis-*.md` | Reference `standard_field_id` in field-level assignments, I/O notes, and TBDs when field identity is clear. |
| `flow-*.md` | Preserve `standard_field_id` in cross-program data flow rows when the payload contains known fields. |
| `04_modules/*/04-data-flow.md` | Use `standard_field_id` to connect data trails, object lifecycle, and cross-module dependencies. |
| `spec.yaml` | Preserve dictionary IDs in data model fields, inputs, outputs, business rules, and traceability where applicable. |
| Traceability / handoff packages | Carry dictionary IDs into downstream SDLC context packs so generated code and tests can preserve the same field identity. |

If a legacy field cannot be matched to the dictionary center, create a `TBD-*`
or finding rather than inventing a canonical field. Unknown fields should be
routed back to dictionary-center stewardship or SME review.

## Version And Drift Handling

Dictionary-center data and legacy evidence can drift independently. Treat this
as a normal governance case, not an error to hide.

| Drift Case | Required Handling |
| --- | --- |
| Dictionary says field exists, but code never reads/writes it | Record as candidate dormant/zombie usage; require SME or data steward review. |
| Code uses a field not present in dictionary center | Create a field-mapping TBD and route to dictionary-center steward. |
| Dictionary calculation basis conflicts with code behavior | Preserve both: code-backed observed behavior and dictionary-approved definition; block promotion until SME resolves. |
| Dictionary visibility policy conflicts with screen/report evidence | Create a contradiction finding and route to business/data owner. |
| Dictionary version changes after spec approval | Re-run affected artifact checks and update traceability if behavior, visibility, or acceptance criteria changed. |

Every artifact that depends on dictionary-center data should record the
dictionary package version or effective date in its metadata or evidence index.

## Current Non-Goals

Do not build these in the current repo phase:

- a full dictionary-center replacement
- a new `legacy-ibmi-field-logic-analyzer` skill
- mandatory all-field eight-logic matrix generation
- executable field formula replay for every standard field
- centralized UI for dictionary stewardship

The eight-logic matrix remains a valid future enhancement, but it should be
added only after dictionary-center inputs and one or more real project slices
stabilize.

## Near-Term Repo Work

The useful next increments are lightweight:

1. Add optional `standard_field_id` guidance to relevant templates when those
   templates are next revised.
2. Add a dictionary package reference to project-level metadata once an actual
   export format is known.
3. Add validation checks that flag unmapped fields and dictionary/code
   contradictions without blocking projects that do not yet have dictionary
   exports.
4. Keep `spec.yaml` as the implementation-facing source of truth, while
   preserving dictionary IDs for downstream traceability.
