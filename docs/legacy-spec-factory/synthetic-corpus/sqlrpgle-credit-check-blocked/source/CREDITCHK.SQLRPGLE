     H DFTACTGRP(*NO) ACTGRP(*CALLER) OPTION(*SRCSTMT:*NODEBUGIO)
     FQSYSPRT   O    F  132        PRINTER
     D CustNo          S              9P 0
     D ReqAmt          S              9P 2
     D AvailCredit     S              9P 2
     D ApprAmt         S              9P 2
     D Status          S              1A
     D Decision        S              1A
     D MsgText         S             50A
     D CREDITCHK       PR             1A
     D  pCustNo                       9P 0 CONST
     D  pReqAmt                       9P 2 CONST
     D  pApprAmt                      9P 2
     D CREDITCHK       PI             1A
     D  pCustNo                       9P 0 CONST
     D  pReqAmt                       9P 2 CONST
     D  pApprAmt                      9P 2

      /EXEC SQL
      SET OPTION COMMIT = *NONE, CLOSQLCSR = *ENDMOD
      /END-EXEC

     C                   EVAL      CustNo = pCustNo
     C                   EVAL      ReqAmt = pReqAmt
     C                   EVAL      ApprAmt = 0
     C                   EVAL      Decision = 'D'
     C                   EVAL      MsgText = ' '

      /EXEC SQL
      SELECT STATUS,
             AVAIL_CREDIT
        INTO :Status,
             :AvailCredit
        FROM CREDITVW
       WHERE CUSTNO = :CustNo
      /END-EXEC

     C                   IF        SQLCOD = 100
     C                   EVAL      MsgText = 'CUSTOMER NOT FOUND'
     C                   EXSR      PRTMSG
     C                   RETURN    Decision
     C                   ENDIF

     C                   IF        SQLCOD <> 0
     C                   EVAL      MsgText = 'SQL ERROR ON CREDIT LOOKUP'
     C                   EXSR      PRTMSG
     C                   RETURN    Decision
     C                   ENDIF

     C                   IF        Status = 'H'
     C                   EVAL      MsgText = 'CUSTOMER ON HOLD'
     C                   EXSR      PRTMSG
     C                   RETURN    Decision
     C                   ENDIF

     C                   IF        Status <> 'A'
     C                   EVAL      MsgText = 'CUSTOMER INACTIVE'
     C                   EXSR      PRTMSG
     C                   RETURN    Decision
     C                   ENDIF

     C                   IF        ReqAmt <= AvailCredit
     C                   EVAL      ApprAmt = ReqAmt
     C                   EVAL      Decision = 'A'
     C                   ELSE
     C                   EVAL      ApprAmt = AvailCredit
     C                   EVAL      MsgText = 'REQUEST OVER AVAILABLE CREDIT'
     C                   EXSR      PRTMSG
     C                   ENDIF

     C                   EVAL      pApprAmt = ApprAmt
     C                   RETURN    Decision

     C     PRTMSG        BEGSR
     C                   WRITE     PRTLINE
     C                   ENDSR

     OQSYSPRT   E            PRTLINE        1
     O                         MsgText
