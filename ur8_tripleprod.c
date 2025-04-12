#include <stddef.h>  // for size_t

float tripleprod(float x[], float y[], float z[], int n) {
    float sum = 0.0;
    size_t i;

    // Main loop unrolled by a factor of 8
    for (i = 0; i < n; i += 8) {
        sum += x[i] * y[i] * z[i];
        sum += x[i+1] * y[i+1] * z[i+1];
        sum += x[i+2] * y[i+2] * z[i+2];
        sum += x[i+3] * y[i+3] * z[i+3];
        sum += x[i+4] * y[i+4] * z[i+4];
        sum += x[i+5] * y[i+5] * z[i+5];
        sum += x[i+6] * y[i+6] * z[i+6];
        sum += x[i+7] * y[i+7] * z[i+7];
    }

    return sum;
}

