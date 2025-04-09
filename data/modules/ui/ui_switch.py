
from data.modules.data_management import UnpackManager
from data.modules.ui.ui_element import UIElement, UIC
from data.modules.constants import MEDIUM_BACKGROUND_COLOR,TEXT_COLOR,HIGHLIGHT_TEXT_COLOR,PRESSED_TEXT_COLOR
from pygame.draw import rect as rect_draw
from pygame import Surface, Rect, Color, SRCALPHA
class UXSwitch:
    def __init__(self,
                 **options) -> None:
        
        self.size = UnpackManager('size',options,(24,24))
        self.borderRadius = UnpackManager('borderRadius',options,6)
        self.bg =  UnpackManager('bg_color',options,Color(MEDIUM_BACKGROUND_COLOR))
        self.normalColor = UnpackManager('normal_color',options,Color(TEXT_COLOR))
        self.hoveredColor = UnpackManager('hovered_color',options,Color(HIGHLIGHT_TEXT_COLOR))
        self.pressedColor = UnpackManager('pressed_color',options,Color(PRESSED_TEXT_COLOR))
        
        #On: Pressed
        #on: Hove
        #on normal
        #off pressed
        #off hove
        #off normal
        
        self.normalOffImage,self.hoveredOffImage, self.pressedOffImage,self.normalOnImage,self.hoveredOnImage, self.pressedOnImage = self.draw()
    def draw(self):
        return self.gen([
            (self.normalColor,False),
            (self.hoveredColor,False),
            (self.pressedColor,False),
            (self.normalColor,True),
            (self.hoveredColor,True),
            (self.pressedColor,True),
        ])
    def gen(self,array:list=[]):
        _ret = []
        
        
        
        for foregroundColor,state in array:
            SURF = Surface(self.size,SRCALPHA)
            rect_draw(
                    SURF,
                    self.bg,
                    (
                        0,
                        0,
                        *self.size
                        ),
                    border_radius = self.borderRadius
                )
            if state:
                rect_draw(
                    SURF,
                    foregroundColor,
                    (
                        2,
                        2,
                        20,
                        20
                        ),
                    border_radius = self.borderRadius
                )
                
            
            
            _ret.append(SURF)
        return _ret

class UISwitch(UIElement):
    def __init__(self, rect: Rect, **kwargs):
        super().__init__(rect,**kwargs)
        UIC.addElement('uiSwitch')
        self.toggle = UnpackManager('initialValue',kwargs,False)
        self.UX = UXSwitch()
        self.setImage(self.UX.normalOffImage)
        self.oHC = UnpackManager('onHoveredCallback',kwargs,self.noCallback)
        
        self.oPC = UnpackManager('onPressCallback',kwargs,self.noCallback)
        
        self.oUHC = UnpackManager('onUnHoverCallback',kwargs,self.noCallback)
    def noCallback(self,_):
        pass
    def update(self):
        #Change Texture on the fly
        if self.thisFrameHovered:
            self.setImage([self.UX.hoveredOffImage,self.UX.hoveredOnImage][self.toggle])
            self.oHC(self)
        if self.thisFramePressed:
            self.toggle = not self.toggle
            self.setImage([self.UX.normalOffImage,self.UX.normalOnImage][self.toggle])
            self.oPC(self)
        if self.thisFrameUnHovered:
            self.setImage([self.UX.normalOffImage,self.UX.normalOnImage][self.toggle])
            self.oUHC(self)
        super().update()
   