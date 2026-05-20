# Module Analysis Model: The 4-View Standard

This document defines the standard module-level analysis model used by
Legacy Spec Factory. It is the design basis for the
`legacy-ibmi-module-analyzer` skill and the input contract for the
`legacy-spec-writer` skill.

## Origin

Banking, insurance, and securities firms have used a 4-view model for
30+ years to document, modernize, and audit large mainframe / midrange
systems. The view names vary by firm and methodology (TOGAF, Zachman,
shop-internal frameworks), but the substance is consistent.

Legacy Spec Factory adopts the four views with concrete IBM i bindings
so they are executable, not just aspirational.

## The Four Views

Each module produces all four views. They are complementary; together they
form a complete picture of one business module.

### View 1 — Operation Flow / Business Background

**Question answered:** "What does this module do for the business?"

**Captures:**
- Business scope statement (e.g., "Card Authorization for On-Us Transactions")
- Business actors (cardholders, merchants, banks, risk team, call center)
- Business events processed (swipe, online, refund, pre-auth, chargeback, …)
- BAU (Business As Usual) rhythm: cut-off times, peak hours, month-end,
  year-end, seasonal patterns
- Manual intervention points (reject queue, manual approval, compensation
  transactions)
- Exception handling (chargeback, dispute, fraud lifecycle)
- Business-rule seeds (BR-\* candidates; resolved to rules by spec-writer)

**Primary source:** SME interviews, business documentation, operations
manuals, BAU notes. Code is a secondary source.

**Anti-pattern:** Do not derive business rules from field names. The fact
that a field is called `CREDLIMIT` does not explain *why* the limit exists,
*who* sets it, *how often* it changes, or *what happens* when it is
breached. The Operation Flow captures the business reality the code is
trying to encode.

### View 2 — System Flow

**Question answered:** "How does this module participate in the broader
system landscape?"

**Captures:**
- Upstream systems (ATM, POS, internet banking, mobile, call center, …)
- Downstream systems (clearing, GL, risk, fraud detection, reporting,
  analytics, …)
- External interfaces (Visa, Mastercard, UnionPay, SWIFT, regulator,
  partner banks)
- Integration patterns (real-time API, batch file drop, MQ message,
  IFS file, JDBC, web service)
- Synchronous vs asynchronous boundaries
- SLA constraints (response time, throughput, cut-off windows)
- Network and security boundaries (DMZ, encryption, mTLS, signed payloads)

**Primary source:** Architecture diagrams, integration specifications,
operations runbooks. Code confirms or refutes; SME judgment fills gaps.

### View 3 — Program Flow

**Question answered:** "What is the actual program-level call structure
across all transactions in this module?"

**Captures:**
- Inventory of flows in scope (one row per `flow-<FLOW-SLUG>.md`
  produced by `legacy-ibmi-flow-analyzer`)
- Per-flow summary: trigger model, entry program, exit program, runtime
  model (batch, interactive, scheduled, triggered, API)
- Cross-flow dependencies: which flow must run before which; which flow
  writes data another flow reads
- Shared sub-programs called from multiple flows (utility programs,
  validation routines, audit writers)
- Overall call topology of the module

**Primary source:** All `flow-<FLOW-SLUG>.md` documents produced by
`legacy-ibmi-flow-analyzer`, plus their child `program-analysis-<OBJ-ID>.md`
documents.

**This view is the aggregate of the application/program perspective.**
It does not re-analyze individual programs; it references and synthesizes
them.

### View 4 — Data Flow

**Question answered:** "How does data move through this module?"

**Captures:**
- All data objects in scope (PF, LF, DSPF, PRTF, \*DTAARA, \*DTAQ, \*MSGF,
  copybooks, parameter data structures) — aggregated from flow `DATA-*`
  rows and backed by program Data Touch Maps / Object Dependencies
- Data lifecycle per object: **Created → Updated → Read → Archived → Purged**
  with the program(s) responsible at each stage
- Critical data trails (e.g., a transaction record's path from intake to
  GL posting to reporting to archive)
