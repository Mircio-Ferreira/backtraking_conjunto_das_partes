#include "linked_list.h"
#include "backtracking.h"
#include <stdlib.h>

#define len_conjunto 5

int main(){

    char alphabet[26];
    int n = 26;

    for (int i = 0; i < n; i++) alphabet[i] = 'A' + i;

    List *list = init_list();

    backtrack(alphabet , 0 , len_conjunto , list);


    return 0;
}