;Write a program to add two 8-bit BCD numbers

.MODEL SMALL
.STACK 100H
.DATA
    BCD_NUM1    DB 059H     ; Represents BCD 59
    BCD_NUM2    DB 035H     ; Represents BCD 35
    MSG1        DB '59 (BCD) + 35 (BCD) = ', '$'
    RESULT      DB ?

.CODE
MAIN PROC
    ; Initialize Data Segment
    MOV AX, @DATA
    MOV DS, AX

    ; --- Print message ---
    LEA DX, MSG1
    MOV AH, 09H
    INT 21H

    ; --- Perform BCD Addition ---
    MOV AL, BCD_NUM1    ; Load the first BCD number into AL
    ADD AL, BCD_NUM2    ; Add the second BCD number
    
    ; Decimal Adjust after Addition
    ; DAA instruction corrects the result of an addition to be a valid BCD number.
    ; For 59H + 35H = 8EH, DAA will correct it to 94H and set Carry Flag.
    DAA
    
    MOV RESULT, AL      ; Store the BCD result

    ; --- Print the BCD Result ---
    ; The result may have a carry. We print "1" if Carry Flag is set.
    JNC NO_CARRY        ; Jump if No Carry
    MOV DL, '1'         ; If carry, print '1' for the hundreds place
    MOV AH, 02H
    INT 21H

NO_CARRY:
    ; Print the higher digit (tens place)
    MOV DL, RESULT      ; Load the result
    AND DL, 0F0H        ; Isolate the high nibble
    MOV CL, 4           ; Set shift count to 4
    SHR DL, CL          ; Shift right by 4 bits
    ADD DL, '0'         ; Convert to ASCII character
    MOV AH, 02H         ; Function to print a character
    INT 21H

    ; Print the lower digit (ones place)
    MOV DL, RESULT      ; Reload the result
    AND DL, 0FH         ; Isolate the low nibble
    ADD DL, '0'         ; Convert to ASCII character
    MOV AH, 02H         ; Function to print a character
    INT 21H

    ; --- Exit the program ---
    MOV AH, 4CH
    INT 21H

MAIN ENDP
END MAIN
