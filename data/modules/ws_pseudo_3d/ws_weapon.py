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
    def draw(self):
        self.app.window.render(self.images[0],self.weapon_pos)
    def update(self):
        pass