org 100h
.model small ;
.data   
msg1 db "Emter your name : $"   
msg2 db 10,13, "Your name is : $"
.code
start:
mov ax,@data
mov ds,ax

mov dx,offset msg1
mov ah,09h

int 21h
mov ah,1h   

int 21h
mov bl,al

mov dx,offset msg2
mov ah,09h  

int 21h
mov ah,1h   

int 21h
mov dl,bl   

mov ah,02h
int 21h     

mov ah,4ch

ret