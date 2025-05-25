from data.modules.ui.ui_element import UIElement
from data.modules.ui.ui_button import UIButton
from data.modules.ui.ui_image import UIImage
from pygame.draw import circle
from pygame import Surface,SRCALPHA
from pygame.transform import scale
from pygame.mouse import get_pos
from data.modules.vector import Vector4
from data.modules.logic_2d.algorithms import flood_fill

class UIArray(UIElement):
    def __init__(self, vector:Vector4, **kwargs):
        super().__init__(vector,**kwargs)
        
        w,h = kwargs.get('element_size',(8,8))
        self.btn_array = []
        self.image_vector: Vector4 = Vector4(1,1,w,h)
        self.image = UIImage(vector,ux={'size': vector.to_list()[:2]},group=self.group,parent=self,layer=self.layer)
        self.low_res_surface = Surface((self.dest[0] // w,self.dest[1] // h),SRCALPHA)
        #self.low_res_surface.fill((128,128,128))
        self.image.set_image(scale(self.low_res_surface,self.dest))
        self.set_color((255,255,255))
        self.tool_size = 1
        self.current_tool = 'pixel'
    def color_change(self,btn:UIButton):
        btn.surface.fill((255,255,255))
    def set_color(self,col):
        self.color = col
        
    def get_xy(self) -> tuple[int,int]:
        
        for x in range(self.low_res_surface.get_width()):

            for y in range(self.low_res_surface.get_height()):
                _x = self.pos[0] + (x * self.image_vector.w)
                _y = self.pos[1] + (y * self.image_vector.z)
                _w = self.pos[0] + ((x+1) * self.image_vector.w)
                _h = self.pos[1] + ((y+1) * self.image_vector.z)
                _mx, _my = get_pos()
                if _mx >= _x and _my >= _y and _mx <= _w and _my <= _h:
                    return x,y
    def update(self):
        if self.is_pressed:
            px_set = self.get_xy()
            if px_set is not None:
                #self.low_res_surface.set_at(px_set,self.color)
                match self.current_tool:
                    case 'pixel':
                        self.low_res_surface.set_at(px_set,self.color)
                    case 'brush':
                        circle(self.low_res_surface,self.color,px_set,self.tool_size)
                    case 'fill':
                        flood_fill(self.low_res_surface,*px_set,self.color)
                self.image.set_image(scale(self.low_res_surface,self.dest))

        return super().update()