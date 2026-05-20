# Error Handling Taxonomy: IBM i Error Patterns

This guide documents common error handling patterns in IBM i programs (RPGLE, CLLE, COBOL) and their modernization equivalents, helping the analyzer recognize error paths and classify error conditions.

---

## RPGLE Error Handling Patterns

### 1. File Operation Errors with Indicators

```rpgle
**  Legacy pattern (indicators):
CHAIN CustID CREDFILE           99 95
C  *IN99              IFEQ      *ON
C                     EVAL      RC = -1  // Not found
C                     ELSE
C  *IN95              IFEQ      *ON
C                     EVAL      RC = -2  // I/O error
C                     ELSE
C                     EVAL      RC = 0   // Success
C                     ENDIF
C                     ENDIF

**  Modern pattern (built-in functions):
CHAIN CustID CREDFILE;
if not %found(CREDFILE);
   EVAL RC = -1;  // Not found
   return;
endif;
if %error();
   EVAL RC = -2;  // I/O error
   return;
endif;
EVAL RC = 0;      // Success

**  Indicators:
**  — *IN99 (record not found after CHAIN)
**  — *IN95 (I/O error)
**  — Other numbered indicators (*IN01, *IN02, etc.) for custom flags
**
**  Built-in functions:
**  — %found() — true if record found
**  — %error() — true if I/O error occurred
**  — %status() — numeric status code (0 = success)
```

### 2. MONITOR / ON-ERROR Blocks

```rpgle
**  Basic MONITOR:
MONITOR;
   CHAIN CustID CREDFILE;
   CALL 'EXTERNAL' (Param Result);
   
ON-ERROR;  // Catch all exceptions
   EVAL RC = -99;
ENDMON;

**  Specific message catching:
MONITOR;
   OPEN CREDFILE;
   
ON-ERROR CPF4401;  // File already open
   EVAL RC = 1;
   
ON-ERROR CPF4101;  // File not found
   EVAL RC = -1;
   
ON-ERROR;          // Any other error
   EVAL RC = -99;
ENDMON;

**  CPF message classes:
**  — CPF24xx (File operation errors)
**  — CPF40xx (File open/close errors)
**  — CPF99xx (Various system errors)
**  — SQL0xxx (Database errors)
**
**  MONITOR catches exceptions that would normally terminate the program.
**  ON-ERROR CPFxxxx catches specific IBM i message classes.
**  Multiple ON-ERROR handlers can stack (specific to general).
**  Last ON-ERROR (no suffix) catches all remaining errors.
```

### 3. Call to External Program Errors

```rpgle
**  Check return status:
EVAL RC = 0;
CALL 'EXTERNAL' (Input Output);
if RC <> 0;
   // Error occurred; Output contains error code
endif;

**  With MONITOR:
MONITOR;
   CALL 'EXTERNAL' (Input Output);
   if Output = 'ERROR';
      EVAL RC = -1;
   else
      EVAL RC = 0;
   endif;
   
ON-ERROR CPD0006;  // Program not found
   EVAL RC = -2;
   
ON-ERROR;          // I/O error, system error
   EVAL RC = -99;
ENDMON;

**  Return value styles (RPGLE only):
EVAL RC = EXTERNAL_FUNC(Input);  // Function returns value
EVAL RC = ValidateAmount(Amount, Limit);  // PR returning numeric/logical

**  External program styles:
CALL 'PROGRAM' (Input Output);    // Output modified by called program
EVAL RC = CALLP(Input);           // CALLP returns value (RPGLE to RPGLE)
```

### 4. Data Validation Errors

```rpgle
**  Numeric validation:
if %NUMVAL(InputString) < 0;
   EVAL RC = -1;  // Invalid: negative amount
endif;

if InputAmount = *ZERO;
   EVAL RC = -2;  // Invalid: zero amount
endif;

if InputAmount > MaxAmount;
   EVAL RC = -3;  // Invalid: exceeds limit
endif;

**  String validation:
if %TRIM(InputString) = '';
   EVAL RC = -1;  // Invalid: empty input
endif;

if %LEN(%TRIM(InputString)) > 10;
   EVAL RC = -2;  // Invalid: exceeds max length
endif;

**  Built-in functions for validation:
**  — %NUMVAL() — convert string to numeric (fails if not valid)
**  — %TRIM() — remove leading/trailing spaces
**  — %LEN() — string length
**  — %UPPER(), %LOWER() — case conversion
```

