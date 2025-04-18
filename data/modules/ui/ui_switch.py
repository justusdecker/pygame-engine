from data.modules.ui.ui_element import UIElement, UIC
from data.modules.constants import MEDIUM_BACKGROUND_COLOR,TEXT_COLOR,HIGHLIGHT_TEXT_COLOR,PRESSED_TEXT_COLOR
from pygame.draw import rect as rect_draw
from pygame import Surface, Rect, Color, SRCALPHA

from data.modules.ui.ux_element import UXElement


class UXSwitch(UXElement):
    def __init__(self,
                 **options) -> None:
        if not 'bcg' in options: options['bcg'] = (MEDIUM_BACKGROUND_COLOR,)
        if not 'tcg' in options: options['tcg'] = (TEXT_COLOR,HIGHLIGHT_TEXT_COLOR,PRESSED_TEXT_COLOR)
        super().__init__(**options)
        self.normal_off_image,self.hovered_off_image, self.pressed_off_image,self.normal_on_image,self.hovered_on_image, self.pressed_on_image = self.draw()
    def draw(self):
        return self.gen([
            (self.get_color(self.text_color_group,0),False),
            (self.get_color(self.text_color_group,1),False),
            (self.get_color(self.text_color_group,2),False),
            (self.get_color(self.text_color_group,0),True),
            (self.get_color(self.text_color_group,1),True),
            (self.get_color(self.text_color_group,2),True),
        ])
    def gen(self,array:list=[]):
        _ret = []
        for foreground_color,state in array:
            SURF = Surface(self.size,SRCALPHA)
            rect_draw(
                    SURF,
                    self.get_color(self.background_color_group,0),
                    (0,0,*self.size),
                    border_radius = self.border_radius
                )
            if state:
                rect_draw(
                    SURF,
                    foreground_color,
                    (
                        2,
                        2,
                        20,
                        20
                        ),
                    border_radius = self.border_radius
                )
                
            
            
            _ret.append(SURF)
        return _ret

class UISwitch(UIElement):
    def __init__(self, rect: Rect, **kwargs):
        super().__init__(rect,**kwargs)
        UIC.add_element('uiSwitch')
        self.toggle = kwargs.get('initialValue',False)
        self.UX = UXSwitch(**kwargs.get('ux', {}))
        self.set_image(self.UX.normal_off_image)
        self.oHC = kwargs.get('onHoveredCallback',self.noCallback)
        
        self.oPC = kwargs.get('onPressCallback',self.noCallback)
        
        self.oUHC = kwargs.get('onUnHoverCallback',self.noCallback)
    def noCallback(self,_):
        pass
    def update(self):
        #Change Texture on the fly
        if self.this_frame_hovered:
            self.set_image([self.UX.hovered_off_image,self.UX.hovered_on_image][self.toggle])
            self.oHC(self)
        if self.this_frame_pressed:
            self.toggle = not self.toggle
            self.set_image([self.UX.normal_off_image,self.UX.normal_on_image][self.toggle])
            self.oPC(self)
        if self.this_frame_un_hovered:
            self.set_image([self.UX.normal_off_image,self.UX.normal_on_image][self.toggle])
            self.oUHC(self)
        super().update()
   