from numpy import array as ndarray,uint8
from pygame import Surface,surfarray

def gamma_correction(surface: Surface, scale: float) -> Surface:
    """
    All of the rgb values will be multiplied by ``scale``
    """
    array = surfarray.array3d(surface)
    for x in range(surface.width):
        for y in range(surface.height):
            for z in range(3):
                c = array[x][y][z] * scale
                array[x][y][z] = c if c <= 255 else 255
    return surfarray.make_surface(array)

def invert_rgb(surface: Surface) -> Surface:
    """
    All pixels will be inverted
    """
    array = surfarray.array3d(surface)
    for x in range(surface.width):
        for y in range(surface.height):
            for z in range(3):
                array[x][y][z] = uint8((255 - int(array[x][y][z])) % 256)
    return surfarray.make_surface(array)
def blending_mul(surface_a: Surface, surface_b: Surface):
    """
    a & b must have the same size
    (col_a * col_b) % 256
    """
    array_a = surfarray.array3d(surface_a)
    array_b = surfarray.array3d(surface_b)
    
    for x in range(surface_a.width):
        for y in range(surface_a.height):
            for z in range(3):
                a = int(array_a[x][y][z])
                b = int(array_b[x][y][z])
                c = uint8((a * b) / 256)
                array_a[x][y][z] = c
    return surfarray.make_surface(array_a)