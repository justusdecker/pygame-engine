from math import sin
from pygame import Rect,image, Color, Surface,SRCALPHA
from pygame.display import set_icon
from pygame.draw import line
from pygame.mouse import get_pos,set_visible,get_pressed
from pygame.transform import scale,flip
from random import randint
from data.modules.kernel.log import LOG
LOG.tobash = False
from data.modules.constants import *
from data.modules.ui.ui_font import FONT,FONTDRAW
from data.modules.ui.ui_element import UIM
from data.modules.ui.ui_label import UILabel
from data.modules.ui.ui_button import UIButton
from data.modules.kernel.app import Application
from data.modules.animation import Animation
from data.modules.audio_handler import AudioHandler
set_icon(image.load(f'{IMAGE_PATH}cookie_clicker_logo.ico'))


"""
Documentation
******
Globals
-----
.. TRANSPARENT:: background color
.. BUTTON_COLORS:: default transparent
.. BUTTON_DEST:: default button size
.. UPGRADE_BUTTON_UX:: defines the default UXElement to save memory & organize the code
.. KEYFRAMES:: the cookie animation keyframes
.. UPGRADE_KEYFRAMES:: the upgrade animation keyframes used for all upgrades
.. LABEL_IVENTORY_UX:: defines a default UXElement to save memory & organize the code
.. LABEL_COST_UX:: defines a default UXElement to save memory & organize the code
"""

TRANSPARENT = ((0,0,0,0),)
BUTTON_COLORS = {'tcg':TRANSPARENT,'bcg':TRANSPARENT}

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

