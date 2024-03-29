#include <stdio.h>

int nested_array[3][5] = {
  {0,8,8,5,4},
  {0,8,9,0,1},
  {0,8,9,0,4}
};

int piscataway[5] =    {0,8,8,5,4};
int new_brunswick[5] = {0,8,9,0,1};
int highland_park[5] = {0,8,9,0,4};

int* multilevel_array[3] = {
  piscataway,
  new_brunswick,
  highland_park
};

int get_nested (int array[3][5], long row, long col) {
  return array[row][col];
}

int get_multilevel (int** array, long row, long col) {
  return array[row][col];
}

int main() {
  printf("%d\n", get_nested(nested_array,1,4));
  printf("%d\n", get_multilevel(multilevel_array,1,4));
  return 0;
}
