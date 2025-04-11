from data.modules.constants import *

from pygame import Rect,image
from data.modules.ui.ui_font import FONT

from data.modules.ui.ui_element import UIGroup,UIM
from data.modules.ui.ui_image import UIImage
from data.modules.ui.ui_label import UILabel
from data.modules.ui.ui_button import UIButton
from data.modules.ui.ui_switch import UISwitch
from data.modules.ui.ui_drop_down import UIDropDown
from data.modules.ui.ui_progress_bar import UIProgressBar
from data.modules.ui.ui_calendar import UICalendar
from data.modules.ui.ui_time_select import UITimeSelect
from data.modules.ui.ui_text_input import UITextInput
from data.modules.tests.tile_based_game import Map
from data.modules.app import Application
from data.modules.animation import Animation

def test_print(*args):
    print(args, "Hello World!")

class App(Application):
    def __init__(self):
        super().__init__()
        self.mine_button = UIButton(
            Rect(HALF_WIDTH-QUARTER_WIDTH,HALF_HEIGHT-QUARTER_HEIGHT,HALF_WIDTH,HALF_HEIGHT),
            ux={
                'text':"MINE",
                'size': (HALF_WIDTH,HALF_HEIGHT),
                'font':FONT(size=40)
                }
        )
        self.animation = Animation(self,
                                   image.load("data\\bin\\img\\cookie.png"),
                                   [
                                       {
            "x_offset": 0,
            "y_offset": 0,
            "scale": [.5,.5]
        },
                                       {
            "x_offset": 0,
            "y_offset": 25,
            "scale": [.5,.47]
        },
                                       {
            "x_offset": 0,
            "y_offset": 50,
            "scale": [.5,.45]
        },
                                       {
            "x_offset": 0,
            "y_offset": 200,
            "scale": [.5,.40]
        },
                                       {
            "x_offset": 0,
            "y_offset": 300,
            "scale": [.6,.3]
        },
                                       {
            "x_offset": 0,
            "y_offset": 350,
            "scale": [.65,.25]
        },
                                       {
            "x_offset": 0,
            "y_offset": 200,
            "scale": [.6,.4]
        },
                                       {
            "x_offset": 0,
            "y_offset": 50,
            "scale": [.5,.45]
        },
                                       {
            "x_offset": 0,
            "y_offset": 25,
            "scale": [.5,.47]
        }
                                   ],
                                   (HALF_WIDTH,HALF_HEIGHT*.8),loops=-1,time_multiplier=30)
    def run(self):
        self.animation.start_animation()
        while self.is_running:
            GLOBAL_DELTA_TIME.before()
            self.window.surface.fill((0,0,0))
            self.animation.update()
            UIM.render_queue(self)
            
            self.update()
            GLOBAL_DELTA_TIME.after()

if __name__ == "__main__":
    APP = App()
    APP.run()