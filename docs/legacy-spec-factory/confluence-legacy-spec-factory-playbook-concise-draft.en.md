# Legacy Spec Factory Internal Knowledge Base Draft

> Sync note: This English concise draft is maintained in lockstep with the Chinese concise draft [`confluence-legacy-spec-factory-playbook-concise-draft.md`](confluence-legacy-spec-factory-playbook-concise-draft.md). Any future change to structure, tables, headings, or content must be applied to both files.

## 1. Goal

Legacy Spec Factory is an evidence-backed method for IBM i / AS400 modernization. Its goal is not to directly translate RPGLE, CLLE, COBOL, or DDS code into Java. Its goal is to recover the real business intent embedded in the legacy system and produce auditable, reviewable specifications that can be handed off to downstream SDLC teams.

Core principles:

- Center the work on business capabilities, not individual programs.
- RAG / code knowledge graphs provide evidence context, but they are not final truth.
- Legacy behavior, inferred business rules, and modernization decisions must be managed separately.
- Key rules must be backed by evidence or reviewed by SMEs.
- `spec.yaml` / `spec.md` are the main downstream delivery inputs.

## 2. Recommended Page Structure

| No. | Page | Purpose |
|---:|---|---|
| 01 | Method, Principles & Delivery Process | Explain the methodology, core principles, and delivery process |
| 02 | Scope, Non-Goals & Assumptions | Define scope, non-goals, assumptions, and risks |
| 03 | Evidence Model, SME Review & Traceability | Define the evidence model, SME review rules, and traceability chain |
| 04 | System Context & Architecture | Describe legacy systems, target systems, and upstream/downstream relationships |
| 05 | As-Is Business Processes | Capture business, system, program, and data flows |
| 06 | Functional Requirements Catalogue | Consolidate functional requirements for downstream teams |
| 07 | Business Rules Catalogue | Manage business rules, evidence, confidence, and SME decisions |
| 08 | Data Model & Data Dictionary | Capture data objects, field meanings, relationships, and data quality issues |
| 09 | Integrations, Batch Jobs & Scheduling | Record interfaces, batch jobs, scheduling, reports, and rerun mechanisms |
| 10 | NFRs, Controls & Observability | Capture non-functional requirements, controls, audit, and monitoring needs |
| 11 | Delivery Packaging, Gates & Handoff | Define delivery packages, quality gates, and downstream handoff standards |

## 3. Page Draft: 01 | Method, Principles & Delivery Process

### Purpose

This page explains why Legacy Spec Factory exists, what problem it solves, and how a legacy modernization effort should move from raw system knowledge to an approved, delivery-ready specification package.

Legacy modernization is not a code conversion exercise. The goal is not to translate RPGLE, CLLE, COBOL, DDS, or legacy jobs directly into Java or cloud services. The real goal is to recover the business intent embedded in the legacy system, separate proven behavior from assumptions, and create a trusted specification layer that both humans and downstream engineering agents can use.

### Why This Method Exists

Many legacy modernization efforts fail because they treat the old system as a source-code translation problem. In practice, the most valuable knowledge is distributed across many places:

- source code and control flow
- DDS files and DB2 for i tables
- batch jobs, schedulers, job logs, and spool files
- screens, reports, and operational procedures
- SME knowledge that was never fully documented

Legacy Spec Factory turns these fragmented sources into evidence-backed business understanding. The output is not just documentation. It is a reviewed, traceable specification package that can guide target-system design, development, testing, and cutover planning.

### Core Principles

| Principle | Meaning |
|---|---|
| Business intent over code conversion | We recover what the business capability does and why it exists, instead of mechanically translating legacy implementation details. |
| Evidence over assumptions | Every important behavior, rule, and decision should link back to code, runtime evidence, data, documents, or SME confirmation. |
| RAG as context, not final truth | RAG, ARCAD, code knowledge graphs, and data dictionaries help locate evidence, but their output must still be validated. |
| SME as control point | SMEs decide whether inferred rules, ambiguous behavior, and modernization decisions are valid enough to move forward. |
| Separate observed, inferred, and decided | Legacy behavior, inferred business rules, and target-system decisions must not be mixed together. |
| Traceability by default | Evidence, behaviors, rules, requirements, acceptance criteria, tests, and handoff items should be connected through stable IDs. |
| TBDs stay visible | Unknowns, conflicts, and missing evidence must be explicitly tracked instead of silently filled in. |

