;Write a program  for Binary to Decimal Conversion

.MODEL SMALL
.STACK 100H
.DATA
    BINARY_NUM  DW 11011011B ; Binary number to be converted (219 in decimal)
    MSG1        DB 'The decimal value of 11011011b is: ', '$'

.CODE

; Procedure to print a number in decimal format
PRINT_NUM PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX

    XOR CX, CX      ; CX will count the digits
    MOV BX, 10      ; Divisor for decimal conversion

CONVERT_LOOP:
    XOR DX, DX      ; Clear DX for division
    DIV BX          ; AX = AX / 10, DX = AX % 10
    PUSH DX         ; Push remainder (digit) onto the stack
    INC CX          ; Increment digit count
    CMP AX, 0       ; Is quotient zero?
    JNE CONVERT_LOOP ; If not, repeat

PRINT_LOOP:
    POP DX          ; Pop digit from the stack
    ADD DL, '0'     ; Convert digit to its ASCII character representation
    MOV AH, 02H     ; Function to print a character
    INT 21H
    LOOP PRINT_LOOP ; Repeat for all digits

    POP DX
    POP CX
    POP BX
    POP AX
    RET
PRINT_NUM ENDP


MAIN PROC
    ; Initialize Data Segment (DS)
    MOV AX, @DATA
    MOV DS, AX

    ; --- Print the message ---
    LEA DX, MSG1
    MOV AH, 09H
    INT 21H

    ; --- Load the binary number and print its decimal equivalent ---
    MOV AX, BINARY_NUM
    CALL PRINT_NUM

    ; --- Exit the program ---
    MOV AH, 4CH
    INT 21H

MAIN ENDP
END MAIN
