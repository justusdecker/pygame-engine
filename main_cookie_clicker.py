from data.modules.constants import *

from pygame import Rect,image, Color
from data.modules.ui.ui_font import FONT

from data.modules.ui.ui_element import UIM

from data.modules.ui.ui_label import UILabel
from data.modules.ui.ui_button import UIButton

from data.modules.app import Application
from data.modules.animation import Animation
from data.modules.audio_handler import AudioHandler
BUTTON_COLORS = {'tcg':('#FFE5CC','#FFF5FF','#D2BFAC'),'bcg':('#CC6600',)}

BUTTON_DEST = (WIDTH*.15,HEIGHT*.1)

UPGRADE_BUTTON_UX = {'size': BUTTON_DEST, 'font':FONT(size=20), 'border_radius':45, **BUTTON_COLORS}

def test_print(*args):
    print(args, "Hello World!")

class CookieClicker:
    def __init__(self):
        self.cookies = 0
        self.upgrades = {
            'cursor': 0,
            'grandma': 0,
            'farm': 0,
            'mine': 0,
            'factory': 0
        }
        self.multiplicators = {
            'cursor': 1,
            'grandma': 1,
            'farm': 1,
            'mine': 1,
            'factory': 1
        }
    def get_auto_clicker(self):
        CURSOR = self.upgrades['cursor'] * 0.1 * self.multiplicators['cursor']
        GRANDMA = self.upgrades['grandma'] * self.multiplicators['grandma']
        FARM = self.upgrades['farm'] * 8 * self.multiplicators['farm']
        MINE = self.upgrades['mine'] * 47 * self.multiplicators['mine']
        FACTORY = self.upgrades['factory'] * 65 * self.multiplicators['factory']
        
        return CURSOR + GRANDMA + FARM + MINE + FACTORY
    def update(self):
        self.cookies += GLOBAL_DELTA_TIME.get() * self.get_auto_clicker()
    def get_multiplicator_price(self,key):
        if self.multiplicators[key] > 2: return False
        return {'cursor': (100,1000),
         'grandma': (5000,10000),
         'farm': (50_000,200_000),
         'mine': (400_000,600_000),
         'factory': (800_000,1_200_000)
         }[key][self.multiplicators[key]-1]
    def get_price(self,key):
        return int({'cursor': 15 + (15 * self.upgrades['cursor'] * 0.2),
         'grandma': 100 + (100*self.upgrades['grandma']*0.2),
         'farm': 1_100 + (1_100*self.upgrades['farm']*0.2),
         'mine': 12_000 + (12_000*self.upgrades['mine']*0.2),
         'factory': 130_000 + (130_000*self.upgrades['factory']*0.2)
         }[key])
    def upgrade_multiplicator(self,button:UIButton):
        key = button.element_name
        price = self.get_multiplicator_price(key)
        if not price: return
        if self.get() >= price:
            self.cookies -= price
            self.multiplicators[key] += 1
    def upgrade(self,button:UIButton):
        key = button.element_name
        price = self.get_price(key)
        if self.get() >= price:
            self.cookies -= price
            self.upgrades[key] += 1
    def click(self):
        self.cookies += 1
    def get(self):
        return int(self.cookies)

