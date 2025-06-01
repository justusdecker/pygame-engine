from math import pi, tan, cos, sin, atan2, hypot, tau

from data.modules.constants import WIDTH as w, HEIGHT as h, HALF_WIDTH, HALF_HEIGHT, GLOBAL_DELTA_TIME
from data.modules.kernel.log import LOG
from data.modules.constants import WIDTH, HEIGHT
from data.modules.grop import blending_mul

from pygame.transform import scale as surf_scale, smoothscale as surf_smoothscale
from pygame import Surface,K_0,K_1,K_2,K_3,K_w,K_s,K_a,K_d
from pygame.key import get_pressed as kb_get_pressed
from pygame.surfarray import make_surface as sa_make_surface
from pygame.image import load as img_load
from pygame.mouse import get_pressed as mouse_get_pressed,get_pos as mouse_get_pos,set_pos as mouse_set_pos,get_rel as mouse_get_rel

from numpy import array, deg2rad
from numba import jit
from collections import deque
from time import time
from os.path import isfile, join as pjoin
from os import listdir
from random import randint

from data.modules.kernel.opt_surfarray import Surfarray

# internal screen size

W = w // 4
H = h // 4

HW = W // 2
HH = H // 2

QW = W // 4
QH = H // 4

# raycasting constants

FOV = pi / 3
H_FOV = FOV / 2
NUM_RAYS = W // 2
H_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 20
SCREEN_DIST = HW / tan(H_FOV)
SCALE = W // NUM_RAYS

# object renderer

TEXTURE_SIZE = 256
H_TEXTURE_SIZE = TEXTURE_SIZE // 2

# player

MOUSE_SENSITIVITY = 0.3
MOUSE_MAX_REL = 40
MOUSE_BORDER_LEFT = 100
MOUSE_BORDER_RIGHT = WIDTH - MOUSE_BORDER_LEFT


_ = False
mini_map = [ #! Will be replaced later
    [1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,_,_,_,_,_,1,1,1,_,_,_,1],
    [1,1,1,_,1,_,_,1,_,2,_,_,1],
    [1,1,1,_,_,_,1,1,_,2,_,1,1],
    [1,_,1,_,_,_,1,_,1,_,_,_,1],
    [1,_,_,_,_,_,_,_,_,_,_,_,1],
    [3,3,3,3,3,3,1,1,1,1,1,1,1]
]

class Map:
    def __init__(self,app):
        self.app = app
        self.mini_map = mini_map
        self.world_map = {}
        self.get_map()
    def get_map(self):
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i,j)] = value

class RayCasting:
    def __init__(self,app):
        self.app = app
        self.ray_casting_result = []
        self.objects_to_render = []
        self.textures = self.app.object_renderer.wall_textures
    def get_objects_to_render(self):
        self.objects_to_render = []
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values
            if proj_height < H:
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                wall_column = surf_scale(wall_column,(SCALE,proj_height))
                wall_pos = (ray * SCALE, HH - proj_height // 2)
            else:
                texture_height = TEXTURE_SIZE * H / proj_height
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), H_TEXTURE_SIZE - texture_height // 2, SCALE, texture_height
                )
                wall_column = surf_scale(wall_column,(SCALE,H))
                wall_pos = (ray * SCALE,0)
            self.objects_to_render.append((depth,wall_column,wall_pos))
                 
    def ray_cast(self):
        self.ray_casting_result = []
        px, py = self.app.player.pos
        mx, my = self.app.player.map_pos
        ray_angle = self.app.player.angle - H_FOV + 0.0001 #The small number is here to prevent further ZeroDivision Errors!
        
        texture_vert, texture_hor = 1, 1
        
        for ray in range(NUM_RAYS):
            sin_a = sin(ray_angle)
            cos_a = cos(ray_angle)
            
            #horizontals
            
            y_hor, dy = (my + 1, 1) if sin_a > 0 else (my - 1e-6, -1)
            
            depth_hor = (y_hor - py) / sin_a
            x_hor = px + depth_hor * cos_a
            delta_depth = dy / sin_a
            dx = delta_depth * cos_a
            
            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.app.map.world_map:
                    texture_hor = self.app.map.world_map[tile_hor]
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
                if tile_vert in self.app.map.world_map:
                    texture_vert = self.app.map.world_map[tile_vert]
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth
            
            # depth, texture offset
            
            if depth_vert < depth_hor:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                depth, texture = depth_hor, texture_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor
            
            # debug drawing
            
            #pg.draw.line(self.app.window.surface,'yellow',(100*px,100*py),(100*px+100*depth*cos_a,100*py+100*depth*sin_a),2)
            
            # remove fishbowl effect
            depth *= cos(self.app.player.angle - ray_angle)
            
            # projection
            proj_height = SCREEN_DIST / (depth + 0.0001)
            
            """# draw walls
            
            color = [255 / (1 + depth ** 5 * 0.00002)] * 3
            
            pg.draw.rect(self.app.window.surface,color,
                         (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height))"""
            
            #ray casting result
            
            #distance color change


            self.ray_casting_result.append((depth,proj_height,texture,offset))
            
            ray_angle += DELTA_ANGLE
    def update(self):
        self.ray_cast()
        self.get_objects_to_render()

