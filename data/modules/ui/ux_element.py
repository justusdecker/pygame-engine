from pygame import Color,Surface
from data.modules.ui.ui_font import FONTDRAW
from data.modules.vector import Vector2,Vector4
from pygame import Surface, SRCALPHA
from pygame.draw import rect as rect_draw
from data.modules.ui.ui_calculation import get_center
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
        
        self.array = [color if color else Color(0,0,0,0) for color in colors]
    def get(self,index:int):
        if index < len(self.array):
            return self.array[index]
        return self.array[len(self.array)-1]
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
                 border_radius:int,
                 size: list[int,int]):
        
        self.array = []
        for col_or_surf in colors_or_surfaces:
            if isinstance(col_or_surf,str) or isinstance(col_or_surf,tuple):
                surf = Surface(size)
                rect_draw(surf,Color(col_or_surf),(0,0,*size),border_radius= border_radius)

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
    
    GEN METHOD
    ******
    Takes a list that contains layers
    
    each layer is then iterated to get the ind, obj & vec values.
    
    ind is used to find the corresponding option: font,rect or surf
    
    obj is the argument for the font,rect or surf elements.
    
    vec is the vector to determine the blit pos or the pos & dest.
    """
    def __init__(self, **options):
        self.size = options.get('size',(1,1))
        self.border_radius = options.get('border_radius',15)
        self.text_color_group = ColorGroup(options.get('tcg',[]))
        self.background_color_group = TextureGroup(options.get('bcg',[]),self.border_radius,self.size)
        self.text = options.get('text','')
        self.font = options.get('font',FONTDRAW)
        self.tex_arr = []
    def gen(self,group:list,m:int=1):
        self.tex_arr = []
        for idx,layer in enumerate(group):
            SURF = Surface(self.size,SRCALPHA)
            for ind, obj, vec in layer:
                #Syntax: [ind | obj | vec]
                if not ind:
                    SURF.blit(obj,vec.to_list())

                else:

                    img = self.font.draw(self.text, color= obj, size = self.font.font.get_height())
                    if vec == 'center':
                        SURF.blit(img,get_center(self.size,img.get_size()))
                    else:
                        SURF.blit(img,vec.to_list())

                    
            self.tex_arr.append(SURF)
            
        return self.tex_arr[0:m]