### Delivery Process

```text
RAG / Source Evidence / SME Knowledge
  -> Module Context
  -> As-Is Business Processes
  -> Observed Behaviors
  -> Business Rules
  -> Functional Requirements
  -> SME Review
  -> spec.yaml / spec.md
  -> Traceability Package
  -> SDLC Handoff
```

### Key Artifacts

| Artifact | Purpose |
|---|---|
| Module Context | Defines the business capability, system boundary, actors, flows, and available evidence |
| As-Is Process | Describes how the legacy process works today across business, system, program, and data views |
| Business Rules Catalogue | Captures rules, evidence, confidence, SME decisions, and exceptions |
| Functional Requirements Catalogue | Converts approved business understanding into downstream requirements |
| `spec.yaml` | Structured source of truth for automation, engineering agents, and downstream SDLC |
| `spec.md` | Human-readable review view for SMEs, architects, analysts, and delivery teams |
| Traceability Package | Connects evidence to behavior, rules, requirements, acceptance criteria, tests, and handoff items |

### Approval Expectations

A page or artifact should not move to the next delivery step unless:

- key claims have linked evidence
- inferred business rules have SME review status
- open questions are recorded as `TBD-*`
- confidence level is visible
- modernization decisions are separated from legacy behavior
- approval status is clear: Draft, In Review, Approved, Blocked, or Retired

### Output of This Page

After reading this page, the team should understand:

- why this method is needed
- how it differs from code conversion
- what role evidence and SMEs play
- how work moves from legacy understanding to approved specifications
- what quality bar must be met before downstream handoff

## 4. Page Drafts: 02-11

### 02 | Scope, Non-Goals & Assumptions

**Purpose:** Define the boundary of the modernization effort so a module pilot does not expand into an uncontrolled system rewrite.

**What to Capture**

| Area | Content |
|---|---|
| In Scope | Business capabilities, programs, files, reports, batch jobs, interfaces, and data objects. |
| Non-Goals | Items that will not be migrated, analyzed, refactored, or owned in the current phase. |
| Assumptions | Rule continuity, target platform constraints, SME availability, data availability, and similar assumptions. |
| Risks | Missing evidence, conflicting rules, hidden dependencies, undocumented manual operations, and over-broad scope. |
| Open Questions | Questions that need product, architecture, SME, or delivery-owner confirmation. |

**Outputs:** scope statement, non-goals list, assumptions log, risk / TBD list.

**Approval Gate:** scope owner and SME have confirmed the boundary; out-of-scope items will not silently enter delivery.

### 03 | Evidence Model, SME Review & Traceability

**Purpose:** Define how the team decides what is fact, what is inference, and what is a target-system decision, while keeping every key claim traceable.

**What to Capture**

| Area | Content |
|---|---|
| Knowledge Types | `observed_behavior`, `inferred_business_rule`, `modernization_decision`, `unknown_tbd`. |
| Evidence Strength | `confirmed_from_code`, `observed_in_runtime`, `confirmed_by_sme`, `strongly_inferred`, `weakly_inferred`, `contradictory`, `missing`. |
| Evidence IDs | ID, source, path, sensitivity level, and availability for each evidence item. |
| SME Decisions | Confirmed, rejected, modified, marked non-blocking, or requested for evidence repair. |
| Traceability Links | evidence -> behavior -> rule -> requirement -> acceptance criteria -> test / handoff item. |

**Outputs:** evidence taxonomy, SME decision log, traceability rules, TBD policy.

**Approval Gate:** content without evidence cannot become a requirement; inferred rules must carry SME review status.

### 04 | System Context & Architecture

**Purpose:** Explain where the capability sits in the enterprise landscape and how the legacy and target systems relate to each other.

**What to Capture**

