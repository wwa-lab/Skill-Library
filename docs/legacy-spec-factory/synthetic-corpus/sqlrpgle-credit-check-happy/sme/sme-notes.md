# SME Notes

Reviewer: Mei Chen  
Role: Credit Operations SME  
Review Date: 2026-05-20

## Confirmed Business Meaning

- `STATUS = 'A'` means the customer account is active and eligible for credit
  evaluation.
- If the customer is inactive, the request must be denied even if a historical
  credit limit exists.
- If the request exceeds available credit, the legacy system denies the request
  but still returns the maximum approvable amount for agent reference.
- The CLLE wrapper is operational glue only; it is not the source of the
  business rule.

## Open Questions For Later Expansion

- In month-end operations, some shops may temporarily override available credit
  using a control table or data area. This fixture intentionally omits that
  pattern.
- A later batch-oriented fixture should show whether denied requests are queued
  for supervisor review or simply rejected inline.
