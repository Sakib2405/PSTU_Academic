#include <stdio.h>     // printf() ব্যবহার করার জন্য standard I/O header
#include <signal.h>    // signal handle করার জন্য header
#include <unistd.h>    // sleep() function এর জন্য header

// signal handler function
void handler(int sig) {
    printf("\nCtrl+C চাপা হয়েছে, কিন্তু আমি বন্ধ হচ্ছি না!\n");
}

int main() {
    signal(SIGINT, handler); // যখন Ctrl+C চাপা হবে, তখন handler() call হবে

    while(1) {               // infinite loop
        printf("Running...\n");
        sleep(2);            // প্রতি 2 সেকেন্ডে message print করবে
    }
}
