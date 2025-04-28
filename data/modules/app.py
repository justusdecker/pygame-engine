from data.modules.constants import *
from data.modules.window import Window
from pygame.event import get as get_events
from pygame import QUIT,quit as pg_quit,Clock

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

    def update(self):
        "Updates the window & calls the event handler"

        self.window.update()
        
        self.event_handler()
            
    def event_handler(self):
        "A default pygame event handler"
        for event in get_events():
            if event.type == QUIT:
                pg_quit()
                self.is_running = False
