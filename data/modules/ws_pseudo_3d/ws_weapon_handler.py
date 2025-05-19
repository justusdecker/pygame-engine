from data.modules.ws_pseudo_3d.ws_weapon import Weapon
from pygame.mouse import get_pressed
class WeaponHandler:
    def __init__(self,app):
        self.app = app
        
        self.state = 0 # 0 is default walking 1 is weapon shot 2 is others
        self.reloading = False
        self.anim_walk = Weapon(app,'data\\bin\\img\\lantern_animated\\lantern_f1.png',13,0.2,False)
        self.anim_attack = Weapon(app,'data\\bin\\img\\lantern_attack_animated\\lantern_f1.png',13,0.1,False)
    def update(self):
        self.app.player.single_fire_event()
        m = get_pressed()[0] 
        print(m, self.reloading)
        if m or self.reloading:
            if m:
                self.reloading = m
                self.anim_attack.reloading = m
            self.anim_attack.update(self.anim_attack.animate_shot)
            self.anim_attack.draw()
            self.reloading = self.anim_attack.reloading
        elif self.app.player.moving: 
            self.anim_walk.update(self.anim_walk.animate_walk)
            self.anim_walk.draw()
        elif not self.reloading and not m: 
            self.anim_walk.update(self.anim_walk.animate_walk)
            self.anim_walk.draw()