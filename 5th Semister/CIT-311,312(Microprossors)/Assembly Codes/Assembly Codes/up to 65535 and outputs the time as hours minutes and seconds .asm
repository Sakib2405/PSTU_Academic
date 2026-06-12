.MODEL SMALL
.STACK 64
.DATA
M1 DB 0AH,0DH,'THE TIME IS $'
.CODE 




INOEe PROC
2: ; reads a number in range -32768 to 32767
3: ;input: none
4: ; output: AX • binary equivalent of number
5: PUSf! BX ; save registers used
6:
7:
PUSH ex
PUSH DX
8: ; print prompt
9: @BEGIN:
10:
11:
MOV
MOV
12: INT
AH,2
DL, '?'
21H
13: ;total • 0
14: XOR BX,BX
15:
16:
17:
1 e:
19:
20:
21:
22:
23:
24:
25:
;negative .. false
xoR ex,ex
;read a character
MOV AH, 1
INT 21H
;case character of
eMP AL,'-'
JE @MINUS
eMP AL,'+'
JE @PLUS
JMP @REPEAT2
26: @Mil'US:
27: MOV
28: @PLUS:
29: INT
30: ;end_case
31: @REPEAT.2:
ex,1
21H
32:
33:
34:
;if character is between
eMP AL,' 0'
JNGE @NOT_DIGIT
;print '?'
; BX holds total
; ex holds sign ·
; character in AL
;minus sign?
;yes, set sign
;plus sign
;yes, get another character
;start processing characters
;negative a true
;read a character
'O' and '9'
;character >a '0'?
;illegal character
35.: CMP AL,' 9' ;chllracter <- '9'?
36: JNLE @NOT_DIGIT ;no, illegal character
37: ; then convert character to, a digit
38: AND AX,OOOFH ;convert to digit
39: PUSH AX ;save on stack
40: ;total .. total x 10 + digit
41: MOV AX,10 ;get 10
42: MUL BX ;AX .. total x 10
4 3: POP BX ; retrieve digit
44: ADD BX,AX ;total -·total x 10 + di~it
45:
4 6:
4 7:
48:
4 9:
50:
51:
52:
53:
;read a character
MOV AH,1
INT 21H
CMP AL,ODH
JNE @REPEAT2
;until CR
MOV AX,BX
;if negative
OR ex, ex
;carriage return?
; no, keep going
;store number in AX
;negative number
MAIN PROC
MOV AX,@DATA ;intialize DS
MOV DS,AX
CALL INDEC
MOV DX,0 ;make sure no thing in DX
MOV BX,3600 ;60min*60sec=1hr
DIV BX
PUSH AX
PUSH DX
;---------
MOV AH,9 ;display result
LEA DX,M1
INT 21H
POP DX
POP AX ;AX has hours
CALL OUTDEC
PUSH DX
MOV AH,2
MOV DL,':'
INT 21H
;----------
POP AX
MOV BX,60
MOV DX,0
DIV BX
CALL OUTDEC ;AX has mins
PUSH DX
;-----------
MOV AH,2
MOV DL,':'
INT 21H
POP AX
CALL OUTDEC ;AX has sec remainder
;----------
MOV AH,4CH ;return to DOS
INT 21H
MAIN ENDP
END MAIN