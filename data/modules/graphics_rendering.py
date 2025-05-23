
from colorsys import hsv_to_rgb
from numpy import array
from pygame import Surface
from data.modules.data_management import DM

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

COLORRECT = clib.ColorLine
COLORRECT.restype = RGB_POINTER

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
        color_array = []
        for x in range(360):
            _line = []
            for y in range(16):
                _line.append([col * 255 for col in hsv_to_rgb(x/360,1.,1.)])
            color_array.append(_line)
        return array(color_array)
class ComplexSurface(Surface):
    def __init__(self,size,flags,depth,masks):
        super().__init__(size,flags,depth,masks)
        self.rotation = 0
        self.pivot_position = [0,0]