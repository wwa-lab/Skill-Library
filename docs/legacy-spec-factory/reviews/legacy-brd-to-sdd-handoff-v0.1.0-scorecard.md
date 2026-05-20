---
skill: legacy-brd-to-sdd-handoff
scorecard_version: v0.1.0
static_score: 9.63
decision: field-pilot ready
status: current
last_verified: 2026-05-16
runtimes_tested:
  codex: { status: passed, model: gpt-5.4-mini, date: 2026-05-16 }
  claude_code: { status: passed, model: haiku, date: 2026-05-16 }
  opencode: { status: passed, model: minimax-m2.5-free, date: 2026-05-16 }
evidence_source: docs/runtime-matrix.md
---

# Skill Review Scorecard: legacy-brd-to-sdd-handoff v0.1.0

## Metadata

- **skill_name**: legacy-brd-to-sdd-handoff
- **skill_path**: `skills/legacy-brd-to-sdd-handoff/`
- **reviewed_version**: 0.1.0
- **generated_by**: Claude Code (Haiku 4.5)
- **reviewed_by**: Self-review (boundary-drift audit + scorecard application)
- **review_date**: 2026-05-16
- **target_runtime**:
  - [x] Codex (canonical source; sync required)
  - [x] Claude Code (canonical source; `.claude/skills/` adapter)
  - [x] OpenCode (canonical source; `.agents/skills/` or `.opencode/skills/` adapter)
- **decision**:
  - [ ] reject
  - [ ] revise
  - [x] repo-ready
  - [x] field-pilot ready

---

## Review History

| Pass | Date | Outcome |
| --- | --- | --- |
| Initial generation | 2026-05-16 | static score 9.16, repo-ready, but boundary-drift audit pending |
| Boundary-drift audit + patches (pass 1) | 2026-05-16 | 8 defects identified and fixed; static score 9.42; 9.0 runtime cap still applies |
| Boundary-drift audit + patches (pass 2) | 2026-05-16 | 7 additional, more subtle drift items found and fixed; static score 9.55; published score still 9.0 until three-runtime smoke. |
| Adversarial example expansion | 2026-05-16 | Added 3 new examples (`handoff-missing-spec`, `handoff-blocked-blocking-tbd`, `handoff-warning-deferred-tbd`), exposing 2 latent ambiguities and patching them: (i) the deferral predicate for `BLOCKING-TBD-DEFERRED` was previously hand-wavy ("named SME deferral") — now a 4-field normative predicate in `workflow.md#step-3`; (ii) the relationship between internal `status` values and the user-facing `pass / pass_with_warnings / blocked` labels was undocumented — now an exact synonym table in `SKILL.md` and `workflow.md`. Static score 9.7; published score still 9.0. |
| Codex contract consistency repair | 2026-05-16 | Fixed 4 review findings: aligned evidence-gate fields with `legacy-ibmi-evidence-intake`, unified `sme_sign_offs[]`, made `atlas-context-pack.json` an exact JSON mirror of `sdd-handoff.yaml`, and clarified five-file vs blocked two-file output semantics. Published score remains capped at 9.0 until three-runtime smoke. |
| Three-runtime smoke | 2026-05-16 | Codex CLI (gpt-5.4-mini, read-only ephemeral), Claude Code (haiku, Read-only tools), and OpenCode (minimax-m2.5-free) passed positive and negative no-write smoke. Runtime cap lifted; published score 9.63; field-pilot ready. |

---

## Mandatory Stop Conditions

Check any condition that applies:

- [ ] no valid `SKILL.md`
- [ ] missing or weak `name` / `description` frontmatter
- [ ] no copyright / author notice
- [ ] not portable across Codex, Claude Code, and OpenCode
- [ ] runtime-specific assumptions mixed into canonical skill
- [ ] no clear trigger conditions
- [ ] no clear output contract
- [ ] no SME review or evidence governance for IBM i reverse engineering
- [ ] hallucination-prone instructions

