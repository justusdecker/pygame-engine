from numpy import array as ndarray,uint8
from json import dumps
from pygame.surfarray import array3d, make_surface
from pygame.image import load as imgload
from cv2 import resize as arrayresize, INTER_AREA as INTERPOLATION_CV2
from data.modules.testing.result_tests import surfarray_result_check
from pygame import Surface

from numba import jit

class int3:
    def __init__(self,r:int,g:int,b:int):
        self.r, self.g, self.b = r, g, b

class Surfarray: 
    dimensions : tuple[int, int, int]
    def __init__(self,
                 size: tuple[int,int],
                 alpha: bool = False):
        pass

# Testing System:
"""
create
scale
blit
fill
pos:
    floats must be converted to int

"""


class Surfarray:
    def __init__(self,
                 size: tuple[int,int] = (1,1),
                 alpha: bool = False):
        self.dimensions : tuple[int, int, int] = (*size,4 if alpha else 3)
        self.dimensions = tuple([int(i) for i in self.dimensions])
        self.array = ndarray([0 for i in range(self.dimensions[0] * self.dimensions[1] * self.dimensions[2])],dtype=uint8).reshape(([*self.dimensions]))
    

    def load_from_file(self,file_path: str):
        self.array = array3d(imgload(file_path)) #we will currently use the pygame method to load images. Will be changed later
        self.dimensions = tuple(self.array.shape)
        return self
    
    def load_from_surface(self,surface: Surface):
        self.array = array3d(surface) #we will currently use the pygame method to load images. Will be changed later
        self.dimensions = tuple(self.array.shape)
        return self
    
    def load_from_array(self,arr: ndarray):
        self.array = arr
        self.dimensions = tuple(self.array.shape)
        return self
    
    def subarray(self, area: tuple[int, int, int, int]):
        arr = Surfarray((area[2],area[3]))
        #print(area[2],area[3])
        #arr.blit(self,(area[0],area[1])) # !here is the error!
        #print(area[0] , area[2] , area[1] , area[3],arr.array.shape, self.array.shape)
        area = [int(i) for i in area]
        arr.array = self.array[area[0] : area[0] + area[2] , area[1] : area[1] + area[3]].copy()
        #sprint(area[0],area[1])
        return arr

    def resize(self,size: tuple[int,int]):
        w,h = size
        w,h = int(w), int(h)
        self.array = arrayresize(self.array.astype(uint8),(w,h),interpolation=INTERPOLATION_CV2) # .> self.array.astype(uint8) this i only a failsave
        self.dimensions = self.array.shape
        return self
    
    @jit
    def fastblit(a: Surfarray, b: Surfarray,dim_a: tuple[int, int, int], dim_b: tuple[int, int, int], pos: tuple[int, int]) -> bool:
        x,y = pos
        x,y = int(x-1),int(y-1)
        w,h,_ = dim_b

        if (x + w < 0 and y + h < 0) or (x > w and y > h):
            return a
        for offset_x in range(w):
            for offset_y in range(h):
                if x + offset_x >= 0 and y + offset_y >= 0 and x + offset_x < dim_a[0] and y + offset_y < dim_a[1]:
                    a[x+offset_x][y+offset_y] = b[offset_x][offset_y]
        return a
    
    def blit(self,surface: Surfarray,pos: tuple[int, int]) -> bool:
        """
        Will blit some another array onto this!
        """
        self.array = Surfarray.fastblit(self.array,surface.array,self.dimensions,surface.dimensions,pos)

    def fastfill(arr, color, area):
        color = [uint8(i) for i in color]
        if area is not None:
            x, y, w, h = area
            x, y, w, h = int(x), int(y), int(w), int(h)
            arr[x:x+w, y:y+h] = color
        else:
            arr[:][:] = color
        return arr
    
    def fast_col_mul(arr, multiplicator: float,shape):
        for x in range(shape[0]):
            for y in range(shape[1]):
                for z in range(shape[2]):
                    arr[x][y][z] *= multiplicator
                    arr[x][y][z] = uint8(arr[x][y][z])
                    if arr[x][y][z] > 255:
                        arr[x][y][z] = 255
        return arr
            
    def color_multiplication(self,multiplicator: float):
        Surfarray.fast_col_mul(self.array,multiplicator,self.array.shape)
    
    
    def fill(self,color: tuple[int, int, int], area: tuple[int, int, int, int] | None = None):
        if area is not None:
            if len(color) != self.dimensions[2]: raise Exception(f"color doesn't match dimensions: {len(color)} {self.dimensions[2]}")
        self.array = Surfarray.fastfill(self.array,color,area)
    
    def get_surface(self) -> ndarray:
        return make_surface(self.array)
    
    def get_array(self) -> ndarray:
        return self.array
    
    def __str__(self):
        return f'Surfarray({self.dimensions})'