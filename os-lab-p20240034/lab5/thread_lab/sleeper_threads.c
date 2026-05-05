#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

void *sleeper(void *arg) {
    int id = *(int *)arg;
    printf("Thread %d: going to sleep...\n", id);
    sleep(id);
    printf("Thread %d: woke up after %d second(s)\n", id, id);
    return NULL;
}

int main() {
    const int NUM_THREADS = 4;
    pthread_t threads[NUM_THREADS];
    int ids[NUM_THREADS];

    for (int i = 0; i < NUM_THREADS; i++) {
        ids[i] = i + 1;
        pthread_create(&threads[i], NULL, sleeper, &ids[i]);
    }

    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }

    printf("All threads done.\n");
    return 0;
}
