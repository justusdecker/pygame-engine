

from data.modules.ui.ui_element import UIElement, UIC
from pygame import Surface, Rect, Color, SRCALPHA
from data.modules.ui.ui_font import FONTDRAW
from data.modules.ui.ui_calculation import get_center
from pygame.draw import rect as rect_draw
from data.modules.ui.ux_element import UXElement
from data.modules.constants import (DEFAULT_BACKGROUND_COLOR,
                                    TEXT_COLOR,
                                    PRESSED_TEXT_COLOR,
                                    HIGHLIGHT_TEXT_COLOR)
from data.modules.ui.ui_debug import outliner
class UXButton(UXElement):
    def __init__(self,
                 **options) -> None:
        if not 'tcg' in options: options['tcg'] = (TEXT_COLOR,HIGHLIGHT_TEXT_COLOR,PRESSED_TEXT_COLOR)
        if not 'bcg' in options: options['bcg'] = (DEFAULT_BACKGROUND_COLOR,)
        super().__init__(**options)
        self.draw()
    def getAllImages(self):
        return self.normal_image,self.hovered_image,self.pressed_image 
    def draw(self):
        self.normal_image , self.hovered_image , self.pressed_image = self.gen(
            [
                (self.get_color(self.text_color_group,0),self.get_color(self.background_color_group,0)),
                (self.get_color(self.text_color_group,1),self.get_color(self.background_color_group,1)),
                (self.get_color(self.text_color_group,2),self.get_color(self.background_color_group,2))
            ]
        )
        
    def gen(self,array:list):
        _ret = []
        for text_color,background_color in array:
            SURF = Surface(self.size,SRCALPHA)
            rect_draw(
                SURF,
                background_color,
                (
                    0,
                    0,
                    *self.size
                    ),
                border_radius = self.border_radius
            )
            
            img = self.font.draw(
                self.text,
                color=text_color,
                size = self.font.font.get_height()
                )
            

            SURF.blit(
                img,
                get_center(
                    self.size,
                    img.get_size()
                    )
                )

            _ret.append(SURF)
        return _ret

class UIButton(UIElement):
    def __init__(self,
                 rect:Rect,
                 **kwargs) -> None:
        UIC.add_element('uiButton')
        
        
        self.UX = UXButton(
            **kwargs.get(
                'ux',
                {}
                )
            )
            
        self.set_image(self.UX.normal_image)
        super().__init__(rect,**kwargs)
        
        self.oHC = kwargs.get('on_hovered_callback',self.noCallback)
        
        self.oPC = kwargs.get('on_press_callback',self.noCallback)
        
        self.oUHC = kwargs.get('on_un_hover_callback',self.noCallback)
        
        self.oUPC = kwargs.get('on_un_press_callback',self.noCallback)
        
    def noCallback(self,*btn):
        pass
    def update(self):
        #Change Texture on the fly
        if self.this_frame_hovered:
            self.set_image(self.UX.hovered_image)
            self.oHC(self)
        if self.this_frame_pressed:
            self.set_image(self.UX.pressed_image)
            self.oPC(self)
        if self.this_frame_un_pressed:
            self.set_image(self.UX.normal_image)
            self.oUPC(self)
        if self.this_frame_un_hovered:
            self.set_image(self.UX.normal_image)
            self.oUHC(self)
        super().update()
