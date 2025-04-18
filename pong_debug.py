from data.modules.log import LOG
from data.modules.constants import *
from data.modules.ui.ui_element import UIM
from data.modules.app import Application

LOG.tobash = False



class App(Application):
    def __init__(self): super().__init__()
        
    def run(self):
        while self.is_running:
            GLOBAL_DELTA_TIME.before()
            self.CLK.tick(60)
            self.window.surface.fill((0,0,0))
            UIM.render_queue(self)
            self.update()
            GLOBAL_DELTA_TIME.after()

if __name__ == "__main__":
    APP = App()
    APP.run()