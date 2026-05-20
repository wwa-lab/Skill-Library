<!--
Legacy Spec Factory
Copyright 2026 Leo L Zhang

Original author: Leo L Zhang
License: Apache License 2.0
-->

# Finding Taxonomy

This file defines the shape of one **finding** emitted by
`legacy-step-validator`. Every finding in
`06_quality/step-validation-report.md` and
`06_quality/blocking-findings.yaml` carries the same fields.

## Finding Schema

```yaml
finding_id: FIND-<SLUG>-<NNN>
dimension: 1..10                # one of the ten review dimensions
layer: mechanical | semantic | sme_readiness
severity: blocking | non_blocking
step_type: inventory | program | flow | module | spec | handoff
points_to:
  - <artifact path>             # e.g., 01_inventory/inventory.yaml
  - <line range>                # optional
  - <ID>                        # e.g., BR-CREDIT-CHECK-004
resolver: source_owner | sme | architecture | reviewer | runner
recommended_action: <one short sentence>
referenced_check: <row from references/validation-checklists.md>
notes:
```

Rules:

- One finding = one dimension. Split if it spans two.
- A finding cites artifact paths and IDs, never prose-only references.
- `recommended_action` is a single short sentence. Detail belongs in
  `notes`.
- `referenced_check` makes the finding auditable against the checklist
  row that detected it.

## Dimension Reference

| # | Dimension | Common triggers |
| --- | --- | --- |
| 1 | Input readiness | Upstream artifact missing, below status, gate blocked, required SME owner not assigned |
| 2 | Execution traceability | Decision point not recorded, procedure not cited, idempotency unstated |
| 3 | Output contract completeness | Required file / section / field missing or out-of-order |
| 4 | Evidence integrity | Claim without `EV-*` link; `EV-*` content does not support the claim |
| 5 | Knowledge taxonomy correctness | Inferred rule labeled as observed; modernization decision smuggled into legacy behaviour; evidence strength overstated |
| 6 | SME review readiness | No SME owner; review checklist missing; SME role / date / IDs not recorded on approvals |
| 7 | Downstream handoff readiness | Next-step gate fails; required artifact for next step absent |
| 8 | Open TBD handling | TBD without category; TBD without resolver; TBD blocking-status ambiguous |
| 9 | Contradiction / missing evidence detection | Two evidence items disagree without a `DEC-*` recording resolution; SME claim contradicts code without TBD |
| 10 | Evidence authorization and sensitivity safety | `sensitivity: unknown`; raw PII / financial detail outside authorized samples; missing source-path authorization; missing required redaction approval |

A finding tagged under dimension 10 always has `severity: blocking`. The
Evidence Authorization Gate is non-negotiable.

## Layer Reference

| Layer | Reproducible by | Example |
| --- | --- | --- |
| `mechanical` | Script / schema / linter | "`evidence_ids[]` is empty for OBJ-CREDIT-CHECK-003" |
| `semantic` | Reading claims against evidence | "BR-CREDIT-CHECK-004 claims `confirmed_from_code` but linked EV-* only contains a comment" |
| `sme_readiness` | Inspecting the artifact's review surface | "Inventory `sme_review.decision` is `pending` and no SME owner is named" |

Layer does **not** imply severity. A mechanical failure can be
non-blocking (e.g., a missing optional section), and a semantic finding
can be blocking (e.g., an invented field).

## Severity Reference

| Severity | Effect on status | Default when uncertain |
| --- | --- | --- |
| `blocking` | Contributes to `blocked` | This — bias toward blocking |
| `non_blocking` | Contributes at most to `pass_with_warnings` | Only when the cost of a false pass is clearly low |

Override rule: a `blocking` row can be marked `non_blocking` only when
the artifact records a named SME waiver (role, date, IDs, reason). The
validator records the waiver verbatim; it does not invent one.

## Resolver Reference

| Resolver | Meaning |
| --- | --- |
| `source_owner` | Owner of the legacy evidence — can provide a missing source member, redaction, or formal waiver |
| `sme` | Domain expert — only one who can answer business-rule, intentionality, or BAU questions |
| `architecture` | Architecture / product authority for `DEC-*` and target-platform decisions |
| `reviewer` | The validator itself — used only for findings about the report's own internal consistency |
| `runner` | The agent / human running the step — can re-execute or re-format the artifact |

A finding must name exactly one resolver. If two roles can resolve it,
pick the earliest in this list and explain in `notes`.

## Recommended Action Style

Short, imperative, one sentence. Examples:

- "Add `evidence_ids[]` to OBJ-CREDIT-CHECK-003 or mark it deprecated."
- "Surface the comment-vs-code disagreement as a TBD and route to SME."
- "Record SME role, date, and approved BR-* IDs in `spec-review.md`."

Avoid:

- "Consider reviewing the artifact for completeness." (vague)
- "This looks suspicious." (no action)
- "Refactor inventory." (too broad)

## Why "Default to Blocking"

The validator sits between cheap revisions and expensive downstream
work: code generation, golden master comparison, production deployment.
A false `pass` propagates the gap into systems that cost much more to
revise. A false `blocked` costs one extra round-trip. The asymmetry is
the reason every uncertain row is `blocking`.

If reviewers find themselves frequently overriding `blocking` to
`non_blocking`, the cause is usually a vague checklist row, not a
miscalibrated default. Tighten the row.
