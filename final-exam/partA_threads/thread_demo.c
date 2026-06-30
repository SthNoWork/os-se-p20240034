#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>

#define NUM_THREADS 3
#define NUM_EXTRA_THREADS 1

void *worker(void *arg) {
    int id = *(int *)arg;
    int computed = (id + 1) * (id + 1);
    sleep(5);

    printf("Worker thread id=%d (pthread_self=%lu) computed value=%d\n",
           id, (unsigned long)pthread_self(), computed);
    fflush(stdout);

    int *result = malloc(sizeof(int));
    *result = computed;
    return (void *)result;
}

void *extra_worker(void *arg) {
    int id = *(int *)arg;
    printf("EXTRA worker id=%d (pthread_self=%lu) starting, PID=%d\n",
           id, (unsigned long)pthread_self(), getpid());
    fflush(stdout);
    sleep(15);
    printf("EXTRA worker id=%d finishing.\n", id);
    fflush(stdout);
    return NULL;
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

    printf("\n--- Summary (original %d workers) ---\n", NUM_THREADS);
    for (int i = 0; i < NUM_THREADS; i++) {
        printf("Thread %d returned %d\n", i, collected[i]);
    }
    fflush(stdout);

    pthread_t extra_tid[NUM_EXTRA_THREADS];
    int extra_ids[NUM_EXTRA_THREADS] = {100};

    printf("\nSpawning %d extra worker(s) now that originals are done...\n", NUM_EXTRA_THREADS);
    fflush(stdout);
    for (int i = 0; i < NUM_EXTRA_THREADS; i++) {
        pthread_create(&extra_tid[i], NULL, extra_worker, &extra_ids[i]);
    }

    for (int i = 0; i < NUM_EXTRA_THREADS; i++) {
        pthread_join(extra_tid[i], NULL);
    }

    printf("Extra worker(s) joined. Program exiting.\n");
    fflush(stdout);

    return 0;
}
