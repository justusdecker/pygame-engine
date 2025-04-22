from data.modules.log import LOG
from data.modules.constants import *
from data.modules.app import Application
from data.modules.ui.ui_element import UIM
from data.modules.ui.ui_label import UILabel
from data.modules.entity import Entity
from data.modules.vector import Vector2,Vector4
from pygame import Surface,K_w,K_s,K_UP,K_DOWN
from pygame.key import get_pressed
LOG.tobash = False
class App(Application):
    def __init__(self): 
        super().__init__()
        surf = Surface((WIDTH*.025,HALF_HEIGHT))
        surf.fill((36,36,36))
        self.bar_left = Entity(self,surf,Vector4(20,20,WIDTH*.025,HALF_HEIGHT))
        self.bar_right = Entity(self,surf,Vector4(WIDTH-20-(WIDTH*.025),20,WIDTH*.025,HALF_HEIGHT))
        surf = Surface((WIDTH*.025,WIDTH*.025))
        surf.fill((48,48,48))
        self.ball = Entity(self,surf,Vector4(HALF_WIDTH-(WIDTH*.025),HALF_HEIGHT-(WIDTH*.025),WIDTH*.025,WIDTH*.025))
        self.reset()
    def reset(self):
        self.move = Vector2(10,10)
        self.ball.vector = Vector4(HALF_WIDTH-(WIDTH*.025),HALF_HEIGHT-(WIDTH*.025),WIDTH*.025,WIDTH*.025)
    def set_move(self,v:Vector2):
        self.move *= v
        return self.move
    def x_change(self,st:bool):
        if st: self.ball.vector += self.set_move(Vector2(-1,1))
    def y_change(self,st:bool):
        if st: self.ball.vector += self.set_move(Vector2(1,-1))
    def key_check(self):#! refactor this
        KEYS = get_pressed()
        if KEYS[K_w]: self.bar_left.vector += Vector2(0,-5)
        elif KEYS[K_s]: self.bar_left.vector += Vector2(0,5)
        if KEYS[K_UP]: self.bar_right.vector += Vector2(0,-5)
        elif KEYS[K_DOWN]: self.bar_right.vector += Vector2(0,5)
    def run(self):
        while self.is_running:
            GLOBAL_DELTA_TIME.before()
            self.CLK.tick(60)
            self.window.surface.fill((0,0,0))
            self.key_check()
            self.bar_left.collision_mbts()
            self.bar_right.collision_mbts()
            self.bar_left.render()#! Will be moved to the Entity Render
            self.bar_right.render()#! Will be moved to the Entity Render
            self.ball.render()#! Will be moved to the Entity Render
            self.x_change(self.bar_left.check_line_collision(self.ball,1))
            self.x_change(self.bar_right.check_line_collision(self.ball,0))
            self.x_change(self.ball.vector.x < 0 or self.ball.vector.x + self.ball.vector.z > WIDTH)
            self.y_change(self.ball.vector.y < 0 or self.ball.vector.y + self.ball.vector.w > HEIGHT)
            self.ball.vector += self.move
            if self.ball.vector.x < 20: self.reset()
            if self.ball.vector.x + self.ball.vector.z > WIDTH - 20: self.reset()
            self.update()
            GLOBAL_DELTA_TIME.after()
if __name__ == "__main__":
    App().run()