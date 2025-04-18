from pygame import Surface
from pygame.image import load as load_image
from data.modules.vector import Vector4
class Sprite:
    def __init__(self,
                 image_path:str,
                 vector: Vector4 = Vector4(0,0,1,1)):
        self.vector = vector
        self.surface = load_image(image_path)