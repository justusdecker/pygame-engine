from data.modules.ws_pseudo_3d.ws_sprite_object import *
from random import randint, random, choice
from data.modules.constants import WIDTH, HALF_WIDTH
"""
Folderstructure:

data\\
    img\\
        {object}\\
            attack\\
                ...
            death\\
                ...
            idle\\
                ...
            pain\\
                ...
            walk\\
                ...
            0.png
            
"""
class NPC(AnimatedSprite):
    def __init__(self, app, path, pos=(4.5,3.5), scale=0.5, shift=0.45, animation_time=0.1):
        super().__init__(app, path, pos, scale, shift, animation_time)
        self.attack_images = self.get_images(self.path + '\\attack')
        self.death_images = self.get_images(self.path + '\\death')
        self.idle_images = self.get_images(self.path + '\\idle')
        self.pain_images = self.get_images(self.path + '\\pain')
        self.walk_images = self.get_images(self.path + '\\walk')
        
        # stats
        self.attack_dist = randint(3,6)
        self.speed = 0.03
        self.size = .3
        self.health = 100
        self.attack_damage = 10
        self.accuracy = 0.15
        self.alive = True
        self.pain = False
    def update(self):
        self.check_animation_time()
        self.get_sprite()
        self.run_logic()
    def check_hit_in_npc(self):
        print(self.app.player.shot, HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width)
        if self.app.player.shot:
            if HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width:
                self.app.player.shot = False
                self.pain = True
    def animate_pain(self):
        self.animate(self.pain_images)
        if self.animation_trigger:
            self.pain = False
    def run_logic(self):
        if self.alive:
            self.check_hit_in_npc()
            if self.pain:
                self.animate_pain()
            else:
                self.animate(self.idle_images)