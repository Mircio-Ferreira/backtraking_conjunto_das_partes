#include "linked_list.h"
#include "backtracking.h"
#include <stdlib.h>
#include <time.h>
#include <windows.h>

int main(){

    char alphabet[30];
    int n = 30;
    
    LARGE_INTEGER star, end , frequency;
    QueryPerformanceFrequency(&frequency);

    for (int i = 0; i < n; i++) alphabet[i] = 'A' + i;

    for(int i =0 ; i < n+1 ; i+=5){

        List *list = init_list();

        QueryPerformanceCounter(&star);

        backtrack(alphabet , 0 , i , list);

        QueryPerformanceCounter(&end);

        long long dif_ticker = end.QuadPart - star.QuadPart;

        double seconds =(double)dif_ticker/ frequency.QuadPart;

        printf("len set %d time: %.9f\n",i,seconds);

        free(list);
    }


    return 0;
}