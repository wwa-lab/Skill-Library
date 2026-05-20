# Control Flow Patterns: IBM i Language Conventions

This guide documents common control flow patterns in RPGLE, CLLE, and COBOL, helping the analyzer recognize standard structures and avoid misinterpreting idioms.

---

## RPGLE Control Flow Patterns

### Entry Points

```rpgle
**  Main program entry point:
H MAIN
D Main            PR
D   CustID                  9P 0 const
D   Amount                  7P 2 const
D   ReturnCode              1A

Main(CustID: Amount: ReturnCode);

**  This program is called with (CustID, Amount).
**  ReturnCode is returned as output (passed by reference).
**  Evidence: MAIN control statement + procedure signature
```

### Sub-Procedures (BEGPR / ENDPR)

```rpgle
**  Callable sub-procedure within same source:
D ValidateCredit  PR              N
D   Amount                  7P 2 const
D   Limit                   7P 2 const

/free
   if ValidateCredit(InputAmount: CreditLimit);
      // Validation passed
   else
      // Validation failed
   endif;
/end-free

P ValidateCredit  B
D PI              PR              N
D   Amount                  7P 2 const
D   Limit                   7P 2 const

/free
   if Amount <= Limit;
      return *ON;
   else
      return *OFF;
   endif;
P ValidateCredit  E

**  Sub-procedure is defined between P/B (begin) and P/E (end) opcodes.
**  Declaration (D) section shows entry point, parameters, return type.
**  ENDPR marks the end of the procedure.
**  Evidence: BEGPR / ENDPR blocks and D spec in header
```

### Conditional Branching

```rpgle
**  Simple IF / ELSE:
if ValidateAmount = *on;
   EVAL RC = 'PASS';
else
   EVAL RC = 'FAIL';
endif;

**  SELECT / WHEN (multi-way branch):
select;
   when Amount < 0;
      EVAL RC = 'INVALID';
   when Amount > Limit;
      EVAL RC = 'DENIED';
   when Amount = *zero;
      EVAL RC = 'MISSING';
   other;
      EVAL RC = 'PASS';
endsl;

**  Indicator-driven branching (legacy):
C     CUSTID        CHAIN      CREDFILE                   99
C     *IN99         IFEQ       *ON
C                   EVAL       RC = -1
C                   ELSE
C                   EVAL       RC = 0
C                   ENDIF

**  *IN99 is set by CHAIN if not found.
**  Legacy style uses numbered indicators (e.g., *IN01, *IN99).
**  Modern style uses %found() or %status() instead.
```

### Loops

```rpgle
**  Simple DO loop (fixed iterations):
for I = 1 to 10;
   // Process item I
endfor;

**  DO UNTIL loop (exit condition):
do until %eof(CUSTFILE);
   // Process current record
   read CUSTFILE;
enddo;

**  READE loop (read equal, automatic loop):
CHAIN CustID CUSTFILE;
READE CustID CUSTFILE;
   // Process record matching CustID
   READE CustID CUSTFILE;
enddo;

**  READE automatically loops through records with matching key.
**  Loop exits when EOF or key no longer matches.
```

### File Operations

```rpgle
**  SETLL (Set Lower Limit):
SETLL (Country Category) LIMITTBL;
if not %found(LIMITTBL);
   // No matching record; skip READE
endif;

**  Sets file pointer to first record matching key.
**  %found() returns true if exact match found.
**  Used with READE to loop through matching records.

**  READE (Read Equal):
READE (Country Category) LIMITTBL;
   // Process record with matching key
   READE (Country Category) LIMITTBL;
enddo;

**  Reads records while key matches.
**  Stops when EOF or key no longer matches.

**  CHAIN (Random Access):
CHAIN CustID CREDFILE;
if not %found(CREDFILE);
   // No matching record
else
   // Process found record
endif;

**  Direct record access by key.
**  %found() returns true if record found.

**  WRITE / UPDATE / DELETE:
WRITE NEWREC CREDFILE;       // Add new record
UPDATE EXISTINGREC CREDFILE; // Modify existing record
DELETE CREDFILE;              // Delete current record
```

### Error Handling with MONITOR

