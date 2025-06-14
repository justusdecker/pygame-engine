from data.modules.constants import *
from data.modules.kernel.app import Application
from data.modules.vector import Vector4
from data.modules.wsp3d import Map
from data.modules.wsp3d import Player
from data.modules.wsp3d import RayCasting
from data.modules.wsp3d import ObjectRenderer
from data.modules.wsp3d import SpriteObject, AnimatedSprite
from data.modules.wsp3d import ObjectHandler
from data.modules.wsp3d import WeaponHandler
from data.modules.algorithms.pathfinding import PathFinding
from data.modules.audio_handler import AudioHandler
from data.modules.ui.ui_element import UIM
from data.modules.ui.ui_debug import UIDebug
from pygame.mouse import set_visible
from pygame.image import load
import pygame.key as keys
from time import perf_counter
from data.modules.testing.timing_tests import T
def test_print(*args):
    print(args, "Hello World!")


class App(Application):
    def __init__(self):
        super().__init__()
        #self.tileset = TileSet(self,load('data\\bin\\img\\test_tileset.png'),Vector2(16,16),Vector2(32,32))
        arr = [[2 for x in range(32)] for i in range(17)]
        arr.append([0 for x in range(32)])
        set_visible(False)
        self.deb = UIDebug(Vector4(0,0,1,1),render_times=3)
        self.new_game()
    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.obj_handler = ObjectHandler(self)
        self.weapon = WeaponHandler(self)
        self.sound = AudioHandler({},{'attack': 'data\\bin\\sfx\\attack.mp3',
                                      'step_0': 'data\\bin\\sfx\\step_0.mp3',
                                      'step_1': 'data\\bin\\sfx\\step_1.mp3',
                                      'step_2': 'data\\bin\\sfx\\step_2.mp3'})
        self.pathfinding = PathFinding(self)
    def run(self):

        while self.is_running:
            T.clr()
            GLOBAL_DELTA_TIME.before()
            #self.window.surface.fill((36,36,36))
            #self.map.draw()

            self.player.update()

            self.raycasting.update()
            
            self.obj_handler.update()

            self.object_renderer.draw()

            self.weapon.update()

            UIM.render_queue(self)
            
            #self.deb.timings.append(self.object_renderer.this_frame_render_pixels)

            self.update()
            GLOBAL_DELTA_TIME.after()
            for t in T.tims:
                print(t)
            print()
if __name__ == "__main__":
    APP = App()
    APP.run()