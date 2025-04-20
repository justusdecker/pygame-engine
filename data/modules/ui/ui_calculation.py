from data.modules.vector import Vector2,Vector4
def get_top_center(size,dest):
    x,y = size[0]//2,0
    w,h = dest[0]//2,0
    return x - w, y - h
def get_center(size,dest):
    x,y = size[0]//2,size[1]//2
    w,h = dest[0]//2,dest[1]//2
    return x - w, y - h
def get_anchor_position(vector:Vector4,type:str) -> Vector4:
    match type:
        case 'top_left':
            return vector
        case 'top_center':
            vector = (vector // Vector4(2,1,2,1))
            print(vector)
            return vector - Vector4()
print(get_anchor_position(Vector4(8,2,7,2),'top_center'))