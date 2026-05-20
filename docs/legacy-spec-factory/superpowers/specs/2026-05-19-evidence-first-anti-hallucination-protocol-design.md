# Evidence-First Anti-Hallucination Protocol Design

Status: approved for implementation planning
Date: 2026-05-19
Repository: Legacy Spec Factory

## Purpose

Legacy Spec Factory must help teams understand large IBM i / AS400 systems
without allowing AI-generated summaries to become unsupported facts. This design
defines an evidence-first anti-hallucination protocol for IBM i analysis skills,
especially when processing large RPG programs, multi-program flows, data flows,
and modernization handoffs.

The protocol strengthens the existing taxonomy in
`docs/evidence-and-knowledge-taxonomy.md`. It does not replace that taxonomy.
Instead, it makes the taxonomy operational across program analysis, flow
analysis, module synthesis, SME review, and spec generation.

## Problem

Large RPG and CL systems often contain tens of thousands of lines, many legacy
subroutines, shared utility programs, display files, printer files, data queues,
and database side effects. If an AI agent summarizes these systems in one pass,
it can easily:

- treat naming hints as business facts
- turn inferred intent into approved requirements
- omit common utility calls or shared dependencies
- miss file update side effects while describing control flow
- smooth over contradictions between code, runtime evidence, and SME memory
- generate Java/cloud designs directly from legacy code without a reviewed spec
  boundary

The target behavior is not simply "be cautious." The target behavior is an
auditable evidence protocol where every claim has a known support level and a
safe downstream route.

## Design Principles

1. **Evidence before narrative**: agents collect structured facts before writing
   business summaries.
2. **Claims are typed**: observed behavior, inferred rule, unknown, SME
   confirmation, and modernization decisions are never mixed.
3. **No evidence, no fact**: unsupported statements must be marked as inferred
   or moved to a ledger for review.
4. **Program facts precede flow facts**: flow-level conclusions must be assembled
   from program-level call maps, data touch maps, object dependencies, and
   runtime evidence.
5. **Runtime calibrates source analysis**: job logs, screens, spool files, and
   transaction samples confirm or challenge source-derived understanding, but do
   not replace source analysis.
6. **SMEs resolve business meaning**: agents can identify behavior and propose
   questions; SMEs confirm business intent and resolve material ambiguity.
7. **Modernization decisions are separate**: target Java/cloud design choices
   are documented as modernization decisions, not as legacy facts.

## Claim Model

Each material claim must carry a knowledge type and evidence support. The
repository already defines canonical knowledge types and evidence strengths. The
protocol maps common analysis language to those canonical terms:

| Analysis wording | Canonical type or strength | Meaning |
| --- | --- | --- |
| `observed_from_code` | `confirmed_from_code` evidence | Directly visible in RPG, CL, DDS, SQL, or object metadata |
| `observed_from_runtime` | `observed_in_runtime` evidence | Visible in job logs, spool output, screens, traces, or approved samples |
| `confirmed_by_sme` | `confirmed_by_sme` evidence | Confirmed by named IBM i, business, or operations SME |
| `inferred` | `inferred_business_rule` with `strongly_inferred` or `weakly_inferred` evidence | Plausible interpretation that cannot become a requirement without confirmation |
| `unknown_or_conflicting` | `unknown_tbd` with `missing`, `needs_sme_review`, or `contradictory` evidence | Must stay out of approved requirements until resolved or explicitly deferred |
| `modernization_decision` | `modernization_decision` | Target-state design choice, approved through architecture/product governance |

## Required Claim Fields

Every behavior, business rule, call edge, data-flow edge, side effect, and
modernization decision should be expressed with these fields when it is used
downstream:

```yaml
id:
statement:
knowledge_type:
evidence_ids:
confidence:
review_status:
review_notes:
downstream_allowed:
```

`downstream_allowed` is derived from the claim and evidence state:

| Value | Meaning |
| --- | --- |
| `yes` | Claim may be used in spec or handoff artifacts |
| `with_warning` | Claim may be included only with visible caveat or SME deferral |
| `no` | Claim must remain in analysis, review, or TBD sections |

## Hard Rules

1. A claim without `evidence_ids` cannot be written as a fact.
2. `inferred_business_rule` cannot become an approved requirement until SME
   confirmed or explicitly accepted through review governance.
3. `unknown_tbd` cannot enter `spec.yaml` as a requirement.
4. `modernization_decision` cannot be described as legacy behavior.
5. Every Program Call Map edge must cite code, metadata, runtime, or SME
   evidence.
6. Every Data Touch Map row must cite the carrier, operation, and source
   location or runtime observation.
7. Every Cross-Program Data Flow row must identify producer, consumer, carrier,
   timing, state impact, and evidence.
8. Large RPG programs must be analyzed through structure-first passes before
   business narrative generation.
9. Contradictions must be recorded; agents must not silently reconcile them.
10. Missing artifacts must create review items rather than invented behavior.

## Layered Workflow

### Program Layer

