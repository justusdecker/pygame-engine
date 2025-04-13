from data.modules.constants import *

from pygame import Rect,image, Color
from data.modules.ui.ui_font import FONT
from pygame.mixer import music,init as mixer_init

from data.modules.ui.ui_element import UIGroup,UIM
from data.modules.ui.ui_image import UIImage
from data.modules.ui.ui_label import UILabel
from data.modules.ui.ui_button import UIButton
from data.modules.ui.ui_switch import UISwitch
from data.modules.ui.ui_drop_down import UIDropDown
from data.modules.ui.ui_progress_bar import UIProgressBar
from data.modules.ui.ui_calendar import UICalendar
from data.modules.ui.ui_time_select import UITimeSelect
from data.modules.ui.ui_text_input import UITextInput
from data.modules.tests.tile_based_game import Map
from data.modules.app import Application
from data.modules.animation import Animation

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
        #efficiency upgrades / doubles the default output
        
        self.lvl_click = 1
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
    def upgrade_multiplicator(self,lvl:str):
        if self.multiplicators[lvl] <= 2:
            price = self.get_multiplicator_price(lvl)
            if self.get() >= price:
                self.cookies -= price
                self.multiplicators[lvl] += 1
    def upgrade(self,lvl:str):
        price = self.get_price(lvl)
        if self.get() >= price:
            self.cookies -= price
            self.upgrades[lvl] += 1
    def buy_cursor_multiplicator(self,*_):
        self.upgrade_multiplicator('cursor')
    def buy_cursor(self,*_):
        self.upgrade('cursor')
    def buy_grandma(self,*_):
        self.upgrade('grandma')
    def buy_grandma_multiplicator(self,*_):
        self.upgrade_multiplicator('grandma')    
    def buy_farm(self,*_):
        self.upgrade('farm')
    def buy_mine(self,*_):
        self.upgrade('mine')
    def buy_factory(self,*_):
        self.upgrade('factory')
    def click(self):
        self.cookies += 1
    def get(self):
        return int(self.cookies)

