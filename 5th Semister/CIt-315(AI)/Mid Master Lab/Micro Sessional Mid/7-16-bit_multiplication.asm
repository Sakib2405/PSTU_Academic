;Write a program to multiply two 16-bit numbers
 
.MODEL SMALL
.STACK 100H
.DATA
    NUM1    DW 1234
    NUM2    DW 567
    MSG1    DB '1234 * 567 = ', '$'

.CODE

; Procedure to print a 32-bit number in decimal format (from DX:AX)
PRINT_NUM_32 PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX

    XOR CX, CX      ; CX will count the digits
    MOV BX, 10      ; Divisor for decimal conversion

CONVERT_LOOP_32:
    XOR DX, DX      ; Clear high part of dividend (DX) for 16-bit DIV
                    ; But here we do 32-bit division, so we divide DX:AX by BX
    DIV BX          ; AX = (DX:AX) / 10, DX = (DX:AX) % 10
    PUSH DX         ; Push remainder (digit) onto the stack
    INC CX          ; Increment digit count
    CMP AX, 0       ; Is quotient zero?
    JNE CONVERT_LOOP_32 ; If not, repeat

PRINT_LOOP_32:
    POP DX          ; Pop digit from the stack
    ADD DL, '0'     ; Convert digit to its ASCII character representation
    MOV AH, 02H     ; Function to print a character
    INT 21H
    LOOP PRINT_LOOP_32 ; Repeat for all digits

    POP DX
    POP CX
    POP BX
    POP AX
    RET
PRINT_NUM_32 ENDP


MAIN PROC
    ; Initialize Data Segment
    MOV AX, @DATA
    MOV DS, AX

    ; --- Print message ---
    LEA DX, MSG1
    MOV AH, 09H
    INT 21H

    ; --- Perform 16-bit Multiplication ---
    MOV AX, NUM1    ; Load first number into AX (multiplicand)
    MOV BX, NUM2    ; Load second number into BX
    
    ; MUL BX multiplies AX by BX.
    ; The 32-bit result is stored in DX:AX.
    ; DX contains the high 16 bits, AX contains the low 16 bits.
    MUL BX

    ; --- Print the 32-bit result ---
    ; The result is already in DX:AX, which is what PRINT_NUM_32 expects.
    CALL PRINT_NUM_32

    ; --- Exit the program ---
    MOV AH, 4CH
    INT 21H

MAIN ENDP
END MAIN
