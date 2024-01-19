#include <stdlib.h>
#include <stdio.h>
// https://www.tutorialspoint.com/c_standard_library/limits_h.htm
#include <limits.h>

int main () {

    printf("sizeof(char) = %ld byte\n", sizeof(char));
    for (size_t i=0; i<UCHAR_MAX; i++) {
        printf("(char) %ld = %c\n", i, (char) i);
    }

    return(EXIT_SUCCESS);
}
