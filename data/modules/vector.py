class Vector2: x, y = 0,0 # For Documentation only
class Vector2:
    def __init__(self,x=0,y=0):
        self.x, self.y = x, y
    def __add__(self,v:Vector2):
        return Vector2(self.x + v.x,self.y + v.y)
    def __sub__(self,v:Vector2) -> Vector2:
        return Vector2(self.x - v.x,self.y - v.y)
    def __mul__(self,v:Vector2) -> Vector2:
        return Vector2(self.x * v.x,self.y * v.y)
    def __floordiv__(self,v:Vector2) -> Vector2:
        return Vector2((self.x // v.x) if v.x and self.x else 0,(self.y // v.y) if v.y and self.y else 0)
    def __truediv__(self,v:Vector2) -> Vector2:
        return Vector2((self.x / v.x) if v.x and self.x else 0,(self.y / v.y) if v.y and self.y else 0)
    def coords(self) -> tuple[int,int]:
        return self.x, self.y
    def __str__(self):
        return f'Vector2({self.x} {self.y})'

class Vector3: x,y,z = 0,0,0 # For Documentation only
class Vector3:
    def __init__(self,x=0,y=0,z=0):
        self.x, self.y, self.z = x, y, z
    def __add__(self,v:Vector3):
        return Vector3(self.x + v.x,self.y + v.y,(self.z + v.z) if hasattr(v,'z') else self.z)
    def __sub__(self,v:Vector3) -> Vector3:
        return Vector3(self.x - v.x,self.y - v.y,(self.z - v.z) if hasattr(v,'z') else self.z)
    def __mul__(self,v:Vector3) -> Vector3:
        return Vector3(self.x * v.x,self.y * v.y,(self.z * v.z) if hasattr(v,'z') else self.z)
    def __floordiv__(self,v:Vector3) -> Vector3:
        return Vector3((self.x // v.x) if v.x and self.x else 0,(self.y // v.y) if v.y and self.y else 0,((self.z // v.z) if v.z and self.z else 0) if hasattr(v,'z') else self.z)
    def __truediv__(self,v:Vector3) -> Vector3:
        return Vector3((self.x / v.x) if v.x and self.x else 0,(self.y / v.y) if v.y and self.y else 0,((self.z / v.z) if v.z and self.z else 0) if hasattr(v,'z') else self.z)
    def coords(self) -> tuple[int,int,int]:
        return self.x, self.y, self.z
    def __str__(self):
        return f'Vector3({self.x} {self.y} {self.z})'
    
class Vector4: x, y, z, w = 0,0,0,0 # For Documentation only
class Vector4:
    def __init__(self,x=0,y=0,z=0,w=0):
        self.x, self.y, self.z, self.w = x, y, z, w
    def __add__(self,v:Vector4):
        return Vector4(self.x + v.x,self.y + v.y,(self.z + v.z) if hasattr(v,'z') else self.z,(self.w + v.w) if hasattr(v,'w') else self.w)
    def __sub__(self,v:Vector4) -> Vector4:
        return Vector4(self.x - v.x,self.y - v.y,(self.z - v.z) if hasattr(v,'z') else self.z,(self.w - v.w) if hasattr(v,'w') else self.w)
    def __mul__(self,v:Vector4) -> Vector4:
        return Vector4(self.x * v.x,self.y * v.y,(self.z * v.z) if hasattr(v,'z') else self.z,(self.w * v.w) if hasattr(v,'w') else self.w)
    def __floordiv__(self,v:Vector4) -> Vector4:
        return Vector4(self.x // v.x,self.y // v.y,(self.z // v.z) if hasattr(v,'z') else self.z,(self.w // v.w) if hasattr(v,'w') else self.w)
    def __truediv__(self,v:Vector4) -> Vector4:
        return Vector4((self.x / v.x) if v.x and self.x else 0,(self.y / v.y) if v.y and self.y else 0,((self.z / v.z) if v.z and self.z else 0) if hasattr(v,'z') else self.z,((self.w / v.w) if v.w and self.w else 0) if hasattr(v,'w') else self.w)
    def coords(self) -> tuple[int,int,int,int]:
        return self.x, self.y, self.z, self.w
    def __str__(self):
        return f'Vector4({self.x} {self.y} {self.z} {self.w})'