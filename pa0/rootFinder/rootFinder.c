#include <stdlib.h>
#include <stdio.h>
#include <math.h>

int main(int argc, char* argv[]) {

  // Open the filename given as the first command line argument for reading
  FILE* fp = fopen(argv[1], "r");
  if (!fp) {
    perror("fopen failed");
    return EXIT_FAILURE;
  }

  char buf[256];

  char* string = fgets(buf, 256, fp);

  int square = atoi(string);

  int root = sqrt( square );

  if ( root*root == square ) {

    // Printing in C.
    // %d is the format specifier for integer numbers.
    // \n is the newline character
    printf( "%d\n", root );
    return EXIT_SUCCESS;

  } else {

    printf("square root not integer\n");

  }

}