<!--
Legacy Spec Factory
Copyright 2026 Leo L Zhang

Original author: Leo L Zhang
License: Apache License 2.0
-->

# Anti-Hallucination Rules for Traceability Packaging

This document lists what `legacy-traceability-packager` must **refuse to invent**. It is referenced from `SKILL.md` and from `references/workflow.md` (Step 8a).

## Golden Rule

**The traceability package is a sealed audit, not a generator.** The skill validates, indexes, and routes; it never invents business content. Every ID in the output already exists upstream, except for `FIND-*` (findings raised by this run) and `PKG-*` (the package's own ID).

If you find yourself drafting a missing `BR-*`, completing a half-written `AC-*`, paraphrasing a `TBD-*`, or "tidying up" a dangling reference, you are in the wrong skill. Stop, raise a `FIND-*`, and route to the owning upstream skill.

## What the Packager Must NOT Invent

### 1. Business rules, behaviors, decisions

❌ **DO NOT**:

- mint a new `BR-*`, `BEH-*`, or `DEC-*`;
- promote a `BR-*` / `BEH-*` / `DEC-*` `review_status` from `needs_sme_review` or `draft` to `approved`;
- merge two `BR-*` into one or split one into two;
- rewrite, paraphrase, or normalise the `rule`, `statement`, or `decision` text.

✅ **DO**:

- copy the upstream record verbatim into `business_rule_coverage` / `behavior_coverage` / `decision_coverage`;
- raise `BR-NO-EVIDENCE`, `BR-NO-BEHAVIOR`, or `BR-MISSING-AC` as a blocking finding and route to `legacy-spec-writer`.

### 2. Acceptance criteria

❌ **DO NOT**:

- generate a new `AC-*` to close an approved `BR-*` that is missing one;
- rewrite or clarify AC wording (acceptance criteria belong to the capability-owner SME via `legacy-spec-writer`);
- invent a SME waiver to demote `AC-NOT-APPROVED` to a warning.

✅ **DO**:

- raise `BR-MISSING-AC` (blocking) and route to `legacy-spec-writer`;
- record an existing, named SME waiver only when it is already present in `spec-review.md` with AC ID, reason, and ISO date.

### 3. Evidence

❌ **DO NOT**:

- create a new `EV-*` record in the manifest or in the package;
- reclassify `sensitivity` (e.g. silently treat `unknown` as `internal`);
- assume a `redacted_filename` / approved analysis path when one is missing;
- assume source-path authorization when `source_path_verified` is not `true`;
- hide an orphan `EV-*` by deleting it from the inventory.

✅ **DO**:

- copy every manifest field verbatim into `evidence_coverage`;
- raise `EVIDENCE-SENSITIVITY-UNKNOWN`, `EVIDENCE-AWAITING-REDACTION`,
  `EVIDENCE-SOURCE-NOT-AUTHORIZED`, or `EVIDENCE-APPROVED-PATH-MISSING`
  (all blocking) and route to `legacy-ibmi-evidence-intake`;
- record orphan `EV-*` either as a warning (`ORPHAN-EVIDENCE`) or, when the spec / BRD claims full closure, as `ORPHAN-EVIDENCE-IN-CLOSURE-PACKAGE` (blocking).

### 4. Test cases

❌ **DO NOT**:

- generate a new `TC-*` to cover an `AC-*` that has none;
- invent a `sample_data_evidence_id` when the spec leaves it empty;
- flip `golden_master_enabled` to `true` because "it makes the metrics look better".

✅ **DO**:

- copy every `TC-*` row verbatim;
- raise `TC-DANGLING-VALIDATES` or `EV-DANGLING-IN-TC` (blocking) when the spec is inconsistent;
- route TC gaps to `legacy-golden-master-test-planner` or `legacy-spec-writer`.

### 5. Open questions / TBDs

❌ **DO NOT**:

- resolve a `TBD-*` that the spec leaves open;
- demote `blocking: true` to `blocking: false`;
- merge multiple `TBD-*` into one;
- paraphrase the `question`, `resolution`, or `resolver` text.

✅ **DO**:

- carry every `TBD-*` forward verbatim;
- apply the deferral predicate from `references/workflow.md` Step 7 mechanically — all four fields plus `deferral_recorded_in` must be present to warrant a warning rather than a block;
- route every remaining TBD to its named resolver.

### 6. Findings and severity

❌ **DO NOT**:

- demote a blocking finding to a warning to make the status `pass_with_warnings`;
- promote a warning to an info finding because the SME is busy;
- combine multiple findings into one to reduce the count.

✅ **DO**:

- raise one `FIND-*` per distinct rule violation;
- use the catalog in `references/output-contract.md` — adding a new rule requires editing that file first;
- record SME-waivers verbatim only when they exist in `spec-review.md` or `brd-review.md`.

### 7. Sign-offs and status

❌ **DO NOT**:

- invent SME names or roles;
- backdate `approved_date`;
- promote `traceability-package` status from `blocked` to `pass_with_warnings` without rerunning the gate;
- emit a `traceability-package` sign-off block when the status is `blocked`.

✅ **DO**:

- copy spec / BRD approvers from their review documents verbatim;
- write the packager validator block deterministically from this run's version and timestamp;
- require an explicit capability-owner SME sign-off for `pass` and `pass_with_warnings` outcomes.

### 8. Routing

❌ **DO NOT**:

- recommend an architecture, framework, deployment topology, or test strategy;
- decide what Atlas should build, even at a high level;
- mark a finding "resolved" because routing it would be inconvenient.

✅ **DO**:

- for every finding, name the responsible upstream skill (`legacy-spec-writer`, `legacy-brd-writer`, `legacy-ibmi-evidence-intake`, `legacy-ibmi-inventory`, `legacy-ibmi-program-analyzer`, `legacy-ibmi-flow-analyzer`, `legacy-ibmi-module-analyzer`, `legacy-brd-to-sdd-handoff`, or `legacy-golden-master-test-planner`);
- quote the remediation text from the rule definition, not paraphrased prose;
- defer architecture and design questions to the Atlas SDD chain via `legacy-brd-to-sdd-handoff`.

### 9. Handoff cross-check

❌ **DO NOT**:

- modify, overwrite, or replace `06_sdd_handoffs/<CAP>/` files;
- silently reconcile differences between the handoff and the spec;
- claim alignment when wording differs.

✅ **DO**:

- read the handoff for cross-check;
- raise `HANDOFF-ID-MISMATCH` (blocking) when a `BR-*` / `AC-*` / `EV-*` differs in wording, status, or membership;
- route the mismatch to `legacy-brd-to-sdd-handoff` and `legacy-spec-writer` so the upstream artefact is reconciled.

### 10. Output discipline

❌ **DO NOT**:

- write a fifth file beyond the four (or two for blocked);
- write into `05_specs/`, `05_brds/`, `06_sdd_handoffs/`, or any upstream directory;
- emit partial packages on `blocked`.

✅ **DO**:

- on `pass` / `pass_with_warnings`: write exactly four files into `06_traceability_packages/<SLUG>/`;
- on `blocked`: write exactly two files into `06_traceability_packages/<SLUG>/`;
- treat the canonical source under `skills/legacy-traceability-packager/` as the only authoritative version; sync via `scripts/sync-skills.sh` after any change.

## Hallucination Check (Run Before Sign-Off)

Before finalising the package, ask of every field:

- [ ] Does this field come directly from the spec, BRD, evidence manifest, or an upstream analysis?
- [ ] If it is a coverage row, is every ID inside it already present in `id_inventory`?
- [ ] If it is a finding, does its rule appear verbatim in `references/output-contract.md`?
- [ ] If it is a sign-off, does the name + role + ISO date come from an upstream review document or from this run's deterministic packager block?
- [ ] If it is a status, does it match the actual findings (no demotion, no promotion)?

If you answer **no** to any of these, **delete the field and raise a `FIND-*` instead.**
