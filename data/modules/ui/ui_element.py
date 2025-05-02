from data.modules.log import LOG
from pygame import Surface, Rect
from data.modules.vector import Vector4
from pygame.mouse import get_pos as mouse_pos, get_pressed as mouse_pressed
class UIElement: pass

class UICounter:
    """
    For debugging & Performance testing.
    
    Each UI Element adds itself automatically to the ``count`` & ``all_elements`` value
    """
    def __init__(self):
        self.count = {}
        self.all_elements = 0
    def log(self,t:str, key:str):
        LOG.nlog(1,f'{t} UIE of Type: $ | e: $',[key,self.count[key]])
    def add_element(self,key):
        "Add a element to the UICounter."
        self.all_elements += 1
        self.count[key] = self.count[key] + 1 if key in self.count else 1
        self.log('created',key)
    def rem_element(self,key):
        "Remove a element from the UICounter if existing."
        self.all_elements -= 1
        if key in self.count:
            self.count[key] -= 1
        self.log('removed',key)
            
UIC = UICounter()
class UIID:
    """
    This class is managing the ``èlement_id`` upcounting for each added UIElement.
    """
    ID = 0
    def add(self) -> int:
        "Add a new ID to UIID & return the current one"
        self.ID += 1
        return self.ID - 1
    
UIIDCOUNT = UIID()
class UIManager:
    def __init__(self) -> None:
        self.queue = {}
        UIC.add_element('uiManager')
        
    def add_to_queue(self,object,layer):
        """
        This adds a ``UIElement`` to the render queue & create a new layer if its not existing.
        """
        if layer not in self.queue:
            self.queue[layer] = []
        self.queue[layer].append(object)
        LOG.nlog(1,'$ added to queue on layer $',[object.element_id,layer])
        
    def remove_from_queue(self,id):
        """
        Remove an existing ``UIElement`` from the queue & remove a layer if empty.
        """
        for layer in self.queue:
            for idx,obj in enumerate(self.queue[layer]):
                if obj.element_id == id:
                    self.queue[layer].pop(idx)
                    LOG.nlog(1,'$ removed from queue  $',[obj.element_id,layer])
                if not self.queue[layer]:
                    self.queue.pop(layer)
                    
    def render_queue(self,
                    app,
                    groups:list | tuple = ('default',),
                    ignore_list=[]):
        """
        Go through all existing layers, if layer is not ignored.
        
        Render every ``UIElement`` in the current layer if object is visible.
        
        The default group ist 'default' & you can use multiple groups to organize your project.
        
        Check ``UIElement`` collisions in reversed order.
        
        If a ``UIElement`` has already been pressed, the next ``UIElement's`` will not update.
        """
        _updates = []
        layers = [layer for layer in self.queue.keys()]
        layers.sort()
        for layer in layers:
            if layer in ignore_list: continue
            for object in self.queue[layer]:
                if object.group.group_name in groups: # Check the group.
                    if object.visible:
                        _updates.append(object)
                        app.window.surface.blit(object.get_image(),object.get_abs_position())
        _updates.reverse()
        for object in _updates:
            object.update() 
            if object.this_frame_pressed:
                break

UIM = UIManager()

class UIGroup:
    """
    Used to draw groups of UI elements. 
        
    Multiple groups can be rendered.
    """
    def __init__(self,
                 group_name):
        self.group_name = group_name
        UIC.add_element('uiGroup')
UI_DEFAULT_GROUP = UIGroup('default')
class UIElement:
    """
    The core UIElement class
    ******
    Arguments
    ^^^^
    
    .. rect:: A ``pygame.Rect`` value. Will be stored as ``pos`` & ``dest``
    .. group:: 
        
        Used to draw groups of UI elements. 
        
        Multiple groups can be rendered.

        Defaults to: ``UI_DEFAULT_GROUP``
    .. layer::

        Layers are used to determine the z position on screen.
        
        The higher the layer, the higher the priority on the screen.

        Defaults to: ``0``
    .. visible::
        Defaults to: ``True``
    .. canvas::
        CURRENTLY NOT BEING USED!
    .. anchor::
        Determines the anchor position e.g. ``'bottom-center'`` will accordingly offset the position by a certain value.
        
        Currently not complete! The most ``UIElement's`` will not support this. Will be changed later!
        
        Defaults to: ``'top-left'``
    .. parent::
        A parent is used in combination with get_abs_position to get the absolute offset or a higher priority ``UIElement``

        Defaults to: ``None``
    .. element_id::
        Used to determine which ``UIElement`` is being used. 
        
        Useful for dropdown menus and much more.
    .. element_name
        Used to determine which ``UIElement`` is being used. 
        
        Useful for dropdown menus and much more.
        
        Defauls to ``''``
    """
    def __init__(self,
                 vector: Vector4,
                 **kwargs) -> None:
        self.rect = vector
        
        UIC.add_element('uiElement')
        self.pos = vector.x,vector.y
        self.dest = vector.z,vector.w
        
        self.group = kwargs.get('group',UI_DEFAULT_GROUP)
        
        self.element_id = UIIDCOUNT.add()
        self.element_name = kwargs['element_name'] if 'element_name' in kwargs else ''
        
        self.set_layer(kwargs['layer'] if 'layer' in kwargs else 100)
        
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
        """
        Remove itself
        """
        UIM.remove_from_queue(self.element_id)
        del self
    def update(self):
        """
        Don't use this method!
        This will be called by the ``UIManager``
        """
        if self.visible:
            return self.check(self.get_abs_position(),self.dest)
    
    def get_image(self) -> Surface:
        if not hasattr(self,'surface'):
            self.surface = Surface((1,1))
        return self.surface
    
    def get_abs_position(self) -> tuple[int,int]:
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
