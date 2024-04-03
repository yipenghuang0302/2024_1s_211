#include <stddef.h>
#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include <complex.h>

/* Markers used to bound trace regions of interest */
volatile char MARKER_START, MARKER_END;

// Cache oblivious matrix transpose
// https://en.wikipedia.org/wiki/Cache-oblivious_algorithm
void recursiveMatTrans (
    size_t global_n,
    size_t n,
    complex* A, size_t offset_row_A, size_t offset_col_A,
    complex* B, size_t offset_row_B, size_t offset_col_B
) {

    if (n<=32) { // base case
        for ( size_t i=0; i<n; i++ ) {
            for ( size_t j=0; j<n; j++ ) {
                B[ (offset_row_B+j)*global_n + offset_col_B+i ] = conj(A[ (offset_row_A+i)*global_n + offset_col_A+j ]);
            }
        }
    } else { // recursive case
        /* ... */
    }
}

int main(int argc, char* argv[])
{

    /* Record marker addresses */
    FILE* marker_fp = fopen(".marker","w");
    assert(marker_fp);
    fprintf(marker_fp, "%llx\n%llx",
        (unsigned long long int) &MARKER_START,
        (unsigned long long int) &MARKER_END );
    fclose(marker_fp);

    if (argc!=2) {
        printf("Usage: ./matTrans <matrix_a_file>\n");
        exit(EXIT_FAILURE);
    }

    FILE* matrix_a_fp = fopen(argv[1], "r");
    if (!matrix_a_fp) {
        perror("fopen failed");
        return EXIT_FAILURE;
    }
    size_t n;
    fscanf(matrix_a_fp, "%ld\n", &n);
    complex* a = calloc( n*n, sizeof(complex) );
    for ( size_t i=0; i<n; i++ ) {
        for ( size_t j=0; j<n; j++ ) {
            double real, imag;
            fscanf(matrix_a_fp, "(%lf%lfj) ", &real, &imag);
            a[i*n+j] = CMPLX(real, imag);
        }
        fscanf(matrix_a_fp, "\n");
    }
    fclose(matrix_a_fp);

    complex* b = calloc( n*n, sizeof(complex) );
    MARKER_START = 211;
    recursiveMatTrans ( n, n, a, 0, 0, b, 0, 0 );
    MARKER_END = 211;

    for ( size_t i=0; i<n; i++ ) {
        for ( size_t j=0; j<n; j++ ) {
            if (cimag(b[i*n+j])<0) {
                printf( "(%.12lf%.12lfj) ", creal(b[i*n+j]), cimag(b[i*n+j]) );
            } else {
                printf( "(%.12lf+%.12lfj) ", creal(b[i*n+j]), cimag(b[i*n+j]) );
            }
        }
        printf( "\n" );
    }

    free(b);
    free(a);
    exit(EXIT_SUCCESS);

}
