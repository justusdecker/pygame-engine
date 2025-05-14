from math import tan
from numpy import array
class Projection:
    def __init__(self,render):
        NEAR = render.camera.near_plane
        FAR = render.camera.far_plane
        RIGHT = tan(render.camera.h_fov / 2)
        LEFT = -RIGHT
        TOP = tan(render.camera.v_fov / 2)
        BOTTOM = -TOP
        
        m00 = 2 / (RIGHT - LEFT)
        m11 = 2 / (TOP - BOTTOM)
        m22 = (FAR + NEAR) / (FAR - NEAR)
        m32 = -2 * NEAR * FAR / (FAR - NEAR)
        self.projection_matrix = array(
            [m00,0,0,0],
            [0,m11,0,0],
            [0,0,m22,1],
            [0,0,m32,0]
        )