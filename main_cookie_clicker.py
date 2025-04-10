from data.modules.constants import *
from data.modules.window import Window
from pygame.event import get as get_events
from pygame import QUIT,quit as pg_quit,Rect,image
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
def test_print(*args):
    print(args, "Hello World!")

class App(Application):
    def __init__(self):
        super().__init__()
        self.mine_button = UIButton(
            Rect(HALF_WIDTH-(WIDTH//4),HALF_HEIGHT-(HEIGHT//4),WIDTH//4,HEIGHT//4),
            ux={'text':"HALLO WELT",'size': (WIDTH//4,HEIGHT//4),'font':FONT(size=40)}
        )
    def run(self):
        while self.is_running:
            GLOBAL_DELTA_TIME.before()

            UIM.render_queue(self)
            self.update()
            GLOBAL_DELTA_TIME.after()

if __name__ == "__main__":
    APP = App()
    APP.run()