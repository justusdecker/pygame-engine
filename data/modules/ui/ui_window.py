from data.modules.constants import TEXT_COLOR, MEDIUM_BACKGROUND_COLOR, DEFAULT_BACKGROUND_COLOR
from data.modules.ui.ui_element import UIElement, UIC
from pygame import image
from pygame.draw import rect as rect_draw
from data.modules.ui.ui_font import FONTDRAW
from data.modules.ui.ui_calculation import get_center
from data.modules.ui.ux_element import UXElement
from data.modules.vector import Vector4
from pygame.mouse import get_pos
class UXWindow(UXElement):
    def __init__(self,**options) -> None:
        if 'bcg' not in options:
            options['bcg'] = (DEFAULT_BACKGROUND_COLOR,MEDIUM_BACKGROUND_COLOR)
        if 'tcg' not in options:
            options['tcg'] = (TEXT_COLOR,)
        super().__init__(**options)
        
        self.text = options.get('text','')
        
    def draw(self):
        g = [
                [[0,self.background_color_group.get(0),Vector4(0,0,*self.size)],[0,self.background_color_group.get(1),Vector4(0,0,self.size[0],24)],[1,self.text_color_group.get(0),'window-text-center+h:24']]
        ]
        return self.gen(g)[0]
        #? _[]X in the next versions?

class UIWindowManager:
    def __init__(self) -> None:
        self.window_move_id = -1
        self.window_busy = False
    def check_id(self,id):
        return self.window_move_id == id
UIWM = UIWindowManager()

class UIWindow(UIElement):
    def __init__(self, vector: Vector4, **kwargs):
        UIC.add_element('uiWindow')
        super().__init__(vector, **kwargs)
        self.UX = UXWindow(**kwargs.get('ux',{}))
        
        self.set_image(self.UX.draw())
        self.last_mouse_pos = (0,0)
        self.drag = False
    def update(self):
        
        mX,mY = get_pos()
        x,y = self.get_abs_position()
        w,h = self.dest[0],24
        
        if self.drag:
            self.pos = (mX) - (self.surface.get_width() // 2), mY - 12
            self.last_mouse_pos = mX,mY
        
        #! Sollte die Maus über der Bar liegen und gedrückt sein. Dann ist das Fenster beweglich.
        #? Aber nur falls nicht schon ein anderes Fenster UIWM belegt!
        if mX > x and mY > y and mX < x + w and mY < y + h and self.is_pressed:
            #? Ist UIWM nicht beschäftigt mit einem anderen Fenster dann:
            if not UIWM.window_busy:
                self.drag = True
                UIWM.window_busy = True
                UIWM.window_move_id = self.element_id
        else:
            #! Ist UIWM beschäftigt nicht mit diesem Element sondern einem anderem
            if not UIWM.check_id(self.element_id):
                self.drag = False
            else:
                self.drag = False
                UIWM.window_busy = False
                UIWM.window_move_id = -1
        super().update()
