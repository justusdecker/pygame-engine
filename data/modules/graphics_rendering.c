#include <stdio.h>
#include <math.h>
#include <stdint.h>
#include <stdlib.h>
typedef struct rgb_color {
    unsigned char rgb[3];
} color;

color ConvertHsvToRgb(float H, float S, float V) {
    float r, g, b;
    

    // First, we get the hue (H), saturation (S), brightness (V ), where H is in a scale
    // between 0 to 6 inclusively, and S and V in a scale between 0 to 1.

    float h = H; // must be in range 0-1
    float s = S; // must be in range 0-1
    float v = V; // must be in range 0-1

    //Incidentally, the brightness, V , also happens to represent the brightest channel in our resulting RGB colour.

    int i = floor(h * 6);
    float f = h * 6 - i;

	float x = v * (1 - s);
	float y = v * (1 - f * s);
	float z = v * (1 - (1 - f) * s);
    // V(v) alpha(x) beta(y) gamma(z)
    switch (i % 6) {
		case 0: r = v, g = z, b = x; break;
		case 1: r = y, g = v, b = x; break;
		case 2: r = x, g = v, b = z; break;
		case 3: r = x, g = y, b = v; break;
		case 4: r = z, g = x, b = v; break;
		case 5: r = v, g = x, b = y; break;
	}

    color rgb;

    rgb.rgb[0] = (unsigned char) (r * 255);
    rgb.rgb[1] = (unsigned char) (g * 255);
    rgb.rgb[2] = (unsigned char) (b * 255);
    
    return rgb;
}

unsigned char *ColorRect(float hue) {

    unsigned char *pixel_array = malloc(256*256*3);
    unsigned char def = 255;
    for (unsigned int x = 0; x <= 255; x++) {
        for (unsigned int y = 0; y <= 255; y++) {
            color rgb = ConvertHsvToRgb(hue,(float)(x)/256,(255-(float)(y))/256);
            // pixel_array[x*y];
            // each x , y set
            // this is a x*y*3 array
            //
            for (unsigned char z = 0; z < 3; z++) {
                //(unsigned char)rgb.rgb[0]
                pixel_array[(x*256+y) * 3] = rgb.rgb[0];
                pixel_array[(x*256+y) * 3+1] = rgb.rgb[1];
                pixel_array[(x*256+y) * 3+2] = rgb.rgb[2];
            }
            
        }
    }
    return pixel_array;
}