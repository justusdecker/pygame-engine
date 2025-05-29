from numpy import array as ndarray,uint8
from json import dumps
from pygame.surfarray import array3d
from pygame.image import load as imgload
class Surfarray: 
    dimensions : tuple[int, int, int]
    def __init__(self,
                 size: tuple[int,int],
                 alpha: bool = False):
        pass

class Surfarray:
    def __init__(self,
                 size: tuple[int,int],
                 alpha: bool = False):
        self.dimensions : tuple[int, int, int] = (*size,4 if alpha else 3)
        
        self.array = ndarray([0 for i in range(self.dimensions[0] * self.dimensions[1] * self.dimensions[2])]).reshape(([*self.dimensions]))
    def load_from_file(self,file_path: str):
        self.array = array3d(imgload(file_path)) #we will currently use the pygame method to load images. Will be changed later
        self.dimensions = tuple(self.array.shape)
        return self
    def blit(self,surface: Surfarray,pos: tuple[int, int]) -> bool:
        """
        Will blit some another array onto this!
        """
        x,y = pos
        x,y = x-1,y-1
        w,h,_ = surface.dimensions

        if (x + w < 0 and y + h < 0) or (x > surface.dimensions[0] and y > surface.dimensions[1]):
            return False
        for offset_x in range(surface.dimensions[0]):
            for offset_y in range(surface.dimensions[1]):
                if x + offset_x >= 0 and y + offset_y >= 0 and x + offset_x < self.dimensions[0] and y + offset_y < self.dimensions[1]:
                    self.array[x+offset_x][y+offset_y] = surface.array[offset_x][offset_y]
        return True

    def fill(self,color: tuple[int, int, int], area: tuple[int, int, int, int] | None = None):
        if area is not None:
            if len(color) != self.dimensions[2]: raise Exception(f"color doesn't match dimensions: {len(color)} {self.dimensions[2]}")
        color = tuple(uint8(i) for i in color)
        if area is not None:
            x, y, w, h = area
            self.array[x:x+w, y:y+h] = color
        else:
            self.array[:][:] = color

    def get_array(self) -> ndarray:
        return self.array
    def __str__(self):
        return f'Surfarray({self.dimensions})'