from data.modules.ui.ui_element import UIElement, UIC
from data.modules.constants import MEDIUM_BACKGROUND_COLOR,TEXT_COLOR,HIGHLIGHT_TEXT_COLOR,PRESSED_TEXT_COLOR
from pygame.draw import rect as rect_draw
from pygame import Surface, Rect, Color, SRCALPHA
class UXSwitch:
    def __init__(self,
                 **options) -> None:
        
        self.size = options.get('size',(24,24))
        self.border_radius = options.get('border_radius',6)
        self.bg =  options.get('bg_color',Color(MEDIUM_BACKGROUND_COLOR))
        self.normal_color = options.get('normal_color',Color(TEXT_COLOR))
        self.hovered_color = options.get('hovered_color',Color(HIGHLIGHT_TEXT_COLOR))
        self.pressed_color = options.get('pressed_color',Color(PRESSED_TEXT_COLOR))
        
        #On: Pressed
        #on: Hove
        #on normal
        #off pressed
        #off hove
        #off normal
        
        self.normal_off_image,self.hovered_off_image, self.pressed_off_image,self.normal_on_image,self.hovered_on_image, self.pressed_on_image = self.draw()
    def draw(self):
        return self.gen([
            (self.normal_color,False),
            (self.hovered_color,False),
            (self.pressed_color,False),
            (self.normal_color,True),
            (self.hovered_color,True),
            (self.pressed_color,True),
        ])
    def gen(self,array:list=[]):
        _ret = []
        
        
        
        for foreground_color,state in array:
            SURF = Surface(self.size,SRCALPHA)
            rect_draw(
                    SURF,
                    self.bg,
                    (
                        0,
                        0,
                        *self.size
                        ),
                    border_radius = self.border_radius
                )
            if state:
                rect_draw(
                    SURF,
                    foreground_color,
                    (
                        2,
                        2,
                        20,
                        20
                        ),
                    border_radius = self.border_radius
                )
                
            
            
            _ret.append(SURF)
        return _ret

class UISwitch(UIElement):
    def __init__(self, rect: Rect, **kwargs):
        super().__init__(rect,**kwargs)
        UIC.add_element('uiSwitch')
        self.toggle = kwargs.get('initialValue',False)
        self.UX = UXSwitch()
        self.set_image(self.UX.normal_off_image)
        self.oHC = kwargs.get('onHoveredCallback',self.noCallback)
        
        self.oPC = kwargs.get('onPressCallback',self.noCallback)
        
        self.oUHC = kwargs.get('onUnHoverCallback',self.noCallback)
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
   