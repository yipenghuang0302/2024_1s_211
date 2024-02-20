#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>

// Author: Pedro Torres

size_t anyToInteger(char* source, int base, int digitCount) {
    // Implement logic to convert the source string to integer representation
    // Remember to return the integer value

    size_t repr = 0;

    /* ... */

    return repr;
}

void integerToAny(char* result, size_t repr, int base) {
    // Implement the logic to convert the represented value to any base
    // Store this value as a string in the 'result' array

    /* ... */

    return;
}

int main(int argc, char* argv[]) {
    FILE* fp = fopen(argv[1], "r");
    if (!fp) {
        perror("fopen failed");
        return EXIT_FAILURE;
    }

    int digitCount;
    int sourceBase;
    int destBase;

    if (!fscanf(fp, "%d\n", &digitCount)) {
      perror("reading the input digit count failed");
      exit(EXIT_FAILURE);
    }

    if (!fscanf(fp, "%d\n", &sourceBase)) {
      perror("reading the source base failed");
      exit(EXIT_FAILURE);
    }

    if (!fscanf(fp, "%d\n", &destBase)) {
      perror("reading the destination base failed");
      exit(EXIT_FAILURE);
    }

    char* sourceNum = calloc(sizeof(char), digitCount+1);

    if (!fscanf(fp, "%s\n", sourceNum)) {
      perror("reading the source number");
      exit(EXIT_FAILURE);
    }

    size_t repr;

    repr = anyToInteger(sourceNum, sourceBase, digitCount);

    // Size 65 accounts for the largest digit result (64 bit binary) + 1 null operator
    char* result = (char*)calloc(sizeof(char), 65);

    integerToAny(result, repr, destBase);

    // Print string
    /* ... */

    free(sourceNum);
    free(result);

    return EXIT_SUCCESS;
}
