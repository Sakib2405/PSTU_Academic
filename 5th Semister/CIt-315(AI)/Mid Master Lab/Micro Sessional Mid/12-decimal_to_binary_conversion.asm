;Write a program  for Decimal to Binary Conversion

.MODEL SMALL
.STACK 100H
.DATA
    DECIMAL_NUM DW 25
    MSG1        DB 'The binary value of ', '$'
    MSG2        DB ' is: ', '$'

.CODE

; Procedure to print a number in decimal format
PRINT_DEC PROC
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
PRINT_DEC ENDP


MAIN PROC
    ; Initialize Data Segment (DS)
    MOV AX, @DATA
    MOV DS, AX

    ; --- Print the message ---
    LEA DX, MSG1
    MOV AH, 09H
    INT 21H
    
    MOV AX, DECIMAL_NUM
    CALL PRINT_DEC

    LEA DX, MSG2
    MOV AH, 09H
    INT 21H

    ; --- Convert and Print Binary Representation ---
    MOV AX, DECIMAL_NUM ; Load the number to be converted.
    MOV CX, 16          ; A 16-bit number has 16 digits, so we loop 16 times.

PRINT_BIN_LOOP:
    ; The SHL (Shift Logical Left) instruction shifts all bits in AX to the left
    ; by one position. The bit that was in the most-significant position (bit 15)
    ; is moved into the Carry Flag (CF).
    SHL AX, 1

    ; We will default the character to print to '0' and change it to '1' only if
    ; the carry flag was set.
    MOV DL, '0'
    JNC PRINT_BIT       ; JNC means "Jump if No Carry". If CF is 0, print '0'.
    
    ; If the jump was not taken, it means the Carry Flag was set to 1.
    MOV DL, '1'

PRINT_BIT:
    ; We must save AX before calling the DOS interrupt, as INT 21H can
    ; modify the AL register, which would corrupt our number.
    PUSH AX
    MOV AH, 02H
    INT 21H
    POP AX              ; Restore AX after the interrupt.

    LOOP PRINT_BIN_LOOP ; This instruction decrements CX and jumps back to the
                        ; beginning of the loop if CX is not yet zero.

    ; --- Exit the program ---
    MOV AH, 4CH
    INT 21H

MAIN ENDP
END MAIN

