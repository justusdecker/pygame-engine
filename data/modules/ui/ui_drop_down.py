from data.modules.ui.ui_element import UIElement,UIC
from pygame import Surface, Rect
from data.modules.ui.ui_button import UIButton
class UIDropDown(UIElement):
    def __init__(self, rect: Rect, **kwargs) -> None:
        super().__init__(rect, **kwargs)
        self.set_image(Surface((1,1)))
        UIC.add_element('uiDropDown')
        self.toggle = False
        self.mother_instance_button = UIButton(rect,ux=kwargs.get('ux',{}),on_press_callback=self.switch,layer=self.layer,parent=self.parent,group=self.group)
        self.child_instances = []
        ux = kwargs.get('ux',{})
        rect.x = 0
        rect.y = 0
        self._callbacks = []
        for text,callback in kwargs.get('childsInstances',[]):
            
            ux['text'] = text
            rect.y += 24
            UIB = UIButton(rect,ux=ux,on_press_callback=self.btnPress,parent=self,layer=self.layer,group=self.group)
            self.child_instances.append(UIB)
            self._callbacks.append((callback,UIB.element_id))
        for e in self.child_instances:
            
            e.visible = False
    def btnPress(self,*_):
       
        for callback,id in self._callbacks:
            if id == _[0].element_id:
                _[0].this_frame_pressed = False
                callback(_[0])
                break
        self.toggle = False
        for e in self.child_instances:
           
            e.visible = self.toggle
    def switch(self,*_):
        self.toggle = not self.toggle
        for e in self.child_instances:
           
            e.visible = self.toggle

    def update(self):
        return super().update()
