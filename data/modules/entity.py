from data.modules.sprite import Sprite
from data.modules.vector import Vector4
from data.modules.constants import WIDTH,HEIGHT
from pygame import Surface
class Entity(Sprite):
    def __init__(self,
                 app,
                 image_path_or_surface:str | Surface,
                 vector: Vector4):
        super().__init__(app,image_path_or_surface,vector)
    def collision_mbts(self):
        """
        move back to screen
        """
        if self.vector.x < 0:
            self.vector.x = 0
        if self.vector.y < 0:
            self.vector.y = 0
        if self.vector.x + self.vector.z > WIDTH:
            self.vector.x = WIDTH - self.vector.z
        if self.vector.y + self.vector.w > HEIGHT:
            self.vector.y = HEIGHT - self.vector.w
