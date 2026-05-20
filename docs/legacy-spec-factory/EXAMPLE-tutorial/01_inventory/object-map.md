# Object Map — PRICE-CALC module

Human-readable companion to [`inventory.yaml`](inventory.yaml).

## Programs

| OBJ ID | Name | Subtype | Source | Role |
| --- | --- | --- | --- | --- |
| OBJ-PRICE-CALC-PRICECALC | PRICECALC | RPGLE | `PRICECALC.RPGLE` | Calculate unit price given customer tier + item |

## Files

| OBJ ID | Name | Subtype | Source | Role |
| --- | --- | --- | --- | --- |
| OBJ-PRICE-CALC-PRICEFL | PRICEFL | PF | `PRICEFL.PF` | Base price + tier discount table |

## Call Graph (textual)

```
(out-of-scope ORDENTR)
        │
        ▼
   PRICECALC ──► reads PRICEFL keyed by (ITEMID, TIER)
```

## SME Approval

- **Decision:** approved (2026-05-16, Jane Doe)
- **Note:** promotion stacking logic is hard-coded in PRICECALC source.
  No separate promotion table.
