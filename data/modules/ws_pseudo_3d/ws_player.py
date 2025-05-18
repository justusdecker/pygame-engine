import pygame as pg
import math
from data.modules.constants import GLOBAL_DELTA_TIME,WIDTH,HEIGHT

class Player:
    speed = 1.6
    rot_speed = .6
    scale = .2
    def __init__(self,app):
        self.app = app
        self.x , self.y = 1.5, 5
        self.angle = 0
    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0,0
        speed = GLOBAL_DELTA_TIME.get() * self.speed
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a
        
        keys = pg.key.get_pressed()
        
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        elif keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos
        elif keys[pg.K_d]:
            dx += -speed_sin
            dy += speed_cos
        self.check_wall_collision(dx,dy)
        if keys[pg.K_LEFT]:
            self.angle -= self.rot_speed * GLOBAL_DELTA_TIME.get()
        elif keys[pg.K_RIGHT]:
            self.angle += self.rot_speed * GLOBAL_DELTA_TIME.get()
        self.angle %= math.tau
    def draw(self):
        
        
        #pg.draw.line(self.app.window.surface,'yellow',(self.x*100,self.y*100),(self.x*100+WIDTH* math.cos(self.angle),
        #                                                                       self.y*100+WIDTH* math.sin(self.angle)),2)
        pg.draw.circle(self.app.window.surface,'green',(self.x*100,self.y*100),15)
    def check_wall(self,x,y):
        return (x,y) not in self.app.map.world_map
    def check_wall_collision(self,dx,dy):
        scale = self.scale / (GLOBAL_DELTA_TIME.get() + 0.000001)
        if self.check_wall(int(self.x + dx * scale),int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x),int(self.y + dy * scale)):
            self.y += dy
    def update(self):
        self.movement()
    @property
    def pos(self):
        return self.x, self.y
    @property
    def map_pos(self):
        return int(self.x), int(self.y)