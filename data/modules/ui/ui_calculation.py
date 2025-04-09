def getTopCenter(size,dest):
    x,y = size[0]//2,0
    w,h = dest[0]//2,0
    return x - w, y - h
def getCenter(size,dest):
    x,y = size[0]//2,size[1]//2
    w,h = dest[0]//2,dest[1]//2
    return x - w, y - h
