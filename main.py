from src.src_py.constants import *
from src.src_py.kernel.app import Application
from src.src_py.vector import Vector4
from src.src_py.wsp3d import Map
from src.src_py.wsp3d import Player
from src.src_py.wsp3d import RayCasting
from src.src_py.wsp3d import ObjectRenderer
from src.src_py.wsp3d import SpriteObject, AnimatedSprite
from src.src_py.wsp3d import ObjectHandler
from src.src_py.wsp3d import WeaponHandler
from src.src_py.algorithms.pathfinding import PathFinding
from src.src_py.audio_handler import AudioHandler
from src.src_py.ui.ui_element import UIM
from src.src_py.ui.ui_debug import UIDebug
from pygame.mouse import set_visible
from pygame.image import load
import pygame.key as keys
from time import perf_counter
from tools.testing.timing_tests import T
def test_print(*args):
    print(args, "Hello World!")


class App(Application):
    def __init__(self):
        super().__init__()
        #self.tileset = TileSet(self,load('data\\img\\test_tileset.png'),Vector2(16,16),Vector2(32,32))
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
        self.sound = AudioHandler({},{'attack': 'data\\sfx\\attack.mp3',
                                      'step_0': 'data\\sfx\\step_0.mp3',
                                      'step_1': 'data\\sfx\\step_1.mp3',
                                      'step_2': 'data\\sfx\\step_2.mp3'})
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