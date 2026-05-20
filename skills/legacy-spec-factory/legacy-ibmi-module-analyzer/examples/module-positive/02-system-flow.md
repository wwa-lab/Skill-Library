# View 2: System Flow — Card Authorization

## Status: draft → needs_sme_review

## Upstream Systems
| System ID | Name | Type | Integration Pattern | Flow(s) | Evidence |
| --- | --- | --- | --- | --- | --- |
| SYS-CARD-AUTH-01 | Visa | External card network | MQ inbound (mTLS, ISO 8583) | FLOW-ONUS-AUTH-001 | David Park 2026-05-12 + FLOW-ONUS-AUTH Trigger Context |
| SYS-CARD-AUTH-02 | Mastercard | External card network | MQ inbound (mTLS, ISO 8583) | FLOW-ONUS-AUTH-001 | David Park |
| SYS-CARD-AUTH-03 | CSR Workstation (5250 emulator) | Internal | 5250 over TLS | FLOW-MANUAL-AUTH-001 | SME |
| SYS-CARD-AUTH-04 | IBM i Job Scheduler | Internal (WRKJOBSCDE) | Scheduler trigger | FLOW-NIGHTLY-RECON-001 | scheduler entry |

## Downstream Systems
| System ID | Name | Type | Integration Pattern | Flow(s) | Evidence |
| --- | --- | --- | --- | --- | --- |
| SYS-CARD-AUTH-10 | GL System (Oracle-based, off-platform) | External | File handoff via GLPOSTPF + nightly SFTP | FLOW-NIGHTLY-RECON-001 | David Park + downstream system contract |
| SYS-CARD-AUTH-11 | Risk Monitoring | Internal | DTAQ async (RECONDTAQ) | FLOW-NIGHTLY-RECON-001 | FLOW-NIGHTLY-RECON DATA-06 |
| SYS-CARD-AUTH-12 | Compliance Reporting | Internal/manual | Spool review (RECONPRT) | FLOW-NIGHTLY-RECON-001 | View 1 Exception Lifecycle |

## External Interfaces
| Interface ID | Counterparty | Direction | Format | SLA | Auth | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| IF-CARD-AUTH-01 | Visa | Bidirectional | ISO 8583 over MQ | sub-second (P95 < 800ms) | mTLS + HMAC | Integration spec v2.3 (David Park) |
| IF-CARD-AUTH-02 | Mastercard | Bidirectional | ISO 8583 over MQ | sub-second | mTLS + HMAC | Integration spec v1.8 |
| IF-CARD-AUTH-03 | GL System | Outbound | Fixed-width file + SFTP | daily by 06:00 | SSH key | Internal SFTP config |

## Integration Patterns Summary
| Pattern | Used By | Async Boundary | Notes |
| --- | --- | --- | --- |
| MQ inbound (mTLS) | Visa, Mastercard | Yes | retries by card network |
| File handoff + SFTP | GL System | No (sync batch) | cut-off 06:00 |
| DTAQ async | Risk Monitoring | Yes | non-blocking notification |
| Spool review | Finance Analyst (manual) | No | morning routine |

## Security & Network Boundaries
- Visa/Mastercard MQ inbound terminates at the IBM i partition DMZ.
- TLS terminates at MQ; payloads validated by HMAC at NODE-01 of FLOW-ONUS-AUTH.
- GL SFTP outbound goes through corporate egress firewall; SSH key rotated quarterly.
- 5250 sessions from CSR workstations encrypted via TLS to LPAR.

## TBDs
### Pending Source
- TBD-CARD-AUTH-SYS-001 — Confirm GL system schema contract; agreement is in another team's repo

### Pending SME Judgment
- (none for this view)

### Non-Blocking
- TBD-CARD-AUTH-SYS-002 — Document SFTP key rotation procedure

## SME Sign-Off
- **Reviewer:** David Park (Integration Architect) — pending
- **Decision:** draft → needs_sme_review
