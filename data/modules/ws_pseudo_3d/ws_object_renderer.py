import pygame as pg
from data.modules.constants import WIDTH, HALF_HEIGHT, HEIGHT

TEXTURE_SIZE = 256
H_TEXTURE_SIZE = TEXTURE_SIZE // 2

class ObjectRenderer:
    def __init__(self,app):
        self.app = app
        self.screen = app.window
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('data\\bin\\img\\sky.png',(WIDTH,HALF_HEIGHT))
        self.sky_offset = 0
    def draw(self):
        self.draw_background()
        self.render_game_objects()
    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.app.player.rel) % WIDTH
        self.screen.surface.blit(self.sky_image,(-self.sky_offset,0))
        self.screen.surface.blit(self.sky_image,(-self.sky_offset + WIDTH,0))
        
        # floor
        
        self.screen.surface.fill((24,24,24),(0,HALF_HEIGHT,WIDTH,HEIGHT))
    def render_game_objects(self):
        list_objects = sorted(self.app.raycasting.objects_to_render,key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.render(image,pos)
    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE,TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture,res)
    def load_wall_textures(self):
        return {
            1: self.get_texture('data\\bin\\img\\stone.png'),
            2: self.get_texture('data\\bin\\img\\stone_with_window.png'),
            3: self.get_texture('data\\bin\\img\\dark_stone.png')
        }