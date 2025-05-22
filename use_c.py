#gcc -fPIC -shared -o
import ctypes
from time import perf_counter
clib = ctypes.CDLL('data\\modules\\graphics_rendering.so')
def conv(a: int):
    return a ** 2


#print(clib.ColorRect(ctypes.c_float(0.2)))
#!exception: access violation writing