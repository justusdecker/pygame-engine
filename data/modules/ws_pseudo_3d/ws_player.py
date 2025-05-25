import pygame as pg
import math
from data.modules.constants import GLOBAL_DELTA_TIME,WIDTH
from data.modules.ws_pseudo_3d.ws_constants import HEIGHT,HALF_WIDTH,HALF_HEIGHT
MOUSE_SENSITIVITY = 0.3
MOUSE_MAX_REL = 40
MOUSE_BORDER_LEFT = 100
MOUSE_BORDER_RIGHT = WIDTH - MOUSE_BORDER_LEFT

class Player:
    speed = 1.6
    rot_speed = .6
    scale = .2
    def __init__(self,app):
        self.app = app
        self.x , self.y = 1.5, 5
        self.angle = 0
        self.shot = False
        self.moving = False

    def step_sounds(self):
        """ Will be added soon!"""
    def single_fire_event(self):
        if pg.mouse.get_pressed()[0]:
            if not self.shot and not self.app.weapon.reloading:
                self.app.sound.play_sound('attack')
                self.shot = True
                self.app.weapon.reloading = True
    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0,0
        speed = GLOBAL_DELTA_TIME.get() * self.speed
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a
        
        keys = pg.key.get_pressed()
        self.moving = False
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
            self.moving = True
        elif keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin
            self.moving = True
        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos
            self.moving = True
        elif keys[pg.K_d]:
            dx += -speed_sin
            dy += speed_cos
            self.moving = True
        self.check_wall_collision(dx,dy)
        """if keys[pg.K_LEFT]:
            self.angle -= self.rot_speed * GLOBAL_DELTA_TIME.get()
        elif keys[pg.K_RIGHT]:
            self.angle += self.rot_speed * GLOBAL_DELTA_TIME.get()"""
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
    def mouse_control(self):
        mx,my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH,HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * GLOBAL_DELTA_TIME.get()
    def update(self):
        self.movement()
        self.mouse_control()
        self.step_sounds()
    @property
    def pos(self):
        return self.x, self.y
    @property
    def map_pos(self):
        return int(self.x), int(self.y)