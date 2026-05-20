# Spool File Parsing Patterns

This document provides guidance for parsing IBM i printer output (spool files / PRTF output) to extract observations.

---

## Spool File Structure

IBM i printer output (PRTF - printer file) generates fixed-width text reports. These are typically captured as spool files from job output.

**Typical structure**:
```
                            CREDIT AUTHORIZATION REPORT
                            Report Date: 05/15/2026

CUSTOMER DATA                                          CREDIT DECISION
-------- ----   --    -- -------- --- ---- ---- ---  -----------
Cust ID  Name   Type Status Amount   Fee Int Risk Decision Code
======== ===== ==== ===== ========= === ==== ==== ==== ========
00000001 ACME  CLI  ACTV  1,500.00  15  12  LOW  APPR A001
00000002 BETA  VAR  INAC    150.50  02  06  LOW  DENY D002
00000003 GAMMA CLI  ACTV  5,000.00  50  10  HIGH APPR A003

                                          Page Total:    6,650.50
Report Grand Total:    6,650.50
Report Date/Time: 05/15/2026 14:35:22
```

---

## Key Sections to Extract

### 1. Report Header
**Pattern**: Title and metadata at the top

**Markers**:
- Report name or title (usually centered, all caps)
- Report date / generation date
- Page number or header row

**Regex**:
```
^\s+([A-Z ]+REPORT)\s*$
Report Date:\s+(\d{2}/\d{2}/\d{4})
```

**Extract**:
- Report name
- Report date
- Any header labels

**Use for**: report_structure observation; validation of report generation

---

### 2. Column Headers and Field Positions
**Pattern**: Column headers (often separated by spaces) followed by dashes (------)

**Regex**:
```
^([A-Z ]+)$        # Column header line
^(-+\s*)+$         # Dashes separator line
```

**Parsing strategy**:
1. Identify header line (all caps, words separated by spaces)
2. Identify separator line (dashes below each column)
3. Use dashes to determine column positions
4. Extract field names and position ranges

**Example**:
```
Input:
  Cust ID  Name   Type Status Amount   Fee Int Risk Decision Code
  ======== ===== ==== ===== ========= === ==== ==== ==== ========

Extract:
  {
    field_name: "Cust ID",
    column_start: 1,
    column_end: 8,
    data_type: "numeric (ID)"
  },
  {
    field_name: "Name",
    column_start: 10,
    column_end: 14,
    data_type: "alphanumeric"
  },
  ...
```

**Use for**: report_structure observation; field position mapping

---

### 3. Data Rows
**Pattern**: Detail lines containing actual data values

**Parsing**:
- Use column positions from header to extract field values
- Identify data type by value patterns (digits, letters, punctuation)
- Extract ranges and examples

**Example**:
```
Input line:
  00000001 ACME  CLI  ACTV  1,500.00  15  12  LOW  APPR A001

Extract using column positions:
  Cust ID: "00000001" (numeric, range 1–8)
  Name: "ACME" (alpha, 4–5 chars)
  Type: "CLI" (alpha, 3 chars)
  Status: "ACTV" (alpha, 4 chars)
  Amount: "1,500.00" (numeric, 7–9 digits with comma)
  Decision: "APPR" (alpha, 4 chars)
  Code: "A001" (alphanumeric, A + 3 digits)
```

**Use for**: Inferring data types and value ranges; field_value_range observation (Phase 2)

---

### 4. Subtotals and Control Breaks
**Pattern**: Summary lines that appear at section boundaries

**Markers**:
- Line containing word "Total" or "Subtotal"
- Line with only numbers or computed values
- Spacing change or visual separator

**Regex**:
```
^.*(Subtotal|Total|TOTAL).*$
^(\s*[-=]+\s*)+$    # Visual separator line
```

**Example**:
```
Input:
  00000003 GAMMA CLI  ACTV  5,000.00  50  10  HIGH APPR A003
                                          Page Total:    6,650.50
  Report Grand Total:    6,650.50

Extract:
  {
    section_marker: "Page Total",
    total_field: "Amount",
    total_value: 6650.50
  }
```

**Use for**: report_structure observation; control break detection