```rpgle
**  MONITOR / ON-ERROR:
MONITOR;
   CHAIN CustID CREDFILE;
   if not %found(CREDFILE);
      EVAL RC = -1;
   endif;
   
   CALL 'EXTERNAL' (Param Result);
   
ON-ERROR CPF9801;  // Specific message class
   EVAL RC = -2;
   EVAL ErrorMsg = 'File not found';
   
ON-ERROR;          // Catch-all (any unhandled error)
   EVAL RC = -99;
   EVAL ErrorMsg = 'Unexpected error';
ENDMON;

**  MONITOR catches exceptions and recovers.
**  ON-ERROR CPFxxxx catches specific IBM i message classes.
**  ON-ERROR without suffix catches any unhandled error.
**  Multiple ON-ERROR handlers can be stacked.
```

### Evaluation & Assignment

```rpgle
**  EVAL / EVAL-CORR:
EVAL RC = ValidateAmount(Amount, Limit);
EVAL-CORR OutputRec = InputRec;  // Copy matching fields by name

**  EVAL evaluates expression and assigns result.
**  EVAL-CORR matches field names; fills output with input values where names match.

**  Built-in Functions:
EVAL Upper = %UPPER(Lower);
EVAL Found = %FOUND(CREDFILE);
EVAL EOF = %EOF(CUSTFILE);
EVAL Status = %STATUS();
EVAL Length = %LEN(Variable);

**  %FOUND() — true if last file operation found a record
**  %EOF() — true if end-of-file reached on last read
**  %STATUS() — numeric status after last operation
**  %UPPER(), %LOWER() — case conversion
**  %LEN() — length of variable or field
```

### Return from Procedure

```rpgle
**  Explicit return:
P ValidateCredit  B
D PI              PR              N
D   Amount                  7P 2 const
D   Limit                   7P 2 const

/free
   if Amount <= Limit;
      return *ON;      // Return true, exit procedure
   else
      return *OFF;     // Return false, exit procedure
   endif;
P ValidateCredit  E

**  Implicit return (fall through):
P GetRate        B
D PI              PR            7P 4
D   RateCode                4A   const

/free
   CHAIN RateCode RATETBL;
   if %found(RATETBL);
      return RATE;     // Return RATE field value
   else
      return 0;        // Return default (0.0000)
   endif;
   // If no return statement, procedure returns to caller
P GetRate        E
```

---

## CLLE Control Flow Patterns

### Entry Point

```clle
       PGM        PARM(&INPUT &OUTPUT &STATUS)
       
       DCL &INPUT *CHAR 10
       DCL &OUTPUT *CHAR 20
       DCL &STATUS *CHAR 1
       
       // Main logic
       RETURN
       ENDPGM

**  PARM statement declares input/output parameters.
**  RETURN exits the program (optional; falls through to ENDPGM).
```

### Conditional Branching

```clle
       IF (&RC *EQ 0)
       THEN(DO)
           // Success path
           CALL PGM(PROCESS)
       ENDDO
       ELSE(DO)
           // Error path
           SNDPGMMSG 'Error occurred'
       ENDDO

**  IF ... THEN ... ELSE ... ENDDO
**  Conditions: *EQ, *NE, *LT, *LE, *GT, *GE
**  Parentheses required around variable comparisons.

       SELECT
       WHEN (&MODE *EQ 'A')
           CALL PGM(ADD)
       WHEN (&MODE *EQ 'D')
           CALL PGM(DELETE)
       WHEN (&MODE *EQ 'U')
           CALL PGM(UPDATE)
       OTHRWISE
           SNDPGMMSG 'Unknown mode'
       ENDSEL

**  SELECT / WHEN / OTHRWISE for multi-way branching.
```

### Loops

```clle
       DOFOR &I *FROM 1 *TO 100
           // Process item &I
       ENDDO

**  DOFOR loops from start value to end value.

       DOWHILE (&RC *EQ 0)
           CALL PGM(PROCESS) PARM(&RC)
           // Continue while RC = 0
       ENDDO

**  DOWHILE loops while condition is true.
```

### Calling Programs

```clle
       CALL PGM(VALIDATE) PARM(&INPUT &OUTPUT &RC)
       
**  CALL invokes another program.
**  PARM passes parameters by reference.
**  RC is output parameter (modified by called program).

       CALL PGM(EXTERNAL) PARM(&INPUT) RTNVAL(&RESULT)
       
**  RTNVAL captures return value from called program (RPGLE).
```

### Error Handling with MONMSG

