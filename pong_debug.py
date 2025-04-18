from data.modules.log import LOG
from data.modules.constants import *
from data.modules.ui.ui_element import UIM
from data.modules.app import Application
from data.modules.entity import Entity
from data.modules.vector import Vector2,Vector4
from pygame import Surface
LOG.tobash = False
from pygame.key import get_pressed
from pygame.mouse import get_pos
from pygame import K_w,K_s,K_UP,K_DOWN

class App(Application):
    def __init__(self): 
        super().__init__()
        surf = Surface((WIDTH*.025,HALF_HEIGHT))
        surf.fill((36,36,36))
        self.bar_left = Entity(self,surf,Vector4(20,20,WIDTH*.025,HALF_HEIGHT))
        self.bar_right = Entity(self,surf,Vector4(WIDTH-20-(WIDTH*.025),20,WIDTH*.025,HALF_HEIGHT))
        surf = Surface((WIDTH*.025,WIDTH*.025))
        surf.fill((48,48,48))
        self.ball = Entity(self,surf,Vector4(20,20,WIDTH*.025,WIDTH*.025))
        surf = Surface((WIDTH-(WIDTH*.05),HEIGHT-(WIDTH*.05)))
        surf.fill((96,96,96))
        self.field = Entity(self,surf,Vector4(WIDTH*.025,WIDTH*.025,WIDTH-(WIDTH*.05),HEIGHT-(WIDTH*.05)))
        self.multiplicator = 1
    def run(self):
        while self.is_running:
            GLOBAL_DELTA_TIME.before()
            self.CLK.tick(60)
            self.window.surface.fill((0,0,0))
            UIM.render_queue(self)
            
            KEYS = get_pressed()
            if KEYS[K_w]:
                self.bar_left.vector = self.bar_left.vector + Vector2(0,-5)
            elif KEYS[K_s]:
                self.bar_left.vector = self.bar_left.vector + Vector2(0,5)
            if KEYS[K_UP]:
                self.bar_right.vector = self.bar_right.vector + Vector2(0,-5)
            elif KEYS[K_DOWN]:
                self.bar_right.vector = self.bar_right.vector + Vector2(0,5)
            movement = 100*self.multiplicator*GLOBAL_DELTA_TIME.get()
            self.ball.vector += Vector2(movement,movement)
            self.field.render()
            self.bar_left.collision_mbts()
            self.bar_right.collision_mbts()
            self.bar_left.render()
            self.bar_right.render()
            self.ball.render()
            if self.bar_left.check_rect_collision(self.ball) or \
                self.bar_right.check_rect_collision(self.ball) or \
                    not self.field.check_rect_collision(self.ball):
                        self.multiplicator *= -1
            print(self.bar_left.check_rect_collision(self.ball))
            self.update()
            
            GLOBAL_DELTA_TIME.after()

if __name__ == "__main__":
    APP = App()
    APP.run()