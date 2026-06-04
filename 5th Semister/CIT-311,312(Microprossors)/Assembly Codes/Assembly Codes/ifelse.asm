include 'emu8086.inc'          
.MODEL SMALL;might be large/huge/medium/compact
.STACK 100H

.DATA       ;START Data Segment

     
.CODE              ;Starting code sement
    MAIN PROC      ;Main Procedure as like void main()
    
     MOV BX , -10 
     
     CMP BX , 0
     JL ifff;JUMP LESS
     JGE eelse   ;jump greater than or equal
     
     
     
     ifff:  
     printn "number is negative"
     jmp last; if this is avoided then sequential execution is execited
     ;;;
     
     eelse:
        printn "number is positive"
     
             
     last:
     printn "you are terminated"
     
     
; Ending PROC
MOV AH , 4CH
INT 21H
MAIN ENDP
    END MAIN                                                                 