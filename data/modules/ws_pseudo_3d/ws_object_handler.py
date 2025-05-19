from data.modules.ws_pseudo_3d.ws_sprite_object import *
from data.modules.ws_pseudo_3d.ws_npc import NPC
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