
from colorsys import hsv_to_rgb
from numpy import array
from pygame import Surface
from data.modules.data_management import DM
from numba import jit
from ctypes import (
    CDLL,
    POINTER,
    c_float,
    c_char,c_int
)
clib = CDLL('data\\modules\\graphics_rendering.so')
clib_pa = CDLL('data\\modules\\pixelarray_manipulation.so')

RGB_POINTER = POINTER(c_char)

COLORRECT = clib.ColorRect
COLORRECT.restype = RGB_POINTER

COLORLINE = clib.ColorLine
COLORLINE.restype = RGB_POINTER

COLORTEST = clib_pa.GammaCorrection
COLORTEST.restype = RGB_POINTER


def color_rect(hue=0.2) -> array:
    """
    creates a new color rect for a colorpicker
    """
    result = clib.ColorRect(c_float(hue))
    return array([int.from_bytes(result[i],"big") for i in range(256*256*3)]).reshape((256,256,3))
    
def color_line() -> array:
        result = clib.ColorLine()
        return array([int.from_bytes(result[i],"big") for i in range(256*16*3)]).reshape((256,16,3))

def color_correction(pixel_array: list, scale: float) -> array:
        result = clib_pa.GammaCorrection(c_float(4.0), (c_char * len(pixel_array))(*pixel_array), c_int(len(pixel_array)))
        return array([int.from_bytes(result[i],"big") for i in range(256*256*3)]).reshape((256,256,3))
@jit
def convert_3d_array_to_1d(surface_array:list[list[list[int,int,int]]]) -> array:
    _ret = []
    for x in range(x):
        for y in range(y):
            for z in range(3):
                _ret.append(surface_array[x][y][z])
    return _ret