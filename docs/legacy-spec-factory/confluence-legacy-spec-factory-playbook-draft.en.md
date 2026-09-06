# Legacy Spec Factory: Evidence-Backed Legacy Modernization Playbook

> Bilingual sync note: This English draft is maintained in lockstep with the Chinese version: [`confluence-legacy-spec-factory-playbook-draft.md`](confluence-legacy-spec-factory-playbook-draft.md). Any future change to structure, wording, tables, action plan, or Definition of Done must be applied to both versions in the same update.

## Purpose

Legacy Spec Factory is an evidence-backed methodology for IBM i / AS400 modernization.

Its goal is not to directly translate RPGLE, CLLE, COBOL, or DDS code into Java. Its goal is to recover the real business intent embedded in the legacy system and produce auditable, reviewable specifications that can be handed off to a modern cloud SDLC.

The core deliverable is an SME-reviewed business capability specification package, including:

- `observed_behavior`: behavior proven by evidence from the legacy system
- `inferred_business_rule`: business rules inferred from code, data, or runtime evidence
- `modernization_decision`: target-system design decisions for modernization
- `spec.yaml` / `spec.md`: specification sources consumable by downstream engineering teams and AI agents
- `traceability_package`: the traceability chain from evidence, rules, and acceptance criteria to tests and delivery

## Operating Model

Legacy Spec Factory supports two operating paths.

### Default Path: RAG-Assisted Module-First

```text
RAG / Code Knowledge Graph / ARCAD / Data Dictionary
  -> Four-view Module Context
  -> Module Analysis
  -> BRD + Validation Package
  -> SME Review
  -> spec.yaml / spec.md
  -> Traceability + SDLC Handoff
```

The default enterprise adoption path is **module-first**. When the team already has module boundaries, four-view flows, RAG retrieval output, or a code knowledge graph, it does not need to excavate the full source code base from scratch.

### Verification Path: Source-First Evidence Repair

```text
Raw IBM i Evidence
  -> Evidence Intake
  -> Inventory
  -> Program / Flow / Data / Screen / Report Analysis
  -> Evidence Repair
  -> Module / BRD / Spec Synthesis
```

Source-level analysis is mainly used to repair missing evidence, resolve conflicts, verify high-risk rules, and close uncertainty gaps.

## Page Tree

```text
01 | Method, Principles & Delivery Process
02 | Scope, Non-Goals & Assumptions
03 | Evidence Model, SME Review & Traceability
04 | System Context & Architecture
05 | As-Is Business Processes
06 | Functional Requirements Catalogue
07 | Business Rules Catalogue
08 | Data Model & Data Dictionary
09 | Integrations, Batch Jobs & Scheduling
10 | NFRs, Controls & Observability
11 | Delivery Packaging, Gates & Handoff
```

## Standard Page Contract

Each page should follow the same structure:

```text
Purpose
Scope
Inputs
Outputs
Evidence Required
Open Questions / TBDs
Review Owner
Approval Gate
Examples / Templates
```

## 01 | Method, Principles & Delivery Process

Explain why this methodology exists, which problems it solves, and what the overall delivery chain looks like.

Key points to clarify:

- This is not code conversion; it is business intent recovery.
- `spec.yaml` is the structured source of truth, while `spec.md` is the human-readable review view.
- RAG is evidence context, not final truth.
- SMEs are the control point for legacy understanding.
- Every step must preserve evidence, confidence, TBDs, and approval status.

## 02 | Scope, Non-Goals & Assumptions

Define the current modernization scope, explicitly state what is out of scope, and record key assumptions.

Recommended content:

- In scope: business modules, programs, files, reports, batch jobs, and interfaces.
- Out of scope: modules not migrated in the current phase, historical data cleansing, non-core reports, and similar exclusions.
- Assumptions: rule continuity, target platform constraints, data availability, and SME availability.
- Risks: missing evidence, conflicting rules, implicit dependencies, and undocumented manual operations.

## 03 | Evidence Model, SME Review & Traceability

This is the core page and should appear early in the playbook.

Define four categories of knowledge:

```text
observed_behavior
inferred_business_rule
modernization_decision
unknown_tbd
```

Use a consistent evidence strength model:

```text
confirmed_from_code
observed_in_runtime
confirmed_by_sme
strongly_inferred
weakly_inferred
needs_sme_review
contradictory
missing
```

Approval rules:

- Content without evidence cannot be promoted into a requirement.
- Inferred rules must be confirmed by an SME.
- Modernization decisions must be approved by architecture or product owners.
- All `TBD-*` items must be resolved or explicitly marked as non-blocking by an SME.

## 04 | System Context & Architecture

Describe the context between the current legacy system and the target system.

Recommended content:

- Current IBM i / AS400 system boundary
- Upstream and downstream systems
- Human actors and operational roles
- External interfaces
- Batch and scheduling dependencies
- Data mastership and ownership
- Target-system decomposition principles

