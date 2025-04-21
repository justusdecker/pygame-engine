from pygame import Surface
from pygame.image import load as load_image
from data.modules.vector import Vector4
class Sprite:
    def __init__(self,
                 app,
                 image_path_or_surface:str | Surface,
                 vector: Vector4 = Vector4(0,0,1,1)):
        self.app = app
        self.vector = vector
        self.surface = Surface(vector.to_list()[2:])
        if isinstance(image_path_or_surface,str):
            self.surface = load_image(image_path_or_surface)
        else:
            self.surface = image_path_or_surface
    def render(self):
        x,y,*_ = self.vector.to_list()
        self.app.window.render(self.surface,(x,y))