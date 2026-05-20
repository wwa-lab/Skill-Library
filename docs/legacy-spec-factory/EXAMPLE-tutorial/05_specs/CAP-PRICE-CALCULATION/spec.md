# Spec — CAP-PRICE-CALCULATION

> Calculate Final Unit Price for One Order Line
> **Status:** approved (8c)  ·  **Version:** 1.0.0  ·  **Module:** PRICE-CALC

Human-readable companion to [`spec.yaml`](spec.yaml). The YAML is the
authoritative contract; this file explains it in prose.

## What this capability does

Given an item, customer tier, quantity, and optional promo code, return
the final unit price for one order line. Read-only — no side effects, no
database writes.

## Inputs

| Name | Type | Required | Notes |
| --- | --- | --- | --- |
| `item_id` | string(10) | yes | Item code; must exist in PRICEFL |
| `tier` | string(1) | yes | Customer tier A / B / C / D |
| `quantity` | integer | yes | Must be ≥ 1 |
| `promo_code` | string(5) | no | Optional; unknown values silently ignored |

## Outputs

| Name | Type | Notes |
| --- | --- | --- |
| `final_price` | decimal(13,2) | Rounded to 2dp (half-up, NOT banker's rounding) |
| `status_code` | string(1) | `'0'` success, `'1'` item+tier not found |

## Rules

### BR-PRICE-001 — Final price formula

```
final_price = round(
  base_price × qty × (1 - tier_discount/100) × (1 - promo_discount/100),
  2dp
)
```

Source: PRICEFL row for `(item_id, tier)` provides `BASEPRC` (base_price)
and `DISCPCT` (tier_discount). Promo discount comes from BR-PRICE-002.

### BR-PRICE-002 — Promo code stacking

| `promo_code` value | Promo discount |
| --- | --- |
| `SUMMR` | 5% |
| `WINTR` | 5% |
| `VIP10` | 10% |
| anything else (including null / empty / typo) | 0% (silent — no error) |

**Important:** the silent-skip on unknown promo codes is intentional. The
modernized implementation MUST preserve this behavior (operators
occasionally fat-finger codes; they should get the un-discounted price
rather than a hard error).

## Error conditions

### ERR-PRICE-001 — Item / tier not found

If `(item_id, tier)` is not found in `PRICEFL`, return `status_code='1'`
and `final_price=0`. Do NOT raise an exception.

## Acceptance test sketch

| Case | Inputs | Expected |
| --- | --- | --- |
| baseline | item=A123, tier=B, qty=10, promo='', PRICEFL: BASE=10.00 DISC=5.00 | price=95.00, status='0' |
| summer promo | same + promo='SUMMR' | price=90.25, status='0' |
| VIP10 promo | same + promo='VIP10' | price=85.50, status='0' |
| typo'd promo | same + promo='ABCDE' | price=95.00, status='0' (silent skip) |
| missing row | item=ZZZ, tier=B | price=0.00, status='1' |

## Traceability

See [`traceability.md`](traceability.md) for rule → evidence → test
mapping.

## SME sign-off

Approved 2026-05-16 by Jane Doe. SME notes recorded in `spec.yaml`.
