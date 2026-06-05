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

        ;*******Unconditional JUMP
    START:       
    PRINTN "CSE.PSTU"
    JMP START
     
    ; Ending PROC
MOV AH , 4CH
INT 21H
MAIN ENDP
    END MAIN                                                                 