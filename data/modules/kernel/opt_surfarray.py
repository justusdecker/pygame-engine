from numpy import array as ndarray,uint8
from json import dumps
from pygame.surfarray import array3d, make_surface
from pygame.image import load as imgload
from cv2 import resize as arrayresize
from pygame import Surface
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
        self.dimensions = tuple([int(i) for i in self.dimensions])
        self.array = ndarray([0 for i in range(self.dimensions[0] * self.dimensions[1] * self.dimensions[2])]).reshape(([*self.dimensions]))
    def load_from_file(self,file_path: str):
        self.array = array3d(imgload(file_path)) #we will currently use the pygame method to load images. Will be changed later
        self.dimensions = tuple(self.array.shape)
        return self
    def load_from_surface(self,surface: Surface):
        self.array = array3d(surface) #we will currently use the pygame method to load images. Will be changed later
        self.dimensions = tuple(self.array.shape)
        return self
    def subarray(self, area: tuple[int, int, int, int]):
        arr = Surfarray((area[2],area[3]))
        arr.blit(self,(area[0],area[1]))
        return arr
    def resize(self,size: tuple[int,int]):
        w,h = size
        w,h = int(w), int(h)
        arr = arrayresize(self.array,(w,h))
        return arr
    def setarray(self,arr: ndarray):
        pass
    def blit(self,surface: Surfarray,pos: tuple[int, int]) -> bool:
        """
        Will blit some another array onto this!
        """
        x,y = pos
        x,y = int(x-1),int(y-1)
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
        color = tuple(int(i) for i in color)
        if area is not None:
            x, y, w, h = area
            x, y, w, h = int(x), int(y), int(w), int(h)
            self.array[x:x+w, y:y+h] = color
        else:
            self.array[:][:] = color
    def get_surface(self) -> ndarray:
        return make_surface(self.array)
    def get_array(self) -> ndarray:
        return self.array
    def __str__(self):
        return f'Surfarray({self.dimensions})'