# Review Workflow

This document describes the complete workflow for facilitating an SME review
session and recording decisions using Legacy SME Review Facilitator.

## Workflow Phases

### Phase 0: Pre-Review Checks (Blocking Gates)

Before initiating a review session, verify:

1. **SME Owner is Named**
   - Full name, title/role, organization, and confirmed availability
   - If no SME owner: BLOCK, emit `blocked-findings.yaml`, stop

2. **Artifact Status**
   - Artifact must be at `approved_with_non_blocking_tbd` or higher
   - If artifact is `draft` or `in_review`: ROUTE BACK to generating skill
   - If artifact is below required status: STOP

3. **Evidence Manifest Complete**
   - All linked `EV-*` IDs in the artifact must appear in evidence manifest
   - Every `EV-*` in manifest must have known `sensitivity` and acceptable
     `redaction_status`
   - If any `EV-*` is missing or has `sensitivity: unknown` or
     `redaction_status: unknown`: BLOCK
   - Report `sensitivity` and `redaction_status` independently for each
     evidence item; do not change a known sensitivity value because redaction
     is unknown

4. **Scope is Bounded**
   - Review focus is specific to one capability or one gate
   - Scope is narrow enough to review in one session (1-2 hours)
   - If scope is unbounded (e.g., "review entire system"): CLARIFY with SME

**Gate Status:** `CLEAR` → proceed to Phase 1  
**Gate Status:** `BLOCKED` → emit `blocked-findings.yaml` and stop

---

### Phase 1: Session Setup (5-10 minutes)

**Goal:** Confirm everything is in place for productive SME conversation.

**Steps:**

1. **Confirm SME Availability**
   - Verify SME is available for the scheduled time
   - Check for any scheduling conflicts or last-minute changes
   - If SME is unavailable: DEFER session, reschedule

2. **Load and Organize Materials**
   - Load artifact (BRD, spec, module analysis, etc.)
   - Load evidence manifest (verify all `EV-*` linked)
   - Load evidence summaries (strength, confidence)
   - Prepare question pack (outline below in Phase 2)

3. **Confirm Scope with SME**
   - Describe what you will review (e.g., "inferred rules for the credit check capability")
   - Describe what is out of scope
   - Ask SME to confirm they understand and can commit to scope

4. **Prepare Facilitator Notes**
   - Open `templates/sme-review-session.md`, fill in header and scope
   - Verify all materials are readable and organized

**Output:** Completed `sme-review-session.md` with scope confirmed

**Stop Conditions:**
- SME is unavailable → DEFER
- Scope is misunderstood → CLARIFY
- Materials are missing → GATHER before proceeding

---

### Phase 2: Question Organization (15-30 minutes)

**Goal:** Build a structured question pack that guides the SME review without
inserting opinion or inference.

**Steps:**

1. **Extract Open Items from Artifact**
   - All `TBD-*` with current status (blocking / non-blocking / open)
   - All `BR-*` seeds with status `draft` or `needs_sme_review`
   - All contradictions discovered during analysis
   - All behavior claims awaiting SME confirmation
   - All `DEC-*` (modernization decisions) awaiting SME acceptance

2. **For Each Item, Gather Context**
   - Linked `EV-*` evidence IDs
   - Evidence strength (from manifest)
   - Confidence level (high / medium / low)
   - Current claim or statement in artifact

3. **Organize Questions by Type**

   | Item Type | Section | Focus |
   | --- | --- | --- |
   | `TBD-*` | "Open TBDs" | Ask for SME judgment; record if blocking/non-blocking |
   | `BR-*` seeds | "Inferred Rules" | Ask if rule matches business intent; request corrections |
   | Contradictions | "Contradictions" | Ask SME to choose/clarify when each applies |
   | Behavior claims | "Behavior Confirmations" | Ask if behavior is intended or a bug |
   | `DEC-*` | "Decisions" | Ask for SME acceptance; note any conditions |

