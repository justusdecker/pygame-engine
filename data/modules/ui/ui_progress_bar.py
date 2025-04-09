from data.modules.ui.ui_element import UIElement, UIC
from pygame import Surface, Rect, Color, SRCALPHA
from data.modules.data_management import UnpackManager
from pygame.draw import rect as rect_draw
from data.modules.constants import MEDIUM_BACKGROUND_COLOR,DEFAULT_BACKGROUND_COLOR
class UXLoadingBar:
    def __init__(self,**options) -> None:
        self.size = UnpackManager('size',options,(512,24))
        self.borderRadius = UnpackManager('borderRadius',options,15)
        self.barColor = UnpackManager('bar_color',options,Color(MEDIUM_BACKGROUND_COLOR))
        self.bgColor = UnpackManager('bg_color',options,Color(DEFAULT_BACKGROUND_COLOR))
        self.bg,self.bar = self.gen([self.bgColor,self.barColor])
        self.currentProgress = 0
        self.currentProgressImage = self.bg.copy()
    def getCurrentProgress(self,percent:float):
        if percent != self.currentProgress:
            self.currentProgress = percent
            SURF:Surface = self.bg.copy()
            max = self.bg.get_width()
            SURF.blit(self.bar,(0,0),area=(0,0,int(percent * max),self.bg.get_height()))
            self.currentProgressImage = SURF
            return SURF
        return self.currentProgressImage
    def gen(self,array:list):
        _surfaces = []
        for color in array:
            
            SURF = Surface(self.size,SRCALPHA)
            rect_draw(
                SURF,
                color,
                (
                    0,
                    0,
                    *self.size
                    ),
                border_radius = self.borderRadius
            )
        
            _surfaces.append(SURF)
        return _surfaces

class UIProgressBar(UIElement):
    def __init__(self, rect: Rect, **kwargs):
        super().__init__(rect, **kwargs)
        UIC.addElement('uiProgressBar')
        self.UX = UXLoadingBar(**UnpackManager('ux',kwargs,{}))
        self.setImage(Surface((1,1)))
    def draw(self,progress):
        self.setImage(self.UX.getCurrentProgress(progress))
    def update(self):
        return super().update()
  