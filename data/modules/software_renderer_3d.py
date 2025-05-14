from pygame import Color
from data.modules.object_3d import Object3D
class SoftwareRenderer:
    def __init__(self,app):
        self.app = app
        self.create_objects()
    def create_objects(self):
        self.object = Object3D()
    def draw(self):
        self.app.window.surface.fill(Color('#242424'))