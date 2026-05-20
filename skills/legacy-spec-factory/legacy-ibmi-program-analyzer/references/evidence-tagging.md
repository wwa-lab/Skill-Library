# Evidence Tagging: How to Tag Behaviors with Evidence Strength

This guide explains how to assign evidence strength labels to each claim in the program analysis, ensuring every behavior is backed by source evidence or explicitly flagged as needing SME judgment.

## Core Principle

**Every non-trivial behavior must carry evidence**, even if the evidence is weak. Do not document "likely" behavior or "probably happens" without explicitly tagging the evidence strength and the source.

---

## Evidence Strength Levels

### 1. confirmed_from_code

**Definition:** The source code directly shows this behavior. It is visible and unambiguous in:
- Procedure specifications (RPGLE `BEGPR / ENDPR`, parameter declarations)
- F-specs (file specifications, access methods)
- I/O statements (SETLL, READE, CHAIN, WRITE, UPDATE, DELETE)
- CALL statements or copybook bindings
- MONITOR blocks or exception handlers
- Explicit IF/SELECT conditions
- **Source-level flow-header comments** (common IBM i convention: ASCII tree at top of program documenting the subroutine call hierarchy). When present, this is first-class evidence for the Program Call Map — but always cross-check against actual EXSR/CALL/PERFORM statements; a stale header creates a TBD, not a fact.

**Examples:**

```rpgle
D Main            PR
D   CustID                  9P 0 const
D   Amount                  7P 2 const

**  This entry point is confirmed_from_code
**  — procedure spec shows entry point name, parameter types, and const direction.
```

```rpgle
/free
   CHAIN CustID CREDFILE;
   if not %found(CREDFILE);
     // Error handling
   endif;
/end-free

**  File I/O is confirmed_from_code:
**  — CHAIN on CREDFILE with key CUSTID (visible)
**  — Error check with %found() indicator (visible)
```

```rpgle
CALL 'GETRATE' (RateCode RATE);

**  External call is confirmed_from_code:
**  — program name 'GETRATE' (visible)
**  — parameters: RateCode (in), RATE (out) (visible in call statement)
```

**How to tag:**
- Reference the source line numbers or file location
- Quote the source statement if brief
- Use `confirmed_from_code` in the evidence strength column

**When to use this:**
- Always for procedure specifications, F-specs, and I/O statements
- Always for visible CALL statements or copybook bindings
- Always for explicit error handling (MONITOR, EVAL indicators)

---

### 2. medium_confidence

**Definition:** Inferred from usage patterns or implicit language semantics, but not explicitly declared in source. The behavior is strongly suggested by code logic, but requires careful reading to confirm.

**Examples:**

```rpgle
if CustID = *zero;
   // ... error handling
else
   CHAIN CustID CREDFILE;
endif;

**  The implication is: "CustID must be non-zero before CHAIN."
**  The behavior is inferred from the if/else logic, not from explicit validation rule.
**  Evidence strength: medium_confidence
**  — Source shows conditional, but validation rule is implicit.
```

```rpgle
C   Amount         CMPD      Limit
C                  IF        Amount > Limit
C                  EVAL      RC = 0
C                  ELSE
C                  EVAL      RC = 1
C                  ENDIF

**  COBOL-style (CMPD = compare decimal):
**  The implication is: "Return 1 if Amount ≤ Limit, 0 if Amount > Limit."
**  The behavior is inferred from the comparison and EVAL assignment, but
**  the rule is implicit (no explicit "limit exceeded" comment).
**  Evidence strength: medium_confidence
```

**How to tag:**
- Explain the inference (e.g., "inferred from conditional logic")
- Note what the code shows vs. what you infer
- Flag with `medium_confidence` in evidence strength column
- Consider creating a TBD if the inference is critical to understanding

**When to use this:**
- When behavior is strongly suggested by code logic but not explicitly stated
- When field names or control structures hint at purpose but are not documented
- When error paths are implied by indicator logic or conditional branches

---

### 3. strongly_inferred

**Definition:** Multiple evidence points converge on the same conclusion, making the behavior highly likely even without explicit documentation. Typically used when:
- An external call is always preceded by specific validation
- An error code is always returned after a specific operation
- A field is only assigned in one code path
- Call sites show a consistent pattern

**Examples:**

```rpgle
// In VALIDATECREDIT subroutine:
CHAIN CustID CREDFILE;
if not %found(CREDFILE);
   EVAL RC = -1;
   return;
endif;

CHAIN (COUNTRY, CATEGORY) LIMITTBL;
if not %found(LIMITTBL);
   EVAL RC = -1;
   return;
endif;

// ... perform validation logic ...

EVAL RC = 1;
return;

**  Inference: "Both CREDFILE and LIMITTBL must be found before returning success."
**  Multiple evidence points:
**  — Both CHAIN operations followed by %found() check
**  — Return path shows RC = 1 only after both checks pass
**  — Return path shows RC = -1 for both cases of not found
**  Evidence strength: strongly_inferred
**  — Pattern is consistent and repeats, making the behavior highly likely.
```

