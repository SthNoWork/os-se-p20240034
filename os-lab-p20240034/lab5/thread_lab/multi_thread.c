#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

#define NUM_THREADS 4

int shared_counter = 0;
pthread_mutex_t lock;

void *thread_func(void *arg) {
    int id = *(int *)arg;

    pthread_mutex_lock(&lock);
    shared_counter++;
    printf("Thread %d: shared_counter = %d\n", id, shared_counter);
    pthread_mutex_unlock(&lock);

    return NULL;
}

int main() {
    pthread_t threads[NUM_THREADS];
    int ids[NUM_THREADS];

    pthread_mutex_init(&lock, NULL);

    for (int i = 0; i < NUM_THREADS; i++) {
        ids[i] = i + 1;
        pthread_create(&threads[i], NULL, thread_func, &ids[i]);
    }

    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }

    printf("Final shared_counter: %d\n", shared_counter);
    pthread_mutex_destroy(&lock);
    return 0;
}
