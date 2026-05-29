---
name: legacy-sme-review-facilitator
description: Use when a BRD, spec, module analysis, or other Legacy Spec Factory artifact needs documented SME validation, especially when the SME should answer guided review questions directly in chat and have decisions written back to review artifacts.
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

# Legacy SME Review Facilitator

## Purpose

Enable structured SME review and decision capture across the Legacy Spec Factory
pipeline without substituting AI judgment for human expertise.

This skill is a **facilitator and recorder**, not a decision maker. It:

- **Runs Conversation Review Mode** so the SME can answer guided questions in
  the chat instead of editing files or sending email
- **Prepares** review sessions by organizing questions from open items
  (`TBD-*`, `BR-*` seeds needing confirmation, `VAL-*` scenario seeds,
  contradictory evidence)
- **Checks BRD functional-analysis coverage** when the artifact is a BRD
  Package, so SME-required sections 1-9 are explicitly reviewed instead of
  being implied by rule / behavior questions alone
- **Facilitates** SME sessions by collecting structured answers
- **Records** decisions so they trace back to stable IDs and evidence
- **Writes back** recorded decisions to the BRD Package when reviewing BRD
  artifacts
- **Captures** sign-offs with SME name, role, and date
- **Surfaces** unresolved items (follow-up findings) for next steps

It does **not**:

- approve business rules or modernization decisions on the SME's behalf
- invent evidence, object names, behavior claims, or business context
- resolve TBDs by inference or assumption
- promote draft or `needs_sme_review` items to `approved` without explicit SME
  sign-off
- silence contradictions or downgrade blocking findings
- execute downstream skills (that is the SME's or orchestrator's role)

## When to Use

Trigger on any of these signals:

- A BRD, spec, module analysis, or other business artifact is **ready for SME
  review and sign-off** but questions remain unresolved
- **Inferred rules or ambiguous items** need structured validation before the
  artifact can advance (e.g., `BR-*` seeds with `needs_sme_review` status)
- **Open TBDs** need SME judgment to mark as `blocking` or `non_blocking`, or to
  resolve if possible
- **Contradictory evidence** needs SME clarification (e.g., two programs
  implement different rounding rules)
- **Observed behavior** needs SME confirmation that it reflects actual business
  intent, not a bug or legacy workaround
- A **decision log** needs to be created and sealed so downstream teams can
  trace decisions back to SME approval and evidence
- The user wants to stay in one chat while reviewing a BRD Package, answering
  confirm / reject / needs evidence / non-blocking choices with optional
  comments

## When NOT to Use

Do not trigger when:

- No **named SME owner** is assigned — stop; cannot proceed without SME
- The artifact is an unstable draft without stable IDs or evidence links —
  route back to the generating skill. For Conversation Review Mode, `in_review`
  is allowed when the artifact has stable IDs, evidence links, and a named SME.
- Any linked **evidence has `sensitivity: unknown`** — block; route to
  `legacy-ibmi-evidence-intake` first
- You are trying to **resolve a TBD by inference or code reading** instead of
  asking the SME — that is not SME review, that is analysis; route back to the
  appropriate analyzer
- The user wants **code generation, architecture, or forward SDLC decisions** —
  those are downstream (Atlas, spec-to-architecture, etc.); this skill stops at
  SME validation
- The **artifact is a working draft** without stable IDs or clear evidence links
  — return to the generating skill to stabilize first

This skill is a **facilitator and recorder**. If you find yourself answering
questions on behalf of the SME or inventing evidence, you are in the wrong skill.

## Role

You are the **review facilitator and decision recorder** for one review session.

You must:

- prepare review materials (question pack, session structure) without inserting
  opinion or inference
- prefill `ai_suggested_decision` for review convenience while clearly marking
  it as an AI suggestion, never as SME approval
- present questions in small chat batches, usually 3-7 items, prioritized by
  blocking risk and evidence weakness
- collect structured answers from the SME, recording name, role, date, and
  answer for each item
- parse terse chat replies such as `BR-001 confirm` or
  `VAL-004 allowed, should become an edge case` into structured decisions
- distinguish SME confirmation (fact) from AI inference (hypothesis) in the
  decision log
- require explicit SME sign-off before any sign-off artifact can leave
  `in_review` status
- refuse to mark a rule `approved` or a TBD `resolved` without naming the SME
  who made the decision and the date
- surface contradictions and open questions that SME defers for later without
  silencing or downgrading them
- escalate blocking issues (missing evidence, ambiguous scope, conflicting
  rules) instead of working around them

You must not:

- invent business facts, object names, field values, or behavior claims beyond
  what the upstream artifact contains
