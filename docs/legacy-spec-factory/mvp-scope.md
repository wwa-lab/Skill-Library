# MVP Scope

The MVP must deliver an **end-to-end (e2e) production-ready pilot bundle**
that can be imported into a client's air-gapped IBM i environment and run
against real legacy code without requiring further skill development outside
the air gap.

## Rationale: e2e over narrow slice

Financial-services IBM i shops typically operate behind strict network
isolation. Importing code, skills, and tooling into the air-gapped
environment is a high-cost, infrequent operation. The MVP therefore
optimizes for **maximum coverage in one delivery**, not minimum
exploratory slice.

Every skill the pilot will plausibly need must be in the bundle on day one,
field-pilot ready (9.5 / 10 per `docs/skill-review-gate.md`).

## Pilot Bundle Target

The pilot must deliver:

- one business **module** (multiple business capabilities)
- one reviewed `spec.yaml` / `spec.md` for at least one capability in that module
- module-level 4-view analysis (Operation / System / Program / Data)
- multiple flow analyses (one per business transaction in the module)
- per-program analyses for every program in scope
- one SME approval pass per analysis layer

## Skill Set (Layer 1 + Layer 2)

| # | Skill | Layer | Status | Role |
|---|---|---|---|---|
| 1 | `legacy-ibmi-inventory` | 1 (platform-specific) | ✅ v0.1.0 | Catalogue every legacy object touched by the module |
| 2 | `legacy-ibmi-program-analyzer` | 1 (platform-specific) | ✅ v0.1.0 | Deep-dive one program: Program Call Map, file I/O, object deps, error handling |
| 3 | `legacy-ibmi-flow-analyzer` | 1.5 (platform-specific) | ✅ v0.1.1 | Analyze a call chain (job flow, menu option, subfile dispatch, F-key branch, trigger, scheduler, API) — one business transaction end-to-end |
| 4 | `legacy-ibmi-module-analyzer` | 1.5 (platform-specific) | ✅ v0.1.1 | Synthesize a business module from multiple flows + BAU, producing the **4-view model** (Operation / System / Program / Data). See `docs/module-analysis-model.md`. |
| 5 | `legacy-spec-writer` | 2 (platform-agnostic) | ✅ v0.1.0 | Produce `spec.yaml` + `spec.md` from module + flow + program analyses |

Entry-point router:

| Skill | Status | Role |
|---|---|---|
| `legacy-modernization-orchestrator` | ✅ v0.2.0 | Route the user through the full e2e chain (inventory → program → flow → module → spec) |

## Dependency Order

```
inventory ──► program-analyzer ──► flow-analyzer ──► module-analyzer ──► spec-writer
                                                          │
                                                          └── 4 views:
                                                              1. Operation flow / Business background
                                                              2. System flow
                                                              3. Program flow (aggregates flows)
                                                              4. Data flow
```

Every layer is an aggregation of the one below it. Every layer cross-checks
against `inventory.yaml`; gaps surface as `pending_source` TBDs that route
back to the inventory skill.

## Success Criteria (e2e) — Status

**Implemented (2026-05-14):**

- All five Layer 1 / Layer 2 skills are implemented:
  - `legacy-ibmi-inventory` v0.1.0
  - `legacy-ibmi-program-analyzer` v0.1.0
  - `legacy-ibmi-flow-analyzer` v0.1.1
  - `legacy-ibmi-module-analyzer` v0.1.1
  - `legacy-spec-writer` v0.1.0
- Pre-inventory evidence governance is implemented as
  `legacy-ibmi-evidence-intake` v0.1.0.
- `legacy-modernization-orchestrator` v0.2.0 routes the full chain
  (inventory → program → flow → module → spec).
- Runtime smoke status is mixed:
  - `legacy-step-contract` and `legacy-step-validator` passed Codex CLI,
    Claude Code, and OpenCode smoke tests.
  - `legacy-ibmi-evidence-intake` is synced to all runtimes; smoke execution
    is pending.
  - `legacy-ibmi-flow-analyzer`, `legacy-spec-writer`, and
    `legacy-modernization-orchestrator` have Claude Code pass evidence;
    Codex and OpenCode execution are still pending.
  - `legacy-ibmi-module-analyzer` reached `executed` in all three runtimes,
    but strict positive-pass evidence is still pending.
  - `legacy-ibmi-inventory` and `legacy-ibmi-program-analyzer` remain synced
    only until their smoke tests are run.
- Spec contracts are schema-validated for the root and `legacy-spec-writer`
  templates.
- All skills are repo-ready (9.0+); field-pilot readiness (9.5+) depends on
  completing strict runtime smoke evidence and refreshed scorecards.

**Field-Pilot Bundle:** not yet field-pilot ready. It becomes ready for
air-gapped pilot delivery once all target runtimes pass smoke tests, the module
analyzer strict-pass issue is resolved, and the scorecards agree with the
runtime matrix.

For at least one business module in the pilot library:
  - Inventory is complete and SME-approved
  - Every program in scope has an approved `program-analysis-<OBJ-ID>.md`
  - Every business transaction (flow) has an approved `flow-<FLOW-SLUG>.md`
  - The module has an approved 4-view analysis
  - At least one capability inside the module has an approved `spec.yaml`
  - Every approved business rule has evidence or explicit SME approval
  - Every blocking TBD is explicit
- All deliverables are reproducible offline (no external network calls
  required at pilot time)

## Deferred From MVP

- expanded runtime mining for transaction samples beyond job logs and spool files
- full equivalence test generator (`legacy-equivalence-tester`)
- automated Java / cloud code generation (handed off to `build-agent-skill`)
- complete parser coverage for all IBM i source dialects (RPG II, RPG III,
  fixed-format RPG IV)
- multi-module spec synthesis (each module produces its own `spec.yaml`;
  cross-module synthesis is post-MVP)

## Air-Gap Delivery Notes

The bundle imported into the pilot environment must include:

- canonical `skills/` directory (5 skills + orchestrator)
- all runtime adapter copies (`.codex/`, `.claude/`, `.opencode/`, `.agents/`)
- `docs/` (review gate, model documents, ID conventions, evidence taxonomy,
  runtime smoke-test protocol, **`module-analysis-model.md`**)
- `schemas/spec.schema.yaml`
- `scripts/sync-skills.sh` and `scripts/check-spec-contract.py`
- no external network dependencies; all references resolve to files in this
  repository

The goal is: **one import, full pilot run**.
