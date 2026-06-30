#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>

void handler(int sig) {
    printf("\nCaught signal %d — cleaning up and exiting gracefully.\n", sig);
    exit(0);
}

int main(void) {
    signal(SIGINT, handler);
    signal(SIGTERM, handler);

    printf("signal_demo running. PID=%d. Send SIGINT (Ctrl+C) or SIGTERM to stop.\n", getpid());

    while (1) {
        printf("Working...\n");
        sleep(2);
    }

    return 0;
}