class App(Application):
    def __init__(self):
        super().__init__()
        self.audio_handler = AudioHandler(sfx_lib={'click': "data\\bin\\click.mp3"})
        self.cc = CookieClicker()
        self.mine_button = UIButton(
            Rect(HALF_WIDTH-(QUARTER_HEIGHT >> 1),HALF_HEIGHT-(QUARTER_HEIGHT >> 1),QUARTER_HEIGHT,QUARTER_HEIGHT),
            ux={
                'size': (QUARTER_HEIGHT,QUARTER_HEIGHT),
                'font':FONT(size=40),
                'border_radius':45,
                'bcg': ('',)
                },
            on_press_callback = self.on_cookie_click
        )
        
        #? Level Up & Multiplicator Buttons
        
        self.lvl_cursor_upgrade_button = UIButton( Rect(0,0,*BUTTON_DEST), ux={ 'text': f'Cursor: {self.cc.get_price("cursor")}', **UPGRADE_BUTTON_UX }, on_press_callback = self.cc.upgrade,element_name = 'cursor')
        
        self.lvl_cursor_multiplicator_upgrade_button = UIButton( Rect(WIDTH*.15,0,*BUTTON_DEST), ux={'text': f'Multiplicator: {self.cc.get_multiplicator_price("cursor")}', **UPGRADE_BUTTON_UX}, on_press_callback = self.cc.upgrade_multiplicator,element_name = 'cursor')
        
        self.lvl_grandma_upgrade_button = UIButton( Rect(0,HEIGHT*.1,*BUTTON_DEST), ux={'text': f'Grandma: {self.cc.get_price("grandma")}', **UPGRADE_BUTTON_UX},on_press_callback = self.cc.upgrade,element_name = 'grandma')
        
        self.lvl_grandma_multiplicator_upgrade_button = UIButton( Rect(WIDTH*.15,HEIGHT*.1,*BUTTON_DEST),ux={'text': f'Multiplicator: {self.cc.get_multiplicator_price("grandma")}', **UPGRADE_BUTTON_UX},on_press_callback = self.cc.upgrade_multiplicator,element_name = 'grandma')
        
        self.lvl_farm_upgrade_button = UIButton( Rect(0,HEIGHT*.2,*BUTTON_DEST),ux={'text': f'Farm: {self.cc.get_price("farm")}',**UPGRADE_BUTTON_UX},on_press_callback = self.cc.upgrade,element_name = 'farm')
        
        self.lvl_farm_multiplicator_upgrade_button = UIButton( Rect(WIDTH*.15,HEIGHT*.2,*BUTTON_DEST),ux={'text': f'Multiplicator: {self.cc.get_multiplicator_price("farm")}',**UPGRADE_BUTTON_UX},on_press_callback = self.cc.upgrade_multiplicator,element_name = 'farm')
        
        self.lvl_mine_upgrade_button = UIButton( Rect(0,HEIGHT*.3,*BUTTON_DEST),ux={'text': f'Mine: {self.cc.get_price("mine")}',**UPGRADE_BUTTON_UX},on_press_callback = self.cc.upgrade,element_name = 'mine')
        
        self.lvl_mine_multiplicator_upgrade_button = UIButton(Rect(WIDTH*.15,HEIGHT*.3,*BUTTON_DEST),ux={'text': f'Multiplicator: {self.cc.get_multiplicator_price("mine")}',**UPGRADE_BUTTON_UX},on_press_callback = self.cc.upgrade_multiplicator,element_name = 'mine')
        
        self.lvl_factory_upgrade_button = UIButton( Rect(0,HEIGHT*.4,*BUTTON_DEST),ux={'text': f'Factory: {self.cc.get_price("factory")}',**UPGRADE_BUTTON_UX},on_press_callback = self.cc.upgrade,element_name = 'factory')
        
        self.lvl_factory_multiplicator_upgrade_button = UIButton( Rect(WIDTH*.15,HEIGHT*.4,*BUTTON_DEST),ux={'text': f'Multiplicator: {self.cc.get_multiplicator_price("factory")}',**UPGRADE_BUTTON_UX},on_press_callback = self.cc.upgrade_multiplicator,element_name = 'factory')
        
        self.cookie_label = UILabel(
            Rect(QUARTER_WIDTH*1.5,0,QUARTER_WIDTH,HEIGHT*.1),
            ux = {
                'text': '0',
                'size': (QUARTER_WIDTH,HEIGHT*.1),
                'font': FONT(size=40),
                'bcg': ('#CC6600',),
                'tcg': ('#FFE5CC',)
            }
        )


        self.animation = Animation(self,
                                   image.load("data\\bin\\img\\cookie.png"),
                                   [
                                       {
            "x_offset": 0,
            "y_offset": 0,
            "scale": [.3,.3]
        },{
            "x_offset": 0,
            "y_offset": 10,
            "scale": [.28,.3]
        },{
            "x_offset": 0,
            "y_offset": 20,
            "scale": [.25,.3]
        },{
            "x_offset": 0,
            "y_offset": 40,
            "scale": [.3,.25]
        },{
            "x_offset": 0,
            "y_offset": 40,
            "scale": [.35,.15]
        },{
            "x_offset": 0,
            "y_offset": 40,
            "scale": [.3,.25]
        },{
            "x_offset": 0,
            "y_offset": 20,
            "scale": [.25,.3]
        },{
            "x_offset": 0,
            "y_offset": 10,
            "scale": [.28,.3]
        }
                                   ],
                                   (HALF_WIDTH,HALF_HEIGHT),time_multiplier=50)
    def update_cookie_label(self):
        self.cookie_label.UX.text = f"{self.cc.get()}" + (f"+{self.cc.get_auto_clicker():.1f}" if self.cc.get_auto_clicker() else '')
        self.cookie_label.set_image(self.cookie_label.UX.gen())
            
    def on_cookie_click(self,*_):
        self.audio_handler.play_sound('click')
        self.animation.start_animation()
        self.cc.click()
    def run(self):
        
        while self.is_running:
            GLOBAL_DELTA_TIME.before()
            self.window.surface.fill(Color('#FFB266'))
            #! Button image dont change !
            if self.lvl_cursor_upgrade_button.this_frame_hovered:
                self.lvl_cursor_upgrade_button.UX.text = f'Cursor: {self.cc.get_price("cursor")}'
                self.lvl_cursor_upgrade_button.UX.draw()
            if self.lvl_grandma_upgrade_button.this_frame_hovered:
                self.lvl_grandma_upgrade_button.UX.text = f'Grandma: {self.cc.get_price("grandma")}'
                self.lvl_grandma_upgrade_button.UX.draw()
            if self.lvl_farm_upgrade_button.this_frame_hovered:
                self.lvl_farm_upgrade_button.UX.text = f'Farm: {self.cc.get_price("farm")}'
                self.lvl_farm_upgrade_button.UX.draw()
            if self.lvl_mine_upgrade_button.this_frame_hovered:
                self.lvl_mine_upgrade_button.UX.text = f'Mine: {self.cc.get_price("mine")}'
                self.lvl_mine_upgrade_button.UX.draw()
            if self.lvl_factory_upgrade_button.this_frame_hovered:
                self.lvl_factory_upgrade_button.UX.text = f'Factory: {self.cc.get_price("factory")}'
                self.lvl_factory_upgrade_button.UX.draw()
            if self.lvl_cursor_multiplicator_upgrade_button.this_frame_hovered:
                price = self.cc.get_multiplicator_price("cursor")
                text = f'Multiplicator: {price}' if price else 'MAX'
                self.lvl_cursor_multiplicator_upgrade_button.UX.text = text
                self.lvl_cursor_multiplicator_upgrade_button.UX.draw()
            if self.lvl_grandma_multiplicator_upgrade_button.this_frame_hovered:
                price = self.cc.get_multiplicator_price("grandma")
                text = f'Multiplicator: {price}' if price else 'MAX'
                self.lvl_grandma_multiplicator_upgrade_button.UX.text = text
                self.lvl_grandma_multiplicator_upgrade_button.UX.draw()
            if self.lvl_farm_multiplicator_upgrade_button.this_frame_hovered:
                price = self.cc.get_multiplicator_price("farm")
                text = f'Multiplicator: {price}' if price else 'MAX'
                self.lvl_farm_multiplicator_upgrade_button.UX.text = text
                self.lvl_farm_multiplicator_upgrade_button.UX.draw()
            if self.lvl_mine_multiplicator_upgrade_button.this_frame_hovered:
                price = self.cc.get_multiplicator_price("mine")
                text = f'Multiplicator: {price}' if price else 'MAX'
                self.lvl_mine_multiplicator_upgrade_button.UX.text = text
                self.lvl_mine_multiplicator_upgrade_button.UX.draw()
            if self.lvl_factory_multiplicator_upgrade_button.this_frame_hovered:
                price = self.cc.get_multiplicator_price("factory")
                text = f'Multiplicator: {price}' if price else 'MAX'
                self.lvl_factory_multiplicator_upgrade_button.UX.text = text
                self.lvl_factory_multiplicator_upgrade_button.UX.draw()
            UIM.render_queue(self)
            self.animation.update()
            self.cc.update()
            self.update_cookie_label()
            self.update()
            GLOBAL_DELTA_TIME.after()

if __name__ == "__main__":
    APP = App()
    APP.run()