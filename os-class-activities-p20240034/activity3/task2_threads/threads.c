#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

#define NUM_THREADS 5
#define NUM_INCREMENTS 100000

int counter = 0;

void *increment(void *arg) {
    int id = *(int *)arg;
    for (int i = 0; i < NUM_INCREMENTS; i++) {
        counter++;
    }
    printf("Thread %d done. Counter so far: %d\n", id, counter);
    return NULL;
}

int main() {
    pthread_t threads[NUM_THREADS];
    int ids[NUM_THREADS];

    printf("Starting without mutex — expect race condition\n");
    printf("Expected final counter: %d\n", NUM_THREADS * NUM_INCREMENTS);

    for (int i = 0; i < NUM_THREADS; i++) {
        ids[i] = i;
        pthread_create(&threads[i], NULL, increment, &ids[i]);
    }
    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }

    printf("Final counter (no mutex): %d\n", counter);
    return 0;
}
