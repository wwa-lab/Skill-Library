# Inventory Review Checklist

## Metadata

- capability: Customer Credit Check
- reviewer:
- review_date:
- decision:
  - [ ] approved
  - [ ] approved_with_non_blocking_tbd
  - [ ] blocked

## Coverage

- [x] all expected RPGLE / COBOL programs are listed
- [x] all expected CLLE programs and submitted jobs are listed
- [x] all PF/LF objects are listed
- [ ] all DSPF objects are listed or ruled out
- [x] all PRTF and report outputs are listed
- [x] spool samples or report examples are available where needed
- [ ] data areas, data queues, and message queues are listed or ruled out
- [ ] external interfaces are listed or ruled out
- [ ] copybooks and shared includes are listed or ruled out

## Evidence

- [x] every object has at least one evidence ID or SME confirmation
- [x] sensitivity is reviewed for every evidence item
- [x] raw production data is not included in committed artifacts
- [x] missing evidence is represented as a TBD

## Downstream Readiness

- [ ] inventory is sufficient for program analysis
- [ ] inventory is sufficient for DDS/schema analysis
- [x] blocking TBDs are identified
- [x] non-blocking TBDs are explicitly marked

## SME Notes

| ID | Note | Blocking |
| --- | --- | --- |
| `TBD-CREDIT-CHECK-001` | Scheduler path needs confirmation before Program Call Map analysis. | pending |
| `TBD-CREDIT-CHECK-002` | Data area usage must be ruled out before business rule mining. | pending |
