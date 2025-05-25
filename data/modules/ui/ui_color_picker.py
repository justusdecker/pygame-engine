
from data.modules.ui.ui_element import UIElement, UIC
from data.modules.ui.ui_button import UIButton
from data.modules.ui.ux_element import UXElement
from data.modules.ui.ui_text_input import UITextInput
from data.modules.graphics_rendering import color_rect,color_line
from colorsys import rgb_to_hsv,hsv_to_rgb
from data.modules.ui.ui_window import UIWindow
from data.modules.vector import Vector4
from pygame.surfarray import make_surface
from pygame.transform import scale
from pygame.mouse import get_pos
from pygame import Color, Surface, SRCALPHA
from data.modules.ui.ui_image import UIImage
from data.modules.constants import DEFAULT_BACKGROUND_COLOR,MEDIUM_BACKGROUND_COLOR
from data.modules.kernel.log import LOG
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
        
        self.window = UIWindow(vector,ux= {'size':(vector.z,vector.w),'text':'Colorpicker','bcg': (DEFAULT_BACKGROUND_COLOR,MEDIUM_BACKGROUND_COLOR)},group=self.group)
        
        self.color_rect = UIImage(Vector4(4,28,163,163),
                                  ux={'size': (163,163)},parent=self.window,group=self.group,layer=self.layer+1)
        self.color_rect.set_image(scale(make_surface(color_rect(0.3)),(163,163)))
        
        self.color_line = UIImage(Vector4(4,195,163,24),
                                  ux={'size': (163,24)},parent=self.window,group=self.group,layer=self.layer+1)
        self.color_line.set_image(scale(make_surface(color_line()),(163,24)))

        self.color_preview = UIImage(Vector4(40,40,82,82),ux={'size': (82,82)},parent=self.color_rect,group=self.group,layer=self.layer+2)
        
        self.hex_input = UITextInput(Vector4(4,219,99,24),app=self.app,default_text = 'hex', max_letters = 7,mode = 'hex_color_value',group = self.group, parent = self.window)

        self.hex_set_button = UIButton(Vector4(103,219,64,24),ux={'size':(64,24),'text':'set'},group = self.group, parent = self.window,cb_on_press = self.set_col_by_hex)

        self.r_input = UITextInput(Vector4(4,247,40,24),app=self.app,default_text = 'r', max_letters = 3,mode = 'only_numbers',group = self.group, parent = self.window)
        
        self.g_input = UITextInput(Vector4(44,247,40,24),app=self.app,default_text = 'g', max_letters = 3,mode = 'only_numbers',group = self.group, parent = self.window)
        
        self.b_input = UITextInput(Vector4(84,247,40,24),app=self.app,default_text = 'b', max_letters = 3,mode = 'only_numbers',group = self.group, parent = self.window)
        
        self.hex_set_button = UIButton(Vector4(122,247,40,24),ux={'size':(40,24),'text':'set'},group = self.group, parent = self.window,cb_on_press = self.set_col_by_rgb)
        
        self.h_input = UITextInput(Vector4(4,275,40,24),app=self.app,default_text = 'h', max_letters = 3,mode = 'float',group = self.group, parent = self.window)
        
        self.s_input = UITextInput(Vector4(44,275,40,24),app=self.app,default_text = 's', max_letters = 3,mode = 'float',group = self.group, parent = self.window)
        
        self.v_input = UITextInput(Vector4(84,275,40,24),app=self.app,default_text = 'v', max_letters = 3,mode = 'float',group = self.group, parent = self.window)
        
        self.hex_set_button = UIButton(Vector4(122,275,40,24),ux={'size':(40,24),'text':'set'},group = self.group, parent = self.window,cb_on_press = self.set_col_by_hsv)
        
        self.current_color = (0,0,0,255)
        self.last_pos = (0,162)
        self.hue = 0.2
    def set_col_by_hex(self,*_):
        if len(self.hex_input.text) == 7:
            rgb = self.hex_input.text
            
            r,g,b = int(rgb[1:3],16),int(rgb[3:5],16),int(rgb[5:7],16)
            self.current_color = r,g,b,255
            r = (r / 255) if r > 0 else 0
            g = (g / 255) if g > 0 else 0
            b = (b / 255) if b > 0 else 0
            self.hue = rgb_to_hsv(r,g,b)[0]
            self.color_rect.set_image(scale(make_surface(color_rect(self.hue)),(163,163)))
            self.rerender_text_inputs()
    def set_col_by_rgb(self,*_):
        if not self.r_input.text or not self.g_input.text or not self.b_input.text: return
        r = int(self.r_input.text)
        r = r if r < 256 else 255
        g = int(self.g_input.text)
        g = g if g < 256 else 255
        b = int(self.b_input.text)
        b = b if b < 256 else 255
        self.current_color = r,g,b,255
        hsv = rgb_to_hsv(r,g,b)
        self.hue = hsv[0]
        self.color_rect.set_image(scale(make_surface(color_rect(self.hue)),(163,163)))
        self.rerender_text_inputs()
    def set_col_by_hsv(self,*_):
        if not self.h_input.text or not self.s_input.text or not self.v_input.text: return
        h, s, v = hsv_to_rgb(float(self.h_input.text),float(self.s_input.text),float(self.v_input.text))
        r = (h if h <= 1 else 1) * 255
        g = (s if s <= 1 else 1) * 255
        b = (v if v <= 1 else 1) * 255
        self.current_color = r,g,b
        self.hue = h
        self.color_rect.set_image(scale(make_surface(color_rect(self.hue)),(163,163)))
        self.rerender_text_inputs()
    def rerender_text_inputs(self):
        r,g,b,a = tuple(self.current_color)
        h, s, v = rgb_to_hsv((r / 255) if r > 0 else 0 , (g / 255) if g > 0 else 0, (b / 255) if b > 0 else 0)

        self.h_input.overwrite_text(f'{h:.2f}'[:3])
        self.s_input.overwrite_text(f'{s:.2f}'[:3])
        self.v_input.overwrite_text(f'{v:.2f}'[:3])
        self.r_input.overwrite_text(str(int(r)))
        self.g_input.overwrite_text(str(int(g)))
        self.b_input.overwrite_text(str(int(b)))
    def update(self):
        
        if self.color_rect.is_pressed:
            x1 , y1 = get_pos()
            x2, y2 = self.color_rect.get_abs_position()
            x, y = x1 - x2, y1 - y2
            
            if x >= 0 and y >= 0 and x < self.color_rect.dest[0] and y < self.color_rect.dest[1]:
                
                self.current_color = self.color_rect.get_image().get_at((x,y))
                self.last_pos = x,y
                self.rerender_text_inputs()
        if self.color_line.is_pressed:
            x1 , y1 = get_pos()
            x2, y2 = self.color_line.get_abs_position()
            x, y = x1 - x2, y1 - y2
            
            if x >= 0 and y >= 0 and x < self.color_line.dest[0] and y < self.color_line.dest[1]:
                p = (x / self.color_line.dest[0]) if x > 0 else 0
                self.hue = p
                self.color_rect.set_image(scale(make_surface(color_rect(self.hue)),(163,163)))
                self.current_color = self.color_rect.get_image().get_at(self.last_pos)
                self.rerender_text_inputs()   

        if self.color_rect.is_pressed or self.color_line.is_pressed:
            
            surf = Surface(self.color_preview.dest,SRCALPHA)
            surf.fill(self.current_color)
            self.color_preview.set_image(surf)
        else:
            surf = Surface(self.color_preview.dest,SRCALPHA)
            self.color_preview.set_image(surf)
        return super().update()