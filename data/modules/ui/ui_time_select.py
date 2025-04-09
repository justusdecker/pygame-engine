from pygame import Surface, Rect
from data.modules.ui.ui_element import UIElement, UIC
from data.modules.ui.ui_button import UIButton
from data.modules.ui.ui_label import UILabel  
class UITimeSelect(UIElement):
    def __init__(self, rect: Rect, **kwargs):
        super().__init__(rect, **kwargs)
        UIC.addElement('uiTimeSelect')
        self.setImage(Surface((1,1)))
        self.hour = 0
        self.minute = 0
        self.minuteMultiplier = 15
        
        self.minuteUpButton = UIButton(Rect(24,0,24,24),ux={'size':(24,24),'text': '/\\'},onPressCallback = self.changeMinuteUp,parent=self,layer=self.layer,group=self.group)
        self.minuteDownButton = UIButton(Rect(24,48,24,24),ux={'size':(24,24),'text': '\\/'},onPressCallback = self.changeMinuteDown,parent=self,layer=self.layer,group=self.group)
        self.hourUpButton = UIButton(Rect(0,0,24,24),ux={'size':(24,24),'text': '/\\'},onPressCallback = self.changeHourUp,parent=self,layer=self.layer,group=self.group)
        self.hourDownButton = UIButton(Rect(0,48,24,24),ux={'size':(24,24),'text': '\\/'},onPressCallback = self.changeHourDown,parent=self,layer=self.layer,group=self.group)
        
        self.timeLabel = UILabel(Rect(0,24,48,24,ux={'size':(48,24)}),parent=self,layer=self.layer,group=self.group)
        self.updateTimeLabel()
    def updateTimeLabel(self):
        self.timeLabel.UX.text = f'{self.getDoubleZeros(self.hour)}:{self.getDoubleZeros(self.minute)}'
        self.timeLabel.setImage(self.timeLabel.UX.gen())
    def changeHourUp(self,*_):
            self.hour += 1
            if self.hour > 23:
                self.hour = self.hour % 24
            self.updateTimeLabel()
    def changeHourDown(self,*_):
        self.hour -= 1
        if self.hour < 0:
            self.hour += 24
        self.updateTimeLabel()
    def changeMinuteUp(self,*_):
        self.minute += self.minuteMultiplier
        if self.minute > 59:
            self.minute = self.minute % 60
            self.changeHourUp()
        self.updateTimeLabel()
    def changeMinuteDown(self,*_):
        self.minute -= self.minuteMultiplier
        if self.minute < 0:
            self.minute += 60
            self.changeHourDown()
        self.updateTimeLabel()
    def getDoubleZeros(self,val):
        if val < 10:
            return '0' + str(val)
        return str(val)
    def update(self):
        return super().update()
