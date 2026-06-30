#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>

#define NUM_THREADS 3

void *worker(void *arg) {
    int id = *(int *)arg;
    int computed = (id + 1) * (id + 1);
    sleep(15);

    printf("Worker thread id=%d (pthread_self=%lu) computed value=%d\n",
           id, (unsigned long)pthread_self(), computed);

    int *result = malloc(sizeof(int));
    *result = computed;
    return (void *)result;
}

int main(void) {
    pthread_t tid[NUM_THREADS];
    int ids[NUM_THREADS] = {0, 1, 2};
    int collected[NUM_THREADS];

    for (int i = 0; i < NUM_THREADS; i++) {
        if (pthread_create(&tid[i], NULL, worker, &ids[i]) != 0) {
            perror("pthread_create failed");
            exit(1);
        }
    }

    for (int i = 0; i < NUM_THREADS; i++) {
        void *res;
        pthread_join(tid[i], &res);
        collected[i] = *(int *)res;
        free(res);
    }

    printf("\n--- Summary ---\n");
    for (int i = 0; i < NUM_THREADS; i++) {
        printf("Thread %d returned %d\n", i, collected[i]);
    }

    return 0;
}
