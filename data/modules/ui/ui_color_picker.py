
from data.modules.ui.ui_element import UIElement, UIC
from data.modules.ui.ui_button import UIButton
from data.modules.ui.ux_element import UXElement
from data.modules.graphics_rendering import ColorLine,ColorRect

class UXColorPicker(UXElement):
    def __init__(self):
        pass
class UIColorPicker(UIElement):
    def __init__(self, rect, **kwargs):
        super().__init__(rect, **kwargs)
        UIC.add_element('uiColorPicker')
        
        
        
        """
        Needed:
            Background UX
            Preview
            RGB Value Textinputs
            HSV Value Textinputs
            HEX Value Textinput
            SET Button
            RST Button
            Color Picker?
        """