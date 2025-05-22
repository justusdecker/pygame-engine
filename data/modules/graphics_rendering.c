#include <stdio.h>
#include <math.h>

char *ConvertHsvToRgb(float H, float S, float V) {
    float r, g, b;
    

    // First, we get the hue (H), saturation (S), brightness (V ), where H is in a scale
    // between 0 to 6 inclusively, and S and V in a scale between 0 to 1.

    float h = H / 360;
    float s = S / 100;
    float v = V / 100;

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
    static char rgb[3];

    rgb[0] = (char)r * 255;
    rgb[1] = (char)g * 255;
    rgb[2] = (char)b * 255;
    return rgb;
    
}


char *ColorRect(float hue) {

    unsigned char arr[256][256][3];
    for (unsigned x = 0; x < 256; x++) {
        for (unsigned y = 0; y < 256; y++) {
            //next step calculation of and creating a array
            
            }
    }
    return arr;
}