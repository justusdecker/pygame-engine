from data.modules.ui.ui_element import UIElement
from data.modules.ui.ui_button import UIButton
from pygame import Surface
from pygame.transform import scale
from data.modules.vector import Vector4
class UIArray(UIElement):
    def __init__(self, vector:Vector4, **kwargs):
        super().__init__(vector,**kwargs)
        
        w,h = kwargs.get('element_size',(8,8))
        self.btn_array = []
        self.image_vector: Vector4 = vector // Vector4(1,1,w,h)
        self.low_res_surface = Surface(self.image_vector.to_list()[2:])
        self.set_image(scale(self.low_res_surface,vector.to_list()[2:]))
        
                
    def color_change(self,btn:UIButton):
        btn.surface.fill((255,255,255))
    def update(self):
        if self.this_frame_pressed:
            for x in range(self.image_vector.w):

                for y in range(self.image_vector.z):
                    #Check left / right
                    #Check up / down
                    #Change Pixel Color
                    #Recalc / Resize surface
                    pass
        return super().update()