```rpgle
if %eof(CUSTFILE);
   EVAL done = *on;
endif;

// Later...
if %eof(CUSTFILE);
   EVAL RESULT = 'NO_RECORDS';
endif;

**  Inference: "EOF indicator controls loop termination and final result."
**  Multiple evidence points:
**  — %eof() check drives done flag
**  — Same check drives result assignment
**  — Pattern repeats across multiple code paths
**  Evidence strength: strongly_inferred
```

**How to tag:**
- List the evidence points that converge
- Explain why the pattern makes the conclusion likely
- Note if alternative interpretations exist
- Flag with `strongly_inferred` in evidence strength column

**When to use this:**
- When a pattern repeats consistently across multiple code paths
- When call-site behavior shows a uniform requirement
- When field assignments are restricted to specific contexts

---

### 4. needs_sme_review

**Definition:** Evidence is present, but interpretation is ambiguous or context-dependent. Multiple valid explanations exist, and SME judgment is required to determine the intended behavior.

**Examples:**

```rpgle
CALL 'CHECKEXPOSE' (Amount CustID RC);

**  Evidence present: Source shows CALL statement.
**  Interpretation ambiguous:
**  — What does RC = 'A' mean? (Approved? Active? Allowed?)
**  — What does RC = 'D' mean? (Denied? Default? Downgraded?)
**  — Are there other return values?
**  — Is the call always made, or conditional?
**  Evidence strength: needs_sme_review
**  — Visible in source, but undocumented behavior.
```

```rpgle
// In procedure, undocumented:
EVAL SomeField = COMPUTE_VALUE(Input);

**  Evidence present: Source shows external call to COMPUTE_VALUE.
**  Interpretation ambiguous:
**  — What does COMPUTE_VALUE return? (A business calculation? A lookup? A status code?)
**  — What happens if COMPUTE_VALUE fails?
**  — Is COMPUTE_VALUE always available, or conditional?
**  Evidence strength: needs_sme_review
**  — Visible call, but no documentation of intent or error handling.
```

**How to tag:**
- Describe what the source shows
- Describe the ambiguity (multiple possible meanings)
- Explain why SME judgment is needed
- Create a TBD if the behavior is critical to understanding
- Flag with `needs_sme_review` in evidence strength column

**When to use this:**
- When external programs are called but their purpose/parameters are undocumented
- When error codes are used but their meanings are unclear
- When procedures are called but their context/timing requirements are not obvious
- When field assignments appear but their business purpose is not documented

---

### 5. missing (Use sparingly — Usually Creates a TBD)

**Definition:** Evidence required to confirm a behavior is not available. The behavior cannot be documented or confirmed from source alone. Creates a TBD instead of guessing.

**Examples:**

```rpgle
**  File reference in F-spec:
F CUSTFILE    IF   A        K        DISK

**  Evidence missing:
**  — DDS for CUSTFILE is not in inventory
**  — Field names and types are unknown
**  — Access methods are assumed but not confirmed
**  Action: Create TBD-CREDIT-CHECK-NNN: "Provide CUSTFILE DDS definition"
**  Evidence strength: missing
```

```rpgle
CALL 'EXTERNAL_PROCESS' (Input Output);

**  Evidence missing:
**  — EXTERNAL_PROCESS documentation not provided
**  — Parameters not documented (are they input/output/both?)
**  — Return values not documented
**  Action: Create TBD-CREDIT-CHECK-NNN: "Document EXTERNAL_PROCESS signature and error codes"
**  Evidence strength: missing
```

**How to tag:**
- Describe what evidence is missing
- Explain why the missing evidence is needed
- Create a TBD with blocking status (`pending_source` or `pending_sme_judgment`)
- Do NOT guess or invent the missing information
- Note "missing" in the evidence section, then link to the TBD

**When to use this:**
- When DDS is referenced but not provided
- When external programs are called but documentation is not available
- When copybooks or includes are referenced but not provided
- When behavior depends on undocumented external systems or APIs

---

## Language-Specific Evidence Examples

### RPGLE

```rpgle
**  Procedure specification (confirmed_from_code):
D ValidateAmount  PR              N
D   Amount                  7P 2 const
D   Limit                   7P 2 const
**  — Entry point and parameters are explicit in the spec.
**  — Evidence strength: confirmed_from_code

**  File specification (confirmed_from_code):
F CREDFILE    IF   A        K        DISK
D CREDFILE    E DS                  EXTNAME(CREDFILE)
**  — File name, type, access method are explicit.
**  — Evidence strength: confirmed_from_code

**  I/O statement (confirmed_from_code):
CHAIN CustID CREDFILE;
if not %found(CREDFILE);
   EVAL RC = -1;
   return;
endif;
**  — File access, key field, error path are explicit.
**  — Evidence strength: confirmed_from_code

**  Conditional logic (medium_confidence):
if Amount > 0;
   // process
else
   // error
endif;
**  — The implication is "Amount must be positive."
**  — Rule is inferred from the if/else structure, not explicitly declared.
**  — Evidence strength: medium_confidence

**  Error handling pattern (strongly_inferred):
MONITOR;
   CALL 'EXTERNAL' (Param Result);
   if Result = 'OK';
      EVAL Success = *on;
   endif;
ON-ERROR;
   EVAL Success = *off;
ENDMON;
**  — Multiple points suggest: "External call may fail; error handling is expected."
**  — Pattern shows both success and failure paths.
**  — Evidence strength: strongly_inferred
```

