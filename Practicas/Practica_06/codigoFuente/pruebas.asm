E1 EQU 50
 ORG $4000
E5 EQU 15
 JMP E1
 JMP E4
E2 BNE $0
 LBNE 0
 BCS E2
 BCS E4
 LBNE E1
E3 LBNE E4
 IBEQ A,E2
 IBEQ A,E2
 IBEQ A,E4
 IBEQ B,E4
 JMP E5
 LBNE E5
 ORG $4050
 DC.B 30
E4 END