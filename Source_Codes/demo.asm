MCHRS     START   1000
FIRST     LDX     ZERO
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