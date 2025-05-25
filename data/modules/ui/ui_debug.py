from pygame import Rect,Surface
from pygame.draw import rect as draw_rect, line as draw_line
from data.modules.ui.ui_element import UIElement, UIC
from data.modules.ui.ui_label import UILabel
from data.modules.ui.ui_font import FONT
from data.modules.vector import Vector4
from data.modules.constants import GLOBAL_DELTA_TIME
def outliner(surf: Surface, rect: Rect,o_type:str):
    """
    Use this to make the outlines of UI / UX Elements visible!
    
    .. surf:: A pygame Surface
    
    .. rect:: A pygame Rect: ``x`` , ``y`` , ``w`` , ``h`` 

    .. o_type:: 

        ``self`` or ``subsurface`` = ``0`` or ``1``
    """
    draw_rect(surf,(255,0,0) if o_type else (0,255,0),rect,width=1)
    for i in range(0,rect.h,10):
        
        draw_line(surf,(192,0,0) if o_type else (0,192,0),(rect.w//2,i),(rect.w//2,i + 5),width=1)
    for i in range(0,rect.w,10):
        draw_line(surf,(192,0,0) if o_type else (0,192,0),(i,rect.h//2),(i + 5,rect.h//2),width=1)

class UIDebug(UIElement):
    def __init__(self, vector, **kwargs):
        super().__init__(vector, **kwargs)
        self.fps_lable = UILabel(
            Vector4(0,0,128,48),
            ux={'text': "","size": (128,48),'font': FONT(size=30),'tcg': ('#ffffff',),'bcg': ('#77777744',)},layer=self.layer,parent=self
        )
        self.rt_lable = UILabel(
            Vector4(128,0,128,48),
            ux={'text': "","size": (128,48),'font': FONT(size=30),'tcg': ('#ffffff',),'bcg': ('#77777744',)},layer=self.layer,parent=self
        )
        self.rt_lables = []
        self.timings = []
        if 'render_times' in kwargs:
            for i in range(kwargs['render_times']):
                uil = UILabel(Vector4(0,(i+1)*48,256,48),ux={'text': "","size": (256,48),'font': FONT(size=30),'tcg': ('#ffffff',),'bcg': ('#77777744',)},layer=self.layer,parent=self)
                self.rt_lables.append(uil)
    def add_timings(self,t:list):
        self.timings = t
    def update(self):
        _rt = GLOBAL_DELTA_TIME.get()
        for rt,t in zip(self.rt_lables, self.timings):
            rt.render(f'{t:.2f}ms')
        self.fps_lable.render(f'{int(1//_rt)}fps' if _rt else 'undefined')
        self.rt_lable.render(f'{_rt*1000:.1f}ms' if _rt else 'undefined')
        return super().update()