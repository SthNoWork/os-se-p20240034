#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <signal.h>
#include <unistd.h>

volatile int running = 1;

void handle_sigint(int sig) {
    printf("\nCaught signal %d (SIGINT), shutting down...\n", sig);
    running = 0;
}

void *worker(void *arg) {
    int id = *(int *)arg;
    while (running) {
        printf("Thread %d: working...\n", id);
        sleep(1);
    }
    printf("Thread %d: exiting.\n", id);
    return NULL;
}

int main() {
    signal(SIGINT, handle_sigint);

    const int NUM_THREADS = 2;
    pthread_t threads[NUM_THREADS];
    int ids[NUM_THREADS];

    for (int i = 0; i < NUM_THREADS; i++) {
        ids[i] = i + 1;
        pthread_create(&threads[i], NULL, worker, &ids[i]);
    }

    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }

    printf("Main: all threads stopped.\n");
    return 0;
}
