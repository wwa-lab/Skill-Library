# Runtime Evidence Analysis Guide

This document provides guidance on analyzing runtime evidence for screens and reports: screenshots, spool files, job logs, and sample transactions.

## Evidence Types & Collection

### 1. Screen Screenshots / Terminal Captures

**What it is:** Image or text capture of a DSPF interactive screen during operation.

**How to collect:**
- Use terminal screenshot tools (e.g., `WRKOBJ`, `DSPF` field-by-field navigation)
- Capture different modes if present (edit mode, add mode, browse mode)
- Capture error states (invalid input, error message display)
- Capture both initial load state and state after user input

**What to look for during analysis:**
- Field layout and positioning (confirm against DDS positions)
- Field data types and edit formatting (does numeric show with commas?)
- Error message display location and format
- Subfile layout (rows visible, selection indicator position)
- Function key labels and their behavior
- Read-only vs. editable field visual distinction

**Redaction requirements:**
- Mask or remove customer names, account numbers, SSNs
- Mask transaction amounts if sensitive
- Mask internal control numbers or reference IDs if needed
- Keep field structure and formatting intact so layout analysis is possible

**Evidence tag:**
```
EV-<SLUG>-NNN: Screenshot of <screen name> in edit mode, DSPF layout confirmed, 
evidence_strength: observed_in_runtime
```

### 2. Spool Files / Report Samples

**What it is:** Printed output of a PRTF report, typically captured from a job's spool file.

**How to collect:**
- Run the report with representative data
- Capture the full report (all pages)
- Capture edge cases (empty result set, maximum size, control breaks on all values)
- Preserve formatting (spaces, dashes, alignment)

**What to look for during analysis:**
- Page layout (headers, footers, blank space)
- Detail record formatting (field positions, edit codes, decimal places)
- Control breaks and subtotals (when do they print? what values are summed?)
- Page breaks (where does overflow occur? are pages complete?)
- Apparent total reconciliation (does the visible grand total reconcile to
  visible subtotals in this sample? are count-like fields explained?)
- Special formatting (underlines, asterisks, leading zeros)

**Redaction requirements:**
- Mask customer PII (names, addresses, phone numbers)
- Mask account numbers and financial data if sensitive
- Mask transaction dates or amounts if needed
- Keep structure, field positions, and totals intact for analysis
- Example: "123-45-6789" → "XXX-XX-6789"; "$1,234.56" → "$XXXX.XX"

**Evidence tag:**
```
EV-<SLUG>-NNN: Spool sample of <report name> for month=Jan showing 10 detail records
with 2 department subtotals and 1 grand total, evidence_strength: observed_in_runtime
```

### 3. Job Logs

**What it is:** Execution log of a job that shows program flow, error messages, and state changes.

**How to collect:**
- Run a transaction or report that uses the screen/report
- Capture the job log from the job queue or job history
- Include the complete log from start to end

**What to look for:**
- Which programs are called (CALL statements)
- Which screens are displayed (EXFMT to DSPF)
- Which reports are generated (OVRPRTF, CALL to print program)
- Error messages and their indicators
- Message waits (USER program paused at user input)
- Submitted jobs or batch operations triggered

**Redaction requirements:**
- Mask job parameters that contain sensitive data
- Mask file override paths if they contain account numbers
- Mask any embedded SQL or data values
- Keep program names, flow sequence, and error messages

**Evidence tag:**
```
EV-<SLUG>-NNN: Job log for ORDER-ENTRY transaction showing EXFMT to ORDERSCR,
field validation, function key F2 (CANCEL) behavior, evidence_strength: observed_in_runtime
```

### 4. Sample Transactions / Data

**What it is:** Representative input/output data samples showing what a screen accepts or a report produces.

**How to collect:**
- Save input transactions before processing
- Save output records after processing
- Collect edge cases (minimum value, maximum value, empty, special codes)

**What to look for:**
- Field data types and ranges in actual use
- Special codes or control values (status codes, type flags)
- Decimal places and numeric formatting in practice
- String length and character usage
- Null or missing value handling