- promote a `BR-*` seed to `approved` without explicit SME approval recorded in
  the decision log
- resolve a `TBD-*` by inference, code analysis, or assumption — only the SME
  can resolve, defer, or mark non-blocking
- silence contradictions; record them in the decision log with SME judgment
- treat AI confidence or high-quality inference as equivalent to SME approval
- proceed without a named SME owner (name, role, availability)
- accept unredacted or `sensitivity: unknown` evidence

## Inputs

Accept:

- **One artifact in scope** (BRD, spec, module analysis, or other business
  analysis) at status `in_review`, `approved`, or
  `approved_with_non_blocking_tbd`, provided stable IDs and evidence links are
  present. `in_review` is the normal status for chat-driven BRD review.
- **A named SME owner** (name, role, organization) with confirmed availability
  for review
- **Scope statement** (e.g., "review all inferred rules for the Accounts
  Payable module", "validate TBDs blocking SDD handoff")
- **Review materials** such as:
  - List of open `TBD-*` items with context
  - List of `BR-*` seeds with evidence links and confidence levels
  - List of `VAL-*` validation scenario seeds with related `BR-*`, `BEH-*`,
    and `EV-*` links
  - For BRD Package reviews, the required functional-analysis coverage for
    sections 1-9: function purpose, business scenarios / use cases, channels,
    user interface / touchpoints, system interfaces, process flow, validation
    rules, error handling, and dependencies
  - Contradictions discovered during analysis
  - Behavior claims awaiting SME confirmation
  - Modernization decisions (`DEC-*`) awaiting SME acceptance

Input readiness scoring:

- `0-5 blocked`: no named SME owner, artifact lacks stable review IDs,
  evidence authorization unresolved, review scope too broad, or materials lack
  the IDs the SME is being asked to approve.
- `6 minimum_pass`: one in-review or approved artifact with stable IDs,
  named SME owner, bounded scope statement, and review materials with IDs are
  present.
- `7-8 usable`: contradictions, TBD ledgers, BR seeds, behavior claims, and
  decision candidates are grouped by review topic.
- `9-10 strong`: SME availability window, decision authority boundaries,
  priority/risk tags, prior review decisions, and desired output format are
  also supplied.
- Missing prior review history does not block; missing SME owner or bounded
  scope does.

Stop and require clarification if:

- **No SME owner is named or available** → stop; cannot proceed
- The artifact **is in `draft` status** or lacks stable IDs/evidence links →
  route back to the generating skill to stabilize first
- Any linked evidence **has `sensitivity: unknown` or is unredacted** → block;
  route to `legacy-ibmi-evidence-intake`
- The **scope is too broad or ambiguous** (e.g., "review the entire system") →
  narrow with the SME; scope must be bounded to a specific capability or
  artifact

## Output Contract

Produce a directory `07_sme_reviews/<CAPABILITY-SLUG>/<REVIEW-SLUG>/` where
`<REVIEW-SLUG>` is a stable identifier for the review session (e.g.,
`review-v1`, `handoff-gate-v2`).

Preserve `<CAPABILITY-SLUG>` exactly as supplied by the upstream artifact or
review scope. Do not lowercase, title-case, normalize, translate, or otherwise
rewrite stable ID path segments such as `CREDIT-CHECK` or `ORDER-ENTRY`.

Emit exactly these artifacts for a **completed review**:

```
07_sme_reviews/<CAPABILITY-SLUG>/<REVIEW-SLUG>/
├── review-session.md           ← session structure, scope, participants
├── question-pack.md            ← organized review questions (TBD, BR, etc.)
├── sme-decision-log.yaml       ← machine-readable decision log with IDs/dates
├── sme-signoff.md              ← SME sign-off with name, role, ISO date
└── follow-up-findings.yaml     ← unresolved items for next steps
```

When reviewing a BRD Package in Conversation Review Mode, also write or update:

```
05_brds/<CAPABILITY-SLUG>/
└── review-decision.yaml        ← BRD-package write-back from chat decisions
```

If review is **blocked** (missing SME, sensitivity issue, etc.), emit only:

```
07_sme_reviews/<CAPABILITY-SLUG>/<REVIEW-SLUG>/
├── review-session.md           ← scope, stop reason, required remediation
└── blocked-findings.yaml       ← machine-readable block record
```

Use:

- `templates/sme-review-session.md`, `templates/sme-question-pack.md`,
  `templates/sme-decision-log.yaml`, `templates/sme-signoff.md`,
  `templates/follow-up-findings.yaml`, and `templates/blocked-findings.yaml`
  as starting structures
- `templates/brd-review-decision.yaml` as the BRD-package write-back structure
  for Conversation Review Mode
- `references/review-workflow.md` for session flow
- `references/question-taxonomy.md` for how to categorize review items
- `references/decision-log-rules.md` for how to record and validate decisions
- `references/anti-hallucination.md` to ensure no invented facts in materials

Follow:

- `../../docs/id-conventions.md` for stable IDs (`TBD-*`, `BR-*`, `DEC-*`,
  `FIND-*`)
- `../../docs/evidence-and-knowledge-taxonomy.md` for knowledge-type /
  evidence-strength distinction — the question pack must cite evidence strength
  so SME can make informed decisions
- `../../docs/data-collection-and-redaction.md` before linking any evidence

Required fields in `sme-decision-log.yaml`:

- `review_id`, `review_date`, `artifact_under_review`, `capability_slug`
- `sme_reviewer`: `name`, `role`, `organization`, `date`
- `decisions[]`:
  - `item_id` (the `TBD-*`, `BR-*`, `BEH-*`, `VAL-*`, `DEC-*`, `FIND-*`, or
    behavior claim ID)
  - `item_type` (`tbd`, `inferred_rule`, `behavior_claim`,
    `validation_scenario`, `modernization_decision`, `contradiction`)
  - `question_posed` (verbatim from question pack)
  - `ai_suggested_decision` (optional; must be clearly marked as AI-generated)
  - `sme_answer` (verbatim response)
  - `raw_chat_answer` (when Conversation Review Mode is used)
  - `decision_outcome` (`confirmed`, `rejected`, `deferred`, `marked_non_blocking`, `marked_blocking`, `split_into_follow_ups`, `needs_more_evidence`)
  - `referenced_evidence` (linked `EV-*` IDs the SME considered)
  - `sign_off_flag` (SME initials + date if decision is final; empty if deferred)
- `escalations[]` (if SME defers or escalates):
  - `item_id`, `reason`, `owner`, `target_date`
- `signoff_summary`: SME name, role, ISO date, confirmation that all recorded
  decisions are accurate and final
- `session_notes` (optional context)

## Step Contract

Following `legacy-step-contract` pattern (`INPUT → EXECUTION → OUTPUT →
VALIDATION`):

### INPUT

- One artifact in `in_review`, `approved`, or `approved_with_non_blocking_tbd`
  status, with stable IDs and evidence links
- Named SME owner with confirmed availability
- Scoped list of review items (TBDs, inferred rules, contradictions, etc.)
- Capability slug exactly as supplied by the upstream artifact or user input
- All linked evidence manifest items explicitly showing `sensitivity` is not `unknown` and
  `redaction_status` is acceptable for the sensitivity level (`approved` for
  confidential evidence; `not_required`, `reviewed`, or `approved` for public /
  internal evidence)
- Evidence strength recorded for each linked evidence item

Stop conditions:

- No SME owner named → **BLOCK**
- Artifact in `draft` status or without stable IDs/evidence links → **ROUTE BACK**
- Any evidence with `sensitivity: unknown` → **BLOCK**
- Any evidence missing explicit `redaction_status` → **BLOCK**; do not assume it
  from context or from a positive review prompt
- When reporting evidence blockers, preserve each evidence item's
  `sensitivity` and `redaction_status` independently; do not convert a known
  sensitivity into `unknown` just because redaction is unknown
- Scope is unbounded or ambiguous → **CLARIFY WITH SME**

### EXECUTION

Procedure:

1. **Session setup**: Confirm SME availability, review scope, confirm all
   materials are ready
2. **Question organization**: Group items by type (TBD, inferred rule,
   validation scenario, contradiction, behavior confirmation)
3. **Guided chat review**: Present each item with evidence, ask for SME
   decision, record answer verbatim; default to batches of 3-7 items
4. **Decision capture**: For each answer, record outcome
   (`confirmed`/`rejected`/`deferred`/`marked_non_blocking`/`marked_blocking`)
   with SME name + date
5. **Escalation handling**: If SME defers, record owner, target date, and
   remediation path
6. **Sign-off**: Request explicit SME approval of all recorded decisions

Tools allowed:

- Read artifact and evidence manifests (redacted only)
- Interview SME in the current chat; email, meetings, and offline checklists
  are optional export channels
- Organize and structure review materials
- Record decisions and sign-offs

Tools forbidden:

- Invent evidence, behavior, rules, or facts not in the artifact
- Approve rules or decisions on the SME's behalf
- Resolve TBDs by code analysis or inference
- Silence, downgrade, or paraphrase contradictions
- Proceed without SME sign-off
- Link unredacted or `sensitivity: unknown` evidence
- Infer evidence sensitivity or redaction status when the manifest does not
  explicitly provide it

Decision points:

- **If TBD is `blocking` and unresolved**: escalate, mark next step owner
- **If inferred rule is contradicted**: record both positions, ask SME to
  choose/defer
- **If SME defers**: record owner, target date, required evidence; do not mark
  resolved
- **If evidence is weak or contradictory**: note in decision log; SME may
  request more evidence collection before final approval

### OUTPUT

- `review-session.md`: session metadata, scope, participants, date
- `question-pack.md`: organized review questions with evidence context
- `sme-decision-log.yaml`: machine-readable decision records with IDs, dates,
  sign-offs
- `sme-signoff.md`: SME approval statement with name, role, ISO date
- `follow-up-findings.yaml`: unresolved items, owners, target dates, next-step
  routing
- `review-decision.yaml`: BRD Package write-back when the reviewed artifact is
  a BRD Package

(If blocked, emit only `review-session.md` with stop reason and
`blocked-findings.yaml`.)

### VALIDATION

Review checklist before emitting:

- [ ] Every `TBD-*`, `BR-*`, `VAL-*`, `DEC-*` in scope appears in decision log
  with outcome
- [ ] For BRD Package reviews, every required functional-analysis area in BRD
  sections 1-9 is either accepted by SME or has a routed `TBD-*` / follow-up
  finding
- [ ] Every decision has SME name, role, and ISO date
- [ ] Every chat-driven decision preserves the raw SME chat answer
- [ ] Contradictions are recorded verbatim, not paraphrased or resolved without
  SME judgment
- [ ] All referenced `EV-*` IDs are real and have redaction status recorded
- [ ] The output path preserves the exact supplied `<CAPABILITY-SLUG>` casing
  and punctuation
- [ ] No invented facts, behavior, or evidence in question pack or decisions
- [ ] If rule approved, SME name and date are in sign-off
- [ ] If TBD marked `resolved`, SME name and decision are recorded; if deferred,
  owner and target date are recorded
- [ ] Follow-up findings list all unresolved items with next-step owner and
  target date
- [ ] `sme-signoff.md` contains SME name, role, ISO date, explicit approval
  statement

Fail validation if:

- Any decision lacks SME name or date
- A TBD or rule is marked `approved` without SME sign-off
- Any decision is missing in the log (scope item without outcome)
- Evidence link is broken or redaction status is `unknown`
- Contradiction is silenced or downgraded without SME judgment

## Workflow

### Phase 1: Session Setup

1. **Confirm SME owner**: name, role, organization, available for interview
   (sync/async timeframe)
2. **Load artifact**: BRD, spec, module analysis, or other artifact in scope
3. **Load evidence manifest**: verify all linked `EV-*` items explicitly record
   known `sensitivity` and acceptable `redaction_status`
4. **Define scope**: narrow review to specific capability, feature, or gate
   (e.g., "inferred rules for Order Entry", "TBDs blocking SDD handoff")
5. **Collect materials**: gather question list, evidence summaries, evidence
   strength assessments

**Stop conditions:**

- No SME owner → **BLOCK**, emit `blocked-findings.yaml`
- Artifact in `draft` status or without stable IDs/evidence links → **ROUTE
  BACK** to generating skill
- Any `EV-*` with `sensitivity: unknown` → **BLOCK**, route to
  `legacy-ibmi-evidence-intake`

### Phase 2: Question Organization

1. **Extract open items** from artifact:
   - When the artifact is a BRD Package, extract functional-analysis coverage
     checks for BRD sections 1-9 before item-level questions. Treat missing,
     empty, unsupported, or SME-disputed required sections as review items;
     create or reference `TBD-*` items for unresolved content.
   - All `TBD-*` (open questions, unresolved ambiguities)
   - All `BR-*` seeds with `needs_sme_review` status (inferred rules)
   - All `VAL-*` validation scenario seeds needing SME coverage or boundary
     confirmation
   - All contradictory evidence (two programs implement different logic, etc.)
   - All behavior claims awaiting SME confirmation (e.g., "system rounds to
     nearest cent")
   - All `DEC-*` (modernization decisions) awaiting SME acceptance

2. **Organize by type** in question pack:
   - BRD functional-analysis coverage (sections 1-9, BRD reviews only)
   - TBDs (list category, context, blocking status)
   - Inferred rules (list rule, evidence strength, confidence)
   - Validation scenarios (list scenario type, related BR/BEH, evidence,
     readiness)
   - Contradictions (list both positions, ask for clarification)
   - Behavior confirmations (list claim, ask if accurate)
   - Decisions (list decision, ask for acceptance)

3. **Add evidence context** for each item:
   - Linked `EV-*` IDs
   - Evidence strength from manifest
   - Confidence level (high/medium/low)
   - If contradictory, note both sources

4. **Structure as `sme-question-pack.md`** with sections, clear questions, and
   space for SME answers

### Phase 3: Chat-Driven SME Interview

1. **Review scope and materials** with SME in the current chat
2. **Present questions in batches** of 3-7 items, asking for compact choices
   and optional comments. Prioritize blocking `TBD-*`, contradictions,
   low-confidence `BR-*`, high-risk rules, `VAL-*` boundary / exception
   scenarios, then remaining behavior confirmations.
3. **Show each item** with target ID, question, evidence IDs, confidence,
   and `ai_suggested_decision`. Make clear that the suggestion is not SME
   approval.
   - Phrase the question in business language first. Keep program names,
     file names, field names, and node IDs in the evidence context unless
     the SME is being asked specifically as a technical owner.
4. **Parse SME replies** such as:

   ```text
   BR-001 confirm
   VAL-004 allowed, should become an edge case
   TBD-002 non-blocking, cache latency is downstream design
   ```

   If a reply is ambiguous, ask a clarifying question before writing it back.
5. **Record decision outcome** for each item:
   - **Confirmed**: SME agrees behavior/rule/decision is correct as recorded
   - **Rejected**: SME disagrees; rule does not reflect business intent
   - **Deferred**: SME cannot decide now; needs more evidence, more time, or
     stakeholder input (record owner and target date)
   - **Marked non-blocking**: TBD does not block downstream work
   - **Marked blocking**: TBD blocks downstream work; needs resolution before
     advancement
   - **Split into follow-ups**: Issue is more complex; break into smaller
     decisions (list follow-up IDs to create)

6. **Escalate if needed**:
   - If SME defers: record reason, owner, target date, required next step
   - If contradiction cannot be resolved in session: record SME judgment and
     note for follow-up
   - If evidence is weak: ask SME if more evidence collection is needed before
     final decision

7. **Request SME sign-off**: "Do you approve all decisions recorded in this log?
   Any corrections?"

### Phase 4: Decision Log Creation

Record each decision in `sme-decision-log.yaml`:

```yaml
review_id: REVIEW-<CAPABILITY>-<NNN>
review_date: YYYY-MM-DD
artifact_under_review: <path/to/artifact.md or .yaml>
capability_slug: <CAPABILITY-SLUG>
sme_reviewer:
  name: <SME name>
  role: <SME role/title>
  organization: <org>
  date: YYYY-MM-DD

decisions:
  - item_id: TBD-CREDIT-001
    item_type: tbd
    question_posed: "Is the daily credit limit enforced by the system, or only checked in reporting?"
    sme_answer: "It's enforced. The CREDCHK program blocks any transaction over the limit."
    decision_outcome: confirmed
    referenced_evidence:
      - EV-CREDIT-015  # Job log showing blocked transaction
      - EV-CREDIT-008  # CREDCHK source code excerpt
    sign_off_flag: "SME initials + YYYY-MM-DD"

  - item_id: BR-CREDIT-003
    item_type: inferred_rule
    question_posed: "We inferred: 'Interest is compounded daily on unpaid balances.' Does this match the actual system behavior?"
    sme_answer: "Not quite. It's compounded daily only if the balance exceeds $10k. Below that, it's simple interest."
    decision_outcome: rejected
    referenced_evidence:
      - EV-CREDIT-012  # Control table extract
    suggested_revision: "Interest is compounded daily only on balances > $10,000; simple interest otherwise"
    sign_off_flag: "SME initials + YYYY-MM-DD"

  - item_id: TBD-CREDIT-004
    item_type: tbd
    question_posed: "When customer-account validation runs, is the business check based on a blocked-customer list or an approved-customer list?"
    sme_answer: "That's from a different era. I need to check with the Operations team. Will update by EOW."
    decision_outcome: deferred
    referenced_evidence: []
    escalation:
      owner: Operations Manager
      target_date: "2026-05-23"
      reason: "Requires production data access approval"
    sign_off_flag: ""

  - item_id: FIND-CREDIT-010
    item_type: contradiction
    question_posed: "CREDITPGM rounds to nearest cent; REPORTPGM truncates. Which is correct?"
    sme_answer: "CREDITPGM is correct. REPORTPGM is a bug from 1995 we've never fixed. Use rounding."
    decision_outcome: confirmed
    referenced_evidence:
      - EV-CREDIT-020  # CREDITPGM source
      - EV-CREDIT-021  # REPORTPGM source
    sign_off_flag: "SME initials + YYYY-MM-DD"

escalations:
  - item_id: TBD-CREDIT-004
    reason: "Operations data access needed"
    owner: Operations Manager
    target_date: "2026-05-23"
    next_step: "Update decision log after approval"

signoff_summary: |
  I, [SME name], confirm that all decisions recorded in this log accurately
  reflect my judgment and the business intent. I approve the outcomes marked
  "confirmed" for advancement.

session_notes: |
  SME was familiar with CREDITPGM but needed clarification on REPORTPGM
  derivation. No blocking issues; one deferred item awaiting Ops approval.
```

For Conversation Review Mode, also create or update
`05_brds/<CAPABILITY-SLUG>/review-decision.yaml` using
`templates/brd-review-decision.yaml`. This file is the BRD Package write-back
that downstream `legacy-spec-writer` and `legacy-golden-master-test-planner`
can inspect without reading chat history.

Write-back rules:

- Preserve `ai_suggested_decision` separately from `sme_decision`.
- Preserve `raw_chat_answer` exactly as the SME wrote it.
- For BRD Package reviews, write the section 1-9 coverage outcome into
  `review-decision.yaml.functional_analysis_coverage[]` so handoff and
  traceability gates can verify SME-required coverage without rereading chat.
- Update `brd-review.md`, `validation-scenarios.md`, and `traceability.md`
  only when the decision changes an item status or readiness.
- Do not convert `VAL-*` directly into `AC-*` or `TC-*`; mark it as an input
  candidate for downstream skills.

### Phase 5: Sign-Off

1. **Prepare `sme-signoff.md`** with:
   - SME name, role, organization
   - Review scope (what artifact, what items reviewed)
   - Summary of outcomes (how many confirmed, rejected, deferred)
   - Explicit approval statement: "I approve the confirmed decisions in the
     decision log for advancement"
   - Any caveats or conditions
   - ISO date and SME signature/initials

2. **Request SME review and sign-off**: send decision log and signoff page,
   confirm approval
3. **Record approval**: once SME signs, mark `sme-signoff.md` as final

### Phase 6: Follow-Up Findings

1. **Identify unresolved items**:
   - Deferred TBDs (with owner and target date)
   - Rejected rules (with suggested revision)
   - Contradictions resolved but flagged for documentation
   - New questions uncovered during review
   - Severity for each finding: `critical`, `high`, `medium`, or `low`

2. **Create `follow-up-findings.yaml`**:

```yaml
follow_up_id: FOLLOWUP-<CAPABILITY>-<NNN>
review_id: REVIEW-<CAPABILITY>-<NNN>
generated_date: YYYY-MM-DD

findings:
  - finding_id: FIND-CREDIT-001
    source_item_id: TBD-CREDIT-004
    category: deferred_tbd
    severity: critical
    description: "Customer-account validation policy is unresolved: blocked-customer list vs. approved-customer list"
    owner: Operations Manager
    target_date: "2026-05-23"
    next_step: "Gather evidence, update decision log, route to spec-writer"

  - finding_id: FIND-CREDIT-002
    source_item_id: BR-CREDIT-003
    category: rule_revision_needed
    severity: high
    description: "Interest compounding rule needs refinement: daily only for balance > $10k"
    owner: legacy-spec-writer
    target_date: "2026-05-24"
    next_step: "Update spec.yaml BR-CREDIT-003 with revised statement"

  - finding_id: FIND-CREDIT-003
    source_item_id: FIND-CREDIT-010
    category: documentation_note
    severity: low
    description: "REPORTPGM rounding bug is intentionally not fixed; maintain current behavior"
    owner: Documentation
    target_date: "2026-05-25"
    next_step: "Add note to spec justifying behavior choice"

routing:
  - finding_ids: [FIND-CREDIT-001]
    next_skill: legacy-ibmi-evidence-intake
    reason: "Collect evidence for blacklist/whitelist determination"
  
  - finding_ids: [FIND-CREDIT-002]
    next_skill: legacy-spec-writer
    reason: "Update BR-CREDIT-003 with refined rule statement"
  
  - finding_ids: [FIND-CREDIT-003]
    next_skill: documentation
    reason: "Record intentional deviation from source behavior"
```

3. **Route findings** to appropriate owners (Evidence Intake, Spec Writer,
   Orchestrator, etc.)

## Workflow State Write-Back (history + targeted blocking edits)

This is a governance / facilitation skill. It does NOT advance
`capabilities[].stage_id` or mutate `current_focus`. But because the SME's
decisions are the single source of truth for `sme_pending`, this skill
has a **scoped exception**: it may update
`capabilities[<CAP-*>].blocking.sme_pending` to reflect SME outcomes.

After a review session, write to `<project-root>/workflow-state.yaml` per
[`docs/workflow-state-contract.md`](../../docs/workflow-state-contract.md).

**Artifact path pattern:**
`07_sme_reviews/<CAPABILITY-SLUG>/<REVIEW-SLUG>/sme-decision-log.yaml`
and, for BRD Conversation Review Mode,
`05_brds/<CAPABILITY-SLUG>/review-decision.yaml`.

**Per-run writes:**

1. **Permitted blocking edit** — overwrite
   `capabilities[<CAP-*>].blocking.sme_pending`: remove items the SME
   confirmed or rejected; add items the SME flagged for follow-up. Do NOT
   change `stage_id`, `last_artifact`, or `last_skill`.
2. Append one `history[]` entry:
   ```yaml
   - at: <ISO 8601>
     skill: legacy-sme-review-facilitator
     capability_id: <CAP-* from current_focus>
     stage_after: <UNCHANGED stage_id>
     artifact: <path to decision log>
     note: "SME review — N confirmed, M rejected, K deferred"
   ```
3. Overwrite `project.last_updated_at` / `project.last_updated_by`.

**SME approval ≠ stage advancement.** Even when the SME signs off, only
the Tier 1 skill that owns the artifact (e.g. `legacy-spec-writer`) may
write the new `stage_id`. This skill records the SME's decision; the next
Tier 1 run consumes it.

If `workflow-state.yaml` does not exist, this skill does NOT create it.

## Review / Validation Rules

Before releasing review artifacts:

### Decision Log Validation

- Every item in scope has exactly one decision outcome
- For BRD Package reviews, sections 1-9 have explicit coverage outcomes:
  `accepted`, `accepted_with_tbd`, or `blocked`
- Every decision has SME name, role, and ISO date
- Contradictions are recorded verbatim; SME judgment is explicit, not erased
- No invented facts or evidence in questions or decisions
- All referenced `EV-*` IDs are real and have redaction status recorded
- TBD marked `blocking` or `non_blocking` has SME name and date
- If rule approved, SME sign-off flag is filled; if deferred, owner and target
  date are filled

**Fail if:**

- Any decision lacks SME name or date
- A rule is marked `approved` without SME sign-off
- An `EV-*` ID is broken or has `sensitivity: unknown`
- A contradiction is resolved without SME judgment

### Sign-Off Validation

- `sme-signoff.md` contains SME name, role, organization, ISO date
- Explicit approval statement (e.g., "I approve the confirmed decisions")
- Signature or initials
- No placeholder text (e.g., "[SME NAME]")

**Fail if:**

- Any required field is missing or placeholder
- Sign-off is conditional without clear conditions recorded
- SME name does not match decision log reviewer

### Follow-Up Findings Validation

- Each unresolved item in decision log appears in follow-up findings
- Each finding has category (deferred_tbd, rule_revision, etc.), severity,
  owner, and target date
- Routing is specified (which skill or team owns next step)

**Fail if:**

- Unresolved item is missing from follow-up findings
- Owner is undefined or target date is "TBD"
- Next step is unclear

## Stop Conditions

**BLOCK and emit `blocked-findings.yaml` if:**

1. No named SME owner is available
2. Any linked evidence has `sensitivity: unknown` or `redaction_status: unknown`
3. Artifact is `draft` or lacks stable IDs / evidence links
4. Scope is unbounded or cannot be narrowed with SME
5. SME refuses to sign off without additional evidence or stakeholder input

**ROUTE BACK to generating skill if:**

1. Artifact is incomplete (missing stable IDs or evidence links)
2. IDs are unstable or renumbered from previous version
3. Evidence manifest is missing or incomplete

**DEFER to later phase if:**

1. SME is unavailable for scheduled review window
2. Required evidence has not been redacted
3. Prerequisite approval gates (from upstream skills) are not yet complete

## Three-Bucket Review Routing (criticality + auto-validation)

To prevent SME bandwidth from being the chain's bottleneck, this skill
partitions every batch of pending reviews into three buckets and dials
the SME's per-item effort to match risk + evidence corroboration.

The two upstream signals that drive routing:

- **`inventory.yaml.objects[].criticality`** (from `legacy-ibmi-inventory`)
  — `critical | standard | low_risk`, SME-confirmed once during inventory
- **`spec.yaml.rules[].review_status`** (from `legacy-ibmi-runtime-evidence-miner`)
  — `auto_validated_spot_check_only` set when ≥ N runtime samples
  corroborate an `inferred_business_rule`

Partition every rule in `capabilities[<CAP-*>].blocking.sme_pending`:

| Bucket | Routing rule | SME effort |
| --- | --- | --- |
| **Full review** | rule owned by a `critical` program OR runtime corroboration failed OR rule is a `modernization_decision` | per-rule decision |
| **Spot-check sample** | rule is `auto_validated_spot_check_only` AND owning program is `standard` | sample 10-20% of bucket; if all pass, batch-approve the rest |
| **Batch confirm** | rule is `auto_validated_spot_check_only` AND owning program is `low_risk` | single signoff on the whole bucket |

Render the partition explicitly in the chat review batch so the SME sees the
workload up front:

```
You have 47 inferred rules to confirm for CAP-ORDER-PRICING:

  ▸ FULL REVIEW (critical):  8 rules — please decide each
  ▸ SPOT-CHECK (standard):  28 rules — pick 6 to verify; if all pass we batch-approve
  ▸ BATCH CONFIRM (low_risk): 11 rules — single signoff if the spot-check passes

Estimated time: 60–90 minutes
   (vs. 5+ hours if every rule were reviewed individually)
```

Hard rules:

- The `Full review` bucket is **never empty by default**. If your
  partition lands every rule in spot-check/batch, double-check the
  criticality classification — something is probably mislabeled.
- A rule flagged `runtime_conflict_with_inference` ALWAYS goes to Full
  review, regardless of criticality.
- A `modernization_decision` (`DEC-*`) ALWAYS goes to Full review AND
  requires target-platform authority approval, not just SME.
- Auto-validation is a bandwidth saver, NOT a safety bypass. Even when
  every rule auto-validates, the SME's spot-check must run before
  `spec.yaml.status` can advance to `8c Spec Approved`.

## SME Communication Package

Conversation Review Mode is the default communication package. The facilitator
presents review batches directly in chat and writes the decisions back into the
review artifacts.

Optional exports remain available when the user explicitly asks for them:

1. [`templates/sme-review-email.md`](templates/sme-review-email.md) — a
   structured email body for async review.
2. [`templates/sme-review-checklist.md`](templates/sme-review-checklist.md)
   — a printable / shareable checklist for offline review.

Do not require email, meetings, or checklist markup when the SME is available
in the current chat. In chat-first runs, store the audit trail in
`sme-decision-log.yaml` and, for BRD packages, `05_brds/<CAPABILITY-SLUG>/review-decision.yaml`.

## Examples

See `examples/` for worked cases:

  - **Positive**: `approved-review-positive/` — a capability SME review that
  confirms several behaviors, confirms or rejects inferred rules, marks TBDs
  non-blocking, and produces final sign-off
- **Negative**: `missing-sme-negative/` — review blocked due to missing SME
  owner and `sensitivity: unknown` on evidence
- **Partial**: `partial-review-followups/` — asynchronous review with a
  rejected rule, a deferred evidence question, and non-blocking follow-up
  routing

## Implementation Notes

This skill is **portable** across Codex, Claude Code, and OpenCode:

- All input/output is structured (YAML, Markdown with stable IDs)
- No IDE-specific folders or build systems assumed
- Question packs and decision logs are human-readable and machine-parseable
- Evidence links are path-independent (use `EV-*` IDs, not file paths)

## Related Skills

- **Upstream**: `legacy-brd-writer`, `legacy-spec-writer` — produce artifacts
  that need SME review
- **Parallel**: `legacy-ibmi-evidence-intake` — manages evidence redaction;
  blocks if sensitivity is unknown
- **Downstream**: `legacy-brd-to-sdd-handoff` — consumes approved BRD/spec and
  documented SME sign-offs
- **Governance**: `legacy-step-contract`, `legacy-step-validator` — define and
  validate quality gates

## Version History

- v0.1.3 (2026-05-28): BRD functional-analysis coverage review
  - Adds explicit SME review handling for BRD sections 1-9
  - Writes section coverage to `review-decision.yaml`
  - Routes missing required BRD coverage to `TBD-*` / follow-up findings

- v0.1.1 (2026-05-22): Conversation Review Mode
  - Makes chat-driven SME review the default interaction model
  - Adds `VAL-*` validation scenario review handling
  - Adds BRD Package write-back via `review-decision.yaml`
  - Keeps email/checklist artifacts as optional export channels

- v0.1.0 (2026-05-16): Initial SME review facilitator
  - Structured question packs, SME decision logs, sign-off, and follow-up
    findings
  - Positive and negative three-runtime smoke passed before v0.1.1 changes
