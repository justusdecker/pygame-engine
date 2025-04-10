from data.modules.constants import *
from data.modules.window import Window
from pygame.event import get as get_events
from pygame import QUIT,quit as pg_quit,Rect,image

class Application:
    def __init__(self):
        self.window = Window()
        self.is_running = True

    def update(self):

        self.window.update()
        
        self.event_handler()
            
    def event_handler(self):
        for event in get_events():
            if event.type == QUIT:
                pg_quit()
                self.is_running = False
