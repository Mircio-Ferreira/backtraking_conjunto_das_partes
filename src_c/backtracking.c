#include "backtracking.h"

void backtrack(char *alphabet, int idx, int n, List *list){

    if(idx == n){
        //print_list(list);
        return;
    }
      
    push(list, alphabet[idx]);

    backtrack(alphabet, idx+1 , n , list); // include current letter

    pop(list);

    backtrack(alphabet, idx+1 , n , list); // dont include current letter

}