.MODEL SMALL
.DATA
START DB 0AH,0DH
HLF DB ?,' Half '
QUA DB ?,' Quarter '
DIM DB ?,' Dimes '
NIC DB ?,' Nickels '
PEN DB ?,' Pennies ','$'
.CODE
MAIN PROC
MOV AX,@DATA
MOV DS,AX
;-------------------------------------------------

MOV BL,50 ;half DOllaR
DIV BL
ADD AL,30h ;CONVERT TO DIGIT
MOV HLF,AL

;----------------------
MOV AL,AH
MOV AH,0
MOV BL,25 ;Quarter
DIV BL
ADD AL,30h
MOV QUA,AL
;---------------------
MOV AL,AH
MOV AH,0
MOV BL,10 ;DIME
DIV BL
ADD AL,30H
MOV DIM,AL
;-------------------
MOV AL,AH
MOV AH,0
MOV BL,5 ;nickle
DIV BL
ADD AL,30h
MOV NIC,AL
;----------------
ADD AH,30h
MOV PEN,AH ;remainder is pennies
;---------------------------------------------------------
MOV AH,9 ;display result
LEA DX,START
INT 21H

;-----------------
MOV AH,4CH
INT 21H
MAIN ENDP

END MAIN


