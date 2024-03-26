#include <stdio.h>

// Recursive popcount

long pcount_r (
  unsigned long x
) {
  return x==0 ? 0 : (0b1&x) + pcount_r(x>>1);
}

int main () {
  printf("%ld\n",pcount_r(12903714));
  return 0;
}
