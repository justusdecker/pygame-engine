
from data.modules.ui.ui_element import UIElement, UIC
from data.modules.ui.ui_switch import UISwitch
from data.modules.ui.ux_element import UXElement
from data.modules.ui.ui_text_input import UITextInput
from data.modules.graphics_rendering import color_rect,color_line
from colorsys import rgb_to_hsv
from data.modules.ui.ui_window import UIWindow
from data.modules.vector import Vector4
from pygame.surfarray import make_surface
from pygame.transform import scale
from pygame.mouse import get_pos
from pygame import Color, Surface, SRCALPHA
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
        
        if 'app' in kwargs:
            self.app = kwargs['app']
        else:
            raise Exception('No App. No Game!')
        
        self.window = UIWindow(vector,ux= {'size':(vector.z,vector.w),'bcg': (DEFAULT_BACKGROUND_COLOR,MEDIUM_BACKGROUND_COLOR)},group=self.group)
        
        self.color_rect = UIImage(Vector4(4,28,163,163),
                                  ux={'size': (163,163)},parent=self.window,group=self.group,layer=self.layer+1)
        self.color_rect.set_image(scale(make_surface(color_rect(0.3)),(163,163)))
        
        self.color_line = UIImage(Vector4(4,195,163,24),
                                  ux={'size': (163,24)},parent=self.window,group=self.group,layer=self.layer+1)
        self.color_line.set_image(scale(make_surface(color_line()),(163,24)))

        self.color_preview = UIImage(Vector4(40,40,82,82),ux={'size': (82,82)},parent=self.color_rect,group=self.group,layer=self.layer+2)
        
        self.hex_input = UITextInput(Vector4(4,219,163,24),app=self.app,default_text = 'hex', max_letters = 7,mode = 'hex_color_value',group = self.group, parent = self.window)

        self.current_color = Color(0,0,0,255)
        self.last_pos = (0,162)
        self.hue = 0.2
    def update(self):
        if self.color_rect.is_pressed:
            x1 , y1 = get_pos()
            x2, y2 = self.color_rect.get_abs_position()
            x, y = x1 - x2, y1 - y2
            
            if x >= 0 and y >= 0 and x < self.color_rect.dest[0] and y < self.color_rect.dest[1]:
                
                self.current_color = self.color_rect.get_image().get_at((x,y))
                self.last_pos = x,y
        if self.color_line.is_pressed:
            x1 , y1 = get_pos()
            x2, y2 = self.color_line.get_abs_position()
            x, y = x1 - x2, y1 - y2
            
            if x >= 0 and y >= 0 and x < self.color_line.dest[0] and y < self.color_line.dest[1]:
                p = (x / self.color_line.dest[0]) if x > 0 else 0
                self.hue = p
                self.color_rect.set_image(scale(make_surface(color_rect(self.hue)),(163,163)))
                self.current_color = self.color_rect.get_image().get_at(self.last_pos)
            
        if self.hex_input.active:
            if len(self.hex_input.text) == 7:
                rgb = self.hex_input.text
                
                r,g,b = int(rgb[1:3],16),int(rgb[3:5],16),int(rgb[5:7],16)
                self.current_color = r,g,b
                r = (r / 255) if r > 0 else 0
                g = (g / 255) if g > 0 else 0
                b = (b / 255) if b > 0 else 0
                self.hue = rgb_to_hsv(r,g,b)[0]
                self.color_rect.set_image(scale(make_surface(color_rect(self.hue)),(163,163)))
        if self.color_rect.is_pressed or self.color_line.is_pressed:
            
            surf = Surface(self.color_preview.dest,SRCALPHA)
            surf.fill(self.current_color)
            self.color_preview.set_image(surf)
        else:
            surf = Surface(self.color_preview.dest,SRCALPHA)
            self.color_preview.set_image(surf)
        return super().update()