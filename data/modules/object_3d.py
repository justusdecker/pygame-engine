from data.modules.matrix_functions import *
from numpy import any as np_any
from data.modules.constants import HALF_WIDTH,HALF_HEIGHT
from pygame.draw import polygon as poly_draw
from pygame import Color
class Object3D:
    def __init__(self, render):
        self.render = render
        self.vertexes = array([(0,0,0,1),(0,1,0,1),(1,1,0,1),(1,0,0,1),
                               (0,0,1,1),(0,1,1,1),(1,1,1,1),(1,0,1,1)])
        self.faces = array([(0,1,2,3),(4,5,6,7),(0,4,5,1),(2,3,7,6),(1,2,6,5),(0,3,7,4)])
    def screen_projection(self):
        vertexes = self.vertexes @ self.render.camera.camera_matrix()
        vertexes @= self.render.projection.projection_matrix()
        vertexes /= vertexes[: -1].reshape(-1,1)
        vertexes[(vertexes > 1 | vertexes < -1)] = 0
        vertexes @= self.render.projection.to_screen_matrix()
        vertexes = vertexes[:, :2]
        for face in self.faces:
            polygon = vertexes[face]
            if not np_any(polygon == HALF_WIDTH | polygon == HALF_HEIGHT):
                poly_draw(self.app.window.surface,Color('#256256'), polygon,3)
    def translate(self,pos):
        self.vertexes @= translate(pos)
    def scale(self,scale_to):
        self.vertexes @= scale(scale_to)
    def rotate_x(self,angle):
        self.vertexes @= rotate_x(angle)
    def rotate_y(self,angle):
        self.vertexes @= rotate_y(angle)
    def rotate_z(self,angle):
        self.vertexes @= rotate_z(angle)