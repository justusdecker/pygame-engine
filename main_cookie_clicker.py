from data.modules.constants import *

from pygame import Rect,image, Color
from data.modules.ui.ui_font import FONT
from pygame.display import set_caption

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

class CookieClicker:
    def __init__(self):
        self.cookies = 0
        self.lvl_click = 1
    def click(self):
        self.cookies += self.lvl_click

class App(Application):
    def __init__(self):
        super().__init__()
        self.cc = CookieClicker()
        self.mine_button = UIButton(
            Rect(HALF_WIDTH-(QUARTER_HEIGHT//2),HALF_HEIGHT-(QUARTER_HEIGHT//2),QUARTER_HEIGHT,QUARTER_HEIGHT),
            ux={
                'size': (QUARTER_HEIGHT,QUARTER_HEIGHT),
                'font':FONT(size=40),
                'border_radius':45,
                'normal_color': (0,0,0,0),
                'hovered_color': (0,0,0,0),
                'pressed_color': (0,0,0,0)
                }
        )
        self.animation = Animation(self,
                                   image.load("data\\bin\\img\\cookie.png"),
                                   [
                                       {
            "x_offset": 0,
            "y_offset": 0,
            "scale": [.3,.3]
        },{
            "x_offset": 0,
            "y_offset": 10,
            "scale": [.28,.3]
        },{
            "x_offset": 0,
            "y_offset": 20,
            "scale": [.25,.3]
        },{
            "x_offset": 0,
            "y_offset": 40,
            "scale": [.3,.25]
        },{
            "x_offset": 0,
            "y_offset": 40,
            "scale": [.35,.15]
        },{
            "x_offset": 0,
            "y_offset": 40,
            "scale": [.3,.25]
        },{
            "x_offset": 0,
            "y_offset": 20,
            "scale": [.25,.3]
        },{
            "x_offset": 0,
            "y_offset": 10,
            "scale": [.28,.3]
        }
                                   ],
                                   (HALF_WIDTH,HALF_HEIGHT),time_multiplier=50)
    def run(self):
        
        while self.is_running:
            GLOBAL_DELTA_TIME.before()
            self.window.surface.fill((0,0,0))
            
            UIM.render_queue(self)
            self.animation.update()
            if self.mine_button.this_frame_pressed:
                self.animation.start_animation()
                self.cc.click()
                set_caption(f"Cookies: {self.cc.cookies}")
            self.update()
            GLOBAL_DELTA_TIME.after()

if __name__ == "__main__":
    APP = App()
    APP.run()