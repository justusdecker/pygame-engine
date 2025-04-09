from pygame.display import set_mode,update as display_update
from pygame import Surface
from data.modules.constants import RESOLUTION
class Window:
    def __init__(self):
        self.surface = set_mode(RESOLUTION)
    def render(self,
               object:Surface,
               pos:tuple[int,int],
               offset:tuple[int,int]):
        self.surface.blit(object,(pos[0] + offset[0],pos[1] + pos[1]))
    def update(self):
        display_update()