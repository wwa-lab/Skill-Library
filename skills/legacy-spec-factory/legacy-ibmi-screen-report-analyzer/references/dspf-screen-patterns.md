# DSPF Screen Patterns Reference

This document lists common DSPF (display file DDS) patterns and keywords to help identify behavior during screen analysis.

## Record Formats and Field Roles

Display files define record formats and fields. Do not infer "input screen" or
"output screen" from one leading character alone; field usage, DDS keywords,
conditioning indicators, and program EXFMT/WRITE/READ behavior determine the
role.

Use these role labels in the analysis:

| Role | Meaning | Evidence to cite |
|------|---------|------------------|
| `input` | User can enter or return a value | Field usage in DDS plus EXFMT/READ evidence |
| `output` | Value is displayed but not returned as user input | DDS usage, PROTECT/DSPATR context, WRITE evidence |
| `both` | Program displays a value and accepts a returned value | DDS plus EXFMT evidence |
| `hidden` | Field is present but conditionally invisible or non-display | DDS keyword and indicator context |
| `constant/message` | Literal text or message surface | DDS literal / MSGID / ERRMSG evidence |

## Field Type Keywords

| Type | Meaning | Example |
|------|---------|---------|
| `A` | Alphanumeric (character) | `A A CUSTNAME 30` |
| `N` | Numeric (unsigned) | `A N AMOUNT 7` |
| `P` | Packed decimal | `A P PRICE 7 2` |
| `S` | Signed numeric (zoned) | `A S QUANTITY 5` |
| `D` | Date field | `A D ORDERDATE 8Y/M/D` |
| `T` | Time field | `A T CLOCKTIME 6T` |
| `H` | Hexadecimal | `A H HEXVALUE 10` |

## Indicator Keywords

### Display Control

| Keyword | Purpose | Example |
|---------|---------|---------|
| `PROTECT` | Make field non-enterable | `PROTECT(02)` — field protected if indicator #02 is on |
| `EDTCDE` | Apply edit code for display/input | `EDTCDE(A)` — comma edit code (thousands separator) |
| `INVISIBLE` | Hide field from display | `INVISIBLE(01)` — field hidden if indicator #01 is on |
| `OVERLAY` | Display at specific row/column, overlay previous field | `OVERLAY` — field prints on top of previous field position |

### Error Handling

| Keyword | Purpose | Example |
|---------|---------|---------|
| `ERRMSG` | Display error message if indicator is on | `ERRMSG(error-text 00)` — shows error-text if indicator #00 is on |
| `ERRSFL` | Display error in subfile instead of message line | `ERRSFL(subrec-name 00)` — error shown in subfile if #00 is on |

### Validation & Constraints

| Keyword | Purpose | Example |
|---------|---------|---------|
| `MINVAL` | Minimum numeric value | `MINVAL(0)` — must be >= 0 |
| `MAXVAL` | Maximum numeric value | `MAXVAL(999999)` — must be <= 999999 |
| `RANGE` | Value must be in list | `RANGE(1 2 3 4 5)` — must be one of these values |
| `VALUES` | List of valid values (synonym for RANGE) | `VALUES(YES NO)` |
| `COMP` | Comparison operator for conditional display | `COMP(EQ value)` — compare to a specific value |

### Field Behavior

| Keyword | Purpose | Example |
|---------|---------|---------|
| `MANDATORY` | Field must be entered | `MANDATORY` — user cannot skip this field |
| `OPTIONAL` | Field may be blank | `OPTIONAL` — user can leave this field empty |
| `AUTOFMT` | Automatic formatting (spacing, punctuation) | `AUTOFMT` — field auto-fills with formatting |
| `DSPATR` | Display attribute (highlight, blink, reverse video) | `DSPATR(HI)` — highlight the field; `DSPATR(BL)` — blink; `DSPATR(RI)` — reverse image |

## Function Key & Command Key Keywords

### Function Key Definition

