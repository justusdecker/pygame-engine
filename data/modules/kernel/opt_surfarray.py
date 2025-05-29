from numpy import array as ndarray,uint8
class Surfarray: 
    dimensions : tuple[int, int, int]
class Surfarray:
    def __init__(self,
                 size: tuple[int,int],
                 alpha: bool = False):
        self.dimensions : tuple[int, int, int] = (*size,4 if alpha else 3)
        
        self.array = ndarray([0 for i in range(self.dimensions[0] * self.dimensions[1] * self.dimensions[2])]).reshape(([*self.dimensions]))
    def blit(self,surface: Surfarray,pos: tuple[int, int]):
        x,y = pos
        w,h = surface.dimensions
        self.array[x:w][y:h] = surface
    def fill(self,color: tuple[int, int, int], area: tuple[int, int, int, int] | None = None):
        if area is not None:
            if len(color) != self.dimensions[2]: raise Exception(f"color doesn't match dimensions: {len(color)} {self.dimensions[2]}")
            color = tuple(uint8(i) for i in color)
        if area is not None:
            x, y, w, h = area
            print(x,x+w,y,y+h)
            self.array[x:x+w][y:y+h] = color
        else:
            self.array[:-1][:-1] = color

    def get_array(self) -> ndarray:
        return self.array
    def __str__(self):
        return f'Surfarray({self.dimensions})'