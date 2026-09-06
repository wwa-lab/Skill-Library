# View [N]: [View Name] — [Module Name]

## Status: draft | needs_sme_review | approved | approved_with_non_blocking_tbd | blocked_pending_source | blocked_pending_sme | rejected

## Mermaid Flow Diagram

```mermaid
flowchart TD
  VIEW_<SLUG>_001["<View-specific flow node or TBD placeholder>"]
```

Diagram rules:
- Use `flowchart TD` unless the reviewed source flow is explicitly
  left-to-right.
- Place this section before evidence, inventory, or traceability tables.
- View 1 should use business-readable actor, event, manual intervention,
  exception, and rule-seed labels.
- View 2 should show upstream systems, interfaces, the IBM i module boundary,
  downstream systems, and security boundaries.
- View 3 should show flow entry points, entry programs, shared programs, exit
  programs, and external response or batch outcomes.
- View 4 should show data movement across flows and objects, with edge labels
  such as `creates`, `updates`, `reads`, `hands off`, `archives`, or `purges`.
- Use stable node IDs that mirror `ACTOR-*`, `EVENT-*`, `SYS-*`, `IF-*`,
  `FLOW-*`, `PGM-*`, `DATA-*`, `OBJ-*`, `BR-*`, or `TBD-*`, replacing hyphens
  with underscores.
- Do not add diagram nodes or edges unless they are backed by the evidence /
  traceability sections below or by a named `TBD-*`.

## [View-specific sections, per `references/output-contract.md`]

For View 1 (Operation Flow): Business Scope / Actors / Events / BAU Rhythm /
Manual Interventions / Exception Lifecycle / Business Rule Seeds

For View 2 (System Flow): Upstream / Downstream / External Interfaces /
Integration Patterns / Security Boundaries

For View 3 (Program Flow): Flow Inventory / Cross-Flow Dependencies /
Shared Sub-Programs / Overall Call Topology

For View 4 (Data Flow): Data Objects / Lifecycle / Coupling Hotspots /
Critical Data Trails / DB Relationships / Cross-Module Dependencies

## TBDs

### Pending Source
- TBD-[SLUG]-[NNN]: ...

### Pending SME Judgment
- TBD-[SLUG]-[NNN]: ...

### Non-Blocking
- TBD-[SLUG]-[NNN]: ...

## Review Checklist

Before sign-off, the reviewer must verify all items in the per-view checklist for
this view in `references/output-contract.md`:

- For **View 1 (Operation Flow):** Business actors, BAU rhythm, exception procedures, business-rule seeds, and evidence linking
- For **View 2 (System Flow):** Upstream/downstream systems, integration patterns, SLAs, security boundaries, and evidence linking
- For **View 3 (Program Flow):** All flows in scope, cross-flow dependencies, shared sub-programs, call topology, and evidence linking
- For **View 4 (Data Flow):** Data lifecycle, coupling hotspots, cross-module dependencies, DB relationships, and evidence linking

## SME Sign-Off
- **Reviewer:** ____
- **Review Date:** ____
- **Decision:** ____
- **Notes:** ____
