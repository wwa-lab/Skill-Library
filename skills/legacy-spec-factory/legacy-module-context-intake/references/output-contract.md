# Output Contract: Module Context Intake

This reference defines the required files under
`00_context_packages/<MODULE-SLUG>/`.

The context package is an intake artifact. It is not an approved module
analysis, BRD, spec, or modernization decision.

The four Markdown files in this package are context views. They are not the
canonical module-analysis flow files in `04_modules/<MODULE-SLUG>/`; those are
created only by `legacy-ibmi-module-analyzer`.

## Package Layout

```text
00_context_packages/<MODULE-SLUG>/
|-- context-index.yaml
|-- 01-operation-business-flow.md
|-- 02-system-flow.md
|-- 03-program-flow.md
|-- 04-data-flow.md
|-- rag-evidence-map.md
|-- contradiction-log.md
`-- open-questions.md
```

## `context-index.yaml`

Required shape:

```yaml
schema_version: "0.1"
package_type: module_context_intake
module:
  slug: CREDIT-CHECK
  module_id: MODULE-CREDIT-CHECK-001
  business_name: Credit Check
  scope_statement: "SME-confirmed scope statement."
  owner: "Role or named SME"
  source_state: draft | sme_confirmed | approved_with_non_blocking_tbd

intake:
  skill: legacy-module-context-intake
  version: v0.1.4
  generated_at: "YYYY-MM-DDTHH:MM:SSZ"
  status: ready_for_module_analysis
  decision_reason: "Short reason."
  downstream_next_step: legacy-ibmi-module-analyzer

evidence_authorization:
  status: approved | synthetic_non_production | public | blocked | unknown
  evidence_manifest: "evidence/redacted/evidence-manifest.yaml"
  redaction_notes: "Short note."

rag_runs:
  - run_id: RAG-20260521-001
    source_path: "rag_runs/CREDIT-CHECK/RAG-20260521-001/rag-run-index.yaml"
    source_snapshot: "ibmi-export-2026-05-21"
    dictionary_version: "dict-v34"
    arcad_ref_snapshot: "arcad-ref-2026-05-21"
    sensitivity: synthetic_non_production

flow_normalization_input:
  path: "00_context_packages/CREDIT-CHECK/flow-normalization/flow-context-index.yaml"
  status: ready_with_warnings
  quality_level: L1 sparse
  risk_acceptance_status: accepted
  accepted_by: "Credit Operations Owner"

input_files:
  - role: flow_hydration_summary
    path: "rag_runs/.../flow-hydration-summary.md"
    required: true
    status: present

output_files:
  operation_business_flow: 01-operation-business-flow.md
  system_flow: 02-system-flow.md
  program_flow: 03-program-flow.md
  data_flow: 04-data-flow.md
  rag_evidence_map: rag-evidence-map.md
  contradiction_log: contradiction-log.md
  open_questions: open-questions.md

coverage:
  four_views_present: true
  source_snippets_mapped: true
  dictionary_context_mapped: true
  contradictions_carried_forward: true
  open_questions_carried_forward: true
  brd_functional_analysis_hints:
    function_purpose: absent | partial | usable | strong
    business_scenarios: absent | partial | usable | strong
    channels: absent | partial | usable | strong
    user_touchpoints: absent | partial | usable | strong
    system_interfaces: absent | partial | usable | strong
    process_flow: absent | partial | usable | strong
    validation_rules: absent | partial | usable | strong
    error_handling: absent | partial | usable | strong
    dependencies: absent | partial | usable | strong
    optional_security_auth: absent | partial | usable | strong
    optional_workflow_design_notes: absent | partial | usable | strong
    optional_source_document_mapping: absent | partial | usable | strong

gates:
  evidence_authorization_gate: pass | warning | blocked
  module_scope_gate: pass | warning | blocked
  four_view_gate: pass | warning | blocked
  contradiction_visibility_gate: pass | warning | blocked
  rule_promotion_gate: pass | warning | blocked

blocking_items:
  - id: TBD-CREDIT-CHECK-001
    reason: "Missing evidence authorization."
    owner: legacy-ibmi-evidence-intake
```

Rules:

- `status` must be one of:
  - `ready_for_module_analysis`
  - `ready_with_warnings`
  - `blocked_pending_evidence`
  - `blocked_pending_scope`
  - `blocked_pending_contradiction_review`
- `downstream_next_step` is `legacy-ibmi-module-analyzer` unless blocked.
- `blocking_items[]` is empty only when all gates pass or all remaining items
  are explicitly non-blocking.
- Owner-accepted sparse flow-normalization input is allowed only when
  `flow_normalization_input.status: ready_with_warnings`,
  `quality_level: L1 sparse`, and `risk_acceptance_status: accepted`. Preserve
  all missing views as low-confidence `TBD-*`; do not convert sparse context to
  approved facts.
- `coverage.brd_functional_analysis_hints` is advisory. It tells downstream
  module analysis and BRD preparation which normalized context can feed the
  SME-required BRD sections 1-9 and optional sections 10-12. Missing or partial
  hints must stay visible as gaps; this skill must not fill them by inference.

## View Files

The four view files normalize supplied context into the downstream
`legacy-ibmi-module-analyzer` vocabulary. They must stay labeled as intake
context, even when all four are present and SME-confirmed.

Each view file must include:

```markdown
# View N: [Name] - [Module Name]

## Intake Status
- status: draft | sme_confirmed | ready_for_module_analysis | blocked
- source_state: human_confirmed | rag_hydrated | mixed | draft
- primary_sources:
  - [source ID or file path]