class ObjectRenderer:
    #TEXTURE_SIZE = 256
    #H_TEXTURE_SIZE = TEXTURE_SIZE // 2
    def __init__(self,app):
        self.app = app
        self.screen = app.window
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('data\\bin\\img\\sky.png',(W,HH))
        self.sky_offset = 0
        self.this_frame_render_pixels = 0
        self.background_layer = Surface((W,H))
        self.depth_buffer_surface = Surface((W,H)).convert_alpha()
        self.floor_casting_surface = Surface((W,HH)).convert_alpha()
        
        self.debugmode = 0
    def draw(self):
        
        k = kb_get_pressed()
        if k[K_0]:
            self.debugmode = 0
            LOG.nlog(0,"toggled WSP3D debug mode to $",[self.debugmode])
        elif k[K_1]:
            self.debugmode = 1
            LOG.nlog(0,"toggled WSP3D debug mode to $",[self.debugmode])
        elif k[K_2]:
            self.debugmode = 2
            LOG.nlog(0,"toggled WSP3D debug mode to $",[self.debugmode])
        elif k[K_3]:
            self.debugmode = 3
            LOG.nlog(0,"toggled WSP3D debug mode to $",[self.debugmode])
        
        self.background_layer.fill((24,24,24),(0,HH,W,H))
        #self.floor_casting()
        self.draw_foreground()
        self.render_game_objects()
    #@jit
    def fcjit(horizontal_resolution: int,
              half_vertical_resolution: int,
              pos_x: float,
              pos_y: float,
              angle: float,
              arr: array):
        fov = horizontal_resolution / 60
        
        for i in range(horizontal_resolution):
            roti = angle + deg2rad(i / fov - 30)
            sina,cosa = sin(roti), cos(roti)
            for j in range(half_vertical_resolution):
                n = half_vertical_resolution / (half_vertical_resolution - j)
                
                x, y = pos_x + cosa * n, pos_y + sina * n
                if int(x) % 2 == int(y) % 2:
                    arr[i][half_vertical_resolution*2-j-1] = [0] * 3
                else:
                    arr[i][half_vertical_resolution*2-j-1] = [255] * 3
        return arr
    def floor_casting(self):
        #posx, posy, rot = 0,0,0
        self.floor_casting_array = ObjectRenderer.fcjit(H,HW,*self.app.player.pos,self.app.player.angle,self.floor_casting_array)
        self.floor_casting_surface = sa_make_surface(self.floor_casting_array)
        self.background_layer.fill((24,24,24),(0,HH,W,H))
        self.background_layer.blit(self.floor_casting_surface,(0,0))    
    def draw_foreground(self):
        self.sky_offset = (self.sky_offset + 0.5 * self.app.player.rel) % W # Sky rotation the mod value is currently dependent on the screen size
        
        # sky
        
        self.background_layer.blit(self.sky_image,(-self.sky_offset,0))
        self.background_layer.blit(self.sky_image,(-self.sky_offset + W,0))
        
        # floor
        
        
    @jit
    def fast_gamma_change(img,p,x,y) -> array:
        for x in range(x):
            for y in range(y):
                img[x][y][0] *= p
                img[x][y][1] *= p
                img[x][y][2] *= p
        return img
    def render_game_objects(self):
        list_objects = sorted(self.app.raycasting.objects_to_render,key=lambda t: t[0], reverse=True)
        self.this_frame_render_pixels = 0
        depthbuffer = []
        for depth, image, pos in list_objects:
            image : Surface
            percentage = (1 - depth ** 7 * 0.00002) # calculation of the gamma value
            depthbuffer.append((*pos,image.width,image.height,percentage))
            #self.this_frame_render_pixels += image.get_width()*image.get_height()
            self.background_layer.blit(image,pos)
        
        self.render_depth_buffer(depthbuffer)
        if self.debugmode == 1: # show Depth-Buffer
            self.screen.render(surf_scale(self.depth_buffer_surface,(WIDTH,HEIGHT)),(0,0))
        elif self.debugmode == 2:
            self.screen.render(surf_scale(self.background_layer,(WIDTH,HEIGHT)),(0,0))
        elif self.debugmode == 3:
            self.screen.render(surf_scale(self.floor_casting_surface,(WIDTH,HEIGHT)),(0,0))
        else:
            self.screen.render(surf_scale(blending_mul(self.background_layer,self.depth_buffer_surface),(WIDTH,HEIGHT)),(0,0))
        
        #print(self.this_frame_render_pixels)
    def render_depth_buffer(self, db):
        """
        This function renders a depth buffer, use: to make tiles darker in the distance
        """
        self.depth_buffer_surface.fill((255,255,255))
        for x, y, w, h, d in db:
            d = (d*255) if d > 0 else 0
            c = [d,d,d]
            self.depth_buffer_surface.fill(c,(x,y,w,h))
        
        #self.screen.render(blend_mult(self.background_layer, self.depth_buffer_surface),(0,0))
    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE,TEXTURE_SIZE)):
        texture = img_load(path).convert()
        return surf_scale(texture,res)
    def load_wall_textures(self):
        return {
            1: self.get_texture('data\\bin\\img\\stone.png'),
            2: self.get_texture('data\\bin\\img\\stone_with_window.png'),
            3: self.get_texture('data\\bin\\img\\dark_stone.png')
        }
        
