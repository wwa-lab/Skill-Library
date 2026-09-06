---
name: legacy-traceability-packager
description: Use when one capability's end-to-end traceability across the Legacy Spec Factory reverse chain needs packaging, validation, or audit — evidence manifest, inventory, program/flow/module analyses, optional BRD, approved `spec.yaml`/`spec.md`/`traceability.md`, and optional SDD handoff. Audit / packager / gate skill — does not mint business rules, behaviors, acceptance criteria, modernization decisions, evidence, test cases, or SDD handoffs, and does not promote review status. Emits a sealed traceability package or a strict blocked-findings report. Layer 2 (platform-agnostic).
license: Apache-2.0
metadata:
  author: Leo L Zhang
  maintainer: platform-engineering
  source: https://github.com/wwa-lab/legacy-spec-factory
  source_commit: 3b6a16b
  domain: legacy-spec-factory
---

<!--
Legacy Spec Factory
Copyright 2026 Leo L Zhang

Original author: Leo L Zhang
License: Apache License 2.0

This skill is part of the Legacy Spec Factory project.
Retain this notice in substantial copies or derived versions.
-->

# Legacy Traceability Packager

## Purpose

Package one capability's **end-to-end traceability** into a sealed, audit-friendly bundle that answers four questions deterministically:

1. **EV coverage** — for every `EV-*`, which `BEH-*` / `BR-*` / `DEC-*` / `STEP-*` / `AC-*` / `TC-*` use it?
2. **BR closure** — for every approved `BR-*`, is there evidence, behavior, acceptance criteria, and test coverage?
3. **Mechanical integrity** — are there dangling IDs, orphan evidence, orphan AC, missing evidence, `sensitivity: unknown` items, authorization gaps, or blocking TBDs?
4. **Routing** — which downstream handoff blockers remain, and which upstream skill owns each one?

This skill is an **audit and governance packager**. It is **not** `legacy-brd-to-sdd-handoff` — it neither produces nor replaces the Atlas-bound SDD handoff. It consumes the same upstream artefacts and emits a parallel, traceability-focused package that auditors, SMEs, compliance, and the modernization orchestrator can consume without re-deriving cross-references.

The package is a **carrier**, not a creator. Every row in the output is a value already present (or already absent and therefore a finding) in the upstream artefacts.

## When to Use

Trigger when **all** of the following hold:

- An approved `05_specs/<CAPABILITY-SLUG>/spec.yaml` (and `spec.md`) exists for the capability, or a `blocked` audit of an unapproved spec is explicitly requested for routing.
- The upstream chain (`01_inventory/`, `02_programs/`, `03_flows/`, `04_modules/`) is at or above `approved_with_non_blocking_tbd` for every artefact the spec references.
- An evidence manifest from `legacy-ibmi-evidence-intake` is available for every `EV-*` referenced by the BRD or spec.
- A reviewer (audit, compliance, capability owner SME) needs a sealed traceability report — for example before forward SDLC handoff, before an external audit, or as part of an internal field pilot review.

Also use when the orchestrator wants a fast, deterministic answer to "is this capability internally consistent?" before invoking `legacy-brd-to-sdd-handoff`.

## When NOT to Use

Block and route elsewhere when any of the following hold:

- `spec.yaml` is missing entirely → route to `legacy-spec-writer`. Never fabricate a spec.
- Caller wants new `BR-*`, `BEH-*`, `AC-*`, `DEC-*`, `EV-*`, `TC-*`, or `TBD-*` → route to the owning skill (`legacy-spec-writer`, `legacy-brd-writer`, `legacy-ibmi-program-analyzer`, etc.).
- Caller wants an Atlas-consumable SDD handoff package → route to `legacy-brd-to-sdd-handoff`.
- Caller wants architecture, design, user stories, code, or tests → that is the Atlas SDD chain.
- The evidence manifest has any item with `sensitivity: unknown`, missing
  source-path authorization, or required redaction without approval → route to
  `legacy-ibmi-evidence-intake`.
