
from data.modules.ui.ui_element import UIElement, UIC
from data.modules.ui.ui_switch import UISwitch
from data.modules.ui.ux_element import UXElement
from data.modules.graphics_rendering import color_rect
from data.modules.ui.ui_window import UIWindow
from data.modules.vector import Vector4
from pygame.surfarray import make_surface
from pygame.transform import scale
from data.modules.ui.ui_image import UIImage
from data.modules.constants import DEFAULT_BACKGROUND_COLOR,MEDIUM_BACKGROUND_COLOR
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
        
        self.color_rect = UIImage(Vector4(49,95,163,163),
                                  ux={'size': (163,163)},parent=self.window,group=self.group,layer=self.layer+1)
        self.set_image(scale(make_surface(color_rect(0.3)),(163,163)))
        
        self.switch = UISwitch(
            Vector4(0,24,24,24),
            ux={'size':(24,24)},
            group=self.group,
            parent = self.window)
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
        self.pos = self.window.pos
        return super().update()