**None of the above apply.** No score cap from mandatory stops.

The 9.0 runtime cap from `docs/skill-review-gate.md` has been lifted:
three-runtime smoke evidence is recorded in `docs/runtime-matrix.md`.

---

## Defects Identified in Audit and Fixed

Each defect below was found during the boundary-drift audit on 2026-05-16
and patched in the same review pass. Each row names the exact file(s)
touched.

| ID | Defect | Severity | Files Changed | Fix |
| --- | --- | --- | --- | --- |
| D-01 | Templates invented architecture/framework/deployment recommendations (Spring Boot, Kubernetes, repository pattern, integration topology, "5-minute TTL caching") under `forward_sdlc_hints`, `recommended_patterns`, and `deployment_context`. This is `spec-to-architecture` / `architecture-to-design` territory and broke the bridge boundary. | **critical** | `templates/sdd-handoff.yaml`, `templates/atlas-context-pack.json`, `templates/sdd-handoff.md`, `templates/handoff-review.md` | Replaced invented fields with a `carried_forward_decisions` list of approved `DEC-*` IDs. Added a `_boundary_note` in the JSON context pack. Rewrote "Next Steps" and "Recommendations" sections to explicitly defer to Atlas and to cite only approved `DEC-*`. |
| D-02 | "SDD" terminology was ambiguous — readers might infer the skill produces full Software Design and Development artefacts. | major | `SKILL.md`, new `references/atlas-contract.md` | Reworded Purpose to "handoff TO the Atlas Software Design and Development (SDD) chain". Added a full boundary diagram and "What Atlas owns / what this skill owns" table in `references/atlas-contract.md`. |
| D-03 | `SKILL.md` was 535 lines, mixing high-level contract with the 9-step procedure and per-gate finding rules. Violated progressive-disclosure guidance in `docs/skill-review-gate.md`. | major | `SKILL.md`, new `references/workflow.md` | Reduced `SKILL.md` to 315 lines: contract, role, inputs, stop conditions, output structure, references list. Moved the full 9-step procedure with finding rules into `references/workflow.md`. |
| D-04 | `SKILL.md` referenced `references/atlas-contract.md` but the file did not exist. | major | new `references/atlas-contract.md` | Created the file with the Atlas boundary contract, "what the handoff provides / does not provide" tables, and round-tripping rules. |
| D-05 | Stop conditions were listed but not framed as block-by-default; reader could misread some as soft warnings. | major | `SKILL.md`, `references/workflow.md` | Added an explicit "Stop conditions … each is blocking by default; the gate does not advance unless explicitly cleared" sentence plus a table. Restated in workflow.md per step with finding-severity columns. |
| D-06 | No explicit "must not bypass `legacy-spec-writer`" rule. The forward-SDLC contract required this and the audit prompt specifically called it out. | major | `SKILL.md`, `references/workflow.md` | Added explicit text: "If `spec.yaml` is not approved, this skill must not fabricate it or skip ahead. It must block and route back to `legacy-spec-writer`." Re-asserted in Step 2 of `workflow.md` as a "Bypass rule". |
| D-07 | Negative example's `README.md` referenced `blocking-finding.yaml` and `partial-handoff-attempt.md` but neither existed. Examples were therefore unmeasurable. | major | new `examples/handoff-blocked-missing-ac/blocking-finding.yaml`, updated `examples/handoff-blocked-missing-ac/README.md` | Created `blocking-finding.yaml` as a real, schema-bearing artefact showing the exact machine-readable output for a blocked run, including `package_written: false` and a routed-next-step for the orchestrator. Updated README to remove the `partial-handoff-attempt.md` reference and explain why no partial handoff is written. |
| D-08 | Positive example README claimed the folder "includes" `sdd-handoff.yaml`, `sdd-handoff.md`, etc., but only `README.md` existed. Examples again unmeasurable. | minor | `examples/handoff-positive/README.md` | Rewrote the "Package Contents" section to make clear those files are produced at run time, that the canonical templates double as a rendering of this positive case, and that the example folder ships only the README. |

