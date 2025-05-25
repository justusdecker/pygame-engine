#include <stdio.h>
#include <stdlib.h>
unsigned char *GammaCorrection(float scale, unsigned char* pxarr,int size) {
    
    unsigned char *pixel_array = malloc(size);
    for (unsigned int x = 0; x <= 255; x++) {

        for (unsigned int y = 0; y <= 255; y++) {

            for (unsigned int z = 0; z < 3; z++) {
                unsigned int a = scale*pxarr[(x*256+y) * 3 + z];
                if ( a > 255 ) { a = 255; }
                pixel_array[(x*256+y) * 3 + z] = (unsigned char)(a); // (unsigned char)(255*scale)
            }
            
        }
    }
    return pixel_array;
}

unsigned char *BlendingMultiply(unsigned char* pxarr1,unsigned char* pxarr2,int size) {
    
    unsigned char *pixel_array1 = malloc(size);
    unsigned char *pixel_array2 = malloc(size);
    for (unsigned int x = 0; x <= 255; x++) {

        for (unsigned int y = 0; y <= 255; y++) {

            for (unsigned int z = 0; z < 3; z++) {
                unsigned char a = pixel_array1[(x*256+y) * 3 + z];
                unsigned char b = pixel_array2[(x*256+y) * 3 + z];
                
                pixel_array1[(x*256+y) * 3 + z] = (unsigned char)(a * b); // (unsigned char)(255*scale)
            }
            
        }
    }
    return pixel_array1;
}