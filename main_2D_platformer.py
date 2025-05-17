from data.modules.constants import *
from data.modules.app import Application
from data.modules.platformer_rendering.tileset import TileSet
from data.modules.platformer_rendering.tilemap import TileMap
from data.modules.vector import Vector2
from pygame.image import load
import pygame.key as keys
def test_print(*args):
    print(args, "Hello World!")


class App(Application):
    def __init__(self):
        super().__init__()
        #self.tileset = TileSet(self,load('data\\bin\\img\\test_tileset.png'),Vector2(16,16),Vector2(32,32))
        arr = [[2 for x in range(32)] for i in range(17)]
        arr.append([0 for x in range(32)])
        
        self.tilemap = TileMap(self,load('data\\bin\\img\\test_tileset.png'),Vector2(16,16),Vector2(40,40),arr)
    def run(self):

        while self.is_running:
            GLOBAL_DELTA_TIME.before()
            self.window.surface.fill((36,36,36))
            self.tilemap.render()
            
            self.update()
            GLOBAL_DELTA_TIME.after()
if __name__ == "__main__":
    APP = App()
    APP.run()