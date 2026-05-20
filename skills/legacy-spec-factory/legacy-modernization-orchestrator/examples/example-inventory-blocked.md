# Example Routing: Inventory Blocked → Resolve Before Proceeding

## User Input

> "I ran legacy-ibmi-inventory on the credit-check capability. The inventory
> lists ORDENTR, but it references CRHOLDP (a PRTF) and CRCHKSRV (a service
> program) and we don't have source for either. The inventory.yaml has
> sme_review.decision: blocked. Can I just run the program analyzer next
> anyway? We're under time pressure."

## Orchestrator Output

```
## Workflow Decision

- **Current Stage:** Inventory Blocked (Stage 2b)
- **Desired Outcome:** Run program analyzer next
- **Recommended Next Skill:** `legacy-ibmi-inventory` (resume) (status: Implemented v0.1.0)
- **Why:** The Inventory Completeness Gate fails. Running the analyzer now
  will either produce a hallucinated Program Call Map (analyzer invents what
  CRHOLDP and CRCHKSRV look like) or stop with errors. Neither saves time.

## Routing Notes

- **Stage skip safe?** No. Time pressure does not bypass the gate — see
  Redaction-First and Inventory-Before-Inference rules. The two missing
  artifacts will compound into every downstream artifact.
- **Gate check:** Inventory Completeness Gate — **BLOCKED**. Unresolved
  items:
  - `TBD-CREDIT-CHECK-001` (CRHOLDP PRTF source or approved spool sample
    missing)
  - `TBD-CREDIT-CHECK-002` (CRCHKSRV service program source or interface
    contract missing)
- **Minimum input needed next:** one of:
  1. DDS source for CRHOLDP and source / interface for CRCHKSRV, then re-run
     inventory; or
  2. an SME-signed waiver in `sme_review.notes` marking each TBD as
     non-blocking with explicit rationale.
- **Route confidence:** High — the block is determined by the inventory's
  own structured fields.
- **Next artifact expected:** updated `inventory.yaml` with `decision:
  approved` or `approved_with_non_blocking_tbd`.

## Next Step

- **Invoke:** `legacy-ibmi-inventory` (resume mode) after the source owner
  provides the missing artifacts, OR record an SME waiver.
- **Produce:** updated `inventory.yaml`.
- **Save reminder:** Replace the existing `inventory.yaml` rather than
  branching — keep `OBJ-*` IDs stable.
- **SME reminder:** If pursuing the waiver path, the SME must record (a) why
  the gap does not block, and (b) what compensating evidence will be used
  for the missing artifact (e.g., a spool sample stands in for absent PRTF
  source).
- **Review/export reminder:** Do not export HTML as a workaround. The inventory
  is blocked; resolve source or SME-waiver evidence in Markdown/YAML first.
- **Manual fallback:** Not applicable — this is a gate failure, not a
  missing skill.

## Pressure Note

If the user pushes back on this gate, restate the rule rather than yielding:
running rule mining on guessed call targets is the primary path to
unsafe-to-deploy specs.
```
