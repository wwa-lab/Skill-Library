<!--
Legacy Spec Factory
Copyright 2026 Leo L Zhang
License: Apache License 2.0
-->

# Atlas SDD Chain Contract

This document defines **what this skill hands to the Atlas SDD chain** and,
just as importantly, **what it does not**. The boundary matters: Atlas owns
stories, architecture, design, code, and tests; this skill stops at the
handoff package.

## What "SDD" Means Here

"SDD" in this repo refers to the **Atlas Software Design and Development
chain**, listed in `README.md` under the row range #19–#28:

- `req-to-user-story`
- `user-story-to-spec`
- `spec-to-architecture`
- `architecture-to-design`
- `design-to-tasks`
- `tasks-to-implementation`
- `tasks-to-code`
- `review-doc-quality`, `review-code-against-design`, `architecture-review`

This skill (`legacy-brd-to-sdd-handoff`) produces an **input bundle** for
that chain. It does not implement, replace, or shortcut any of those
skills.

## Boundary Diagram

```text
Legacy Spec Factory                     |   Atlas SDD Chain
                                        |
legacy-ibmi-evidence-intake             |
        |                               |
legacy-ibmi-inventory                   |
        |                               |
legacy-ibmi-program-analyzer            |
        |                               |
legacy-ibmi-flow-analyzer               |
        |                               |
legacy-ibmi-module-analyzer             |
        |                               |
legacy-brd-writer    legacy-spec-writer |
        \                /              |
         \              /               |
   legacy-brd-to-sdd-handoff  <-- this skill, the bridge
                |                       |
                |  06_sdd_handoffs/<CAP>/
                |    sdd-handoff.yaml
                |    atlas-context-pack.json
                |    ...
                v                       v
                                  req-to-user-story
                                        |
                                  user-story-to-spec
                                        |
                                  spec-to-architecture
                                        |
                                  architecture-to-design
                                        |
                                  design-to-tasks → tasks-to-code
```

Everything to the **left** of the boundary is owned by this repo. Everything
to the **right** is Atlas territory.

## What the Handoff Provides

`atlas-context-pack.json` is the agent-facing entry point. It is a
**reshape**, not an expansion, of `sdd-handoff.yaml`.

Atlas consumers can rely on these fields:

| Field | Source in this repo | Notes |
| --- | --- | --- |
| `capability.{id,name,slug,owner}` | spec | unchanged |
| `scope.{in_scope,out_of_scope}` | spec | unchanged |
| `business_rules[]` | spec, `review_status: approved` only | full statement + evidence links |
| `acceptance_criteria[]` | spec, `review_status: approved` only | linked back to `BR-*` |
| `modernization_decisions[]` | spec | only approved `DEC-*` |
| `data_model.entities[]` | spec | legacy→target field mapping |
| `inputs[]`, `outputs[]`, `exceptions[]` | spec | unchanged |
| `test_cases[]` | spec | golden-master flag preserved |
| `evidence_summary` | evidence manifest | IDs + sensitivity status |
| `open_questions[]` | spec | non-blocking `TBD-*` and named-SME-deferred blocking `TBD-*`, verbatim |
| `assumptions[]` | spec / BRD | only assumptions already recorded upstream |

## What the Handoff Does Not Provide

The following are **explicitly out of scope** for this skill and must not
appear anywhere in the handoff package:

- recommended frameworks (Spring Boot, Quarkus, FastAPI, etc.) — unless
  encoded as an approved `DEC-*`
- deployment topology (Kubernetes, ECS, serverless, etc.) — `DEC-*` only
- integration topology (REST vs gRPC, service mesh, queue choice) —
  `DEC-*` only
- API contracts, schemas, OpenAPI fragments — owned by
  `spec-to-architecture` / `architecture-to-design`
- DDL, JPA entities, repository code — owned by
  `architecture-to-design` and `tasks-to-code`
- test code, mocks, fixtures — owned by `tasks-to-code`
- sprint plans, story points, swimlanes — owned by `design-to-tasks`

If the spec is silent on a topic, the handoff is silent. The skill never
fills a gap with a "reasonable default".

## How Atlas Should Consume the Pack

Typical Atlas entry into the chain:

1. `req-to-user-story` reads `atlas-context-pack.json`. Its inputs are the
   approved `BR-*` (each becomes one or more user stories) and the
   `acceptance_criteria[]` (each `AC-*` becomes the story's acceptance
   criterion). Non-blocking `TBD-*` become tagged backlog items.
2. `user-story-to-spec` may consume `data_model`, `inputs`, `outputs`,
   `exceptions` to produce an implementation-facing spec.
3. `spec-to-architecture` decides framework, deployment, integration —
   **the first place those decisions may originate** if not already in
   `DEC-*`.
4. Downstream Atlas skills proceed as usual.

If Atlas needs more legacy context (e.g. a specific evidence excerpt), it
should resolve the `EV-*` ID via the link in `sdd-handoff.yaml.evidence[]`
and read the upstream artifact directly. The handoff intentionally does
not bake raw evidence into the pack.

## Round-Tripping

If Atlas surfaces a question that cannot be answered from the pack, the
correct response is:

1. file a `TBD-*` against the spec (via `legacy-spec-writer` revision), or
2. raise an evidence request against `legacy-ibmi-evidence-intake`

It is **never** correct to silently invent the answer in
`atlas-context-pack.json` or to edit `sdd-handoff.yaml` after the fact.
The handoff is sealed; revisions require a new handoff version with its
own scorecard entry.

## Versioning of the Handoff Itself

The handoff is content-addressed by:

- `capability.slug`
- the approved spec commit (recorded in `source_artifacts.spec.commit`
  when the analysis output repo is under git)
- the handoff ISO date

If the spec is revised, a new handoff must be produced. The previous
handoff stays in place for audit; it is not edited in place.

## Summary

The handoff is a **sealed bundle of facts** that the Atlas chain can act
on. It carries spec content forward unchanged, records gate findings, and
respects the boundary: Atlas decides architecture, design, and code;
Legacy Spec Factory decides what is known and approved about the legacy
behavior.
