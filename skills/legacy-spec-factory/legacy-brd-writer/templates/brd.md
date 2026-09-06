# Business Requirements Document: `<CAPABILITY-NAME>`

**Document ID:** `BRD-<CAPABILITY-SLUG>-001`
**Capability ID:** `CAP-<CAPABILITY-SLUG>-001`
**Module ID:** `MODULE-<MODULE-SLUG>-001`
**Module Analysis Source:** `04_modules/<MODULE-SLUG>/`
**Status:** `draft` | `in_review` | `approved`
**Owner:** `<SME Name / Role>`
**Created:** `<YYYY-MM-DD>`
**Last Updated:** `<YYYY-MM-DD>`

---

Sections 1-9 are required for SME review. Sections 10-12 are optional and must
only be included when supported by evidence or explicit SME input. If optional
information is expected but missing, record a `TBD-*` instead of inventing it.

## 1. Function Purpose

### Purpose Statement

`<What business function this capability performs and why it exists. Use SME
language before implementation names.>`

### Business Value

`<Customer impact, operational value, compliance need, risk control, revenue
protection, or other business reason. Keep to 2-3 sentences.>`

### Scope Boundary

**In Scope:**
- `<Capability area 1>`
- `<Capability area 2>`

**Out of Scope:**
- `<Related area not included>`
- `<Adjacent process not included>`

### Scope Clarification Need

Use this only when the function boundary, actors, triggers, states, interfaces,
or handoffs require SME confirmation. Do not add a standalone `Problem
Statement` about scattered documents, technical coupling, or downstream rework.
If ambiguity exists, state the SME-answerable boundary question and link the
corresponding `TBD-*`; otherwise write `None identified from approved inputs.`

---

## 2. Business Scenarios / Use Cases

Describe the business scenarios this function supports. These are SME-reviewable
use cases, not formal `AC-*` acceptance criteria or `TC-*` test cases.

| Scenario ID | Business Scenario / Use Case | Primary Actor | Trigger | Business Outcome | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| `SCN-<CAPABILITY-SLUG>-001` | `<Normal business scenario>` | `<Actor>` | `<Trigger>` | `<Outcome>` | `EV-<CAPABILITY-SLUG>-001` | `confirmed` |
| `SCN-<CAPABILITY-SLUG>-002` | `<Exception / boundary scenario>` | `<Actor>` | `<Trigger>` | `<Outcome or open question>` | `EV-<CAPABILITY-SLUG>-002` | `needs_sme_review` |

---

## 3. Channels

List the channels or entry points through which the business function is
started, continued, or consumed. Include channels only when they are supported
by evidence or SME confirmation.

| Channel ID | Channel / Entry Point | Direction | Business Role | Evidence | Confidence / Status |
| --- | --- | --- | --- | --- | --- |
| `CH-<CAPABILITY-SLUG>-001` | `<HCCFE / SFE / PIB / MobileX / API / batch / operations queue>` | `inbound` | `<How this channel starts or influences the function>` | `EV-<CAPABILITY-SLUG>-001` | `high` |
| `CH-<CAPABILITY-SLUG>-002` | `<Channel>` | `outbound` | `<How this channel receives results>` | `EV-<CAPABILITY-SLUG>-002` | `needs_sme_review` |

---

## 4. User Interface / User Touchpoints

List business-visible touchpoints: screens, notifications, reports, messages,
queues, operational dashboards, or manual review worklists. Do not design a new
UI and do not invent screens that are not evidenced.

| Touchpoint ID | Touchpoint Type | Business User / Recipient | Purpose | Evidence | Notes |
| --- | --- | --- | --- | --- | --- |
| `UI-<CAPABILITY-SLUG>-001` | `screen` \| `notification` \| `report` \| `message` \| `queue` | `<Role>` | `<What the user sees or acts on>` | `EV-<CAPABILITY-SLUG>-001` | `<Known limitation or TBD>` |
| `UI-<CAPABILITY-SLUG>-002` | `<Type>` | `<Role>` | `<Purpose>` | `EV-<CAPABILITY-SLUG>-002` | `<Notes>` |

If no user interface or touchpoint is identified from current evidence, state
`No user-facing touchpoint identified from approved inputs` and create a
`TBD-*` only if SME review must confirm it.

---

## 5. System Interfaces

