
from data.modules.ui.ui_element import UIElement, UIC
from data.modules.ui.ui_switch import UISwitch
from data.modules.ui.ux_element import UXElement
from data.modules.graphics_rendering import color_rect,color_line
from data.modules.ui.ui_window import UIWindow
from data.modules.vector import Vector4
from pygame.surfarray import make_surface
from pygame.transform import scale
from pygame.mouse import get_pos
from pygame import Color
from data.modules.ui.ui_image import UIImage
from data.modules.constants import DEFAULT_BACKGROUND_COLOR,MEDIUM_BACKGROUND_COLOR
from data.modules.log import LOG
class UXColorPicker(UXElement):
    def __init__(self):
        pass
    def draw(self):
        [[[0,]]]
        self.gen()
class UIColorPicker(UIElement):
    def __init__(self, vector:Vector4, **kwargs):
        vector.z = 172
        vector.w = 278 + 24
        super().__init__(vector, **kwargs)
        UIC.add_element('uiColorPicker')
        
        self.window = UIWindow(vector,ux= {'size':(vector.z,vector.w),'bcg': (DEFAULT_BACKGROUND_COLOR,MEDIUM_BACKGROUND_COLOR)},group=self.group)
        
        self.color_rect = UIImage(Vector4(4,28,163,163),
                                  ux={'size': (163,163)},parent=self.window,group=self.group,layer=self.layer+1)
        self.color_rect.set_image(scale(make_surface(color_rect(0.3)),(163,163)))
        
        self.color_line = UIImage(Vector4(4,195,163,24),
                                  ux={'size': (163,24)},parent=self.window,group=self.group,layer=self.layer+1)
        self.color_line.set_image(scale(make_surface(color_line()),(163,24)))

        self.current_color = Color(0,0,0,255)

        self.hue = 0.2
    def update(self):
        if self.color_rect.is_pressed:
            x1 , y1 = get_pos()
            x2, y2 = self.color_rect.get_abs_position()
            x, y = x1 - x2, y1 - y2
            
            if x >= 0 and y >= 0 and x < self.color_rect.dest[0] and y < self.color_rect.dest[1]:
                
                self.current_color = self.color_rect.get_image().get_at((x,y))
                LOG.nlog(1,'set new color_picker_color: $',[tuple(self.current_color)])
        
        if self.color_line.is_pressed:
            x1 , y1 = get_pos()
            x2, y2 = self.color_line.get_abs_position()
            x, y = x1 - x2, y1 - y2
            
            if x >= 0 and y >= 0 and x < self.color_line.dest[0] and y < self.color_line.dest[1]:
                p = (x / self.color_line.dest[0]) if x > 0 else 0
                self.hue = p
                self.color_rect.set_image(scale(make_surface(color_rect(self.hue)),(163,163)))
                
                LOG.nlog(1,'set new color_picker_color: $ $',[self.hue,p])
        return super().update()