| Area | Content |
|---|---|
| Legacy Boundary | Current IBM i / AS400 subsystem, program group, file group, and runtime boundary. |
| Actors | Business users, operators, support teams, external systems, and automated jobs. |
| Upstream / Downstream | Callers, callees, data sources, data consumers, and report recipients. |
| Target Context | Target services, APIs, databases, event flows, batch jobs, or platform constraints. |
| Architecture Decisions | Architecture points to retain, split, replace, or redesign. |

**Outputs:** context diagram, system inventory, integration map, architecture assumptions.

**Approval Gate:** key upstream/downstream systems and owners are identified; target architecture assumptions are approved by architecture or marked as TBD.

### 05 | As-Is Business Processes

**Purpose:** Record how the legacy process actually works today before writing the target-state solution.

**What to Capture**

| Area | Content |
|---|---|
| Business Flow | Business trigger, actors, main path, exception paths, and business outcome. |
| System Flow | System interactions, interface calls, batch triggers, and external dependencies. |
| Program Flow | Supporting technical trace: entry points, key branches, error paths, and call-chain evidence. Do not use this as the main business-process narrative. |
| Data Flow | Inputs, outputs, file reads/writes, key fields, and data-state changes. |
| Controls / Workarounds | Manual checks, reruns, reconciliations, report checks, and operational routines. |

**Outputs:** as-is process map, flow notes, observed behavior list, open questions.

**Approval Gate:** critical paths and high-risk exception paths have SME review; unconfirmed content is recorded as `TBD-*`.

### 06 | Functional Requirements Catalogue

**Purpose:** Convert confirmed business processes and rules into functional requirements that downstream teams can consume.

**What to Capture**

| Area | Content |
|---|---|
| Requirement ID | Stable ID for traceability and reference. |
| Actor / User | Who triggers or uses the capability. |
| Requirement Statement | What the business capability must do, without describing the technical implementation. |
| Linked Rules | Related `BR-*` business rules. |
| Acceptance Criteria | Verifiable acceptance conditions. |
| Evidence Links | Supporting evidence, behavior, or SME decision. |
| Status | Draft, In Review, Approved, Blocked, or Retired. |

**Outputs:** functional requirements catalogue, acceptance criteria seeds, open requirement TBDs.

**Approval Gate:** every requirement traces back to confirmed behavior, an approved business rule, or an explicit modernization decision.

### 07 | Business Rules Catalogue

**Purpose:** Manage business rules centrally so they are not scattered across process maps, meeting notes, code comments, and requirements documents.

**What to Capture**

| Area | Content |
|---|---|
| BR ID | Stable business rule ID. |
| Rule Statement | Clear and verifiable rule statement. |
| Rule Type | Calculation, validation, eligibility, routing, state transition, control, or exception rule. |
| Source Behavior | Legacy behavior or runtime observation behind the rule. |
| Evidence IDs | Code, runtime logs, reports, data samples, or SME confirmation. |
| Confidence / Status | Confidence level and approval status. |
| Exceptions | Boundary conditions, special customers, period processing, reruns, or manual handling. |
| Modernization Implication | Retain, adjust, retire, or redesign in the target system. |

**Outputs:** business rules catalogue, exception list, SME decision log.

**Approval Gate:** inferred rules cannot be marked Approved without SME confirmation; conflicting rules must have a resolution or TBD.

### 08 | Data Model & Data Dictionary

**Purpose:** Capture legacy data objects, field semantics, relationships, and data quality issues as trusted input for the target data model.

**What to Capture**

| Area | Content |
|---|---|
| Data Objects | PF, LF, DB2 for i table, view, data area, or work file. |
| Field Meaning | Business meaning, format, length, value range, and code values. |
| Keys / Relationships | Primary keys, access paths, logical files, cross-table relationships, and reference rules. |
| CRUD Lifecycle | Programs that create, read, update, delete, or archive data. |
| Ownership | Data owner, source of record, and downstream consumers. |
| Quality Issues | Missing values, duplicates, historical dirty data, implicit codes, and special values. |
| Target Implications | Target-field mapping, split, merge, cleanup, and migration notes. |