## Summary
[Concise supplied context. No invented facts.]

## Evidence-Linked Details
| Claim ID | Knowledge Type | Statement | Evidence | Strength | Review Status |
| --- | --- | --- | --- | --- | --- |

## Candidate Seeds
| Candidate ID | Candidate Statement | Business Signal | Evidence Basis | Required Review |
| --- | --- | --- | --- | --- |

## Gaps For Module Analyzer
| TBD ID | Category | Question | Evidence | Owner | Blocking |
| --- | --- | --- | --- | --- | --- |
```

View-specific guidance:

- **View 1, Operation / Business Flow**: actors, business events, BAU rhythm,
  manual intervention, exception lifecycle, candidate business-rule seeds.
- **View 2, System Flow**: upstream/downstream systems, interfaces, integration
  patterns, synchronous/asynchronous boundaries, security/SLA notes.
- **View 3, Program Flow**: entry programs, call paths, shared programs,
  runtime trigger model, suggested program-analysis focus.
- **View 4, Data Flow**: data objects, field dictionary mappings, lifecycle,
  derivation gaps, data ownership, cross-module dependencies.

Candidate seed rules:

- `Candidate Statement` is the business-language candidate or the analysis
  action whose business meaning must be resolved.
- `Business Signal` explains the business behavior, decision, SLA, exception,
  ownership, or control affected by the candidate.
- `Evidence Basis` carries program names, file names, field names, source
  snippets, runtime observations, dictionary IDs, and RAG IDs.
- For View 3 technical candidates, name the business decision that depends on
  the program-analysis focus; do not make a program name the capability
  boundary.

## `rag-evidence-map.md`

Required sections:

```markdown
# RAG Evidence Map - <MODULE-SLUG>

## RAG Runs
| Run ID | Source Snapshot | Dictionary Version | Sensitivity | Status |

## Source Snippets
| Evidence ID | Artifact | Lines | Summary | Strength | Used In |

## Runtime Observations
| Evidence ID | Source | Lines | Observed Detail | Used In |

## Dictionary Mappings
| Standard Field ID | Legacy Reference | Meaning | Owner | Status | Used In |

## Impact Scope
| Target | Impact Type | Evidence | Confidence | Used In |

## Candidate Facts
| Candidate ID | Statement | Business Signal | Evidence Basis | Promotion Status | Required Review |
| --- | --- | --- | --- | --- | --- |
```

Rules:

- Preserve original RAG IDs. Do not rename `SNP-*`, `RUN-*`, `DD-*`,
  `RAG-CAND-*`, or `RAG-CONFLICT-*`.
- `Candidate Facts` may not use `approved` as `Promotion Status`; use
  `needs_sme_review`, `blocked`, or `deferred`.
- Program names, files, fields, and source snippets belong in `Evidence Basis`.
  The `Statement` and `Business Signal` columns must remain readable without
  knowing the raw object names.
- If a view cites an evidence ID, that ID must appear here.

## `contradiction-log.md`

Required sections:

```markdown
# Contradiction Log - <MODULE-SLUG>

## Summary
- status: none_found | open_contradictions | blocked
- evaluated_checks_present: true | false

## Open Contradictions
| Conflict ID | Type | Summary | Evidence A | Evidence B | Owner | Blocking |

## Evaluated Checks
| Check | Result | Notes |

## Routing
[What must happen before module analysis or BRD writing.]
```

Rules:

- "No contradictions found" is valid only when `Evaluated Checks` is present.
- Blocking contradictions set `context-index.yaml.intake.status` to
  `blocked_pending_contradiction_review`.
- Contradictions are never silently resolved by this skill.

## `open-questions.md`

Required sections:

```markdown
# Open Questions - <MODULE-SLUG>

## Blocking Questions
| TBD ID | Source ID | Question | Owner | Route To | Needed Before |

## Non-Blocking Questions
| TBD ID | Source ID | Question | Owner | Carry Forward To |

## Non-Blocking Assumptions
| Assumption ID | Statement | Evidence | Review Status |

## Recommended Next Prompt
[Prompt for the next skill.]
```

Rules:

- Mint `TBD-*` for unresolved questions that need Legacy Spec Factory tracking.
- Preserve RAG gap IDs as `Source ID`; do not replace them with TBD IDs.
- Use `blocking: yes` only when the next step would invent facts without the
  answer.

## Promotion Rules

Allowed:

- RAG candidates -> `Candidate Seeds` or `Candidate Facts`
- Retrieval gaps -> `TBD-*` open questions
- Contradictions -> `contradiction-log.md`
- Source snippets/runtime observations -> evidence map entries
- Approved dictionary terms -> terminology context

Forbidden:

- RAG candidates -> approved `BR-*`
- Dictionary terms -> source-proven behavior without code/runtime evidence
- One runtime sample -> normal operating frequency
- No contradiction found -> approval
- `ready_with_warnings` -> downstream approval
- Owner-accepted sparse context -> approved facts, approved `BR-*`, or BRD
  claims without later corroboration

## Local Validation

Use the bundled validator for package-level checks:

```bash
python3 skills/legacy-module-context-intake/scripts/validate_context_package.py \
  00_context_packages/<MODULE-SLUG>/
```

It checks required files, status vocabulary, output-file references, view-to
evidence-map linkage, contradiction-log completeness, and RAG candidate
promotion status. It is a structural guard only; SME approval and semantic
review are still required downstream.
