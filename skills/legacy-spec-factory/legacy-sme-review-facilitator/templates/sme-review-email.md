<!--
SME Review Request Email — copy-paste template.

The facilitator skill fills the {{placeholders}} from:
  - workflow-state.yaml: capability_id, module_slug, stage_id, blocking.sme_pending
  - the artifact under review (spec.yaml / module-overview / etc.)
  - the SME contact in evidence-manifest.yaml

Replace every {{...}} before sending. The structure is deliberately
boring — SMEs are busy; clarity beats cleverness.
-->

Subject: [LSF Review] {{project_name}} · {{capability_id}} · {{n_items}} item(s) need your confirmation

Hi {{sme_name}},

I'm working on **{{project_name}}** (`docs/{{project_name}}/`) and need
your confirmation on **{{n_items}} item(s)** before I can advance the
{{capability_id}} capability from `{{current_stage}}` to the next stage.

**Artifact under review:** `{{artifact_path}}`
(open this file first — every question below cites a specific row in it)

**Estimated time:** {{estimated_minutes}} minutes total

The items are partitioned into **three buckets** so you spend the most
attention where it matters most:

- **Full review ({{n_full}} item(s))** — please decide each one
- **Spot-check sample ({{n_spotcheck}} item(s))** — pick {{spotcheck_sample_size}} to verify; if all pass, the rest batch-approve
- **Batch confirm ({{n_batch}} item(s))** — single signoff if the spot-check passes

For each item, please answer one of:

- **Confirm** — yes, the rule / behavior is correct as written
- **Reject + correct** — no; the correct version is: ______
- **Defer** — I can't decide now; please follow up by {{follow_up_date}}

---

## Bucket 1: FULL REVIEW ({{n_full}} item(s)) — per-rule decision needed

These are rules from `critical` programs (money / inventory / compliance /
posting), proposed modernization decisions, or rules where runtime data
conflicted with the code-side inference. Please decide each.

{{#each full_review_items}}
### {{this.id}} — {{this.short_title}}

- **Where it lives:** `{{this.artifact_path}}` row `{{this.row_ref}}`
- **Criticality:** {{this.criticality}} ({{this.criticality_reason}})
- **What I observed in legacy:** {{this.observed}}
- **What I inferred (needs your confirmation):** {{this.inferred}}
- **Evidence I'm relying on:** {{this.evidence_ids}}
- **Why this matters:** {{this.impact}}

**Your decision:** ☐ confirm   ☐ reject (correct: ____)   ☐ defer until ____

---
{{/each}}

## Bucket 2: SPOT-CHECK SAMPLE ({{n_spotcheck}} item(s)) — pick {{spotcheck_sample_size}} to verify

These rules from `standard` programs have ≥ {{n_runtime_corroborations}}
runtime samples corroborating the code-side inference. Please pick
{{spotcheck_sample_size}} rules from the list below to verify. If all
your picks confirm, I'll batch-approve the remaining
{{n_spotcheck_unsampled}}.

{{#each spotcheck_items}}
- `{{this.id}}` — {{this.short_title}} ({{this.runtime_corroborations}} runtime matches)
{{/each}}

**Your picks (≥ {{spotcheck_sample_size}}):** _________________________________

For each pick, decide: ☐ confirm   ☐ reject (correct: ____)   ☐ defer

---

## Bucket 3: BATCH CONFIRM ({{n_batch}} item(s)) — single signoff

These rules from `low_risk` programs have strong runtime corroboration.
If the spot-check above passes, please batch-confirm by ticking the box
below.

{{#each batch_items}}
- `{{this.id}}` — {{this.short_title}}
{{/each}}

☐ **Batch-confirm all {{n_batch}} rules above** (contingent on spot-check passing)

---

## How to respond

Pick whichever is easiest for you:

1. Reply to this email with `confirm` / `reject` / `defer` next to each ID
2. Mark up `{{artifact_path}}` directly and send back the diff
3. Schedule 15 min with me and we'll walk through it live

After your decisions, I'll:
- Run `legacy-sme-review-facilitator` to record your verdicts
- Update `docs/{{project_name}}/STATUS.md`
- Either advance the spec (if all confirms) or open follow-up items (if rejects / defers)

## Background (if you need it)

- **Project goal:** {{project_goal}}
- **What stage we're at:** {{stage_description}}
- **What unblocks if you confirm:** {{unblocks_what}}

Thanks for your time.

— {{operator_name}}
