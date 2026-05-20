# Traceability — CAP-PRICE-CALCULATION

Maps every rule and error condition in [`spec.yaml`](spec.yaml) to the
evidence that supports it and the acceptance test that will verify it.

## Rule → Evidence → Test

| Rule ID | Statement (short) | Evidence | Source artifact rows | Acceptance test |
| --- | --- | --- | --- | --- |
| BR-PRICE-001 | Final price formula | EV-SRC-001 | `program-analysis.md` rows P2–P5 | spec.yaml acceptance row 1–3 |
| BR-PRICE-002 | Promo code stacking | EV-SRC-001, EV-SME-001 | `program-analysis.md` row P4; SME walkthrough | spec.yaml acceptance row 4–7 |
| ERR-PRICE-001 | Item/tier not found | EV-SRC-001 | `program-analysis.md` row P1 + Error Handling table | spec.yaml acceptance row "missing row" |

## Evidence → Rules consumed

| Evidence ID | Type | Consumed by |
| --- | --- | --- |
| EV-SRC-001 | RPGLE source | BR-PRICE-001, BR-PRICE-002, ERR-PRICE-001 |
| EV-DDS-001 | DDS file definition | (informs PRICEFL field types in spec inputs) |
| EV-SME-001 | SME walkthrough notes | BR-PRICE-002 (silent-skip behavior) |

## Flow → Rules invoked

| Flow ID | Rules invoked |
| --- | --- |
| FLOW-PRICE-CALCULATE-LINE | BR-PRICE-001, BR-PRICE-002, ERR-PRICE-001 |

## SME decision log

| Date | Decision | Affected rules | SME |
| --- | --- | --- | --- |
| 2026-05-16 | Confirm BR-PRICE-001 formula matches legacy | BR-PRICE-001 | Jane Doe |
| 2026-05-16 | Confirm silent-skip on unknown promo is intentional | BR-PRICE-002 | Jane Doe |
| 2026-05-16 | Resolve TBD-PRICE-001 (keep silent-skip) | BR-PRICE-002 | Jane Doe |
| 2026-05-16 | Approve spec for forward SDLC handoff | (all) | Jane Doe |

## Coverage check

- Every spec rule is backed by ≥ 1 `evidence_id`. ✓
- Every `inferred_business_rule` would need SME confirmation — there are
  none in this spec (all `confirmed_from_code`). ✓
- Every approved rule has `acceptance_criteria`. ✓
- No open `TBD-*`. ✓
