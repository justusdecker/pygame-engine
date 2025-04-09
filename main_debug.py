from data.modules.constants import *
from data.modules.window import Window
from pygame.event import get as get_events
from pygame import QUIT,quit as pg_quit
class App:
    def __init__(self):
        self.window = Window()
        self.is_running = True
    def run(self):
        while self.is_running:
            self.window.update()
            self.event_handler()
    def event_handler(self):
        for event in get_events():
            if event.type == QUIT:
                pg_quit()
                self.is_running = False
if __name__ == "__main__":
    APP = App()
    APP.run()