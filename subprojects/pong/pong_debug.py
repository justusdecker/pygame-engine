from data.modules.log import LOG
from data.modules.constants import *
from data.modules.app import Application
from data.modules.ui.ui_element import UIM
from data.modules.ui.ui_label import UILabel
from data.modules.entity import Entity
from data.modules.sprite import SPR
from data.modules.vector import Vector2,Vector4
from data.modules.ui.ui_font import FONT
from pygame import Rect
from pygame import Surface,K_w,K_s,K_UP,K_DOWN
from pygame.draw import line as line_draw
from pygame.transform import flip
from math import sin

from pygame.key import get_pressed
LOG.tobash = False
class App(Application):
    def __init__(self): 
        super().__init__()
        surf = Surface((WIDTH*.025,HALF_HEIGHT))
        for x in range(surf.get_width()):
            line_draw(surf,(96+x,48+x,48+x),(x,0),(x,surf.get_height()))

        self.bar_left = Entity(self,surf,Vector4(20,20,WIDTH*.025,HALF_HEIGHT))
        surf = flip(surf,True,False)
        self.bar_right = Entity(self,surf,Vector4(WIDTH-20-(WIDTH*.025),20,WIDTH*.025,HALF_HEIGHT))
        surf = Surface((WIDTH*.025,WIDTH*.025))
        
        surf.fill((96+x,48+x,48+x))
        self.ball = Entity(self,surf,Vector4(HALF_WIDTH-(WIDTH*.025),HALF_HEIGHT-(WIDTH*.025),WIDTH*.025,WIDTH*.025))
        self.reset()
        self.scores = [0,0]
        
        self.score_label = UILabel(Rect(HALF_WIDTH-(QUARTER_WIDTH//2),0,QUARTER_WIDTH,HEIGHT*.1),ux={'size':(QUARTER_WIDTH,HEIGHT*.1),'font':FONT(size=40),'bcg': ['#482424'],'tcg': ['#969696'],'text': '0:0'})
        self.flash_frames = 0
        self.background_color_mul = 0
        
    def reset(self):
        self.speed = 1
        self.move = Vector2(10,10)
        self.ball.vector = Vector4(HALF_WIDTH-(WIDTH*.025),HALF_HEIGHT-(WIDTH*.025),WIDTH*.025,WIDTH*.025)
    def set_move(self,v:Vector2):
        self.move *= v
        return self.move
    def x_change(self,st:bool):
        if st: self.ball.vector += self.set_move(Vector2(-1*self.speed,1*self.speed))
    def y_change(self,st:bool):
        if st: self.ball.vector += self.set_move(Vector2(1*self.speed,-1*self.speed))
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
            self.background_color_mul += GLOBAL_DELTA_TIME.get()
            if self.flash_frames:
                col = (128,128,128)
                self.flash_frames -= 1
            else: 
                col = [50 * abs(sin(self.background_color_mul)),25 * abs(sin(self.background_color_mul)),25 * abs(sin(self.background_color_mul))]
            
            self.window.surface.fill(col)
            self.key_check()
            self.bar_left.collision_mbts()
            self.bar_right.collision_mbts()
            self.x_change(self.bar_left.check_line_collision(self.ball,1))
            self.x_change(self.bar_right.check_line_collision(self.ball,0))
            self.x_change(self.ball.vector.x < 0 or self.ball.vector.x + self.ball.vector.z > WIDTH)
            self.y_change(self.ball.vector.y < 0 or self.ball.vector.y + self.ball.vector.w > HEIGHT)
            
            self.ball.vector += self.move
            if self.ball.vector.x < 20: 
                self.scores[1] += 1
                self.score_label.render(f'{self.scores[0]}:{self.scores[1]}')
                self.reset()
                self.flash_frames = 3
            if self.ball.vector.x + self.ball.vector.z > WIDTH - 20: 
                self.scores[0] += 1
                self.score_label.render(f'{self.scores[0]}:{self.scores[1]}')
                self.reset()
                self.flash_frames = 3
            self.speed += GLOBAL_DELTA_TIME.get() * 0.0005
            SPR.update()
            UIM.render_queue(self)
            self.update()
            GLOBAL_DELTA_TIME.after()
if __name__ == "__main__":
    App().run()