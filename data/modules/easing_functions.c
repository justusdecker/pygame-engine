#include <math.h>


float *animator(float (*ptr)()) {
    // will be tested & changed later
    float arr[100];
    for (char i; i < 100; i++) {
        arr[i] = (*ptr)(i * 0.01);
    }
    
}

float EF_EaseInOutQuad(float x) {

    if (x == 0) {
        return 0;
    }
    if (x > 0.5) {
        return 8*x*x;
    }
    else {
        return 1 - pow(-2 * x + 2, 2) / 2;
    }
}

float EF_EaseInOutCubic(float x) {

    if (x == 0) {
        return 0;
    }
    if (x > 0.5) {
        return 4*x*x*x;
    }
    else {
        return 1 - pow(-2 * x + 2, 3) / 2;
    }
}

float EF_EaseInOutQuart(float x) {

    if (x == 0) {
        return 0;
    }
    if (x > 0.5) {
        return 8*x*x*x*x;
    }
    else {
        return 1 - pow(-2 * x + 2, 4) / 2;
    }
}

float EF_EaseInOutQuint(float x) {

    if (x == 0) {
        return 0;
    }
    if (x > 0.5) {
        return 16*x*x*x*x*x;
    }
    else {
        return 1 - pow(-2 * x + 2, 5) / 2;
    }
}

float EF_EaseInOutCirc(float x) {
    if (x == 0) {
        return 0;
    }
    if (x > 0.5) {
        return (1 - sqrt(abs(1 - pow(2 * x , 2)))) / 2;
    }
    else {
        return (sqrt(abs(1 - pow(-2 * x + 2 , 2))) + 1) / 2;
    }
}

float EF_Heartbeat(float x) {
    const float E = 2.5949095; // mul res of 1.70158 * 1.525
    
    if (x > 0.5) {
        return pow(2 * x, 2) * ((E + 1) * (2 * x) - E) / 2;
    }
    else {
        return pow(2 * x - 2, 2) * ((E + 1) * (2 * x - 2) + E) / 2;
    }
}

float EF_Linear(float x) {
    return x;
}

float EF_EaseInBack(float x) {
    const double C = 1.70158;
    const double E = C - 1;

    return C * pow(x,3) - E * pow(x,2);
}

float EF_EaseOutBack(float x) {
    const double C = 1.70158;
    const double E = C - 1;
    return 1 + C * pow(x - 1, 3) + E * pow(x - 1, 2);
}

float EF_EaseOutCirc(float x) {
    return sqrt(1 - pow(x - 1, 2));
}

float EF_EaseInCirc(float x) {
    return 1 - sqrt(1 - pow(x, 2));
}

float EF_EaseOutQuint(float x) {
    return 1 - pow(1 - x, 5);
}

float EF_EaseInQuint(float x) {
    return pow(x, 5);
}

float EF_EaseOutQuart(float x) {
    return 1 - pow(1 - x, 4);
}

float EF_EaseInQuart(float x) {
    return pow(x, 4);
}

float EF_EaseOutCubic(float x) {
    return 1 - pow(1 - x, 3);
}

float EF_EaseInCubic(float x) {
    return pow(x, 3);
}

float EF_EaseOutQuad(float x) {
    return 1 - pow(1 - x, 2);
}

float EF_EaseInQuad(float x) {
    return pow(x, 2);
}

float EF_EaseInSine(float x) {
    const float PI = 3.14159;
    return 1 - cos(x * PI / 2);
}

float EF_EaseOutSine(float x) {
    const float PI = 3.14159;
    return cos(x * PI / 2);
}

float EF_EaseInOutSine(float x) {
    const float PI = 3.14159;
    return -(cos(x * PI) - 1) / 2;
}

float EF_EaseInBounce(float x) {
    const float N = 7.5625;
    const float D = 2.75;

    const float A = 0.75;
    const float B = 0.9375;
    const float C = 0.984375;

    const float X1 = x - (1.5 / D);
    const float X2 = x - (2.25 / D);
    const float X3 = x - (2.625 / D);

    if ( x < 1 / D ) {
        return N * pow(x, 2);
    }
    else if (x < 2 / D) {
        return N * pow(X1, 2) + A;
    }
    else if (x < 2.5 / D) {
        return N * pow(X2, 2) + B;
    }
    else {
        return N * pow(X3, 2) + C;
    }
}

float EF_EaseOutBounce(float x) {
    const float PI = 3.14159;
    return 1 - EF_EaseInBounce(1 - x);
}

// currently not implemented

float EF_EaseInOutBounce(float x) {
    // currently not implemented
    printf("%s is not implemented yet!",__func__);
    return x;
}



float EF_EaseInExpo(float x) {
    // currently not implemented
    printf("%s is not implemented yet!",__func__);
    return x;
}

float EF_EaseOutExpo(float x) {
    // currently not implemented
    printf("%s is not implemented yet!",__func__);
    return x;
}

float EF_EaseInOutExpo(float x) {
    // currently not implemented
    printf("%s is not implemented yet!",__func__);
    return x;
}

float EF_EaseInElastic(float x) {
    // currently not implemented
    printf("%s is not implemented yet!",__func__);
    return x;
}

float EF_EaseOutElastic(float x) {
    // currently not implemented
    printf("%s is not implemented yet!",__func__);
    return x;
}

float EF_EaseInOutElastic(float x) {
    // currently not implemented
    printf("%s is not implemented yet!",__func__);
    return x;
}