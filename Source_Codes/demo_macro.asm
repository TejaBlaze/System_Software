M1        MACRO   &A,&B
          STCH    &A,X
          LDCH    &B,X
          MEND
M2        MACRO   &A
          LDCH    &A,X
          STCH    &A,X
          MEND
MCHRS     START   1000
FIRST     LDX     ZERO
          M1      STR1,STR2
          M2      STR2
          M1      STR3,STR2
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
          END     FIRST