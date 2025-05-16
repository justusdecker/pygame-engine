from data.modules.constants import *
from data.modules.app import Application
from data.modules.software_rendering_3d.software_renderer_3d import SoftwareRenderer
import pygame.key as keys
def test_print(*args):
    print(args, "Hello World!")


class App(Application):
    def __init__(self):
        super().__init__()
        self.renderer = SoftwareRenderer(self)
    def run(self):

        while self.is_running:
            GLOBAL_DELTA_TIME.before()
            self.renderer.draw()
            self.update()
            GLOBAL_DELTA_TIME.after()
if __name__ == "__main__":
    APP = App()
    APP.run()