class SpriteObject:
    def __init__(self, app, path,pos=(4.5,3.5),scale=0.5,shift=0.45):
        self.app = app
        self.player = app.player
        self.x, self.y = pos
        self.image = img_load(path).convert_alpha()
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_H_WIDTH = self.IMAGE_WIDTH // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0,0,0,0,1,1
        self.sprite_half_width = 0
        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = shift
        
    def get_sprite_projection(self):
        proj = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE
        proj_width, proj_height = proj * self.IMAGE_RATIO,proj
        image = surf_scale(self.image,(proj_width,proj_height))
        
        self.sprite_half_width = proj_height // 2
        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT
        pos = self.screen_x - self.sprite_half_width, HH - proj_height // 2 + height_shift
        self.app.raycasting.objects_to_render.append((self.norm_dist,image,pos))
    def get_sprite(self):
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx, self.dy = dx,dy
        self.theta = atan2(dy,dx)
        
        delta = self.theta - self.player.angle
        if (dx > 0 and self.player.angle > pi) or (dx < 0 and dy < 0):
            delta += tau
        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (H_NUM_RAYS + delta_rays) * SCALE
        
        self.dist = hypot(dx,dy)
        self.norm_dist = self.dist * cos(delta)
        
        if -self.IMAGE_H_WIDTH < self.screen_x < (WIDTH + self.IMAGE_H_WIDTH) and self.norm_dist > 0.5:
            self.get_sprite_projection()
        
    def update(self):
        self.get_sprite()


class AnimatedSprite(SpriteObject):
    def __init__(self, app, path:str, pos=(4.5, 3.5), scale=0.5, shift=0.45, animation_time=.1):
        super().__init__(app, path, pos, scale, shift)
        self.animation_time = animation_time
        self.path = path.rsplit('\\',1)[0]
        self.images = self.get_images(self.path)
        self.animation_time_prev = time()
        self.animation_trigger = False
    def update(self):
        super().update()
        self.check_animation_time()
        self.animate(self.images)
    def animate(self,images: deque):
        if self.animation_trigger:
            images.rotate(-1)
            self.image = images[0]
    def check_animation_time(self):
        self.animation_trigger = False
        time_now = time()
        if time_now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = time_now
            self.animation_trigger = True
            
    def get_images(self,path):
        images = deque()
        for file_name in listdir(path):
            if isfile(pjoin(path,file_name)):
                img = img_load(path + '\\' + file_name).convert_alpha()
                images.append(img)
                
        return images

