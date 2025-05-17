from data.modules.vector import Vector2
from pygame import Surface, SRCALPHA
class TileSet:
    def __init__(self,app,surf:Surface, tile_size: Vector2,include_alpha: bool = True):
        self.tiles = []
        self.app = app
        print(surf.get_width()//tile_size.x,surf.get_width()//tile_size.y)
        for x in range(surf.get_width()//tile_size.x):
            for y in range(surf.get_height()//tile_size.y):
                _x,_y = x * tile_size.x, y * tile_size.y
                SURF = Surface(tile_size.to_list(), SRCALPHA) if include_alpha else Surface(tile_size.to_list())
                SURF.blit(surf,(0,0),(_x,_y,tile_size.x,tile_size.y))
                self.tiles.append(SURF)
    def get(self,id:int):
        if id < len(self.tiles):
            return self.tiles[id]
        else:
            return self.tiles[0]
    def render(self,pos:Vector2,id:int):
        self.app.window.render(self.get(id),pos.to_list())
                