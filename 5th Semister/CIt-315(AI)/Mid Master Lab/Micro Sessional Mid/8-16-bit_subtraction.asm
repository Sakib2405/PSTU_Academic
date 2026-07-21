;Write a program to subtract two 16-bit numbers with or without borrow

.MODEL SMALL
.STACK 100H
.DATA
    NUM_A       DW 5000
    NUM_B       DW 2000
    
    NUM_C       DW 1000
    NUM_D       DW 3000

    MSG1        DB '5000 - 2000 = ', '$'
    MSG2        DB 10, 13, 'No borrow needed. (Carry Flag = 0)', '$'
    MSG3        DB 10, 13, '1000 - 3000 = ', '$'
    MSG4        DB 10, 13, 'Borrow was needed. (Carry Flag = 1)', '$'

.CODE

; Procedure to print a number in decimal format
PRINT_NUM PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Handle negative numbers
    CMP AX, 0
    JGE POSITIVE
    
    ; It's negative, print '-' and negate AX
    PUSH AX
    MOV DL, '-'
    MOV AH, 02H
    INT 21H
    POP AX
    NEG AX

POSITIVE:
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

    ; --- Scenario 1: Subtraction without borrow ---
    LEA DX, MSG1
    MOV AH, 09H
    INT 21H

    MOV AX, NUM_A
    SUB AX, NUM_B   ; Subtract NUM_B from NUM_A. Result in AX.
    ; After this, Carry Flag (CF) is 0 because 5000 > 2000 (no borrow).
    
    CALL PRINT_NUM  ; Print the result

    LEA DX, MSG2
    MOV AH, 09H
    INT 21H

    ; --- Scenario 2: Subtraction with borrow ---
    LEA DX, MSG3
    MOV AH, 09H
    INT 21H

    MOV AX, NUM_C
    SUB AX, NUM_D   ; Subtract NUM_D from NUM_C.
    ; After this, Carry Flag (CF) is 1 because 1000 < 3000 (borrow needed).
    ; The result in AX will be the 2's complement representation of -2000.
    
    CALL PRINT_NUM  ; Print the result
    
    LEA DX, MSG4
    MOV AH, 09H
    INT 21H

    ; --- Exit the program ---
    MOV AH, 4CH
    INT 21H

MAIN ENDP
END MAIN
