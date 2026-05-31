.MODEL SMALL
.DATA
M1 DB 0AH,'TYPE A HEXA NUMBER 0 -FFFF :$'
M2 DB 0AH,'THE SUM IN HEXA IS $'
COUNTER DB 4
NUM DW ?
.CODE
MAIN PROC
MOV AX,@DATA ;initialize DS
MOV DS,AX
MOV AH,9 ;prompt user
LEA DX,M1
INT 21H
CALL READ
MOV NUM,BX ;store 1st num.
MOV AH,9 ;prompt user for 2nd number
LEA DX,M1
INT 21H
CALL READ ;no need to store 2nd num.
;because it will still in BX

;-----------
MOV AH,9 ;display result msg
LEA DX,M2
INT 21H
ADD BX,NUM
;BX=num1(NUM)+num2(BX)
JC SHOWCY ;if there carry
MOV AH,2 ;no carry
MOV DL,'0'
INT 21H
JMP NEXT
SHOWCY:MOV AH,2
MOV DL,'1'
INT 21H
NEXT: CALL SHOW
MOV AH,4CH ;return to DOS
INT 21H
MAIN ENDP ;end of main program

;----------------------------------------
READ PROC ;for read hexa digit
XOR BX,BX
MOV CL,4
MOV AH,1
INT 21H
WHILE_: CMP AL,0DH
JE END_W
CMP AL,'9' ;detect for letter hexa
JG LETTER
AND AL,0FH
JMP SHIFT
LETTER: SUB AL,37H
SHIFT: SHL BX,CL
OR BL,AL
INT 21H
JMP WHILE_
END_W: RET
READ ENDP
;------------------------------------
SHOW PROC ;to display result of addition
MOV CL,4
START: MOV DL,BH
SHR DL,CL
CMP DL,9
JG LETTER1
ADD DL,30H
JMP SHOW1

LETTER1:ADD DL,37H
SHOW1: MOV AH,2
INT 21H
ROL BX,CL
DEC COUNTER
CMP COUNTER,0
JNE START
RET
SHOW ENDP
;----------------------------------------


