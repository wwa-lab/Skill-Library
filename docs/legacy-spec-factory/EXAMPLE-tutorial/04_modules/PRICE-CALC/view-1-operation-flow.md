# View 1: Operation Flow — PRICE-CALC

User / operator perspective on the price-calculation operation. Drives BR
seed extraction.

## Actor

The Order Entry operator (using ORDENTR — out of scope) implicitly
invokes price calculation as they enter or modify an order line. The
operator does not see PRICECALC directly; they see the final price on
the ORDENTR screen.

## Operation Sequence (user view)

1. Operator types item code, quantity, and (optionally) a promo code on
   the ORDENTR order-line screen.
2. ORDENTR looks up the customer's tier from the customer master.
3. ORDENTR calls PRICECALC with (item, tier, qty, promo).
4. PRICECALC returns the final line price.
5. ORDENTR displays the price; operator presses Enter to commit the line.

## Business Rules Observed

### BR-PRICE-001 — Price formula

```
final_price = round(
  base_price × qty × (1 - tier_discount/100) × (1 - promo_discount/100),
  2dp
)
```

- **Evidence:** EV-SRC-001 (PRICECALC steps P2–P5)
- **Knowledge type:** confirmed_from_code
- **Review status:** approved

### BR-PRICE-002 — Promo code stacking

| Promo code | Promo discount |
| --- | --- |
| `SUMMR` | 5% |
| `WINTR` | 5% |
| `VIP10` | 10% |
| anything else | 0% (silent skip — no error) |

- **Evidence:** EV-SRC-001 (P4), EV-SME-001 (silent-skip is intentional)
- **Knowledge type:** confirmed_from_code
- **Review status:** approved
- **Note:** SME confirmed the silent-skip behavior matches BAU — operators
  occasionally fat-finger a promo code and should get the un-discounted
  price rather than a hard error.

## Open Questions

(none — all TBDs resolved)