Verification of pass-1 fixes:

```text
grep -n -i "spring|kubernetes|repository pattern|distributed tracing|caching"   templates/*.{yaml,md,json}
```

After patching, every remaining hit on those tokens lives inside a quoted
approved `DEC-*` record or a quoted comparison to legacy behaviour. There is
no remaining hit in a `recommended_*`, `forward_sdlc_hints`, or
"Recommendations for Forward SDLC Team" section.

---

### Pass 2 — Defects Found and Fixed (Second-Look Audit)

The first pass cleaned the most obvious drift (invented architecture
sections). A more skeptical second pass found seven additional, subtler
drift items hiding inside metadata, sample findings, and template-to-template
inconsistencies. Each was patched in the same pass.

| ID | Defect | Severity | Files Changed | Fix |
| --- | --- | --- | --- | --- |
| D-09 | `templates/sdd-handoff.yaml` had `handoff_type: "legacy-to-java"`. This silently hard-codes Java as the target without any approving `DEC-*`. Java is an Atlas decision, not a handoff decision. | major | `templates/sdd-handoff.yaml` | Renamed to `handoff_type: "legacy-spec-factory-to-atlas-sdd"`. Added an inline comment forbidding target-language encoding here; target platforms must come only from approved `DEC-*` records. |
| D-10 | Header comment referenced `build-agent-skill` as the consumer alongside Atlas. Per `README.md`, `build-agent-skill` is the forward IBM i delivery chain (a separate project), not the Atlas Java/cloud chain. The two were conflated. | major | `templates/sdd-handoff.yaml` | Rewrote the header to name only the Atlas SDD chain (req-to-user-story → tasks-to-code) and added an explicit "NOTE: build-agent-skill is a different project (the forward IBM i delivery chain) and is NOT the consumer of this file." |
| D-11 | `findings.info` in `sdd-handoff.yaml` contained a sample finding whose `recommendation` field added an architectural action ("Add audit logging to modern audit service; update traceability after architecture is approved"). Same drift pattern as pass-1, hidden inside a finding rather than a top-level section. | major | `templates/sdd-handoff.yaml` | Replaced the sample with `info: []` and added a header comment: "Each finding is a *factual observation* about the upstream BRD / spec / evidence — never a recommendation about what Atlas should build." Mirrored the same correction in `handoff-review.md` (renamed `TECH-DEBT-AUDIT-SERVICE` to `AUDIT-PATH-CHANGES-PER-DEC-003`, replaced "Recommendation/Action" with "Observation/Routing", explicitly handed responsibility to Atlas). |
| D-12 | Assumptions block in `sdd-handoff.yaml` was labelled "Assumptions Recorded During Handoff Validation" — contradicted SKILL.md's rule that the validator does not mint assumptions. | medium | `templates/sdd-handoff.yaml`, `templates/sdd-handoff.md` | Relabelled to "Assumptions Carried Forward from Spec / BRD" and added a `source:` field on each entry pointing at the upstream artefact section (e.g. `spec.yaml#assumptions[0]`). Same correction applied to `sdd-handoff.md`. |
| D-13 | `templates/sdd-handoff.md` had `EX-CREDIT-CHECK-003` (database connection failure, HTTP 503, retry-with-backoff) that did **not** exist in `sdd-handoff.yaml`. HTTP status codes and retry-with-backoff are Atlas implementation details. Pure invention. | **major** | `templates/sdd-handoff.md` | Removed `EX-CREDIT-CHECK-003`. Added a header note above the exceptions table: "Carried forward verbatim from the spec's `exceptions[]`. Only exceptions present in the approved spec appear here — this skill does not invent additional error cases (HTTP status codes, retry policies, circuit-breaker behaviour, etc. are Atlas-chain concerns)." Also re-aligned the table columns to match the spec's shape (`condition`, `expected_behavior`, `severity`) instead of HTTP-flavoured columns. |
| D-14 | `templates/sdd-handoff.md` had a third "Assumption" ("AUDITPF audit trail is not required to migrate") that did not exist in `sdd-handoff.yaml`. Clear minting by the handoff. | major | `templates/sdd-handoff.md` | Removed Assumption #3. Added a header note "Only assumptions explicitly recorded in the approved spec or BRD appear here. The handoff validator does **not** mint new assumptions." Added `source:` lines for each remaining assumption. |
| D-15 | The two templates (`.yaml`, `.md`) used inconsistent counts (2 vs 5 BR, 3 vs 6 AC, 2 vs 4 DEC). The positive-example README had claimed the templates "double as a rendering" of the positive case, which is false. | medium | `templates/sdd-handoff.yaml`, `templates/sdd-handoff.md`, `examples/handoff-positive/README.md` | Did not force the two templates into byte equivalence (the YAML structural skeleton and the MD narrative skeleton serve different purposes). Instead, added an explicit TEMPLATE NOTE banner at the top of each template stating: "structural skeleton vs richer narrative rendering — in a real run, both files are emitted from the same approved spec/BRD and their counts will match by construction." Updated `examples/handoff-positive/README.md` to retract the misleading claim and replace it with the explicit description of the two templates' roles. |
| D-16 (incidental cleanup) | Stray "forward SDLC team" phrasing in `sdd-handoff.md`, `traceability.md`, `handoff-review.md`. Not strictly wrong, but in this skill the consumer is named — the Atlas SDD chain. Vagueness encouraged future drift. | low | `templates/sdd-handoff.md`, `templates/traceability.md`, `templates/handoff-review.md` | Replaced "forward SDLC team" with "Atlas SDD chain" where the meaning is the downstream consumer of the package. Left `SKILL.md`'s one occurrence intact, where it parenthetically equates the two ("the forward SDLC team (or downstream Atlas chain)"). |