**Outputs:** data dictionary, relationship map, CRUD matrix, data quality notes.

**Approval Gate:** key field meanings must not be guessed from names alone; they need support from code, dictionary entries, samples, or SMEs.

### 09 | Integrations, Batch Jobs & Scheduling

**Purpose:** Record interfaces, batch jobs, schedules, reports, and asynchronous flows so runtime chains are not missed during modernization.

**What to Capture**

| Area | Content |
|---|---|
| Jobs / Schedules | Job name, trigger, frequency, time window, dependencies, and owner. |
| Program Chain | CL, RPGLE, SQL, report, or utility programs called by the job. |
| External Interfaces | File exchange, message queue, data queue, API, FTP, or third-party system. |
| Reports / Spool | Reports, spool outputs, recipients, business purpose, and retention requirements. |
| Retry / Rerun | Failure handling, rerun steps, idempotency, manual intervention, and recovery flow. |
| Cutoff / Period-End | Day-end, month-end, year-end, freeze windows, and special business days. |

**Outputs:** integration inventory, batch calendar, job dependency map, recovery notes.

**Approval Gate:** critical jobs have known runtime conditions, failure handling, and owners; unknown dependencies are recorded as TBD.

### 10 | NFRs, Controls & Observability

**Purpose:** Turn implicit legacy controls and operational expectations into explicit target-system non-functional requirements.

**What to Capture**

| Area | Content |
|---|---|
| Performance | Response time, throughput, batch window, peak load, and capacity assumptions. |
| Availability | Availability target, maintenance window, recovery time, and business continuity requirements. |
| Security | Authentication, authorization, sensitive data, segregation of duties, and access controls. |
| Auditability | Audit logs, operation records, approval trail, and regulatory requirements. |
| Reconciliation | Reconciliation, control totals, report checks, and variance handling. |
| Error Handling | Error classification, retry, alerting, manual handling, and user messaging. |
| Observability | Logs, metrics, traces, dashboards, alerts, and runbooks. |

**Outputs:** NFR catalogue, controls matrix, observability requirements, operational acceptance criteria.

**Approval Gate:** high-risk controls have an owner, validation method, and downstream implementation responsibility.

### 11 | Delivery Packaging, Gates & Handoff

**Purpose:** Define when the specification package is ready for downstream engineering, testing, architecture, or AI-native SDLC.

**What to Capture**

| Area | Content |
|---|---|
| Required Artifacts | BRD, validation scenarios, `spec.yaml`, `spec.md`, traceability, decision log. |
| Quality Gates | input readiness, evidence approval, SME approval, traceability completeness, handoff readiness. |
| Open TBDs | Unresolved questions, owner, target date, and blocking status. |
| Approvals | SME, product, architecture, delivery, and QA sign-off. |
| Handoff Consumers | Downstream teams, agents, systems, tests, or migration owners. |
| Validation Plan | Golden master, parallel run, acceptance tests, or manual validation. |

**Outputs:** handoff checklist, approved spec package, traceability package, delivery notes.

**Approval Gate:** `spec.yaml` / `spec.md` are approved; blocking TBDs are closed; traceability is sufficient for downstream implementation and testing.

## 5. Standard Page Template

Each page should use the same structure:

| Section | Content |
|---|---|
| Purpose | What problem this page solves |
| Scope | What is covered and not covered |
| Inputs | Required input materials |
| Outputs | Expected page outputs |
| Evidence Required | Evidence that must be linked |
| Open Questions / TBDs | Unconfirmed questions |
| Review Owner | Who owns review |
| Approval Gate | Conditions required before moving forward |

## 6. Evidence and Review Model

Knowledge types:

| Type | Meaning |
|---|---|
| `observed_behavior` | Real legacy behavior proven by code, runtime logs, reports, or samples |
| `inferred_business_rule` | Business rule inferred from behavior, code, or data |
| `modernization_decision` | Target-system design decision or tradeoff |
| `unknown_tbd` | Issue with missing evidence, unclear meaning, or conflicting evidence |

Evidence strength:

