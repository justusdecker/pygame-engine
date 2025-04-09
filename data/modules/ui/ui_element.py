from data.modules.data_management import UnpackManager
from data.modules.log import LOG
from pygame import Surface, Rect
from pygame.mouse import get_pos as mouse_pos, get_pressed as mouse_pressed
class UIElement: pass

class UICounter:
    def __init__(self):
        self.count = {}
        self.all = 0
    def addElement(self,key):
        self.all += 1
        
        if key in self.count:
            self.count[key] += 1
        else:
            self.count[key] = 1
            
        LOG.nlog(1,'created UIE of Type: $ | e: $',[key,self.count[key]])
    def remElement(self,key):
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
        UIC.addElement('uiManager')
    def addToQueue(self,object,layer):
        if not layer in self.queue:
            self.queue[layer] = []
        
        self.queue[layer].append(object)
        
        LOG.nlog(1,'$ added to queue on layer $',[object.elementId,layer])
    def removeFromQueue(self,id):
        for layer in self.queue:
            for idx,obj in enumerate(self.queue[layer]):
                if obj.elementId == id:
                    self.queue[layer].pop(idx)
                    LOG.nlog(1,'$ removed from queue  $',[obj.id,layer])
                    

        
        
    def renderQueue(self,
                    app,
                    groups:list | tuple = ('default',),
                    ignoreList=[]):
        #+ Only One button is clickable
        _updates = []
        for layer in self.queue.keys():
            if layer in ignoreList: continue
            for object in self.queue[layer]:

                if object.group.groupName in groups:
                        
                    _updates.append(object)
                    if object.visible:
                        app.window.surface.blit(object.getImage(),object.getAbsPosition())
        _updates.reverse()
        for object in _updates:
            object.update() 
            if object.thisFramePressed:
                break
            #! Check Frame is checked

UIM = UIManager()

class UIGroup:
    def __init__(self,
                 groupName):
        self.groupName = groupName
        UIC.addElement('uiGroup')
UIDefaultGroup = UIGroup('default')
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
                group   :UIGroup        = UIDefaultGroup
        """
        self.rect = rect.copy()
        
        UIC.addElement('uiElement')
        self.pos = rect.x,rect.y
        self.dest = rect.w,rect.h
        
        self.group = UnpackManager('group',kwargs,UIDefaultGroup)
        
        self.elementId = UIIDCOUNT.add()
        self.elementName = kwargs['name'] if 'name' in kwargs else ''
        
        self.setLayer(kwargs['layer'] if 'layer' in kwargs else 0)
        
        self.setVisibility(kwargs['visible'] if 'visible' in kwargs else True)
        
        self.setCanvas(kwargs['canvas'] if 'canvas' in kwargs else None)
        
        self.setAnchor(kwargs['anchor'] if 'anchor' in kwargs else 'top_left')
        
        self.setParent(kwargs['parent'] if 'parent' in kwargs else None)
        
        UIM.addToQueue(self,self.layer)
        
        #Clickable Stuff
        self.isHovered = False
        self.isPressed = False
        self.stop = False
        self.thisFrameHovered = False
        self.thisFrameUnHovered = False
        self.thisFramePressed = False
        self.thisFrameUnPressed = False
        self.lastFrameHover = False
        
    def check(self,absPos,dest):
        #! Defines thisFrame Values
        self.thisFrameHovered = False
        self.thisFrameUnHovered = False
        self.thisFramePressed = False
        self.thisFrameUnPressed = False
        click = mouse_pressed()[0]
        
        if not self.stop:
            
            x,y,w,h = absPos[0],absPos[1],dest[0],dest[1]
            g,l = mouse_pos()
            
            if g > x and l > y and g < x + w and l < y + h: #? Check Hovering
                self.isHovered = True
                if not self.lastFrameHover:
                    self.thisFrameHovered = True
                    self.lastFrameHover = True
            else:
                self.isHovered = False
                if self.lastFrameHover:
                    self.lastFrameHover = False
                    self.thisFrameUnHovered = True
            
            if not self.isHovered and click:# ? Check not over!
                self.stop = True
                return

            if not click and self.isPressed:    # ? Check Unpress Condition
                self.isPressed = False
                self.thisFrameUnPressed = True

            if self.isHovered and click and not self.isPressed:    # ? Check Pressed Condition
                self.isPressed = True
                self.thisFramePressed = True
            
        if not click: # ? Reset Blocking!
            self.stop = False     
    def kill(self):
        UIM.removeFromQueue(self.elementId)
        del self
    def update(self):
        if self.visible:
            return self.check(self.getAbsPosition(),self.dest)
    
    def getImage(self):
        if not hasattr(self,'surface'):
            self.surface = Surface((1,1))
        return self.surface
    
    def getAbsPosition(self):
        x,y = self.getParentOffsets()
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
    
    def getPosition(self) -> list:
        return self.pos
    
    def getDest(self) -> list:
        return self.dest
    
    def getLayer(self) -> int:
        return self.layer
    
    def getParentOffsets(self) -> list:
        xOffset,yOffset = 0,0
        parent = self.parent
        
        while parent is not None:
            xOffset += parent.pos[0]
            yOffset += parent.pos[1]
            parent = parent.parent
            
        return xOffset,yOffset
    
    def getAllParents(self) -> list[UIElement]:
        parents = []
        parent = self.parent
        while parent is not None:
            parents.append(parent)
            parent = parent.parent
            
        return parents
    
    def getParent(self) -> UIElement:
        return self.parent
    
    def setLayer(self,layer:int) -> None:
        self.layer: int = layer
    
    def setParent(self,parent: UIElement) -> None:
        self.parent: UIElement = parent
    
    def setAnchor(self,position:str) -> None:
        self.anchor: str = position
        
    def setImage(self,surface:Surface) -> None:
        self.surface: Surface = surface
        
    def setCanvas(self,value:Rect) -> None:
        self.canvas: Rect = value
        
    def setVisibility(self,value:bool) -> None:
        self.visible: bool = value
