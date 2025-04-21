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
class Entity(Sprite):
    def __init__(self,
                 app,
                 image_path_or_surface:str | Surface,
                 vector: Vector4):
        super().__init__(app,image_path_or_surface,vector)
    def check_line_collision(self,obj:Entity,collider_side:int=0) -> bool:
        #Vector2
        """
        x,y,w,h from to
        """
        match collider_side:
            case 0:
                A = int(self.vector.x <= obj.vector.x + obj.vector.z)
                B = int(self.vector.y <= obj.vector.y)
                C = int(self.vector.y + self.vector.w >= obj.vector.y - obj.vector.w)
                return A and B and C
                    
            case 1:
                A = int(self.vector.x + self.vector.z >= obj.vector.x)
                B = int(self.vector.y <= obj.vector.y)
                C = int(self.vector.y + self.vector.w >= obj.vector.y - obj.vector.w)
                return A and B and C


        
    def check_rect_collision(self,obj:Entity) -> bool:
        x1,x2,y1,y2 = self.vector.x,obj.vector.x,self.vector.y,obj.vector.y
        w1,w2,h1,h2 = self.vector.z,obj.vector.z,self.vector.w,obj.vector.w
        #Calculation Matrix
        return x1 + w1 >= x2 and \
        x1 <= x2 + w2 and \
        y1 + h1 >= y2 and \
        y1 <= y2 + h2
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
