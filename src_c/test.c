#include <time.h>
#include <windows.h>
#include "linked_list.h"
#include "backtracking.h"
#include "file.h"

void test(int len ,char *alphabet,char *file_name){

    LARGE_INTEGER star, end , frequency;

    QueryPerformanceFrequency(&frequency);

    List *list = init_list();

    QueryPerformanceCounter(&star);

    backtrack(alphabet , 0 , len , list);

    QueryPerformanceCounter(&end);

    long long dif_ticker = end.QuadPart - star.QuadPart;

    double seconds =(double)dif_ticker/ frequency.QuadPart;

    //printf("len set %d time: %.9f\n",len,seconds);

    write_file(file_name,len,seconds);

    free(list);
}