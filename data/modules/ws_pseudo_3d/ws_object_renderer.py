import pygame as pg
from data.modules.ws_pseudo_3d.ws_constants import WIDTH, HALF_HEIGHT, HEIGHT, HALF_WIDTH
from data.modules.constants import WIDTH as O_WIDTH, HEIGHT as O_HEIGHT
from data.modules.grop import blending_mul
from numpy import array, char,deg2rad,rot90
from math import cos,sin,pi
from time import sleep
from numba import jit
from data.modules.kernel.log import LOG

TEXTURE_SIZE = 256
H_TEXTURE_SIZE = TEXTURE_SIZE // 2

class ObjectRenderer:
    #TEXTURE_SIZE = 256
    #H_TEXTURE_SIZE = TEXTURE_SIZE // 2
    def __init__(self,app):
        self.app = app
        self.screen = app.window
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('data\\bin\\img\\sky.png',(WIDTH,HALF_HEIGHT))
        self.sky_offset = 0
        self.this_frame_render_pixels = 0
        self.background_layer = pg.Surface((WIDTH,HEIGHT))
        self.depth_buffer_surface = pg.Surface((WIDTH,HEIGHT)).convert_alpha()
        self.floor_casting_array = array([0]*HALF_WIDTH*HEIGHT*3).reshape((HALF_WIDTH,HEIGHT,3))
        self.floor_casting_surface = pg.Surface((WIDTH,HALF_HEIGHT)).convert_alpha()
        
        self.debugmode = 0
    def draw(self):
        
        k = pg.key.get_pressed()
        if k[pg.K_0]:
            self.debugmode = 0
            LOG.nlog(0,"toggled WSP3D debug mode to $",[self.debugmode])
        elif k[pg.K_1]:
            self.debugmode = 1
            LOG.nlog(0,"toggled WSP3D debug mode to $",[self.debugmode])
        elif k[pg.K_2]:
            self.debugmode = 2
            LOG.nlog(0,"toggled WSP3D debug mode to $",[self.debugmode])
        elif k[pg.K_3]:
            self.debugmode = 3
            LOG.nlog(0,"toggled WSP3D debug mode to $",[self.debugmode])
        
        self.background_layer.fill((24,24,24),(0,HALF_HEIGHT,WIDTH,HEIGHT))
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
        self.floor_casting_array = ObjectRenderer.fcjit(HEIGHT,HALF_WIDTH,*self.app.player.pos,self.app.player.angle,self.floor_casting_array)
        self.floor_casting_surface = pg.surfarray.make_surface(self.floor_casting_array)
        self.background_layer.fill((24,24,24),(0,HALF_HEIGHT,WIDTH,HEIGHT))
        pg.image.save(self.floor_casting_surface,'test.png')
        self.background_layer.blit(self.floor_casting_surface,(0,0))    
    def draw_foreground(self):
        self.sky_offset = (self.sky_offset + 0.5 * self.app.player.rel) % WIDTH # Sky rotation the mod value is currently dependent on the screen size
        
        # sky
        
        self.background_layer.blit(self.sky_image,(-self.sky_offset,0))
        self.background_layer.blit(self.sky_image,(-self.sky_offset + WIDTH,0))
        
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
            image : pg.Surface
            percentage = (1 - depth ** 7 * 0.00002) # calculation of the gamma value
            depthbuffer.append((*pos,image.width,image.height,percentage))
            #self.this_frame_render_pixels += image.get_width()*image.get_height()
            self.background_layer.blit(image,pos)
        
        self.render_depth_buffer(depthbuffer)
        if self.debugmode == 1: # show Depth-Buffer
            self.screen.render(pg.transform.scale(self.depth_buffer_surface,(O_WIDTH,O_HEIGHT)),(0,0))
        elif self.debugmode == 2:
            self.screen.render(pg.transform.scale(self.background_layer,(O_WIDTH,O_HEIGHT)),(0,0))
        elif self.debugmode == 3:
            self.screen.render(pg.transform.scale(self.floor_casting_surface,(O_WIDTH,O_HEIGHT)),(0,0))
        else:
            self.screen.render(pg.transform.scale(blending_mul(self.background_layer,self.depth_buffer_surface),(O_WIDTH,O_HEIGHT)),(0,0))
        
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
        texture = pg.image.load(path).convert()
        return pg.transform.scale(texture,res)
    def load_wall_textures(self):
        return {
            1: self.get_texture('data\\bin\\img\\stone.png'),
            2: self.get_texture('data\\bin\\img\\stone_with_window.png'),
            3: self.get_texture('data\\bin\\img\\dark_stone.png')
        }