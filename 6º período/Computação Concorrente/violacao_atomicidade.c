// Exemplo de violação de atomicidade em C
#include <stdio.h>
#include <pthread.h>

int contador = 0;

void* incrementa(void* arg) {
    for (int i = 0; i < 100000; i++) {
        contador++;
    }
    return NULL;
}

int main() {
    pthread_t t1, t2;
    pthread_create(&t1, NULL, incrementa, NULL);
    pthread_create(&t2, NULL, incrementa, NULL);

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    printf("Contador final: %d\n", contador);
    return 0;
}
