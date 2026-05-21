#include <stdlib.h>
#include "test.h"
#include "macro.h"
#include "file.h"

#define FILE_NAME_SMALL "case_tests/SMALL_TEST"
#define FILE_NAME_MIDDLE "case_tests/MIDDLE_TEST"
#define FILE_NAME_BIG "case_tests/BIG_TEST"

int main(){

    char alphabet[30];
    int n = 30;

    
    eraser_test_file(FILE_NAME_SMALL);
    eraser_test_file(FILE_NAME_MIDDLE);
    eraser_test_file(FILE_NAME_BIG);
    
    for (int i = 0; i < n; i++) alphabet[i] = 'A' + i;

    for(int i = 0; i < LEN_TEST; i++){
        test(SMALL ,alphabet,FILE_NAME_SMALL);
        test(MIDDLE ,alphabet,FILE_NAME_MIDDLE);
        test(BIG ,alphabet,FILE_NAME_BIG);
    }


    return 0;
}