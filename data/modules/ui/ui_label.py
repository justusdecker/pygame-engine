from data.modules.data_management import UnpackManager
from data.modules.ui.ui_element import UIElement, UIC
from pygame.draw import rect as rect_draw
from pygame import Surface, Rect, Color, SRCALPHA
from data.modules.ui.ui_font import FONTDRAW
from data.modules.ui.ui_calculation import getCenter,getTopCenter
from data.modules.constants import DEFAULT_BACKGROUND_COLOR,TEXT_COLOR
class UXLabel:
    def __init__(self,**options) -> None:
        self.size = UnpackManager('size',options,(128,24))
        self.borderRadius = UnpackManager('borderRadius',options,15)
        self.textColor = UnpackManager('text_color',options,Color(TEXT_COLOR))
        self.backgroundColor = UnpackManager('background_color',options,Color(DEFAULT_BACKGROUND_COLOR))
        self.text = UnpackManager('text',options,'')
        self.anchor = UnpackManager('anchor',options,'center')
        self.surface = self.gen()
        
    def gen(self):

        SURF = Surface(self.size,SRCALPHA)
        rect_draw(
            SURF,
            self.backgroundColor,
            (
                0,
                0,
                *self.size
                ),
            border_radius = self.borderRadius
        )
        
        img = FONTDRAW.draw(
            self.text,
            color=self.textColor
            )
        match self.anchor:
            case 'center':
                SURF.blit(
                    img,
                    getCenter(
                        self.size,
                        img.get_size()
                        )
                    )
            case 'top_center':
                SURF.blit(
                    img,
                    getTopCenter(
                        self.size,
                        img.get_size()
                        )
                    )
        
        return SURF

class UILabel(UIElement):
    def __init__(self, rect: Rect, **kwargs):
        UIC.addElement('uiLabel')
        super().__init__(rect, **kwargs)
        self.UX = UXLabel(
            **UnpackManager(
                'ux',
                kwargs,
                {
                    'size' : self.dest
                    }
                )
            )
        self.setImage(self.UX.surface)
    def render(self,text:str):
        self.UX.text = "test"
        self.setImage(self.UX.gen())
    def update(self):
        super().update()
