#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <assert.h>

#define M 256
#define N 256

/* Markers used to bound trace regions of interest */
volatile char MARKER_START, MARKER_END;

short sumArrayRows (
    short a[M][N]
) {
    short sum = 0;

    MARKER_START = 211;
    for ( int i=0; i<M; i++ )
        for ( int j=0; j<N; j++ ) {
            // printf( "a[i][j]=%d\n", a[i][j] );
            sum += a[i][j];
        }
    MARKER_END = 211;

    // printf( "sumArrayRows sum=%d\n", sum );
    return sum;
}

short sumArrayCols (
    short a[M][N]
) {
    short sum = 0;

    MARKER_START = 211;
    for ( int j=0; j<N; j++ )
        for ( int i=0; i<M; i++ )
            sum += a[i][j];
    MARKER_END = 211;

    // printf( "sumArrayCols sum=%d\n", sum );
    return sum;
}

int main(int argc, char* argv[])
{

    // prepare random number generator
    time_t t;
    srand((unsigned) time(&t));

    // prepare timing infrastructure
    clock_t start, end;
    double cpu_time_used;

    /* Record marker addresses */
    FILE* marker_fp = fopen(".marker","w");
    assert(marker_fp);
    fprintf(marker_fp, "%llx\n%llx",
        (unsigned long long int) &MARKER_START,
        (unsigned long long int) &MARKER_END );
    fclose(marker_fp);

    short a[M][N];
    // INITIALIZE ARRAY WITH RANDOM NUMBERS
    for ( int i=0; i<M; i++ )
        for ( int j=0; j<N; j++ )
            a[i][j] = rand() % 256;

    // TIME sumArrayRows
    start = clock();
    int sumArrayRowsResult = sumArrayRows(a);
    end = clock();
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    printf("sumArrayRows took %lf seconds.\n", cpu_time_used);

    // TIME sumArrayCols
    start = clock();
    int sumArrayColsResult = sumArrayCols(a);
    end = clock();
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    printf("sumArrayCols took %lf seconds.\n", cpu_time_used);

    assert ( sumArrayRowsResult == sumArrayColsResult );

    exit(EXIT_SUCCESS);

}