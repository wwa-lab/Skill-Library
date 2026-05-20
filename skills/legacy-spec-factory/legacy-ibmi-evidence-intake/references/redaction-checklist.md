# Redaction Checklist and Patterns

Master checklist for identifying and redacting PII, financial data, credentials,
and other sensitive content in IBM i evidence.

All before/after values in this reference are synthetic examples. Do not place
real raw sensitive values in manifests, redaction logs, review checklists, or
agent-readable prompts.

---

## PII Redaction Patterns

### Customer/Employee Identifiers

| Pattern | Examples | Replacement | Preserve |
|---------|----------|-------------|----------|
| Account numbers (9-digit numeric) | 123456789, 234567890 | 999999001, 999999002 | Numeric type, field length |
| Social Security numbers (XXX-XX-XXXX) | 123-45-6789 | 999-99-9999 | Format, length |
| Employee numbers | EMP001234 | EMP999001 | Type, length |
| Customer names | John Smith | CUST-FAKE-001 | Field position, type |
| Email addresses | john@example.com | cust+fake-001@redacted.com | Format |
| Phone numbers | (555) 123-4567 | (999) 999-9999 | Format, length |

**Stable mapping:** Use consistent replacements within a document. If customer
123456789 appears 50 times, replace with same fake ID all 50 times. Maintain
mapping file (held by redaction owner, not committed).

### Personal Information

- [ ] Names (first, last, full)
- [ ] Birthdates and ages
- [ ] Addresses (street, city, state, ZIP)
- [ ] Phone numbers (landline, mobile, fax)
- [ ] Email addresses
- [ ] Government IDs (SSN, driver license, passport)
- [ ] Medical information or claims
- [ ] Policy numbers or claim numbers

---

## Financial Data Redaction

| Category | Examples | Strategy | Preserve |
|----------|----------|----------|----------|
| Amounts | 10000.00, 5000.50, 0.00 | Change values; keep scale and precision | Numeric type, decimal places, zero/negative |
| Interest rates | 0.15, 0.05, 0.25 | Change values | Numeric(5,2) type, decimal places |
| Credit limits | 100000, 500000 | Change values | Numeric type, field length |
| Account balances | 1234567.89 | Change values | Numeric type, decimal places |
| Commission rates | 0.03, 0.05 | Change values | Type, precision |
| Percentages | 15%, 25%, 100% | Change values | Format, range |

**Calculation preservation:** After redaction, verify that calculations still
work. Example:

```
BEFORE: principal=5000, rate=0.15 → interest=750
AFTER:  principal=5000, rate=0.25 → interest=1250
VALID:  Yes (same structure, calculation valid)
```

### Strategic decisions on amounts

- **Preserve amounts if:** Business logic depends on specific thresholds
  (e.g., "requests > $10,000 require manager approval")
- **Redact amounts if:** Amounts alone identify customers or business patterns
- **If a rule-critical value is changed:** mark the replacement as synthetic,
  preserve type/scale/comparison behavior, and prevent downstream skills from
  treating the replacement as the exact legacy threshold.

---

## Credential and Secret Removal

| Item | Pattern | Action | Notes |
|------|---------|--------|-------|
| API keys | Bearer tokens, JWT | Remove entirely | Do not replace; remove |
| Passwords | `PASSWORD=...` | Remove entirely | Do not replace |
| Hostnames | server.company.com | Remove or replace | May need to preserve for interface docs |
| IP addresses | 192.168.1.1 | Remove entirely | Do not replace |
| Database URLs | jdbc:db2://host:port | Remove entirely | Or mask hostname only |
| SSH keys | (RSA/ED25519) | Remove entirely | Do not replace |
| OAuth tokens | refresh_token, access_token | Remove entirely | Do not replace |
| Hard-coded secrets | API_KEY="abc123" | Remove entirely | Do not replace |

**Rule:** If you see a credential, remove it entirely. Do NOT replace with a
fake credential.

---

## Operational Data (NOT redacted)

Keep these intact; they are not secrets:

