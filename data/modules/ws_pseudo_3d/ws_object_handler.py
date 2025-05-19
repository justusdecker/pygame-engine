from data.modules.ws_pseudo_3d.ws_sprite_object import *

class ObjectHandler:
    def __init__(self, app):
        self.app = app
        self.sprite_list = []
        self.static_sprite_path = 'data\\bin\\img\\static\\'
        self.animated_sprite_path = 'data\\bin\\img\\animated\\'
        add_sprite = self.add_sprite

        # sprite map
        add_sprite(SpriteObject(app,'data\\bin\\img\\soul_stone_animated\\soul_stone_f1.png'))
        add_sprite(AnimatedSprite(app,'data\\bin\\img\\soul_stone_animated\\soul_stone_f1.png',(4.7,3.5)))
    def update(self):
        [sprite.update() for sprite in self.sprite_list]
    def add_sprite(self,sprite):
        self.sprite_list.append(sprite)