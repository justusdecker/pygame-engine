from pygame import Surface
from pygame.transform import scale_by
from data.modules.constants import GLOBAL_DELTA_TIME
class Animation:
    def __init__(self,
                 app,
                 image: Surface,
                 keyframes: list[dict],
                 pos: list[int,int],
                 fps:int=10,
                 loops: int = 1,
                 time_multiplier: float = 1,
                 stay:bool=True):
        self.stay = stay
        self.loops = loops
        self.pos = pos
        self.app = app
        self.image = image
        self.render_images = [None for x in range(len(keyframes))]
        self.keyframes = keyframes
        self.time = 0
        self.time_multiplier = time_multiplier
        self.run = False
        {
            "frame": 0,
            "x_offset": 0,
            "y_offset": 0,
            "scale": [0,0]
        }
        for i in range(len(keyframes)):
            self.crop(i)
    def crop(self,index:int):
        
        self.render_images[index] = scale_by(self.image,self.keyframes[index]['scale'])
    def start_animation(self):
          self.time = 0
          self.run = True
    def update(self):
        
        if self.loops == -1 and not self.run:
            self.start_animation()
        if self.run:
            self.time += GLOBAL_DELTA_TIME.get() * self.time_multiplier
            if int(self.time) >= len(self.render_images):
                self.time = 0
                self.run = 0
            x,y = self.keyframes[int(self.time)]['x_offset'],self.keyframes[int(self.time)]['y_offset']
            img = self.render_images[int(self.time)]
            modified_pos = self.pos[0] - (img.get_width()//2),self.pos[1] - (img.get_height()//2)
            self.app.window.render(img,modified_pos,(x,y))
        elif not self.run and self.stay:
            x,y = self.keyframes[int(self.time)]['x_offset'],self.keyframes[0]['y_offset']
            img = self.render_images[0]
            modified_pos = self.pos[0] - (img.get_width()//2),self.pos[1] - (img.get_height()//2)
            self.app.window.render(img,modified_pos,(x,y))
            
        