- Module / flow / program analyses are below `approved_with_non_blocking_tbd` → route to the relevant analyzer.

This skill is an **audit gate and packager**. If you find yourself writing new business content, you are in the wrong skill.

## Role

You are the **traceability auditor and packager** for one capability.

You must:

- carry every `EV-*`, `BEH-*`, `BR-*`, `DEC-*`, `AC-*`, `TC-*`, `TBD-*`, `IN-*`, `OUT-*`, `EX-*`, `STEP-*` ID forward **unchanged** from the upstream artefacts;
- resolve every cross-reference mechanically — every claim of "linked" must point to an ID that actually exists in the upstream artefacts;
- apply the gate rules in [references/output-contract.md](references/output-contract.md) **block-by-default**;
- record every blocking finding with rule, location, upstream owner, and exact required remediation;
- route open issues to the owning upstream skill, never resolve them.

You must not:

- invent `BR-*`, `BEH-*`, `AC-*`, `DEC-*`, `EV-*`, `TC-*`, `TBD-*`, `IN-*`, `OUT-*`, `EX-*`, or `STEP-*`;
- rewrite, paraphrase, or merge upstream content;
- promote any review status or downgrade severity to make the package green;
- silently demote a `sensitivity: unknown` evidence item;
- treat a missing spec as recoverable by reading the BRD or the analyses directly;
- mint a competing SDD handoff package — `legacy-brd-to-sdd-handoff` owns that artefact.

The only IDs this skill may mint are:

- `FIND-<CAPABILITY-SLUG>-<NNN>` — findings raised by this run; and
- a package identifier `PKG-<CAPABILITY-SLUG>-<NNN>` for the package itself (one per run).

## Inputs

Required:

- approved `05_specs/<CAPABILITY-SLUG>/spec.yaml` and `spec.md` (or, for an explicit blocked-audit run, a `draft`/`in_review` spec accompanied by an explicit `status_override: blocked_audit` from the caller — the package is still produced as `blocked`);
- `05_specs/<CAPABILITY-SLUG>/traceability.md` if present (read for cross-check, not for content);
- approved upstream analyses referenced by the spec (`04_modules/...`, `03_flows/...`, `02_programs/...`, `01_inventory/inventory.yaml`);
- evidence manifest produced by `legacy-ibmi-evidence-intake` for every `EV-*` referenced by the BRD or spec, using the canonical manifest fields `evidence_id`, `sensitivity`, `redaction_status`, `redacted_filename`, `source_path_verified`, `redaction_required`, `sme_required`, and `sme_approval`;
- a named capability-owner SME (for sign-off on the resulting package).

Optional:

- approved `05_brds/<CAPABILITY-SLUG>/brd.md` and `brd-review.md` (if a BRD step was executed);
- approved `06_sdd_handoffs/<CAPABILITY-SLUG>/` package (if the SDD handoff has already been packaged — the traceability package then cross-checks the handoff for consistency);
- approved `legacy-golden-master-test-planner` output, if present, for `TC-*` cross-check.

Input readiness scoring:

- `0-5 blocked`: required spec/upstream analysis missing or below status,
  evidence manifest incomplete or unauthorized, referenced IDs unresolved,
  blocking TBDs unresolved, or required SME sign-off missing.
- `6 minimum_pass`: approved spec, approved upstream analyses, canonical
  evidence manifest, named capability-owner SME, and resolvable ID graph are
  present.
- `7-8 usable`: approved BRD, handoff package, and existing traceability view
  are supplied for cross-checking.
- `9-10 strong`: approved golden-master test outputs, runtime coverage notes,
  audit/compliance review context, and downstream package expectations are also
  supplied.
- Missing BRD, handoff, or golden-master outputs does not block when the run is
  explicitly spec-centered; it limits cross-check coverage and should be listed
  as optional missing.

Stop conditions are listed under **When NOT to Use**; each one is **blocking by default** and the gate does not advance unless explicitly cleared by an SME-recorded waiver in the upstream artefact.

## Output Contract

