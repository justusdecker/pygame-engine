from pygame import Surface, Rect, SRCALPHA
from data.modules.ui.ui_element import UIElement, UIC
from pygame.draw import rect as rect_draw
from data.modules.ui.ui_button import UIButton
from data.modules.ui.ui_label import UILabel
from data.modules.ui.ui_progress_bar import UIProgressBar
from moviepy.video.io.VideoFileClip import VideoFileClip
from data.modules.constants import GLOBAL_DELTA_TIME
from data.modules.data_management import DM
from pygame import mixer, pixelcopy
import numpy
from pygame.image import save as image_save
from time import time
from pygame.transform import scale as image_scale
from pygame.mouse import get_pos
#!Currently not working
class UXVideo:
    def __init__(self,**options) -> None:
        self.size = options.get('size',(384,216))
        self.border_radius = options.get('border_radius',15)
        CUTOUT = Surface(self.size,SRCALPHA)
        BACKGROUND = Surface(self.size)
        CUTOUT.fill((0,255,0))
        rect_draw(CUTOUT,
                     (0,0,0,0),
                     (0,
                      0,
                      *self.size
                      ),
                        border_radius=self.border_radius
                        )
        self.CUTOUT = CUTOUT

class UIVideoPlayer(UIElement):
    def __init__(self, rect: Rect, **kwargs):
        super().__init__(rect, **kwargs)
        UIC.add_element('uiVideoPlayer')
        self.next_frame = 0
        self.n_pos = self.pos
        self.current_frame = 0
        self.is_playing = False
        self.is_loaded = False
        self.frame = Surface(self.dest)
        self.UX = UXVideo()
        self.fullscreen = False
        self.audio_path,self.video_path = '',''
        self.last_audio_path,self.last_video_path = '',''
        self.play_button = UIButton(Rect(24,216-24,24,24),ux={'text': '|>','size':(24,24)},on_press_callback=self.toggle_play,parent=self,group=self.group)
        
        self.ff_button = UIButton(Rect(48,216-24,24,24),ux={'text': '>>','size':(24,24)},on_press_callback=self.move_frame_plus,parent=self,group=self.group)
        self.rw_button = UIButton(Rect(0,216-24,24,24),ux={'text': '<<','size':(24,24)},on_press_callback=self.move_frame_minus,parent=self,group=self.group)
        self.fullscreen_toggle_button = UIButton(Rect(384-24,216-24,24,24),ux={'text': '=','size':(24,24)},on_press_callback=self.toggle_fullscreen,parent=self,group=self.group)
        self.take_thumbnail_button = UIButton(Rect(384-48,216-24,24,24),ux={'text': '[]','size':(24,24)},on_press_callback=self.take_image,parent=self,group=self.group)
        self.time_label = UILabel(Rect(72,216-24,144,24),ux={'text': '<<','size':(144,24)},parent=self,group=self.group)
        self.time_label.UX.text = f'00:00 / INF'
        self.time_label.set_image(self.time_label.UX.gen())
        
        self.progress_bar = UIProgressBar(Rect(0,216-32,384,8),ux={'size':(384,8)},parent=self,group=self.group)
        self.progress_fullscreen_bar = UIProgressBar(Rect(0,720-32,1280,8),ux={'size':(1280,8)},parent=self,group=self.group)
        self.progress_fullscreen_bar.visible = False
        self.set_image(self.frame)
        if 'app' in kwargs:
            self.app = kwargs['app']
        else:
            raise Exception('No App. No Game!')
    def toggle_fullscreen(self,*_,force:bool=None):
        self.fullscreen = not self.fullscreen if force is None else force
        
        if self.fullscreen:
            self.pos = (0,0)
            self.time_label.pos = (72,720-24)
            self.rw_button.pos = (0,720-24)
            self.play_button.pos = (24,720-24)
            self.ff_button.pos = (48,720-24)
            self.fullscreen_toggle_button.pos = (1280-24,720-24)
            self.take_thumbnail_button.pos = (1280-48,720-24)
            self.progress_bar.visible = False
            self.progress_fullscreen_bar.visible = True
        else:
            self.pos = self.n_pos
            self.rw_button.pos = (0,216-24)
            self.play_button.pos = (24,216-24)
            self.ff_button.pos = (48,216-24)
            self.time_label.pos = (72,216-24)
            self.fullscreen_toggle_button.pos = (384-24,216-24)
            self.take_thumbnail_button.pos = (384-48,216-24)
            self.progress_bar.visible = True
            self.progress_fullscreen_bar.visible = False
    def gdz(self,val):
        if val < 10:
            return '0' + str(val)
        return str(val)
    def mod60(self,val):
        if val == 0: return 0
        return val % 60
    
    def _load_data(self,video_path,audio_path):
        try:
            if self.visible:
                self.current_frame = 0
                self.next_frame = 0
                self.is_loaded = False
                self.video_path = video_path
                self.audio_path = audio_path
                self.video = VideoFileClip(video_path)
                self.first_audio = mixer.music.load(audio_path)
                self.time_label.UX.text = f'{self.get_time()}'
                self.time_label.set_image(self.time_label.UX.gen())
                self.surface.fill((0,0,0))
                self.video.rotation = 90
                self.is_loaded = True
                self.fullscreen = False
                self.toggle_fullscreen(force=False)
        except:
            self.is_loaded = False
    def switch(self,trig:bool):
        if trig:
            if not mixer.music.get_busy():mixer.music.play(0,self.current_frame)
        else:
            if mixer.music.get_busy():mixer.music.stop()
    def move_frame_plus(self,*_):
        self.move_frame(15)
    def move_frame_minus(self,*_):
        self.move_frame(-15)
    def take_image(self,*_):
        frame = pixelcopy.make_surface(numpy.flipud(numpy.rot90(self.video.get_frame(self.current_frame),1)))
        image_save(frame,f'{int(time())}.png')
    def move_frame(self,num:int):
        if self.is_playing:
            if self.current_frame + num > self.video.duration:
                self.current_frame = 0
                self.next_frame = 0
            elif self.current_frame + num < 0:
                self.current_frame = 0
                self.next_frame = 0
            else: 
                self.current_frame += num
                self.next_frame = self.current_frame
            mixer.music.pause()
            mixer.music.play(0,self.current_frame)
    def toggle_play(self,*_):
        
        if DM.existFile(self.video_path) and DM.existFile(self.audio_path):
            
            if self.video_path != self.last_video_path or self.audio_path != self.last_audio_path:
                self._load_data(self.video_path,self.audio_path)
                self.last_video_path = self.video_path 
                self.last_audio_path = self.audio_path
            self.is_playing = not self.is_playing
            self._play()
        else:
            print(f'video or Audio File dont exist [{self.audio_path}] [{self.video_path}]')
    def _stop(self):
        self.is_playing = False
        self.is_loaded = False
        self._play()
    def _play(self,*_):
        if self.is_playing:
            if mixer.music.get_busy():mixer.music.stop()
            mixer.music.play(0,self.current_frame)
        elif not self.is_playing:
            if mixer.music.get_busy():mixer.music.stop()
    def get_time(self):
            
        minutes = self.gdz(int(self.current_frame / 60))
        seconds = self.gdz(int(self.current_frame % 60))
        mminutes = self.gdz(int(self.video.duration / 60))
        mseconds = self.gdz(int(self.video.duration % 60))


        return f'{minutes}:{seconds}/{mminutes}:{mseconds}'
    def update(self):#! Change
        
        if not self.is_playing: 
            
            return
        if not self.visible: return
        if not self.is_loaded: return
        if self.progress_fullscreen_bar.is_pressed:
            mx = abs(get_pos()[0] / 1280) if get_pos()[0] > 0 else 0

            self.current_frame = self.video.duration * (mx)
            mixer.music.pause()
            mixer.music.play(0,self.current_frame)
        if self.progress_bar.is_pressed:
            mx = abs((self.get_abs_position()[0]-get_pos()[0]) / self.dest[0])
            

            self.current_frame = self.video.duration * (mx)
            mixer.music.pause()
            mixer.music.play(0,self.current_frame)
        if self.fullscreen:
            self.progress_fullscreen_bar.draw(self.current_frame / self.video.duration)
        else:
            self.progress_bar.draw(self.current_frame / self.video.duration)
        
        
        
        if self.current_frame <= self.video.duration:
            self.current_frame += GLOBAL_DELTA_TIME.get()
            if not mixer.music.get_busy(): 
                mixer.music.play(0,self.current_frame)
            if self.current_frame >= self.next_frame:
                self.next_frame = self.current_frame + (1/60)
                img = pixelcopy.make_surface(numpy.flipud(numpy.rot90(self.video.get_frame(self.current_frame),1)))
            else:
                img = self.surface.copy()
            self.time_label.UX.text = f'{self.get_time()}'
            self.time_label.set_image(self.time_label.UX.gen())
            if self.fullscreen:
                
                self.surface = image_scale(img,(1280,720))
                
                #self.surface.blit(FONTDRAW.draw(self.get_time(),True,size=50),(0,0))
                
            else:
                self.surface = Surface(self.dest)
                if self.dest is not None: img = image_scale(img,self.dest)
                self.surface.blit(img,(0,0))
                #self.surface.blit(FONTDRAW.draw(self.get_time(),True,size=13),(0,0))
                self.surface.blit(self.UX.CUTOUT,(0,0))
                self.surface.set_colorkey((0,255,0))

        else:
            if mixer.get_busy(): 
                mixer.music.stop()
        super().update()
