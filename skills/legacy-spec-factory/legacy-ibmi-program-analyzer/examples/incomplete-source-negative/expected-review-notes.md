# Review Notes: Incomplete Source Handling (Negative Case)

## What This Example Demonstrates

This is a **NEGATIVE CASE** showing how the analyzer should handle **incomplete or partial source code**:

- ❌ **Do NOT:** Invent missing procedure bodies or subroutine definitions
- ❌ **Do NOT:** Guess what external calls are made based on comments alone
- ❌ **Do NOT:** Assume field meanings without DDS definitions
- ✅ **DO:** Create clear TBDs for missing source
- ✅ **DO:** Document what IS visible and mark what is NOT
- ✅ **DO:** Flag the analysis as blocked until source is complete

---

## Problems in This Source

### 1. Incomplete Source Extract
```
COMPUTE-RATE Paragraph:
   **[Comment indicates external call, but CALL statement not shown]
   **Needs CALL 'GET-BASE-RATE' here
```

**What the analyzer SHOULD do:**
```
❌ WRONG:
"COMPUTE-RATE calls GET-BASE-RATE to fetch base interest rate."

✅ RIGHT:
"COMPUTE-RATE paragraph is incomplete in provided source.
Comment indicates external call to GET-BASE-RATE, but CALL statement not visible.
TBD-RATE-COMP-001: Provide complete COMPUTE-RATE paragraph definition."
```

### 2. Missing Paragraph Body
```
LOOKUP-ADJUSTMENT-TABLE.
   **[Paragraph body not provided in source extract]
   **[This paragraph appears to modify WS-COMPUTED-RATE]
```

**What the analyzer SHOULD do:**
```
❌ WRONG:
"Paragraph looks up adjustment table and applies multiplier to base rate."

✅ RIGHT:
"LOOKUP-ADJUSTMENT-TABLE paragraph is declared but body not provided.
Inferred purpose: adjusts WS-COMPUTED-RATE (referenced in COMPUTE-RATE).
TBD-RATE-COMP-002: Provide LOOKUP-ADJUSTMENT-TABLE paragraph definition."
```

### 3. Missing DDS for RATEFILE
```
RATEFILE: File declared with FD and record structure
but DDS definition not provided
```

**What the analyzer SHOULD do:**
```
❌ WRONG:
"RATEFILE stores rates by rate code (4-char) and rate value (3.2 decimal)."

✅ RIGHT:
"RATEFILE record contains RATE-CODE (X(4)) and RATE-VALUE (9(3)V99).
However, file DDS not provided. Cannot confirm:
— Whether RATE-CODE is unique key or can have duplicates
— Whether other fields exist in file
— Whether RATE-VALUE field type matches application usage
TBD-RATE-COMP-003: Provide RATEFILE DDS definition."
```

---

## Correct Analysis Approach

### Step 1: Document What IS Visible

```
Entry Points:
✅ Main entry point (implicit COBOL main)
   — PROCEDURE DIVISION with no parameters
   — No explicit CALL statement from external
   — Accepts WS-INPUT-AMOUNT from user

✅ VALIDATE-AMOUNT paragraph
   — Called by PERFORM
   — Validates input amount
   — Sets WS-STATUS (0=valid, 1=invalid)

✅ COMPUTE-RATE paragraph
   — Called by PERFORM
   — Incomplete: body shows comment but actual call missing

❌ LOOKUP-ADJUSTMENT-TABLE paragraph
   — Called by PERFORM LOOKUP-ADJUSTMENT-TABLE
   — Body not provided (source incomplete)
```

### Step 2: Mark Missing Parts with TBDs

```
TBD-RATE-COMP-001: Complete COMPUTE-RATE paragraph
   Blocking: pending_source
   Question: COMPUTE-RATE includes comment about external call to GET-BASE-RATE,
   but CALL statement not visible in provided source.
   Provide complete paragraph.

TBD-RATE-COMP-002: Provide LOOKUP-ADJUSTMENT-TABLE definition
   Blocking: pending_source
   Question: Paragraph is declared but body not provided. What is adjustment logic?
   
TBD-RATE-COMP-003: Confirm RATEFILE DDS and key field
   Blocking: pending_source
   Question: Record layout inferred from FD (RATE-CODE, RATE-VALUE),
   but file DDS not provided. Confirm field types and whether RATE-CODE is unique key.
```

### Step 3: Set Status to BLOCKED

```
Status: blocked_pending_source

Cannot proceed with downstream analysis until:
— Complete COMPUTE-RATE paragraph provided
— LOOKUP-ADJUSTMENT-TABLE paragraph body provided
— RATEFILE DDS definition provided
```