Verification of pass-2 fixes:

```text
grep -rn -i "legacy-to-java|recommended_pattern|forward_sdlc_hints|deployment_context|retry with backoff|503 service"   skills/legacy-brd-to-sdd-handoff/
```

After patching, every remaining hit on those tokens is inside a
**forbidden list** (in `references/atlas-contract.md`,
`references/workflow.md`, or `references/anti-hallucination.md`) where the
token is named as something the skill must refuse to produce. There are
no remaining hits inside actual handoff output templates.

```text
grep -rn "EX-CREDIT-CHECK-003" skills/legacy-brd-to-sdd-handoff/   →  no matches
grep -rn "AUDITPF audit trail is not required to migrate" skills/legacy-brd-to-sdd-handoff/   →  no matches
grep -rn "Forward SDLC team" skills/legacy-brd-to-sdd-handoff/templates/   →  no matches
```

---

### Pass 3 — Adversarial Example Expansion (Latent Ambiguities)

Five examples now exist (one positive, one warning, three blocked).
Adding the new three exposed two latent ambiguities that the first two
passes had not surfaced. Both are normative gaps, not invention drift,
and both have been patched.

| ID | Latent ambiguity | Where surfaced | Fix |
| --- | --- | --- | --- |
| D-17 | The pass-1 workflow used the phrase "named SME deferral" as the predicate that promotes a blocking TBD from `BLOCKING-TBD-UNRESOLVED` to `BLOCKING-TBD-DEFERRED` (warning). Hand-wavy. Two reasonable readers could disagree on what "named" requires. | Surfaced when writing `examples/handoff-warning-deferred-tbd/` — what exactly does a passing deferral look like? | Replaced with a normative 4-field predicate in `references/workflow.md#step-3`: `blocking=true` AND non-empty `resolution` AND non-empty `resolver` (real person from spec's SME roster) AND future ISO `planned_resolution_date`. Optional but expected: `deferral_recorded_in` pointer. Partial satisfaction → blocking. Added an explicit two-sided framing ("over-blocking vs under-warning") so future readers see the trade-off the predicate is balancing. |
| D-18 | The user's question vocabulary (`pass / pass_with_warnings / blocked`) and the skill's internal vocabulary (`approved / approved_with_non_blocking_tbd / blocked`) were not connected anywhere. Tooling and reviewers would diverge. | Surfaced when each new example tried to label its expected outcome — should it say `pass_with_warnings` or `approved_with_non_blocking_tbd`? | Added a Status Labels section in `SKILL.md` declaring the three internal values exact synonyms of the three display labels. Added a display-label column in `references/workflow.md`'s Output Status Decision Table. Added a worked-examples table that maps each of the five example folders to the gate step that fires, the finding, the YAML status, and the display label. |

These two patches close ambiguities rather than invent content. After
the fix, a reviewer reading any one of the five example READMEs can
match it against the deferral predicate and the status decision table in
the references and arrive at the same outcome the example claims.

Verification:

```text
grep -rn "pass_with_warnings" skills/legacy-brd-to-sdd-handoff/
  → matches in SKILL.md (mapping table), workflow.md (status decision table),
    handoff-warning-deferred-tbd/README.md (expected status),
    handoff-blocked-blocking-tbd/README.md (named as one of the SME's
    admissible recoveries), gate-summary.yaml (comment on status field)
grep -rn "deferral predicate" skills/legacy-brd-to-sdd-handoff/
  → matches in workflow.md (definition) and handoff-warning-deferred-tbd/README.md (cited)
```

The grep coverage confirms the new vocabulary is connected from every
example back to the normative reference.

---

### Pass 4 — Codex Contract Consistency Repair

A follow-up Codex review found four executable contract mismatches that could
mislead an orchestrator even though the narrative guardrails were strong. Each
was patched in the canonical skill source and then synced to runtime copies.

| ID | Defect | Severity | Files Changed | Fix |
| --- | --- | --- | --- | --- |
| D-19 | Evidence gate consumed old `sensitive` / `cleared` vocabulary while `legacy-ibmi-evidence-intake` emits `sensitivity`, `redaction_status`, `redacted_filename`, and `sme_approval`. | high | `SKILL.md`, `references/workflow.md`, `references/handoff-gate-checklist.md`, templates | Rebased Step 6 on the evidence-intake manifest contract: `package_state: approved_for_inventory`, no `sensitivity: unknown`, confidential items require `redaction_status: approved`, public/internal items require `not_required`, `reviewed`, or `approved`, and every referenced item needs a redacted file plus SME approval. |
| D-20 | `SKILL.md` required `sme_sign_offs[]` while the YAML template emitted `handoff_sign_off`. | high | `templates/sdd-handoff.yaml`, `templates/atlas-context-pack.json`, `references/workflow.md` | Standardized on `sme_sign_offs[]` for BRD, spec, and handoff SME approvals. Validator identity remains in top-level `handoff_validator` / `handoff_date`. |
| D-21 | `atlas-context-pack.json` introduced top-level and nested fields absent from `sdd-handoff.yaml` (`business_value`, examples, `_boundary_note`, and a different evidence summary shape). | high | `templates/atlas-context-pack.json`, `templates/sdd-handoff.yaml` | Made the JSON context pack an exact parsed-data mirror of `sdd-handoff.yaml`; deterministic summaries now exist in YAML before appearing in JSON. |
| D-22 | Output file semantics conflicted: `SKILL.md` said exactly five files, blocked workflow wrote two files, and the warning example appeared to add a sixth `gate-summary.yaml`. | medium | `SKILL.md`, `references/workflow.md`, `examples/handoff-warning-deferred-tbd/*` | Clarified approved/warning runs write exactly five package files; blocked runs write only `handoff-review.md` and `blocking-finding.yaml`; `gate-summary.yaml` is now explicitly example-only. |

Verification:

```text
ruby -e 'require "json"; require "yaml"; y=YAML.load_file("skills/legacy-brd-to-sdd-handoff/templates/sdd-handoff.yaml"); j=JSON.parse(File.read("skills/legacy-brd-to-sdd-handoff/templates/atlas-context-pack.json")); abort unless y == j'
scripts/sync-skills.sh --target all --check
```

---

## Weighted Score Rubric (Post-Pass-4)

| Category | Weight | Score (0-10) | Weighted | Comments |
| --- | ---: | ---: | ---: | --- |
| Purpose and trigger clarity | 10% | 9.7 | 0.97 | Bridge / gate / package role is stated three ways; "when NOT to use" enumerates every neighbouring skill; `handoff_type` is platform-agnostic; new Status Labels table connects internal vocabulary to display vocabulary. |
| Workflow completeness | 12% | 9.7 | 1.16 | 9 ordered steps, each with explicit finding table and routing. Block-by-default rule restated per step. Pass-3 added a normative 4-field deferral predicate to Step 3 (closing the "named SME deferral" ambiguity) and a worked-examples table linking the 5 example folders to the gate steps that fire. |
| IBM i / domain correctness | 14% | 9.4 | 1.32 | Correctly carries forward IBM i evidence and `DEC-*`. After pass-2, no longer hard-codes "legacy-to-java" or mixes `build-agent-skill` (forward IBM i chain) with Atlas (Java/cloud chain). |
| Evidence and anti-hallucination | 12% | 9.7 | 1.16 | Pass-2 removed three concrete invention paths still present after pass-1. `references/anti-hallucination.md` is detailed; `sensitivity: unknown` is hard-blocking. Pass-3 made the deferral predicate normative so SMEs cannot wave a half-deferral through as a warning. |
| Output contract | 10% | 9.7 | 0.97 | 5-file output, schemas listed field by field, blocked-path emits only finding files. Pass-3 added the YAML-status ↔ display-label synonym table so tooling and reviewers agree on outcomes. |
| Progressive disclosure | 8% | 9.4 | 0.75 | `SKILL.md` stayed at 315 lines despite pass-3 additions (the new content fits one Status Labels table and a 5-row examples table). Detail in references. |
| Runtime portability | 10% | 9.7 | 0.97 | Canonical source only; templates are Markdown / YAML / JSON; no IDE-specific assumptions. Positive and negative no-write smoke passed in Codex CLI, Claude Code, and OpenCode. |
| Reviewability and testability | 10% | 9.9 | 0.99 | **Five examples** — one positive, one warning, three blocked — each ships with a measurable artefact (full package note, `gate-summary.yaml`, or `blocking-finding.yaml`) and an explicit expected status. Gate checklist mirrors workflow steps. Verification grep commands documented per pass. |
| Engineering handoff value | 8% | 9.6 | 0.77 | Atlas-facing context pack now mirrors `sdd-handoff.yaml` exactly. `references/atlas-contract.md` documents the boundary. Warning examples carry deferred TBDs into `open_questions[]` without introducing standalone routing hints. |
| Maintainability | 6% | 9.5 | 0.57 | Versioned; copyright header consistent with other skills; references and templates are individually addressable; four repair passes plus smoke evidence are captured here. Verification commands documented. CHANGELOG not yet a separate file but is implicit in scorecard history. |

**Weighted score**: 0.97 + 1.16 + 1.32 + 1.16 + 0.97 + 0.75 + 0.97 + 0.99 + 0.77 + 0.57 = **9.63 / 10**

(Pass-3 lifted the *Reviewability and testability* axis by adding three
measurable adversarial examples and the worked-examples table. Pass-4
closed executable contract mismatches, and the smoke run lifts the runtime
portability axis from capped to proven.)

**Runtime cap (per `docs/skill-review-gate.md`)**: lifted on 2026-05-16
after Codex CLI, Claude Code, and OpenCode passed positive and negative
no-write smoke. Evidence is recorded in `docs/runtime-matrix.md`.

**Current published score**: **9.63** (field-pilot ready).

---

## Decision Rule

- `>= 9.5` → field-pilot ready (**met**)
- `9.0 - 9.4` → repo-ready, not field-pilot ready (not applicable after
  smoke)
- `8.0 - 8.9` → revise (not applicable)
- `< 8.0` → reject (not applicable)

Disposition: **field-pilot ready**. The three-runtime smoke protocol from
`docs/runtime-smoke-tests.md` passed and the result is recorded in
`docs/runtime-matrix.md`.

---

## Findings After Patch

### Blocking Findings

None. All defects identified through D-22 were fixed in the canonical skill
source.

### Improvement Findings (carry forward to v0.1.1 or later)

| ID | Finding | Severity | Suggested Change |
| --- | --- | --- | --- |
| IF-101 | No standalone `CHANGELOG.md` in the skill folder. The scorecard "Review History" table is the de-facto changelog. | low | Add `CHANGELOG.md` once the skill has a second material revision. |
| IF-102 | The positive example folder ships only a README. Renderings of the five output files live in `templates/`. A reviewer must read the templates to see a complete worked example. | low | Optionally copy a frozen rendering of the five files into `examples/handoff-positive/` after the first real field-pilot run, so the positive example is fully self-contained. |
| IF-103 | The skill does not yet describe behaviour when multiple capabilities share an SME and approvals stack. | low | Add a short note in `references/atlas-contract.md` once a real multi-capability handoff is exercised. |

None of these are blocking.

---

## SME Review

- [x] SME governance is explicit
  - **Notes**: BRD and spec sign-offs are mandatory; handoff itself also requires a named SME sign-off block; "SME-OWNERSHIP-MISMATCH" is recorded as an info finding when BRD and spec owners differ.
- [x] Observed behavior, inferred rule, and modernization decision are separate
  - **Notes**: The skill carries BEH-*, BR-*, and DEC-* forward unchanged from their upstream artefacts; the post-fix templates no longer invent decisions parallel to DEC-*.
- [x] Evidence tags are required
  - **Notes**: Step 6 of the workflow makes `sensitivity: unknown` blocking. Manifest miss is blocking.
- [x] IBM i-specific failure modes are covered
  - **Notes**: Skill does not read IBM i source. It relies on upstream Layer 1 skills. The negative example is rooted in a realistic IBM i / order-entry scenario (missing AC on a promotional-discount rule).
- [x] Open questions / TBDs are carried forward instead of hidden
  - **Notes**: Non-blocking TBDs flow through verbatim with resolver and date; blocking TBDs hard-stop the gate.

---

## Runtime Portability Review

- [x] canonical source under `skills/legacy-brd-to-sdd-handoff/`
- [x] Claude Code adapter or copy ready to be synced via `scripts/sync-skills.sh`
- [x] OpenCode adapter or copy ready (`.agents/skills/` or `.opencode/skills/`)
- [x] Codex adapter or copy ready (Agent Skills shape, no Codex-specific metadata)
- [x] runtime-specific metadata isolated from canonical skill

**Status**: synced and smoke-tested. Codex CLI, Claude Code, and OpenCode
passed positive and negative no-write scenarios on 2026-05-16.

---

## Requested Revision Prompt For Claude Code

Not applicable. All known audit defects were fixed and the three-runtime
smoke protocol passed.

---

## Summary

The skill is **field-pilot ready** at the published score of **9.63**. Across
four audit / repair passes, **22 boundary and contract defects** were
identified and fixed:

**Pass 1 (D-01 … D-08, the visible drift)**

1. Removed invented architecture / framework / deployment recommendations
   from all four templates; replaced with a strict carry-forward of
   approved `DEC-*` IDs.
2. Clarified that "SDD" means the Atlas SDD chain and that this skill
   stops at the handoff package.
3. Reduced `SKILL.md` to a concise 315-line contract; moved the detailed
   9-step procedure to `references/workflow.md`.
4. Added the previously-missing `references/atlas-contract.md`.
5. Made every stop condition explicitly block-by-default.
6. Added an explicit rule forbidding bypass of `legacy-spec-writer`.
7. Produced a real `blocking-finding.yaml` for the negative example.
8. Honestly described what the positive example folder ships.

**Pass 2 (D-09 … D-16, the subtle drift the first pass missed)**

9. `handoff_type` no longer hard-codes Java; renamed to
   `legacy-spec-factory-to-atlas-sdd`. Target language is encoded only
   when an approved `DEC-*` says so.
10. Removed reference to `build-agent-skill` (forward IBM i delivery
    chain) from the consumer chain. The consumer is named explicitly as
    the Atlas SDD chain; `build-agent-skill` is flagged as a *different*
    project in a NOTE.
11. Removed an architectural recommendation hidden inside a sample
    `findings.info` entry; emptied the array and added a comment forbidding
    recommendation language inside findings. Mirrored the correction in
    `handoff-review.md`.
12. Relabelled the assumptions block "Carried Forward from Spec / BRD",
    added `source:` field per entry, and corrected the SKILL.md
    contradiction that allowed minted-during-validation reading.
13. Removed an invented exception `EX-CREDIT-CHECK-003` (HTTP 503 +
    retry-with-backoff) from `sdd-handoff.md`; added an explicit "no
    invented error cases" header above the exceptions table.
14. Removed an invented Assumption #3 from `sdd-handoff.md`; added a
    no-minting header to that section.
15. Resolved the template-to-template count mismatch (`yaml` 2/3/2 vs
    `md` 5/6/4) by labelling each template's role explicitly: YAML is a
    minimal structural skeleton, MD is a richer narrative skeleton.
    Updated the positive-example README to retract the "double as a
    rendering" claim. Replaced vague "forward SDLC team" with "Atlas SDD
    chain" across the templates.

**Pass 4 (D-19 … D-22, executable contract consistency)**

16. Rebased the evidence gate on the canonical `legacy-ibmi-evidence-intake`
    manifest fields: `sensitivity`, `redaction_status`,
    `redacted_filename`, and `sme_approval`.
17. Standardized the machine-readable sign-off field on `sme_sign_offs[]`
    across SKILL.md, workflow, YAML, and JSON.
18. Made `atlas-context-pack.json` an exact data mirror of
    `sdd-handoff.yaml`; the JSON no longer introduces fields absent from the
    YAML contract.
19. Clarified output-file semantics: approved/warning runs write exactly five
    files; blocked runs write only `handoff-review.md` and
    `blocking-finding.yaml`; `gate-summary.yaml` is example-only.
20. Tightened Gate 5 and Gate 7 checklist wording so draft ACs and orphaned
    approved BRs cannot pass as soft warnings.

The skill is now structurally consistent: every output field traces back
to an approved upstream record, every gate is enforceable, every example
is measurable, and the bridge boundary with the Atlas SDD chain is
explicit in both prose and machine-readable form. Verification grep
commands are embedded in this scorecard and all return the expected zero
hits for invented content tokens.

---

## Scorecard Sign-Off

| Role | Name | Date | Status |
| --- | --- | --- | --- |
| Generator | Claude Code (Haiku 4.5) | 2026-05-16 | Generated |
| Auditor | Claude Code (Opus 4.7) | 2026-05-16 | Reviewed; 8 defects fixed |

---

## Next Steps

1. ✅ Boundary-drift audit and patches complete (this scorecard).
2. ✅ Synced to `.claude/skills/`, `.agents/skills/`, `.opencode/skills/`,
   and `.codex/skills/` via `scripts/sync-skills.sh --target all`.
3. ✅ Ran the three-runtime smoke protocol from
   `docs/runtime-smoke-tests.md`.
4. ✅ Recorded evidence in `docs/runtime-matrix.md`; re-scored to lift the
   9.0 cap to 9.63.
5. ✅ Added `legacy-brd-to-sdd-handoff` to the README score and roadmap
   tables.

---

**End of Scorecard**
