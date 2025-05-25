from data.modules.constants import *
from data.modules.kernel.window import Window
from pygame.event import get as get_events
from pygame import QUIT,quit as pg_quit,Clock, KEYDOWN,KEYUP, WINDOWLEAVE
from pygame.mouse import get_visible,set_pos
from pygame.image import load
from time import sleep

class Application:
    """
    .. window:: A pygame-engine window
    .. is_running:: IF False - the app closes
    .. CLK:: A pygame.Clock object
    """
    def __init__(self):
        self.window = Window()
        self.is_running = True
        self.CLK = Clock()
        self.pressed_keys = []
        self.window.render(load('data\\bin\\img\\pe_logo.ico'),(HALF_WIDTH,HALF_HEIGHT),(-128,-128))
        self.update()
        sleep(.35)

    def update(self):
        "Updates the window & calls the event handler"

        self.window.update()
        
        self.event_handler()
            
    def event_handler(self):
        "A default pygame event handler"
        self.pressed_keys = []
        for event in get_events():
            if event.type == QUIT:
                pg_quit()
                self.is_running = False
            if event.type == KEYDOWN:
                self.pressed_keys.append(event.key)