```clle
       MONMSG CPF0001 EXEC(DO)
           SNDPGMMSG 'Operation failed'
           GOTO ERRHANDLR
       ENDDO
       
       CALL PGM(EXTERNAL)
       
       MONMSG CPF9801 EXEC(GOTO NOTFND)  // File not found
       MONMSG CPF0006 EXEC(GOTO ENDPROG) // Any error
       
       GOTO ENDPROG
       
       NOTFND:
       SNDPGMMSG 'File not found'
       
       ERRHANDLR:
       SNDPGMMSG 'Unhandled error'
       
       ENDPROG:
       RETURN
       ENDPGM

**  MONMSG monitors for specific CPF message codes.
**  EXEC clause specifies recovery action (GOTO, CALL, etc.).
**  Multiple MONMSG statements can stack.
**  GOTO jumps to a label (marked with LABEL:).
```

---

## COBOL Control Flow Patterns

### Entry Point

```cobol
       IDENTIFICATION DIVISION.
       PROGRAM-ID. VALIDATE-AMOUNT.
       
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01 WS-AMOUNT PIC 9(7)V99 VALUE 0.
       01 WS-LIMIT PIC 9(7)V99 VALUE 0.
       01 WS-RESULT PIC X VALUE 'F'.
       
       PROCEDURE DIVISION USING
           BY VALUE WS-AMOUNT
           BY VALUE WS-LIMIT
           BY REFERENCE WS-RESULT.
           
           IF WS-AMOUNT <= WS-LIMIT
               MOVE 'P' TO WS-RESULT
           ELSE
               MOVE 'F' TO WS-RESULT
           END-IF.
           
           STOP RUN.

**  PROCEDURE DIVISION USING declares parameters.
**  BY VALUE — parameter is input only (copy passed)
**  BY REFERENCE — parameter is input/output (reference passed)
**  STOP RUN exits the program.
```

### Conditional Branching

```cobol
       IF AMOUNT <= LIMIT
           PERFORM VALIDATE-OK
       ELSE
           PERFORM VALIDATE-FAIL
       END-IF.

**  IF ... ELSE ... END-IF

       EVALUATE TRUE
           WHEN AMOUNT < 0
               MOVE 'INVALID' TO RESULT
           WHEN AMOUNT > LIMIT
               MOVE 'DENIED' TO RESULT
           WHEN AMOUNT = 0
               MOVE 'MISSING' TO RESULT
           WHEN OTHER
               MOVE 'PASS' TO RESULT
       END-EVALUATE.

**  EVALUATE / WHEN / WHEN OTHER for multi-way branching.
**  EVALUATE TRUE with WHEN conditions is COBOL idiom (switch on condition).
```

### Loops with PERFORM

```cobol
       PERFORM PROCESS-RECORD
           VARYING COUNTER FROM 1 BY 1
           UNTIL COUNTER > 100.

**  PERFORM ... VARYING loops from start value by increment until condition.

       PERFORM PROCESS-RECORD
           UNTIL EOF-FLAG = 'Y'.

**  PERFORM ... UNTIL loops while condition is false.

       PERFORM PROCESS-RECORD.
       READ CUSTFILE
           AT END MOVE 'Y' TO EOF-FLAG
       END-READ.

**  PERFORM statement executes a paragraph (like a subroutine).
**  Automatically returns to next statement after paragraph.
```

### File Operations

```cobol
       OPEN INPUT CUSTFILE.
       
       READ CUSTFILE INTO CUSTOMER-REC
           AT END MOVE 'Y' TO EOF-FLAG
           NOT AT END PERFORM VALIDATE-CUSTOMER
       END-READ.
       
       CLOSE CUSTFILE.

**  OPEN / CLOSE for file management.
**  READ with AT END and NOT AT END for conditional logic.
**  INTO clause moves record into working storage.

       MOVE CUSTID TO SEARCH-KEY.
       START CREDFILE KEY >= SEARCH-KEY.
       READ CREDFILE
           AT END MOVE 'Y' TO EOF-FLAG
       END-READ.

**  START positions file for sequential read.
**  KEY >= starts at first record >= key value.
```

### Calling External Programs

```cobol
       CALL 'GETRATE' USING
           BY VALUE RATE-CODE
           BY REFERENCE RATE
           BY REFERENCE STATUS-CODE.

**  CALL invokes external program.
**  BY VALUE passes copy of parameter.
**  BY REFERENCE passes reference (output allowed).
**  Program modifies BY REFERENCE parameters.
```

### Error Handling

