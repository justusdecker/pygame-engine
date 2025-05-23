#include <stdio.h>
#include <stdlib.h>
unsigned char *ColorTest(float scale, unsigned char* pxarr,int size) {
    
    unsigned char *pixel_array = malloc(sizeof(pxarr));
    printf("%d",size);
    for (unsigned int x = 0; x <= 255; x++) {

        for (unsigned int y = 0; y <= 15; y++) {

            for (unsigned int z = 0; z < 3; z++) {
                
                //this line here is faulty VVV
                //printf("%d",(unsigned char)(pxarr[(x*16+y) * 3] * scale));
                //pixel_array[(x*16+y) * 3] = 
                
            }
            
        }
    }
    return pixel_array;
}