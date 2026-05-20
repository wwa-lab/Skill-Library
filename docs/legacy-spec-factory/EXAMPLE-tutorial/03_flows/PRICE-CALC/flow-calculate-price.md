# Flow: Calculate Price for One Order Line

## Metadata

- flow_id: FLOW-PRICE-CALCULATE-LINE
- module_slug: PRICE-CALC
- trigger_model: api_remote   # called by ORDENTR (out-of-scope here)
- review_status: approved
- evidence_ids: [EV-SRC-001, EV-SME-001]
- programs_involved: [OBJ-PRICE-CALC-PRICECALC]

## Trigger Context

The order-entry program ORDENTR (out of scope for this PPCR) calls
PRICECALC once per order line to obtain the final line price. The call is
synchronous, no commit boundary inside PRICECALC.

## Sequence

| Step | Actor | Action | Evidence IDs |
| --- | --- | --- | --- |
| F1 | ORDENTR (out-of-scope) | Calls PRICECALC with item, tier, qty, promo | EV-SRC-001 |
| F2 | PRICECALC | Chains PRICEFL by (ITEMID, TIER); if miss, RC='1' return | EV-SRC-001 |
| F3 | PRICECALC | Computes base × qty, applies tier discount | EV-SRC-001 |
| F4 | PRICECALC | Applies promotion stacking (SUMMR/WINTR=5%, VIP10=10%, else none) | EV-SRC-001, EV-SME-001 |
| F5 | PRICECALC | Rounds to 2dp, returns P_PRICE + RC='0' | EV-SRC-001 |

## Cross-Program Data Flow

```
ORDENTR (call) ──► PRICECALC ──► PRICEFL (read)
                       │
                       └──► returns (PRICE, RC) to ORDENTR
```

## Error Propagation

- Chain miss on PRICEFL → RC='1' returned to ORDENTR. Caller's
  handling is out-of-scope for this PPCR.
- Unknown PROMO code → silent (no error). Documented as intentional.

## Commit Boundaries

None inside PRICECALC. It is a read-only, side-effect-free calculation.

## UI Surfaces

None. PRICECALC has no DSPF / PRTF surfaces.

## Business-Capability Seeds

- `CAP-PRICE-CALCULATION` — calculate final unit price for an order line
  given customer tier and item, applying any active promotion.

## Open Questions

(none — TBD-PRICE-001 was resolved during program analysis)