Summarize upstream and downstream systems, APIs, file handoffs, external
processors, reports, or operational consumers. Keep the business-facing summary
here; put detailed file names, libraries, sequence diagrams, and section
references in `traceability.md` or section 12.

| Interface ID | System / API / Interface | Direction | Business Purpose | Evidence | Confidence / Status |
| --- | --- | --- | --- | --- | --- |
| `IF-<CAPABILITY-SLUG>-001` | `<Upstream system or API>` | `inbound` | `<What business event/data it provides>` | `EV-<CAPABILITY-SLUG>-001` | `high` |
| `IF-<CAPABILITY-SLUG>-002` | `<Downstream system / report / processor>` | `outbound` | `<What business result/data it receives>` | `EV-<CAPABILITY-SLUG>-002` | `needs_sme_review` |

---

## 6. Process Flow

Describe the current-state business flow. It must be understandable without
reading program names. Program, file, library, and object names are evidence
anchors, not the primary narrative.

### Business Trigger

`<What business event starts this function?>`

### Current-State Flow

1. `<Business phase 1: intake / request / selection / eligibility>`
2. `<Business phase 2: validation / decision / execution / handoff>`
3. `<Business phase 3: response / completion / exception handling / reporting>`

### Business States

| State | Meaning | Entry Condition | Exit Condition | Evidence |
| --- | --- | --- | --- | --- |
| `<Requested / Pending / Approved / Rejected / Completed / Exception>` | `<Business meaning>` | `<How state is entered>` | `<How state is exited>` | `EV-<CAPABILITY-SLUG>-001` |

### Business Outcomes and Controls

- **Normal outcome:** `<What successful completion means to the business>`
- **Exception outcome:** `<What happens when the function cannot complete normally>`
- **Control or audit point:** `<Business-visible validation, approval, reconciliation, audit, or reporting point>`

---

## 7. Validation Rules

Validation rules must be evidence-backed and SME-reviewable. Keep observed
legacy behavior separate from inferred business rules.

### 7.1 Observed Validation Behaviors

Factual statements about what the legacy system demonstrably does, derived from
approved program / flow analyses, data flows, runtime evidence, or SME-confirmed
manual procedures.

#### BEH-<CAPABILITY-SLUG>-001: `<Behavior Title>`

**Statement:** `<Factual description of observed validation behavior>`

**Evidence:** `EV-<CAPABILITY-SLUG>-001` (source type: flow analysis, program
analysis, spool output, SME note, etc.)

**Knowledge Type:** `observed_behavior`
**Confidence:** `high` | `medium` | `low`

---

### 7.2 Inferred Business Rules

Rules inferred from observed behavior. Every `BR-*` below carries
`Review Status: needs_sme_review` until SME review and spec-writer promotion.

#### BR-<CAPABILITY-SLUG>-001: `<Rule Title>`

**Statement:** `<Proposed business rule>`

**Rationale:** Inferred from `BEH-<CAPABILITY-SLUG>-001` and
`BEH-<CAPABILITY-SLUG>-002`.

**Evidence:** `EV-<CAPABILITY-SLUG>-001`, `EV-<CAPABILITY-SLUG>-002`

**Knowledge Type:** `inferred_business_rule`
**Confidence:** `high` | `medium` | `low`
**Review Status:** `needs_sme_review`

**SME Decision:** `pending` | `confirmed_for_spec_promotion` | `rejected` |
`needs_evidence`

**SME Notes:** `<Space for reviewer to confirm or reject>`

---

## 8. Error Handling

List rejection, fallback, exception, retry, manual-review, and reporting paths.
Do not turn errors into policy unless the business rule is evidenced or
SME-confirmed.

| Error / Exception ID | Condition | Observed Handling | Business Impact | User/System Response | Evidence | SME Focus |
| --- | --- | --- | --- | --- | --- | --- |
| `ERR-<CAPABILITY-SLUG>-001` | `<Condition>` | `<What the legacy system does>` | `<Business impact>` | `<Message, report, queue, fallback, or none>` | `EV-<CAPABILITY-SLUG>-001` | `<What SME should confirm>` |

---

## 9. Dependencies

List business, data, system, operational, and evidence dependencies that affect
this function. Keep dependency purpose business-readable; move low-level
technical chains to `traceability.md`.

