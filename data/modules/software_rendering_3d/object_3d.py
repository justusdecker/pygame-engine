from data.modules.matrix_functions import *
from numpy import any as np_any
from data.modules.constants import HALF_WIDTH,HALF_HEIGHT
from pygame.draw import polygon as poly_draw, circle as circle_draw
from pygame import Color
class Object3D:
    def __init__(self, render):
        self.render = render
        self.vertexes = array([(0,0,0,1),(0,1,0,1),(1,1,0,1),(1,0,0,1),
                               (0,0,1,1),(0,1,1,1),(1,1,1,1),(1,0,1,1)])
        self.faces = array([(0,1,2,3),(4,5,6,7),(0,4,5,1),(2,3,7,6),(1,2,6,5),(0,3,7,4)])
    def draw(self):
        self.screen_projection()
    def screen_projection(self):
        vertexes = self.vertexes @ self.render.camera.camera_matrix()
        vertexes = vertexes @ self.render.projection.projection_matrix
        vertexes /= vertexes[:, -1].reshape(-1,1)
        vertexes[((vertexes > 1) | (vertexes < -1))] = 0
        vertexes = vertexes @ self.render.projection.to_screen_matrix
        vertexes = vertexes[:, :2]
        for face in self.faces:
            polygon = vertexes[face]
            if not np_any((polygon == HALF_WIDTH) | (polygon == HALF_HEIGHT)):
                poly_draw(self.render.app.window.surface,Color('#256256'), polygon,3)
        for vertex in vertexes:
            if not np_any((vertex == HALF_WIDTH) | (vertex == HALF_HEIGHT)):
                circle_draw(self.render.app.window.surface,Color('#128512'),vertex,6)
    def translate(self,pos):
        self.vertexes = self.vertexes @ translate(pos)
    def scale(self,scale_to):
        self.vertexes = self.vertexes @ scale(scale_to)
    def rotate_x(self,angle):
        self.vertexes = self.vertexes @ rotate_x(angle)
    def rotate_y(self,angle):
        self.vertexes = self.vertexes @ rotate_y(angle)
    def rotate_z(self,angle):
        self.vertexes = self.vertexes @ rotate_z(angle)