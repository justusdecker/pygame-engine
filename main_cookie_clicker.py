from data.modules.constants import *
from math import sin
from pygame import Rect,image, Color, Surface,SRCALPHA
from pygame.draw import line
from pygame.mouse import get_pos,set_visible,get_pressed
from pygame.transform import scale,flip
from data.modules.ui.ui_font import FONT,FONTDRAW
from random import randint

from data.modules.ui.ui_element import UIM

from data.modules.ui.ui_label import UILabel
from data.modules.ui.ui_button import UIButton

from data.modules.app import Application
from data.modules.animation import Animation
from data.modules.audio_handler import AudioHandler
BUTTON_COLORS = {'tcg':('#FFE5CC00',),'bcg':('#CC660000',)}

BUTTON_DEST = (HEIGHT*.1,HEIGHT*.1)

UPGRADE_BUTTON_UX = {'size': BUTTON_DEST, 'font':FONT(size=20), 'border_radius':45, **BUTTON_COLORS}

KEYFRAMES = [
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
                                   ]

UPGRADE_KEYFRAMES = [
    {
            "x_offset": 0,
            "y_offset": 0,
            "scale": [.4,.4]
        },
    {
            "x_offset": 0,
            "y_offset": 0,
            "scale": [.43,.4]
        },
    {
            "x_offset": 0,
            "y_offset": 0,
            "scale": [.47,.4]
        },
    {
            "x_offset": 0,
            "y_offset": 5,
            "scale": [.49,.4]
        },
    {
            "x_offset": 0,
            "y_offset": 0,
            "scale": [.47,.4]
        },
    {
            "x_offset": 0,
            "y_offset": 0,
            "scale": [.43,.4]
        }
]

def test_print(*args):
    print(args, "Hello World!")

def get_shortened_number(x:int) -> str:
    x = int(x)

    if x >= 1_000_000:
        return f'{x/1_000_000:.2f}M'
    elif x >= 1000:
        return f'{x/1000:.2f}K'
    else: return f'{x}'

class MilkWaves:
    def __init__(self,app):
        self.app = app
        
        self.shifter = 0
        self.updown_shifter = 0
        self.generate()
    def generate(self):
        self.b = [sin((i*.00025)+self.shifter) for i in range(WIDTH)]
        self.m = [abs(sin((i*.005)+self.shifter)) for i in range(WIDTH)]
        self.f = [abs(sin((i*.015)+self.shifter)) for i in range(WIDTH)]
    def update(self):
        self.shifter += GLOBAL_DELTA_TIME.get() * .25
        self.generate()
        surf = Surface((WIDTH,HEIGHT*2),SRCALPHA)
        for l,c in [(self.b,'#F2C9A0'),(self.m,'#F0D0B0'),(self.f,'#FFF3E6')]:
            for index,pos in enumerate(l):
                line(self.app.window.surface,Color(c),(index,HEIGHT),(index,(pos*HEIGHT*.1)+(HEIGHT*.9)))
        surf = flip(surf,False,True)
        self.app.window.render(surf,(0,HEIGHT*.6))

