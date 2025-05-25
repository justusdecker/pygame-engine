
from colorsys import hsv_to_rgb
from threading import Thread
from numpy import array
from pygame import Surface,surfarray
from data.modules.data_management import DM
from numba import jit
from time import perf_counter
from ctypes import (
    CDLL,
    POINTER,
    c_float,
    c_char
)
clib = CDLL('data\\modules\\graphics_rendering.so')

RGB_POINTER = POINTER(c_char)

COLORRECT = clib.ColorRect
COLORRECT.restype = RGB_POINTER

COLORLINE = clib.ColorLine
COLORLINE.restype = RGB_POINTER

def color_rect(hue=0.2) -> array:
    """
    creates a new color rect for a colorpicker
    """
    result = clib.ColorRect(c_float(hue))
    return array([int.from_bytes(result[i],"big") for i in range(256*256*3)]).reshape((256,256,3))
    
def color_line() -> array:
    result = clib.ColorLine()
    return array([int.from_bytes(result[i],"big") for i in range(256*16*3)]).reshape((256,16,3))

def surf_to_1d(surface: Surface) -> array:
    x,y = surface.width,surface.height
    return surfarray.array3d(surface).reshape((x*y*3)).tolist()