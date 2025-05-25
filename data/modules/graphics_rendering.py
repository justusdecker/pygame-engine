
from colorsys import hsv_to_rgb
from numpy import array
from pygame import Surface,surfarray
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

BLENDMUL = clib_pa.BlendingMultiply
BLENDMUL.restype = RGB_POINTER


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
def surf_to_1d(surface: Surface) -> array:
    x,y = surface.width,surface.height
    
    Surface().get
    return surfarray.array3d(surface).reshape((x*y*3)).tolist()
def blend_mult(a: Surface,b: Surface) -> Surface:
    x,y = a.width,a.height
    pa = surf_to_1d(a)
    pb = surf_to_1d(b)
    result = clib_pa.BlendingMultiply((c_char * len(pa))(*pa),(c_char * len(pb))(*pb),x*y)
    arr = array([int.from_bytes(result[i],"big") for i in range(x*y*3)]).reshape((x,y,3))
    return surfarray.make_surface(arr)