#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>
#include <assert.h>
#include "matMul.h"

int main(int argc, char* argv[])
{

    // Get matrix A
    FILE* matrix_a_fp = fopen(argv[1], "r");
    if (!matrix_a_fp) {
        perror("fopen failed");
        return EXIT_FAILURE;
    }

    unsigned int length_l, length_m;
    if (!fscanf(matrix_a_fp, "%d %d", &length_l, &length_m)) {
        perror("reading the row and column dimensions of matrix A failed");
        exit(EXIT_FAILURE);
    }

    int** matrix_a = calloc( length_l, sizeof(int*) );
    for ( unsigned int i=0; i<length_l; i++ ) {
        matrix_a[i] = calloc( length_m, sizeof(int) );
        for ( unsigned int j=0; j<length_m; j++ ) {
            int element;
            if (!fscanf(matrix_a_fp, "%d", &element)) {
                perror("reading the elements of matrix A failed");
                exit(EXIT_FAILURE);
            }
            matrix_a[i][j] = element;
        }
    }

    fclose(matrix_a_fp);

    // Get matrix B
    FILE* matrix_b_fp = fopen(argv[2], "r");
    if (!matrix_b_fp) {
        perror("fopen failed");
        return EXIT_FAILURE;
    }

    unsigned int temp, length_n;
    if (!fscanf(matrix_b_fp, "%d %d", &temp, &length_n)) {
        perror("reading the row and column dimensions of matrix B failed");
        exit(EXIT_FAILURE);
    }
    assert ( temp == length_m );

    int** matrix_b = calloc( length_m, sizeof(int*) );
    for ( unsigned int j=0; j<length_m; j++ ) {
        matrix_b[j] = calloc( length_n, sizeof(int) );
        for ( unsigned int k=0; k<length_n; k++ ) {
            int element;
            if (!fscanf(matrix_b_fp, "%d", &element)) {
                perror("reading the elements of matrix B failed");
                exit(EXIT_FAILURE);
            }
            matrix_b[j][k] = element;
        }
    }

    fclose(matrix_b_fp);

    // Malloc the memory space for the matMulProduct
    int** matMulProduct = calloc( length_l, sizeof(int*) );
    for ( unsigned int i=0; i<length_l; i++ ) {
        matMulProduct[i] = calloc( length_n, sizeof(int) );
    }

    matMul ( length_l, length_m, length_n, matrix_a, matrix_b, matMulProduct );
    for ( unsigned int i=0; i<length_l; i++ ) {
        for ( unsigned int k=0; k<length_n; k++ ) {
            printf ("%d ", matMulProduct[i][k]);
        }
        printf ("\n");
    }

    for ( unsigned int i=0; i<length_l; i++ ) {
        free( matMulProduct[i] );
    }
    free( matMulProduct );

    for ( unsigned int j=0; j<length_m; j++ ) {
        free( matrix_b[j] );
    }
    free( matrix_b );

    for ( unsigned int i=0; i<length_l; i++ ) {
        free( matrix_a[i] );
    }
    free( matrix_a );

    return 0;

}