---

### 5. Footer and Metadata
**Pattern**: Lines at end of report with date/time, page number, or totals

**Markers**:
- "Report Grand Total:"
- "Page XXX of YYY"
- "Date/Time:" or timestamp
- "End of Report"

**Regex**:
```
Report Grand Total:\s+([\d,.]+)
Page\s+(\d+)\s+of\s+(\d+)
Report Date/Time:\s+(.+)$
```

**Extract**:
- Grand total amount
- Total page count
- Report generation date/time
- End marker

**Use for**: Confirming report structure; timing observation

---

## Parsing Strategy

### Column-Position-Based Extraction

1. **Identify the header row** (all caps, field names)
2. **Identify the separator row** (dashes under each field)
3. **Calculate column positions** from separator dashes:
   ```
   Cust ID  Name   Type Status Amount
   ======== ===== ==== ===== =========
   
   Column positions:
   - "Cust ID": 1–8
   - "Name": 10–14
   - "Type": 16–19
   - "Status": 21–25
   - "Amount": 27–35
   ```

4. **Extract values** using these positions from data rows:
   ```
   Data row: "00000001 ACME  CLI  ACTV  1,500.00"
   Value at 1–8: "00000001" = Cust ID
   Value at 10–14: "ACME" = Name
   Value at 27–35: "1,500.00" = Amount
   ```

### Handling Variable-Width Spool Files

Some spool files use spaces instead of fixed columns. Alternative approach:

1. **Split by whitespace**
2. **Use header count to align fields**
3. **Apply type inference** (numeric vs. alpha)

**Example**:
```
Header: "Cust ID Name Type Status Amount Fee"  (6 fields)
Data:   "00000001 ACME CLI ACTV 1500.00 15"
Parse:  ["00000001", "ACME", "CLI", "ACTV", "1500.00", "15"]
```

---

## Common Patterns

### Simple Flat Report

**Pattern**: Header → Dashes → Detail rows → Grand total

```
                            CUSTOMER LIST
                         Generated: 05/15/2026

ID   Name        Type     Status   Amount
==== =========== ======== ======== ===========
0001 Customer A  Regular  Active     1,000.00
0002 Customer B  Premium  Inactive     500.00
0003 Customer C  Regular  Active     2,500.00

Report Total:                            4,000.00
```

**Extraction**:
- Header: "CUSTOMER LIST", Date: 05/15/2026
- Fields: ID (4 chars), Name (12 chars), Type (8 chars), Status (8 chars), Amount (11 chars)
- 3 data rows
- Grand total: 4,000.00

---

### Multi-Section Report (Control Breaks)

**Pattern**: Grouped data with section subtotals

```
CREDIT PROCESSING BY DECISION

APPROVED ACCOUNTS
-----------------
0001 ACME            1,500.00  A001
0003 GAMMA           5,000.00  A003
           Approved Subtotal:   6,500.00

DENIED ACCOUNTS
-----------------
0002 BETA              150.50  D002
           Denied Subtotal:      150.50

Report Grand Total:            6,650.50
```

**Extraction**:
- Two sections: "APPROVED ACCOUNTS" and "DENIED ACCOUNTS"
- Each section has detail rows and subtotal
- Grand total at end

**Output observation**:
```json
{
  "observation_type": "report_structure",
  "sections": [
    {
      "section_name": "APPROVED ACCOUNTS",
      "lines": "4–7",
      "subtotal_line": 8,
      "subtotal_amount": 6500.00
    },
    {
      "section_name": "DENIED ACCOUNTS",
      "lines": "10–12",
      "subtotal_line": 13,
      "subtotal_amount": 150.50
    }
  ],
  "grand_total": 6650.50
}
```

---

### Multi-Page Report

**Pattern**: Page breaks, page headers, page totals

```
[Page 1]
                            CUSTOMER LIST
                            Page 1 of 3

ID   Name        Amount
==== =========== ===========
...
                   Page 1 Total:  10,000.00

[Page 2]
                            CUSTOMER LIST
                            Page 2 of 3
...
```

**Extraction**:
- Identify page breaks (blank lines or "Page X of Y" markers)
- Extract page totals
- Aggregate to report total

