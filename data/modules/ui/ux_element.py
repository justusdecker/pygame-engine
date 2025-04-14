from pygame import Color
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
        self.array = [Color(color) for color in colors]
        
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
        self.text_color_group = ColorGroup(options.get('tcg',[]))
        self.background_color_group = ColorGroup(options.get('bcg',[]))
        self.text = options.get('text','')
        self.font = options.get('font',FONTDRAW)
    def get_color(self,group:ColorGroup,index:int):
        if index < len(group.array):
            return group.array[index]
        return group.array[len(group.array)-1]    #Missing color indicator