LABEL_INVENTORY_UX = {
    'size': (BUTTON_DEST[0]//2,HEIGHT*.025),
    'font': FONT(size=15),
    'bcg': TRANSPARENT,
    'tcg': ('#FFE5CC',)
}

LABEL_COST_UX = {
    'size': (BUTTON_DEST[0],HEIGHT*.025),
    'font': FONT(size=13),
    'bcg': ('#CC6600AA',),
    'tcg': ('#FFE5CC',)
}

def get_num_short(x:int) -> str:
    if not str(x).isdecimal(): return 'MAX'
    x = int(x)

    if x >= 1_000_000:
        return f'{x/1_000_000:.2f}M'
    elif x >= 1000:
        return f'{x/1000:.2f}K'
    else: return f'{x}'

class MilkWaves:
    """
    .. step_1:: Generate 3 different Waves
    .. step_2:: Draw the waves one the screen
    .. step_3:: shift each frame a bit to the left
    """
    def __init__(self,app):
        self.app = app
        
        self.shifter = 0
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
        self.cookies = 0
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
            self.app.lbl_mul_cost_cursor.render(str(get_num_short(self.get_click_price())))
            self.app.lbl_mul_inv_click.render(str(self.click_upgrades))
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
                    self.app.animation_mul_cursor.start_animation()
                    self.app.lbl_mul_cost_cursor.render(str(get_num_short(self.get_multiplicator_price('cursor'))))
                    self.app.lbl_mul_inv_cursor.render(str(self.multiplicators['cursor']-1))
                case 'grandma':
                    self.app.animation_mul_grandma.start_animation()
                    self.app.lbl_mul_cost_grandma.render(str(get_num_short(self.get_multiplicator_price('grandma'))))
                    self.app.lbl_mul_inv_grandma.render(str(self.multiplicators['grandma']-1))
                case 'farm':
                    self.app.animation_mul_farm.start_animation()
                    self.app.lbl_mul_cost_farm.render(str(get_num_short(self.get_multiplicator_price('farm'))))
                    self.app.lbl_mul_inv_farm.render(str(self.multiplicators['farm']-1))
                case 'mine':
                    self.app.animation_mul_mine.start_animation()
                    self.app.lbl_mul_cost_mine.render(str(get_num_short(self.get_multiplicator_price('mine'))))
                    self.app.lbl_mul_inv_mine.render(str(self.multiplicators['mine']-1))
                case 'factory':
                    self.app.animation_mul_factory.start_animation()
                    self.app.lbl_mul_cost_factory.render(str(get_num_short(self.get_multiplicator_price('factory'))))
                    self.app.lbl_mul_inv_factory.render(str(self.multiplicators['factory']-1))
    def upgrade(self,button:UIButton):
        key = button.element_name
        price = self.get_price(key)
        if self.get() >= price:
            self.cookies -= price
            self.upgrades[key] += 1
            
            match button.element_name:
                case 'cursor':
                    self.app.animation_cursor.start_animation()
                    self.app.lbl_cost_cursor.render(str(get_num_short(self.get_price('cursor'))))
                    self.app.lbl_inv_cursor.render(str(self.upgrades['cursor']))
                case 'grandma':
                    self.app.animation_grandma.start_animation()
                    self.app.lbl_cost_grandma.render(str(get_num_short(self.get_price('grandma'))))
                    self.app.lbl_inv_grandma.render(str(self.upgrades['grandma']))
                case 'farm':
                    self.app.animation_farm.start_animation()
                    self.app.lbl_cost_farm.render(str(get_num_short(self.get_price('farm'))))
                    self.app.lbl_inv_farm.render(str(self.upgrades['farm']))
                case 'mine':
                    self.app.animation_mine.start_animation()
                    self.app.lbl_cost_mine.render(str(get_num_short(self.get_price('mine'))))
                    self.app.lbl_inv_mine.render(str(self.upgrades['mine']))
                case 'factory':
                    self.app.animation_factory.start_animation()
                    self.app.lbl_cost_factory.render(str(get_num_short(self.get_price('factory'))))
                    self.app.lbl_inv_factory.render(str(self.upgrades['factory']))
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
        "Create a new cookie"
        return [randint(0,int(WIDTH*.95)),-randint(int(HEIGHT*1.05),int(HEIGHT*1.15))] # randint(int(HEIGHT*1.05),int(HEIGHT*1.1))
    def update(self):
        """
        Raining cookies are simple
        Move each cookie
        If cookie is lower than the screen height then delete the current & create a new one
        Render the cookie
        """
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
        """
        Each number flows a bit higher & gets smaller each frame
        """
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
        self.star_image = image.load(f'{IMAGE_PATH}star.png')
        
        self.mouse_image_normal = scale(image.load(f'{IMAGE_PATH}mouse.png'),(32,32))
        self.mouse_image_hover = scale(image.load(f'{IMAGE_PATH}mouse_hovered.png'),(32,32))
        self.mouse_image_pressed = scale(image.load(f'{IMAGE_PATH}mouse_pressed.png'),(32,32))
        
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
                'bcg': TRANSPARENT
                },
            on_press_callback = self.on_cookie_click
        )
        
        #? Level Up & Multiplicator Buttons
        #{UIElement}_upgrade_{element_name}
        self.btn_upgrade_cursor = UIButton( Rect(0,0,*BUTTON_DEST), ux={**UPGRADE_BUTTON_UX }, on_press_callback = self.cc.upgrade,element_name = 'cursor')
        
        self.btn_mul_upgrade_cursor = UIButton( Rect(BUTTON_DEST[0],0,*BUTTON_DEST), ux={**UPGRADE_BUTTON_UX}, on_press_callback = self.cc.upgrade_multiplicator,element_name = 'cursor')
        
        self.btn_upgrade_grandma = UIButton( Rect(0,HEIGHT*.1,*BUTTON_DEST), ux={**UPGRADE_BUTTON_UX},on_press_callback = self.cc.upgrade,element_name = 'grandma')
        
        self.btn_mul_upgrade_grandma = UIButton( Rect(BUTTON_DEST[0],HEIGHT*.1,*BUTTON_DEST),ux={**UPGRADE_BUTTON_UX},on_press_callback = self.cc.upgrade_multiplicator,element_name = 'grandma')
        
        self.btn_upgrade_farm = UIButton( Rect(0,HEIGHT*.2,*BUTTON_DEST),ux={**UPGRADE_BUTTON_UX},on_press_callback = self.cc.upgrade,element_name = 'farm')
        
        self.btn_mul_upgrade_farm = UIButton( Rect(BUTTON_DEST[0],HEIGHT*.2,*BUTTON_DEST),ux={**UPGRADE_BUTTON_UX},on_press_callback = self.cc.upgrade_multiplicator,element_name = 'farm')
        
        self.btn_upgrade_mine = UIButton( Rect(0,HEIGHT*.3,*BUTTON_DEST),ux={**UPGRADE_BUTTON_UX},on_press_callback = self.cc.upgrade,element_name = 'mine')
        
        self.btn_mul_upgrade_mine = UIButton(Rect(BUTTON_DEST[0],HEIGHT*.3,*BUTTON_DEST),ux={**UPGRADE_BUTTON_UX},on_press_callback = self.cc.upgrade_multiplicator,element_name = 'mine')
        
        self.btn_upgrade_factory = UIButton( Rect(0,HEIGHT*.4,*BUTTON_DEST),ux={**UPGRADE_BUTTON_UX},on_press_callback = self.cc.upgrade,element_name = 'factory')
        
        self.btn_mul_upgrade_factory = UIButton( Rect(BUTTON_DEST[0],HEIGHT*.4,*BUTTON_DEST),ux={**UPGRADE_BUTTON_UX},on_press_callback = self.cc.upgrade_multiplicator,element_name = 'factory')
        
        self.btn_upgrade_click = UIButton( Rect(BUTTON_DEST[0],HEIGHT*.5,*BUTTON_DEST),ux={**UPGRADE_BUTTON_UX},on_press_callback = self.cc.upgrade_click,element_name = 'click')
        
        #? Level ammount Label
        
        self.lbl_inv_cursor = UILabel( Rect(BUTTON_DEST[0]//2,0,BUTTON_DEST[0]//2,HEIGHT*.025),ux = {'text': str(self.cc.upgrades['cursor']),**LABEL_INVENTORY_UX})
        
        self.lbl_inv_grandma = UILabel( Rect(BUTTON_DEST[0]//2,HEIGHT*.1,BUTTON_DEST[0]//2,HEIGHT*.025),ux = {'text': str(self.cc.upgrades['grandma']),**LABEL_INVENTORY_UX})
        
        self.lbl_inv_farm = UILabel( Rect(BUTTON_DEST[0]//2,HEIGHT*.2,BUTTON_DEST[0]//2,HEIGHT*.025),ux = {'text': str(self.cc.upgrades['farm']),**LABEL_INVENTORY_UX})
        
        self.lbl_inv_mine = UILabel( Rect(BUTTON_DEST[0]//2,HEIGHT*.3,BUTTON_DEST[0]//2,HEIGHT*.025),ux = {'text': str(self.cc.upgrades['mine']),**LABEL_INVENTORY_UX})
        
        self.lbl_inv_factory = UILabel( Rect(BUTTON_DEST[0]//2,HEIGHT*.4,BUTTON_DEST[0]//2,HEIGHT*.025),ux = {'text': str(self.cc.upgrades['factory']),**LABEL_INVENTORY_UX})
        
        self.lbl_mul_inv_cursor = UILabel( Rect((BUTTON_DEST[0]//2)+BUTTON_DEST[0],0,BUTTON_DEST[0]//2,HEIGHT*.025),ux = {'text': str(self.cc.upgrades['cursor']),**LABEL_INVENTORY_UX})
        
        self.lbl_mul_inv_grandma = UILabel( Rect((BUTTON_DEST[0]//2)+BUTTON_DEST[0],HEIGHT*.1,BUTTON_DEST[0]//2,HEIGHT*.025),ux = {'text': str(self.cc.upgrades['grandma']),**LABEL_INVENTORY_UX})
        
        self.lbl_mul_inv_farm = UILabel( Rect((BUTTON_DEST[0]//2)+BUTTON_DEST[0],HEIGHT*.2,BUTTON_DEST[0]//2,HEIGHT*.025),ux = {'text': str(self.cc.upgrades['farm']),**LABEL_INVENTORY_UX})
        
        self.lbl_mul_inv_mine = UILabel( Rect((BUTTON_DEST[0]//2)+BUTTON_DEST[0],HEIGHT*.3,BUTTON_DEST[0]//2,HEIGHT*.025),ux = {'text': str(self.cc.upgrades['mine']),**LABEL_INVENTORY_UX})
        
        self.lbl_mul_inv_factory = UILabel( Rect((BUTTON_DEST[0]//2)+BUTTON_DEST[0],HEIGHT*.4,BUTTON_DEST[0]//2,HEIGHT*.025),ux = {'text': str(self.cc.upgrades['factory']),**LABEL_INVENTORY_UX})
        
        self.lbl_mul_inv_click = UILabel( Rect((BUTTON_DEST[0]//2)+BUTTON_DEST[0],HEIGHT*.5,BUTTON_DEST[0]//2,HEIGHT*.025),ux = {'text': str(0),**LABEL_INVENTORY_UX})
        
        #? Level Up & Multiplicator Label
        
        self.lbl_cost_cursor = UILabel( Rect(0,BUTTON_DEST[1]-(HEIGHT*.025),QUARTER_WIDTH,HEIGHT*.025),ux = {'text': str(get_num_short(self.cc.get_price('cursor'))),**LABEL_COST_UX})
        
        self.lbl_cost_grandma = UILabel( Rect(0,(BUTTON_DEST[1]*2)-(HEIGHT*.025),QUARTER_WIDTH,HEIGHT*.025),ux = {'text': str(get_num_short(self.cc.get_price('grandma'))),**LABEL_COST_UX})
        
        self.lbl_cost_farm = UILabel( Rect(0,(BUTTON_DEST[1]*3)-(HEIGHT*.025),QUARTER_WIDTH,HEIGHT*.025),ux = {'text': str(get_num_short(self.cc.get_price('farm'))),**LABEL_COST_UX})
        
        self.lbl_cost_mine = UILabel( Rect(0,(BUTTON_DEST[1]*4)-(HEIGHT*.025),QUARTER_WIDTH,HEIGHT*.025),ux = {'text': str(get_num_short(self.cc.get_price('mine'))),**LABEL_COST_UX})
        
        self.lbl_cost_factory = UILabel( Rect(0,(BUTTON_DEST[1]*5)-(HEIGHT*.025),QUARTER_WIDTH,HEIGHT*.025),ux = {'text': str(get_num_short(self.cc.get_price('factory'))),**LABEL_COST_UX})
        
        self.lbl_mul_cost_cursor = UILabel( Rect(BUTTON_DEST[0],BUTTON_DEST[1]-(HEIGHT*.025),QUARTER_WIDTH,HEIGHT*.025),ux = {'text': str(get_num_short(self.cc.get_multiplicator_price('cursor'))),**LABEL_COST_UX})
        
        self.lbl_mul_cost_grandma = UILabel( Rect(BUTTON_DEST[0],(BUTTON_DEST[1]*2)-(HEIGHT*.025),QUARTER_WIDTH,HEIGHT*.025),ux = {'text': str(get_num_short(self.cc.get_multiplicator_price('grandma'))),**LABEL_COST_UX})
        
        self.lbl_mul_cost_farm = UILabel( Rect(BUTTON_DEST[0],(BUTTON_DEST[1]*3)-(HEIGHT*.025),QUARTER_WIDTH,HEIGHT*.025),ux = {'text': str(get_num_short(self.cc.get_multiplicator_price('farm'))),**LABEL_COST_UX})
        
        self.lbl_mul_cost_mine = UILabel( Rect(BUTTON_DEST[0],(BUTTON_DEST[1]*4)-(HEIGHT*.025),QUARTER_WIDTH,HEIGHT*.025),ux = {'text': str(get_num_short(self.cc.get_multiplicator_price('mine'))),**LABEL_COST_UX})
        
        self.lbl_mul_cost_factory = UILabel( Rect(BUTTON_DEST[0],(BUTTON_DEST[1]*5)-(HEIGHT*.025),QUARTER_WIDTH,HEIGHT*.025),ux = {'text': str(get_num_short(self.cc.get_multiplicator_price('factory'))),**LABEL_COST_UX})
        
        self.lbl_mul_cost_cursor = UILabel( Rect(BUTTON_DEST[0],(BUTTON_DEST[1]*6)-(HEIGHT*.025),QUARTER_WIDTH,HEIGHT*.025),ux = {'text': str(get_num_short(self.cc.get_click_price())),**LABEL_COST_UX})
        
        #? Level Up & Multiplicator Animations
        
        self.animation_click = Animation(self,self.star_image,UPGRADE_KEYFRAMES,(self.btn_upgrade_click.pos[0]+(self.btn_upgrade_click.dest[0]//2),self.btn_upgrade_click.pos[1]+(self.btn_upgrade_click.dest[1]//2)),time_multiplier=50)
        
        self.animation_mul_cursor = Animation(self,self.star_image,UPGRADE_KEYFRAMES,(self.btn_mul_upgrade_cursor.pos[0]+(self.btn_upgrade_cursor.dest[0]//2),self.btn_upgrade_cursor.pos[1]+(self.btn_upgrade_cursor.dest[1]//2)),time_multiplier=50)
        
        self.animation_mul_grandma = Animation(self,self.star_image,UPGRADE_KEYFRAMES,(self.btn_mul_upgrade_grandma.pos[0]+(self.btn_mul_upgrade_grandma.dest[0]//2),self.btn_mul_upgrade_grandma.pos[1]+(self.btn_mul_upgrade_grandma.dest[1]//2)),time_multiplier=50)
        
        self.animation_mul_farm = Animation(self,self.star_image,UPGRADE_KEYFRAMES,(self.btn_mul_upgrade_farm.pos[0]+(self.btn_mul_upgrade_farm.dest[0]//2),self.btn_mul_upgrade_farm.pos[1]+(self.btn_mul_upgrade_farm.dest[1]//2)),time_multiplier=50)
        
        self.animation_mul_mine = Animation(self,self.star_image,UPGRADE_KEYFRAMES,(self.btn_mul_upgrade_mine.pos[0]+(self.btn_mul_upgrade_mine.dest[0]//2),self.btn_mul_upgrade_mine.pos[1]+(self.btn_mul_upgrade_mine.dest[1]//2)),time_multiplier=50)
        
        self.animation_mul_factory = Animation(self,self.star_image,UPGRADE_KEYFRAMES,(self.btn_mul_upgrade_factory.pos[0]+(self.btn_mul_upgrade_factory.dest[0]//2),self.btn_mul_upgrade_factory.pos[1]+(self.btn_mul_upgrade_factory.dest[1]//2)),time_multiplier=50)
        
        self.animation_cursor = Animation(self,image.load(f"{IMAGE_PATH}cursor.png"),UPGRADE_KEYFRAMES,(self.btn_upgrade_cursor.pos[0]+(self.btn_upgrade_cursor.dest[0]//2),self.btn_upgrade_cursor.pos[1]+(self.btn_upgrade_cursor.dest[1]//2)),time_multiplier=50)
        
        self.animation_grandma = Animation(self,image.load(f"{IMAGE_PATH}grandma.png"),UPGRADE_KEYFRAMES,(self.btn_upgrade_grandma.pos[0]+(self.btn_upgrade_grandma.dest[0]//2),self.btn_upgrade_grandma.pos[1]+(self.btn_upgrade_grandma.dest[1]//2)),time_multiplier=50)
        
        self.animation_farm = Animation(self,image.load(f"{IMAGE_PATH}farm.png"),UPGRADE_KEYFRAMES,(self.btn_upgrade_farm.pos[0]+(self.btn_upgrade_farm.dest[0]//2),self.btn_upgrade_farm.pos[1]+(self.btn_upgrade_farm.dest[1]//2)),time_multiplier=50)
        
        self.animation_mine = Animation(self,image.load(f"{IMAGE_PATH}mine.png"),UPGRADE_KEYFRAMES,(self.btn_upgrade_mine.pos[0]+(self.btn_upgrade_mine.dest[0]//2),self.btn_upgrade_mine.pos[1]+(self.btn_upgrade_mine.dest[1]//2)),time_multiplier=50)
        
        self.animation_factory = Animation(self,image.load(f"{IMAGE_PATH}factory.png"),UPGRADE_KEYFRAMES,(self.btn_upgrade_factory.pos[0]+(self.btn_upgrade_factory.dest[0]//2),self.btn_upgrade_factory.pos[1]+(self.btn_upgrade_factory.dest[1]//2)),time_multiplier=50)
        
        self.animation_cookie_click = Animation(self,image.load(f"{IMAGE_PATH}cookie.png"),KEYFRAMES,(HALF_WIDTH,HALF_HEIGHT),time_multiplier=50)
        
        self.cookie_label = UILabel(
            Rect(QUARTER_WIDTH*1.5,0,QUARTER_WIDTH,HEIGHT*.1),
            ux = {
                'text': '0',
                'size': (QUARTER_WIDTH,HEIGHT*.1),
                'font': FONT(size=40),
                'bcg': TRANSPARENT,
                'tcg': ('#FFE5CC',)
            }
        )
        
            
    def on_cookie_click(self,*_):
        self.audio_handler.play_sound('click')
        self.animation_cookie_click.start_animation()
        self.cc.click()
        self.ft.add_object()
        
    def run(self):
        while self.is_running:
            GLOBAL_DELTA_TIME.before()
            self.CLK.tick(60)
            self.window.surface.fill(Color('#FFB266'))
            self.cr.update()
            self.mw.update()
            
            self.animation_cookie_click.update()
            
            self.animation_click.update()
            
            self.animation_cursor.update()
            self.animation_grandma.update()
            self.animation_farm.update()
            self.animation_mine.update()
            self.animation_factory.update()
            
            self.animation_mul_cursor.update()
            self.animation_mul_grandma.update()
            self.animation_mul_farm.update()
            self.animation_mul_mine.update()
            self.animation_mul_factory.update()
            
            UIM.render_queue(self)
            
            self.cc.update()
            self.cookie_label.render(f"{get_num_short(self.cc.get())}" + (f"+{self.cc.get_auto_clicker():.1f}" if self.cc.get_auto_clicker() else ''))
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