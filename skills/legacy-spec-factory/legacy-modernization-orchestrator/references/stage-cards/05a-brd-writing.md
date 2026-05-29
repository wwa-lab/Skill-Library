# Stage 05a: BRD Writing And Review

**You are here if:** module analysis is approved for a selected `CAP-*`, and
you need the business-facing BRD Package for SME / stakeholder review before
writing the technical `spec.yaml`.

This is the standard review gate between module synthesis and spec writing.
The BRD answers "what business capability are we preserving or modernizing?"
in SME-readable language.

## Need before starting

- `04_modules/<MODULE-SLUG>/` — overview + all 4 views, all approved
- A single `CAP-*` from `module-overview.md` to scope this BRD
- Linked `BR-*`, `BEH-*`, `EV-*`, and `TBD-*` seeds for that capability
- Capability owner SME / BA availability for BRD review

## Run

- **Skill:** `legacy-brd-writer` (Implemented v0.1.5)
- **Manual fallback:** Use the templates in
  `skills/legacy-brd-writer/templates/` and keep sections 1-9 populated with
  evidence-backed content or named `TBD-*` gaps.

## Produce

- **Artifact set per capability:**
  - `brd.md` — business-facing BRD; sections 1-9 required, 10-12 optional
  - `brd-review.md` — SME review checklist and sign-off page
  - `validation-scenarios.md` — BRD-stage `VAL-*` scenario seeds
  - `traceability.md` — BRD requirement / behavior / evidence / TBD mapping
- **Save under:** `05_brds/<CAPABILITY-SLUG>/` *(relative to your
  `project.root`)*
- **Consumed by:** `legacy-sme-review-facilitator`, then `legacy-spec-writer`

## Gate before advancing

- **Name:** BRD Review Gate
- **Check:**
  - BRD sections 1-9 are present and SME-reviewable
  - Missing details are explicit `TBD-*`, not silent blanks
  - Observed behavior, inferred rules, SME decisions, assumptions, and TBDs are
    separated
  - `brd-review.md` or `review-decision.yaml` records SME / business approval
- **Blocks if:** BRD is missing, draft without review, blocked by SME, or any
  required section 1-9 is absent without a named `TBD-*`.

## SME action

- **Required:** yes — this is the main business review point.
- **Ask:** "Do sections 1-9 correctly describe the function purpose, use cases,
  channels, user touchpoints, interfaces, process, validation, error handling,
  and dependencies? Which gaps remain?"
- **Recorded in:** `brd-review.md` and, when used,
  `review-decision.yaml`.

## Next card

[`06-spec-writing.md`](06-spec-writing.md) — once the BRD Package is approved
or an explicit technical-spec-only bypass has been recorded.
