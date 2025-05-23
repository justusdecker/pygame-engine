unsigned char *ColorLine(float scale, unsigned char pxarr) {
    
    unsigned char *pixel_array = pxarr;
    for (unsigned int x = 0; x <= 255; x++) {

        for (unsigned int y = 0; y <= 15; y++) {

            for (unsigned int z = 0; z <= 3; z++) {

                printf(z);
                pixel_array[(x*16+y) * 3] = (unsigned char)(pixel_array[(x*16+y) * 3] * scale);
                //pixel_array[(x*16+y) * 3+1] = rgb.rgb[1];
                //pixel_array[(x*16+y) * 3+2] = rgb.rgb[2];
                
            }
            //pixel_array[(x*16+y) * 3] = (unsigned char)(pixel_array[(x*16+y) * 3] * scale);
            //pixel_array[(x*16+y) * 3+1] = rgb.rgb[1];
            //pixel_array[(x*16+y) * 3+2] = rgb.rgb[2];
            
        }
    }
    return pixel_array;
}