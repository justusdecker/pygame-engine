from pygame import Surface, Rect
from data.modules.ui.ui_element import UIElement, UIC
from data.modules.ui.ui_button import UIButton
from data.modules.ui.ui_label import UILabel  
class UITimeSelect(UIElement):
    def __init__(self, rect: Rect, **kwargs):
        super().__init__(rect, **kwargs)
        UIC.add_element('uiTimeSelect')
        self.set_image(Surface((1,1)))
        self.hour = 0
        self.minute = 0
        self.minute_multiplier = 15
        
        self.minute_up_button = UIButton(Rect(24,0,24,24),ux={'size':(24,24),'text': '/\\'},on_press_callback = self.change_minute_up,parent=self,layer=self.layer,group=self.group)
        self.minute_down_button = UIButton(Rect(24,48,24,24),ux={'size':(24,24),'text': '\\/'},on_press_callback = self.change_minute_down,parent=self,layer=self.layer,group=self.group)
        self.hour_up_button = UIButton(Rect(0,0,24,24),ux={'size':(24,24),'text': '/\\'},on_press_callback = self.change_hour_up,parent=self,layer=self.layer,group=self.group)
        self.hour_down_button = UIButton(Rect(0,48,24,24),ux={'size':(24,24),'text': '\\/'},on_press_callback = self.change_hour_down,parent=self,layer=self.layer,group=self.group)
        
        self.time_label = UILabel(Rect(0,24,48,24,ux={'size':(48,24)}),parent=self,layer=self.layer,group=self.group)
        self.update_time_label()
    def update_time_label(self):
        self.time_label.UX.text = f'{self.getDoubleZeros(self.hour)}:{self.getDoubleZeros(self.minute)}'
        self.time_label.set_image(self.time_label.UX.gen())
    def change_hour_up(self,*_):
            self.hour += 1
            if self.hour > 23:
                self.hour = self.hour % 24
            self.update_time_label()
    def change_hour_down(self,*_):
        self.hour -= 1
        if self.hour < 0:
            self.hour += 24
        self.update_time_label()
    def change_minute_up(self,*_):
        self.minute += self.minute_multiplier
        if self.minute > 59:
            self.minute = self.minute % 60
            self.change_hour_up()
        self.update_time_label()
    def change_minute_down(self,*_):
        self.minute -= self.minute_multiplier
        if self.minute < 0:
            self.minute += 60
            self.change_hour_down()
        self.update_time_label()
    def getDoubleZeros(self,val):
        if val < 10:
            return '0' + str(val)
        return str(val)
    def update(self):
        return super().update()
