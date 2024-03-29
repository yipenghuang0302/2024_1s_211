#include <stdio.h>

struct element {
    int number;
    struct element* next;
};

struct element c = {3, NULL};
struct element b = {2, &c};
struct element a = {1, &b};

int access() {
  return a.next->number;
}

int main() {
  printf("%d\n", access());
  return 0;
}
