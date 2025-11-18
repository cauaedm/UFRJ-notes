// Exemplo de violação de ordem em C
#include <stdio.h>
#include <pthread.h>

int x = 0, y = 0;
int r1 = 0, r2 = 0;

void* thread1(void* arg) {
    x = 1;
    r1 = y;
    return NULL;
}

void* thread2(void* arg) {
    y = 1;
    r2 = x;
    return NULL;
}

int main() {
    for (int i = 0; i < 100000; i++) {
        x = y = r1 = r2 = 0;
        pthread_t t1, t2;
        pthread_create(&t1, NULL, thread1, NULL);
        pthread_create(&t2, NULL, thread2, NULL);
        pthread_join(t1, NULL);
        pthread_join(t2, NULL);
        if (r1 == 0 && r2 == 0) {
            printf("Reordenação detectada na iteração %d!\n", i);
            break;
        }
    }
    return 0;
}
