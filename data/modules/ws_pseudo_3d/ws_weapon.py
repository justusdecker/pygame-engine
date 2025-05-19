from data.modules.ws_pseudo_3d.ws_sprite_object import *
from data.modules.constants import HALF_WIDTH,HEIGHT
class Weapon(AnimatedSprite):
    def __init__(self, app, path,scale=1, animation_time=0.1,sc=True):
        super().__init__(app, path, scale=scale, animation_time=animation_time)
        
        scale_func = pg.transform.smoothscale if sc else pg.transform.scale
        self.images = deque([
            scale_func(img, (self.image.get_width() * scale,self.image.get_height() * scale))
        for img in self.images ])
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())
        self.reloading = False
        self.num_images = len(self.images)
        self.frame_counter = 0
        self.damage = 50
    def animate_shot(self):
        if self.reloading:
            
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                    self.app.player.shot = False
                    self.reloading = False
                    self.frame_counter = 0
                    
    def animate_walk(self):
        if self.app.player.moving:
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                    self.frame_counter = 0
    def draw(self):
        self.app.window.render(self.images[0],self.weapon_pos)
    def update(self,animation_callback):
        self.check_animation_time()
        animation_callback()
        #self.app.player.single_fire_event()
        #self.animate_shot()