---

## What NOT to Do (Mistakes to Avoid)

### ❌ Mistake 1: Inventing the Missing CALL
```
WRONG:
"COMPUTE-RATE calls GET-BASE-RATE (RateCode) with implicit error handling."
(Invents entire call contract)

RIGHT:
"TBD-RATE-COMP-001: CALL to GET-BASE-RATE mentioned in comment but statement
not visible. Provide complete COMPUTE-RATE paragraph with full CALL syntax."
```

### ❌ Mistake 2: Guessing Paragraph Logic
```
WRONG:
"LOOKUP-ADJUSTMENT-TABLE likely performs tier-based adjustments,
multiplying base rate by tier factor stored in separate table."
(Invents logic without source evidence)

RIGHT:
"TBD-RATE-COMP-002: LOOKUP-ADJUSTMENT-TABLE paragraph body not provided.
Source comments suggest it modifies WS-COMPUTED-RATE (adjustment logic unknown).
Provide complete paragraph definition."
```

### ❌ Mistake 3: Silent Gaps (No TBD)
```
WRONG:
(Analyze only the visible parts, ignore incomplete sections)

RIGHT:
(Flag every incomplete section with explicit TBD; don't analyze beyond source boundary)
```

### ❌ Mistake 4: Continuing Downstream Analysis
```
WRONG:
"File I/O: RATEFILE uses RATE-CODE as key; confirmed.
Control flow: COMPUTE-RATE → LOOKUP-ADJUSTMENT-TABLE → output result."
(Treats incomplete source as complete)

RIGHT:
"Analysis cannot proceed: source is incomplete.
Status: blocked_pending_source
Required before continuing:
  — TBD-RATE-COMP-001: Complete COMPUTE-RATE
  — TBD-RATE-COMP-002: Complete LOOKUP-ADJUSTMENT-TABLE
  — TBD-RATE-COMP-003: Provide RATEFILE DDS"
```

---

## How This Would Be Documented

### Initial Analysis (Incomplete)
```
# Program Analysis: Rate Computation (OBJ-RATE-COMP-001)

## Status: blocked_pending_source

[Metadata section with what IS known]

## Coverage Notes

Analysis is INCOMPLETE due to missing source. Of the 4 paragraphs referenced:
✅ VALIDATE-AMOUNT — fully visible (defined and body present)
⚠️ COMPUTE-RATE — partially visible (called, but body missing)
❌ LOOKUP-ADJUSTMENT-TABLE — declared but body completely missing
? RATEFILE — declared but DDS not provided

## TBDs Blocking Completion

### Pending Source (Critical)
- TBD-RATE-COMP-001: Provide complete COMPUTE-RATE paragraph
  Blocking: pending_source — Cannot analyze control flow without source
  
- TBD-RATE-COMP-002: Provide LOOKUP-ADJUSTMENT-TABLE paragraph
  Blocking: pending_source — Missing entire paragraph body
  
- TBD-RATE-COMP-003: Provide RATEFILE DDS definition
  Blocking: pending_source — Cannot confirm file structure or key field

## Next Steps

This analysis cannot proceed to downstream skills (spec-writer, modernizer)
until all three pending_source TBDs are resolved by providing complete source.

Once source is complete, analysis must be re-run.
```

### After Source is Provided
```
# Program Analysis: Rate Computation (OBJ-RATE-COMP-001) [REVISED]

## Status: draft

[Complete analysis with full control flow, file I/O, error handling, etc.]

## Previously Blocking TBDs (Now Resolved)
- TBD-RATE-COMP-001 ✅ RESOLVED: COMPUTE-RATE now shows CALL 'GET-BASE-RATE'
- TBD-RATE-COMP-002 ✅ RESOLVED: LOOKUP-ADJUSTMENT-TABLE provides tier adjustment logic
- TBD-RATE-COMP-003 ✅ RESOLVED: RATEFILE DDS confirms RATE-CODE is unique key
```

---

## Summary: Handling Incomplete Source

| Situation | Analyzer Response |
| --- | --- |
| Paragraph called but body missing | Create TBD; don't analyze beyond visible source |
| External call hinted in comment but not shown | Create TBD; don't invent CALL statement |
| File declared but DDS missing | Create TBD; document visible record structure only |
| Unclear logic (inferred vs. explicit) | Tag evidence as `needs_sme_review` or `missing`; create TBD |
| Source extract (partial program) | Mark status as `blocked_pending_source`; list all missing pieces |

**Core principle:** Better to admit a gap than invent a bridge.

