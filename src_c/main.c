#include <stdlib.h>
#include "test.h"
#include "macro.h"
#include "file.h"


int main(){

    char alphabet[30];
    int n = 30;
    
    for (int i = 0; i < n; i++) alphabet[i] = 'A' + i;

    eraser_test_file(FILE_NAME_SMALL);
    eraser_test_file(FILE_NAME_MIDDLE);
    eraser_test_file(FILE_NAME_BIG);

    for(int i = 0; i < LEN_TEST; i++){
        test(SMALL ,alphabet,FILE_NAME_SMALL);
    }

    for(int i = 0; i < LEN_TEST; i++){
        test(MIDDLE ,alphabet,FILE_NAME_MIDDLE);
    }

    for(int i = 0; i < LEN_TEST; i++){
        test(BIG ,alphabet,FILE_NAME_BIG);
    }


    return 0;
}