### CLLE

```clle
**  Entry point (confirmed_from_code):
       PGM        PARM(&INPUT &OUTPUT)
**  — Parameters are explicit in the PGM statement.
**  — Evidence strength: confirmed_from_code

**  CALL statement (confirmed_from_code):
       CALL       PGM(VALIDATE) PARM(&CUSTID &RC)
**  — Called program and parameters are explicit.
**  — Evidence strength: confirmed_from_code

**  Conditional logic (medium_confidence):
       IF         (&RC *EQ 0)
       THEN(DO)
           CALL   PGM(PROCESS)
       ENDDO
**  — The implication is "VALIDATE must return 0 before PROCESS is called."
**  — Rule is inferred from the if/then structure, not explicitly stated.
**  — Evidence strength: medium_confidence

**  Error monitoring (confirmed_from_code):
       MONMSG     CPF9801 EXEC(GOTO ERRHANDLR)
**  — Message monitoring is explicit.
**  — Evidence strength: confirmed_from_code
```

### COBOL

```cobol
       IDENTIFICATION DIVISION.
       PROGRAM-ID. VALIDATE-AMOUNT.
       
       PROCEDURE DIVISION USING
           BY VALUE AMOUNT
           BY VALUE LIMIT
           BY REFERENCE RESULT.
       
       **  Entry point (confirmed_from_code):
       **  — Parameters, direction (VALUE/REFERENCE), and types explicit.
       **  — Evidence strength: confirmed_from_code
       
           IF AMOUNT > LIMIT
               MOVE 'FAIL' TO RESULT
           ELSE
               MOVE 'PASS' TO RESULT
           END-IF.
           
       **  Conditional logic (confirmed_from_code):
       **  — IF condition is explicit; MOVE assignments are explicit.
       **  — Evidence strength: confirmed_from_code
           
           CALL 'GET-RATE' USING BY VALUE RATE-CODE
               RETURNING RATE.
       
       **  External call (confirmed_from_code):
       **  — Called program, parameter passing, return value explicit.
       **  — Evidence strength: confirmed_from_code
```

---

## Decision Tree: Which Evidence Strength?

```
Does the source code directly show the behavior?
(procedure spec, F-spec, I/O statement, CALL, MONITOR, IF condition?)
    ├─ YES → confirmed_from_code
    └─ NO  → Is the behavior inferred from a clear pattern?
            (e.g., field only assigned in one branch, call always preceded by validation?)
            ├─ Single point → medium_confidence
            ├─ Multiple points, consistent → strongly_inferred
            └─ Ambiguous or undocumented → needs_sme_review or missing
```

---

## Common Tagging Mistakes to Avoid

### Mistake 1: Inventing Evidence
**Wrong:**
```
File I/O: CREDFILE (evidence_strength: confirmed_from_code)
— Assumed the program reads CREDFILE based on field names.
```

**Right:**
```
File I/O: CREDFILE (evidence_strength: missing)
— DDS not provided; field access inferred from source but not confirmed.
→ TBD: Provide CREDFILE DDS definition
```

### Mistake 2: Tagging Inference as Confirmation
**Wrong:**
```
Entry Point: VALIDATECREDIT (evidence_strength: confirmed_from_code)
— The procedure is called, so it must exist.
```

**Right:**
```
Entry Point: VALIDATECREDIT (evidence_strength: medium_confidence)
— Called from main, but BEGPR block not visible in provided source.
→ TBD: Locate VALIDATECREDIT procedure definition
```

### Mistake 3: Vague TBDs Instead of Evidence
**Wrong:**
```
Error Handling: Unknown (needs_sme_review)
```

**Right:**
```
Error Handling: Network timeout behavior for GETRATE (needs_sme_review)
— Source shows CALL to GETRATE with no explicit timeout handling.
→ TBD: Confirm whether GETRATE call times out or returns error code
```

---

## Summary

- **confirmed_from_code:** Direct evidence in source (procedure spec, I/O statement, CALL, MONITOR)
- **medium_confidence:** Inferred from code logic but not explicitly stated
- **strongly_inferred:** Multiple evidence points converge on one conclusion
- **needs_sme_review:** Evidence present but interpretation ambiguous
- **missing:** Required evidence not available → create TBD

Every claim must carry evidence. When in doubt, use `needs_sme_review` or create a TBD rather than guessing.
