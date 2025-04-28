from data.modules.constants import *
from data.modules.window import Window
from pygame.event import get as get_events
from pygame import QUIT,quit as pg_quit,Rect,image
from data.modules.data_management import DM
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
from data.modules.vector import Vector4
def test_print(*args):
    print(args, "Hello World!")


class App(Application):
    def __init__(self):
        super().__init__()
        self.group_test = UIGroup('test')
        """self.thumbnail = UIImage(
            Rect(
                48,
                48,
                576,
                324
                ),
            ux={
                'size': (576,324)
                },
            group=self.group_test
            )"""
        self.nameLabel = UILabel(
            Vector4(HALF_WIDTH-100, HALF_HEIGHT-24, 200, 24),
            change=True,
            clean=True,
            text='',
            group=self.group_test,
            ux = {'tcg': ('#ffffff',),'bcg': ('#777777',),'text':'hello'}
            )
        self.nameLabel.render("test")
        """self.btn = UIButton(
            Rect(128,0,128,24),
            ux={'text':'root' , 'size':(128,24)},
            group=self.group_test,
            cb_on_press= test_print)
        self.switch = UISwitch(
            Rect(0,24,24,24),
            ux={'size':(24,24)},
            group=self.group_test)
        
        self.fileDD = UIDropDown(
            Rect(
                256,
                0,
                48,
                24
                ),
            ux= {
                'size': (48,24),
                'text': 'File'
                },
            childsInstances= [
                ('New',test_print),
                ('Load',test_print),
                ('Save',test_print),
                ('Exit',test_print)
                ],
            layer=100,
            group= self.group_test
            )
        self.progress_bar = UIProgressBar(
            Rect(
                512,
                0,
                128,
                24
                ),group= self.group_test
        )
        self.calendar = UICalendar(Rect(512,0,20,20),group= self.group_test)
        self.time_select = UITimeSelect(Rect(512,512,48,24),group= self.group_test)
        self.text_input = UITextInput(Rect(256,512,48,24),app=self,group= self.group_test)
        
        self.map = Map(self)"""
    def run(self):
        while self.is_running:
            GLOBAL_DELTA_TIME.before()
            #self.map.update()
            self.window.surface.fill((0,0,0))
            UIM.render_queue(self,['test'])
            #self.progress_bar.UX.current_progress += GLOBAL_DELTA_TIME.get() * .25
            self.update()
            GLOBAL_DELTA_TIME.after()
            #self.nameLabel.render(f"{GLOBAL_DELTA_TIME.get()}")

if __name__ == "__main__":
    APP = App()
    APP.run()