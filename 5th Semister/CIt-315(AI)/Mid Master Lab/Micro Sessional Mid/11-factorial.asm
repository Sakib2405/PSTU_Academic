;Write a program  to find the factorial of a number

.MODEL SMALL
.STACK 100H
.DATA
    NUMBER      DB 5 ; Find the factorial of this number (max ~8 for 16-bit, ~12 for 32-bit)
    MSG1        DB 'Factorial of ', '$'
    MSG2        DB ' is: ', '$'

.CODE

; Procedure to print a 32-bit number in decimal format (from DX:AX)
PRINT_NUM_32 PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; This procedure converts the 32-bit number in DX:AX to a string of
    ; decimal digits and prints them. It works by repeatedly dividing
    ; the number by 10 and pushing the remainders (the digits) onto the stack.
    
    XOR CX, CX          ; Clear digit counter
    MOV BX, 10          ; Set divisor to 10

CONVERT_LOOP:
    ; Check if the number (DX:AX) is zero.
    CMP DX, 0           ; Is the high word zero?
    JNE DO_DIVIDE       ; If not, continue to divide.
    CMP AX, 0           ; Is the low word zero?
    JE CONVERT_DONE     ; If both are zero, conversion is done.

DO_DIVIDE:
    ; The DIV instruction with a 16-bit operand (BX) divides the 32-bit
    ; number in DX:AX by the operand.
    ; Result: Quotient is in AX, Remainder is in DX.
    DIV BX
    
    PUSH DX             ; Push the remainder (this is our digit) onto the stack.
    INC CX              ; Increment the digit counter.
    
    ; For the next iteration, the number to divide is the quotient, which is
    ; now in AX. We must clear DX because the quotient fits entirely in AX.
    XOR DX, DX
    JMP CONVERT_LOOP

CONVERT_DONE:
    ; If the original number was 0, we need to print a single '0'.
    CMP CX, 0
    JNE PRINT_LOOP
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    JMP PRINT_EXIT

PRINT_LOOP:
    POP DX              ; Pop a digit from the stack.
    ADD DL, '0'         ; Convert it to its ASCII character representation.
    MOV AH, 02h         ; DOS function to print a character.
    INT 21h
    LOOP PRINT_LOOP     ; Repeat until all digits are printed.

PRINT_EXIT:
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

    ; --- Print the initial message ---
    LEA DX, MSG1
    MOV AH, 09H
    INT 21H

    XOR AH, AH          ; Clear AH to safely work with AL
    MOV AL, NUMBER
    ADD AL, '0'         ; Convert number to ASCII to print it
    MOV DL, AL
    MOV AH, 02H
    INT 21H

    LEA DX, MSG2
    MOV AH, 09H
    INT 21H

    ; --- Calculate Factorial ---
    XOR AH, AH          ; Clear high byte of AX
    MOV AL, NUMBER      ; Load number into AL for calculation
    
    MOV CX, AX          ; Use CX as the loop counter
    DEC CX              ; We need to multiply N * (N-1) * ... * 1, so N-1 loops.
    
    ; For the first multiplication, we need to multiply AX by CX
    MUL CX              ; AX = AX * CX (e.g., 8 * 7)
    
FACTORIAL_LOOP:
    DEC CX              ; Decrement counter (e.g., 6, 5, 4...)
    CMP CX, 1           ; Stop when we get to 1
    JBE END_FACTORIAL   
    
    ; MUL CX multiplies AX by CX. The 32-bit result is stored in DX:AX.
    MUL CX              
    JMP FACTORIAL_LOOP

END_FACTORIAL:
    ; The final result is in DX:AX.
    CALL PRINT_NUM_32   ; Print the 32-bit result.

    ; --- Exit the program ---
    MOV AH, 4CH
    INT 21H

MAIN ENDP
END MAIN
