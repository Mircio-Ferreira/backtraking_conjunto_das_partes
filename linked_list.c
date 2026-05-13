#include "linked_list.h"

List *init_list(){

    List *list = malloc(sizeof(List));
    if(list == NULL) return NULL;
    list->head = NULL;
    list->tail = NULL;
    list->len = 0;

    return list;

}

void push(List *list , char letter){
    if(list == NULL) return;

    Node *new_node = (Node*) malloc(sizeof(Node));
    if(new_node == NULL) return;
    
    new_node->letter = letter;
    new_node->next = NULL;
    new_node->prev = NULL;
    
    if(list->head == NULL && list->tail == NULL){
        list->head = list->tail = new_node;
    }
    else{
        new_node->prev = list->tail;
        list->tail->next = new_node;
        list->tail=new_node;
    }
    list->len ++;
}

void pop(List *list){
    if(list == NULL || list->tail == NULL) return;

    if(list->head == list->tail){
        free(list->head);
        list->head = list->tail = NULL;
    }
    else{
        Node *temp = list->tail;
        list->tail = list->tail->prev;
        list->tail->next = NULL;
        free(temp);
    }
    list->len--;
}

void print_list(List *list){
    if(list == NULL) return;

    Node *temp = list->head;
    while(temp != NULL){
        printf("%c ",temp->letter);
        temp = temp->next;
    }
}