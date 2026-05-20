# Module: [Business Module Name] (MODULE-[SLUG]-001)

## Metadata
- **Module ID:** MODULE-[SLUG]-001
- **Business Name:** [Name]
- **Scope Statement:** [SME-confirmed one paragraph]
- **Module Owner:** [SME name / role]
- **In-scope Flows:**
  - FLOW-[SLUG]-001 ([business event])
  - FLOW-[SLUG]-002 ([business event])
- **Status:** draft | needs_sme_review | approved | approved_with_non_blocking_tbd | blocked_pending_source | blocked_pending_sme | rejected

## View Index
| View | File | Status | Reviewer |
| --- | --- | --- | --- |
| 1. Operation Flow | 01-operation-flow.md | draft | [SME] |
| 2. System Flow | 02-system-flow.md | draft | [SME] |
| 3. Program Flow | 03-program-flow.md | draft | [SME] |
| 4. Data Flow | 04-data-flow.md | draft | [SME] |

## Top Blocking TBDs
(Aggregate of `pending_source` and `pending_sme_judgment` from all views.)

## Capability Seeds For spec-writer
| CAP Seed | Suggested By | SME Question |
| --- | --- | --- |
| CAP-[SLUG]-001 | [view + reason] | [question] |

## Module Review Checklist
- [ ] All four views are at least `approved_with_non_blocking_tbd`
- [ ] Cross-view consistency check passed
- [ ] No blocking TBDs remain
- [ ] Capability seeds reviewed
- [ ] Module ready for spec-writer

## Sign-Off
- **Module Owner:** ____
- **Date:** ____
- **Decision:** ____
