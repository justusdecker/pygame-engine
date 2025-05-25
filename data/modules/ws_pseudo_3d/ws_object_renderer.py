import pygame as pg
from data.modules.constants import WIDTH, HALF_HEIGHT, HEIGHT
from data.modules.graphics_rendering import color_correction
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
        for depth, image, pos in list_objects:
            image : pg.Surface
            #percentage = (1 - depth ** 5 * 0.00002) # calculation of the gamma value
            #nd_img = [int(i) for i in pg.surfarray.array3d(image).reshape((image.get_width() * image.get_height() * 3,))]
            #print(image.get_width(),image.get_height(),depth,pos)
            #if percentage < 0:
            #    percentage = 0
            self.this_frame_render_pixels += image.get_width()*image.get_height()
            #sleep(0.01)
            #pg.display.update()
            #pg.event.get()
            #nd_img = pg.surfarray.array3d(image)
            #image = pg.surfarray.make_surface(ObjectRenderer.fast_gamma_change(pg.surfarray.array3d(image),percentage,image.get_width(),image.get_height()))
            
            self.screen.render(image,pos)
        #print(self.this_frame_render_pixels)
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