import pygame as pg
from colorsys import rgb_to_hsv,hsv_to_rgb
SURF = pg.Surface((256,256),pg.SRCALPHA)
from numpy import array
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