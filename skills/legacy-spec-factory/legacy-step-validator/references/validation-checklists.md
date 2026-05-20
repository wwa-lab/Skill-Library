<!--
Legacy Spec Factory
Copyright 2026 Leo L Zhang

Original author: Leo L Zhang
License: Apache License 2.0
-->

# Validation Checklists (Per Step)

This file is the working checklist the validator runs against a detected
step package. Each step has three columns:

- **Mechanical** — reproducible by a script or schema check.
- **Semantic** — requires reading claims against evidence.
- **SME readiness** — whether the artifact is shaped so an SME can
  meaningfully review it (not whether SME has approved).

A finding's **severity** (blocking / non-blocking) is taken from the
right-hand column. The validator must not soften a `blocking` row to
`non_blocking` without a named SME waiver recorded in the artifact.

The "Maps to dimension" column indicates which of the ten review
dimensions the row primarily belongs to. Findings carry one dimension
only — split if you find yourself wanting two.

## Step Type Detection (run first)

| Package fingerprint | Detected step |
| --- | --- |
| `01_inventory/inventory.yaml` + `01_inventory/object-map.md` | inventory |
| Single `program-analysis-<OBJ-ID>.md` (with Program Call Map, Data Touch Map, control flow, file I/O sections) | program analysis |
| Single `flow-<FLOW-SLUG>.md` (with trigger model, nodes, edges, data flow sections) | flow analysis |
| `04_modules/<MODULE-SLUG>/module-overview.md` + four `0N-*.md` view files | module analysis |
| `05_specs/<CAPABILITY-SLUG>/spec.yaml` + `spec.md` + `spec-review.md` + `traceability.md` | spec writing |
| Handoff bundle citing approved `spec.yaml`, `traceability-matrix.md`, golden master samples | forward SDLC handoff |

If two fingerprints match the same package, request clarification. If
none matches, mark the package unrecognised and stop.

Spec review is intentionally not a separate detected step while
`legacy-spec-reviewer` is planned. Until that skill exists, validate
`spec-review.md` as part of the spec-writing package and use the spec-writing
checklist as the manual fallback.

## Pre-flight (every step)

Run these **before** any step-specific check. If any fails, status is
`blocked` immediately.

| Check | Layer | Maps to dimension | Severity |
| --- | --- | --- | --- |
| No `sensitivity: unknown` in evidence | mechanical | 10 | blocking |
| No raw production PII / financial detail outside authorized samples | semantic | 10 | blocking |
| Source-path authorization or required redaction approval exists for every `EV-*` | mechanical | 10 | blocking |
| Input readiness summary exists with `score`, `status`, `hard_blockers`, `optional_missing`, and `quality_boosters_available` | mechanical | 1 | non_blocking |
| `STEP-*` / `TBD-*` ID prefixes conform to `docs/id-conventions.md` | mechanical | 3 | blocking |
| All cross-referenced IDs resolve (no dangling `EV-*` / `OBJ-*` / `BR-*`) | mechanical | 4 | blocking |
| Knowledge type labels are one of `observed_behavior`, `inferred_business_rule`, `modernization_decision`, `unknown_tbd` | mechanical | 5 | blocking |
| Evidence strength labels are one of the eight allowed values | mechanical | 5 | blocking |

## Inventory step

Detected when `01_inventory/inventory.yaml` + `01_inventory/object-map.md`
are present.

### Mechanical

| Check | Maps to dimension | Severity |
| --- | --- | --- |
| `01_inventory/inventory.yaml` exists and parses as YAML | 3 | blocking |
| `01_inventory/object-map.md` exists | 3 | blocking |
| `01_inventory/inventory-review-checklist.md` exists | 3 | blocking |
| Every object has `id` (`OBJ-*`), `object_type`, `library`, `evidence_ids[]`, `sensitivity`, `review_status` | 3 | blocking |
| Every object's `evidence_ids[]` is non-empty | 4 | blocking |
| Every relationship has `from_id`, `relationship`, `to_id`, `evidence_ids[]`, `confidence`, `review_status` | 3 | blocking |
| Object types are within the allowed enum (`program`, `service_program`, `module`, …, `unknown`) | 3 | blocking |
| Relationship types are within the allowed enum (`calls`, `reads`, `writes`, …, `unknown`) | 3 | blocking |
| `sme_review.decision` is one of `pending`, `approved`, `approved_with_non_blocking_tbd`, `blocked` | 3 | blocking |
| Every TBD is in exactly one of `coverage_gaps` or `open_questions` | 8 | blocking |