class ObjectHandler:
    def __init__(self, app):
        self.app = app
        self.sprite_list = []
        self.npc_list = []
        self.npc_sprite_path = 'data\\bin\\img\\npc\\'
        self.static_sprite_path = 'data\\bin\\img\\static\\'
        self.animated_sprite_path = 'data\\bin\\img\\animated\\'
        add_sprite = self.add_sprite
        add_npc = self.add_npc
        # sprite map
        add_sprite(SpriteObject(app,'data\\bin\\img\\soul_stone_animated\\soul_stone_f1.png'))
        add_sprite(AnimatedSprite(app,'data\\bin\\img\\soul_stone_animated\\soul_stone_f1.png',(3.7,3.5)))
        
        add_npc(NPC(app,'data\\bin\\img\\npc\\soul\\0.png',animation_time=0.2))
    def update(self):
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]
    def add_npc(self,npc):
        self.npc_list.append(npc)
    def add_sprite(self,sprite):
        self.sprite_list.append(sprite)

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
        self.speed = 0.01
        self.size = .6
        self.health = 100
        self.attack_damage = 10
        self.accuracy = 0.15
        self.alive = True
        self.pain = False
        
        self.on_me = False,False
        
        self.ray_cast_value = False
        self.player_search_trigger = False
        self.frame_counter = 0
    def update(self):
        self.check_animation_time()
        self.get_sprite()
        self.run_logic()
        
    def movement(self):
        next_pos = self.app.pathfinding.get_path(self.map_pos, self.app.player.map_pos)
        next_x, next_y = next_pos
        angle = atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
        dx = cos(angle) * self.speed
        dy = sin(angle) * self.speed
        self.check_wall_collision(dx,dy)
    def check_wall(self,x,y):
        return (x,y) not in self.app.map.world_map
    def check_wall_collision(self,dx,dy):
        if self.check_wall(int(self.x + dx * self.size),int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x),int(self.y + dy * self.size)):
            self.y += dy
    def check_hit_in_npc(self):
        on_me_l = self.on_me
        self.on_me = self.app.player.shot, HW - self.sprite_half_width < self.screen_x < HW + self.sprite_half_width
        if on_me_l[1] and not on_me_l[0] and all(self.on_me) and self.ray_cast_value:
            #! SOUND: HIT MISSING
            if HW - self.sprite_half_width < self.screen_x < HW + self.sprite_half_width:
                self.app.player.shot = False
                self.health -= self.app.weapon.anim_attack.damage
                self.check_health()
                self.pain = True
    def check_health(self):
        if self.health < 1:
            self.alive = False
            #! SOUND: DEATH MISSING
    def animate_death(self):
        if not self.alive:
            if self.animation_trigger and self.frame_counter < len(self.death_images) - 1:
                self.death_images.rotate(-1)
                self.image = self.death_images[0]
                self.frame_counter += 1
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
            elif self.ray_cast_value:
                self.player_search_trigger = True
                self.animate(self.walk_images)
                self.movement()
            elif self.player_search_trigger:
                self.animate(self.walk_images)
                self.movement()
            else:
                self.animate(self.idle_images)
        else:
            self.animate_death()
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

        sin_a = sin(ray_angle)
        cos_a = cos(ray_angle)
        
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

class Weapon(AnimatedSprite):
    def __init__(self, app, path,scale=1, animation_time=0.1,sc=True):
        super().__init__(app, path, scale=scale, animation_time=animation_time)
        
        scale_func = surf_smoothscale if sc else surf_scale
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
class WeaponHandler:
    def __init__(self,app):
        self.app = app
        
        self.state = 0 # 0 is default walking 1 is weapon shot 2 is others
        self.reloading = False
        self.anim_walk = Weapon(app,'data\\bin\\img\\lantern_animated\\lantern_f1.png',13,0.2,False)
        self.anim_attack = Weapon(app,'data\\bin\\img\\lantern_attack_animated\\lantern_f1.png',13,0.1,False)
    def update(self):
        self.app.player.single_fire_event()
        m = mouse_get_pressed()[0]
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
        if mouse_get_pressed()[0]:
            if not self.shot and not self.app.weapon.reloading:
                self.app.sound.play_sound('attack')
                self.shot = True
                self.app.weapon.reloading = True
    def movement(self):
        sin_a = sin(self.angle)
        cos_a = cos(self.angle)
        dx, dy = 0,0
        speed = GLOBAL_DELTA_TIME.get() * self.speed
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a
        
        keys = kb_get_pressed()
        self.moving = False
        if keys[K_w]:
            dx += speed_cos
            dy += speed_sin
            self.moving = True
        elif keys[K_s]:
            dx += -speed_cos
            dy += -speed_sin
            self.moving = True
        if keys[K_a]:
            dx += speed_sin
            dy += -speed_cos
            self.moving = True
        elif keys[K_d]:
            dx += -speed_sin
            dy += speed_cos
            self.moving = True
        self.check_wall_collision(dx,dy)
        """if keys[pg.K_LEFT]:
            self.angle -= self.rot_speed * GLOBAL_DELTA_TIME.get()
        elif keys[pg.K_RIGHT]:
            self.angle += self.rot_speed * GLOBAL_DELTA_TIME.get()"""
        self.angle %= tau
    def draw(self):
        
        pass
        #pg.draw.line(self.app.window.surface,'yellow',(self.x*100,self.y*100),(self.x*100+WIDTH* math.cos(self.angle),
        #                                                                       self.y*100+WIDTH* math.sin(self.angle)),2)
        #pg.draw.circle(self.app.window.surface,'green',(self.x*100,self.y*100),15)
    def check_wall(self,x,y):
        return (x,y) not in self.app.map.world_map
    def check_wall_collision(self,dx,dy):
        scale = self.scale / (GLOBAL_DELTA_TIME.get() + 0.000001)
        if self.check_wall(int(self.x + dx * scale),int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x),int(self.y + dy * scale)):
            self.y += dy
    def mouse_control(self):
        mx,my = mouse_get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            mouse_set_pos([HALF_WIDTH,HALF_HEIGHT])
        self.rel = mouse_get_rel()[0]
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