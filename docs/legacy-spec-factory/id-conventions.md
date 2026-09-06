# ID Conventions

Stable IDs are required for traceability across legacy evidence, generated
specifications, SME review, tests, and downstream Java/cloud implementation.

## ID Format

Use uppercase prefixes, a capability slug, and a three-digit sequence:

```text
<PREFIX>-<CAPABILITY-SLUG>-<NNN>
```

Example:

```text
EV-CREDIT-CHECK-001
BR-CREDIT-CHECK-004
AC-CREDIT-CHECK-002
```

## Prefixes

| Prefix | Artifact | Example |
| --- | --- | --- |
| `CAP` | Business capability | `CAP-CREDIT-CHECK-001` |
| `BRD` | Business Requirements Document | `BRD-CREDIT-CHECK-001` |
| `VAL` | BRD-stage validation scenario seed | `VAL-CREDIT-CHECK-001` |
| `SPEC` | Capability specification package | `SPEC-CREDIT-CHECK-001` |
| `PKG` | Governance or traceability package | `PKG-CREDIT-CHECK-001` |
| `OBJ` | Legacy object, file, program, job, screen, or report | `OBJ-CREDIT-CHECK-003` |
| `EV` | Evidence item | `EV-CREDIT-CHECK-012` |
| `DOC` | Source document in a flow-normalization package | `DOC-CREDIT-CHECK-001` |
| `FRAG` | Extracted document fragment in a flow-normalization package | `FRAG-CREDIT-CHECK-001` |
| `BEH` | Observed behavior | `BEH-CREDIT-CHECK-006` |
| `BR` | Business rule | `BR-CREDIT-CHECK-004` |
| `DEC` | Modernization decision | `DEC-CREDIT-CHECK-002` |
| `STEP` | Process step | `STEP-CREDIT-CHECK-001` |
| `REVIEW` | SME review session | `REVIEW-CREDIT-CHECK-001` |
| `FOLLOWUP` | SME review follow-up package | `FOLLOWUP-CREDIT-CHECK-001` |
| `FLOW` | End-to-end business transaction flow | `FLOW-CREDIT-CHECK-001` |
| `NODE` | Program or system node inside a flow | `NODE-CREDIT-CHECK-001` |
| `EDGE` | Call, dispatch, or handoff between flow nodes | `EDGE-CREDIT-CHECK-001` |
| `DATA` | Cross-program or cross-step data exchange | `DATA-CREDIT-CHECK-001` |
| `SEED` | Candidate rule or capability question awaiting SME review | `SEED-CREDIT-CHECK-001` |
| `CAND` | Draft candidate extracted from non-standard source context | `CAND-CREDIT-CHECK-001` |
| `MODULE` | Business module synthesized from related flows | `MODULE-CREDIT-CHECK-001` |
| `VIEW` | Module analysis view | `VIEW-CREDIT-CHECK-001` |
| `ACTOR` | Human or organizational actor in a module view | `ACTOR-CREDIT-CHECK-001` |
| `SYS` | External system, integration partner, or subsystem in a module view | `SYS-CREDIT-CHECK-001` |
| `IN` | Input contract item | `IN-CREDIT-CHECK-001` |
| `OUT` | Output contract item | `OUT-CREDIT-CHECK-001` |
| `EX` | Exception or error behavior | `EX-CREDIT-CHECK-001` |
| `TBD` | Open question or unresolved ambiguity | `TBD-CREDIT-CHECK-005` |
| `AC` | Acceptance criterion | `AC-CREDIT-CHECK-003` |
| `TC` | Test case, including golden master cases | `TC-CREDIT-CHECK-007` |
| `FIND` | Validation or review finding | `FIND-CREDIT-CHECK-001` |

## External / RAG Context Prefixes

The following prefixes may appear in `legacy-module-context-intake` packages
when they come from an external RAG or code-knowledge-graph bundle. Preserve
them as upstream IDs; do not renumber them into Legacy Spec Factory IDs unless
the owning downstream skill explicitly promotes the item.

| Prefix | Artifact | Example |
| --- | --- | --- |
| `RAG` | RAG run, candidate, contradiction, gap, or assumption | `RAG-CAND-CREDIT-CHECK-001` |
| `SNP` | Source snippet from a RAG bundle | `SNP-CREDIT-CHECK-004` |
| `RUN` | Runtime observation from a RAG bundle | `RUN-CREDIT-CHECK-SPOOL-001` |
| `DD` | Enterprise data dictionary term or field | `DD-CREDIT-AVAILABLE-AMOUNT` |

## Capability Slug

The capability slug should be:

- stable across artifacts
- uppercase
- words separated by hyphens
- based on business capability, not program name

Good:

```text
CREDIT-CHECK
ORDER-ENTRY
INVOICE-GENERATION
```

Avoid:

```text
PGM123
TEMP-FIX
RPG-MIGRATION
```

Governance-only steps that run before a capability slug exists may use a
reserved workflow slug, such as `STEP-ROUTING-001`. Once a business capability
is known, use the capability slug instead.

## Scope and Uniqueness

- IDs are unique within a repository.
- Do not renumber existing IDs after review.
- If an item is retired, keep the ID and mark `status: retired`.
- If a rule is split, keep the original ID as retired and create new IDs.
- If two items are merged, preserve the surviving ID and reference the retired
  ID in `supersedes`.

## Cross-Artifact References

Use IDs instead of prose references wherever possible.

Example:

```yaml
business_rules:
  - id: BR-CREDIT-CHECK-004
    evidence:
      - EV-CREDIT-CHECK-012
      - EV-CREDIT-CHECK-013
    acceptance_criteria:
      - AC-CREDIT-CHECK-003
    tests:
      - TC-CREDIT-CHECK-007
```

## Review Status

Every rule, behavior, decision, and TBD should carry one of:

- `draft`
- `needs_sme_review`
- `approved`
- `rejected`
- `retired`
