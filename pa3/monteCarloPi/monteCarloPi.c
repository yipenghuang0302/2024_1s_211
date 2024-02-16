// Authors:
// Eshaan Gandhi @eshaang2000
// Yipeng Huang @yipenghuang0302

#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <float.h>
#include <math.h>

double fabs (double value) {
    return value<0.0 ? -value : value;
}

int main(int argc, char *argv[]) {

    FILE* fp = fopen(argv[1], "r");
    if (!fp) {
        perror("fopen failed");
        return EXIT_FAILURE;
    }

    srand(time(NULL));
    // The problem we are trying to solve is:
    // Find PI
    // PI needs to be found such that PI is within the answer value specified by precision.

    double precision;
    fscanf(fp, "%lf", &precision);

    double estimated_pi = 0.0;
    double error = DBL_MAX;

    size_t inside = 0;
    size_t total = 0;

    while ( precision<fabs(error) ) {

        // generate a uniformly distributed pseudo-random number between 0.0 and 1.0.
        double x = (double)rand() / RAND_MAX;
        double y = rand() / (double)RAND_MAX;

        // find distance from origin
        double distance = sqrt( x*x + y*y );

        // if point within the unit quarter circle in the first quadrant
        if ( distance < 1. ) {
            inside++;
        }
        total++;

        estimated_pi = 4.0 * inside / total;
        // estimated_pi = 4.0 * ((double) inside) / ((double) total);

        // printf("inside=%ld, total=%ld, estimated_pi=%f\n", inside, total, estimated_pi);

        error = estimated_pi-M_PI;

    }

    printf("%.12f\n", estimated_pi); // print with enhanced precision

    return EXIT_SUCCESS;

}
