from data.modules.ui.ui_element import UIElement, UIC
from pygame import Surface, image
from pygame.draw import rect as rect_draw
from data.modules.ui.ux_element import UXElement
from data.modules.vector import Vector4
from data.modules.constants import DEFAULT_BACKGROUND_COLOR,MEDIUM_BACKGROUND_COLOR
class UXLoadingBar(UXElement):
    def __init__(self,**options) -> None:
        self.current_progress = 0
        super().__init__(**options)
        g = [
                [[0,self.background_color_group.get(0),Vector4(0,0,*self.size)]],
                [[0,self.background_color_group.get(1),Vector4(0,0,*self.size)]]
        ]
        self.background, self.foreground = self.gen(g,2)
    def set_progress(self,percent:float,orfirst:bool=False):
        if percent != self.current_progress or orfirst:
            self.current_progress = percent
            SURF:Surface = self.background.copy()
            max = self.background.get_width()
            SURF.blit(self.foreground,(0,0),area=(0,0,int(percent * max),self.background.get_height()))
            self.current_progress_image = SURF
        return self.current_progress_image

class UIProgressBar(UIElement):
    def __init__(self, rect: Vector4, **kwargs):
        super().__init__(rect, **kwargs)
        UIC.add_element('uiProgressBar')
        self.UX = UXLoadingBar(**kwargs.get('ux',{}))
        self.render(self.UX.current_progress,True)
    def render(self,progress,orfirst:bool=False):
        self.set_image(self.UX.set_progress(progress,orfirst))
    def update(self):
        return super().update()
  