### Semantic

| Check | Maps to dimension | Severity |
| --- | --- | --- |
| Object scope matches the declared capability slug | 6 | blocking |
| No `notes` field smuggles an inferred business rule | 5 | blocking |
| Prior shop spreadsheets / wikis cited as tier-3/4 hints, not as ground truth | 4 | non_blocking |
| Missing DDS / PRTF / DSPF / PF / LF / job / subroutine gaps surfaced as TBDs rather than smoothed over | 9 | blocking |
| Every `coverage_gap` is a "developer-fixable" item; every `open_question` is "SME-only" | 8 | non_blocking |

### SME readiness

| Check | Maps to dimension | Severity |
| --- | --- | --- |
| SME owner named in `inventory.yaml` when inventory is being marked approved; otherwise SME routing is documented as pending/not required | 6 | blocking |
| `inventory-review-checklist.md` covers object coverage, hidden dependencies, reports, sensitivity, downstream readiness | 6 | non_blocking |
| `sme_review.decision` recorded with date and SME role when not `pending` | 6 | blocking |

### Next-step gate

Inventory Completeness Gate passes when:

- `sme_review.decision` ∈ `approved`, `approved_with_non_blocking_tbd`
- No `coverage_gaps` entry with `blocking: yes` remains

If either fails, dimension 7 is `blocked`.

## Program analysis step

Detected when a single `program-analysis-<OBJ-ID>.md` is supplied.

### Mechanical

| Check | Maps to dimension | Severity |
| --- | --- | --- |
| File exists and follows `templates/program-analysis.md` section order | 3 | blocking |
| Header cites `OBJ-*` from an `approved` / `approved_with_non_blocking_tbd` inventory | 1 | blocking |
| Analysis Coverage & Scope, Program Call Map (visual overview + node inventory + call tree + call edge table + reverse caller index), Routine Cards, Deep Read Windows, entry points, object dependencies, Data Touch Map, control flow, file I/O, external calls, error handling, TBDs, SME checklist sections present | 3 | blocking |
| Analysis mode is one of `standard`, `segmented`, or `large_program` | 3 | blocking |
| Coverage Ledger records routines found, routines deep-read, external edges resolved, data touches resolved, blocking gaps, and non-blocking gaps | 3 | blocking |
| Segmented or large-program mode includes Routine Cards and Deep Read Windows | 3 | blocking |
| Every non-trivial behaviour has ≥1 `EV-*` link | 4 | blocking |
| TBDs grouped by `pending_source` / `pending_sme_judgment` / `non_blocking` | 8 | blocking |
| No `BR-*` or `CAP-*` minted (only program-local `BEH-*`, `EX-*`, `TBD-*`) | 3 | blocking |

### Semantic

| Check | Maps to dimension | Severity |
| --- | --- | --- |
| Behaviours are consistent with linked source lines | 4 | blocking |
| No invented subroutines, fields, files, jobs, or error codes | 4 | blocking |
| Flow-header (if present) reconciled against code-derived Program Call Map; mismatches recorded as TBDs | 9 | blocking |
| Evidence strength not overstated (no `weakly_inferred` posing as `confirmed_from_code`) | 5 | blocking |
| Knowledge type matches each statement's nature (observed vs inferred) | 5 | blocking |
| Whole-program summary does not claim more certainty than the coverage ledger supports | 5 | blocking |
| State-changing or external-boundary routines are not left `indexed_only` without a blocking or non-blocking review item | 4 | blocking |
| Fixed line-chunk summaries are not used as the source of business facts without routine/call/data evidence | 5 | blocking |

### SME readiness

| Check | Maps to dimension | Severity |
| --- | --- | --- |
| SME review checklist present at end of the document | 6 | blocking |
| SME requirement classified (required if money / inventory / compliance / customer-status; recommended otherwise) | 6 | blocking |
| Open TBDs name a resolver role | 8 | non_blocking |

### Next-step gate

Program analysis is ready for flow analysis when:

- `status` ∈ `approved`, `approved_with_non_blocking_tbd`
- SME sign-off recorded when required by the program's risk class

## Flow analysis step

