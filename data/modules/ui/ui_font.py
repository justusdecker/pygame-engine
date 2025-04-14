from pygame import font, Color,Surface,SRCALPHA

class FONT:
    def __init__(self,name:str='bahnschrift',size:int=13) -> None:
        font.init()
        self.font = font.SysFont(name,size)
    def cut_off(self,surf: Surface):
        """
        Fixes the asymmetric problem in issue #32
        """
        for y in range(surf.get_height()):
            if any([surf.get_at((x,y)).a for x in range(surf.get_width())]):
                break
        start = y
        for y in range(surf.get_height()):
            if any([surf.get_at((x,surf.get_height() - 1 - y)).a for x in range(surf.get_width())]):
                break
        end = y
        new_surf = Surface((surf.get_width(),surf.get_height()-start-end),SRCALPHA)
        new_surf.blit(surf,(0,-start))
        return new_surf
    def draw(self,
             text: str = '',
             aa: bool = True,
             color: tuple | list | Color = Color('#454545'),
             size: int = 13):
        
        self.font.set_point_size(size)
        if not text: return Surface((1,1),SRCALPHA)
        return self.cut_off(self.font.render(text,aa,color))
    
FONTDRAW = FONT()