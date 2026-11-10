#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#if defined(_WIN32) || defined(_WIN64)
#include <process.h>
#include <windows.h>
#else
#include <sys/wait.h>
#endif

int main() {
    pid_t pid = fork();

    if (pid == 0) {
        // Child process
        while(1) {
            printf("Child running...\n");
            sleep(1);
        }
    } else {
        // Parent process
        sleep(3); // কিছুক্ষণ অপেক্ষা করো
        printf("Parent: Sending SIGKILL to child...\n");
        kill(pid, SIGKILL); // Child কে জোর করে terminate করো
    #if defined(_WIN32) || defined(_WIN64)
        int status;
        _cwait(&status, pid, 0); // wait for child on Windows (MinGW)
    #else
        wait(NULL); // Child শেষ হওয়া পর্যন্ত অপেক্ষা করো
    #endif
        printf("Parent: Child terminated.\n");
    }
    return 0;
}
