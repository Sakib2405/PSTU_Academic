;Write a program to print a message using individual letters and the ASCII code of letters.
 
 .MODEL SMALL
.STACK 100H
.DATA
    MSG1 DB 'Hello, World!', '$'
    MSG2 DB 72, 101, 108, 108, 111, 32, 65, 83, 67, 73, 73, '!', '$' ; "Hello ASCII!" in ASCII codes

.CODE
MAIN PROC
    ; Initialize Data Segment (DS)
    MOV AX, @DATA
    MOV DS, AX

    ; --- Print the first message using individual letters ---
    ; Load the effective address of MSG1 into DX
    LEA DX, MSG1
    ; Use DOS interrupt 21h, function 09h to print a string
    MOV AH, 09H
    INT 21H

    ; --- Print a newline character to separate the messages ---
    MOV AH, 02H     ; Function to print a character
    MOV DL, 10      ; ASCII for line feed
    INT 21H
    MOV DL, 13      ; ASCII for carriage return
    INT 21H

    ; --- Print the second message using ASCII codes ---
    ; Load the effective address of MSG2 into DX
    LEA DX, MSG2
    ; Use DOS interrupt 21h, function 09h again
    MOV AH, 09H
    INT 21H

    ; --- Exit the program ---
    ; Use DOS interrupt 21h, function 4Ch to terminate
    MOV AH, 4CH
    INT 21H

MAIN ENDP
END MAIN