Produce exactly one directory `06_traceability_packages/<CAPABILITY-SLUG>/`. This path sits **alongside** `06_sdd_handoffs/<CAPABILITY-SLUG>/`, not inside it; the two packages are produced by different skills, serve different consumers, and must not overwrite each other.

For `pass` and `pass_with_warnings` outcomes, write exactly these four files:

```
06_traceability_packages/<CAPABILITY-SLUG>/
├── traceability-package.yaml   ← machine-readable, sealed traceability contract
├── traceability-package.md     ← human-readable rendering of the same content
├── coverage-audit.md           ← EV / BR / AC / TC / DEC coverage tables
└── traceability-review.md      ← gate checklist, findings, sign-offs
```

For `blocked` outcomes, write only:

```
06_traceability_packages/<CAPABILITY-SLUG>/
├── traceability-review.md      ← gate checklist, blocking findings, remediation
└── blocking-findings.yaml      ← machine-readable blocked-run findings record
```

A blocked package is a normal outcome, not an error. The gate's job is to fail loudly and early so the upstream skill can fix the artefact before forward SDLC consumes it.

Distinction with neighbours:

| Artefact | Owner | Purpose |
| --- | --- | --- |
| `05_specs/<CAP>/traceability.md` | `legacy-spec-writer` | Per-spec narrative traceability rendered alongside `spec.yaml` |
| `05_brds/<CAP>/traceability.md` | `legacy-brd-writer` | Per-BRD narrative traceability rendered alongside `brd.md` |
| `06_sdd_handoffs/<CAP>/` | `legacy-brd-to-sdd-handoff` | Atlas-bound SDD handoff package |
| `06_traceability_packages/<CAP>/` | **this skill** | Sealed cross-artefact traceability audit + gate report |

`traceability-package.yaml` is a **carrier**, not a creator. Every field traces back to a value in the BRD, spec, evidence manifest, upstream analyses, or to a `FIND-*` generated during this run.

### Why this directory and not `06_sdd_handoffs/`?

`06_sdd_handoffs/<CAP>/` is the Atlas-bound sealed handoff produced by `legacy-brd-to-sdd-handoff`. Mixing a traceability audit into that directory would (a) confuse downstream Atlas consumers about what the directory contains, (b) collide with that skill's blocked-path discipline (it writes only `handoff-review.md` and `blocking-finding.yaml`), and (c) imply that this skill produces handoffs, which it does not. Numbering both directories `06_` keeps the audit and the handoff at the same governance tier (post-spec, pre-Atlas) while keeping owners and consumers distinct.

### Required `traceability-package.yaml` structure

The full field-level schema lives in [references/output-contract.md](references/output-contract.md). The required top-level keys are:

- `schema_version`
- `package_id` (`PKG-<CAPABILITY-SLUG>-<NNN>`, per `../../docs/id-conventions.md`)
- `package_date` (ISO 8601, UTC)
- `packager` (e.g. `legacy-traceability-packager v0.1.1`)
- `capability` (`id`, `name`, `slug`, `owner` — copied unchanged from the spec)
- `status` — `pass | pass_with_warnings | blocked`
- `source_artifacts` — paths, IDs, and statuses for spec, BRD (optional), module, flows, programs, inventory, evidence manifest, and any pre-existing SDD handoff package
- `brd_functional_coverage` — when a BRD is supplied, section 1-9 coverage
  copied from BRD review decisions and audited for blocked / missing required
  areas
