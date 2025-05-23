#include <stdio.h>
#include <stdlib.h>
unsigned char *ColorTest(float scale, unsigned char* pxarr) {
    
    unsigned char *pixel_array = malloc(sizeof(*pxarr));
    for (unsigned int x = 0; x <= 255; x++) {

        for (unsigned int y = 0; y <= 15; y++) {

            for (unsigned int z = 0; z <= 3; z++) {

                printf("%d",z);
                pixel_array[(x*16+y) * 3] = (unsigned char)(pxarr[(x*16+y) * 3] * scale);

                
            }
            
        }
    }
    return pixel_array;
}