from pygame import Surface, Rect, SRCALPHA
from pygame.draw import rect as rect_draw
from pygame.transform import scale
from pygame.image import load as image_load
from data.modules.ui.ui_element import UIElement, UIC
from data.modules.ui.ux_element import UXElement
class UXImage(UXElement):
    def __init__(self,**options) -> None:
        super().__init__(**options)
        CUTOUT = Surface(self.size,SRCALPHA)
        CUTOUT.fill((0,255,0))
        rect_draw(CUTOUT, (0,0,0,0), (0, 0, *self.size), border_radius=self.border_radius)
        self.CUTOUT = CUTOUT
class UIImage(UIElement):
    """
    The image can be changed by calling the set_sprite method
    """
    def __init__(self, rect: Rect, **kwargs):
        super().__init__(rect, **kwargs)
        UIC.add_element('uiImage')
        self.UX = UXImage(**kwargs.get('ux',{}))
        self.set_image(Surface((1,1)))
    def set_sprite(self,surface):
        
        if isinstance(surface , Surface):
            self.surface = scale(surface,self.dest)
            self.surface.blit(self.UX.CUTOUT,(0,0))
            self.surface.set_colorkey((0,255,0))
        else:
            self.surface = scale(image_load(surface),self.dest)
            self.surface.blit(self.UX.CUTOUT,(0,0))
            self.surface.set_colorkey((0,255,0))
    def update(self):
        return super().update()