;Write a program to subtract two 8-bit BCD numbers
 
.MODEL SMALL
.STACK 100H
.DATA
    BCD_NUM1    DB 092H     ; Represents BCD 92
    BCD_NUM2    DB 038H     ; Represents BCD 38
    MSG1        DB '92 (BCD) - 38 (BCD) = ', '$'
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

    ; --- Perform BCD Subtraction ---
    MOV AL, BCD_NUM1    ; Load the first BCD number into AL
    SUB AL, BCD_NUM2    ; Subtract the second BCD number
    
    ; Decimal Adjust after Subtraction
    ; DAS instruction corrects the result of a subtraction to be a valid BCD number.
    DAS
    
    MOV RESULT, AL      ; Store the BCD result

    ; --- Print the BCD Result ---
    ; The result is in AL (e.g., for 92-38, AL will be 01010100B or 54H)
    ; We need to print it as two separate digits.

    MOV DL, AL          ; Copy result to DL for manipulation
    
    ; Print the higher digit (tens place)
    AND DL, 0F0H        ; Isolate the high nibble (e.g., 50H)
    MOV CL, 4           ; Set shift count to 4
    SHR DL, CL          ; Shift right by 4 bits (e.g., 05H)
    ADD DL, '0'         ; Convert to ASCII character '5'
    MOV AH, 02H         ; Function to print a character
    INT 21H

    ; Print the lower digit (ones place)
    MOV DL, RESULT      ; Reload the original result
    AND DL, 0FH         ; Isolate the low nibble (e.g., 04H)
    ADD DL, '0'         ; Convert to ASCII character '4'
    MOV AH, 02H         ; Function to print a character
    INT 21H

    ; --- Exit the program ---
    MOV AH, 4CH
    INT 21H

MAIN ENDP
END MAIN

