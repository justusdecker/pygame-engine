from data.modules.ui.ui_element import UIElement, UIC
from pygame.draw import rect as rect_draw
from pygame import Surface, Rect, Color, SRCALPHA
from data.modules.ui.ui_font import FONTDRAW
from data.modules.ui.ui_calculation import get_center,get_top_center
from data.modules.constants import DEFAULT_BACKGROUND_COLOR,TEXT_COLOR
from data.modules.ui.ux_element import UXElement
class UXLabel(UXElement):
    def __init__(self,**options) -> None:
        if not 'tcg' in options: options['tcg'] = (TEXT_COLOR,)
        if not 'bcg' in options: options['bcg'] = (DEFAULT_BACKGROUND_COLOR,)
        super().__init__(**options)
        self.anchor = options.get('anchor','center')
        self.surface = self.gen()

    def gen(self):

        SURF = Surface(self.size,SRCALPHA)
        rect_draw(
            SURF,
            self.get_color(self.background_color_group,0),
            (
                0,
                0,
                *self.size
                ),
            border_radius = self.border_radius
        )
        
        img = self.font.draw(
            self.text,
            color=self.get_color(self.text_color_group,0),
            size = self.font.font.get_height()
            )
        match self.anchor:
            case 'center':
                SURF.blit(
                    img,
                    get_center(
                        self.size,
                        img.get_size()
                        )
                    )
            case 'top_center':
                SURF.blit(
                    img,
                    get_top_center(
                        self.size,
                        img.get_size()
                        )
                    )
        
        return SURF

class UILabel(UIElement):
    def __init__(self, rect: Rect, **kwargs):
        UIC.add_element('uiLabel')
        super().__init__(rect, **kwargs)
        self.UX = UXLabel(
            **kwargs.get(
                'ux',
                {
                    'size' : self.dest
                    }
                )
            )
        self.set_image(self.UX.surface)
    def render(self,text:str):
        self.UX.text = text
        self.set_image(self.UX.gen())
    def update(self):
        super().update()
