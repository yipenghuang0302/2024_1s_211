#include <stdlib.h>
#include <stdio.h>

void immediate ( int * ptr ) {
  *ptr = 0x8000000;
}

void displacement_c ( char * ptr ) {
  ptr[3] = 0x80;
}
void displacement_s ( short * ptr ) {
  ptr[3] = 0x8000;
}
void displacement_i ( int * ptr ) {
  ptr[3] = 0x80000000;
}
void displacement_l ( long * ptr ) {
  ptr[3] = 0x8000000000000000;
}

void index_c ( char * ptr, long index ) {
  ptr[index] = 0xFF;
}
void index_s ( short * ptr, long index ) {
  ptr[index] = 0xFFFF;
}
void index_i ( int * ptr, long index ) {
  ptr[index] = 0xFFFFFFFF;
}
void index_l ( long * ptr, long index ) {
  ptr[index] = 0xFFFFFFFFFFFFFFFF;
}

void displacement_and_index ( long * ptr, long index ) {
  ptr[index+3] = 0xFFFFFFFFFFFFFFFF;
}

int main () {

  int a;
  immediate(&a);
  printf("a=%x\n",a);

  short int b[4];
  displacement_s(b);
  printf("b[3]=%x\n",b[3]);

  long c[4];
  index_l(c,3);
  printf("c[3]=%lx\n",c[3]);

  long d[4];
  displacement_and_index(d,1);
  printf("d[3]=%lx\n",d[3]);

  return EXIT_SUCCESS;
}
