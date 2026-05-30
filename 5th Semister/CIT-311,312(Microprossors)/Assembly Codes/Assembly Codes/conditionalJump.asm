include 'emu8086.inc'          
.MODEL SMALL;might be large/huge/medium/compact
.STACK 100H

.DATA       ;START Data Segment

 ;Variable Declaration Part
 ;variable_name variable_size assigned_value
     NUM1 DB ?
     NUM2 DB ?
     CHAR DB '#'
     STR DB "WELCOME TO PSTU $" 
     
.CODE              ;Starting code sement
    MAIN PROC      ;Main Procedure as like void main()
    
      ;Using Data seg variable in code seg.
      MOV AX , @DATA                                                                    
      MOV DS , AX 
      
MOV CX , 5
MOV BX , 0
    
    ;*******Conditional JUMP
    START:   
        CMP BX , CX; result might be bx==cx,bx>cx, bc<cx
        JE LAST;JE stands for jump equal    
        PRINTN "CSE.PSTU" 
        INC BX 
        JNE START; jump not equal
    
    LAST:
    PRINTN "END OF PROC"


      
; Ending PROC
MOV AH , 4CH
INT 21H
MAIN ENDP
    END MAIN                                                                 