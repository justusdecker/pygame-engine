from pygame.display import set_mode,update as display_update,set_caption,set_icon
from pygame import Surface,image
from data.modules.constants import RESOLUTION, TITLE, ICON_PATH
class Window:
    """
    
    .. surface:: the surface the user can see
    .. render:: the given object will be blitted on pos + offset
    """
    def __init__(self):
        "Sets the caption, resolution & icon"
        self.surface = set_mode(RESOLUTION)
        set_caption(TITLE)
        if ICON_PATH:
            set_icon(image.load(ICON_PATH))
    def render(self,
               object:Surface,
               pos:tuple[int,int] = (0,0),
               offset:tuple[int,int] = (0,0)):
        self.surface.blit(object,(pos[0] + offset[0],pos[1] + offset[1]))
    def update(self):
        display_update()