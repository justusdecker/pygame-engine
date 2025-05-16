from data.modules.matrix_functions import *
from data.modules.constants import HEIGHT,WIDTH,GLOBAL_DELTA_TIME
from math import pi
from pygame.key import get_pressed
from pygame import K_a,K_d,K_w,K_s,K_e,K_q,K_LEFT,K_RIGHT,K_UP,K_DOWN
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
        self.moving_speed = 1.2
        self.rotation_speed = 1
    def control(self):
        key = get_pressed()
        if key[K_a]:
            self.position -= self.right * self.moving_speed * GLOBAL_DELTA_TIME.get()
        elif key[K_d]:
            self.position += self.right * self.moving_speed * GLOBAL_DELTA_TIME.get()
        if key[K_w]:
            self.position += self.forward * self.moving_speed * GLOBAL_DELTA_TIME.get()
        elif key[K_s]:
            self.position -= self.forward * self.moving_speed * GLOBAL_DELTA_TIME.get()
        if key[K_q]:
            self.position -= self.up * self.moving_speed * GLOBAL_DELTA_TIME.get()
        elif key[K_e]:
            self.position += self.up * self.moving_speed * GLOBAL_DELTA_TIME.get()
        if key[K_LEFT]:
            self.camera_yaw(-self.rotation_speed)
        elif key[K_RIGHT]:
            self.camera_yaw(self.rotation_speed)
        if key[K_UP]:
            self.camera_pitch(-self.rotation_speed)
        elif key[K_DOWN]:
            self.camera_pitch(self.rotation_speed)
    def camera_yaw(self,angle):
        rotate = rotate_y(angle * GLOBAL_DELTA_TIME.get())
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate
    def camera_pitch(self,angle):
        rotate = rotate_x(angle * GLOBAL_DELTA_TIME.get())
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate
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
            [[rx,ux,fx,0],
            [ry,uy,fy,0],
            [rz,uz,fz,0],
            [0,0,0,1]]
        )
    def camera_matrix(self):
        return self.translate_matrix() @ self.rotate_matrix()