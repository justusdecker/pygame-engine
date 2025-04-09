from data.modules.ui.ui_element import UIElement, UIC
from pygame import Surface, Rect, Color, SRCALPHA
from pygame.draw import rect as rect_draw
from data.modules.constants import MEDIUM_BACKGROUND_COLOR,DEFAULT_BACKGROUND_COLOR
class UXLoadingBar:
    def __init__(self,**options) -> None:
        self.size = options.get('size',(512,24))
        self.border_radius = options.get('border_radius',15)
        self.bar_color = options.get('bar_color',Color(MEDIUM_BACKGROUND_COLOR))
        self.bg_color = options.get('bg_color',Color(DEFAULT_BACKGROUND_COLOR))
        self.bg,self.bar = self.gen([self.bg_color,self.bar_color])
        self.current_progress = 0
        self.current_progress_image = self.bg.copy()
    def get_current_progress(self,percent:float):
        if percent != self.current_progress:
            self.current_progress = percent
            SURF:Surface = self.bg.copy()
            max = self.bg.get_width()
            SURF.blit(self.bar,(0,0),area=(0,0,int(percent * max),self.bg.get_height()))
            self.current_progress_image = SURF
            return SURF
        return self.current_progress_image
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
                border_radius = self.border_radius
            )
        
            _surfaces.append(SURF)
        return _surfaces

class UIProgressBar(UIElement):
    def __init__(self, rect: Rect, **kwargs):
        super().__init__(rect, **kwargs)
        UIC.add_element('uiProgressBar')
        self.UX = UXLoadingBar(**kwargs.get('ux',{}))
        self.set_image(Surface((1,1)))
    def draw(self,progress):
        self.set_image(self.UX.get_current_progress(progress))
    def update(self):
        return super().update()
  