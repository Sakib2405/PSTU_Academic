;Write a program to exchange the value of AX and BX.
 
 .MODEL SMALL
.STACK 100H
.DATA
    MSG_BEFORE DB 'Before exchange: AX=5, BX=10', 10, 13, '$'
    MSG_AFTER  DB 'After exchange: AX and BX swapped', 10, 13, '$'

.CODE
MAIN PROC
    ; Initialize Data Segment
    MOV AX, @DATA
    MOV DS, AX

    ; --- Print initial state message ---
    LEA DX, MSG_BEFORE
    MOV AH, 09H
    INT 21H

    ; --- Load initial values into AX and BX ---
    MOV AX, 5
    MOV BX, 10

    ; (For demonstration, you could print them here if you had a print number routine)

    ; --- Exchange the values of AX and BX ---
    XCHG AX, BX

    ; --- Print final state message ---
    LEA DX, MSG_AFTER
    MOV AH, 09H
    INT 21H

    ; (Now AX holds 10 and BX holds 5. A print routine would confirm this.)

    ; --- Exit the program ---
    MOV AH, 4CH
    INT 21H

MAIN ENDP
END MAIN
