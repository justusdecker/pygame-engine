
from colorsys import hsv_to_rgb
from numpy import array
from pygame import Surface
from data.modules.data_management import DM

from ctypes import (
    CDLL,
    POINTER,
    c_float,
    c_char,c_char_p
)
clib = CDLL('data\\modules\\graphics_rendering.so')
clib_pa = CDLL('data\\modules\\pixelarray_manipulation.so')

RGB_POINTER = POINTER(c_char)

COLORRECT = clib.ColorRect
COLORRECT.restype = RGB_POINTER

COLORLINE = clib.ColorLine
COLORLINE.restype = RGB_POINTER

COLORTEST = clib_pa.ColorTest
COLORTEST.restype = RGB_POINTER

def color_rect(hue=0.2) -> array:
    """
    creates a new color rect for a colorpicker
    """
    result = clib.ColorRect(c_float(hue))
    return array([int.from_bytes(result[i],"big") for i in range(256*256*3)]).reshape((256,256,3))
    
def color_line() -> array:
        result = clib.ColorLine()
        DM.save('test.json',[int.from_bytes(result[i],"big") for i in range(256*16*3)])
        return array([int.from_bytes(result[i],"big") for i in range(256*16*3)]).reshape((256,16,3))

def line_test() -> array:
        result = clib_pa.ColorTest()
        c_char_p([int.from_bytes(result[i],"big") for i in range(256*16*3)])
        DM.save('test.json',[int.from_bytes(result[i],"big") for i in range(256*16*3)])
        return array([int.from_bytes(result[i],"big") for i in range(256*16*3)]).reshape((256,16,3))