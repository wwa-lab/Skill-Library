<!--
SME Review Checklist — a one-page printable / shareable checklist the SME
can mark up offline. Companion to sme-review-email.md.

The facilitator skill fills the {{placeholders}} from the same sources as
the email template. Replace every {{...}} before sharing.
-->

# SME Review Checklist — {{project_name}} / {{capability_id}}

**Module:** {{module_slug}}  ·  **Stage:** {{current_stage}}  ·  **Date prepared:** {{prepared_date}}
**Operator:** {{operator_name}}  ·  **SME:** {{sme_name}}

**Artifact under review:** [`{{artifact_path}}`]({{artifact_path}})

---

## How to use this checklist

For each item:

1. Read the row in the artifact (line/section reference is in the table).
2. Pick one decision: ☐ confirm  ☐ reject (write the correction)  ☐ defer (give a follow-up date).
3. Add a one-line note if useful.

Return the marked-up checklist (or just the decisions) to {{operator_name}}.

---

## Items to decide ({{n_items}} total)

{{#each items}}
### {{this.id}}

| Field | Value |
| --- | --- |
| **Artifact row** | `{{this.artifact_path}}` row `{{this.row_ref}}` |
| **Knowledge type** | `{{this.knowledge_type}}` |
| **Observed in legacy** | {{this.observed}} |
| **Inferred (please confirm)** | {{this.inferred}} |
| **Evidence cited** | {{this.evidence_ids}} |
| **Impact if wrong** | {{this.impact}} |

**Decision** ({{this.id}}):

- ☐ Confirm — rule / behavior is correct as written
- ☐ Reject — correct version is: _________________________________________
- ☐ Defer — follow up by ___________ (date)

**Notes / context:** ___________________________________________________

---
{{/each}}

## Sign-off

After all items are decided:

- **SME name:** _________________________________________
- **Date:** _____________
- **Decision summary:** ___ confirmed · ___ rejected · ___ deferred

Signature: _________________________________________

---

## What happens next

1. {{operator_name}} runs `legacy-sme-review-facilitator` with your
   decisions to update `docs/{{project_name}}/workflow-state.yaml`.
2. STATUS.md is regenerated to reflect the closed items.
3. If all items are confirmed and there are no rejects/defers, the spec
   advances to the next stage (typically `8b Spec In Review` → `8c Spec
   Approved`).
4. If any item was rejected or deferred, follow-up items are opened and
   the spec stays at the current stage until they close.

---

## Quick reference — what each knowledge type means

| Knowledge type | Where it came from | Why we ask SME |
| --- | --- | --- |
| `confirmed_from_code` | Source code makes it unambiguous | Confirm we read the code right; rare to reject |
| `inferred_business_rule` | Inferred from code + behavior, not stated | Confirm intent — this is where rejections usually happen |
| `observed_in_runtime` | Pulled from job logs / spool / runtime samples | Confirm the runtime sample is representative |
| `modernization_decision` | A `DEC-*` proposing a change | Approve only with architecture/product authority |
