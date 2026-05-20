# Stage 06: Spec Writing (one capability at a time)

**You are here if:** module analysis is approved (4 views + overview) AND
you want to produce a per-capability `spec.yaml` + `spec.md` that downstream
forward SDLC can consume.

You produce **one spec per `CAP-*`** capability seed listed in
`module-overview.md`. Do not bundle multiple capabilities into one spec.

## Need before starting

- `04_modules/<MODULE-SLUG>/` — overview + all 4 views, all approved
- A single `CAP-*` from `module-overview.md` to scope this spec
- Linked `BR-*` rules and `evidence_id`s for that capability
- SME availability for `inferred_business_rule` confirmation and the
  `draft → in_review → approved` transitions

## Run

- **Skill:** `legacy-spec-writer` (Implemented v0.1.0)
- **Manual fallback:** Use `schemas/spec.schema.yaml` and the templates in
  `skills/legacy-spec-writer/references/`

Optional companions:

- `legacy-modernization-decision-writer` — if the spec proposes a large /
  risky `DEC-*` decision, formalize it as a separate decision package
- `legacy-sme-review-facilitator` — to organize the SME review session
  that closes the `in_review → approved` transition
- `legacy-html-exporter` — after `spec.md`, `traceability.md`, or review /
  question-pack Markdown exists and SMEs need a browser-friendly review view.
  Markdown remains canonical; fix Markdown first and regenerate HTML if content
  changes.

## Produce

- **Artifact set per capability:**
  - `spec.yaml`  (machine-readable contract; conforms to `schemas/spec.schema.yaml`)
  - `spec.md`    (human-readable explanation)
  - `traceability.md` (rule → evidence → test mapping)
  - `review-report.md` (optional, from `legacy-spec-reviewer` when available)
- **Save under:** `05_specs/<CAP-ID>/` *(relative to your `project.root`)*
  e.g. `docs/XXX260004-demo/05_specs/CAP-ORDER-PRICING/spec.yaml`
- **Consumed by:** `legacy-brd-to-sdd-handoff`,
  `legacy-golden-master-test-planner`, forward SDLC
  (`wwa-lab/build-agent-skill`)

## Gate before advancing

- **Name:** Evidence Approval Gate (during writing) → SME approval
  (transition to `approved`)
- **Check:**
  - Every rule has at least one linked `evidence_id`
  - No rule with `knowledge_type: inferred_business_rule` has
    `review_status: needs_sme_review`
  - Every approved rule has `acceptance_criteria`
  - `spec.yaml.status: approved` AND no blocking `TBD-*` remain
- **Blocks if:** any of the above fail. The orchestrator must refuse to
  hand off to the Forward Handoff Gate until all are satisfied.
- **HTML export note:** HTML companions never satisfy this gate. They only make
  stable Markdown easier to review.

## SME action

- **Required:** yes — at two points:
  1. Per-rule confirmation for every `inferred_business_rule`
  2. Sign-off for `spec.yaml.status: in_review → approved`
- **Ask:** "Confirm each inferred rule (correct / wrong / needs change).
  Are the acceptance criteria sufficient? Approve the spec?"
- **Recorded in:** `spec.yaml.rules[].review_status` +
  `spec.yaml.status` + `spec.yaml.sme_review`

## Next card

[`07-forward-handoff.md`](07-forward-handoff.md) — once `spec.yaml.status:
approved` for every capability planned in this delivery, **and** the
equivalence test pack is ready.
