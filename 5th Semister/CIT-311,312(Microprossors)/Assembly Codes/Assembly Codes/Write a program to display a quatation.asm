.MODEL SMALL
.CODE
MAIN PROC
MOV AH,2
MOV DL,'?'
INT 21H ;display ?
MOV AH,1
INT 21H ; read 1st char. & put it in BL
MOV BL,AL
INT 21H ;read 2nd char. in AL
;--------------------------
CMP BL,AL 

JG SWITCH   ;if not orderd     

JMP DISPLAY 

SWITCH: 

XCHG AL,BL 

DISPLAY:   

MOV AH,2
MOV DL, 0AH ;enter
INT 21H
MOV DL,BL
INT 21H
MOV DL,AL

INT 21H
OUT_:

 MOV AH,4CH
INT 21H
MAIN ENDP
END MAIN