This page answers: "Where does this capability sit in the enterprise system landscape?"

## 05 | As-Is Business Processes

Capture the current business process before writing the target-state solution.

Organize the process using four views:

```text
Operation / Business Flow
System Flow
Program Flow
Data Flow
```

Each flow should capture at least:

- Trigger conditions
- Participating actors
- Inputs and outputs
- Main path
- Exception paths
- Key programs / files / reports
- Evidence IDs
- SME confirmation status

## 06 | Functional Requirements Catalogue

Extract functional requirements from confirmed business processes and rules.

Each requirement should include:

```text
Requirement ID
Capability
User / Actor
Statement
Acceptance Criteria
Linked Business Rules
Linked Evidence
Review Status
```

Avoid mixing implementation design into this page. Functional requirements should describe business capability, not how the target system will be coded.

## 07 | Business Rules Catalogue

Manage business rules in a central catalogue.

Each rule should include:

```text
BR ID
Rule Statement
Rule Type
Source Behavior
Evidence IDs
Confidence
SME Decision
Exceptions
Related Acceptance Criteria
```

Rules must distinguish between:

- Actual legacy-system behavior
- Business meaning inferred from that behavior
- Target-system decisions to retain, adjust, or retire the behavior

## 08 | Data Model & Data Dictionary

Capture data objects, fields, DDS / DB2 for i relationships, and target data semantics.

Recommended content:

- Physical files / logical files
- Key fields
- Field meanings
- Code values
- Referential relationships
- CRUD lifecycle
- Data ownership
- Data quality issues
- Target model implications

This page should avoid guessing meaning from field names alone. Field semantics require support from code, runtime samples, the data dictionary, or SME confirmation.

## 09 | Integrations, Batch Jobs & Scheduling

Capture interfaces, batch jobs, scheduling, reports, and asynchronous flows.

Recommended content:

- Job / scheduler inventory
- Program call-chain evidence (supporting trace, not business narrative)
- Submitted jobs
- Message queues / data queues
- File exchange
- Spool / report outputs
- External systems
- Retry / rerun / recovery behavior
- Cutoff time and period-end behavior

This page is often a high-risk area in modernization, especially around month-end, day-end, reruns, manual recovery, and operational workarounds.

## 10 | NFRs, Controls & Observability

Capture non-functional requirements, controls, and observability expectations.

Recommended content:

- Performance
- Availability
- Security
- Auditability
- Data retention
- Operational controls
- Reconciliation
- Error handling
- Logging and monitoring
- Regulatory or internal compliance needs

The key is to convert implicit legacy-system controls into explicit target-system requirements.

## 11 | Delivery Packaging, Gates & Handoff

Define when the package is ready to be handed off to downstream engineering.

Recommended delivery gates:

```text
Input readiness passed
Evidence authorization passed
SME review completed
Business rules approved
TBDs resolved or accepted
spec.yaml / spec.md generated
Traceability package complete
Golden master / validation scenarios prepared
SDLC handoff accepted
```

The final delivery package should include:

- BRD
- Validation scenarios
- `spec.yaml`
- `spec.md`
- `traceability.md`
- Modernization decisions
- Open questions
- SME sign-off record
- Downstream handoff package

## Action Plan

### Delivery Roadmap

