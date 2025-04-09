from data.modules.data_management import UnpackManager
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
        UIC.addElement('uiTextInput')
        self.deufault_text = UnpackManager('default_text',kwargs,'Enter Text...')
        self.maxLetters = UnpackManager('maxLetters',kwargs,32)
        self.text = ''
        self.active = False
        self.mode = UnpackManager('mode',kwargs,False)
        self.count = 0
        if 'app' in kwargs:
            self.app = kwargs['app']
        else:
            raise Exception('No App. No Game!')
        self.enterButton = UIButton(rect,ux={'size':self.dest},onPressCallback=self.setActive,parent=self.parent,layer=self.layer+1,group=self.group)
        self.textLabel = UILabel(rect,ux={'size':self.dest},parent=self.parent,layer=self.layer+1,group=self.group)
        self.textLabel.UX.text = self.deufault_text
        self.textLabel.setImage(self.textLabel.UX.gen())
        self.delete = False
    def setI(self,text):
        self.textLabel.UX.text = text
        self.text = text
        self.textLabel.setImage(self.textLabel.UX.gen())
    def setActive(self,*_):
        self.active = not self.active
    def setText(self):
        """
        Check Pygame events for KEYDOWN Events and save them in self.text
        """
        if not self.enterButton.isHovered and m_get_pressed()[0]:
            self.active = False
        CTRL = self.app.keyboardInputs['strg']#! Deprecated
        pressedList = kb_get_pressed()
        if pressedList[K_RETURN]:
            
            self.active = False
        if pressedList[K_BACKSPACE] and not pressedList[K_RETURN] and not self.delete:
            self.text = self.text[:-1]
            self.delete = True
        elif not pressedList[K_BACKSPACE]:
            self.delete = False

            
        for key in self.app.keyboardInputs['currentKeys']:#! Deprecated
            if not pressedList[K_RETURN]:
                self.appChars(key)
        if self.text == '' and self.textLabel.UX.text != self.deufault_text:
            self.textLabel.UX.text = self.deufault_text
            self.textLabel.setImage(self.textLabel.UX.gen())
        if self.active:
            self.textLabel.UX.text = f'{self.getTextEx()}'
            self.textLabel.setImage(self.textLabel.UX.gen())
            
                    
        
    def appChars(self,char):
        self.text = str(self.text)
        if len(str(self.text)) < self.maxLetters:
            self.text += char
    def getText(self):
            """
                Get Text Raw
            """
            return '' if self.text is None else self.text
    def getTextEx(self):
        """
        Get Text with Blinker
        """
        return ('' if self.text is None else self.text )+ ('|' if int(self.count) % 2 == 0 else '')
    def update(self):
        self.count += GLOBAL_DELTA_TIME.get()
        if self.active:
            self.setText()
            if self.mode == 'only_numbers':
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
                spText = self.text.split('.')
                if spText.__len__() == 2:
                    if not spText[0].replace('-','').isdecimal():
                        
                        if not spText[1].isdecimal() and spText[1] != '':
                            
                            self.text = ''
        return super().update()
