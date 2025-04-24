from pygame import Color,Surface
from data.modules.ui.ui_font import FONTDRAW
"""
If color group doesn't exist create default

color group type: dict
color type: str #242424

UXButtonElement
│
├────┬> color group e.g. (background-color)
│    │
│    ├> normal  0
│    ├> hovered 1
│    └> pressed 2 etc.
│    
└ and so on
"""
class ColorGroup:
    def __init__(self, colors: list[str]):
        
        self.array = [Color(color) if color else Color(0,0,0,0) for color in colors]
class TextureGroup:
    """
    .. array:: A list consisting of pygame Surface objects
    Will throw an TypeError if type is none of the following:
    .. str:: #RRGGBB | #RRGGBBAA
    .. tuple:: (r,g,b) | (r,g,b,a)
    .. Surface:: pygame.Surface object
    """
    def __init__(self, 
                 colors_or_surfaces: list[str | Surface | tuple[int,int,int] | tuple[int,int,int,int]], 
                 size: list[int,int]):
        
        self.array = []
        for col_or_surf in colors_or_surfaces:
            if isinstance(col_or_surf,str) or isinstance(col_or_surf,tuple):
                surf = Surface(size)
                surf.fill(Color(col_or_surf))
                self.array.append(surf)
            elif isinstance(col_or_surf,Surface):
                self.array.append(col_or_surf)
            else:
                raise TypeError('Type must be Surface, tuple or string!')
    def get(self,index:int):
        if index < len(self.array):
            return self.array[index]
        return self.array[len(self.array)-1]
class UXElement:
    """
    .. size:: ``tuple[int,int]``
        
        the ``UXElement`` size can be different to the ``UIElement`` be careful
    .. border_radius:: ``int``
    .. tcg:: ``list[str]``
        text_color_group
    .. bcg:: ``list[str]``
        background_color_group
    .. text:: ``str``
        the text that should be rendered on top of the UXElement. Default is empty
    .. font:: ``data.modules.ui.ui_font.FONT``
    """
    def __init__(self, **options):
        self.size = options.get('size',(1,1))
        self.border_radius = options.get('border_radius',15)
        self.text_color_group = TextureGroup(options.get('tcg',[]))
        self.background_color_group = TextureGroup(options.get('bcg',[]))
        self.text = options.get('text','')
        self.font = options.get('font',FONTDRAW)