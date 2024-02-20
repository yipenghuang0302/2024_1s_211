#include "../bstLevelOrder/bst.h"


// A program to perform a REVERSE ORDER (DEPTH-FIRST) TRAVERSAL of a binary search tree

void depth_first ( struct BSTNode* root ) {
    if(root!=NULL) // checking if the root is not null
    {
        depth_first(root->r_child);// visiting right child
        printf(" %d ", root->key); // printing data at root
        depth_first(root->l_child); // visiting left child
    }
}

int main ( int argc, char* argv[] ) {

    // READ INPUT FILE TO CREATE BINARY SEARCH TREE
    FILE* fp = fopen(argv[1], "r");
    if (!fp) {
        perror("fopen failed");
        return EXIT_FAILURE;
    }
    BSTNode* root = NULL;
    int key;
    while ( fscanf(fp, "%d", &key)!=EOF ) {
        root = insert (root, key);
    }
    fclose(fp);

    depth_first(root);

    delete_bst(root);
    return EXIT_SUCCESS;
}