```
A CA01(ACCEPT)
A CA02(CANCEL)
A CF05(REFRESH)
A CF06(DELETE)
```

| Keyword | Meaning | Example |
|---------|---------|---------|
| `CA` | Command Attention key (causes screen to exit and return control to program) | `CA01(label)` — F1 causes exit |
| `CF` | Command Function key (submitted with screen data) | `CF05(label)` — F5 submitted with data |
| `PAGEUP` | Page-up key behavior in subfile | `PAGEUP(03)` — page up if indicator #03 is on |
| `PAGEDOWN` | Page-down key behavior in subfile | `PAGEDOWN(04)` — page down if indicator #04 is on |

**Important:** The label in parentheses (for example `ACCEPT`) is a DDS label
or response aid, not proof of the business action. Map a key to a save,
delete, cancel, or navigation action only when program analysis, job logs, or
SME notes confirm it.

## Subfile Keywords

### Subfile Definition

| Keyword | Purpose | Example |
|---------|---------|---------|
| `SFLCTL` | Subfile control record format (the container) | `A R SUBCTL SFL` — defines the subfile container |
| `SFLPAG` | Records per page | `SFLPAG(10)` — shows 10 records per screen |
| `SFLSIZ` | Total subfile size (maximum records) | `SFLSIZ(100)` — subfile can hold up to 100 records |
| `SFL` | Marks record format as subfile detail format | `A R SUBDETAIL SFL` — detail record for subfile |
| `SFLDROP` / `SFLFOLD` | Controls folded/dropped presentation of subfile records | Document keyword presence; runtime navigation requires program/runtime evidence |
| `SFLDLTPG` | Subfile page-delete behavior | Document keyword presence; do not infer reload timing without program/runtime evidence |
| `SFLCLR` | Indicator to clear subfile | `SFLCLR(99)` — clear subfile if indicator #99 is on |
| `SFLRCDNBR` | Subfile relative record number | `SFLRCDNBR(rrnfield)` — field holding current record number |

### Subfile Record Selection

Subfile records typically have a selection field (user marks records for action):

```
A R SUBDETAIL SFL
A  1 SEL        1A I (selection field, indicator #1)
A    CUSTNO     5A O
A    FNAME     30A O
```

The input field lets the user mark records. The program decides how to
interpret that value; do not treat the field or an indicator as delete/edit
logic without program evidence.

## Indicator Usage Patterns

### Conditional Display by Indicator

```
A 01 FLDNAME 10A (field displays only if indicator #01 is on)
A  1 FLDNAME 10A (field displays only if indicator #1 is on — same, short form)
```

### Common Indicator Assignments

| Indicator | Common Use |
|-----------|-----------|
| #00 | General error indicator |
| #01–#09 | Field-level error or validation indicators |
| #10-#19 | Often used for screen/form mode indicators in some shops |
| #20-#29 | Often used for subfile control indicators in some shops |
| #30-#39 | Often used for conditional field display in some shops |
| #40-#49 | Often used for key state indicators in some shops |
| #50-#99 | Application-specific in many systems |

These ranges are shop conventions, not IBM i rules. Treat them as hints only.

## Record Format Positioning

Fields within a record format are positioned using ROW and COL keywords:

```
A          ROW(05) COL(10) CUSTNAME 30A (displays at row 5, column 10)
A          ROW(06) COL(10) CUSTADDR 50A (displays at row 6, column 10)
```

Default positioning flows top-to-bottom, left-to-right if ROW/COL is omitted.

## Common Screen Patterns

### Simple Input Form

```
A R ENTRYFORM
A          DSPATR(HI)
A            ENTER ' Order Entry Screen'
A 01       ERRMSG('Invalid input' 01)
A          MSGLOC(24 1)
A
A            CUSTNO     5A I
A  CUSTNO < 0           01
A            ORDDATE    8A I DATFMT(*ISO)
A            ORDERAMT   9S 2 I MINVAL(0) MAXVAL(999999.99)
A
A            ENTER CA01(ACCEPT)
A            ENTER CA02(CANCEL)
```