- `id_inventory` — counts and ID lists per prefix (`EV`, `BEH`, `BR`, `AC`, `DEC`, `TC`, `TBD`, `IN`, `OUT`, `EX`, `STEP`, `DATA`, `OBJ`, `FLOW`, `MODULE`, `CAP`)
- `evidence_coverage` — for every `EV-*`, the IDs that reference it and whether it is orphan
- `behavior_coverage` — for every `BEH-*`, supporting `EV-*` and the `BR-*` it backs
- `business_rule_coverage` — for every `BR-*`, linked `BEH-*`, `EV-*`, and `AC-*`, plus review status
- `acceptance_criteria_coverage` — for every `AC-*`, validated `BR-*` and any `TC-*` that exercises it
- `test_coverage` — for every `TC-*`, the `AC-*` or `BR-*` it validates and any `EV-*` sample-data reference
- `decision_coverage` — for every `DEC-*`, the `BR-*` / `BEH-*` / constraint cited in its rationale
- `open_questions` — every `TBD-*` carried forward verbatim with `blocking`, `resolution`, `resolver`, `planned_resolution_date`, and `deferral_recorded_in`
- `findings` — `{ blocking[], warnings[], info[] }`, each entry minted as `FIND-*`
- `review_sign_offs` (alias: `sme_sign_offs`) — spec approver, BRD approver (if present), packager validator, packager SME approver, each with `name`, `role`, ISO `date`, and `approval_scope`
- `next_routing` — for each finding, the upstream skill and capability owner who must act, plus whether a re-run is expected

A package is **sealed**: every ID present in `traceability-package.yaml` must already exist in the upstream artefacts. The skill must not append any ID that is not derivable from upstream content.

## Step Contract

This skill is one step in the Legacy Spec Factory reverse chain. It conforms to the canonical Step Contract — see
[../legacy-step-contract/SKILL.md](../legacy-step-contract/SKILL.md) and
[../legacy-step-contract/references/step-contract.md](../legacy-step-contract/references/step-contract.md)
for the full field-level rules. The summary below is normative for this skill.

### Input

See **Inputs** and **When NOT to Use** above. The skill must not start if any required upstream artefact is missing or below its required status.

### Execution

- **Procedure**: see [references/workflow.md](references/workflow.md) — eight ordered steps (intake → ID inventory → cross-reference walk → evidence-sensitivity check → BR closure check → AC / TC coverage → TBD carry-forward → package assembly or blocked-route).
- **Allowed inference**: copying fields verbatim from spec / BRD / evidence manifest / upstream analyses; counting and indexing IDs; computing pass/warn/fail on the gate checklist; minting `FIND-*` for findings and `PKG-*` for the package; routing each finding to its owning upstream skill.
- **Forbidden inference**: see [references/anti-hallucination.md](references/anti-hallucination.md). In particular: no new `BR-*`, `BEH-*`, `AC-*`, `DEC-*`, `EV-*`, `TC-*`, or `TBD-*`; no rewriting of upstream content; no architecture, framework, or platform recommendations.
- **TBD handling**: blocking unresolved TBD → block package, write finding; SME-deferred blocking TBD with named resolver + planned date + `deferral_recorded_in` pointer → carry forward as warning; non-blocking TBD → carry forward as info.

### Output

- **Canonical directory**: `06_traceability_packages/<CAPABILITY-SLUG>/` with the four files above (or two on blocked).
- **ID minting policy**: this skill may mint only `FIND-*` and `PKG-*`. Every other ID (`EV-*`, `BEH-*`, `BR-*`, `DEC-*`, `AC-*`, `TC-*`, `TBD-*`, `IN-*`, `OUT-*`, `EX-*`, `STEP-*`, `OBJ-*`, `FLOW-*`, `MODULE-*`, `CAP-*`, `DATA-*`, `NODE-*`, `EDGE-*`, `VIEW-*`, `ACTOR-*`, `SYS-*`, `SEED-*`, `BRD-*`) must be reused unchanged from upstream artefacts. Using a prefix outside this minting list is a mechanical failure.
- **Immutable guarantees**:
  - every upstream ID appears in the package exactly as in its source artefact; no renumbering, no rewording;
  - no evidence is dropped; sensitivity is recorded, never hidden;
  - traceability is bidirectional (every approved `BR-*` links forward to `AC-*` and backward to `EV-*`);
  - finding categorisation is conservative: ambiguous cases default to `blocked`, never silently `pass_with_warnings`.

### Validation

