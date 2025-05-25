from pygame import Surface
from pygame.image import load as load_image
from data.modules.vector import Vector4

class SpriteRenderer:
    def __init__(self):
        self.objects = []
    def add(self,obj):
        self.objects.append(obj)
    def update(self):
        for obj in self.objects:
            obj.render()
SPR = SpriteRenderer()
class Sprite:
    def __init__(self,
                 app,
                 image_path_or_surface:str | Surface,
                 vector: Vector4 = Vector4(0,0,1,1),
                 sprite_renderer = SPR):
        self.app = app
        self.vector = vector
        self.surface = Surface(vector.to_list()[2:])
        sprite_renderer.add(self)
        if isinstance(image_path_or_surface,str):
            self.surface = load_image(image_path_or_surface)
        else:
            self.surface = image_path_or_surface
    def render(self):
        x,y,*_ = self.vector.to_list()
        self.app.window.render(self.surface,(x,y))