import pygame as pg
from colorsys import hsv_to_rgb
from numpy import array

class ColorWheel:
    def __init__(self):
        self.color_wheel()
    def color_wheel(self,radius = 256):
        self.array = [[(0,0,0) for y in range(radius)] for x in range(radius)]
        diameter = radius
        offset_radius = (diameter / 2) - 0.5
        for i in range(diameter):
            for j in range(diameter):
                x = i - offset_radius
                y = j - offset_radius
                if x * x + y * y <= offset_radius * offset_radius + 1:
                    self.array[i][j] = (255,255,255)
        self.array = array(self.array)
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
        
CR = ColorRect()
SURF = pg.surfarray.make_surface(CR.array)
pg.image.save(SURF,'color_rect.png')

CW = ColorWheel()
SURF = pg.surfarray.make_surface(CW.array)
pg.image.save(SURF,'color_wheel.png')

CL = ColorLine()
SURF = pg.surfarray.make_surface(CL.array)
pg.image.save(SURF,'color_line.png')