#include <stddef.h>  

float tripleprod(float x[], float y[], float z[], int n) {
    float sum0 = 0.0, sum1 = 0.0, sum2 = 0.0, sum3 = 0.0;
    float sum4 = 0.0, sum5 = 0.0, sum6 = 0.0, sum7 = 0.0;
    size_t i;


    for (i = 0; i < n; i += 8) {
        sum0 += x[i] * y[i] * z[i];
        sum1 += x[i+1] * y[i+1] * z[i+1];
        sum2 += x[i+2] * y[i+2] * z[i+2];
        sum3 += x[i+3] * y[i+3] * z[i+3];
        sum4 += x[i+4] * y[i+4] * z[i+4];
        sum5 += x[i+5] * y[i+5] * z[i+5];
        sum6 += x[i+6] * y[i+6] * z[i+6];
        sum7 += x[i+7] * y[i+7] * z[i+7];
    }


    return sum0 + sum1 + sum2 + sum3 + sum4 + sum5 + sum6 + sum7;
}