class CookieClicker:
    def __init__(self,app):
        self.app = app
        self.cookies = 10000000
        self.last_cookie = 0
        
        self.click_upgrades = 0
        
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
    def get_click_price(self):
        prices = [1000,10000,100000]
        if self.click_upgrades >= len(prices): return 'MAX'
        return prices[self.click_upgrades]
    def upgrade_click(self,button:UIButton):
        prices = [1000,10000,100000]
        if self.click_upgrades >= len(prices): return
        price = prices[self.click_upgrades]
        if self.get() >= price:
            self.cookies -= price
            self.click_upgrades += 1
            
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
            match button.element_name:
                case 'cursor':
                    self.app.lvl_cursor_multiplicator_upgrade_animation.start_animation()
                    self.app.lvl_cursor_multiplicator_upgrade_label.render(str(get_shortened_number(self.get_multiplicator_price('cursor'))))
                    self.app.lvl_cursor_multiplicator_cost_label.render(str(self.multiplicators['cursor']-1))
                case 'grandma':
                    self.app.lvl_grandma_multiplicator_upgrade_animation.start_animation()
                    self.app.lvl_grandma_multiplicator_upgrade_label.render(str(get_shortened_number(self.get_multiplicator_price('grandma'))))
                    self.app.lvl_grandma_multiplicator_cost_label.render(str(self.multiplicators['grandma']-1))
                case 'farm':
                    self.app.lvl_farm_multiplicator_upgrade_animation.start_animation()
                    self.app.lvl_farm_multiplicator_upgrade_label.render(str(get_shortened_number(self.get_multiplicator_price('farm'))))
                    self.app.lvl_farm_multiplicator_cost_label.render(str(self.multiplicators['farm']-1))
                case 'mine':
                    self.app.lvl_mine_multiplicator_upgrade_animation.start_animation()
                    self.app.lvl_mine_multiplicator_upgrade_label.render(str(get_shortened_number(self.get_multiplicator_price('mine'))))
                    self.app.lvl_mine_multiplicator_cost_label.render(str(self.multiplicators['mine']-1))
                case 'factory':
                    self.app.lvl_factory_multiplicator_upgrade_animation.start_animation()
                    self.app.lvl_factory_multiplicator_upgrade_label.render(str(get_shortened_number(self.get_multiplicator_price('factory'))))
                    self.app.lvl_factory_multiplicator_cost_label.render(str(self.multiplicators['factory']-1))
    def upgrade(self,button:UIButton):
        key = button.element_name
        price = self.get_price(key)
        if self.get() >= price:
            self.cookies -= price
            self.upgrades[key] += 1
            
            match button.element_name:
                case 'cursor':
                    self.app.lvl_cursor_upgrade_animation.start_animation()
                    self.app.lvl_cursor_upgrade_label.render(str(get_shortened_number(self.get_price('cursor'))))
                    self.app.lvl_cursor_cost_label.render(str(self.upgrades['cursor']))
                case 'grandma':
                    self.app.lvl_grandma_upgrade_animation.start_animation()
                    self.app.lvl_grandma_upgrade_label.render(str(get_shortened_number(self.get_price('grandma'))))
                    self.app.lvl_grandma_cost_label.render(str(self.upgrades['grandma']))
                case 'farm':
                    self.app.lvl_farm_upgrade_animation.start_animation()
                    self.app.lvl_farm_upgrade_label.render(str(get_shortened_number(self.get_price('farm'))))
                    self.app.lvl_farm_cost_label.render(str(self.upgrades['farm']))
                case 'mine':
                    self.app.lvl_mine_upgrade_animation.start_animation()
                    self.app.lvl_mine_upgrade_label.render(str(get_shortened_number(self.get_price('mine'))))
                    self.app.lvl_mine_cost_label.render(str(self.upgrades['mine']))
                case 'factory':
                    self.app.lvl_factory_upgrade_animation.start_animation()
                    self.app.lvl_factory_upgrade_label.render(str(get_shortened_number(self.get_price('factory'))))
                    self.app.lvl_factory_cost_label.render(str(self.upgrades['factory']))
    def get_click_strength(self) -> int:
        return (self.click_upgrades*2) if self.click_upgrades else 1
    def click(self):
        self.cookies += self.get_click_strength()
    def get(self):
        return int(self.cookies)

class CookieRain:
    def __init__(self,app):
        self.app = app
        self.cookie_image = scale(image.load('data\\bin\\img\\cookie.png'),(HEIGHT*.05,HEIGHT*.05))
        self.objects = [ [randint(0,int(WIDTH*.95)),randint(-int(HEIGHT*1.05),int(HEIGHT*.95))] for i in range(100) ]
    def create(self,):
        return [randint(0,int(WIDTH*.95)),-randint(int(HEIGHT*1.05),int(HEIGHT*1.15))] # randint(int(HEIGHT*1.05),int(HEIGHT*1.1))
    def update(self):
        for object in self.objects:
            object[1] += GLOBAL_DELTA_TIME.get()*50
            self.app.window.render(self.cookie_image,object)
        self.objects = [i if i[1] < HEIGHT else self.create() for i in self.objects]