class App(Application):
    def __init__(self):
        super().__init__()
        mixer_init()
        self.cc = CookieClicker()
        self.mine_button = UIButton(
            Rect(HALF_WIDTH-(QUARTER_HEIGHT//2),HALF_HEIGHT-(QUARTER_HEIGHT//2),QUARTER_HEIGHT,QUARTER_HEIGHT),
            ux={
                'size': (QUARTER_HEIGHT,QUARTER_HEIGHT),
                'font':FONT(size=40),
                'border_radius':45,
                'normal_color': (0,0,0,0),
                'hovered_color': (0,0,0,0),
                'pressed_color': (0,0,0,0)
                },
            on_press_callback = self.on_cookie_click
        )
        self.lvl_cursor_upgrade_button = UIButton(
            Rect(0,0,WIDTH*.15,HEIGHT*.1),
            ux={
                
                'text': f'Cursor: {self.cc.get_price("cursor")}',
                'size': (WIDTH*.15,HEIGHT*.1),
                'font':FONT(size=20),
                'border_radius':45,
                'normal_text_color': Color('#FFE5CC'),
                'hovered_text_color': Color('#FFF5FF'),
                'pressed_text_color': Color('#D2BFAC'),
                'normal_color': Color('#CC6600'),
                'hovered_color': Color('#CC6600'),
                'pressed_color': Color('#CC6600')
                },
            on_press_callback = self.cc.buy_cursor
        )
        
        self.lvl_cursor_multiplicator_upgrade_button = UIButton(
            Rect(WIDTH*.15,0,WIDTH*.15,HEIGHT*.1),
            ux={
                
                'text': f'Multiplicator: {self.cc.get_multiplicator_price("cursor")}',
                'size': (WIDTH*.15,HEIGHT*.1),
                'font':FONT(size=20),
                'border_radius':45,
                'normal_text_color': Color('#FFE5CC'),
                'hovered_text_color': Color('#FFF5FF'),
                'pressed_text_color': Color('#D2BFAC'),
                'normal_color': Color('#CC6600'),
                'hovered_color': Color('#CC6600'),
                'pressed_color': Color('#CC6600')
                },
            on_press_callback = self.cc.buy_cursor_multiplicator
        )
        
        self.lvl_grandma_upgrade_button = UIButton(
            Rect(0,HEIGHT*.1,WIDTH*.15,HEIGHT*.1),
            ux={
                
                'text': f'Grandma: {self.cc.get_price("grandma")}',
                'size': (WIDTH*.15,HEIGHT*.1),
                'font':FONT(size=20),
                'border_radius':45,
                'normal_text_color': Color('#FFE5CC'),
                'hovered_text_color': Color('#FFF5FF'),
                'pressed_text_color': Color('#D2BFAC'),
                'normal_color': Color('#CC6600'),
                'hovered_color': Color('#CC6600'),
                'pressed_color': Color('#CC6600')
                },
            on_press_callback = self.cc.buy_grandma
        )
        
        self.lvl_grandma_multiplicator_upgrade_button = UIButton(
            Rect(WIDTH*.15,HEIGHT*.1,WIDTH*.15,HEIGHT*.1),
            ux={
                
                'text': f'Multiplicator: {self.cc.get_multiplicator_price("grandma")}',
                'size': (WIDTH*.15,HEIGHT*.1),
                'font':FONT(size=20),
                'border_radius':45,
                'normal_text_color': Color('#FFE5CC'),
                'hovered_text_color': Color('#FFF5FF'),
                'pressed_text_color': Color('#D2BFAC'),
                'normal_color': Color('#CC6600'),
                'hovered_color': Color('#CC6600'),
                'pressed_color': Color('#CC6600')
                },
            on_press_callback = self.cc.buy_grandma_multiplicator
        )
        
        self.lvl_farm_upgrade_button = UIButton(
            Rect(0,HEIGHT*.2,WIDTH*.15,HEIGHT*.1),
            ux={
                
                'text': f'Farm: {self.cc.get_price("farm")}',
                'size': (WIDTH*.15,HEIGHT*.1),
                'font':FONT(size=20),
                'border_radius':45,
                'normal_text_color': Color('#FFE5CC'),
                'hovered_text_color': Color('#FFF5FF'),
                'pressed_text_color': Color('#D2BFAC'),
                'normal_color': Color('#CC6600'),
                'hovered_color': Color('#CC6600'),
                'pressed_color': Color('#CC6600')
                },
            on_press_callback = self.cc.buy_farm
        )
        self.lvl_mine_upgrade_button = UIButton(
            Rect(0,HEIGHT*.3,WIDTH*.15,HEIGHT*.1),
            ux={
                
                'text': f'Mine: {self.cc.get_price("mine")}',
                'size': (WIDTH*.15,HEIGHT*.1),
                'font':FONT(size=20),
                'border_radius':45,
                'normal_text_color': Color('#FFE5CC'),
                'hovered_text_color': Color('#FFF5FF'),
                'pressed_text_color': Color('#D2BFAC'),
                'normal_color': Color('#CC6600'),
                'hovered_color': Color('#CC6600'),
                'pressed_color': Color('#CC6600')
                },
            on_press_callback = self.cc.buy_mine
        )
        self.lvl_factory_upgrade_button = UIButton(
            Rect(0,HEIGHT*.4,WIDTH*.15,HEIGHT*.1),
            ux={
                
                'text': f'Factory: {self.cc.get_price("factory")}',
                'size': (WIDTH*.15,HEIGHT*.1),
                'font':FONT(size=20),
                'border_radius':45,
                'normal_text_color': Color('#FFE5CC'),
                'hovered_text_color': Color('#FFF5FF'),
                'pressed_text_color': Color('#D2BFAC'),
                'normal_color': Color('#CC6600'),
                'hovered_color': Color('#CC6600'),
                'pressed_color': Color('#CC6600')
                },
            on_press_callback = self.cc.buy_factory
        )
        
        self.cookie_label = UILabel(
            Rect(QUARTER_WIDTH*1.5,0,QUARTER_WIDTH,HEIGHT*.1),
            ux = {
                'text': '0',
                'size': (QUARTER_WIDTH,HEIGHT*.1),
                'font': FONT(size=40),
                'background_color': Color('#CC6600'),
                'text_color': Color('#FFE5CC')
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
        music.load("data\\bin\\click.mp3")
        music.play()
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
                self.lvl_cursor_multiplicator_upgrade_button.UX.text = f'Multiplicator: {self.cc.get_multiplicator_price("cursor")}'
                self.lvl_cursor_multiplicator_upgrade_button.UX.draw()
            UIM.render_queue(self)
            self.animation.update()
            self.cc.update()
            self.update_cookie_label()
            self.update()
            GLOBAL_DELTA_TIME.after()

if __name__ == "__main__":
    APP = App()
    APP.run()