;Write a program to find the Square Root of a number

.MODEL SMALL
.STACK 100H
.DATA
    NUMBER      DW 25  ; The number to find the square root of
    RESULT      DW 0
    MSG1        DB 'The square root of ', '$'
    MSG2        DB ' is: ', '$'

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

    ; --- Print the initial message ---
    LEA DX, MSG1
    MOV AH, 09H
    INT 21H

    ; Print the number
    MOV AX, NUMBER
    CALL PRINT_NUM

    LEA DX, MSG2
    MOV AH, 09H
    INT 21H

    ; --- Calculate Square Root ---
    ; Algorithm: Subtract successive odd numbers (1, 3, 5...)
    ; The number of subtractions is the integer square root.
    MOV AX, NUMBER  ; Load the number
    MOV BX, 1       ; First odd number to subtract
    MOV CX, 0       ; The result (square root)

SQRT_LOOP:
    CMP AX, 0       ; Check if number is zero or less
    JLE END_SQRT    ; If so, we are done
    SUB AX, BX      ; Subtract the odd number
    ADD BX, 2       ; Get the next odd number
    INC CX          ; Increment the root
    JMP SQRT_LOOP   ; Repeat

END_SQRT:
    MOV RESULT, CX  ; Store the result
    MOV AX, RESULT  ; Move result to AX for printing
    CALL PRINT_NUM  ; Print the calculated square root

    ; --- Exit the program ---
    MOV AH, 4CH
    INT 21H

MAIN ENDP
END MAIN
