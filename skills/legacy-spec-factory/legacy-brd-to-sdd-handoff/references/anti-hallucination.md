# Anti-Hallucination Rules for SDD Handoff

This document lists what the SDD handoff skill must **refuse to invent**.

## Golden Rule

**The handoff package is a pass-through, not a generator.** The skill validates and packages; it does not invent content beyond what the BRD and Spec provide.

---

## What the Handoff Must NOT Invent

### 1. Business Rules or Requirements
❌ **DO NOT**:
- Invent new `BR-*` or `BEH-*` that are not in the BRD or spec
- Add acceptance criteria that are not in the spec's `acceptance_criteria[]`
- Invent edge cases beyond what the spec documents
- Assume SME intent where the spec is silent

✅ **DO**:
- Copy business rules directly from the spec unchanged
- Validate that every approved rule has linked acceptance criteria
- Flag missing requirements as a blocking finding; do not fill the gap

### 2. Acceptance Criteria
❌ **DO NOT**:
- Generate new `AC-*` if the spec is missing them
- Rewrite or clarify AC-* wording (acceptance criteria belong to SME)
- Invent test strategies that go beyond what the AC specifies

✅ **DO**:
- Copy AC-* records exactly as they appear in the spec
- Verify that each AC is linked to a rule and is approved
- If acceptance criteria are missing, **stop and return to spec writer** with a blocking finding

