from data.modules.ui.ui_element import UIElement
from pygame import Surface, Rect, Color
from pygame.draw import line as line_draw
from pygame.mouse import get_pos
class UISliderLR(UIElement):#Todo
    def __init__(self, rect: Rect, **kwargs):
        super().__init__(rect, **kwargs)
        #self.btnLeft = UIButton(pg.Rect(0,0,24,24),ux={'text': '<','size': (24,24)},parent=self)
        self.set_image(Surface((rect.w,rect.h)))
        self.surface.fill(Color('#242424'))
        line_draw(self.surface,(128,0,0),(0,0),(0,24),3)
        #self.btnRight = UIButton(pg.Rect(rect.w-24,0,24,24),ux={'text': '>','size': (24,24)},parent=self)
        self.slider_percent = kwargs('percent',0)
        #pg.draw.line(self.surface,(128,0,0),(mp,0),(mp,24),3)
    def update(self):
        if self.is_pressed:
            mp = get_pos()[0]

            if mp > self.dest[0]:
                mp = self.dest[0]
            if mp < self.pos[0]:
                mp = self.pos[0]
            mx = abs((self.get_abs_position()[0]-mp) / self.dest[0])   #Calculates the value bet, 0-1

            self.surface.fill(Color('#242424'))
            
            line_draw(self.surface,(128,0,0),(mp,0),(mp,24),3)
            self.slider_percent = mx
            
        #mx = abs(pg.mouse.get_pos()[0] / 1280) if pg.mouse.get_pos()[0] > 0 else 0
        return super().update()