**Redaction requirements:**
- Extensive redaction typically required for transaction samples
- Consider storing in a separate secure location or using synthetic/anonymized data
- Provide only count/summary data if full details are sensitive

**Evidence tag:**
```
EV-<SLUG>-NNN: Sample of 100 ORDER records showing typical AMOUNT range 
(min=$10.00, max=$9999.99), STATUS codes (A/C/H), evidence_strength: observed_in_runtime
```

## Analysis Workflow

### Step 1: Collect Runtime Evidence

Before analysis, gather evidence:

```markdown
**Evidence Bundle for <Object>**

- DDS Source: EV-001 (DSPF or PRTF member)
- Screenshot 1 (normal state): EV-002
- Screenshot 2 (error state): EV-003
- Spool sample (page 1): EV-004
- Spool sample (page 2): EV-005
- Job log: EV-006
- Sample transaction batch: EV-007

All evidence redacted per data-collection-and-redaction.md
```

### Step 2: Cross-Reference DDS to Runtime

For each section of the DDS:

1. Locate it in the runtime evidence
2. Confirm field names, types, positions match
3. Note formatting differences (edit code results)
4. Mark any discrepancies as TBD

**Example:**

```
DDS: A CUSTNAME 30A POSITION(5 10)
Spool: "Smith, John     " appears at row 5, col 10–40

✓ MATCH: Name present, 30-character field, correct position
```

```
DDS: A AMOUNT 9S 2 EDTCDE(A)
Spool: "1,234,567.89" appears at row 5, col 50

✓ MATCH: Numeric, comma edit code applied correctly
```

```
PRTF DDS / program evidence: SUBAMT appears on a subtotal record format
Spool: "1,234.56" appears on subtotal line, then "2,543.21" on next subtotal

PARTIAL MATCH: spool confirms subtotal-like output. Program/O-spec or SME
evidence is still required before claiming the accumulation formula.
```

### Step 3: Document Observed Behaviors

Behaviors visible in runtime evidence that are not explicit in DDS become `BEH-*`:

```yaml
BEH-ORDER-001: "Screenshot sequence shows 10 rows before and after page-down"
Evidence: EV-004 (screen capture sequence showing paging)
Confidence: high
Observed in runtime

SEED-ORDER-001: "Which DDS keyword and program logic control page-down reload?"
Related: BEH-ORDER-001
Resolution: Check program EXFMT logic for indicator usage
```

### Step 4: Reconcile DDS with Runtime

Create a reconciliation table:

| DDS Element | Expected Behavior | Observed in Runtime | Match | Notes |
|-------------|------------------|------------------|-------|-------|
| SFLPAG(10) | 10 records per page | 10 records visible on screen | ✓ | |
| CA01 (F1) | Exit to ACCEPT | Pressing F1 returns to menu | ✓ | |
| Subtotal label / CUSTSUBTL format | Subtotal-like line may indicate a customer break | Subtotal appears every 5-7 records | ? | Pattern unclear; needs program or SME evidence |
| FORCEOFM(01) | Page break on indicator | Page break does not appear in sample | ✗ | No indicator #01 set in job log, needs test case |

Mark mismatches as TBD with resolution path.

### Step 5: Infer Questions Not Answered by Evidence

If the evidence does not fully explain a behavior, create a SEED or TBD:

```markdown
SEED-REPORT-001: "Report subtotals are labeled 'Department Total' but the DDS 
does not define this text string. Is it hard-coded in the program or does 
the system auto-generate it?"

Related Evidence:
- EV-005: Spool sample showing "Department Total:" text
- DDS (EV-001) has no EDIT keyword for the subtotal line

Resolution Owner: Program analyzer
```

## Common Runtime-to-DDS Mismatches

### Mismatch: Screen Field Not Visible in Runtime

**Possible causes:**
- Field is INVISIBLE(NN) and the indicator is on
- Field is below the fold (PAGESIZE limits visibility)
- Field is in a different record format not displayed in that screenshot

**Resolution:**
- Mark as TBD pending: additional screenshots in different modes, program analysis to confirm indicator usage

