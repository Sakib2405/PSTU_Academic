;Write a program  to print a String 
 
.MODEL SMALL
.STACK 100H
.DATA
    MY_STRING DB 'This is a simple string printing program.', 10, 13, '$'

.CODE
MAIN PROC
    ; Initialize Data Segment (DS)
    ; This is a necessary step to access data defined in the .DATA segment.
    MOV AX, @DATA
    MOV DS, AX

    ; --- Print the String ---
    ; Load the effective address (offset) of MY_STRING into the DX register.
    ; DX must point to the string to be printed.
    LEA DX, MY_STRING

    ; Prepare for DOS interrupt by loading the function number into AH.
    ; Function 09h of INT 21h prints a string terminated by '$'.
    MOV AH, 09H

    ; Call the DOS interrupt to perform the print operation.
    INT 21H

    ; --- Exit the program ---
    ; Use function 4Ch of INT 21h to terminate the program gracefully.
    MOV AH, 4CH
    INT 21H

MAIN ENDP
END MAIN