| Strength | Meaning |
|---|---|
| `confirmed_from_code` | Directly proven by source code |
| `observed_in_runtime` | Proven by job logs, spool files, sample transactions, or reports |
| `confirmed_by_sme` | Explicitly confirmed by an SME |
| `strongly_inferred` | Strongly inferred from multiple evidence points, but still needs review |
| `weakly_inferred` | Weak inference; cannot directly become a requirement |
| `contradictory` | Evidence conflicts |
| `missing` | Required evidence is missing |

Approval rules:

- Content without evidence cannot become a formal requirement.
- Inferred business rules must be confirmed by SMEs.
- Modernization decisions must be confirmed by product, architecture, or delivery owners.
- All `TBD-*` items must be resolved or explicitly marked as non-blocking.

## 7. Recommended Adoption Path

```text
RAG / Code Knowledge Graph / Source Evidence
  -> Module Context
  -> As-Is Process
  -> Business Rules
  -> Functional Requirements
  -> spec.yaml / spec.md
  -> Traceability Package
  -> SDLC Handoff
```

Start from the module view by default. If module boundaries, flows, and RAG evidence are already available, a full source-code excavation is not required first. Source-level analysis is mainly used to repair missing evidence, resolve conflicts, verify high-risk rules, and close TBDs.

## 8. Action Plan

| Phase | Timeline | Objective | Key Actions | Deliverables |
|---|---:|---|---|---|
| 1. Build Structure | Week 1 | Establish the Confluence page structure | Create the homepage and 11 child pages; apply the standard page template | Page tree and blank templates |
| 2. Align Methodology | Week 1 | Build shared methodology alignment | Clarify the goal, principles, evidence model, SME role, and delivery path | Methodology homepage and evidence model page |
| 3. Create Templates | Week 2 | Enable the team to execute from templates | Create Scope, Process, Rule, Requirement, Data, Integration, Traceability, and Handoff templates | Reusable page templates |
| 4. Select Pilot Module | Week 2 | Select one real module for pilot | Confirm module boundary, input materials, owner, and SME | Pilot scope and input checklist |
| 5. Populate Pilot | Week 3 | Validate the structure with real content | Populate flows, rules, data, integrations, batch jobs, and TBDs | Pilot module draft |
| 6. Run SME Review | Week 3-4 | Review high-risk rules and open questions | Run SME review; confirm, reject, or mark rules | SME decision log and approved rules |
| 7. Build Traceability | Week 4 | Build the chain from evidence to delivery | Link evidence -> behavior -> rule -> requirement -> acceptance criteria | Traceability matrix |
| 8. Standardize & Roll Out | Ongoing | Make this a repeatable team workflow | Review pilot lessons; capture good examples and anti-patterns; roll out to more modules | Team playbook and example library |

## 9. Execution Tracker

| Task | Priority | Owner | Target | Status |
|---|---:|---|---|---|
| Create Confluence homepage | High | Modernization Lead | Week 1 | Not Started |
| Create 11 child pages | High | BA | Week 1 | Not Started |
| Draft methodology summary | High | Modernization Lead / Architect | Week 1 | Not Started |
| Define evidence taxonomy | High | BA / SME / Architect | Week 1 | Not Started |
| Create business rule template | High | BA | Week 2 | Not Started |
| Create traceability template | High | BA / Architect | Week 2 | Not Started |
| Select pilot module | High | Product Owner / SME | Week 2 | Not Started |
| Populate pilot pages | High | BA / Engineer | Week 3 | Not Started |
| Run SME review | High | SME / BA | Week 4 | Not Started |
| Finalize handoff checklist | Medium | Delivery Lead / Architect | Week 4 | Not Started |
| Publish pilot as reference | Medium | Modernization Lead | Week 4+ | Not Started |

## 10. Definition of Done

The first version of the knowledge base is done when:

- The 11 core pages have been created.
- Each page has purpose, inputs, outputs, owner, and approval gate.
- The evidence model and SME review rules have been defined.
- At least one pilot module has been populated.
- At least one SME review has been completed.
- At least one complete chain can be demonstrated: evidence -> behavior -> business rule -> requirement -> acceptance criteria.
- The team knows which template to use when starting the next module.
