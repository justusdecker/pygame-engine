#include <math.h>

float EF_Linear(float x) {
    return x;
}
float EF_Heartbeat(float x) {
    // currently not implemented
    printf("%s is not implemented yet!",__func__);
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