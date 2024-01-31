#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>
#include <assert.h>

void matMul (
    unsigned int l,
    unsigned int m,
    unsigned int n,
    int** matrix_a,
    int** matrix_b,
    int** matMulProduct
) {

    // printf("l=%d\n", l);
    // printf("m=%d\n", m);
    // printf("n=%d\n", n);

    for ( unsigned int i=0; i<l; i++ ) {
        // printf("i=%d\n", i);
        for ( unsigned int k=0; k<n; k++ ) {
            // printf("k=%d\n", k);
            matMulProduct[i][k] = 0;
            for ( unsigned int j=0; j<m; j++ ) {
                matMulProduct[i][k] += matrix_a[i][j] * matrix_b[j][k];
            }
        }
    }

}
