from data.modules.constants import *
from data.modules.app import Application
from data.modules.platformer_rendering.tileset import TileSet
from data.modules.platformer_rendering.tilemap import TileMap
from data.modules.vector import Vector2
from data.modules.ws_pseudo_3d.ws_map import Map
from data.modules.ws_pseudo_3d.ws_player import Player
from data.modules.ws_pseudo_3d.ws_ray_casting import RayCasting
from data.modules.ws_pseudo_3d.ws_object_renderer import ObjectRenderer
from data.modules.ws_pseudo_3d.ws_sprite_object import SpriteObject, AnimatedSprite
from pygame.mouse import set_visible
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
        set_visible(False)
        self.new_game()
    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.static_sprite = SpriteObject(self,'data\\bin\\img\\soul_stone_animated\\soul_stone_f1.png')
        self.animated_sprite = AnimatedSprite(self,'data\\bin\\img\\soul_stone_animated\\soul_stone_f1.png',(5.5,3.5))
    def run(self):

        while self.is_running:
            GLOBAL_DELTA_TIME.before()
            #self.window.surface.fill((36,36,36))
            #self.map.draw()
            self.player.update()
            self.raycasting.update()
            self.static_sprite.update()
            self.animated_sprite.update()
            self.object_renderer.draw()
            self.update()
            GLOBAL_DELTA_TIME.after()
if __name__ == "__main__":
    APP = App()
    APP.run()