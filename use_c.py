#gcc -fPIC -shared -o
from colorsys import hsv_to_rgb
import ctypes
from time import perf_counter
from numpy import array
from data.modules.graphics_rendering import color_rect
from json import dumps
clib = ctypes.CDLL('data\\modules\\graphics_rendering.so')

clib.ColorRect.restype = ctypes.POINTER(ctypes.c_char)
result = clib.ColorRect(ctypes.c_float(0.2))
#arr = array()
with open('test.json','w') as f:
    f.write(dumps({i: int.from_bytes(result[i],"big") for i in range(256*256)},indent=4))
color_array = []
hue = 0.2
for x in range(256):
    _line = []
    for y in range(256):
        _line.append([int(col * 255) for col in hsv_to_rgb(hue,x/256,((255-y)/256))])
    color_array.append(_line)
with open('test1.json','w') as f:
    f.write(dumps(color_array,indent=4))
#!exception: access violation writing