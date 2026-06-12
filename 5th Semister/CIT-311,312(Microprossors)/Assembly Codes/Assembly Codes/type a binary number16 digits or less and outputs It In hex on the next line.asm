.MODEL SMALL
.DATA
M1 DB 0AH,0DH,'TYPE A BINARY DIGIT ,UP TO 16-BIT: ','$'
M2 DB 0AH,0DH,'IN HEXA IT IS :','$'
.CODE
MAIN PROC
MOV AX,@DATA ;initialize DS
MOV DS,AX
MOV AH,9 ;prompt user
LEA DX,M1
INT 21H
;--------------
MOV BX,0 ;prepare for read binary
MOV AH,1
MOV CX,16
L1: INT 21H
CMP AL,0DH ;finish enter
JE OUT_
AND AL,01H ;convert to numerical 0,1
SHL BX,1 ;store it in BX
OR BL,AL
LOOP L1

OUT_: MOV AH,9
LEA DX,M2
INT 21H
MOV DH,4 ;show 4-digit hexa
L2: MOV CL,4
MOV DL,BH
SHR DL,CL
MOV AH,2
CMP DL,9 ;detect the digit
JG LETTER
ADD DL,30H
INT 21H
JMP L3
LETTER:
ADD DL,37H
INT 21H
L3: ROL BX,CL ;get second hexa digit
DEC DH
CMP DH,0
JNE L2 ;if 4-digit hexa displayed exit

MOV AH,4CH ;return to DOS
INT 21H
MAIN ENDP
END MAIN




