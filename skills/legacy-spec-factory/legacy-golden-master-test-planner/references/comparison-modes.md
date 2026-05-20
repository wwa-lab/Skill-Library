<!--
Legacy Spec Factory
Copyright 2026 Leo L Zhang

Original author: Leo L Zhang
License: Apache License 2.0

This skill is part of the Legacy Spec Factory project.
Retain this notice in substantial copies or derived versions.
-->

# Comparison Modes for Golden Master Tests

This document defines the allowed modes for comparing legacy outputs against
new system outputs.

## Mode: Exact

**Use when:** Field values and ordering must match precisely.

**Definition:**
- Every field value must match exactly (character-for-character for text,
  bit-for-bit for numbers).
- Field order must match the legacy output.
- Null / blank distinctions must be preserved.
- Decimal scale and sign must match.

**Example:**
```
Legacy output:
  Amount: 1234.56
  Status: APPROVED
  Timestamp: 2025-05-16T14:30:00Z

New output must have:
  Amount: 1234.56 (not 1234.560, not 1234.5600)
  Status: APPROVED (case-sensitive)
  Timestamp: 2025-05-16T14:30:00Z (exact microsecond match)
```

**When to choose:**
- Financial amounts where rounding rules are critical
- Categorical values (codes, status flags)
- Identifiers that must be exact
- Timestamps where precision is contractual

## Mode: Normalized

**Use when:** Values must match after documented transformations.

**Definition:**
- Define explicit transformation rules that convert legacy values to
  comparable form.
- Both legacy and new outputs are normalized by the same rules.
- The rules must be concrete and deterministic.

**Normalization examples:**
- Date format conversion (legacy: MMDDYY -> normalized: YYYY-MM-DD)
- Identifier mapping (legacy: production ID 98765 -> normalized: FAKE-ID-001)
- Whitespace trimming (legacy: "APPROVED  " -> normalized: "APPROVED")
- Currency symbol stripping ("$1,234.56" -> 1234.56)

**Documenting the rule:**
```yaml
test_case:
  id: TC-CARD-AUTH-005
  comparison:
    mode: normalized
    normalization_rules:
      - field: approval_date
        rule: "Convert MM/DD/YY to YYYY-MM-DD"
        legacy_sample: "05/16/25"
        normalized: "2025-05-16"
      - field: customer_id
        rule: "Map production IDs to stable fake IDs per redaction log"
        legacy_sample: "98765"
        normalized: "FAKE-CUST-001"
```

**When to choose:**
- Redacted identifiers that need stable mapping
- Date/time formats that differ between systems
- Currency symbols or thousands separators
- Whitespace differences that are cosmetic, not behavioral

## Mode: Tolerant

**Use when:** Values are functionally equivalent within a known tolerance.

**Definition:**
- Define an explicit numeric tolerance or time tolerance.
- Both legacy and new outputs are compared within that tolerance.
- The tolerance must be approved by the SME or specified in the acceptance
  criteria.

**Tolerance examples:**
- Rounding: amount differs by +/-$0.01 (due to order-of-operations rounding)
- Time: result arrives within +/-5 seconds (due to network or scheduling variance)
- Percentage: interest rate differs by +/-0.001%

**Documenting the rule:**
```yaml
test_case:
  id: TC-INTEREST-CALC-003
  comparison:
    mode: tolerant
    tolerances:
      - field: interest_amount
        tolerance_type: absolute
        tolerance_value: 0.01
        unit: USD
        reason: "Legacy uses fixed-point BCD; new system uses IEEE double"
      - field: processing_time_ms
        tolerance_type: absolute
        tolerance_value: 5000
        unit: milliseconds
        reason: "SME approved variance due to cloud scheduling"
```

**When to choose:**
- Floating-point calculations (even with same algorithm, minor differences occur)
- Processing times where hardware differences are acceptable
- Rounding differences that are explicitly approved
- Numeric fields where the spec describes acceptable variation

## Mode: Presence

**Use when:** The output must contain or omit specific records/messages.

**Definition:**
- Exact values are not checked.
- Instead, verify that expected records exist or don't exist.
- Useful for list outputs, spool files, batch reports.

**Presence examples:**
- "Output must contain exactly 3 approved transactions"
- "Error log must NOT contain 'USER NOT FOUND'"
- "Report must show 'BATCH COMPLETE' as the final line"

