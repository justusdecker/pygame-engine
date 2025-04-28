from data.modules.ui.ui_element import UIElement, UIC
from data.modules.ui.ux_element import UXElement, TextureGroup
from data.modules.constants import MEDIUM_BACKGROUND_COLOR,TEXT_COLOR,HIGHLIGHT_TEXT_COLOR,PRESSED_TEXT_COLOR
from pygame.draw import rect as rect_draw
from pygame import Surface, Rect, SRCALPHA
from data.modules.vector import Vector2


class UXSwitch(UXElement):
    
    def __init__(self,
                 **options) -> None:
        if not 'bcg' in options: options['bcg'] = (MEDIUM_BACKGROUND_COLOR,)
        if not 'fcg' in options: options['fcg'] = (TEXT_COLOR,HIGHLIGHT_TEXT_COLOR,PRESSED_TEXT_COLOR)
        
        super().__init__(**options)
        self.foreground_color_group = TextureGroup(options['fcg'],border_radius=self.border_radius,size=(self.size[0]-4,self.size[1]-4))
        self.normal_off_image,self.hovered_off_image, self.pressed_off_image,self.normal_on_image,self.hovered_on_image, self.pressed_on_image = self.draw()
    def draw(self):
        "Use this in case you want to redraw the switch."
        V_A, V_B = Vector2(0,0), Vector2(2,2)
        g= [
            [
                [0,self.background_color_group.get(0),V_A],
                ],
            [
                [0,self.background_color_group.get(0),V_A],
                ],
            [
                [0,self.background_color_group.get(0),V_A],
                ],[
                [0,self.background_color_group.get(0),V_A],
                [0,self.foreground_color_group.get(1),V_B]
                ],
            [
                [0,self.background_color_group.get(0),V_A],
                [0,self.foreground_color_group.get(2),V_B]
                ],
            [
                [0,self.background_color_group.get(0),V_A],
                [0,self.foreground_color_group.get(3),V_B]
                ]
        ]
        
        return self.gen(g,6)
    def gen1(self,array:list=[]):
        """
        Get the switch images. Off / On states.
        """
        _ret = []
        for foreground_color,state in array:
            SURF = Surface(self.size,SRCALPHA)
            rect_draw(
                    SURF,
                    self.get_color(self.background_color_group,0),
                    (0,0,*self.size),
                    border_radius = self.border_radius
                )
            if state:
                rect_draw(
                    SURF,
                    foreground_color,
                    (2,2,self.size[0]-4,self.size[1]-4),
                    border_radius = self.border_radius
                )
            _ret.append(SURF)
        return _ret

class UISwitch(UIElement):
    """
    .. cb_on_hover:: set the callback for on_hover
    .. cb_on_press:: set the callback for on_press
    .. cb_on_un_hover:: set the callback for on_un_hover
    """
    def __init__(self, rect: Rect, **kwargs):
        super().__init__(rect,**kwargs)
        UIC.add_element('uiSwitch')
        self.toggle = kwargs.get('initialValue',False)
        self.UX = UXSwitch(**kwargs.get('ux', {}))
        self.set_image(self.UX.normal_off_image)
        self.oHC = kwargs.get('cb_on_hover',self.noCallback)
        self.oPC = kwargs.get('cb_on_press',self.noCallback)
        self.oUHC = kwargs.get('cb_on_un_hover',self.noCallback)
    def noCallback(self,_):
        pass
    def update(self):
        #Change Texture on the fly
        if self.this_frame_hovered:
            self.set_image([self.UX.hovered_off_image,self.UX.hovered_on_image][self.toggle])
            self.oHC(self)
        if self.this_frame_pressed:
            self.toggle = not self.toggle
            self.set_image([self.UX.normal_off_image,self.UX.normal_on_image][self.toggle])
            self.oPC(self)
        if self.this_frame_un_hovered:
            self.set_image([self.UX.normal_off_image,self.UX.normal_on_image][self.toggle])
            self.oUHC(self)
        super().update()
   