### 5. Return Codes (Numeric Status)

```rpgle
**  Common return code convention:
**  0    = Success
**  > 0  = Warning (business logic issue, not error)
**  < 0  = Error (system error, recoverable)
**  < -1 = Critical error (unrecoverable)

**  Examples:
*  -1  = File not found
*  -2  = Record not found
*  -3  = I/O error
*  -4  = Program not found
*  -5  = Invalid parameter
*  -99 = Unexpected error

*  1   = Record exists (warning in some contexts)
*  2   = Amount exceeds limit (business rule, not error)
*  0   = Success
```

---

## CLLE Error Handling Patterns

### 1. MONMSG (Monitor Message)

```clle
       MONMSG MSGID(CPF4101) EXEC(DO)
           SNDPGMMSG 'File not found'
           GOTO NOTFND
       ENDDO
       
       OPEN FILE(CREDFILE)
       
       GOTO ENDPROG
       
       NOTFND:
       SNDPGMMSG 'Cannot continue'
       RETURN
       
       ENDPROG:
       CLOSE FILE(CREDFILE)
       RETURN
       ENDPGM

**  MONMSG monitors for specific messages.
**  MSGID(CPFxxxx) specifies message ID to catch.
**  EXEC clause specifies recovery action (CALL, GOTO, DO, etc.).
**  Multiple MONMSG can stack (specific to general).
**  Default MONMSG (no ID) catches all messages.
```

### 2. Call to Program with Status Checking

```clle
       CALL PGM(VALIDATE) PARM(&INPUT &OUTPUT &RC)
       
       IF (&RC *NE 0)
       THEN(DO)
           SNDPGMMSG ('Validation failed: ' *CAT &RC)
           GOTO ERRHANDLR
       ENDDO

**  RC is output parameter from called program.
**  Check RC after CALL to determine success/failure.
**  RC values are set by called program.
```

### 3. CLLE Command Status Checking

```clle
       CALL PGM(PROCESS)
       
       IF (MSGTYPE *EQ 'R')  // Exception (error)
       THEN(DO)
           SNDPGMMSG 'Process failed'
           GOTO ERRHANDLR
       ENDDO
       
       IF (MSGTYPE *EQ 'C')  // Completion (success)
       THEN(DO)
           SNDPGMMSG 'Process completed'
       ENDDO

**  MSGTYPE indicates message type:
**  — C (Completion) — normal completion
**  — I (Informational) — informational message
**  — W (Warning) — warning (but processing continues)
**  — E (Error) — error condition
**  — R (Recovery) — exception (program terminated abnormally)
**
**  Check MSGTYPE after commands to determine success/failure.
```

### 4. Return Code Variable

```clle
       DCL &RC *CHAR 4 VALUE('0000')
       
       CALL PGM(EXTERNAL) PARM(&INPUT &RC)
       
       EVALUATE &RC
       WHEN ('0000')
           SNDPGMMSG 'Success'
       WHEN ('0001')
           SNDPGMMSG 'Warning'
       WHEN ('9999')
           SNDPGMMSG 'Critical error'
       OTHRWISE
           SNDPGMMSG ('Unknown RC: ' *CAT &RC)
       ENDSEL

**  Called program sets &RC (output parameter).
**  Caller checks &RC to determine action.
**  String or numeric format (depends on program).
```

---

## COBOL Error Handling Patterns

### 1. File Operation Status Codes

