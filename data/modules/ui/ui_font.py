from pygame import font
from pygame import Color
class FONT:
    def __init__(self) -> None:
        font.init()
        self.font = font.SysFont('bahnschrift',13)
    def draw(self,
             text: str = '',
             aa: bool = True,
             color: tuple | list | Color = Color('#454545'),
             size: int = 13):
        self.font.set_point_size(size)

        return self.font.render(text,aa,color)
    
FONTDRAW = FONT()