class FloatingText:
    def __init__(self,app):

        self.app = app
        self.objects = []
    def add_object(self,):
        self.objects.append([list(get_pos()),HEIGHT*.05])
    def update(self):
        for object in self.objects:
            object[1] -= GLOBAL_DELTA_TIME.get() * 30
            object[0][1] -= GLOBAL_DELTA_TIME.get() * 50
            if object[1] <= 1: continue
            self.app.window.render(FONTDRAW.draw(str(self.app.cc.get_click_strength()),size=int(object[1]),color=Color('#FFE5CC')),object[0])
        self.objects = [i for i in self.objects if i[1] > 0]

class App(Application):
    def __init__(self):
        super().__init__()
        set_visible(False)
        self.star_image = image.load('data\\bin\\img\\star.png')
        
        self.mouse_image_normal = scale(image.load('data\\bin\\img\\mouse.png'),(32,32))
        self.mouse_image_hover = scale(image.load('data\\bin\\img\\mouse_hovered.png'),(32,32))
        self.mouse_image_pressed = scale(image.load('data\\bin\\img\\mouse_pressed.png'),(32,32))
        
        self.audio_handler = AudioHandler(sfx_lib={'click': "data\\bin\\click.mp3"})
        
        self.mw = MilkWaves(self)
        self.cc = CookieClicker(self)
        self.cr = CookieRain(self)
        self.ft = FloatingText(self)
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
        
        self.lvl_cursor_upgrade_button = UIButton( Rect(0,0,*BUTTON_DEST), ux={**UPGRADE_BUTTON_UX }, on_press_callback = self.cc.upgrade,element_name = 'cursor')
        
        self.lvl_cursor_multiplicator_upgrade_button = UIButton( Rect(BUTTON_DEST[0],0,*BUTTON_DEST), ux={**UPGRADE_BUTTON_UX}, on_press_callback = self.cc.upgrade_multiplicator,element_name = 'cursor')
        
        self.lvl_grandma_upgrade_button = UIButton( Rect(0,HEIGHT*.1,*BUTTON_DEST), ux={**UPGRADE_BUTTON_UX},on_press_callback = self.cc.upgrade,element_name = 'grandma')
        
        self.lvl_grandma_multiplicator_upgrade_button = UIButton( Rect(BUTTON_DEST[0],HEIGHT*.1,*BUTTON_DEST),ux={**UPGRADE_BUTTON_UX},on_press_callback = self.cc.upgrade_multiplicator,element_name = 'grandma')
        
        self.lvl_farm_upgrade_button = UIButton( Rect(0,HEIGHT*.2,*BUTTON_DEST),ux={**UPGRADE_BUTTON_UX},on_press_callback = self.cc.upgrade,element_name = 'farm')
        
        self.lvl_farm_multiplicator_upgrade_button = UIButton( Rect(BUTTON_DEST[0],HEIGHT*.2,*BUTTON_DEST),ux={**UPGRADE_BUTTON_UX},on_press_callback = self.cc.upgrade_multiplicator,element_name = 'farm')
        
        self.lvl_mine_upgrade_button = UIButton( Rect(0,HEIGHT*.3,*BUTTON_DEST),ux={**UPGRADE_BUTTON_UX},on_press_callback = self.cc.upgrade,element_name = 'mine')
        
        self.lvl_mine_multiplicator_upgrade_button = UIButton(Rect(BUTTON_DEST[0],HEIGHT*.3,*BUTTON_DEST),ux={**UPGRADE_BUTTON_UX},on_press_callback = self.cc.upgrade_multiplicator,element_name = 'mine')
        
        self.lvl_factory_upgrade_button = UIButton( Rect(0,HEIGHT*.4,*BUTTON_DEST),ux={**UPGRADE_BUTTON_UX},on_press_callback = self.cc.upgrade,element_name = 'factory')
        
        self.lvl_factory_multiplicator_upgrade_button = UIButton( Rect(BUTTON_DEST[0],HEIGHT*.4,*BUTTON_DEST),ux={**UPGRADE_BUTTON_UX},on_press_callback = self.cc.upgrade_multiplicator,element_name = 'factory')
        
        self.lvl_click_upgrade_button = UIButton( Rect(BUTTON_DEST[0],HEIGHT*.5,*BUTTON_DEST),ux={**UPGRADE_BUTTON_UX},on_press_callback = self.cc.upgrade_click,element_name = 'click')
        
        #! for each upgrade button:
        #   - add a price label
        #   - add a inventory view label
        
        #? Level ammount Label
        
        self.lvl_cursor_cost_label = UILabel(
            Rect(BUTTON_DEST[0]//2,0,BUTTON_DEST[0]//2,HEIGHT*.025),
            ux = {
                'text': str(self.cc.upgrades['cursor']),
                'size': (BUTTON_DEST[0]//2,HEIGHT*.025),
                'font': FONT(size=15),
                'bcg': ('#CC660000',),
                'tcg': ('#FFE5CC',)
            }
        )
        
        self.lvl_grandma_cost_label = UILabel(
            Rect(BUTTON_DEST[0]//2,HEIGHT*.1,BUTTON_DEST[0]//2,HEIGHT*.025),
            ux = {
                'text': str(self.cc.upgrades['grandma']),
                'size': (BUTTON_DEST[0]//2,HEIGHT*.025),
                'font': FONT(size=15),
                'bcg': ('#CC660000',),
                'tcg': ('#FFE5CC',)
            }
        )
        
        self.lvl_farm_cost_label = UILabel(
            Rect(BUTTON_DEST[0]//2,HEIGHT*.2,BUTTON_DEST[0]//2,HEIGHT*.025),
            ux = {
                'text': str(self.cc.upgrades['farm']),
                'size': (BUTTON_DEST[0]//2,HEIGHT*.025),
                'font': FONT(size=15),
                'bcg': ('#CC660000',),
                'tcg': ('#FFE5CC',)
            }
        )
        
        self.lvl_mine_cost_label = UILabel(
            Rect(BUTTON_DEST[0]//2,HEIGHT*.3,BUTTON_DEST[0]//2,HEIGHT*.025),
            ux = {
                'text': str(self.cc.upgrades['mine']),
                'size': (BUTTON_DEST[0]//2,HEIGHT*.025),
                'font': FONT(size=15),
                'bcg': ('#CC660000',),
                'tcg': ('#FFE5CC',)
            }
        )
        
        self.lvl_factory_cost_label = UILabel(
            Rect(BUTTON_DEST[0]//2,HEIGHT*.4,BUTTON_DEST[0]//2,HEIGHT*.025),
            ux = {
                'text': str(self.cc.upgrades['factory']),
                'size': (BUTTON_DEST[0]//2,HEIGHT*.025),
                'font': FONT(size=15),
                'bcg': ('#CC660000',),
                'tcg': ('#FFE5CC',)
            }
        )
        
        self.lvl_cursor_multiplicator_cost_label = UILabel(
            Rect((BUTTON_DEST[0]//2)+BUTTON_DEST[0],0,BUTTON_DEST[0]//2,HEIGHT*.025),
            ux = {
                'text': str(self.cc.upgrades['cursor']),
                'size': (BUTTON_DEST[0]//2,HEIGHT*.025),
                'font': FONT(size=15),
                'bcg': ('#CC660000',),
                'tcg': ('#FFE5CC',)
            }
        )
        
        self.lvl_grandma_multiplicator_cost_label = UILabel(
            Rect((BUTTON_DEST[0]//2)+BUTTON_DEST[0],HEIGHT*.1,BUTTON_DEST[0]//2,HEIGHT*.025),
            ux = {
                'text': str(self.cc.upgrades['grandma']),
                'size': (BUTTON_DEST[0]//2,HEIGHT*.025),
                'font': FONT(size=15),
                'bcg': ('#CC660000',),
                'tcg': ('#FFE5CC',)
            }
        )
        
        self.lvl_farm_multiplicator_cost_label = UILabel(
            Rect((BUTTON_DEST[0]//2)+BUTTON_DEST[0],HEIGHT*.2,BUTTON_DEST[0]//2,HEIGHT*.025),
            ux = {
                'text': str(self.cc.upgrades['farm']),
                'size': (BUTTON_DEST[0]//2,HEIGHT*.025),
                'font': FONT(size=15),
                'bcg': ('#CC660000',),
                'tcg': ('#FFE5CC',)
            }
        )
        
        self.lvl_mine_multiplicator_cost_label = UILabel(
            Rect((BUTTON_DEST[0]//2)+BUTTON_DEST[0],HEIGHT*.3,BUTTON_DEST[0]//2,HEIGHT*.025),
            ux = {
                'text': str(self.cc.upgrades['mine']),
                'size': (BUTTON_DEST[0]//2,HEIGHT*.025),
                'font': FONT(size=15),
                'bcg': ('#CC660000',),
                'tcg': ('#FFE5CC',)
            }
        )
        
        self.lvl_factory_multiplicator_cost_label = UILabel(
            Rect((BUTTON_DEST[0]//2)+BUTTON_DEST[0],HEIGHT*.4,BUTTON_DEST[0]//2,HEIGHT*.025),
            ux = {
                'text': str(self.cc.upgrades['factory']),
                'size': (BUTTON_DEST[0]//2,HEIGHT*.025),
                'font': FONT(size=15),
                'bcg': ('#CC660000',),
                'tcg': ('#FFE5CC',)
            }
        )
        
        #? Level Up & Multiplicator Label
        
        self.lvl_cursor_upgrade_label = UILabel(
            Rect(0,BUTTON_DEST[1]-(HEIGHT*.025),QUARTER_WIDTH,HEIGHT*.025),
            ux = {
                'text': str(get_shortened_number(self.cc.get_price('cursor'))),
                'size': (BUTTON_DEST[0],HEIGHT*.025),
                'font': FONT(size=13),
                'bcg': ('#CC6600AA',),
                'tcg': ('#FFE5CC',)
            }
        )
        
        self.lvl_grandma_upgrade_label = UILabel(
            Rect(0,(BUTTON_DEST[1]*2)-(HEIGHT*.025),QUARTER_WIDTH,HEIGHT*.025),
            ux = {
                'text': str(get_shortened_number(self.cc.get_price('grandma'))),
                'size': (BUTTON_DEST[0],HEIGHT*.025),
                'font': FONT(size=13),
                'bcg': ('#CC6600AA',),
                'tcg': ('#FFE5CC',)
            }
        )
        
        self.lvl_farm_upgrade_label = UILabel(
            Rect(0,(BUTTON_DEST[1]*3)-(HEIGHT*.025),QUARTER_WIDTH,HEIGHT*.025),
            ux = {
                'text': str(get_shortened_number(self.cc.get_price('farm'))),
                'size': (BUTTON_DEST[0],HEIGHT*.025),
                'font': FONT(size=13),
                'bcg': ('#CC6600AA',),
                'tcg': ('#FFE5CC',)
            }
        )
        
        self.lvl_mine_upgrade_label = UILabel(
            Rect(0,(BUTTON_DEST[1]*4)-(HEIGHT*.025),QUARTER_WIDTH,HEIGHT*.025),
            ux = {
                'text': str(get_shortened_number(self.cc.get_price('mine'))),
                'size': (BUTTON_DEST[0],HEIGHT*.025),
                'font': FONT(size=13),
                'bcg': ('#CC6600AA',),
                'tcg': ('#FFE5CC',)
            }
        )
        
        self.lvl_factory_upgrade_label = UILabel(
            Rect(0,(BUTTON_DEST[1]*5)-(HEIGHT*.025),QUARTER_WIDTH,HEIGHT*.025),
            ux = {
                'text': str(get_shortened_number(self.cc.get_price('factory'))),
                'size': (BUTTON_DEST[0],HEIGHT*.025),
                'font': FONT(size=13),
                'bcg': ('#CC6600AA',),
                'tcg': ('#FFE5CC',)
            }
        )
        
        
        self.lvl_cursor_multiplicator_upgrade_label = UILabel(
            Rect(BUTTON_DEST[0],BUTTON_DEST[1]-(HEIGHT*.025),QUARTER_WIDTH,HEIGHT*.025),
            ux = {
                'text': str(get_shortened_number(self.cc.get_multiplicator_price('cursor'))),
                'size': (BUTTON_DEST[0],HEIGHT*.025),
                'font': FONT(size=13),
                'bcg': ('#CC6600AA',),
                'tcg': ('#FFE5CC',)
            }
        )
        
        self.lvl_grandma_multiplicator_upgrade_label = UILabel(
            Rect(BUTTON_DEST[0],(BUTTON_DEST[1]*2)-(HEIGHT*.025),QUARTER_WIDTH,HEIGHT*.025),
            ux = {
                'text': str(get_shortened_number(self.cc.get_multiplicator_price('grandma'))),
                'size': (BUTTON_DEST[0],HEIGHT*.025),
                'font': FONT(size=13),
                'bcg': ('#CC6600AA',),
                'tcg': ('#FFE5CC',)
            }
        )
        
        self.lvl_farm_multiplicator_upgrade_label = UILabel(
            Rect(BUTTON_DEST[0],(BUTTON_DEST[1]*3)-(HEIGHT*.025),QUARTER_WIDTH,HEIGHT*.025),
            ux = {
                'text': str(get_shortened_number(self.cc.get_multiplicator_price('farm'))),
                'size': (BUTTON_DEST[0],HEIGHT*.025),
                'font': FONT(size=13),
                'bcg': ('#CC6600AA',),
                'tcg': ('#FFE5CC',)
            }
        )
        
        self.lvl_mine_multiplicator_upgrade_label = UILabel(
            Rect(BUTTON_DEST[0],(BUTTON_DEST[1]*4)-(HEIGHT*.025),QUARTER_WIDTH,HEIGHT*.025),
            ux = {
                'text': str(get_shortened_number(self.cc.get_multiplicator_price('mine'))),
                'size': (BUTTON_DEST[0],HEIGHT*.025),
                'font': FONT(size=13),
                'bcg': ('#CC6600AA',),
                'tcg': ('#FFE5CC',)
            }
        )
        
        self.lvl_factory_multiplicator_upgrade_label = UILabel(
            Rect(BUTTON_DEST[0],(BUTTON_DEST[1]*5)-(HEIGHT*.025),QUARTER_WIDTH,HEIGHT*.025),
            ux = {
                'text': str(get_shortened_number(self.cc.get_multiplicator_price('factory'))),
                'size': (BUTTON_DEST[0],HEIGHT*.025),
                'font': FONT(size=13),
                'bcg': ('#CC6600AA',),
                'tcg': ('#FFE5CC',)
            }
        )
        
        #? Level Up & Multiplicator Animations
        
        self.lvl_click_upgrade_animation = Animation(self,
                                   self.star_image,
                                   UPGRADE_KEYFRAMES,(self.lvl_click_upgrade_button.pos[0]+(self.lvl_click_upgrade_button.dest[0]//2),self.lvl_click_upgrade_button.pos[1]+(self.lvl_click_upgrade_button.dest[1]//2)),time_multiplier=50)
        
        self.lvl_cursor_multiplicator_upgrade_animation = Animation(self,
                                   self.star_image,
                                   UPGRADE_KEYFRAMES,(self.lvl_cursor_multiplicator_upgrade_button.pos[0]+(self.lvl_cursor_upgrade_button.dest[0]//2),self.lvl_cursor_upgrade_button.pos[1]+(self.lvl_cursor_upgrade_button.dest[1]//2)),time_multiplier=50)
        
        self.lvl_grandma_multiplicator_upgrade_animation = Animation(self,
                                   self.star_image,
                                   UPGRADE_KEYFRAMES,(self.lvl_grandma_multiplicator_upgrade_button.pos[0]+(self.lvl_grandma_multiplicator_upgrade_button.dest[0]//2),self.lvl_grandma_multiplicator_upgrade_button.pos[1]+(self.lvl_grandma_multiplicator_upgrade_button.dest[1]//2)),time_multiplier=50)
        
        self.lvl_farm_multiplicator_upgrade_animation = Animation(self,
                                   self.star_image,
                                   UPGRADE_KEYFRAMES,(self.lvl_farm_multiplicator_upgrade_button.pos[0]+(self.lvl_farm_multiplicator_upgrade_button.dest[0]//2),self.lvl_farm_multiplicator_upgrade_button.pos[1]+(self.lvl_farm_multiplicator_upgrade_button.dest[1]//2)),time_multiplier=50)
        
        self.lvl_mine_multiplicator_upgrade_animation = Animation(self,
                                   self.star_image,
                                   UPGRADE_KEYFRAMES,(self.lvl_mine_multiplicator_upgrade_button.pos[0]+(self.lvl_mine_multiplicator_upgrade_button.dest[0]//2),self.lvl_mine_multiplicator_upgrade_button.pos[1]+(self.lvl_mine_multiplicator_upgrade_button.dest[1]//2)),time_multiplier=50)
        
        self.lvl_factory_multiplicator_upgrade_animation = Animation(self,
                                   self.star_image,
                                   UPGRADE_KEYFRAMES,(self.lvl_factory_multiplicator_upgrade_button.pos[0]+(self.lvl_factory_multiplicator_upgrade_button.dest[0]//2),self.lvl_factory_multiplicator_upgrade_button.pos[1]+(self.lvl_factory_multiplicator_upgrade_button.dest[1]//2)),time_multiplier=50)
        
        
        

        self.lvl_cursor_upgrade_animation = Animation(self,
                                   image.load("data\\bin\\img\\cursor.png"),
                                   UPGRADE_KEYFRAMES,(self.lvl_cursor_upgrade_button.pos[0]+(self.lvl_cursor_upgrade_button.dest[0]//2),self.lvl_cursor_upgrade_button.pos[1]+(self.lvl_cursor_upgrade_button.dest[1]//2)),time_multiplier=50)
        
        self.lvl_grandma_upgrade_animation = Animation(self,
                                   image.load("data\\bin\\img\\grandma.png"),
                                   UPGRADE_KEYFRAMES,(self.lvl_grandma_upgrade_button.pos[0]+(self.lvl_grandma_upgrade_button.dest[0]//2),self.lvl_grandma_upgrade_button.pos[1]+(self.lvl_grandma_upgrade_button.dest[1]//2)),time_multiplier=50)
        
        self.lvl_farm_upgrade_animation = Animation(self,
                                   image.load("data\\bin\\img\\farm.png"),
                                   UPGRADE_KEYFRAMES,(self.lvl_farm_upgrade_button.pos[0]+(self.lvl_farm_upgrade_button.dest[0]//2),self.lvl_farm_upgrade_button.pos[1]+(self.lvl_farm_upgrade_button.dest[1]//2)),time_multiplier=50)
        
        self.lvl_mine_upgrade_animation = Animation(self,
                                   image.load("data\\bin\\img\\mine.png"),
                                   UPGRADE_KEYFRAMES,(self.lvl_mine_upgrade_button.pos[0]+(self.lvl_mine_upgrade_button.dest[0]//2),self.lvl_mine_upgrade_button.pos[1]+(self.lvl_mine_upgrade_button.dest[1]//2)),time_multiplier=50)
        
        self.lvl_factory_upgrade_animation = Animation(self,
                                   image.load("data\\bin\\img\\factory.png"),
                                   UPGRADE_KEYFRAMES,(self.lvl_factory_upgrade_button.pos[0]+(self.lvl_factory_upgrade_button.dest[0]//2),self.lvl_factory_upgrade_button.pos[1]+(self.lvl_factory_upgrade_button.dest[1]//2)),time_multiplier=50)
        
        self.animation = Animation(self,
                                   image.load("data\\bin\\img\\cookie.png"),
                                   KEYFRAMES,
                                   (HALF_WIDTH,HALF_HEIGHT),time_multiplier=50)
        
        self.cookie_label = UILabel(
            Rect(QUARTER_WIDTH*1.5,0,QUARTER_WIDTH,HEIGHT*.1),
            ux = {
                'text': '0',
                'size': (QUARTER_WIDTH,HEIGHT*.1),
                'font': FONT(size=40),
                'bcg': ('#CC660000',),
                'tcg': ('#FFE5CC',)
            }
        )
        
        self.info_label = UILabel(
            Rect(WIDTH*.8,HEIGHT*-.1,WIDTH*.2,HEIGHT*.3),
            ux = {
                'text': '(c) 2025 Justus Decker\n0.0.36 pygame-engine-project',
                'size': (QUARTER_WIDTH,HEIGHT*.3),
                'font': FONT(size=10),
                'bcg': ('#CC660000',),
                'tcg': ('#FFE5CC',)
            }
        )
    def update_cookie_label(self):
        self.cookie_label.UX.text = f"{get_shortened_number(self.cc.get())}" + (f"+{self.cc.get_auto_clicker():.1f}" if self.cc.get_auto_clicker() else '')
        self.cookie_label.set_image(self.cookie_label.UX.gen())
            
    def on_cookie_click(self,*_):
        self.audio_handler.play_sound('click')
        self.animation.start_animation()
        self.cc.click()
        self.ft.add_object()
        
    def run(self):
        
        while self.is_running:
            GLOBAL_DELTA_TIME.before()
            self.CLK.tick(60)
            self.window.surface.fill(Color('#FFB266'))
            self.cr.update()
            self.mw.update()
            
            self.animation.update()
            
            self.lvl_click_upgrade_animation.update()
            
            self.lvl_cursor_upgrade_animation.update()
            self.lvl_grandma_upgrade_animation.update()
            self.lvl_farm_upgrade_animation.update()
            self.lvl_mine_upgrade_animation.update()
            self.lvl_factory_upgrade_animation.update()
            
            self.lvl_cursor_multiplicator_upgrade_animation.update()
            self.lvl_grandma_multiplicator_upgrade_animation.update()
            self.lvl_farm_multiplicator_upgrade_animation.update()
            self.lvl_mine_multiplicator_upgrade_animation.update()
            self.lvl_factory_multiplicator_upgrade_animation.update()
            
            UIM.render_queue(self)
            
            self.cc.update()
            self.update_cookie_label()
            self.ft.update()
            if get_pressed()[0]:
                self.window.render(self.mouse_image_pressed ,get_pos())
            elif any([any([obj.is_hovered for obj in UIM.queue[layer]]) for layer in UIM.queue]):
                self.window.render(self.mouse_image_hover ,get_pos())
            else:
                self.window.render(self.mouse_image_normal ,get_pos())

            self.update()
            GLOBAL_DELTA_TIME.after()

if __name__ == "__main__":
    APP = App()
    APP.run()