- **Mechanical**: gate checklist booleans evaluated against the spec / BRD / evidence manifest; no `null` values left in `traceability-package.yaml`; every referenced ID resolves; only `FIND-*` and `PKG-*` are minted; status field matches the findings actually present.
- **AI semantic**: every blocking finding cites a rule from [references/output-contract.md](references/output-contract.md) and names the responsible upstream skill; every warning carries enough context for a reviewer to decide whether to waive.
- **SME approval**: the package sign-off block records name + role + ISO date for the capability-owner SME plus any audit / compliance reviewer required by the host project.

Use `legacy-step-validator` to validate the produced package against this Step Contract before forwarding it to the orchestrator or to forward SDLC.

## Workflow State Write-Back (history only)

This is a governance / packager skill. It does NOT mutate
`capabilities[].stage_id` or `current_focus`. After a packaging run,
append one `history[]` entry to `<project-root>/workflow-state.yaml` per
[`docs/workflow-state-contract.md`](../../docs/workflow-state-contract.md).

**Package path pattern:**
`09_forward-sdlc/<CAP-*>/traceability-package/` (sealed bundle)

**Per-run write:**

```yaml
history:
  - at: <ISO 8601>
    skill: legacy-traceability-packager
    capability_id: <CAP-* from current_focus>
    stage_after: <the capability's current stage_id — UNCHANGED>
    artifact: <path to the sealed package or findings report>
    note: "traceability sealed for <CAP-*>" | "blocked: <findings count>"
```

Also overwrite `project.last_updated_at` / `project.last_updated_by`.

**Permitted side-effect:** if any blocking finding emerges, you MAY
append items to `capabilities[<CAP-*>].blocking.gates` (e.g.
`"forward_handoff"`) and to `blocking.tbds`. You MUST NOT change
`stage_id`, `last_artifact`, or `last_skill`.

If `workflow-state.yaml` does not exist, this skill does NOT create it.

## References and Templates

- [references/workflow.md](references/workflow.md) — full eight-step procedure and per-step finding rules
- [references/output-contract.md](references/output-contract.md) — field-level schema for `traceability-package.yaml`, gate rules, status decision table
- [references/anti-hallucination.md](references/anti-hallucination.md) — what this skill must refuse to invent
- [templates/traceability-package.yaml](templates/traceability-package.yaml) — sealed package template (machine-readable)
- [templates/traceability-package.md](templates/traceability-package.md) — human-readable rendering template
- [templates/coverage-audit.md](templates/coverage-audit.md) — EV / BR / AC / TC / DEC coverage tables template
- [templates/traceability-review.md](templates/traceability-review.md) — gate checklist, findings, sign-offs template
- [templates/blocking-findings.yaml](templates/blocking-findings.yaml) — blocked-run findings record template

## Status Labels

| `status` (in YAML) | Display label | Meaning |
| --- | --- | --- |
| `pass` | `pass` | every gate passed; no blocking, warning, or info findings were raised |
| `pass_with_warnings` | `pass_with_warnings` | every blocking gate passed, but at least one warning or info finding is present (deferred blocking TBD, non-blocking TBD, SME-waived orphan evidence, or SME-waived AC) |
| `blocked` | `blocked` | at least one blocking finding; only `traceability-review.md` and `blocking-findings.yaml` are written |

There is no fourth status. Ambiguous cases default to `blocked`.

## Examples

Three adversarial examples exercise the gate end-to-end. Each ships with the expected status and the rule that fires; full inputs are referenced rather than duplicated.

| Example | Scenario | Expected status |
| --- | --- | --- |
| [traceability-positive/](examples/traceability-positive/) | Credit Limit Enforcement: every `EV-*` reaches a `BR-*` or `BEH-*`; every approved `BR-*` has `EV-*`, `BEH-*`, and `AC-*`; every `AC-*` validates an approved `BR-*`; no `sensitivity: unknown`; no open TBD. | `pass` |
| [traceability-blocked-dangling-id/](examples/traceability-blocked-dangling-id/) | Order Entry: spec lists `AC-ORDER-ENTRY-004` validating `BR-ORDER-ENTRY-007`, but `BR-ORDER-ENTRY-007` does not exist in `spec.yaml.business_rules[]`. | `blocked` (route to `legacy-spec-writer`) |
| [traceability-warning-deferred-tbd/](examples/traceability-warning-deferred-tbd/) | Returns Processing: every blocking gate clears, but one `TBD-*` with `blocking: true` carries a named SME deferral and a planned 2026-07-31 resolution date recorded in `spec-review.md`. | `pass_with_warnings` |