| Dependency ID | Dependency Type | Dependency | Role in Function | Evidence | Status / Risk |
| --- | --- | --- | --- | --- | --- |
| `DEP-<CAPABILITY-SLUG>-001` | `upstream_system` \| `downstream_system` \| `data` \| `manual_procedure` \| `reporting` \| `policy` | `<Name>` | `<Why it matters>` | `EV-<CAPABILITY-SLUG>-001` | `confirmed` |
| `DEP-<CAPABILITY-SLUG>-002` | `<Type>` | `<Name>` | `<Role>` | `EV-<CAPABILITY-SLUG>-002` | `needs_sme_review` |

---

## 10. Security / Authentication Requirements (Optional)

Include this section only when current evidence or SME input identifies
security, authentication, authorization, role, audit, or access-control
requirements. If absent, omit this section or record a `TBD-*` if confirmation
is required.

| Requirement ID | Security / Auth Requirement | Applies To | Evidence | Status |
| --- | --- | --- | --- | --- |
| `SEC-<CAPABILITY-SLUG>-001` | `<Requirement>` | `<Channel / UI / interface / operation>` | `EV-<CAPABILITY-SLUG>-001` | `confirmed` \| `needs_sme_review` |

---

## 11. Supporting Workflow or Design Notes (Optional)

Include only high-level workflow descriptions, sequence diagrams, or system
design notes that help SMEs understand function behavior. Detailed technical
verification chains belong in `traceability.md` or upstream analysis artifacts.

- **Workflow / diagram reference:** `<Source or diagram title>`
- **Business interpretation:** `<What the workflow means for the capability>`
- **Evidence:** `EV-<CAPABILITY-SLUG>-001`
- **Limitations / TBDs:** `<Any unresolved interpretation>`

---

## 12. Source Document Mapping (Optional)

Use this section when source document names or sections are available and useful
for review. This is a source map, not the main business narrative.

| Source ID | Source Document / Section | Used For | BRD Section | Evidence ID | Notes |
| --- | --- | --- | --- | --- | --- |
| `SRC-<CAPABILITY-SLUG>-001` | `<Document name, section, page, or path>` | `<Boundary / scenario / rule / interface>` | `<Section number>` | `EV-<CAPABILITY-SLUG>-001` | `<Notes>` |

---

## 13. Open Questions & Gaps (TBDs)

Questions that remain unresolved and must be answered before the next phase
(spec-writing), or explicitly carried forward as non-blocking.

### TBD-<CAPABILITY-SLUG>-001: `<Question Title>`

**Category:** `sme_questions` | `evidence_gaps` | `contradictory_evidence` |
`downstream_handoff_blockers`
**Statement:** `<What is unclear or missing?>`
**Evidence:** `EV-<CAPABILITY-SLUG>-001` or `<missing evidence description>`
**Resolver:** `<Role: SME, Source Owner, Architecture team, etc.>`
**Blocking:** `yes` | `no` (for this step and/or next step)

**Context:** `<Why this matters / where it appears in the BRD>`

---

## 14. Validation Scenario Summary

See `validation-scenarios.md` for SME-reviewable `VAL-*` scenario seeds.
These scenarios help validate BRD scope and coverage, but they are not formal
`AC-*` acceptance criteria or formal `TC-*` test cases.

| Scenario ID | Scenario Type | Related BR/BEH | Evidence | Readiness | SME Focus |
| --- | --- | --- | --- | --- | --- |
| `VAL-<CAPABILITY-SLUG>-001` | `happy_path` | `BR-<CAPABILITY-SLUG>-001`, `BEH-<CAPABILITY-SLUG>-001` | `EV-<CAPABILITY-SLUG>-001` | `ready_for_spec` | Confirm the business outcome and coverage |
| `VAL-<CAPABILITY-SLUG>-002` | `exception` | `BR-<CAPABILITY-SLUG>-002` | `EV-<CAPABILITY-SLUG>-004` | `needs_sme_review` | Confirm policy interpretation |

---

## 15. Traceability Summary

See `traceability.md` for the full cross-reference table and detailed evidence
index.

**Quick Summary:**
- X business scenarios documented
- X channels / user touchpoints / system interfaces documented
- X observed validation behaviors documented
- Y inferred business rules identified (all `needs_sme_review`)
- V validation scenario seeds drafted (no formal `AC-*` or `TC-*`)
- Z open questions (A blocking, B non-blocking)
- All claims trace to supporting evidence

---

**Document prepared by:** Claude Code / Agent name (date)
**Last reviewed by:** `<SME name>` (date, status)