Detected when a single `flow-<FLOW-SLUG>.md` is supplied.

### Mechanical

| Check | Maps to dimension | Severity |
| --- | --- | --- |
| File exists with all required sections populated, including Transaction Call Map and Common Dependencies | 3 | blocking |
| `FLOW-*`, `NODE-*`, `EDGE-*`, `DATA-*`, `SEED-*`, `TBD-*` minted; no `BR-*` minted by flow analysis | 3 | blocking |
| Every node cites an approved `program-analysis-<OBJ-ID>.md` | 1 | blocking |
| Every edge traces to evidence type 1, 2, or 3 (source statement, config export, integration contract) | 4 | blocking |
| Every UI surface references a DSPF / PRTF / `*MENU` `OBJ-*` from inventory | 4 | blocking |
| Trigger model is one of the seven allowed types | 3 | blocking |
| Every node records upstream program coverage status and blocking coverage gaps | 3 | blocking |

### Semantic

| Check | Maps to dimension | Severity |
| --- | --- | --- |
| Calls match the upstream program-analyses' External Calls sections and Program Call Map edge tables | 4 | blocking |
| Branch destinations match DSPF option tables | 4 | blocking |
| Error propagation matches each node's program-analysis | 4 | blocking |
| Commit boundaries are evidenced, not assumed | 9 | blocking |
| Business event name comes from SME, not autogenerated from program names | 6 | blocking |
| Capability seeds are questions, not approved rules | 5 | blocking |
| Flow edges, data exchanges, branch decisions, error paths, and commit boundaries do not depend on `indexed_only` state-changing routines without a named SME waiver | 4 | blocking |

### SME readiness

| Check | Maps to dimension | Severity |
| --- | --- | --- |
| Flow review checklist present | 6 | blocking |
| SME required when a cross-program rule emerges or when the flow touches money / inventory / compliance / customer status | 6 | blocking |
| TBDs grouped by blocking status | 8 | non_blocking |

### Next-step gate

Flow is ready for module analysis when:

- `status` ∈ `approved`, `approved_with_non_blocking_tbd`
- No `blocked_pending_source` or `blocked_pending_sme`
- SME has signed off on trigger model + business event name + capability seeds

## Module analysis step

Detected when `04_modules/<MODULE-SLUG>/` contains `module-overview.md`
plus four `0N-*.md` view files.

### Mechanical

| Check | Maps to dimension | Severity |
| --- | --- | --- |
| `module-overview.md` exists with 4-view index, top blocking TBDs, capability seeds, review checklist | 3 | blocking |
| All four views (`01-operation-flow.md`, `02-system-flow.md`, `03-program-flow.md`, `04-data-flow.md`) exist | 3 | blocking |
| `module-review-checklist.md` exists | 3 | blocking |
| `MODULE-*`, `VIEW-*`, `ACTOR-*`, `SYS-*`, module-level `BR-*` seeds, module-level `CAP-*` seeds, `TBD-*` minted; nothing else | 3 | blocking |
| Every in-scope flow is `approved` or `approved_with_non_blocking_tbd` | 1 | blocking |

### Semantic

| Check | Maps to dimension | Severity |
| --- | --- | --- |
| Cross-flow synthesis matches the flow analyses; no new IBM i facts introduced | 4 | blocking |
| Every View 1 actor appears in View 3 (or is tagged manual) | 2 | blocking |
| Every View 2 system appears in View 3 as a trigger or external call | 2 | blocking |
| Every View 4 data object traces to at least one flow in View 3 | 2 | blocking |
| Tier-2 SME claims contradicting tier-1 code are surfaced as TBDs, not overrides | 9 | blocking |
| Capability seeds and business-rule seeds remain *questions* | 5 | blocking |
| BAU rhythm, regulatory references, manual procedures come from SME, not inferred | 4 | blocking |

### SME readiness

| Check | Maps to dimension | Severity |
| --- | --- | --- |
| Each view names its expected SME (business owner / integration architect / dev lead / data analyst) | 6 | blocking |
| Per-view review checklist present | 6 | non_blocking |
| Module-level review checklist present | 6 | blocking |

### Next-step gate

Module is ready for spec writing when **all four views** are at least
`approved_with_non_blocking_tbd` and the module overview is signed off.

## Spec writing step

