from matrix_functions import *
from data.modules.constants import HEIGHT,WIDTH
from math import pi
class Camera:
    def __init__(self,render,position):
        self.render = render
        self.position = array([*position,1.0])
        self.forward = array([0,0,1,1])
        self.up = array([0,1,0,1])
        self.right = array([1,0,0,1])
        self.h_fov = pi / 3
        self.v_fov = self.h_fov * (HEIGHT / WIDTH)
        self.near_plane = 0.1
        self.far_plane = 100
        
    def translate_matrix(self):
        x, y, z, w = self.position
        return array([
            [1,0,0,0],
            [0,1,0,1],
            [0,0,1,0],
            [-x,-y,-z,1]
        ])
    def rotate_matrix(self):
        rx, ry, rz, w = self.right
        fx, fy, fz, w = self.forward
        ux, uy, uz, w = self.up
        
        return array(
            [rx,ux,fx,0],
            [ry,uy,fy,0],
            [rz,uz,fz,0],
            [0,0,0,1]
        )
    def camera_matrix(self):
        return self.translate_matrix @ self.rotate_matrix()