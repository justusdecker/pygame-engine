from data.modules.ws_pseudo_3d.ws_sprite_object import *
from random import randint, random, choice
from data.modules.constants import WIDTH, HALF_WIDTH
from data.modules.ws_pseudo_3d.ws_ray_casting import MAX_DEPTH
import math

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
        
        self.on_me = False,False
        
        self.ray_cast_value = False
    def update(self):
        self.check_animation_time()
        self.get_sprite()
        self.run_logic()
    def check_hit_in_npc(self):
        on_me_l = self.on_me
        self.on_me = self.app.player.shot, HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width
        print(self.ray_cast_value)
        if on_me_l[1] and not on_me_l[0] and all(self.on_me) and self.ray_cast_value:
            #! SOUND: HIT MISSING
            if HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width:
                self.app.player.shot = False
                self.pain = True
                print('hit')
    def animate_pain(self):
        self.animate(self.pain_images)
        if self.animation_trigger:
            self.pain = False
    def run_logic(self):
        if self.alive:
            self.ray_cast_value = self.ray_cast_player_npc()
            self.check_hit_in_npc()
            if self.pain:
                self.animate_pain()
            else:
                self.animate(self.idle_images)
    @property
    def map_pos(self):
        return int(self.x), int(self.y)
    
    def ray_cast_player_npc(self):
        if self.app.player.map_pos == self.map_pos:
            return True
        
        wall_dist_v, wall_dist_h = 0,0
        player_dist_v, player_dist_h = 0,0
        
        px, py = self.app.player.pos
        mx, my = self.app.player.map_pos
        ray_angle = self.theta #The small number is here to prevent further ZeroDivision Errors!

        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)
        
        #horizontals
        
        y_hor, dy = (my + 1, 1) if sin_a > 0 else (my - 1e-6, -1)
        
        depth_hor = (y_hor - py) / sin_a
        x_hor = px + depth_hor * cos_a
        delta_depth = dy / sin_a
        dx = delta_depth * cos_a
        
        for i in range(MAX_DEPTH):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor == self.map_pos:
                player_dist_h = depth_hor
                break
            if tile_hor in self.app.map.world_map:
                wall_dist_h = depth_hor
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth
        
        #verticals
        
        x_vert, dx = (mx + 1, 1) if cos_a > 0 else (mx - 1e-6, -1)
        
        depth_vert = (x_vert - px) / cos_a
        y_vert = py + depth_vert * sin_a
        delta_depth = dx / cos_a
        dy = delta_depth * sin_a
        
        for i in range(MAX_DEPTH):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert == self.map_pos:
                player_dist_v = depth_vert
                break
            if tile_vert in self.app.map.world_map:
                wall_dist_v = depth_vert
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth
        player_dist = max(player_dist_v,player_dist_h)
        wall_dist = max(wall_dist_v,wall_dist_h)
        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        return False