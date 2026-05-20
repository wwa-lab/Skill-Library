# Object Map: Customer Credit Check

## Capability

- ID: `CAP-CREDIT-CHECK-001`
- Name: Customer Credit Check
- Source system: REDACTED-IBM-I
- Library: REDLIB

## Objects

| Object ID | Name | Type | Evidence | Review |
| --- | --- | --- | --- | --- |
| `OBJ-CREDIT-CHECK-001` | ORDENTR | program | `EV-CREDIT-CHECK-001` | needs SME review |
| `OBJ-CREDIT-CHECK-002` | ORDSUBMIT | program | `EV-CREDIT-CHECK-002` | needs SME review |
| `OBJ-CREDIT-CHECK-003` | CUSTPF | pf | `EV-CREDIT-CHECK-003` | needs SME review |
| `OBJ-CREDIT-CHECK-004` | CRHOLDP | prtf | `EV-CREDIT-CHECK-004`, `EV-CREDIT-CHECK-005` | needs SME review |

## Relationships

| From | Relationship | To | Confidence |
| --- | --- | --- | --- |
| `OBJ-CREDIT-CHECK-001` | reads | `OBJ-CREDIT-CHECK-003` | high |
| `OBJ-CREDIT-CHECK-002` | depends_on | `OBJ-CREDIT-CHECK-001` | medium |
| `OBJ-CREDIT-CHECK-001` | uses_printer_file | `OBJ-CREDIT-CHECK-004` | high |

## Open Questions

| ID | Question | Blocking |
| --- | --- | --- |
| `TBD-CREDIT-CHECK-001` | Confirm whether the nightly scheduler invokes ORDSUBMIT directly or through another wrapper. | pending SME judgment |
| `TBD-CREDIT-CHECK-002` | Does any data area override the credit check threshold during month-end processing? | pending SME judgment |

