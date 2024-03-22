#include <stdlib.h>
#include <stdio.h>

long leaq_quiz_0 ( long ptr, long index ) {
  return ptr+8*index+24;
}

long * leaq_quiz_1 ( long * ptr, long index ) {
  return &ptr[index+3];
}

long * leaq_quiz_2 ( long * ptr, long index ) {
  return &ptr[index+24];
}

long * leaq_quiz_3 ( long * ptr, long index ) {
  return &ptr[8*index+3];
}

long leaq_quiz_4 ( long * ptr, long index ) {
  return ptr[index+3];
}

long * leaq ( long * ptr, long index ) {
  return &ptr[index+1];
}

long mulAdd ( long base, long index ) {
  return base+index*8+8;
}

int main () {

  long d[2];
  long * ptr = leaq(d,0);
  printf("ptr=%p\n",ptr);

  return EXIT_SUCCESS;
}
