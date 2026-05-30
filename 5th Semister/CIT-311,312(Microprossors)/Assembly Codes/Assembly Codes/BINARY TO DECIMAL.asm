.model small
.stack 100h
.data
.code
main proc 
    
    mov BX,0; BX=0
    MOV AH,1 
    FOR1:
    int 21h
    cmp al,0DH
    JE END_FOR1
    SUB AL,30H
    SHL BX,1
    
    OR BL,AL
    JMP FOR1
    END_FOR1:   
              
    mov ah,2
    mov dl,10
    int 21h  
    mov dl,13
    int 21h
        
 
     MOV AH,2
     ADD BL,30H
     MOV DL,BL
     INT 21H
     EXIT:
     MOV AH,4CH
     INT 21H
     MAIN ENDP
END MAIN
       
    
    
    