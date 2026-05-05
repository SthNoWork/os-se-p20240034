#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

int shared_counter = 0;

void *thread_func(void *arg) {
    int id = *(int *)arg;
    printf("Thread %d started, PID: %d\n", id, getpid());
    shared_counter++;
    printf("Thread %d: shared_counter = %d\n", id, shared_counter);
    return NULL;
}

int main() {
    const int NUM_THREADS = 3;
    pthread_t threads[NUM_THREADS];
    int ids[NUM_THREADS];

    printf("Main thread PID: %d\n", getpid());

    for (int i = 0; i < NUM_THREADS; i++) {
        ids[i] = i + 1;
        pthread_create(&threads[i], NULL, thread_func, &ids[i]);
    }

    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }

    printf("Final shared_counter: %d\n", shared_counter);
    printf("Main thread done.\n");
    return 0;
}
