     H DFTACTGRP(*NO) ACTGRP(*CALLER) OPTION(*SRCSTMT:*NODEBUGIO)
     FARTXN     IF   E           K DISK
     FARCTRL    UF A E           K DISK
     FARERRRPT  O    F  132        PRINTER
     D RunDate         S              8S 0
     D BatchStatus     S             10A
     D TxnAmt          S              9P 2
     D AppliedAmt      S              9P 2
     D DiffAmt         S              9P 2
     D RestartFlg      S              1A
     D MsgText         S             50A
     D ARRECON         PR
     D ARRECON         PI

      /EXEC SQL
      SET OPTION COMMIT = *NONE, CLOSQLCSR = *ENDMOD
      /END-EXEC

     C                   EXSR      LOADCTRL
     C                   IF        RestartFlg = 'Y'
     C                   EXSR      LOGMSG
     C                   ENDIF

     C                   SETLL     *LOVAL    ARTXN
     C                   READ      ARTXN
     C                   DOW       NOT %EOF(ARTXN)
      /EXEC SQL
      SELECT APPLIED_AMT
        INTO :AppliedAmt
        FROM ARTXN
       WHERE RUNDATE = :RunDate
         AND DOCNO   = :DOCNO
      /END-EXEC
     C                   EVAL      TxnAmt = DOCAMT
     C                   EVAL      DiffAmt = TxnAmt - AppliedAmt
     C                   IF        DiffAmt <> 0
     C                   EVAL      MsgText = 'RECON EXCEPTION'
     C                   EXSR      PRTRPT
     C                   ENDIF
     C                   READ      ARTXN
     C                   ENDDO

     C                   EXSR      MARKDONE
     C                   SETON                                        LR
     C                   RETURN

     C     LOADCTRL      BEGSR
     C                   CHAIN     'ARRECON' ARCTRL
     C                   IF        %FOUND(ARCTRL)
     C                   EVAL      RunDate = CTRLRUNDT
     C                   EVAL      RestartFlg = RESTARTFL
     C                   ELSE
     C                   EVAL      RunDate = 20260520
     C                   EVAL      RestartFlg = 'N'
     C                   ENDIF
     C                   ENDSR

     C     LOGMSG        BEGSR
     C                   EVAL      MsgText = 'RESTART PATH ACTIVE'
     C                   EXSR      PRTRPT
     C                   ENDSR

     C     PRTRPT        BEGSR
     C                   WRITE     RPTLINE
     C                   ENDSR

     C     MARKDONE      BEGSR
     C                   CHAIN     'ARRECON' ARCTRL
     C                   IF        %FOUND(ARCTRL)
     C                   EVAL      BATCHSTS = 'COMPLETE'
     C                   UPDATE    CTRLREC
     C                   ENDIF
     C                   ENDSR

     OARERRRPT  E            RPTLINE        1
     O                         MsgText
     O                         DOCNO
     O                         DOCAMT
     O                         AppliedAmt
     O                         DiffAmt