Detected when `05_specs/<CAPABILITY-SLUG>/spec.yaml` + `spec.md` +
`spec-review.md` + `traceability.md` are present.

### Mechanical

| Check | Maps to dimension | Severity |
| --- | --- | --- |
| `spec.yaml` validates against `schemas/spec.schema.yaml` | 3 | blocking |
| `spec_id`, `capability.{id,name,slug,owner}`, `scope`, `evidence[]`, `behaviors[]`, `business_rules[]`, `modernization_decisions[]`, `data_model`, `process_flow.steps[]`, `inputs[]`, `outputs[]`, `exceptions[]`, `acceptance_criteria[]`, optional `test_cases[]`, `tbds[]` populated | 3 | blocking |
| Every `BEH-*`, `BR-*`, `DEC-*` links to ≥1 `EV-*` | 4 | blocking |
| Every `BR-*` links to ≥1 `BEH-*` | 4 | blocking |
| Every `approved` `BR-*` has ≥1 `AC-*` | 7 | blocking |
| Every `AC-*` carries `validates: [BR-*]` | 4 | blocking |
| Every `TBD-*` has a category and resolver | 8 | blocking |
| `evidence[]` rows all have `sensitive` resolved | 10 | blocking |

### Semantic

| Check | Maps to dimension | Severity |
| --- | --- | --- |
| Each `BR-*` is supported by its linked `BEH-*` and `EV-*` content | 4 | blocking |
| `modernization_decisions` explicitly separated from `observed_behavior` | 5 | blocking |
| No invented Java/target-platform details | 4 | blocking |
| Data-model field semantics never come from field names alone | 4 | blocking |
| Tier 3/4 backing alone does not raise a `BR-*` past `needs_sme_review` | 5 | blocking |
| `traceability.md` is consistent with `spec.yaml` content | 2 | blocking |

### SME readiness

| Check | Maps to dimension | Severity |
| --- | --- | --- |
| `capability.owner` named | 6 | blocking |
| `spec-review.md` checklist present | 6 | blocking |
| SME approval recorded for every `BR-*` reaching `approved` (with role, date, IDs) | 6 | blocking |
| SME approval recorded for transition `in_review` → `approved` | 6 | blocking |

### Next-step gate

Spec is ready for Forward SDLC Handoff when:

- `spec.yaml.status = approved`
- Every business-critical `BR-*` is `approved`
- No blocking TBD remains
- Data sensitivity has been reviewed
- `acceptance_criteria` exist for every approved `BR-*`
- Modernization decisions explicitly separated from observed legacy behaviour

## Forward SDLC handoff step

Detected when a handoff bundle cites `spec.yaml` (`status: approved`),
`spec.md`, `traceability-matrix.md`, golden master samples, and an
acceptance-criteria list.

### Mechanical

| Check | Maps to dimension | Severity |
| --- | --- | --- |
| `spec.yaml.status = approved` | 7 | blocking |
| Every approved `BR-*` has `AC-*` | 7 | blocking |
| `traceability-matrix.md` (or equivalent) present | 3 | blocking |
| Redacted sample transactions included when golden master comparison is required | 10 | blocking |
| No `TBD-*` with `blocks_next_step: yes` remains | 7 | blocking |

### Semantic

| Check | Maps to dimension | Severity |
| --- | --- | --- |
| Modernization decisions explicitly separated from observed legacy behaviour | 5 | blocking |
| Approved rules are linked to evidence that meets the approval rule in `docs/evidence-and-knowledge-taxonomy.md` | 4 | blocking |
| No silent gap (the handoff bundle does not require re-interrogating the SME to be implementable) | 9 | blocking |

### SME readiness

| Check | Maps to dimension | Severity |
| --- | --- | --- |
| SME sign-off named with role and date | 6 | blocking |
| Architecture / product sign-off recorded for any `DEC-*` reaching `approved` | 6 | blocking |

### Next-step gate

After `pass`, the package crosses to `wwa-lab/build-agent-skill` per
`docs/forward-sdlc-contract.md`. The validator's report is the gate's
evidence; the validator does not perform the handoff itself.

## Default-to-Blocking Rule

When a finding's blocking status is genuinely unclear, mark it
`blocking`. The cost of a false `pass` propagates downstream into code,
tests, and production behaviour; the cost of a false `blocked` is one
extra round-trip. Bias accordingly.
