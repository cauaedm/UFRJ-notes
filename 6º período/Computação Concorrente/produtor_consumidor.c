// Exemplo do problema produtor-consumidor usando apenas pthread.h
#include <stdio.h>
#include <pthread.h>
#define TAM_BUFFER 5

int buffer[TAM_BUFFER];
int in = 0, out = 0, count = 0;
pthread_mutex_t mutex;
pthread_cond_t cheio, vazio;

void* produtor(void* arg) {
    for (int i = 0; i < 10; i++) {
        pthread_mutex_lock(&mutex);
        while (count == TAM_BUFFER)
            pthread_cond_wait(&vazio, &mutex);
        buffer[in] = i;
        printf("Produzido: %d\n", i);
        in = (in + 1) % TAM_BUFFER;
        count++;
        pthread_cond_signal(&cheio);
        pthread_mutex_unlock(&mutex);
    }
    return NULL;
}

void* consumidor(void* arg) {
    for (int i = 0; i < 10; i++) {
        pthread_mutex_lock(&mutex);
        while (count == 0)
            pthread_cond_wait(&cheio, &mutex);
        int item = buffer[out];
        printf("Consumido: %d\n", item);
        out = (out + 1) % TAM_BUFFER;
        count--;
        pthread_cond_signal(&vazio);
        pthread_mutex_unlock(&mutex);
    }
    return NULL;
}

int main() {
    pthread_t prod, cons;
    pthread_mutex_init(&mutex, NULL);
    pthread_cond_init(&cheio, NULL);
    pthread_cond_init(&vazio, NULL);

    pthread_create(&prod, NULL, produtor, NULL);
    pthread_create(&cons, NULL, consumidor, NULL);

    pthread_join(prod, NULL);
    pthread_join(cons, NULL);

    pthread_mutex_destroy(&mutex);
    pthread_cond_destroy(&cheio);
    pthread_cond_destroy(&vazio);
    return 0;
}
