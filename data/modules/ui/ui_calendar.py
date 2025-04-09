from pygame import Surface, Rect, SRCALPHA
from data.modules.ui.ui_element import UIElement, UIC
from data.modules.ui.ui_button import UIButton
from data.modules.ui.ui_label import UILabel
import calendar
from datetime import datetime

class UICalendar(UIElement):
    """
    The user can press wanted date on here.
    """
    def __init__(self, rect: Rect, **kwargs):
        UIC.add_element('uiCalendar')
        super().__init__(rect, **kwargs)
        
        self.surface = Surface((1,1),SRCALPHA)
        self.button_array = []
        self.ids = []
        for i in range(31):
            self.button_array.append(UIButton(Rect(-1000,-1000,24,24),on_press_callback=self.setDate,ux={'size':(24,24),'text': f'{i+1}'},parent= kwargs.get('parent',None),layer=self.layer,group=self.group))
            self.ids.append(self.button_array[-1])
        
        self.current_date = str(datetime.today()).split(' ')[0].split('-')
        
        self.selected_day = int(self.current_date[2])
        self.selected_month = int(self.current_date[1])
        self.selected_year = int(self.current_date[0])
        
        
        #self.date_select_label.set_image(self.date_select_label.UX.gen())
        self.date_show_label = UILabel(Rect(-1000,-1000,72,24),parent= kwargs.get('parent',None),layer=self.layer,group=self.group)
        self.change_month_back_button = UIButton(Rect(-1000,-1000,24,24),on_press_callback=self.setMonthLast,ux={'size':(24,24),'text': f'<'},parent= kwargs.get('parent',None),layer=self.layer,group=self.group)
        self.change_month_next_button = UIButton(Rect(-1000,-1000,24,24),on_press_callback=self.setMonthNext,ux={'size':(24,24),'text': f'>'},parent= kwargs.get('parent',None),layer=self.layer,group=self.group)
        self.date_select_label = UILabel(Rect(-1000,-1000,144,24),ux={'text': 'Date Selector','size':(144,24)},parent= kwargs.get('parent',None),layer=self.layer,group=self.group)
        self.changeMonth()
        
    def changeMonth(self,*_):
        weekday,days = calendar.monthrange(self.selected_year,self.selected_month)
        self.buttons = []
        x , y = 0 , 0
        d = 0
        for btn in self.button_array:
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
        self.date_select_label.pos = self.pos
        self.change_month_back_button.pos = self.pos[0]+(24),(24*(y+1))+self.pos[1]
        self.change_month_next_button.pos = self.pos[0]+(24*5),(24*(y+1))+self.pos[1]
        self.date_show_label.pos = self.pos[0]+(24*2),(24*(y+1))+self.pos[1] # ADD +1 to y for under placement
        self.date_show_label.UX.text = f'{self.selected_day}/{self.selected_month}/{self.selected_year}'
        self.date_show_label.set_image(self.date_show_label.UX.gen())
        return x,y
    def setMonthLast(self,*_):
        self.selected_month -= 1
        if self.selected_month < 1:
            self.selected_month += 12
            self.selected_year -= 1
        self.changeMonth()
    def setMonthNext(self,*_):
        self.selected_month += 1
        if self.selected_month > 12:
            self.selected_month -= 12
            self.selected_year += 1
        self.changeMonth()
    def setDate(self,*_):
        
        self.selected_day = self.ids.index(_[0]) + 1
        self.date_show_label.UX.text = f'{self.selected_day}/{self.selected_month}/{self.selected_year}'
        self.date_show_label.set_image(self.date_show_label.UX.gen())
    def getDate(self):
        _ret = ''
        if self.selected_day < 10:
            _ret += f'0{self.selected_day}-'
        else:
            _ret += f'{self.selected_day}-'
        if self.selected_month < 10:
            _ret += f'0{self.selected_month}-'
        else:
            _ret += f'{self.selected_month}-'
        return _ret + str(self.selected_year)