The program analyzer should produce evidence-backed program facts before any
business summary:

- Program Call Map
- Data Touch Map
- Object Dependencies
- File I/O and database operations
- External calls and IBM i APIs
- indicator, data structure, and critical-field notes when relevant
- contradiction and TBD ledger

For very large RPG programs, the analyzer should avoid one-pass summaries. It
should first identify routines, subroutines, procedures, call sites, file specs,
display/report interactions, and major state transitions. Only after that should
it synthesize behavior.

### Flow Layer

The flow analyzer should assemble flows from program outputs rather than
inventing transaction narratives directly from raw source:

- Transaction Call Map derives from program call edges.
- Cross-Program Data Flow derives from Data Touch Maps and Object Dependencies.
- Common dependency handling preserves all edges but may fold technical utility
  hubs in visual diagrams.
- Runtime evidence is used to confirm exercised paths, reveal dynamic calls,
  and challenge unused or unreachable code assumptions.

### Module Layer

The module analyzer should aggregate approved flow findings into business module
views:

- lifecycle of important business data
- cross-flow coupling through files, queues, screens, reports, and common
  programs
- business capabilities supported by observed behavior
- unresolved review items and risk areas

Module-level claims must point back to program and flow evidence. A shared file
or common program is not enough to assert a business capability unless the
underlying data-flow or behavior evidence supports that interpretation.

### Spec Layer

The spec writer should only promote claims when the evidence state permits it:

- approved observed behavior can become legacy behavior requirements
- SME-confirmed inferred rules can become business rules
- unresolved inferred rules become open questions or review notes
- modernization decisions are written separately from legacy behavior
- blocking TBDs prevent clean handoff unless explicitly deferred by governance

## Ledgers

The protocol requires visible ledgers for uncertainty instead of hiding
uncertainty in polished prose.

### TBD Ledger

Used when evidence is missing, unclear, or waiting for SME judgment.

Required fields:

- `tbd_id`
- `issue`
- `category`
- `blocking`
- `resolution_path`
- `owner`
- `related_claims`

### Contradiction Ledger

Used when evidence sources conflict.

Required fields:

- `conflict_id`
- `claim_or_area`
- `source_a`
- `source_b`
- `impact`
- `recommended_resolution`
- `owner`

### Inference Ledger

Used when the AI proposes a plausible interpretation that is not yet approved.

Required fields:

- `inference_id`
- `statement`
- `supporting_evidence`
- `confidence`
- `why_not_fact_yet`
- `sme_question`
- `downstream_allowed`

## Example

Preferred:

```text
SR800 appears to route or validate operator/message state.
knowledge_type: inferred_business_rule
evidence_ids: [EV-CODE-CUE64-SR800-CALL, EV-CODE-SR800-CCOPRMSG]
confidence: medium
review_status: needs_sme_review
downstream_allowed: no
review_notes: Confirm whether this is business validation, technical message
routing, or both.
```

Not allowed:

```text
SR800 validates account status.
```

The second statement may be true, but the protocol does not allow it unless
account-status evidence is present and the claim is typed correctly.

## Validation Strategy

Implementation should add validator checks in phases:

1. Check that required output sections exist.
2. Check that material rows include evidence references.
3. Check that claim types and evidence strengths use canonical values.
4. Check that inferred or unknown claims are not promoted into approved spec
   requirements.
5. Check that contradiction, TBD, and inference ledgers are preserved during
   downstream synthesis.

Validation should prefer clear findings over false precision. A validator does
not need to understand every RPG statement to catch missing evidence, missing
claim type, unsupported promotion, or absent review routing.

## Rollout Plan

Recommended rollout order:

1. Update shared references and templates for the protocol vocabulary.
2. Apply the contract to `legacy-ibmi-program-analyzer`.
3. Apply the contract to `legacy-ibmi-flow-analyzer`.
4. Apply promotion rules to `legacy-ibmi-module-analyzer`.
5. Apply final gating to `legacy-spec-writer` and handoff skills.
6. Extend `legacy-step-validator` with anti-hallucination checks.
7. Add smoke examples covering unsupported inference, contradictory evidence,
   and missing evidence.

## Non-Goals

- This design does not require a full RPG parser before improving safety.
- This design does not require a graph database in the first implementation.
- This design does not attempt to auto-resolve business meaning without SME
  review.
- This design does not make diagrams the source of truth; diagrams remain
  navigation aids over evidence-backed tables.

## Approval Criteria

The implementation is acceptable when:

- all IBM i analysis skills use consistent claim and evidence vocabulary
- program, flow, module, and spec outputs preserve observed, inferred, unknown,
  SME-confirmed, and modernization-decision boundaries
- unsupported claims are blocked or visibly routed to review
- validators catch missing evidence on material claims
- existing skill sync and contract checks pass

## Implementation Boundary

This design is approved for implementation planning. It does not itself change
runtime behavior until the canonical skill templates, references, examples, and
validators are updated and synced into runtime copies.
