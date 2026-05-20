     H DFTACTGRP(*NO) ACTGRP(*CALLER) OPTION(*SRCSTMT:*NODEBUGIO)
     FCUSTINQDSP CF   E             WORKSTN
     D CustNo          S              9P 0
     D ExitFlg         S              1A   INZ('N')
     D RefreshFlg      S              1A   INZ('N')

     C                   EXSR      LOADHDR
     C                   EXSR      LOADSFL
     C                   DOW       ExitFlg = 'N'
     C                   EXFMT     TXNCTL
     C                   IF        *IN05 = *ON
     C                   EVAL      RefreshFlg = 'Y'
     C                   EXSR      LOADSFL
     C                   ENDIF
     C                   IF        *IN12 = *ON
     C                   EVAL      ExitFlg = 'Y'
     C                   ENDIF
     C                   ENDDO
     C                   SETON                                        LR
     C                   RETURN

     C     LOADHDR       BEGSR
     C*                  header lookup omitted in synthetic sample
     C                   ENDSR

     C     LOADSFL       BEGSR
     C*                  transaction subfile population omitted in synthetic sample
     C                   ENDSR
