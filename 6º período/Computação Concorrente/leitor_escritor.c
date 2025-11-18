// Exemplo do problema leitor-escritor usando apenas pthread.h
#include <stdio.h>
#include <pthread.h>

int dados = 0;
int leitores = 0;
pthread_mutex_t mutex_leitor, mutex_escrita;

void* leitor(void* arg) {
    pthread_mutex_lock(&mutex_leitor);
    leitores++;
    if (leitores == 1)
        pthread_mutex_lock(&mutex_escrita);
    pthread_mutex_unlock(&mutex_leitor);

    printf("Leitor lendo: %d\n", dados);

    pthread_mutex_lock(&mutex_leitor);
    leitores--;
    if (leitores == 0)
        pthread_mutex_unlock(&mutex_escrita);
    pthread_mutex_unlock(&mutex_leitor);
    return NULL;
}

void* escritor(void* arg) {
    pthread_mutex_lock(&mutex_escrita);
    dados++;
    printf("Escritor escreveu: %d\n", dados);
    pthread_mutex_unlock(&mutex_escrita);
    return NULL;
}

int main() {
    pthread_t t[5];
    pthread_mutex_init(&mutex_leitor, NULL);
    pthread_mutex_init(&mutex_escrita, NULL);

    for (int i = 0; i < 3; i++)
        pthread_create(&t[i], NULL, leitor, NULL);
    for (int i = 3; i < 5; i++)
        pthread_create(&t[i], NULL, escritor, NULL);

    for (int i = 0; i < 5; i++)
        pthread_join(t[i], NULL);

    pthread_mutex_destroy(&mutex_leitor);
    pthread_mutex_destroy(&mutex_escrita);
    return 0;
}