**Documenting the rule:**
```yaml
test_case:
  id: TC-BATCH-CLOSE-002
  comparison:
    mode: presence
    assertions:
      - "Output contains 'BATCH CLOSEOUT REPORT'"
      - "Output contains 'Total records processed: 1500'"
      - "Output does NOT contain 'ERROR'"
      - "Output does NOT contain 'WARNING'"
```

**When to choose:**
- Batch reports where exact field values vary (time-dependent, sequencing)
- Error messages and log outputs
- List outputs where ordering varies but content is consistent
- Side effects that must be present/absent (files created, messages sent)

## Mode: Ordering Insensitive

**Use when:** Output contains the same records but in any order.

**Definition:**
- The set of records must be identical.
- The order in which they appear may differ.
- Useful for database query results, unordered lists.

**Ordering-insensitive examples:**
```
Legacy output:
  Customer 001 | $100
  Customer 003 | $200
  Customer 002 | $150

New output may have:
  Customer 002 | $150
  Customer 001 | $100
  Customer 003 | $200

(Same records, different order -> acceptable)
```

**Documenting the rule:**
```yaml
test_case:
  id: TC-CUSTOMER-LIST-001
  comparison:
    mode: ordering_insensitive
    notes: "Database query results may vary in order; set of customers must be identical"
```

**When to choose:**
- Database query results (legacy sorts by insertion order, new system by index)
- Report line items where ordering is not business-critical
- Set comparisons where membership matters but order doesn't

## Hybrid Approaches

Sometimes a test case combines multiple modes:

```yaml
test_case:
  id: TC-PAYMENT-PROCESS-004
  comparison:
    primary_mode: exact
    exceptions:
      - field: processing_timestamp
        mode: tolerant
        tolerance_value: 5000
        unit: milliseconds
      - field: customer_id
        mode: normalized
        rule: "Map via redaction log"
```

## Explicitly Ignored Fields

Some fields must be excluded from comparison:

```yaml
test_case:
  id: TC-ORDER-001
  comparison:
    mode: exact
    ignored_fields:
      - field: job_number
        reason: "System-assigned; varies between runs"
      - field: record_timestamp
        reason: "Insertion time is non-deterministic"
      - field: internal_sequence_id
        reason: "Implementation detail; not business-relevant"
```

**When to ignore:**
- System-assigned IDs (job numbers, record sequence)
- Insertion timestamps or clock-dependent fields
- Implementation-specific counters
- Fields that are not mentioned in the spec or acceptance criteria

**When NOT to ignore:**
- Business-meaningful fields even if they seem cosmetic
- Fields that trace back to approved `BR-*` or `AC-*`
- Fields that the SME has approved for testing

## Choosing the Right Mode

| Scenario | Mode | Reasoning |
| --- | --- | --- |
| Financial amount exact match | exact | Cents must align |
| Date format differs | normalized | Apply transformation |
| Rounding difference approved | tolerant | Known variance |
| List contains expected messages | presence | Exact wording varies |
| DB query order differs | ordering_insensitive | Membership is contractual |
| Timestamp within 5 seconds | tolerant | Cloud scheduling variance |
| Customer ID redacted | normalized | Map via redaction log |
| Processing time acceptable variance | tolerant | SME approval required |
| Batch report final line check | presence | Exact formatting may vary |

## Default: Prefer Exact

Unless the acceptance criteria, spec, or redacted evidence explicitly allows
otherwise, **default to `exact` comparison**. This keeps the test plan as
strict as possible and makes any divergence visible.

Only relax to `normalized`, `tolerant`, or `presence` when:

1. The legacy behavior itself documents the variance, OR
2. The spec explicitly names the tolerance, OR
3. The SME approves the relaxation in the test-plan review

## SME Validation

Before approving the test plan, the capability-owner SME must validate:

- [ ] Each `TC-*` comparison mode is correct for its scenario
- [ ] Tolerances are accurate (not arbitrary)
- [ ] Ignored fields are truly non-business-critical
- [ ] Normalization rules preserve the intended legacy behavior
- [ ] Presence assertions capture the important checks

The approval record must document:
- SME name and role
- Date (ISO format)
- Approval of each comparison mode
- Any caveats or conditional approvals