4. **Write Question Pack**
   - Use `templates/sme-question-pack.md`
   - For each question: include prior claim, evidence strength, linked `EV-*` IDs
   - Keep questions neutral (not leading)
   - Provide space for SME answer below each question

**Output:** Completed `sme-question-pack.md` ready for SME review

**Quality Checks:**
- [ ] Every open item in artifact appears as a question
- [ ] No invented facts or inferences in question text
- [ ] Evidence is cited (not just claimed)
- [ ] Questions are clear and answerable by SME
- [ ] Question pack is organized by type, not by ID

---

### Phase 3: SME Interview (30-90 minutes, varies by scope)

**Goal:** Collect SME decisions, record verbatim answers, capture decision
outcomes.

**Format Options:**
- **Synchronous**: Live meeting (Zoom, conference call, in-person)
- **Asynchronous**: SME emails answers; facilitator records in decision log

**Steps:**

1. **Open Session with SME**
   - Review scope and materials
   - Explain decision log format (how answers will be recorded)
   - Confirm SME understands they will be asked to sign off on decisions

2. **Present Each Question in Order**

   For each question:
   - Read the question and context aloud (or have SME read it)
   - Ask SME to provide their answer
   - Record verbatim response
   - Ask clarifying questions if needed (but keep SME's core answer intact)

3. **Record Decision Outcome for Each Item**

   After SME answers, determine outcome:

   | Outcome | Meaning | Sign-Off? |
   | --- | --- | --- |
   | `confirmed` | SME agrees with claim or decision | YES (initials + date) |
   | `rejected` | SME disagrees; rule does not match intent | YES (initials + date) |
   | `deferred` | SME cannot decide now (needs more data, time, or stakeholder input) | NO (record owner + target date) |
   | `marked_non_blocking` | TBD does not block downstream work | YES (initials + date) |
   | `marked_blocking` | TBD blocks downstream work; must be resolved | YES (initials + date) |
   | `split_into_follow_ups` | Issue is complex; break into smaller decisions | NO (list follow-up IDs to create) |
   | `needs_more_evidence` | Cannot decide without additional evidence | NO (record what evidence is needed, who will gather it) |

4. **Escalate If Needed**

   If SME defers:
   - Ask why (unclear question? missing context? needs stakeholder input?)
   - Record reason
   - Ask who should resolve this (owner name or role)
   - Ask when they can provide answer (target date)
   - Ask what would help them decide (more evidence? clarification?)

5. **Continue Until All Questions Are Addressed**
   - Work through entire question pack
   - Keep pace manageable (don't rush SME)
   - Take breaks if session is long

6. **Summarize Outcomes**
   - Count confirmed / rejected / deferred decisions
   - Identify any new contradictions or issues uncovered during session
   - Ask SME if they want to revisit any decision

**Output:** Decision log ready for transcription into `sme-decision-log.yaml`

**Quality Checks:**
- [ ] Every question in pack has an SME answer (even if deferred)
- [ ] Every "confirmed" or "rejected" decision has SME name and date
- [ ] Every "deferred" decision has owner and target date
- [ ] SME answers are recorded verbatim (not paraphrased or edited)
- [ ] No invented facts or corrections by facilitator

---

### Phase 4: Decision Log Creation (15-30 minutes)

**Goal:** Transcribe SME interview into machine-readable decision log with
stable IDs and traceability.

**Steps:**

1. **Prepare `sme-decision-log.yaml`**
   - Use `templates/sme-decision-log.yaml` as starting structure
   - Fill in review metadata (`review_id`, artifact, capability, SME name/role/date)

2. **For Each Question, Create a Decision Entry**
   - Copy question from question pack
   - Copy SME answer verbatim
   - Record decision outcome
   - Record sign-off flag (initials + date) or escalation (owner + target date)
   - List referenced `EV-*` IDs

3. **Quality Assurance**

   For every decision, verify:
   - `item_id` matches artifact (no typos)
   - `question_posed` is accurate
   - `sme_answer` is verbatim from interview
   - `decision_outcome` is one of allowed values
   - If outcome is `confirmed`, `rejected`, `marked_non_blocking`, or
     `marked_blocking`: `sign_off_flag` is filled with SME initials + ISO date
   - If outcome is `deferred` or `needs_more_evidence`: `escalation` section
     has owner and target date
   - All referenced `EV-*` IDs are real and appear in evidence manifest

4. **Escalation Summary**
   - Create `escalations` section
   - List all deferred items with owner, target date, next step
   - Verify every deferred decision appears in escalations

5. **Final Sign-Off**
   - Complete `signoff_summary` with SME name, ISO date, explicit approval
   - Record in decision log

**Output:** Completed `sme-decision-log.yaml` ready for sign-off

**Validation:**
- [ ] Every decision has outcome, SME name, and date (or owner + target date if deferred)
- [ ] No decision is missing or left blank
- [ ] All `EV-*` references are correct
- [ ] Contradictions are recorded verbatim, not resolved without SME judgment
- [ ] Escalations have clear owner and target date

---

### Phase 5: Sign-Off (5-10 minutes)

**Goal:** Obtain explicit SME approval of all recorded decisions.

**Steps:**

1. **Review Decision Log with SME**
   - Send `sme-decision-log.yaml` to SME for review
   - Ask: "Do these decisions accurately reflect your answers?"
   - Ask: "Any corrections or clarifications needed?"

2. **Request SME Sign-Off**
   - Use `templates/sme-signoff.md`
   - Ask SME to complete approval statement
   - Ask for SME signature (or initials) and ISO date
   - Ask for SME role/title for record-keeping

3. **Verify Sign-Off**
   - SME name matches reviewer name in decision log
   - Sign-off date is on or after review date
   - Explicit approval statement is completed (no placeholder text)
   - SME signature / initials are present

**Output:** Completed `sme-signoff.md` with SME approval

**Validation:**
- [ ] All required fields are filled (no placeholders like "[SME NAME]")
- [ ] Sign-off is explicit (e.g., "I approve the confirmed decisions")
- [ ] SME name, role, date, and signature are present

---

### Phase 6: Follow-Up Findings (10-20 minutes)

**Goal:** Identify unresolved items, rule revisions, and routing decisions for
downstream teams.

**Steps:**

1. **Extract Unresolved Items**
   - All deferred TBDs (record owner, target date, next step)
   - All rejected rules (suggest revision based on SME feedback)
   - All contradictions resolved but flagged for documentation
   - All new issues uncovered during review

2. **Categorize Each Finding**

   | Category | Example | Owner |
   | --- | --- | --- |
   | `deferred_tbd` | "Operations team will confirm blacklist vs. whitelist" | Ops Manager |
   | `rule_revision_needed` | "Interest compounding rule needs refinement" | legacy-spec-writer |
   | `behavior_clarification` | "REPORTPGM rounding is intentional legacy behavior" | Documentation |
   | `evidence_gap` | "Need production logs showing credit limit enforcement" | legacy-ibmi-evidence-intake |
   | `new_contradiction` | "Two programs implement different rounding rules" | legacy-ibmi-evidence-intake |
   | `documentation_note` | "Record SME judgment on intentional bug vs. feature" | Documentation |
   | `escalation` | "Requires stakeholder decision on modernization approach" | Product Manager |

3. **Create Finding Records**
   - Use `templates/follow-up-findings.yaml`
   - For each unresolved item: create a finding entry with ID, category,
     severity, owner, target date, next step
   - Use severity levels consistently: `critical` blocks SDD or the next phase,
     `high` must be resolved soon, `medium` is tracked follow-up, and `low` is
     documentation or hygiene

4. **Organize Routing**
   - Group findings by destination skill (legacy-ibmi-evidence-intake, legacy-spec-writer, etc.)
   - For each group: specify target date and next step
   - Verify every finding has a clear owner and target date

5. **Write Summary**
   - Count total findings, blocking vs. non-blocking
   - List primary owners for follow-up
   - Provide recommendation (e.g., "Proceed to SDD handoff; resolve blocking findings in parallel")

**Output:** Completed `follow-up-findings.yaml` with routing

**Validation:**
- [ ] Every deferred item in decision log appears as a finding
- [ ] Every finding has category, severity, owner, target date, and next step
- [ ] Blocking vs. non-blocking status is clear
- [ ] Routing destination is specified for each finding
- [ ] Recommendation makes sense given blocking/non-blocking split

---

### Phase 7: Artifact Finalization & Routing (5-10 minutes)

**Goal:** Package review artifacts and route to next phase.

**Steps:**

1. **Create Review Directory**
   ```
   07_sme_reviews/<CAPABILITY-SLUG>/<REVIEW-SLUG>/
   ├── review-session.md
   ├── question-pack.md
   ├── sme-decision-log.yaml
   ├── sme-signoff.md
   └── follow-up-findings.yaml
   ```
   Preserve `<CAPABILITY-SLUG>` exactly as supplied by the upstream artifact or
   review scope. Do not lowercase, title-case, normalize, or translate stable
   ID path segments such as `CREDIT-CHECK` or `ORDER-ENTRY`.

2. **Verify All Artifacts Are Complete**
   - [ ] `review-session.md`: scope confirmed, materials listed
   - [ ] `question-pack.md`: all open items covered, evidence cited
   - [ ] `sme-decision-log.yaml`: every decision has outcome, SME sign-off
   - [ ] `sme-signoff.md`: SME approval with name, role, date, signature
   - [ ] `follow-up-findings.yaml`: routing specified for all unresolved items
   - [ ] output directory preserves the exact supplied capability slug

3. **Route to Downstream**

   Based on artifact type and outcomes:
   - **If BRD reviewed and approved**: route to `legacy-spec-writer` for spec development
   - **If spec approved and all TBDs resolved**: route to `legacy-brd-to-sdd-handoff`
   - **If blocking TBDs remain**: hold in current phase; update when resolved
   - **If rule revisions needed**: route to `legacy-spec-writer` with `follow-up-findings.yaml`
   - **If evidence gaps**: route to `legacy-ibmi-evidence-intake` for collection

4. **Document Routing Decision**
   - Update `follow-up-findings.yaml` with next-phase destination
   - Document any conditions or prerequisites for downstream advancement

**Output:** Review package ready for next phase

---

## Decision Outcome Rules

### Confirmed

**When to Record:**
- SME explicitly agrees with the claim, rule, or decision
- SME provides no correction or refinement

**Recording:**
```yaml
decision_outcome: confirmed
sign_off_flag: "SME-initials YYYY-MM-DD"
```

**Impact:**
- Item may advance to downstream skills
   - If it is a rule, the owning skill may promote it to `approved` status in
     the next phase after applying its own output contract

---

### Rejected

**When to Record:**
- SME explicitly disagrees with the claim, rule, or decision
- SME states the business intent is different

**Recording:**
```yaml
decision_outcome: rejected
sme_answer: |
  <Verbatim SME disagreement and correction>
suggested_revision: |
  <If rule, SME's proposed correction>
sign_off_flag: "SME-initials YYYY-MM-DD"
```

**Impact:**
- Item must be revised before advancing
- Route to appropriate skill for correction (e.g., `legacy-spec-writer` for BR revision)

---

### Deferred

**When to Record:**
- SME cannot decide in this session
- Requires more data, time, or stakeholder input

**Recording:**
```yaml
decision_outcome: deferred
escalation:
  reason: "<Why SME could not decide>"
  owner: "<Who will resolve>"
  target_date: "YYYY-MM-DD"
  next_step: "<Specific action needed>"
sign_off_flag: ""
```

**Impact:**
- Item is recorded in follow-up findings
- Routed to owner for resolution
- If blocking, prevents downstream advancement until resolved

---

### Marked Non-Blocking

**When to Record:**
- TBD is open but does not prevent downstream work
- SME confirms the question is important but not urgent

**Recording:**
```yaml
item_id: TBD-<CAPABILITY>-<NNN>
decision_outcome: marked_non_blocking
sme_answer: |
  This question doesn't block the credit check logic. We can address it post-launch.
sign_off_flag: "SME-initials YYYY-MM-DD"
```

**Impact:**
- TBD remains open in follow-up findings
- Does not block SDD handoff or downstream advancement
- Route to owner for eventual resolution

---

### Marked Blocking

**When to Record:**
- TBD is open and must be resolved before downstream advancement
- SME confirms the question blocks business logic

**Recording:**
```yaml
item_id: TBD-<CAPABILITY>-<NNN>
decision_outcome: marked_blocking
sme_answer: |
  We must clarify this before SDD handoff. It affects the daily reconciliation job.
sign_off_flag: "SME-initials YYYY-MM-DD"
escalation:
  owner: "<Who will resolve>"
  target_date: "YYYY-MM-DD"
  next_step: "<Resolution action>"
```

**Impact:**
- Item is flagged as blocking in follow-up findings
- Prevents SDD handoff until resolved
- Routed to owner for urgent resolution

---

### Split Into Follow-Ups

**When to Record:**
- Issue is too complex for single decision
- Needs to be broken into smaller, more tractable questions

**Recording:**
```yaml
decision_outcome: split_into_follow_ups
sme_answer: |
  This is actually three separate questions:
  1. Which fields are required...
  2. How do we validate...
  3. What happens if...
new_follow_up_ids:
  - TBD-<CAPABILITY>-<NNN>
  - TBD-<CAPABILITY>-<NNN>
  - TBD-<CAPABILITY>-<NNN>
sign_off_flag: "SME-initials YYYY-MM-DD"
```

**Impact:**
- Original item stays open until the owning skill updates it
- Follow-up findings request new `TBD-*` IDs from the owning skill; the
  facilitator does not mint or insert them directly
- Each sub-question is reviewed independently

---

## Anti-Patterns (What NOT to Do)

### ❌ Inventing Evidence

**Wrong:**
```
question_posed: "Is the credit limit enforced?"
sme_answer: <missing>
facilitator_note: "The code clearly shows enforcement in CREDCHK"
decision_outcome: confirmed
```

**Right:**
```
question_posed: "Is the credit limit enforced?"
sme_answer: "Yes, the system blocks transactions over the limit."
referenced_evidence:
  - EV-CREDIT-015: Job log showing blocked transaction
  - EV-CREDIT-008: CREDCHK source showing enforcement logic
decision_outcome: confirmed
sign_off_flag: "JDM 2026-05-16"
```

### ❌ Resolving a TBD Without SME Approval

**Wrong:**
```
item_id: TBD-CREDIT-004
question_posed: "Does the system validate against a blacklist or whitelist?"
sme_answer: <missing>
facilitator_note: "Code inspection shows blacklist logic in VALJOB"
decision_outcome: confirmed
```

**Right:**
```
item_id: TBD-CREDIT-004
question_posed: "Does the system validate against a blacklist or whitelist?"
sme_answer: "I need to check with Operations; will respond by EOW."
decision_outcome: deferred
escalation:
  owner: Operations Manager
  target_date: 2026-05-23
  next_step: "Gather evidence; update decision log; route to spec-writer"
```

### ❌ Silencing a Contradiction

**Wrong:**
```
item_id: FIND-CREDIT-001
question_posed: "CREDITPGM rounds to nearest cent; REPORTPGM truncates. Which is correct?"
sme_answer: <missing>
facilitator_note: "CREDITPGM is newer; assume it is correct."
decision_outcome: confirmed
```

**Right:**
```
item_id: FIND-CREDIT-001
question_posed: "CREDITPGM rounds to nearest cent; REPORTPGM truncates. Which is correct?"
sme_answer: |
  CREDITPGM is correct. REPORTPGM is a bug from 1995 we've never fixed.
  The business requirement is rounding to nearest cent.
decision_outcome: confirmed
referenced_evidence:
  - EV-CREDIT-020: CREDITPGM source
  - EV-CREDIT-021: REPORTPGM source (noted as legacy)
sign_off_flag: "JDM 2026-05-16"
```

### ❌ Promoting a Draft Rule to Approved Inside the Facilitator

**Wrong:**
```
item_id: BR-CREDIT-003
decision_outcome: confirmed
artifact_update: "Change status from needs_sme_review to approved"
```

**Right:**
```
item_id: BR-CREDIT-003
decision_outcome: confirmed
sme_answer: |
  Yes, interest is compounded daily. But only on balances over $10k.
  Below that, it's simple interest.
suggested_revision: |
  Interest is compounded daily only on balances > $10,000;
  simple interest for balances $10,000 or less.
sign_off_flag: "JDM 2026-05-16"
next_step: "legacy-spec-writer updates BR-CREDIT-003 with revised statement"
```

The spec-writer promotes the rule to `approved` in `spec.yaml`; the review
facilitator only records SME judgment.

---

## Escalation Patterns

### Evidence Gap Escalation

```yaml
- finding_id: FIND-CREDIT-001
  source_item_id: TBD-CREDIT-004
  category: evidence_gap
  severity: critical
  description: "Blacklist vs. whitelist validation — need production evidence"
  sme_request: "Show me a real transaction log where validation is performed"
  owner: legacy-ibmi-evidence-intake
  next_step: "Gather, redact, and index production transaction log"
  target_date: "2026-05-23"
  blocking_status: blocking
  routing_destination: legacy-ibmi-evidence-intake
```

### Stakeholder Escalation

```yaml
- finding_id: FIND-CREDIT-002
  source_item_id: DEC-CREDIT-001
  category: escalation
  severity: critical
  description: "Modernization approach (batch vs. real-time processing)"
  sme_note: "This is a business decision, not my call. Needs Ops + Finance approval"
  owner: Product Manager
  next_step: "Schedule decision meeting with Ops and Finance; document outcome"
  target_date: "2026-05-30"
  blocking_status: blocking
  routing_destination: Product Management
```

### Rule Revision Escalation

```yaml
- finding_id: FIND-CREDIT-003
  source_item_id: BR-CREDIT-003
  category: rule_revision_needed
  severity: high
  description: "Interest compounding has a $10k threshold SME clarified"
  sme_correction: "Interest is compounded daily only for balances > $10,000"
  owner: legacy-spec-writer
  next_step: "Update spec.yaml BR-CREDIT-003 with revised rule"
  target_date: "2026-05-17"
  blocking_status: non_blocking
  routing_destination: legacy-spec-writer
```

---

## Timing and Capacity

**Typical Session Breakdown (per capability):**

| Phase | Duration | Notes |
| --- | --- | --- |
| Pre-Review Checks | 5 min | Verify gates (blocking or clear) |
| Phase 1: Setup | 5-10 min | Confirm scope and materials |
| Phase 2: Questions | 15-30 min | Build question pack |
| Phase 3: Interview | 30-90 min | SME answers (varies by scope) |
| Phase 4: Decision Log | 15-30 min | Transcription and validation |
| Phase 5: Sign-Off | 5-10 min | SME approval |
| Phase 6: Follow-Up | 10-20 min | Categorize unresolved items |
| Phase 7: Routing | 5-10 min | Package and route to next phase |
| **Total** | **1.5-3 hours** | For a single capability review |

**Parallelization:**
- Multiple capabilities can be reviewed in parallel (different SMEs, different facilitators)
- Evidence collection and rule revision can happen in parallel with follow-up findings

---
