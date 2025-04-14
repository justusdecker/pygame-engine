from pygame.mixer import music, Sound,init as mixer_init
from data.modules.log import LOG
mixer_init()
class AudioHandler:
    def __init__(self,
                 bgm_lib: dict[str,str]={},
                 sfx_lib: dict[str,str]={}):
        self.bgm_lib = bgm_lib
        self.sfx_lib: dict[str,Sound] = {key : Sound(sfx_lib[key]) for key in sfx_lib.keys()}
        self.is_playing = False
    def play_sound(self,key:str,*play_args:int):
        self.sfx_lib[key].play(*play_args)
        
    def play(self,key:str):
        music.load()
        LOG.nlog()