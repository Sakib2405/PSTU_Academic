.MODEL SMALL
.stack 64
.DATA
Counter DB 100 ;number to be generated
Counter2 DB 4 ;4 number on same line
.CODE
Main PROC
MOV AX,@DATA
MOV DS,AX
;-------------------
CALL INBINARY
MOV AX,BX
Begin: 
MOV DL,4
L10:
 POP AX
CALL RANDOM
CALL OUTBIN
PUSH AX
;-------------------
MOV AH,2
MOV DL,20H ;blank space
INT 21H
DEC counter2
CMP counter2,0 ;is there 4-number on line
JE NEW_LINE
DEC Counter
CMP Counter,0
JNE L10
JMP OUT_
NEW_LINE: MOV AH,2
MOV DL,0AH ;enter LF
INT 21H
JMP Begin
OUT_:
MOV AH,4CH
INT 21H
;-------------------------
Main ENDP  

INBINARY PROC
XOR BX,BX
Mov CX,15
MOV AH,1
INT 21H
WHILE_: CMP AL,0DH
JE END_WHILE
AND AL,01H
SHL BX,1
OR BL,AL
INT 21H
LOOP WHILE_
END_WHILE:
RET
INBINARY ENDP 
RANDOM PROC
;input in AX : start with any number in the range
;output in AX (Random number)
PUSH BX ;save regs
PUSH DX
SHL AX,1 ; shift left once
MOV DX,AX ;get copy
SHL DX,1 ;make bit-14 be bit-15
XOR AX,DX ;xor bit-14 with bit-15
TEST DX,8000h ;result of XOR bit-14 with bit-15
JZ NOT_ONE
OR AX,1 ;replace bit-0 with result (1)
JMP CL_B15 ;clear bit-15
NOT_ONE: AND AX,0FFFEH ;replace bit-0 with (0)
CL_B15: AND AX,7FFFH
POP DX ;restore regs
POP BX
RET
RANDOM ENDP
OUTBIN PROC
;input AX
;output on screen
;we copy number in BX to make sure not changing the
;number because of output function that depend on AX
MOV BX,AX ;get copy
MOV CX,16
start: ROL BX,1
JC ONE
MOV AH,2
MOV DL,'0'
INT 21H
JMP L1
ONE: MOV AH,2
MOV DL,'1'
INT 21H
L1: LOOP start
;put the random number in AX to be new number to

MOV AX,BX
RET
OUTBIN ENDP
;see Appendix C for include pseudo-ops
;Test is folder’s name in c:\ contain procedures
;INCLUDE C:\TEST\RANDOM.ASM
;INCLUDE C:\TEST\INBINARY.ASM
;INCLUDE C:\TEST\OUTBIN.ASM
END Main