```cobol
       OPEN INPUT CUSTFILE.
       IF STATUS-CODE NOT = '00'
           MOVE 'OPEN FAILED' TO ERROR-MSG
           PERFORM ERROR-HANDLER
       END-IF.

**  COBOL checks STATUS-CODE field after file operations.
**  Status codes: '00' (success), '10' (EOF), '30' (record not found), '9x' (error).

       ACCEPT USER-INPUT.
       EVALUATE TRUE
           WHEN FUNCTION TEST-NUMVAL(USER-INPUT) = 0
               MOVE FUNCTION NUMVAL(USER-INPUT) TO NUMBER
           WHEN OTHER
               MOVE 'INVALID INPUT' TO ERROR-MSG
               PERFORM ERROR-HANDLER
       END-EVALUATE.

**  Built-in functions: TEST-NUMVAL (check validity), NUMVAL (convert string to number).
**  EVALUATE with WHEN conditions for validation.

       EVALUATE STATUS-CODE
           WHEN '00'
               PERFORM SUCCESS-PATH
           WHEN '10'
               PERFORM EOF-HANDLER
           WHEN '30'
               PERFORM NOT-FOUND-HANDLER
           WHEN OTHER
               PERFORM ERROR-HANDLER
       END-EVALUATE.

**  Multi-way branching on status codes (file operations return specific codes).
```

### Paragraphs (Subroutines)

```cobol
       PROCEDURE DIVISION.
       MAIN-PROCEDURE.
           PERFORM VALIDATE-INPUT.
           PERFORM PROCESS-RECORDS.
           PERFORM CLEANUP.
           STOP RUN.

       VALIDATE-INPUT.
           IF INPUT-AMOUNT <= 0
               MOVE 'INPUT INVALID' TO ERROR-MSG
               PERFORM ERROR-HANDLER
           END-IF.

       PROCESS-RECORDS.
           OPEN INPUT CUSTFILE.
           PERFORM UNTIL EOF-FLAG = 'Y'
               READ CUSTFILE
                   AT END MOVE 'Y' TO EOF-FLAG
                   NOT AT END PERFORM PROCESS-ONE-RECORD
               END-READ
           END-PERFORM.
           CLOSE CUSTFILE.

       PROCESS-ONE-RECORD.
           ... process current record ...

       CLEANUP.
           CLOSE CUSTFILE.
           STOP RUN.

**  Paragraphs are subroutines (like RPGLE BEGPR / ENDPR).
**  PERFORM calls a paragraph; control returns after paragraph ends.
**  Paragraphs are defined by label followed by period.
**  PERFORM UNTIL or PERFORM ... VARYING can loop through paragraphs.
```

---

## Common Pitfalls to Avoid

### Pitfall 1: Confusing SETLL and READE
- **SETLL** only sets the file pointer; does not loop or read records.
- **READE** loops through records with matching key.
- Always pair SETLL with READE to read matching records.

### Pitfall 2: Missing Error Handling After CHAIN
```rpgle
**  WRONG (missing error path):
CHAIN CustID CREDFILE;
EVAL ProcessedAmount = Amount + CREDLIMIT;

**  RIGHT (error path included):
CHAIN CustID CREDFILE;
if not %found(CREDFILE);
   EVAL RC = -1;
   return;
endif;
EVAL ProcessedAmount = Amount + CREDLIMIT;
```

### Pitfall 3: Misinterpreting Indicator Logic
```rpgle
**  WRONG (assumes indicator is input):
if *IN99 = *ON;
   // Assumes *IN99 was set externally
endif;

**  RIGHT (indicator is typically output from file operation):
CHAIN CustID CREDFILE;       // *IN99 set by CHAIN
if %found(CREDFILE);         // Modern equivalent
   // Record found
endif;
```

### Pitfall 4: Ignoring EVALUATE / SELECT Exit
```rpgle
**  WRONG (SELECT falls through):
select;
   when Amount < 0;
      EVAL RC = 'INVALID';
   when Amount > Limit;
      EVAL RC = 'DENIED';  // Falls through if first condition matches!
endsl;

**  RIGHT (SELECT exits after matching WHEN):
select;
   when Amount < 0;
      EVAL RC = 'INVALID';
   when Amount > Limit;
      EVAL RC = 'DENIED';   // SELECT exits; no fall-through
   other;
      EVAL RC = 'PASS';
endsl;
```

---

## Summary

**RPGLE:** Procedure-oriented, indicator-driven (legacy) or function-based (modern). BEGPR/ENDPR for sub-procedures. MONITOR for error handling.

**CLLE:** Command-driven, procedural. CALL for program invocation. MONMSG for error monitoring.

**COBOL:** Record-oriented, paragraph-based. PERFORM for subroutines. EVALUATE for branching. Explicit file status handling.

All three use similar concepts (procedures, loops, branching, file I/O) but different syntax. Recognize the pattern, not the syntax, to understand the intended behavior.

