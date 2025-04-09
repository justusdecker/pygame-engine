

from data.modules.ui.ui_element import UIElement, UIC
from pygame import Surface, Rect, Color, SRCALPHA
from data.modules.ui.ui_font import FONTDRAW
from data.modules.ui.ui_calculation import getCenter
from data.modules.data_management import UnpackManager
from pygame.draw import rect as rect_draw
from data.modules.constants import (DEFAULT_BACKGROUND_COLOR,
                                    TEXT_COLOR,
                                    PRESSED_TEXT_COLOR,
                                    HIGHLIGHT_TEXT_COLOR)

class UXButton:
    def __init__(self,
                 **options) -> None:
        
        self.size = UnpackManager('size',options,(64,24))
        self.borderRadius = UnpackManager('borderRadius',options,15)
        
        
        self.normalTextColor = UnpackManager('normal_text_color',options,Color(TEXT_COLOR))
        self.hoveredTextColor = UnpackManager('hovered_text_color',options,Color(HIGHLIGHT_TEXT_COLOR))
        self.pressedTextColor = UnpackManager('pressed_text_color',options,Color(PRESSED_TEXT_COLOR))
        
        self.normalColor = UnpackManager('normal_color',options,Color(DEFAULT_BACKGROUND_COLOR))
        self.hoveredColor = UnpackManager('hovered_color',options,Color(DEFAULT_BACKGROUND_COLOR))
        self.pressedColor = UnpackManager('pressed_color',options,Color(DEFAULT_BACKGROUND_COLOR))
        
        self.text = UnpackManager('text',options,'')
        self.draw()
    def getAllImages(self):
        return self.normalImage,self.hoveredImage,self.pressedImage 
    def draw(self):
        self.normalImage , self.hoveredImage , self.pressedImage = self.gen(
            [
                (self.normalTextColor,self.normalColor),
                (self.hoveredTextColor,self.hoveredColor),
                (self.pressedTextColor,self.pressedColor)
            ]
        )
        
    def gen(self,array:list=[]):
        _ret = []
        for textColor,backgroundColor in array:
            SURF = Surface(self.size,SRCALPHA)
            rect_draw(
                SURF,
                backgroundColor,
                (
                    0,
                    0,
                    *self.size
                    ),
                border_radius = self.borderRadius
            )
            
            img = FONTDRAW.draw(
                self.text,
                color=textColor
                )
            
            SURF.blit(
                img,
                getCenter(
                    self.size,
                    img.get_size()
                    )
                )
            _ret.append(SURF)
        return _ret

class UIButton(UIElement):
    def __init__(self,
                 rect:Rect,
                 **kwargs) -> None:
        UIC.addElement('uiButton')
        
        
        self.UX = UXButton(
            **UnpackManager(
                'ux',
                kwargs,
                {}
                )
            )
            
        self.setImage(self.UX.normalImage)
        super().__init__(rect,**kwargs)
        
        self.oHC = UnpackManager('onHoveredCallback',kwargs,self.noCallback)
        
        self.oPC = UnpackManager('onPressCallback',kwargs,self.noCallback)
        
        self.oUHC = UnpackManager('onUnHoverCallback',kwargs,self.noCallback)
        
        self.oUPC = UnpackManager('onUnPressCallback',kwargs,self.noCallback)
        
    def noCallback(self,btn):
        pass
    def update(self):
        #Change Texture on the fly
        if self.thisFrameHovered:
            self.setImage(self.UX.hoveredImage)
            self.oHC(self)
        if self.thisFramePressed:
            self.setImage(self.UX.pressedImage)
            self.oPC(self)
        if self.thisFrameUnPressed:
            self.setImage(self.UX.normalImage)
            self.oUPC(self)
        if self.thisFrameUnHovered:
            self.setImage(self.UX.normalImage)
            self.oUHC(self)
        super().update()