```cobol
       OPEN INPUT CUSTFILE.
       
       IF WS-RETURN-CODE NOT = 0
           MOVE 'OPEN FAILED' TO ERROR-MSG
           PERFORM ERROR-HANDLER
           STOP RUN
       END-IF.
       
       READ CUSTFILE INTO CUSTOMER-REC
           AT END
               MOVE 'Y' TO EOF-FLAG
           NOT AT END
               PERFORM PROCESS-CUSTOMER
       END-READ.
       
       CLOSE CUSTFILE.

**  RETURN-CODE (global variable) set by system.
**  FILE-STATUS (optional) holds file operation status:
**  — '00' = successful read
**  — '10' = end-of-file
**  — '21' = sequence error
**  — '30' = permanent I/O error
**  — '9x' = vendor-specific error
**
**  AT END / NOT AT END in READ statement for inline handling.
```

### 2. Call to External Program with Return Code

```cobol
       CALL 'GETRATE' USING
           BY VALUE RATE-CODE
           BY REFERENCE RATE
           BY REFERENCE STATUS-CODE.
       
       EVALUATE STATUS-CODE
           WHEN 0
               PERFORM PROCESS-RATE
           WHEN 1
               MOVE 'RATE NOT FOUND' TO ERROR-MSG
           WHEN 2
               MOVE 'SYSTEM ERROR' TO ERROR-MSG
           WHEN OTHER
               MOVE 'UNKNOWN ERROR' TO ERROR-MSG
       END-EVALUATE.

**  STATUS-CODE is output parameter (BY REFERENCE).
**  Called program sets STATUS-CODE.
**  Caller checks to determine action.
```

### 3. Inline Error Handling

```cobol
       READ CUSTFILE INTO CUSTOMER-REC
           AT END
               MOVE 'Y' TO EOF-FLAG
               PERFORM FINAL-PROCESSING
           NOT AT END
               PERFORM PROCESS-CUSTOMER
           ON EXCEPTION
               MOVE 'FILE ERROR' TO ERROR-MSG
               PERFORM ERROR-HANDLER
       END-READ.

**  AT END — condition: EOF
**  NOT AT END — condition: record found
**  ON EXCEPTION — error condition
**  Each condition can have inline PERFORM (subroutine call).
```

### 4. EVALUATE for Conditional Error Handling

```cobol
       ACCEPT USER-INPUT.
       
       EVALUATE TRUE
           WHEN FUNCTION TEST-NUMVAL(USER-INPUT) = 0
               MOVE FUNCTION NUMVAL(USER-INPUT) TO AMOUNT
               PERFORM VALIDATE-AMOUNT
           WHEN USER-INPUT = SPACES
               MOVE 'INPUT REQUIRED' TO ERROR-MSG
               PERFORM ERROR-HANDLER
           WHEN OTHER
               MOVE 'INVALID INPUT' TO ERROR-MSG
               PERFORM ERROR-HANDLER
       END-EVALUATE.

**  EVALUATE with WHEN conditions for validation.
**  Built-in function TEST-NUMVAL checks if string is numeric.
**  FUNCTION NUMVAL converts valid string to number.
**  WHEN OTHER catches unexpected conditions.
```

### 5. Return Code / Status Variables

```cobol
       01 WS-STATUS-CODE PIC 9(4) VALUE 0.
       01 WS-ERROR-FLAG PIC X VALUE 'N'.
       01 WS-ERROR-MSG PIC X(50) VALUE SPACES.
       
       PROCEDURE DIVISION.
       
       OPEN INPUT CREDFILE.
       
       IF WS-STATUS-CODE NOT = 0
           MOVE 'Y' TO WS-ERROR-FLAG
           MOVE 'CREDFILE OPEN FAILED' TO WS-ERROR-MSG
           PERFORM ERROR-HANDLER
           STOP RUN
       END-IF.
       
       PROCESS-LOOP.
           READ CREDFILE INTO CREDFILE-REC
               AT END
                   MOVE 'Y' TO EOF-FLAG
               NOT AT END
                   PERFORM PROCESS-RECORD
           END-READ.
       
       ERROR-HANDLER.
           DISPLAY WS-ERROR-MSG.
           MOVE 'Y' TO WS-ERROR-FLAG.

**  WS-STATUS-CODE = numeric error code
**  WS-ERROR-FLAG = flag (Y/N) indicating error state
**  WS-ERROR-MSG = descriptive error message
**  ERROR-HANDLER paragraph logs error and sets flags.
```

