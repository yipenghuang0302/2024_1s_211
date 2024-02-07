#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "queue.h"


int main(int argc, char* argv[]) {

    FILE* fp = fopen(argv[1], "r");
    if (!fp) {
        perror("fopen failed");
        return EXIT_FAILURE;
    }

    Queue queue = { .front = NULL, .back = NULL };

    char buff[8];
    while ( fscanf(fp, "%s", buff) != -1 ) {

        if ( strcmp(buff,"ENQUEUE")==0 ) {
            fscanf(fp, "%s", buff);
            unsigned char* pointer = malloc( sizeof(unsigned char) );
            *pointer = atoi(buff);
            enqueue(&queue, pointer);
        } else if ( strcmp(buff,"DEQUEUE")==0 ) {
            void* pointer = dequeue(&queue); // discard the return
            free(pointer);
        } else {
            printf("UNEXPECTED INPUT\n");
            return EXIT_FAILURE;
        }
    }

    while (queue.front) {
        unsigned char* data = dequeue(&queue);
        printf( "%d\n", *data );
        free(data);
    }

    fclose(fp);
    return EXIT_SUCCESS;
}
