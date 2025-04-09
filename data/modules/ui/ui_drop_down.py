from data.modules.data_management import UnpackManager
from data.modules.ui.ui_element import UIElement, UIC
from pygame import Surface, Rect, Color, SRCALPHA
from data.modules.ui.ui_button import UIButton
class UIDropDown(UIElement):
    def __init__(self, rect: Rect, **kwargs) -> None:
        super().__init__(rect, **kwargs)
        self.setImage(Surface((1,1)))
        self.toggle = False
        self.motherInstanceButton = UIButton(rect,ux=UnpackManager('ux',kwargs,{}),onPressCallback=self.switch,layer=self.layer,parent=self.parent,group=self.group)
        self.childInstances = []
        ux = UnpackManager('ux',kwargs,{})
        rect.x = 0
        rect.y = 0
        self._callbacks = []
        for text,callback in UnpackManager('childsInstances',kwargs,[]):
            
            ux['text'] = text
            rect.y += 24
            UIB = UIButton(rect,ux=ux,onPressCallback=self.btnPress,parent=self,layer=self.layer,group=self.group)
            self.childInstances.append(UIB)
            self._callbacks.append((callback,UIB.elementId))
        for e in self.childInstances:
            
            e.visible = False
    def btnPress(self,*_):
       
        for callback,id in self._callbacks:
            if id == _[0].elementId:
                _[0].thisFramePressed = False
                callback(_[0])
                break
        self.toggle = False
        for e in self.childInstances:
           
            e.visible = self.toggle
    def switch(self,*_):
        self.toggle = not self.toggle
        for e in self.childInstances:
           
            e.visible = self.toggle

    def update(self):
        return super().update()
