#include <stdlib.h>
#include <stdio.h>
#include <string.h>

size_t min ( size_t x, size_t y ) {
    return x<y ? x : y;
}

size_t levenshtein_recursive ( char* source, char* target ) {

    // printf( "source=%s\n", source );
    // printf( "target=%s\n", target );

    if (strlen(source)==0) return strlen(target);
    else if (strlen(target)==0) return strlen(source);
    else if (source[0]==target[0]) return levenshtein_recursive (source+1, target+1);
    else {
        size_t ins = levenshtein_recursive (source+1, target  );
        size_t del = levenshtein_recursive (source,   target+1);
        size_t sub = levenshtein_recursive (source+1, target+1);
        return 1 + min( min(ins,del), sub );
    }

}

int main(int argc, char* argv[])
{

    FILE* inputFile = fopen(argv[1], "r");
    if (!inputFile) {
        perror("fopen failed");
        return EXIT_FAILURE;
    }

    char source[32];
    char target[32];

    fscanf (inputFile, "%s\n%s", source, target);

    printf("%ld\n", levenshtein_recursive ( source, target ));

    return EXIT_SUCCESS;

}
