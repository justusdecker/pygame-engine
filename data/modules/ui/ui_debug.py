from pygame import Rect,Surface
from pygame.draw import rect as draw_rect, line as draw_line

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
    