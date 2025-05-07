from data.modules.ui.ui_element import UIElement, UIC
from data.modules.ui.ui_button import UIButton
from data.modules.ui.ui_label import UILabel
from pygame import Rect, K_RETURN, K_BACKSPACE
from data.modules.constants import GLOBAL_DELTA_TIME
from pygame.key import get_pressed as kb_get_pressed
from pygame.mouse import get_pressed as m_get_pressed
class UITextInput(UIElement):
    def __init__(self, rect: Rect, **kwargs):
        super().__init__(rect, **kwargs)
        UIC.add_element('uiTextInput')
        self.default_text = kwargs.get('default_text','Enter Text...')
        self.max_letters = kwargs.get('max_letters',32)
        self.text = ''
        self.active = False
        self.mode = kwargs.get('mode',False)
        self.count = 0
        self.delete = False
        
        if 'app' in kwargs:
            self.app = kwargs['app']
        else:
            raise Exception('No App. No Game!')
        
        self.enter_button = UIButton(rect,ux={'size':self.dest,'tcg': [],'bcg': []},cb_on_press=self.set_active,parent=self.parent,layer=self.layer+1,group=self.group)
        
        self.text_label = UILabel(rect,ux={'size':self.dest},parent=self.parent,layer=self.layer+1,group=self.group)
        
        self.text_label.render(self.default_text)
        
        
    def set_i(self,text):
        self.text_label.UX.text = text
        self.text = text
        self.text_label.set_image(self.text_label.UX.gen())
    def set_active(self,*_):
        self.active = not self.active
    def set_text(self):
        """
        Check Pygame events for KEYDOWN Events and save them in self.text
        """
        if not self.enter_button.is_hovered and m_get_pressed()[0]:
            self.active = False
        #CTRL = self.app.pressed_keys#! Deprecated
        pressed_list = kb_get_pressed()
        if pressed_list[K_RETURN]:
            
            self.active = False
        if pressed_list[K_BACKSPACE] and not pressed_list[K_RETURN] and not self.delete:
            self.text = self.text[:-1]
            self.delete = True
        elif not pressed_list[K_BACKSPACE]:
            self.delete = False

            
        for key in self.app.pressed_keys:#! Deprecated
            if not pressed_list[K_RETURN]:
                self.append_characters(key)
        if self.text == '' and self.text_label.UX.text != self.default_text:
            self.text_label.render(self.default_text)
        if self.active:
            self.text_label.render(self.get_text_ex())
            
    def overwrite_text(self,text):
        self.text_label.render(text)      
        
    def append_characters(self,char):
        self.text = str(self.text)
        if len(str(self.text)) < self.max_letters:
            if char <= 0x7E and char >= 0x20:
                self.text += chr(char)
    def get_text(self):
            """
                Get Text Raw
            """
            return '' if self.text is None else self.text
    def get_text_ex(self):
        """
        Get Text with Blinker
        """
        return ('' if self.text is None else self.text )+ ('|' if int(self.count) % 2 == 0 else '')
    def update(self):
        self.count += GLOBAL_DELTA_TIME.get()
        if self.active:
            self.set_text()
            if self.mode == 'hex_color_value':
                text = ''
                for i,char in enumerate(self.text):
                    if char.upper() in '0123456789ABCDEF#':
                        text += char
                if not text:
                    self.text = ''
                else:
                    if text[0] != '#' or len(text) != 7:
                        self.text = ''
                self.text = text
            elif self.mode == 'only_numbers':
                text = ''
                for i,char in enumerate(self.text):
                    if char.isdecimal() or (char == '-' and i == 0 ):
                        text += char
                self.text = text
            elif self.mode == 'only_pos_numbers':
                text = ''
                for char in self.text:
                    if char.isdecimal():
                        text += char
                self.text = text
            elif self.mode == 'float':
                text = ''
                sp_text = self.text.split('.')
                if sp_text.__len__() == 2:
                    if not sp_text[0].replace('-','').isdecimal():
                        
                        if not sp_text[1].isdecimal() and sp_text[1] != '':
                            
                            self.text = ''
        return super().update()
