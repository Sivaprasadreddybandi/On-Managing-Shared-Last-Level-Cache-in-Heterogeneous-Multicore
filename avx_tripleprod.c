#include <immintrin.h>  // include AVX intrinsics
#include <stddef.h>     // for size_t

float tripleprod(float x[], float y[], float z[], int n) {
    __m256 sumVec = _mm256_setzero_ps();  
    size_t i;

    for (i = 0; i < n; i += 8) {
        __m256 xVec = _mm256_load_ps(&x[i]);   
        __m256 yVec = _mm256_load_ps(&y[i]);   
        __m256 zVec = _mm256_load_ps(&z[i]);   
        __m256 prodVec = _mm256_mul_ps(xVec, yVec);
        prodVec = _mm256_mul_ps(prodVec, zVec);    

        sumVec = _mm256_add_ps(sumVec, prodVec);   
    }

    float sumArray[8];
    _mm256_store_ps(sumArray, sumVec);
    float sum = sumArray[0] + sumArray[1] + sumArray[2] + sumArray[3]
              + sumArray[4] + sumArray[5] + sumArray[6] + sumArray[7];

    return sum;
}