### 3. Test Cases
❌ **DO NOT**:
- Invent test cases beyond the planned golden master tests
- Assume test data without evidence
- Generate test code or scripts (that is forward SDLC's job)

✅ **DO**:
- Reference test cases that are planned in the spec
- Note that forward SDLC will generate additional test cases
- Carry forward only test intent already recorded in `TC-*` or `AC-*`

### 4. Data Model or Schema
❌ **DO NOT**:
- Invert legacy data model if spec does not specify target model
- Assume field types, lengths, or null constraints
- Create new fields not in the spec's data model section

✅ **DO**:
- Copy data model from the spec as-is
- Carry forward target platform decisions only when they appear as approved
  `DEC-*` records in the spec
- Reference the spec's modernization decisions about data representation

### 5. Architecture or Technology Choices
❌ **DO NOT**:
- Decide whether to use REST vs. gRPC (unless spec specifies)
- Choose a database technology (unless DEC-* specifies)
- Add middleware, caching, or queuing patterns not in the spec

✅ **DO**:
- Copy approved modernization decisions (`DEC-*`) from the spec
- Note the rationale and trade-offs from the spec
- Flag architectural gaps as findings for forward SDLC to address

### 6. SME Sign-Offs or Approvals
❌ **DO NOT**:
- Invent SME names or roles
- Backdate approvals or sign-offs
- Claim approval when the spec does not show it
- Overwrite or modify SME sign-offs from the spec or BRD

✅ **DO**:
- Copy SME names, roles, and dates directly from the spec and BRD
- Verify that all required approvals are present and named
- Add the handoff validator's own sign-off (Claude Code, timestamp)
- Record if an approval is missing as a blocking finding

### 7. Evidence Interpretation
❌ **DO NOT**:
- Reinterpret evidence or draw new conclusions from it
- Suggest that weak evidence should be treated as strong
- Hide or downplay evidence of contradictions

✅ **DO**:
- Reference evidence IDs exactly as they appear in the spec
- Verify that evidence satisfies the approved evidence-manifest contract
- Note if evidence is contradictory or incomplete (as a finding)
- Allow the evidence to speak for itself

### 8. Open Questions or TBDs
❌ **DO NOT**:
- Resolve TBDs that the spec does not resolve
- Mark a TBD as non-blocking if the spec marks it blocking
- Invent answers to open questions

✅ **DO**:
- Copy TBD records from the spec unchanged
- Verify that blocking TBDs are resolved (or defer is approved)
- Carry forward non-blocking TBDs into the handoff package with status

### 9. Modernization Decisions
❌ **DO NOT**:
- Make architectural decisions for the forward team
- Assume that deferred decisions should move forward
- Invent rationale for decisions that lack one

✅ **DO**:
- Copy approved `DEC-*` records from the spec
- Note the rationale and trade-offs from the spec
- Flag unapproved decisions as findings

### 10. Sensitivity or Redaction Status
❌ **DO NOT**:
- Assume evidence is non-sensitive without explicit clearance
- Redact or sanitize evidence (that happens upstream)
- Hide evidence sensitivity concerns

✅ **DO**:
- Verify that all evidence has a `sensitive` status
- Check that redaction is complete for sensitive evidence
- Stop and escalate if any evidence manifest item has `sensitivity: unknown`

---

## Handoff Package Boundaries

### What Goes In
- ✅ BRD summary and findings
- ✅ Spec data (rules, criteria, decisions, model)
- ✅ Evidence IDs and sensitivity status
- ✅ Test cases from the spec
- ✅ Traceability matrix
- ✅ Gate findings and required remediation for blocked gates
- ✅ Assumptions already recorded in the BRD or spec

### What Does NOT Go In
- ❌ Implementation code or pseudo-code
- ❌ Database schema DDL (forward SDLC generates that)
- ❌ API endpoint definitions (forward SDLC designs those)
- ❌ Test code or test data (forward SDLC writes tests)
- ❌ Deployment scripts (forward SDLC plans deployment)
- ❌ Operational runbooks (DevOps or SRE team owns those)

---

## When Tempted to Add Content

**If you think "this would be helpful to add to the handoff", ask:**

1. **Is it in the BRD or Spec already?** If yes, copy it unchanged. If no, → next question.
2. **Did the SME explicitly ask for it?** If yes, include it with the SME's note. If no, → next question.
3. **Is it a required field in the handoff schema?** If yes, fill it by validating upstream. If no, → next question.
4. **Is it inventing content not in the BRD/Spec?** If yes, **do not add it; file a finding instead**.

---

## Examples

### Good: Carrying Content Through Unchanged
**Input** (from spec):
```yaml
business_rules:
  - id: BR-CREDIT-CHECK-001
    statement: "Orders exceeding limit are rejected with error code 42"
    evidence_ids: [EV-001, EV-002]
```

**Output** (in handoff):
```yaml
business_rules:
  - id: BR-CREDIT-CHECK-001
    statement: "Orders exceeding limit are rejected with error code 42"
    evidence_ids: [EV-001, EV-002]
```

✅ **Correct**: Copied unchanged; no invention.

---

### Bad: Inventing Acceptance Criteria
**Input** (spec has no AC for a rule):
```yaml
business_rules:
  - id: BR-CREDIT-CHECK-001
    acceptance_criteria_ids: []  # empty!
```

**What the handoff skill might be tempted to do:**
```yaml
business_rules:
  - id: BR-CREDIT-CHECK-001
    acceptance_criteria_ids: [AC-INVENTED-001]

acceptance_criteria:
  - id: AC-INVENTED-001
    criterion: "System must validate order amount"
```

❌ **WRONG**: Invented acceptance criteria that the spec does not have.

**What the handoff skill actually does:**
```yaml
findings:
  blocking:
    - finding: BR-MISSING-AC
      rule_id: BR-CREDIT-CHECK-001
      message: "Approved rule has no acceptance criteria"
      action: "Return to legacy-spec-writer to add acceptance criteria"
```

✅ **Correct**: Filed a blocking finding; stopped the handoff; did not invent.

---

### Bad: Inventing Data Model Fields
**Input** (spec specifies Customer, Order; nothing about Audit):
```yaml
data_model:
  entities:
    - legacy_name: CUSTPF
      target_name: Customer
```

**What the handoff skill might invent:**
```yaml
data_model:
  entities:
    - legacy_name: CUSTPF
      target_name: Customer
    - legacy_name: AUDITPF
      target_name: AuditLog       # invented!
      fields:
        - legacy_field: TIMESTAMP
          target_field: logged_at # invented!
```

❌ **WRONG**: Invented data model elements not in spec.

**What the handoff skill does:**
```yaml
# Copies spec's data model exactly as-is
# Notes in findings: DEC-CREDIT-CHECK-003 specifies centralized audit service
# References the decision in the output instead of inventing schema
```

✅ **Correct**: Copied spec; referenced existing modernization decision.

---

### Bad: Resolving Open Questions
**Input** (spec has unresolved TBD):
```yaml
open_questions:
  - id: TBD-CREDIT-CHECK-001
    question: "Should daily limits apply?"
    blocking: false
    resolution: "Deferred to Phase 2"
```

**What the handoff skill might invent:**
```yaml
open_questions:
  - id: TBD-CREDIT-CHECK-001
    question: "Should daily limits apply?"
    blocking: false
    resolution: "Yes, because cloud systems can scale better"  # invented!
```

❌ **WRONG**: Resolved a TBD that is not resolved.

**What the handoff skill does:**
```yaml
# Copies TBD unchanged from spec
# Notes in handoff: TBD deferred to Phase 2 by SME
# Carries it forward into the handoff for Phase 2 team
```

✅ **Correct**: Passed through; did not invent resolution.

---

## Running the Hallucination Check

Before finalizing the handoff, ask of every field:

- [ ] Does this field come directly from the spec or BRD?
- [ ] If not, did an SME explicitly approve it in writing?
- [ ] If not, is it a required validation field (not invented content)?
- [ ] If not, is it a finding or required remediation for a gate result?

If you answer **no** to three or more of these, **do not add that field to the handoff package.**