---

## Error Conditions and Mappings

| Legacy Error | IBM i Message | RPGLE Pattern | COBOL Pattern | Modernization Equivalent |
| --- | --- | --- | --- | --- |
| Record not found | (file op indicator) | %found() → false | AT END | EntityNotFoundException |
| File not found | CPF4101 | MONITOR ON-ERROR | FILE-STATUS '30' | FileNotFoundException |
| File already open | CPF4401 | MONITOR ON-ERROR | FILE-STATUS '21' | DuplicateResourceException |
| Program not found | CPD0006 | MONITOR ON-ERROR | CALL failure | ProgramNotFoundException |
| Invalid parameter | CPD0001 | Data validation | EVALUATE / TEST-NUMVAL | ValidationException |
| I/O error | CPFxxxx | MONITOR ON-ERROR / %error() | FILE-STATUS '30' | IOError / SQLException |
| Access denied | CPF9802 | MONITOR ON-ERROR | CALL failure | AccessDeniedException |
| Numeric overflow | (RPGLE runtime) | %NUMVAL() validation | EVALUATE / TEST-NUMVAL | NumberFormatException |
| Deadlock | CPFxxxx (lock) | MONITOR ON-ERROR | FILE-STATUS / CALL failure | LockTimeoutException |

---

## Error Handling Anti-Patterns to Avoid

### Mistake 1: Ignoring File Operation Errors
```rpgle
**  WRONG (ignores not found):
CHAIN CustID CREDFILE;
EVAL Amount = Amount + CREDLIMIT;  // *IN99 not checked

**  RIGHT (checks not found):
CHAIN CustID CREDFILE;
if not %found(CREDFILE);
   EVAL RC = -1;
   return;
endif;
EVAL Amount = Amount + CREDLIMIT;
```

### Mistake 2: Generic Error Handling (Loses Context)
```clle
**  WRONG (catches all, loses detail):
MONMSG MSGID(*ANY) EXEC(GOTO ERRHANDLR)

**  RIGHT (specific, with recovery):
MONMSG MSGID(CPF4101) EXEC(DO)
   SNDPGMMSG 'File not found'
   GOTO NOTFND
ENDDO
MONMSG MSGID(CPF4401) EXEC(DO)
   SNDPGMMSG 'File already open'
   GOTO ALREADYOPEN
ENDDO
```

### Mistake 3: Unhandled External Call Failures
```rpgle
**  WRONG (no error path):
CALL 'EXTERNAL' (Input Output);
EVAL Result = Output;  // What if EXTERNAL failed?

**  RIGHT (error path):
MONITOR;
   CALL 'EXTERNAL' (Input Output);
   EVAL Result = Output;
ON-ERROR;
   EVAL Result = DEFAULT;
   EVAL RC = -1;
ENDMON;
```

### Mistake 4: Silent Failures (No Logging)
```cobol
**  WRONG (error ignored):
READ CUSTFILE
   AT END
       MOVE 'Y' TO EOF-FLAG
   NOT AT END
       PERFORM PROCESS-RECORD
END-READ.

**  RIGHT (error logged):
READ CUSTFILE
   AT END
       MOVE 'Y' TO EOF-FLAG
   NOT AT END
       PERFORM PROCESS-RECORD
   ON EXCEPTION
       MOVE 'READ ERROR' TO ERROR-MSG
       PERFORM ERROR-HANDLER
       MOVE 'Y' TO EOF-FLAG
END-READ.
```

---

## Error Handling Summary

**RPGLE:**
- Indicators (legacy): *INxx flags set by file operations
- Built-in functions (modern): %found(), %error(), %status()
- MONITOR / ON-ERROR for exception handling

**CLLE:**
- MONMSG for message monitoring and recovery
- MSGTYPE variable for command status
- CALL return code checking

**COBOL:**
- FILE-STATUS codes for file operations
- AT END / NOT AT END / ON EXCEPTION in READ
- EVALUATE for conditional error handling
- Return code variables for program status

All three share common patterns (file not found, I/O error, parameter validation) but express them differently. Recognize the pattern to understand error conditions and recovery paths.

