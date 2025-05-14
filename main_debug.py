from data.modules.constants import *
from data.modules.window import Window
from pygame.event import get as get_events
from pygame import QUIT,quit as pg_quit,Rect,image,K_b,K_p,K_f
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
from data.modules.ui.ui_window import UIWindow,UIWM
from data.modules.tests.tile_based_game import Map
from data.modules.app import Application
from data.modules.vector import Vector4
from data.modules.ui.ui_color_picker import UIColorPicker
from data.modules.ui.ui_array import UIArray
import pygame.key as keys
def test_print(*args):
    print(args, "Hello World!")


class App(Application):
    def __init__(self):
        super().__init__()
        self.group_test = UIGroup('test')
        
        self.nameLabel = UILabel(
            Vector4(HALF_WIDTH-100, HALF_HEIGHT-24, 200, 24),
            change=True,
            clean=True,
            text='',
            group=self.group_test,
            ux = {'tcg': ('#ffffff',),'bcg': ('#777777',),'text':'hello'}
            )
        
        self.btn = UIButton(
            Vector4(128,0,128,24),
            ux={
                'text':'root' , 
                'size':(128,24),'tcg': ('#484848','#a6a6a6','#ffffff'),'bcg': ('#777777',),
                },
            group=self.group_test,
            cb_on_press= test_print)
        self.uiwin = UIWindow(Vector4(300,200,512,256),ux={'size':(512,256),'text':'Window'},group= self.group_test)
        self.switch = UISwitch(
            Vector4(0,24,24,24),
            ux={'size':(24,24)},
            group=self.group_test,
            parent = self.uiwin)
        self.thumbnail = UIImage(
            Vector4(
                48,
                48,
                200,
                200
                ),
            ux={
                'size': (200,200)
                },
            group=self.group_test,
            parent= self.uiwin
            )
        self.fileDD = UIDropDown(
            Vector4(
                256,
                0,
                48,
                24
                ),
            ux= {
                'size': (48,24),
                'text': 'File'
                },
            childs_instances= [
                ('New',test_print),
                ('Load',test_print),
                ('Save',test_print),
                ('Exit',test_print)
                ],
            layer=100,
            group= self.group_test
            )
        
        self.progress_bar = UIProgressBar(
            Vector4(24,24,128,24),group= self.group_test,
            ux= {'size':(128,24),'bcg': (DEFAULT_BACKGROUND_COLOR,MEDIUM_BACKGROUND_COLOR)},
            parent = self.uiwin
        )

        #self.calendar = UICalendar(Rect(512,0,20,20),group= self.group_test)
        #self.time_select = UITimeSelect(Rect(512,512,48,24),group= self.group_test)

        
        self.text_input = UITextInput(Vector4(256,512,48,24),app=self,group= self.group_test)
        
        #self.map = Map(self)
        
        

        self.color_picker = UIColorPicker(Vector4(64,64,1,1),group=self.group_test,app=self)

        self.array = UIArray(Vector4(0,0,512,512),element_size=(8,8),group = self.group_test,layer=60)
    
    def run(self):
        a = 0
        while self.is_running:
            GLOBAL_DELTA_TIME.before()
            
            self.window.surface.fill((14,14,14))
            #self.map.update()
            UIM.render_queue(self,['test'])
            #self.progress_bar.UX.current_progress += GLOBAL_DELTA_TIME.get() * .25
            
            a += (GLOBAL_DELTA_TIME.get() * .25)
            if a > 1:
                a = 0
            if self.array.color != self.color_picker.current_color:
                self.array.set_color(self.color_picker.current_color)
            self.progress_bar.render(a)
            self.nameLabel.render(f"{self.color_picker.color_rect.pos}")
            if keys.get_pressed()[K_b]:
                self.array.current_tool = 'brush'
            if keys.get_pressed()[K_p]:
                self.array.current_tool = 'pixel'
            if keys.get_pressed()[K_f]:
                self.array.current_tool = 'fill'
            self.update()
            GLOBAL_DELTA_TIME.after()
if __name__ == "__main__":
    APP = App()
    APP.run()