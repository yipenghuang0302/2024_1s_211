#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

#define RESTOCK "RESTOCK"
#define SHOW_STOCK "SHOW_STOCK"
#define SALE "SALE"

// Author: @nate-blum

typedef struct HashNode {
    int count;
    char* album_name;
    struct HashNode* next;
} HashNode;

static HashNode** table = NULL;
static int table_fullness = 0, table_size = 4;

int hash(char* str) {
    unsigned long long hash = 0;
	int len = (int) strlen(str);
    for (int i = 0; i < len; i++)
        hash += str[i] * pow(31, len - (i + 1));
    return hash % table_size;
}

void pretty_print_table() {
	// Implement pretty printing of the hash tabled
	// based on the format of the answers
}

void resize() {
	// printf("Resizing the table from %d to %d\n", <first size>, <second size>);
	// Implement resize logic here
}

void update(char* album, int k) {
	// Implement update logic here
	// Remember to resize if necessary
	// printf("No stock of %s\n", album);
	// printf("Not enough stock of %s\n", album);
}

int retrieve(char* album_name) {
	// Implement retrieve logic here
	// Remember to account for non-existent searches (must return -1)
}

void free_table() {
	// Make sure to properly free your hash table
}

int main(int argc, char* argv[]) {
	FILE* fp = fopen(argv[1], "r");
    if (!fp) {
        perror("fopen failed");
        return EXIT_FAILURE;
    }

	if (!fscanf(fp, "%d\n", &table_size)) {
        perror("Reading the initial size of the table failed.\n");
        exit(EXIT_FAILURE);
    }

    char command[20], album[150];
	int count;
    while (fscanf(fp, "%s %d %[^\n]s", command, &count, album) == 3) {
		if (strcmp(command, SALE) == 0) {
			// *** //
		} else if (strcmp(command, RESTOCK) == 0) {
			// *** //
		} else if (strcmp(command, SHOW_STOCK) == 0) {
			//***//
			// printf("No stock of %s\n", album);
			// printf("Current stock of %s: %d\n", album, <stock>);
		}
    }

	pretty_print_table();
	free_table();
    return 0;
}