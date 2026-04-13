#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    int i;
    pid_t pid;

    for (i = 0; i < 3; i++) {
        pid = fork();
        if (pid == 0) {
            printf("Child %d (PID %d): sleeping...\n", i+1, getpid());
            sleep(30);
            exit(0);
        }
    }

    printf("Parent (PID %d): waiting for all children.\n", getpid());
    for (i = 0; i < 3; i++) wait(NULL);
    printf("Parent: all children done.\n");
    return 0;
}