- [ ] Program names (CUSTPGM, CUSTMENU, etc.)
- [ ] Library names (CRDSYS, QSYS, etc.)
- [ ] File names (CUSTMAST, CUSTCALL, etc.)
- [ ] Field names (CUSTNO, CREDLIM, etc.)
- [ ] Job names (CRDBATCH, CUSDLY, etc.)
- [ ] Queue names (BATCHQ, PRTQ, etc.)
- [ ] Error messages (FILE LOCKED, RECORD LOCKED, etc.)
- [ ] Error codes (CPF1234, RPG0001, etc.)
- [ ] Timestamps (when jobs ran, completed)
- [ ] Counts and summary statistics (total approved, total denied)
- [ ] Control flow logic (IF branches, PERFORM loops)
- [ ] Validation rules (RANGE, VALUES keywords in DDS)
- [ ] Calculation expressions (IF/THEN/ELSE logic)

---

## Source Code Redaction

### RPGLE Example

```rpgle
// BEFORE (Confidential):
D CUSTNO         S              9P 0
D CREDLIM        S              7P 2
D APPROVALTHRESH S              7P 2 INZ(10000.00)
...
  IF CUSTNO = 123456789
    CREDLIM = 50000.00
  ENDIF
  
  IF CREDLIM > APPROVALTHRESH
    CALL 'APPROVE' PARM CUSTNO CREDLIM
  ELSE
    CALL 'DECLINE'
  ENDIF

// AFTER (Redacted; threshold value is synthetic):
D CUSTNO         S              9P 0
D CREDLIM        S              7P 2
D APPROVALTHRESH S              7P 2 INZ(25000.00) // SYNTHETIC
...
  IF CUSTNO = 999999001
    CREDLIM = 75000.00
  ENDIF
  
  IF CREDLIM > APPROVALTHRESH
    CALL 'APPROVE' PARM CUSTNO CREDLIM
  ELSE
    CALL 'DECLINE'
  ENDIF
```

**Preserved:** Variable types, field lengths, control flow (IF/CALL)
**Redacted:** Account number (stable fake ID), amounts, threshold value
**Semantic note:** Threshold comparison is preserved, but the exact threshold is
synthetic and must not be promoted as a legacy business rule without separate
approved evidence.
**Valid:** ✅ Logic still understandable

---

### CL Example

```cl
// BEFORE (already Internal; no redaction needed):
CALL PGM(CUSTPGM) PARM(&CUSTNO &REQUEST)
MONMSG MSGID(CPF0000) EXEC(DO)
  SEND MSG('Customer lookup failed') TOUSR(QSYSOPR)
ENDDO

// AFTER:
(No changes; CL is operational logic, not sensitive)
```

---

### DDS Example

```dds
// BEFORE (internal; no redaction needed):
     A          R CUSTREC
     A            CUSTNO         9P 0
     A            CUSTNAME      30A
     A            CREDLIM        7P 2

// AFTER:
(No changes; DDS is metadata, not sensitive)
```

---

## Log File Redaction

### Job Log Example

```
// BEFORE:
START CUSTPGM JOB CRDBATCH 2026-05-14 23:45:00
PROCESS ACCT 123456789 REQUEST 1000.00 APPROVED 2026-05-15 00:15:30
PROCESS ACCT 123456790 REQUEST 25000.00 DENIED   2026-05-15 00:16:45
ERROR FILE LOCKED ON CUSTMAST 2026-05-15 00:45:00
RECOVERY SUCCESSFUL 2026-05-15 00:45:15
PROCESS ACCT 123456791 REQUEST 5000.00  APPROVED 2026-05-15 00:47:00
JOB COMPLETED SUCCESSFULLY TOTAL PROCESSED: 100 APPROVED: 85 DENIED: 15

// AFTER:
START CUSTPGM JOB CRDBATCH 2026-05-14 23:45:00
PROCESS ACCT 999999001 REQUEST 1000.00 APPROVED 2026-05-15 00:15:30
PROCESS ACCT 999999002 REQUEST 25000.00 DENIED  2026-05-15 00:16:45
ERROR FILE LOCKED ON CUSTMAST 2026-05-15 00:45:00
RECOVERY SUCCESSFUL 2026-05-15 00:45:15
PROCESS ACCT 999999003 REQUEST 5000.00  APPROVED 2026-05-15 00:47:00
JOB COMPLETED SUCCESSFULLY TOTAL PROCESSED: 100 APPROVED: 85 DENIED: 15
```

