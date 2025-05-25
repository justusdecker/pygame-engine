import pygame as pg
from data.modules.constants import WIDTH, HALF_HEIGHT, HEIGHT
from data.modules.graphics_rendering import color_correction,surf_to_1d,blend_mult
from numpy import array, char
from time import sleep
from numba import jit
TEXTURE_SIZE = 256
H_TEXTURE_SIZE = TEXTURE_SIZE // 2

class ObjectRenderer:
    def __init__(self,app):
        self.app = app
        self.screen = app.window
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('data\\bin\\img\\sky.png',(WIDTH,HALF_HEIGHT))
        self.sky_offset = 0
        self.this_frame_render_pixels = 0
        self.depth_buffer_surface = pg.Surface((WIDTH,HEIGHT))
    def draw(self):
        self.draw_background()
        self.render_game_objects()
    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.app.player.rel) % WIDTH
        self.screen.surface.blit(self.sky_image,(-self.sky_offset,0))
        self.screen.surface.blit(self.sky_image,(-self.sky_offset + WIDTH,0))
        
        # floor
        
        self.screen.surface.fill((24,24,24),(0,HALF_HEIGHT,WIDTH,HEIGHT))
    @jit
    def fast_gamma_change(img,p,x,y) -> array:
        for x in range(x):
            for y in range(y):
                img[x][y][0] *= p
                img[x][y][1] *= p
                img[x][y][2] *= p
                #r = r if r < 256 else 255
                #g = g if g < 256 else 255
                #b = b if b < 256 else 255
        return img
    def render_game_objects(self):
        list_objects = sorted(self.app.raycasting.objects_to_render,key=lambda t: t[0], reverse=True)
        self.this_frame_render_pixels = 0
        depthbuffer = []
        for depth, image, pos in list_objects:
            image : pg.Surface
            percentage = (1 - depth ** 7 * 0.00002) # calculation of the gamma value
            depthbuffer.append((*pos,image.width,image.height,percentage))
            self.this_frame_render_pixels += image.get_width()*image.get_height()
            self.screen.render(image,pos)
        self.render_depth_buffer(depthbuffer)
        #print(self.this_frame_render_pixels)
    def render_depth_buffer(self, db):
        self.depth_buffer_surface.fill((0,0,0,0))
        for x, y, w, h, d in db:
            d = (d*255) if d > 0 else 0
            c = [d,d,d,16]
            self.depth_buffer_surface.fill(c,(x,y,w,h))
        blend_mult(self.screen.surface, self.depth_buffer_surface)
        #self.screen.render(self.depth_buffer_surface,(0,0))
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