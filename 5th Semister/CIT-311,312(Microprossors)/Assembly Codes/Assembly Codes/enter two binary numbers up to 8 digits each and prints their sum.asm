.MODEL SMALL
.DATA
B1 DB ?
B2 DB ?
M1 DB 0AH,0DH,'TYPE A BINARY NUMBER , UP TO 8 DIGITS :','$'
M2 DB 0AH,0DH,'THE BINARY SUM IS ','$'
;--------------
.CODE
MAIN PROC
MOV AX,@DATA ;initialize DS
MOV DS,AX
MOV AH,9 ;prompt user
LEA DX,M1
INT 21H
MOV BL,0
MOV CX,8
MOV AH,1
L1: INT 21H
CMP AL,0DH
JE OUT
SUB AL,30H ;or use AND AL,01H
SHL BL,1
OR BL,AL
LOOP L1

OUT: MOV B1,BL ;1st no. read and store
MOV AH,9 ;prompt user for 2nd no.
INT 21H
MOV BL,0 ;read 2nd no.
MOV CX,8
MOV AH,1
L2: INT 21H
CMP AL,0DH
JE OUT2
SUB AL,30H
SHL BL,1
OR BL,AL
LOOP L2
OUT2: MOV B2,BL ;2nd no. read and store
MOV AH,9 ;show result
LEA DX,M2
INT 21H
ADD BL,B1 ;BL has 2nd no. (last one read)
MOV AH,2
MOV CX,8
L3: SHL BL,1 ;display binary
JC ONE
MOV DL,'0'
INT 21H
JMP continue
ONE: MOV DL,'1'

INT 21H
continue: LOOP L3
;-----------------
MOV AH,4CH ;return to DOS
INT 21H
MAIN ENDP
END MAIN