**Preserved:** Error codes, timing, decision outcomes, counts
**Redacted:** Account numbers
**Valid:** ✅ Error recovery logic visible

---

## Sample Data Redaction

### CSV Before/After

```csv
// BEFORE:
TRANID,CUSTID,AMOUNT,DECISION,TIMESTAMP
1001,123456789,5000.00,A,2026-05-14T08:30:00Z
1002,123456790,25000.00,D,2026-05-14T08:32:00Z
1003,123456791,100000.00,D,2026-05-14T08:34:00Z

// AFTER:
TRANID,CUSTID,AMOUNT,DECISION,TIMESTAMP
1001,999999001,5000.00,A,2026-05-14T08:30:00Z
1002,999999002,25000.00,D,2026-05-14T08:32:00Z
1003,999999003,100000.00,D,2026-05-14T08:34:00Z
```

**Preserved:** Amount values (needed for threshold analysis), decision codes, timestamps
**Redacted:** Customer IDs
**Valid:** ✅ Sample preserves decision-code structure and amount scale. Do not
infer population approval rates or exact thresholds from synthetic/redacted
sample values without separate approved evidence.

---

## Redaction Tools and Techniques

### Manual Review (Recommended)

1. Open file in text editor
2. Search for PII patterns (regex)
3. Replace matches with stable fake IDs
4. Verify replacements in context
5. Commit redacted file

### Automated Scanning

Use regex patterns to identify likely sensitive content:

```regex
# 9-digit account numbers
\b[0-9]{9}\b

# Amounts (7.2 decimal)
\b[0-9]{1,7}\.[0-9]{2}\b

# Email addresses
[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}

# IP addresses
\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b

# API keys (common patterns)
(api_key|apikey|password|secret|token)=[\w\-\.]+
```

**Warning:** Automated scanning catches patterns but misses context. Always
manually verify before replacing.

---

## Spot-Check Procedure

After redaction, verify:

1. **Syntax validity:**
   - RPGLE: Does it parse?
   - DDS: Are keywords intact?
   - CSV: Can it be imported?

2. **Logic preservation:**
   - Variables types unchanged?
   - IF/THEN/ELSE branches intact?
   - Calculations still valid?

3. **No missed PII:**
   - Re-scan for 9-digit numbers
   - Re-scan for account IDs
   - Re-scan for names
   - Re-scan for emails

4. **Stable mapping:**
   - If same account appears 50 times, same fake ID used all 50 times?

5. **Readability:**
   - Can SME understand the logic after redaction?

---

## Common Redaction Mistakes

| ❌ Mistake | ✅ Correction |
|-----------|--------------|
| Removing all amounts (hides business logic) | Preserve amounts; redact customer IDs |
| Removing error messages (hides recovery logic) | Preserve errors; redact account IDs in messages |
| Inconsistent replacement (same ID replaced differently) | Use stable fake ID mapping |
| Replacing timestamps (hides timing logic) | Preserve timestamps |
| Removing program/file names (hides architecture) | Preserve names; they're not secrets |
| Redacting field lengths (hides data model) | Preserve field types and lengths |
| Replacing field names (hides data flow) | Preserve field names |
| Removing validation rules (hides business logic) | Preserve DDS keywords and RANGE/VALUES |

---

## Redaction Sign-Off

Once redaction is complete:

1. **Redaction owner:** Signs off on completeness
2. **SME reviewer:** Verifies logic preservation and redaction quality
3. **Final manifest:** Lists every item with redaction status

Do NOT use unreviewed redacted evidence in downstream analysis.