### Subfile Browse Screen

```
A R BRSCTRL SFL(R BRSDETAIL)
A                         SFLCTL(BRSCTL)
A                         SFLPAG(10)
A                         SFLSIZ(100)
A                         SFLDROP(05)
A
A R BRSDETAIL SFL
A   1 SEL        1A I
A    CUSTNO     5A O
A    CUSTNAME  30A O
A    CUSTCITY  20A O
```

### Modal Popup with Error Message

```
A R MSGBOX
A                         WINDOW(10 40)
A                         WDWBORDERS(*SINGLE)
A                         OVERLAY
A
A            MSG1       78A O +2 +2
A
A            CA01(OK)
A            CA02(CANCEL)
```

## Edit Code Reference

Edit codes control how numeric fields are displayed:

| Code | Format | Example | Notes |
|------|--------|---------|-------|
| `A` | Floating $ with commas | 1,234,567.89 | Right-aligned, blank if zero |
| `B` | Floating $ with commas | 1,234,567.89 | Suppresses zero and -0 |
| `C` | Comma separator | 1,234,567.89 | Suppresses sign |
| `D` | European format (. thousands, , decimal) | 1.234.567,89 | |
| `E` | Zero suppression | 00001234.56 becomes 1234.56 | |
| `F` | Zero suppression with $ | $1234.56 | |
| `G` | Asterisk fill | ****1234.56 | For check amounts |
| `H` | Blank fill | (spaces for leading zeros) | |
| `I` | No decimal separator | 123456789 | |
| `J` | + or - sign | +1234.56 or -1234.56 | |
| `K` | CR/DB notation | 1234.56DB | Debit/Credit |
| `L` | Parentheses for negative | (1234.56) | Negative in parentheses |
| `M` | Minus sign for negative | -1234.56 | |
| `N` | No editing | 1234.56 | Raw value |
| `O` | European edit | 1.234,56 | With $ |
| `P` | Percent format | 12.34% | |
| `Q` | Japanese format | | |
| `R` | User-defined (via EDTMSK) | | Requires EDTMSK keyword |
| `Z` | Suppress leading zeros | 1234.56 | Without commas |

## Common Anti-Patterns to Watch For

1. **Relying on indicator number to infer logic:** Always check DDS keyword usage. Indicator #01 might mean error, protection, or visibility depending on keyword.

2. **Assuming field is mandatory without MANDATORY keyword:** Check if field is in an input record and verify it's not marked OPTIONAL.

3. **Confusing SFLPAG with actual data:** SFLPAG(10) means 10 records per page, not that the report always prints exactly 10 records.

4. **Missing subfile clear logic:** SFLCLR(99) means the program sets indicator #99 to clear the subfile. Without seeing the program, you cannot confirm when clearing happens.

5. **Over-inferring field semantics from labels:** A field named "AMT" is numeric, but its business meaning (price, discount, tax, total) requires SME confirmation.

## Tips for Analysis

- **Start with record formats:** Identify which records are input, output, or both.
- **Map indicators to keywords:** List every indicator used in the DDS and its keyword context.
- **Trace function keys:** Document DDS labels first; map business action only from program or SME evidence.
- **Identify validation:** Collect all MINVAL, MAXVAL, RANGE, MANDATORY constraints.
- **Check subfiles:** If present, document SFLPAG, SFLSIZ, SFLDROP/SFLFOLD, SFLDLTPG, SFLCLR, and selection fields exactly as evidenced.
- **Cross-reference programs:** Link back to programs that EXFMT this file to understand flow.
- **Separate observations from inference:** Mark field business purpose as `SEED-*` if not explicit in DDS.

## References

- IBM i DDS Keywords: IBM i Information Center, "DDS Language Concepts"
- DSPF (Display File) Definition: IBM i Knowledge Center, "Display File Reference"
- Edit Codes: IBM i Knowledge Center, "Edit Codes and Edit Masks"
