#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <xmmintrin.h> // SSE

#define N 1000000

float A[N], B[N], C[N];

void inicializar_vectores() {
    for (int i = 0; i < N; i++) {
        A[i] = (float)i;
        B[i] = (float)(2 * i);
    }
}

void suma_secuencial() {
    for (int i = 0; i < N; i++) {
        C[i] = A[i] + B[i];
    }
}

void suma_simd_sse() {
    for (int i = 0; i < N; i += 4) {
        __m128 va = _mm_loadu_ps(&A[i]);
        __m128 vb = _mm_loadu_ps(&B[i]);
        __m128 vc = _mm_add_ps(va, vb);
        _mm_storeu_ps(&C[i], vc);
    }
}

int main() {
    clock_t start, end;
    double tiempo_secuencial, tiempo_simd;

    printf("Iniciando vectores\n");
    inicializar_vectores();

    printf("Iniciando suma secuencial\n");
    start = clock();
    suma_secuencial();
    end = clock();
    tiempo_secuencial = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Tiempo suma secuencial: %.5f segundos\n", tiempo_secuencial);

    printf("Iniciando suma SIMD con SSE...\n");
    start = clock();
    suma_simd_sse();
    end = clock();  

    tiempo_simd = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Tiempo suma SIMD (SSE): %.5f segundos\n", tiempo_simd);

    printf("Aceleracion SIMD: %.2fx\n", tiempo_secuencial / tiempo_simd);
    return 0;
}

