#ifndef linked_list   
#define linked_list

#include <stdio.h>
#include <stdlib.h>

typedef struct Node{
    char letter;
    struct Node *next;
    struct Node *prev;
}Node;

typedef struct List{
    Node *head;
    Node *tail;
    int len;
}List;

List *init_list();

void push(List *list , char letter);
void pop(List *list);
void print_list(List *list);




#endif
