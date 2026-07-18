;Write a program to add two 16-bit numbers

.MODEL SMALL
.STACK 100H
.DATA
    NUM1        DW 45000
    NUM2        DW 30000
    SUM         DW ?
    MSG1        DB '45000 + 30000 = ', '$'
    MSG_CARRY   DB 10, 13, 'Result overflowed 16 bits (Carry Flag = 1)', '$'
    MSG_NOCARRY DB 10, 13, 'Result fit in 16 bits (Carry Flag = 0)', '$'
    
.CODE

; Procedure to print a number in decimal format
PRINT_NUM PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    XOR CX, CX
    MOV BX, 10
CONVERT_LOOP:
    XOR DX, DX
    DIV BX
    PUSH DX
    INC CX
    CMP AX, 0
    JNE CONVERT_LOOP
PRINT_LOOP:
    POP DX
    ADD DL, '0'
    MOV AH, 02H
    INT 21H
    LOOP PRINT_LOOP
    POP DX
    POP CX
    POP BX
    POP AX
    RET
PRINT_NUM ENDP


MAIN PROC
    ; Initialize Data Segment
    MOV AX, @DATA
    MOV DS, AX

    ; --- Print message ---
    LEA DX, MSG1
    MOV AH, 09H
    INT 21H

    ; --- Perform 16-bit Addition ---
    MOV AX, NUM1
    ADD AX, NUM2    ; Add NUM2 to AX. Result is in AX.
    MOV SUM, AX     ; Store the low 16 bits of the sum.
    
    ; The Carry Flag (CF) will be set if the result is > 65535.
    
    CALL PRINT_NUM  ; Print the 16-bit result (wraps around on overflow)

    ; --- Check for Carry and print appropriate message ---
    JC CARRY_SET    ; Jump if Carry Flag is set
    
    ; No carry
    LEA DX, MSG_NOCARRY
    MOV AH, 09H
    INT 21H
    JMP EXIT

CARRY_SET:
    ; Carry was set
    LEA DX, MSG_CARRY
    MOV AH, 09H
    INT 21H

EXIT:
    ; --- Exit the program ---
    MOV AH, 4CH
    INT 21H

MAIN ENDP
END MAIN
