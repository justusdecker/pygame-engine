from data.modules.ui.ui_element import UIElement
from data.modules.ui.ui_button import UIButton
from data.modules.vector import Vector4
class UIArray(UIElement):
    def __init__(self, vector:Vector4, **kwargs):
        super().__init__(vector,**kwargs)
        
        w,h = kwargs.get('element_size',(8,8))
        self.btn_array = []
        
        for x in range(vector.w // w):

            for y in range(vector.z // h):
                
                pass
                
    def color_change(self,btn:UIButton):
        btn.surface.fill((255,255,255))
    def update(self):
        return super().update()