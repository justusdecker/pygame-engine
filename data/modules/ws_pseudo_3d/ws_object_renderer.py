import pygame as pg
TEXTURE_SIZE = 256
H_TEXTURE_SIZE = TEXTURE_SIZE // 2

class ObjectRenderer:
    def __init__(self,app):
        self.app = app
        self.screen = app.window
        self.wall_textures = self.load_wall_textures()
    def draw(self):
        self.render_game_objects()
    def render_game_objects(self):
        list_objects = self.app.raycasting.objects_to_render
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