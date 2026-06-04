.MODEL SMALL;might be large/huge/medium/compact
.STACK 100H

.DATA       ;START Data Segment

     ;Variable Declaration Part
     ;variable_name variable_size assigned_value
     NUM1             DB           48
     NUM2 DB ?
     CHAR DB '#'
     STR DB "WELCOME TO PSTU $" 
     
.CODE              ;Starting code sement
    MAIN PROC      ;Main Procedure as like void main()
    
      ;Using Data seg variable in code seg.
      MOV AX , @DATA                                                                    
      MOV DS , AX 
      
 
      ;************Taking input from keyboard *****SCANF()
    MOV AH , 1; A function is called by system for input
    INT 21H 
    MOV NUM2 , AL; Transfer the 
 
 
   ;New line
      MOV AH , 2
      MOV DL , 0AH; ASCII of new line
      INT 21H
      MOV DL , 0DH
      INT 21H
      
 
    ;************Output PRINTF()
    MOV AH , 2
    MOV DL , NUM2
    INT 21H

      
; Ending PROC
MOV AH , 4CH
INT 21H
MAIN ENDP
    END MAIN                                                                 