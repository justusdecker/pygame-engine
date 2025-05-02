
from data.modules.ui.ui_element import UIElement, UIC
from data.modules.ui.ui_switch import UISwitch
from data.modules.ui.ux_element import UXElement
from data.modules.graphics_rendering import color_rect,color_line
from data.modules.ui.ui_window import UIWindow
from data.modules.vector import Vector4
from pygame.surfarray import make_surface
from pygame.transform import scale
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

        
        """
        Needed:
            Background UX✅
            Preview
            RGB Value Textinputs
            HSV Value Textinputs
            HEX Value Textinput
            SET Button
            RST Button
            Color Picker?
        """
    def update(self):
        return super().update()