### Mismatch: Spool Shows Different Totals Than Expected

**Possible causes:**
- Control break field filters data (not all departments appear)
- Calculation is not simple summation (weighted average, percent of total)
- Multiple runs shown in same spool (totals reset between sections)

**Resolution:**
- Mark as TBD pending: SME clarification on calculation logic, access to complete dataset

### Mismatch: Subfile Pagination Behavior Differs from DDS

**Possible causes:**
- Program logic overrides DDS pagination (explicit SFLCLR, reload)
- DDS subfile keyword presence does not explain the whole runtime behavior
  without program load/clear logic
- Screenshot captures only one state; full behavior spans multiple pages

**Resolution:**
- Mark as TBD pending: program analysis to understand exact pagination logic, additional screenshots showing full navigation

## Confidence Levels for Runtime Evidence

Assign confidence to observations based on:

| Confidence | Criteria | Example |
|-----------|----------|---------|
| High | Behavior consistently observed across multiple samples; matches DDS definition | "SFLPAG(10) consistently shows 10 records per page in all screenshots" |
| Medium | Behavior observed but not validated with DDS; single sample; matches pattern | "Subfile pages down when F10 pressed; matches expected PAGEDOWN behavior" |
| Low | Behavior inferred from single instance; contradicts DDS or is ambiguous | "Report subtotal logic appears to use department field, but no CONTROL keyword visible in DDS sample" |

## Redaction Review Protocol

Before committing runtime evidence to analysis:

1. **PII Check:** Does the evidence contain names, addresses, SSNs, passport numbers? → Redact
2. **Financial Check:** Does the evidence contain transaction amounts, account balances, pricing? → Consider redaction or use synthetic ranges
3. **Internal Data Check:** Does the evidence contain control numbers, API keys, internal IDs? → Redact if sensitive
4. **Structure Preservation:** Is the field layout, data type, and formatting still visible after redaction? → Required for analysis
5. **Approval:** Has a data steward or security officer reviewed the redacted evidence? → Document approval in metadata

**Metadata to record:**
```yaml
Evidence ID: EV-NNN
Original Source: (e.g., "Production spool file from 2026-05-10 job")
Redaction Date: 2026-05-11
Redaction Method: (e.g., "Customer PII masked with XXX, amounts replaced with ranges")
Approval: (e.g., "Data Security team, Lucy Brown, 2026-05-11")
Sensitivity Assessment: "redacted" or "safe"
```

## Tips for Runtime Analysis

1. **Collect diverse scenarios:** One screenshot is not enough. Get normal case, error case, edge case (empty, full, special code).

2. **Preserve formatting:** When exporting spool to text, ensure tab stops and spacing are preserved. Use monospace fonts for spool samples.

3. **Date runtime evidence:** Always record the date/time the evidence was collected. Systems evolve; old runtime samples may not match current DDS.

4. **Link back to DDS:** Never analyze runtime in isolation. Always cross-check against source DDS to confirm what is defined vs. what is implemented.

5. **Use evidence IDs:** Consistently tag each runtime sample with an EV-* ID. Use the same ID when referring to it in analysis.

6. **Mark ambiguities:** If runtime evidence is ambiguous (behavior unclear, formatting not matching DDS), do NOT guess. Create a TBD with the specific question.

7. **Separate observation from inference:** 
   - Observation: "The spool shows 'Department Total: 12345' on line 15"
   - Inference: "The program calculates department totals" (needs confirmation)

## Reference Sections

When creating a screen/report analysis, reference this guide:

- **Layout Summary:** Use screenshots to verify positioning and visual structure
- **Fields and Indicators:** Use spool samples to confirm actual field display and edit code application
- **Program Touchpoints:** Use job logs to trace EXFMT/WRITE calls and indicator state
- **Observed Behaviors:** Use spool samples and screenshots for runtime state snapshots
- **Subfile Behavior:** Use screenshots of pagination and selection behavior
- **Report Structure:** Use spool samples to identify headers, control breaks, totals
- **TBD Ledger:** Use runtime evidence gaps to identify required follow-up analysis
