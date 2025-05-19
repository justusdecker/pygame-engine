from data.modules.ws_pseudo_3d.ws_sprite_object import *

class ObjectHandler:
    def __init__(self, app):
        self.app = app
        self.sprite_list = []
        self.static_sprite_path = 'data\\bin\\img\\static\\'
        self.animated_sprite_path = 'data\\bin\\img\\animated\\'