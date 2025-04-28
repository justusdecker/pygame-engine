from data.modules.ui.ui_element import UIElement, UIC
from pygame.draw import rect as rect_draw
from pygame import Surface, Rect, Color, SRCALPHA
from data.modules.ui.ui_font import FONTDRAW
from data.modules.ui.ui_calculation import get_center,get_top_center
from data.modules.constants import DEFAULT_BACKGROUND_COLOR,TEXT_COLOR
from data.modules.ui.ux_element import UXElement
from data.modules.vector import Vector4,Vector2
class UXLabel(UXElement):
    def __init__(self,**options) -> None:
        if not 'tcg' in options: options['tcg'] = (TEXT_COLOR,)
        if not 'bcg' in options: options['bcg'] = (DEFAULT_BACKGROUND_COLOR,)
        super().__init__(**options)
        self.anchor = options.get('anchor','center')
        g = [
            [[0,self.background_color_group.get(0),Vector4(0,0,*self.size)],
             [1,self.text_color_group.get(0),'center']],
        ]
        self.surface = self.gen(g)[0]
class UILabel(UIElement):
    """
    No callbacks
    
    The text can be updated by calling the render method
    """
    def __init__(self, rect: Rect, **kwargs):
        UIC.add_element('uiLabel')
        super().__init__(rect, **kwargs)
        ux = kwargs.get('ux',{'size' : self.dest})
        if 'size' not in ux:
            ux['size'] = self.dest
        self.UX = UXLabel(**ux)
        self.set_image(self.UX.surface)
    def render(self,text:str):
        self.UX.text = text
        g = [
            [[0,self.UX.background_color_group.get(0),Vector4(0,0,*self.UX.size)],
             [2,self.UX.text_color_group.get(0),'center']],
        ]
        self.set_image(self.UX.gen(g)[0])
    def update(self):
        super().update()