---

## Data Type Inference

Based on spool field values, infer data types:

| Pattern | Data Type | Example |
|---------|-----------|---------|
| `\d{4,}` | Numeric ID | "00000001" |
| `\d{1,3}(,\d{3})*\.?\d{0,2}` | Monetary | "1,500.00" |
| `\d+` | Integer | "15", "100" |
| `[A-Z]{2,4}` | Alphanumeric code | "ACME", "CLI", "APPR" |
| `[A-Z ]{4,}` | Text/Name | "Customer Name" |
| `(ACTV\|INAC\|PEND\|...)` | Status enum | "ACTV", "INAC" |

---

## Handling Problematic Spool Files

### Case 1: Misaligned Columns

**Problem**: Columns don't line up; separator line doesn't match header.

**Solution**:
1. Identify actual field boundaries by looking at data rows
2. Recalculate positions based on data
3. Mark confidence as medium (structure inferred, not perfectly clear)

---

### Case 2: Inconsistent Spacing

**Problem**: Some rows have extra spaces; field positions vary.

**Solution**:
1. Use whitespace-based splitting instead of column positions
2. Align by field count from header
3. Mark confidence as medium

---

### Case 3: Truncated or Corrupted Spool

**Problem**: Spool file ends abruptly; some lines are cut off.

**Solution**:
1. Extract what's readable
2. Mark confidence as low
3. Flag incomplete section with TBD

**Example**:
```json
{
  "observation_type": "report_structure",
  "statement": "CREDITRPT has header, detail sections, and footer; structure partially confirmed",
  "confidence": "low",
  "supporting_detail": {
    "note": "Spool file truncated at line 145; footer not observed",
    "lines_parsed": 144,
    "sections_complete": ["header", "detail"],
    "sections_incomplete": ["footer", "grand_total"]
  }
}
```

---

## Value Range Extraction

Across multiple spool files, infer value ranges:

**Single file**:
```
0001 ACME            1,500.00
0002 BETA              150.50
0003 GAMMA           5,000.00

Amount field examples: 150.50, 1500.00, 5000.00
Inferred range: 100.00–9999.99
```

**Multiple files** (Phase 2):
```
File 1: 150–5000
File 2: 100–10000
File 3: 50–25000

Aggregated range: 50.00–25000.00
Confidence: medium (sample covers typical variance)
```

---

## Anti-Hallucination Rules for Spool Files

1. **Never invent columns** — Extract only fields visible in header and data
2. **Never extrapolate beyond observed data** — If max value is 5000, don't claim max is 9999
3. **Never quote unredacted data** — If spool contains customer names, redact or record field count only
4. **Do not infer business rules** — If total is always positive, don't claim "system prevents negatives" without code evidence
5. **Do not assume structure consistency** — If structure varies across files, mark as low confidence

---

## Integration with Inventory

Map extracted fields/files to OBJ-* IDs:

**Example**:
```
Spool file: EV-CREDIT-CHECK-020 (CREDITRPT)
Inventory lookup: OBJ-CREDIT-CHECK-015 (CREDITRPT)

Output: related_object_ids: ["OBJ-CREDIT-CHECK-015"]
```

---

## Tools and Utilities

### Python Snippet for Column Extraction

```python
def extract_columns_from_header(header_line, separator_line):
    columns = []
    col_start = 0
    for i, char in enumerate(separator_line):
        if char == '=' or char == '-':
            if col_start is None:
                col_start = i
        else:
            if col_start is not None:
                col_end = i - 1
                col_name = header_line[col_start:col_end+1].strip()
                columns.append({
                    'name': col_name,
                    'start': col_start,
                    'end': col_end
                })
                col_start = None
    return columns

def extract_values(data_line, columns):
    values = {}
    for col in columns:
        value = data_line[col['start']:col['end']+1].strip()
        values[col['name']] = value
    return values
```

---

## Examples in This Skill

See the `examples/` directory:
- `examples/batch-job-positive/input-spool.txt` — Sample printer output excerpt
- `examples/batch-job-positive/runtime-evidence.jsonl` — Observations extracted from spool
