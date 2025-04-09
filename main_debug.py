from data.modules.constants import *
from data.modules.window import Window
from pygame.event import get as get_events
from pygame import QUIT,quit as pg_quit,Rect,image

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
def test_print(*args):
    print(args, "Hello World!")
class App:
    def __init__(self):
        self.window = Window()
        self.is_running = True
        self.group_test = UIGroup('test')
        self.thumbnail = UIImage(
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
            )
        
        self.thumbnail.setImage(image.load("data\\bin\\img\\test.png"))
        self.nameLabel = UILabel(
            Rect(
                48,
                372,
                576,
                24
                ),
            change=True,
            clean=True,
            text='',
            group=self.group_test
            )
        self.nameLabel.render("test")
        self.btn = UIButton(
            Rect(0,0,128,24),
            ux={'text':'root' , 'size':(128,24),'onPressCallback': test_print},
            group=self.group_test)
        self.btn = UISwitch(
            Rect(0,24,128,24),
            ux={'size':(128,24),'onPressCallback': test_print},
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
    def run(self):
        while self.is_running:
            self.window.surface.fill((128,128,128))
            UIM.renderQueue(self,['test'])
            self.progress_bar.UX.currentProgress += GLOBAL_DELTA_TIME.get() * .25
            self.window.update()
            
            self.event_handler()
            
    def event_handler(self):
        for event in get_events():
            if event.type == QUIT:
                pg_quit()
                self.is_running = False
if __name__ == "__main__":
    APP = App()
    APP.run()