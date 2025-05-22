#include <stdio.h>
#include <math.h>
void display(int a) {
    printf("Hello world");
}

int conv(int a) {
    return pow(a,2);
}

int run_10m() {
    for (int i = 0; i < 10000000; i++) {
        conv(i);
    }
}
