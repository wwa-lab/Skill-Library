# Data Collection and Redaction

Legacy Spec Factory may process source code, DB metadata, job logs, spool files,
screen samples, and transaction samples. These artifacts can contain customer,
financial, employee, operational, and regulated data. Evidence must be
collected and redacted before it is used by agents outside the approved
environment.

## Collection Preconditions

Before collecting evidence, confirm:

- authorized IBM i access for the target libraries and objects
- approval to export source members, DDS, job logs, spool files, and sample data
- agreed retention period for exported evidence
- redaction owner and review process
- approved storage location for raw and redacted evidence

## Common IBM i Evidence Sources

| Evidence | Typical Collection Path |
| --- | --- |
| Source members | source physical files such as `QRPGLESRC`, `QCLLESRC`, `QDDSSRC` |
| Object inventory | library/object listings and DSPFD/DSPPGM-style metadata |
| DB2 metadata | catalog views, DSPFFD-style field descriptions |
| Job logs | job log export from relevant batch or interactive jobs |
| Spool files | spool listing plus copied spool output |
| Printer files | DDS PRTF source plus representative spool output |
| Display files | DSPF source plus screen flow notes or screenshots when permitted |
| Runtime samples | approved, redacted sample transactions and expected outputs |

Exact commands vary by shop policy. Do not embed production extraction commands
in a skill unless they have been approved by the client environment owner.

## Redaction Policy

Raw evidence should not be committed to this repository.

Before evidence enters an agent workflow:

- replace customer, employee, vendor, account, card, tax, claim, and policy
  identifiers with stable fake IDs
- mask financial amounts unless exact arithmetic is required for a test case
- replace names, addresses, emails, and phone numbers
- remove credentials, hostnames, IPs, tokens, and operational secrets
- preserve field shape, lengths, signs, decimal scale, and edge-case values
- record what was redacted in an evidence note

## Evidence Storage

Recommended split:

```text
evidence/raw/        # restricted, never committed
evidence/redacted/   # approved for agent processing
evidence/index/      # metadata and evidence ledger
```

Use `.gitignore` rules to keep raw evidence out of version control.

## Review Gate

If evidence sensitivity is `unknown`, the item must be treated as sensitive and
blocked from downstream agent use until reviewed.

