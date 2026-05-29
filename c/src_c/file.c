#include <stdio.h>
#include <string.h>
#include "macro.h"

void write_file(const char *filename, int len, double seconds) {

    FILE *file;


    file = fopen(filename, "a");

    if (file == NULL) {
        printf("Erro ao abrir arquivo\n");
        return;
    }

    fprintf(file, "len set %d time: %.9f\n", len, seconds);

    fclose(file);
}

void eraser_test_file(const char *filename){
    if(FLAG_ERASER_TEST == 1){

        FILE *file = fopen(filename, "w");

        if (file == NULL) {
            printf("Erro ao abrir arquivo\n");
            return;
        }

        fclose(file);
    }
}
