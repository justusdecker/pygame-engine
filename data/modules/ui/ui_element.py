from data.modules.log import LOG
from pygame import Surface, Rect
from pygame.mouse import get_pos as mouse_pos, get_pressed as mouse_pressed
class UIElement: pass

class UICounter:
    def __init__(self):
        self.count = {}
        self.all = 0
    def add_element(self,key):
        self.all += 1
        
        if key in self.count:
            self.count[key] += 1
        else:
            self.count[key] = 1
            
        LOG.nlog(1,'created UIE of Type: $ | e: $',[key,self.count[key]])
    def rem_element(self,key):
        if key in self.count:
            self.count[key] -= 1
        LOG.nlog(1,'removed UIE of Type: $ | e: $',[key,self.count[key]])
            
UIC = UICounter()
class UIID:
    def __init__(self) -> None:
        self.id = 0
    def add(self):
        self.id += 1
        return self.id - 1
    
UIIDCOUNT = UIID()
class UIManager: #
    def __init__(self) -> None:
        self.queue = {}
        UIC.add_element('uiManager')
    def add_to_queue(self,object,layer):
        if not layer in self.queue:
            self.queue[layer] = []
        
        self.queue[layer].append(object)
        
        LOG.nlog(1,'$ added to queue on layer $',[object.element_id,layer])
    def remove_from_queue(self,id):
        for layer in self.queue:
            for idx,obj in enumerate(self.queue[layer]):
                if obj.element_id == id:
                    self.queue[layer].pop(idx)
                    LOG.nlog(1,'$ removed from queue  $',[obj.id,layer])
                    

        
        
    def render_queue(self,
                    app,
                    groups:list | tuple = ('default',),
                    ignoreList=[]):
        #+ Only One button is clickable
        _updates = []
        for layer in self.queue.keys():
            if layer in ignoreList: continue
            for object in self.queue[layer]:

                if object.group.group_name in groups:
                        
                    _updates.append(object)
                    if object.visible:
                        app.window.surface.blit(object.get_image(),object.get_abs_position())
        _updates.reverse()
        for object in _updates:
            object.update() 
            if object.this_frame_pressed:
                break
            #! Check Frame is checked

UIM = UIManager()

class UIGroup:
    def __init__(self,
                 group_name):
        self.group_name = group_name
        UIC.add_element('uiGroup')
UI_DEFAULT_GROUP = UIGroup('default')
class UIElement:
    def __init__(self,
                 rect: Rect,
                 **kwargs) -> None:
        """
        The Default UI Element:
        Arguments:
            rect    : pygame.Rect = (pos,dest)
            kwargs:
                layer   :   int         =   0
                visible :   bool        =   True
                canvas  :   None        =   None    [CURRENTLY NOT USED!]
                anchor  :   str         =   'top_left'  [BETA: NOT USED IN EVERY FUNCTION]
                name    :   str         =   ''
                ? Makes finding much easier
                parent  :   UIElement   = None
                group   :UIGroup        = UI_DEFAULT_GROUP
        """
        self.rect = rect.copy()
        
        UIC.add_element('uiElement')
        self.pos = rect.x,rect.y
        self.dest = rect.w,rect.h
        
        self.group = kwargs.get('group',UI_DEFAULT_GROUP)
        
        self.element_id = UIIDCOUNT.add()
        self.element_name = kwargs['name'] if 'name' in kwargs else ''
        
        self.set_layer(kwargs['layer'] if 'layer' in kwargs else 0)
        
        self.set_visibility(kwargs['visible'] if 'visible' in kwargs else True)
        
        self.set_canvas(kwargs['canvas'] if 'canvas' in kwargs else None)
        
        self.set_anchor(kwargs['anchor'] if 'anchor' in kwargs else 'top_left')
        
        self.set_parent(kwargs['parent'] if 'parent' in kwargs else None)
        
        UIM.add_to_queue(self,self.layer)
        
        #Clickable Stuff
        self.is_hovered = False
        self.is_pressed = False
        self.stop = False
        self.this_frame_hovered = False
        self.this_frame_un_hovered = False
        self.this_frame_pressed = False
        self.this_frame_un_pressed = False
        self.last_frame_hover = False
        
    def check(self,abs_pos,dest):
        #! Defines thisFrame Values
        self.this_frame_hovered = False
        self.this_frame_un_hovered = False
        self.this_frame_pressed = False
        self.this_frame_un_pressed = False
        click = mouse_pressed()[0]
        
        if not self.stop:
            
            x,y,w,h = abs_pos[0],abs_pos[1],dest[0],dest[1]
            g,l = mouse_pos()
            
            if g > x and l > y and g < x + w and l < y + h: #? Check Hovering
                self.is_hovered = True
                if not self.last_frame_hover:
                    self.this_frame_hovered = True
                    self.last_frame_hover = True
            else:
                self.is_hovered = False
                if self.last_frame_hover:
                    self.last_frame_hover = False
                    self.this_frame_un_hovered = True
            
            if not self.is_hovered and click:# ? Check not over!
                self.stop = True
                return

            if not click and self.is_pressed:    # ? Check Unpress Condition
                self.is_pressed = False
                self.this_frame_un_pressed = True

            if self.is_hovered and click and not self.is_pressed:    # ? Check Pressed Condition
                self.is_pressed = True
                self.this_frame_pressed = True
            
        if not click: # ? Reset Blocking!
            self.stop = False     
    def kill(self):
        UIM.remove_from_queue(self.element_id)
        del self
    def update(self):
        if self.visible:
            return self.check(self.get_abs_position(),self.dest)
    
    def get_image(self):
        if not hasattr(self,'surface'):
            self.surface = Surface((1,1))
        return self.surface
    
    def get_abs_position(self):
        x,y = self.get_parent_offsets()
        match self.anchor: #? Manipulates the offset by a certain value
            case 'center':
                if self.parent is None:
                    return self.pos[0] + (self.dest[0] *.5),self.pos[1] + (self.dest[1] *.5)
                else:
                    return x + (self.parent.dest[0] *.5) - (self.dest[0] *.5) + self.pos[0],y  + (self.parent.dest[1] *.5) - (self.dest[1] *.5)+ self.pos[1]
            case 'top_left':
                if self.parent is None:
                    return self.pos
                else:
                    return x + self.pos[0],y + self.pos[1]
    
    def get_position(self) -> list:
        return self.pos
    
    def get_dest(self) -> list:
        return self.dest
    
    def get_layer(self) -> int:
        return self.layer
    
    def get_parent_offsets(self) -> list:
        x_offset,y_offset = 0,0
        parent = self.parent
        
        while parent is not None:
            x_offset += parent.pos[0]
            y_offset += parent.pos[1]
            parent = parent.parent
            
        return x_offset,y_offset
    
    def get_all_parents(self) -> list[UIElement]:
        parents = []
        parent = self.parent
        while parent is not None:
            parents.append(parent)
            parent = parent.parent
            
        return parents
    
    def get_parent(self) -> UIElement:
        return self.parent
    
    def set_layer(self,layer:int) -> None:
        self.layer: int = layer
    
    def set_parent(self,parent: UIElement) -> None:
        self.parent: UIElement = parent
    
    def set_anchor(self,position:str) -> None:
        self.anchor: str = position
        
    def set_image(self,surface:Surface) -> None:
        self.surface: Surface = surface
        
    def set_canvas(self,value:Rect) -> None:
        self.canvas: Rect = value
        
    def set_visibility(self,value:bool) -> None:
        self.visible: bool = value
