INCLUDE 'EMU8086.INC'



.model small
.stack 100h
.code
.data
main proc
    mov bx,0
    mov AH,1
    FOR1:
    int 21h
    
    
    cmp AL,0DH
    JE END_FOR1
    SUB AL,30H
    SHL BX,1
    OR BL,AL
    JMP FOR1 
    
    END_FOR1:
    PRINTN
    PRINTN    
    MOV AH,2  
    ADD BL,30H
    MOV DL,BL
    INT 21H
    
    
    
    EXIT: 
    MOV AH,4CH
    MAIN ENDP
END MAIN
    