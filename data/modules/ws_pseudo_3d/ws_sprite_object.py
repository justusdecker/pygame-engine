import pygame as pg
from math import atan2, pi, tau, hypot, cos
from data.modules.ws_pseudo_3d.ws_ray_casting import DELTA_ANGLE, SCALE, H_NUM_RAYS,SCREEN_DIST
from data.modules.constants import WIDTH, HALF_HEIGHT
import os
from collections import deque
from time import time
class SpriteObject:
    def __init__(self, app, path,pos=(4.5,3.5),scale=0.5,shift=0.45):
        self.app = app
        self.player = app.player
        self.x, self.y = pos
        self.image = pg.image.load(path).convert_alpha()
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_H_WIDTH = self.IMAGE_WIDTH // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0,0,0,0,1,1
        self.sprite_half_width = 0
        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = shift
    def get_sprite_projection(self):
        proj = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE
        proj_width, proj_height = proj * self.IMAGE_RATIO,proj
        image = pg.transform.scale(self.image,(proj_width,proj_height))
        
        self.sprite_half_width = proj_height // 2
        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT
        pos = self.screen_x - self.sprite_half_width, HALF_HEIGHT - proj_height // 2 + height_shift
        self.app.raycasting.objects_to_render.append((self.norm_dist,image,pos))
    def get_sprite(self):
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx, self.dy = dx,dy
        self.theta = atan2(dy,dx)
        
        delta = self.theta - self.player.angle
        if (dx > 0 and self.player.angle > pi) or (dx < 0 and dy < 0):
            delta += tau
        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (H_NUM_RAYS + delta_rays) * SCALE
        
        self.dist = hypot(dx,dy)
        self.norm_dist = self.dist * cos(delta)
        
        if -self.IMAGE_H_WIDTH < self.screen_x < (WIDTH + self.IMAGE_H_WIDTH) and self.norm_dist > 0.5:
            self.get_sprite_projection()
        
    def update(self):
        self.get_sprite()


class AnimatedSprite(SpriteObject):
    def __init__(self, app, path:str, pos=(4.5, 3.5), scale=0.5, shift=0.45, animation_time=.1):
        super().__init__(app, path, pos, scale, shift)
        self.animation_time = animation_time
        self.path = path.rsplit('\\',1)[0]
        self.images = self.get_images(self.path)
        self.animation_time_prev = time()
        self.animation_trigger = False
    def update(self):
        super().update()
        self.check_animation_time()
        self.animate(self.images)
    def animate(self,images: deque):
        if self.animation_trigger:
            images.rotate(-1)
            self.image = images[0]
    def check_animation_time(self):
        self.animation_trigger = False
        time_now = time()
        if time_now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = time_now
            self.animation_trigger = True
            
    def get_images(self,path):
        images = deque()
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path,file_name)):
                img = pg.image.load(path + '\\' + file_name).convert_alpha()
                images.append(img)
                
        return images