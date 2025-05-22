from math import pi,cos,sqrt

"""
(c) 2025 Justus Decker
"""

def animator(func) -> list[float]: return [func(i * .01) for i in range(101)]
