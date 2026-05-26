
; Program to substract 2 BCD number
.MODEL SMALL
.STACK 100
.DATA
     NUM1 DB 85H
     NUM2 DB 57H
     RES DB 0
 
.CODE
   MOV AX , @DATA ; Initialize Data Segment
   MOV DS , AX
 
   MOV AL , NUM1 ; Load 1'st number
   SUB AL , NUM2 ; Substract 2nd number from 1st number
   DAS ; Only works on AL register
   ; Decimal Adjust After Substraction
 
   MOV RES , AL ; Store result
 
   MOV AH , 4CH  ; Intrupt to exit
   INT 21H
END