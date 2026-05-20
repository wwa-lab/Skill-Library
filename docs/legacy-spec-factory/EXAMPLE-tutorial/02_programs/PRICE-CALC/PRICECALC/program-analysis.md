# Program Analysis: PRICECALC

## Metadata

- program_id: OBJ-PRICE-CALC-PRICECALC
- source_member: PRICECALC.RPGLE
- inventory_source: 01_inventory/inventory.yaml
- review_status: approved
- evidence_ids: [EV-SRC-001, EV-SME-001]

## Entry Points And Parameters

| Entry Point | Parameters | Evidence IDs | Notes |
| --- | --- | --- | --- |
| PRICECALC | `IN P_ITEMID CHAR(10)`, `IN P_TIER CHAR(1)`, `IN P_QTY PACKED(9,0)`, `IN P_PROMO CHAR(5)`, `OUT P_PRICE PACKED(13,2)`, `OUT P_RC CHAR(1)` | EV-SRC-001 | Single entry point; called by ORDENTR |

## Control Flow

| Step ID | Description | Evidence IDs | Confidence |
| --- | --- | --- | --- |
| P1 | Chain PRICEFL by (ITEMID, TIER) — if not found, set RC='1' and return | EV-SRC-001 | confirmed_from_code |
| P2 | If found, compute `LINE_BASE = BASEPRC × QTY` | EV-SRC-001 | confirmed_from_code |
| P3 | Apply tier discount: `LINE_AFTER_TIER = LINE_BASE × (1 - DISCPCT/100)` | EV-SRC-001 | confirmed_from_code |
| P4 | If PROMO ∈ {'SUMMR', 'WINTR'}, apply additional 5% off; if PROMO = 'VIP10', apply 10%; else no promo | EV-SRC-001, EV-SME-001 | confirmed_from_code (promo code list confirmed by SME) |
| P5 | Round to 2 decimal places, set P_PRICE and RC='0' | EV-SRC-001 | confirmed_from_code |

## File I/O

| File | Operation | Key Fields | Evidence IDs | Notes |
| --- | --- | --- | --- | --- |
| PRICEFL | CHAIN (read) | ITEMID, TIER | EV-SRC-001 | Read-only |

## External Calls

| Target | Call Type | Inputs | Outputs | Evidence IDs | TBD |
| --- | --- | --- | --- | --- | --- |
| (none) | — | — | — | — | — |

## Error Handling

| Condition | Legacy Behavior | Evidence IDs | Review Status |
| --- | --- | --- | --- |
| PRICEFL chain miss | Return RC='1', P_PRICE=0 | EV-SRC-001 | approved |
| Unknown PROMO code | Treated as no promotion (silent) | EV-SRC-001, EV-SME-001 | approved (SME confirmed silent behavior is intentional) |

## Open Questions

| TBD ID | Question | Blocking | Owner | Resolution |
| --- | --- | --- | --- | --- |
| TBD-PRICE-001 | Should an unknown PROMO code raise a hard error instead of silent skip? | no | Jane Doe | RESOLVED 2026-05-16: keep silent — matches BAU and is intentional defensive behavior |
