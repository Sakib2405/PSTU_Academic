.MODEL SMALL
.STACK 100H
.DATA

;the string to be printed

STRING DB 'this is a simple string','$',

.CODE

MAIN PROC FAR
    mov ax,'1',
    mov bx, '2'
    
    push ax
    push bx
    
    pop ax
    pop bx
    
    
    mov dx,ax
    mov ah,2
    int 21h
    mov dx,bx
    mov ah,2
    int 21h
    mov ah,4ch
    int 21h
    mov ah,4ch
    int 21h
 
MAIN ENDP
END MAIN
