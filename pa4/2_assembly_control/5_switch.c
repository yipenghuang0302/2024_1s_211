#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>

char hex_switch (
    char val
) {
  char hexChar = '\0';
  switch(val) {
      case 10 :
          hexChar = 'A';
          break;
      case 11 :
          hexChar = 'B';
          break;
      case 12 :
          hexChar = 'C';
          break;
      case 13 :
          hexChar = 'D';
          break;
      case 14 :
          hexChar = 'E';
          break;
      case 15 :
          hexChar = 'F';
          break;
      default :
          hexChar = val+'0';
  }
  return hexChar;
}

int main () {
    return EXIT_SUCCESS;
}
