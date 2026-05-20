# Inventory Output Contract

## `inventory.yaml`

The inventory is a structured object ledger. It should contain:

- capability metadata
- evidence ledger
- object inventory
- relationship map
- coverage gaps (artifact-level)
- open questions (SME-level)
- SME review status

### `coverage_gaps` vs `open_questions`

Both fields hold `TBD-<SLUG>-<NNN>` entries but mean different things and must
not be mixed:

| Field | Meaning | Example | Resolved By |
| --- | --- | --- | --- |
| `coverage_gaps` | A specific legacy artifact is missing, unreadable, or unauthorized | DDS source for a referenced PRTF is not in the bundle | Source-owner action: provide, authorize, redact, or formally waive the artifact |
| `open_questions` | The artifacts are present but a business/runtime fact is unclear and needs SME judgment | Whether a data area overrides a threshold during month-end | SME answer recorded in `sme_review` |

Rule of thumb: if a developer or build engineer can fix it by producing a file,
it is a `coverage_gap`. If only a domain expert can answer it, it is an
`open_question`.

### `sme_review.decision` values

| Value | Meaning |
| --- | --- |
| `pending` | Review has not started |
| `approved` | All objects, evidence, and gaps are acceptable; downstream skills may run |
| `approved_with_non_blocking_tbd` | Some TBDs remain but SME has flagged them as non-blocking |
| `blocked` | One or more blocking gaps or open questions prevent downstream use |

Required object fields:

```yaml
id:
name:
object_type:
library:
source_member:
description:
evidence_ids: []
sensitivity:
review_status:
notes:
```

Object types:

- `program`
- `service_program`
- `module`
- `cl_command`
- `pf`
- `lf`
- `dspf`
- `prtf`
- `job`
- `scheduler_entry`
- `report`
- `spool_sample`
- `data_area`
- `data_queue`
- `message_queue`
- `copybook`
- `external_interface`
- `unknown`

Required relationship fields:

```yaml
from_id:
relationship:
to_id:
evidence_ids: []
confidence:
review_status:
```

Relationship types:

- `calls`
- `reads`
- `writes`
- `updates`
- `deletes`
- `uses_display_file`
- `uses_printer_file`
- `submits_job`
- `uses_data_area`
- `uses_data_queue`
- `uses_message_queue`
- `depends_on`
- `unknown`

## `object-map.md`

The object map is the human-readable view for SME review. It should summarize:

- capability scope
- object coverage
- high-risk gaps
- relationships
- evidence summary
- SME questions

## `inventory-review-checklist.md`

The checklist must include:

- object coverage confirmation
- hidden dependency prompts
- report/spool confirmation
- data sensitivity confirmation
- downstream readiness decision
