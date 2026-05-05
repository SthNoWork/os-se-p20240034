#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int counter = 0;

int main() {
    printf("Parent PID: %d\n", getpid());
    counter = 10;

    pid_t pid = fork();

    if (pid < 0) {
        perror("fork failed");
        exit(1);
    }

    if (pid == 0) {
        printf("Child PID: %d, Parent PID: %d\n", getpid(), getppid());
        counter += 5;
        printf("Child counter: %d\n", counter);
        exit(0);
    } else {
        wait(NULL);
        printf("Parent counter (unchanged): %d\n", counter);
        printf("Parent done.\n");
    }

    return 0;
}