All three examples reuse stable IDs from real or representative capabilities and ship a minimal expected-output snippet so a reviewer can diff the rule against the run.

## Review Gate Checklist

Before writing a non-blocked traceability package, every box below must be true. A clean `pass` also requires zero warning and info findings; otherwise the non-blocked result is `pass_with_warnings`.

- [ ] `spec.yaml` `status: approved` (or explicit `blocked_audit` override for routing-only runs)
- [ ] every referenced upstream artefact (`01_inventory/`, `02_programs/`, `03_flows/`, `04_modules/`, optional `05_brds/`) is at or above `approved_with_non_blocking_tbd`
- [ ] every `EV-*` referenced in the spec / BRD resolves in the evidence manifest and has `sensitivity` ≠ `unknown` and an SME-approved `redaction_status`
- [ ] every approved `BR-*` links to ≥1 `EV-*`, ≥1 `BEH-*`, and ≥1 `AC-*`
- [ ] every `AC-*` validates at least one existing, approved `BR-*` (or carries an SME waiver)
- [ ] every `DEC-*` rationale references at least one of `BR-*`, `BEH-*`, or an explicit platform / regulatory constraint
- [ ] every `TC-*` validates ≥1 `AC-*` or `BR-*` and, when claiming a golden master, names an `EV-*` for sample data
- [ ] for `pass`, no open `TBD-*` remains; for `pass_with_warnings`, every open `TBD-*` carries a category, resolver, and non-blocking or explicitly deferred status
- [ ] for `pass`, no orphan `EV-*`; for `pass_with_warnings`, every orphan `EV-*` is explicitly SME-waived in `spec-review.md`
- [ ] no dangling ID in any cross-reference field
- [ ] `traceability-package.yaml` contains no values that are not derivable from upstream artefacts or this run's findings
- [ ] handoff cross-check passes (if an `06_sdd_handoffs/<CAP>/` package exists, its IDs match the spec; the traceability package neither overwrites nor contradicts it)
- [ ] package sign-off block present (packager + capability SME) with name, role, and ISO date

If even one box is unchecked, the package is `blocked` and the only files written are `traceability-review.md` and `blocking-findings.yaml`.

## Runtime Portability

Canonical source: `skills/legacy-traceability-packager/`. Runtime adapters under `.claude/skills/`, `.codex/skills/`, `.opencode/skills/`, and `.agents/skills/` are produced by `scripts/sync-skills.sh` and must not be edited directly.

## Maintenance and Versioning

- **Current Version**: 0.1.2
- **Last Updated**: 2026-05-28
- **Author**: Leo L Zhang
- **Status**: field-pilot ready; three-runtime smoke passed in Codex, Claude Code, and OpenCode

Version history:

- v0.1.2 (2026-05-28): Added `brd_functional_coverage` audit output when a
  BRD is supplied. Required BRD sections 1-9 must appear exactly once, with
  blocked or missing section coverage raised as traceability findings.

- v0.1.1 (2026-05-16): Tightened status semantics so clean `pass` has no findings, aligned package IDs with shared ID conventions, corrected the positive example to remove open TBDs, clarified AC validation and blocked-run continuation rules, and passed three-runtime smoke in Codex CLI (`gpt-5.4-mini`), Claude Code (`haiku`), and OpenCode (`minimax-m2.5-free`).
- v0.1.0 (2026-05-16): Initial release. Eight-step audit workflow producing `traceability-package.yaml` + `traceability-package.md` + `coverage-audit.md` + `traceability-review.md`. Strict block-by-default discipline. Reuses upstream IDs; mints only `FIND-*` and `PKG-*`. Three adversarial examples (positive, dangling-id blocked, deferred-TBD warning).
