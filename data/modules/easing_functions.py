from math import pi,cos,sqrt

"""
(c) 2025 Justus Decker
"""

def animator(func) -> list[float]: return [func(i * .01) for i in range(101)]

class Animations:

    def ease_in_out_circ(x: float) -> float:
        if x == 0: return 0
        return [((1 - sqrt(abs(1 - ((2 * x)**2)))) / 2),((sqrt(abs(1 - ((-2 * x + 2)**2))) + 1)/ 2)][x > .5]

    def ease_in_out_quint(x: float) -> float:
        return [16*x*x*x*x*x,1 - ((-2 * x + 2)**5)/2][x > .5]

    def ease_in_out_quart(x: float) -> float:
        return [8*x*x*x*x,1 - ((-2 * x + 2)**4)/2][x > .5]

    def ease_in_out_cubic(x: float) -> float:
        return [4*x*x*x,1 - ((-2 * x + 2)**3)/2][x > .5]

    def ease_in_out_quad(x: float) -> float:
        return [2*x*x,1 - ((-2 * x + 2)**2)/2][x > .5]