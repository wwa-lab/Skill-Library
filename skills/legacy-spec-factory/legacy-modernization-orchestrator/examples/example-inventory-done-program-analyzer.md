# Example Routing: Inventory Done -> Program Analyzer

## User Input

> "The inventory for CREDIT-CHECK is SME-approved. `inventory.yaml` has
> `sme_review.decision: approved`, `object-map.md` is complete, and the main
> program is ORDENTR. I want to understand ORDENTR's logic next. Which skill
> should I use?"

## Orchestrator Output

```markdown
## Workflow Decision

- **Current Stage:** Inventory Done (Stage 2c)
- **Desired Outcome:** Program Analysis
- **Recommended Next Skill:** `legacy-ibmi-program-analyzer` (status: Implemented v0.1.0)
- **Why:** Inventory has passed the completeness gate, so the next safest
  step is program-level analysis for ORDENTR. The implemented analyzer
  produces the source-backed behavior, file I/O, call, and error-handling
  record consumed by flow analysis.

## Routing Notes

- **Stage skip safe?** No. Jumping directly to business rules would skip the
  source-backed behavior analysis needed to separate observed behavior from
  inferred business rules.
- **Gate check:** Inventory Completeness Gate — pass, based on
  `sme_review.decision: approved` and no unresolved blocking coverage gaps.
- **Minimum input needed next:** ORDENTR source member, referenced copybooks or
  service-program interfaces, file list from `inventory.yaml`, linked evidence
  IDs, and SME owner for ambiguous branches.
- **Route confidence:** High.
- **Next artifact expected:**
  `02_programs/CREDIT-CHECK/ORDENTR/program-analysis.md`.

## Next Step

- **Invoke:** `legacy-ibmi-program-analyzer`
- **Produce:** `program-analysis-ORDENTR.md` with entry points, parameters,
  control flow, file I/O, external calls, error handling, evidence IDs, and
  `TBD-*` IDs for unclear behavior.
- **Save reminder:** Save the analysis under
  `02_programs/CREDIT-CHECK/ORDENTR/`; it will be consumed later by
  `legacy-ibmi-flow-analyzer`.
- **SME reminder:** Ask the SME to validate any branch affecting money,
  inventory, compliance, customer status, or posting before treating it as a
  confirmed rule.
- **Review/export reminder:** Not applicable yet. Program analysis should stay
  in canonical Markdown; consider `legacy-html-exporter` later only if SMEs
  need browser-friendly review of stable Markdown.
- **Manual fallback:** Not needed — `legacy-ibmi-program-analyzer` is
  implemented. Use fallback only if the runtime cannot load the skill and the
  user explicitly accepts a manual workaround.
```

## Expected Manual Artifact Skeleton

```markdown
# Program Analysis: ORDENTR

## Metadata

- program_id: OBJ-CREDIT-CHECK-ORDENTR
- source_member:
- inventory_source: 01_inventory/inventory.yaml
- review_status: draft

## Entry Points And Parameters

| Entry Point | Parameters | Evidence IDs | Notes |
| --- | --- | --- | --- |

## Control Flow

| Step ID | Description | Evidence IDs | Confidence |
| --- | --- | --- | --- |

## File I/O

| File | Operation | Key Fields | Evidence IDs | Notes |
| --- | --- | --- | --- | --- |

## External Calls

| Target | Call Type | Inputs | Outputs | Evidence IDs | TBD |
| --- | --- | --- | --- | --- | --- |

## Error Handling

| Condition | Legacy Behavior | Evidence IDs | Review Status |
| --- | --- | --- | --- |

## Open Questions

| TBD ID | Question | Blocking | Owner |
| --- | --- | --- | --- |
```
