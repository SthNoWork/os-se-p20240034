#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <signal.h>
#include <unistd.h>

#define NUM_THREADS 3

volatile int running = 1;
pthread_mutex_t lock;
int shared_counter = 0;

void handle_sigint(int sig) {
    printf("\nCaught signal %d (SIGINT), initiating shutdown...\n", sig);
    running = 0;
}

void *worker(void *arg) {
    int id = *(int *)arg;

    while (running) {
        pthread_mutex_lock(&lock);
        shared_counter++;
        printf("Thread %d: counter = %d\n", id, shared_counter);
        pthread_mutex_unlock(&lock);
        sleep(1);
    }

    printf("Thread %d: shutting down gracefully.\n", id);
    return NULL;
}

int main() {
    signal(SIGINT, handle_sigint);
    pthread_mutex_init(&lock, NULL);

    pthread_t threads[NUM_THREADS];
    int ids[NUM_THREADS];

    printf("Main: starting %d threads. Press Ctrl+C to stop.\n", NUM_THREADS);

    for (int i = 0; i < NUM_THREADS; i++) {
        ids[i] = i + 1;
        pthread_create(&threads[i], NULL, worker, &ids[i]);
    }

    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }

    printf("Main: all threads exited. Final counter = %d\n", shared_counter);
    pthread_mutex_destroy(&lock);
    return 0;
}
