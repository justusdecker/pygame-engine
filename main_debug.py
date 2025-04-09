from data.modules.constants import *
from data.modules.window import Window
from pygame.event import get as get_events
from pygame import QUIT,quit as pg_quit,Rect,image
from data.modules.ui.ui_elements import UIGroup,UIImage,UILabel,UIM
class App:
    def __init__(self):
        self.window = Window()
        self.is_running = True
        self.group_test = UIGroup('test')
        self.thumbnail = UIImage(
            Rect(
                48,
                48,
                576,
                324
                ),
            ux={
                'size': (576,324)
                },
            group=self.group_test
            )
        
        self.thumbnail.setImage(image.load("data\\bin\\img\\test.png"))
        self.nameLabel = UILabel(
            Rect(
                48,
                372,
                576,
                24
                ),
            change=True,
            clean=True,
            text='',
            group=self.group_test
            )
    def run(self):
        while self.is_running:
            self.window.surface.fill((128,128,128))
            UIM.renderQueue(self,['test'])
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