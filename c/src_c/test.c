#include <stdio.h>
#include <time.h>
#include "linked_list.h"
#include "backtracking.h"
#include "file.h"

void test(int len ,char *alphabet,char *file_name){

    clock_t start, end;

    List *list = init_list();

    start = clock();

    
    backtrack(alphabet , 0 , len , list);

    end = clock();

    double seconds = (double)(end - start) / CLOCKS_PER_SEC;

    write_file(file_name,len,seconds);

    free(list);
}
