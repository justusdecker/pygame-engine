
from data.modules.data_management import UnpackManager
from pygame import Surface, Rect, SRCALPHA
from data.modules.ui.ui_element import UIElement, UIC
from data.modules.ui.ui_button import UIButton
from data.modules.ui.ui_label import UILabel
import calendar
from datetime import datetime

class UICalendar(UIElement):
    def __init__(self, rect: Rect, **kwargs):
        UIC.addElement('uiCalendar')
        super().__init__(rect, **kwargs)
        
        self.surface = Surface((1,1),SRCALPHA)
        self.buttonArray = []
        self.ids = []
        for i in range(31):
            self.buttonArray.append(UIButton(Rect(-1000,-1000,24,24),onPressCallback=self.setDate,ux={'size':(24,24),'text': f'{i+1}'},parent= UnpackManager('parent',kwargs,None),layer=self.layer,group=self.group))
            self.ids.append(self.buttonArray[-1])
        
        self.currentDate = str(datetime.today()).split(' ')[0].split('-')
        
        self.selectedDay = int(self.currentDate[2])
        self.selectedMonth = int(self.currentDate[1])
        self.selectedYear = int(self.currentDate[0])
        
        
        #self.DateSelectLabel.setImage(self.DateSelectLabel.UX.gen())
        self.dateShowLabel = UILabel(Rect(-1000,-1000,72,24),parent= UnpackManager('parent',kwargs,None),layer=self.layer,group=self.group)
        self.changeMonthBackButton = UIButton(Rect(-1000,-1000,24,24),onPressCallback=self.setMonthLast,ux={'size':(24,24),'text': f'<'},parent= UnpackManager('parent',kwargs,None),layer=self.layer,group=self.group)
        self.changeMonthNextButton = UIButton(Rect(-1000,-1000,24,24),onPressCallback=self.setMonthNext,ux={'size':(24,24),'text': f'>'},parent= UnpackManager('parent',kwargs,None),layer=self.layer,group=self.group)
        self.DateSelectLabel = UILabel(Rect(-1000,-1000,144,24),ux={'text': 'Date Selector','size':(144,24)},parent= UnpackManager('parent',kwargs,None),layer=self.layer,group=self.group)
        self.changeMonth()
        
    def changeMonth(self,*_):
        weekday,days = calendar.monthrange(self.selectedYear,self.selectedMonth)
        self.buttons = []
        x , y = 0 , 0
        d = 0
        for btn in self.buttonArray:
            if x == 6:
                y += 1
                x = 0
            btn:UIButton
            btn.pos = (24*x)+self.pos[0],(24*(y+1))+self.pos[1]
            x += 1
            d += 1
            if d > days:
                btn.visible = False
            else:
                btn.visible = True
        if y < 5: y = 5  
        self.DateSelectLabel.pos = self.pos
        self.changeMonthBackButton.pos = self.pos[0]+(24),(24*(y+1))+self.pos[1]
        self.changeMonthNextButton.pos = self.pos[0]+(24*5),(24*(y+1))+self.pos[1]
        self.dateShowLabel.pos = self.pos[0]+(24*2),(24*(y+1))+self.pos[1] # ADD +1 to y for under placement
        self.dateShowLabel.UX.text = f'{self.selectedDay}/{self.selectedMonth}/{self.selectedYear}'
        self.dateShowLabel.setImage(self.dateShowLabel.UX.gen())
        return x,y
    def setMonthLast(self,*_):
        self.selectedMonth -= 1
        if self.selectedMonth < 1:
            self.selectedMonth += 12
            self.selectedYear -= 1
        self.changeMonth()
    def setMonthNext(self,*_):
        self.selectedMonth += 1
        if self.selectedMonth > 12:
            self.selectedMonth -= 12
            self.selectedYear += 1
        self.changeMonth()
    def setDate(self,*_):
        
        self.selectedDay = self.ids.index(_[0]) + 1
        self.dateShowLabel.UX.text = f'{self.selectedDay}/{self.selectedMonth}/{self.selectedYear}'
        self.dateShowLabel.setImage(self.dateShowLabel.UX.gen())
    def getDate(self):
        _ret = ''
        if self.selectedDay < 10:
            _ret += f'0{self.selectedDay}-'
        else:
            _ret += f'{self.selectedDay}-'
        if self.selectedMonth < 10:
            _ret += f'0{self.selectedMonth}-'
        else:
            _ret += f'{self.selectedMonth}-'
        return _ret + str(self.selectedYear)
    def noCallback(self,btn):
        pass
    