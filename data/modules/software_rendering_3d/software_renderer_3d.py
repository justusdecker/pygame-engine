from pygame import Color
from data.modules.software_rendering_3d.object_3d import Object3D
from data.modules.software_rendering_3d.camera_3d import *
from data.modules.software_rendering_3d.projection_3d import *
class SoftwareRenderer:
    def __init__(self,app):
        self.app = app
        self.create_objects()
    def create_objects(self):
        self.camera = Camera(self,[0.5,1,-4])
        self.projection = Projection(self)
        self.object = Object3D(self)
        self.object.translate([0.2,0.4,0.2])
        self.object.rotate_y(pi / 6)
    def draw(self):
        self.app.window.surface.fill(Color('#242424'))
        self.camera.control()
        self.object.draw()