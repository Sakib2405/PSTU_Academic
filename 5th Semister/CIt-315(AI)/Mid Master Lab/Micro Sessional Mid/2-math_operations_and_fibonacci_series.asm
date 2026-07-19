 ;Write a program to add two numbers as well as form a Fibonacci series.
 
 .MODEL SMALL
.STACK 100H
.DATA
    ADD_MSG     DB 'The sum of 15 and 10 is: ', '$'
    FIB_MSG     DB 10, 13, 'Fibonacci Series (first 10 terms): ', '$'
    NUM1        DW 15
    NUM2        DW 10
    SUM         DW ?
    FIB_COUNT   EQU 10 ; Number of Fibonacci terms to generate

.CODE

; Procedure to print a number in decimal format
PRINT_NUM PROC
    ; This procedure prints the number stored in AX
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

    ; --- Part 1: Add two numbers ---
    ; Print the addition message
    LEA DX, ADD_MSG
    MOV AH, 09H
    INT 21H

    ; Perform the addition
    MOV AX, NUM1
    ADD AX, NUM2
    MOV SUM, AX

    ; Print the result
    CALL PRINT_NUM

    ; --- Part 2: Generate Fibonacci Series ---
    ; Print the Fibonacci message
    LEA DX, FIB_MSG
    MOV AH, 09H
    INT 21H

    ; Initialize first two Fibonacci numbers
    MOV AX, 0       ; First term
    MOV BX, 1       ; Second term
    MOV CX, FIB_COUNT

FIB_LOOP:
    ; Print the current number (in AX)
    CALL PRINT_NUM

    ; Print a space
    MOV DL, ' '
    MOV AH, 02H
    INT 21H

    ; Calculate the next term
    MOV DX, AX      ; Store current term (AX) in DX
    MOV AX, BX      ; Move next term (BX) to current (AX)
    ADD BX, DX      ; New next term = old next term + old current term

    LOOP FIB_LOOP

    ; --- Exit the program ---
    MOV AH, 4CH
    INT 21H

MAIN ENDP
END MAIN
