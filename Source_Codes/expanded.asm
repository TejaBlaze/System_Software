MCHRS     START   1000
FIRST     LDX     ZERO
.          M1      STR1,STR2
          STCH    STR1,X
          LDCH    STR2,X
.          M2      STR2
          LDCH    STR2,X
          STCH    STR2,X
.          M1      STR3,STR2
          STCH    STR3,X
          LDCH    STR2,X
MOVECH    LDCH    STR1,X
          STCH    STR2,X
          TIX     ELEVEN
          JLT     MOVECH
          RSUB
STR1      BYTE    C’EOF’
STR2      RESB    11
STR3      RESW    4
ZERO      WORD    0
ELEVEN    WORD    11
          END     FIRS
