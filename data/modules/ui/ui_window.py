from data.modules.constants import TEXT_COLOR, MEDIUM_BACKGROUND_COLOR, DEFAULT_BACKGROUND_COLOR
from data.modules.ui.ui_element import UIElement, UIC
from pygame import Surface, Rect, SRCALPHA
from pygame.draw import rect as rect_draw
from data.modules.ui.ui_font import FONTDRAW
from data.modules.ui.ui_calculation import get_center
from pygame.mouse import get_pos
class UXWindow:
    def __init__(self,**options) -> None:
        self.size = options.get('size',(128,256))
        self.border_radius = options.get('border_radius',15)
        self.text_color = options.get('text_color',TEXT_COLOR)
        self.bar_color = options.get('bar_color',MEDIUM_BACKGROUND_COLOR)
        self.bg_color = options.get('bg_color',DEFAULT_BACKGROUND_COLOR)
        self.text = options.get('text','')
        self.surface = self.gen()
        #! Draw Top
        #! Draw Bottom
        #? _[]X in the next versions?
        #* This Element is needed for Node Building
    def gen(self):
        SURF = Surface(self.size,SRCALPHA)
        rect_draw(
            SURF,
            self.bg_color,
            (
                0,
                0,
                *self.size
                ),
            border_radius = self.border_radius
        )
        rect_draw(
            SURF,
            self.bar_color,
            (
                0,
                0,
                self.size[0],
                24
                ),
            border_top_left_radius = self.border_radius,
            border_top_right_radius = self.border_radius
        )
        
        img = FONTDRAW.draw(
            self.text,
            color=self.text_color
            )
        
        SURF.blit(
            img,
            get_center(
                (self.size[0],24),
                img.get_size()
                )
            )
        
        return SURF

class UIWindowManager:
    def __init__(self) -> None:
        self.window_move_id = -1
        self.window_busy = False
    def check_id(self,id):
        return self.window_move_id == id
UIWM = UIWindowManager()

class UIWindow(UIElement):
    def __init__(self, rect: Rect, **kwargs):
        UIC.add_element('uiWindow')
        super().__init__(rect, **kwargs)
        self.UX = UXWindow(**kwargs.get('ux',{}))
        self.set_image(self.UX.gen())
        self.last_mouse_pos = (0,0)
        self.drag = False
    def update(self):
        mX,mY = get_pos()
        x,y = self.get_abs_position()
        w,h = self.dest[0],24
        
        if self.drag:
            self.pos = (mX) - (self.UX.surface.get_width() // 2), mY - 12
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
