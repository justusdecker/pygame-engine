#include <math.h>

float EF_Linear(float x) {
    return x;
}
float EF_EaseOutBack(float x) {
    const double C = 1.70158;
    const double E = C - 1;

    return C * pow(x,3) - E * pow(x,2);
}