| Phase | Timeline | Objective | Key Actions | Owner | Deliverables | Exit Criteria |
|---|---:|---|---|---|---|---|
| 1. Structure Setup | Week 1 | Establish the Confluence knowledge-base structure | Create the `Legacy Spec Factory` homepage; create the 11 core pages; apply a consistent page template | Modernization Lead / BA | Confluence page tree; standard page template | Pages are navigable; each page has Purpose / Inputs / Outputs / Review Gate |
| 2. Core Methodology | Week 1 | Clarify the methodology and core principles | Explain that this is not code conversion; define business intent recovery; explain `spec.yaml` / `spec.md`; clarify the roles of RAG, SMEs, and evidence | Modernization Lead / Architect | Homepage methodology; Method page; Evidence Model page | The team can explain how this differs from ordinary reverse engineering |
| 3. Evidence & Review Model | Week 1-2 | Establish evidence, review, and traceability rules | Define observed behavior, inferred business rule, modernization decision, and TBD; define evidence strength; define SME approval rules | BA / SME / Architect | Evidence taxonomy; SME review rules; traceability rules | Each rule has a clear way to link evidence and approval status |
| 4. Template Creation | Week 2 | Build reusable templates | Create templates for Scope, As-Is Process, Business Rule, Functional Requirement, Data Dictionary, Integration, SME Review, Traceability, and Handoff | BA / Solution Analyst | Confluence template set | A new module can start by copying the templates |
| 5. Pilot Module Selection | Week 2 | Select one pilot business module | Choose a module with manageable scope, SME support, and representative complexity; confirm input materials and boundaries | Modernization Lead / Product Owner / SME | Pilot scope; module owner; input checklist | Pilot scope, owner, and SME are confirmed |
| 6. Pilot Content Population | Week 3 | Populate the knowledge base with a real module | Fill in scope, as-is process, business rules, data model, batch/jobs, and integrations; mark `TBD-*`; link evidence IDs | BA / Engineer / SME | Pilot module pages; initial rule catalogue; open TBD list | The pilot module has an end-to-end draft |
| 7. SME Review | Week 3-4 | Have business and IBM i SMEs review key content | Run SME review; confirm observed behavior; approve or reject inferred rules; record open questions and decisions | SME / BA / Modernization Lead | SME decision log; approved rules; review notes | High-risk rules are reviewed; key TBDs are resolved or marked non-blocking |
| 8. Traceability & Handoff | Week 4 | Build the chain from evidence to delivery | Link evidence -> behavior -> business rule -> requirement -> acceptance criteria -> test / handoff item | BA / Architect / Delivery Lead | Traceability matrix; handoff checklist; spec package outline | At least one complete traceability chain can be demonstrated |
| 9. Governance Setup | Week 4 | Formalize quality gates and page statuses | Define Draft / In Review / Approved / Blocked / Retired; define input readiness, evidence approval, SME approval, and handoff readiness | Modernization Lead / QA / Architect | Governance rules; quality gate checklist | Documentation cannot enter delivery without review |
| 10. Rollout & Continuous Improvement | Ongoing | Extend the model to more modules and improve it continuously | Copy templates for new modules; run pilot retrospectives; capture good examples and anti-patterns; regularly review TBDs and traceability | Modernization Lead / Team Leads | Reusable playbook; example library; lessons learned | The team can start the next module using the same method |

### Execution Tracker

| Workstream | Task | Priority | Target Date | Status | Dependencies | Notes |
|---|---|---:|---|---|---|---|
| Confluence Setup | Create Legacy Spec Factory homepage | High | Week 1 | Not Started | None | Single entry point |
| Confluence Setup | Create 11 core child pages | High | Week 1 | Not Started | Homepage | Create after page titles are finalized |
| Methodology | Draft principles and delivery process | High | Week 1 | Not Started | Homepage | Emphasize evidence-backed modernization, not code conversion |
| Evidence | Define evidence taxonomy | High | Week 1 | Not Started | Methodology draft | Requires alignment with SMEs and architecture |
| Evidence | Define SME review and approval rules | High | Week 2 | Not Started | Evidence taxonomy | Determines which items can enter the spec |
| Templates | Create business rule template | High | Week 2 | Not Started | ID convention | Must include evidence IDs |
| Templates | Create traceability matrix template | High | Week 2 | Not Started | Evidence model | Used for pre-handoff checks |
| Pilot | Select pilot module | High | Week 2 | Not Started | Scope criteria | Keep the scope manageable |
| Pilot | Populate pilot module pages | High | Week 3 | Not Started | Templates, input materials | Allow draft quality first; do not aim for perfection on the first pass |
| Pilot | Conduct SME review | High | Week 4 | Not Started | Draft pilot pages | Record approved / rejected / TBD decisions |
| Delivery | Build handoff checklist | Medium | Week 4 | Not Started | Traceability matrix | Aligns with downstream SDLC |
| Governance | Define page status and gates | Medium | Week 4 | Not Started | Pilot findings | Use pilot lessons to shape the standard |
| Rollout | Publish pilot example as reference | Medium | Week 4+ | Not Started | SME-reviewed pilot | Becomes the reference example for later projects |
| Rollout | Schedule recurring review cadence | Medium | Ongoing | Not Started | Governance setup | Focus on TBDs, rule approval, and traceability |

## Suggested 30-Day Plan

| Week | Focus | Key Outcomes |
|---:|---|---|
| Week 1 | Structure and methodology | Build the Confluence page tree; complete the homepage, methodology page, and evidence model page; confirm ID conventions and page statuses |
| Week 2 | Templates and pilot selection | Complete core templates; scaffold Scope, Process, Business Rules, and Data Model pages; select the pilot module |
| Week 3 | Pilot population | Populate the pilot module; record observed behavior, business rules, and TBDs; prepare SME review materials |
| Week 4 | Review and standardization | Complete SME review; update rule status and traceability; summarize pilot lessons learned; formalize the team standard |

## Definition of Done

The first version of this Confluence knowledge base is done when:

- The 11 core pages have been created.
- Each page has a clear purpose, input, output, owner, and approval gate.
- The evidence taxonomy has been defined.
- At least one pilot module has been populated.
- At least one SME review has been completed.
- At least one traceability chain from evidence to business rule to acceptance criteria can be demonstrated.
- The team knows which template to use when starting a new module.
