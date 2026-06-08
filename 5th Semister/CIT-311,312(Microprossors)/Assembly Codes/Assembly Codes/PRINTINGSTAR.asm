include 'emu8086.inc'
.MODEL SMALL
.STACK 100H

.DATA
N DB ?
SUM DB 0 

.CODE

MAIN PROC 
    
   MOV AX,@DATA
   MOV DS,AX
   PRINTN "ENTER INPUT= "
   MOV AH,1
   INT 21H
   
   SUB AL,48
   MOV N,AL ;N HOLDS GIVEN INPUT
   
   MOV BH,1 ;INITIALIZATION OF LOOP
   
   PRINTN
    LOOP1:
    CMP BH,N
    
    JG EXIT_LOOP1
    
    MOV BL,1
    
    LOOP2:
    CMP BL,N
    
    JG EXIT_LOOP2
    ;MOV AH,2
    ;MOV DL,'*'
    
    PRINT '*'
    
    ;INT 21H
    
    INC BL
    JMP LOOP2
    
    EXIT_LOOP2:
    PRINTN 
    INC BH
    JMP LOOP1
    
    EXIT_LOOP1:
    PRINTN "END * PRINT"
    
    MAIN ENDP
END MAIN