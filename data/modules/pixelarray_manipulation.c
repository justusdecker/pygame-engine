#include <stdio.h>
#include <stdlib.h>
unsigned char *ColorTest(float scale, unsigned char* pxarr,int size) {
    
    unsigned char *pixel_array = malloc(size);
    for (unsigned int x = 0; x <= 255; x++) {

        for (unsigned int y = 0; y <= 255; y++) {

            for (unsigned int z = 0; z < 3; z++) {
                
                //this line here is faulty VVV
                //printf("%d",pxarr[(x*16+y) * 3 + z]);
                //unsigned int a = (float)(pxarr[(x*16+y) * 3 + z]);
                //pxarr[(x*16+y) * 3 + z];
                //a *= scale;
                //if ( a > 255 ) { a = 255; }
                
                pixel_array[(x*256+y) * 3 + z] = (unsigned char)(scale*pxarr[(x*256+y) * 3 + z]); // (unsigned char)(255*scale)
                
            }
            
        }
    }
    return pixel_array;
}