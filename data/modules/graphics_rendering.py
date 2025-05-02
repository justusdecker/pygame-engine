
from colorsys import hsv_to_rgb
from numpy import array
from pygame import Surface
class ColorLine:
    def __init__(self):
        self.color_line()
    def color_line(self):
        color_array = []
        for x in range(360):
            _line = []
            for y in range(16):
                _line.append([col * 255 for col in hsv_to_rgb(x/360,1.,1.)])
            color_array.append(_line)
        self.array = array(color_array)
class ColorRect:
    def __init__(self):
        self.color_rect()
    def color_rect(self,hue=0.2):
        color_array = []
        for x in range(256):
            _line = []
            for y in range(256):
                _line.append([col * 255 for col in hsv_to_rgb(hue,x/256,((255-y)/256) if y > 0 else 0)])
            color_array.append(_line)
        self.array = array(color_array)
def color_rect(hue=0.2):
    color_array = []
    for x in range(256):
        _line = []
        for y in range(256):
            _line.append([col * 255 for col in hsv_to_rgb(hue,x/256,((255-y)/256) if y > 0 else 0)])
        color_array.append(_line)
    return array(color_array)

class ComplexSurface(Surface):
    def __init__(self,size,flags,depth,masks):
        super().__init__(size,flags,depth,masks)
        self.rotation = 0
        self.pivot_position = [0,0]