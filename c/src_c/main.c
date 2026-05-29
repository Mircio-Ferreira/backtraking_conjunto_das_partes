#include <stdlib.h>
#include <stdio.h>
#include "test.h"
#include "macro.h"
#include "file.h"

int main(){

    char alphabet[BIG];

    if(BIG < MIDDLE || BIG < SMALL){
        printf("ERRO: BIG CASES NEED TO BE BIGGER THAN MIDDLE OR SMALL");
        return 0;
    }
    
    for (int i = 0; i < BIG; i++) alphabet[i] = 'A' + i;

    eraser_test_file(FILE_NAME_SMALL);
    eraser_test_file(FILE_NAME_MIDDLE);
    eraser_test_file(FILE_NAME_BIG);

    printf("test star\n");

    for(int i = 0; i < LEN_TEST; i++){
        test(SMALL ,alphabet,FILE_NAME_SMALL);
    }

    printf("end small test\n");

    for(int i = 0; i < LEN_TEST; i++){
        test(MIDDLE ,alphabet,FILE_NAME_MIDDLE);
    }

    printf("end middle test\n");

    for(int i = 0; i < LEN_TEST; i++){
        test(BIG ,alphabet,FILE_NAME_BIG);
    }

    printf("end big test\n");

    return 0;
}
