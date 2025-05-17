from data.modules.constants import *
from data.modules.app import Application
from data.modules.platformer_rendering.tileset import TileSet
from data.modules.vector import Vector2
from pygame.image import load
import pygame.key as keys
def test_print(*args):
    print(args, "Hello World!")


class App(Application):
    def __init__(self):
        super().__init__()
        self.tileset = TileSet(self,load('data\\bin\\img\\test_tileset.png'),Vector2(16,16))
    def run(self):

        while self.is_running:
            GLOBAL_DELTA_TIME.before()
            self.window.surface.fill((36,36,36))
            self.tileset.render(Vector2(100,100),2)
            self.update()
            GLOBAL_DELTA_TIME.after()
if __name__ == "__main__":
    APP = App()
    APP.run()