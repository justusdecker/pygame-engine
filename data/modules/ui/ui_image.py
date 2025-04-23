from pygame import Surface, Rect, SRCALPHA
from pygame.draw import rect as rect_draw
from pygame.transform import scale
from pygame.image import load as image_load
from data.modules.ui.ui_element import UIElement, UIC
class UXImage:
    def __init__(self,**options) -> None:
        self.size = options.get('size',(384,216))
        self.border_radius = options.get('border_radius',15)
        CUTOUT = Surface(self.size,SRCALPHA)
        CUTOUT.fill((0,255,0))
        rect_draw(CUTOUT,
                     (0,0,0,0),
                     (0,
                      0,
                      *self.size
                      ),
                        border_radius=self.border_radius
                        )
        self.CUTOUT = CUTOUT
        
class UIImage(UIElement):
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