- Shared data objects within the module (coupling hotspots — files,
  data areas, data queues touched by multiple flows)
- DB table relationships (PK / FK, master / detail, lookup)
- Cross-module data dependencies (input interface files, output interface
  files, shared reference tables)
- Data retention / archival policy (where applicable)

**Primary source:** Aggregated `Cross-Program Data Flow` sections from
every `flow-<FLOW-SLUG>.md`, backed by every program's `Data Touch Map`
and `Object Dependencies`; DDS definitions from inventory; SME notes on
data ownership and retention.

## View Independence vs Cross-View Linking

The four views are produced together but read independently — an SME for
business operations reads View 1, an integration architect reads View 2,
a developer reads View 3, a data analyst reads View 4.

However, every claim must be cross-linkable:
- A business rule seed in View 1 must reference the program(s) in View 3
  that enforce it (or the missing programs that should)
- An upstream system in View 2 must reference the entry program(s) it
  invokes in View 3
- A data object's lifecycle in View 4 must reference the program(s) in
  View 3 that act on it

This is enforced through the shared ID conventions
(`docs/id-conventions.md`): every business actor, system, program,
data object, and flow has a stable ID, and cross-references use those IDs.

## Output Artifact

A module analysis produces a directory:

```
04_modules/<MODULE-SLUG>/
├── module-overview.md          ← summary, 4-view index, blocking TBDs
├── 01-operation-flow.md        ← View 1: Business view
├── 02-system-flow.md           ← View 2: Integration view
├── 03-program-flow.md          ← View 3: Application / program view (aggregates flows)
├── 04-data-flow.md             ← View 4: Data view
└── module-review-checklist.md  ← SME sign-off for the whole module
```

## Granularity Rules

- **Capability ⊂ Module.** A module contains one or more business
  capabilities. (A capability such as "Credit Limit Check" lives inside a
  module such as "Card Authorization".) `spec.yaml` is produced per
  capability; the module analysis informs all capabilities under it.
- **Flow ⊂ Module.** A module contains multiple flows (business
  transactions). A flow is the unit produced by `legacy-ibmi-flow-analyzer`.
- **Program ⊂ Flow.** A program participates in one or more flows.
- **Object ⊂ Program.** Objects (files, data areas, …) are referenced by
  one or more programs.

```
Module
├─ Capability   (BR-* groups; spec.yaml unit)
├─ Flow         (business transaction; flow-*.md)
│   └─ Program  (program-analysis-*.md)
│       └─ Object Dependencies
└─ BAU notes    (manual, periodic, exception-handling processes)
```

## Status Values (per view)

Each view, independently:
- `draft` — initial synthesis, ready for SME review
- `needs_sme_review` — has blocking TBDs or ambiguities
- `approved` — SME confirmed
- `approved_with_non_blocking_tbd` — approved with known non-blocking gaps
- `rejected` — SME found errors

The whole module is `approved` only when **all four views are at least
`approved_with_non_blocking_tbd`**.

## Why Four Views, Not Three or Five

- **Three views** (e.g., dropping Data Flow into Program Flow) loses the
  data-ownership story, which is critical for modernization (target system
  data model design depends on legacy data flow).
- **Five views** (e.g., adding a separate "Security view" or "Performance
  view") spreads attention thin in MVP; security and performance concerns
  are folded into System Flow and Operation Flow respectively, and can be
  extracted in a later release if needed.

Four is the smallest number that produces a complete picture without
overlap or omission for an IBM i / AS400 reverse-modernization context.

## Relationship to Existing Documents

- `docs/id-conventions.md` — stable IDs used across all four views
- `docs/evidence-and-knowledge-taxonomy.md` — evidence tagging applies to
  every claim in every view
- `docs/skill-review-gate.md` — module-analyzer must score ≥ 9.5 / 10
- `docs/runtime-matrix.md` — module-analyzer must sync to all runtime adapters
- `schemas/spec.schema.yaml` — `spec.yaml` references the module ID and
  capability ID; module analysis grounds those references
