from data.modules.platformer_rendering.tileset import TileSet
from data.modules.vector import Vector2
from pygame import Surface
from random import randint
class TileMap:
    def __init__(self,app,surf: Surface,tile_size: Vector2,scaled_size: Vector2,t_map:list[list[int]]):
        self.t_map = [[randint(0,4) for i in range(64)] for x in range(36)]

        self.pos = Vector2(0,0)
        self.tileset = TileSet(app,surf,tile_size,scaled_size)
    def render(self):
        for idy,y in enumerate(self.t_map):
            for idx,x in enumerate(y):
                self.tileset.render(Vector2(idx * self.tileset.scaled_size.x,idy * self.tileset.scaled_size.y),x)